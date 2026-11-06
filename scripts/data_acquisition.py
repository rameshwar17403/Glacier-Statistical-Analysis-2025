"""
NASA HLS v2 Data Acquisition Script (Sentinel-2 HLSS30 & Landsat-8/9 HLSL30)
Author: Antigravity Glacier Statistical Analysis Suite

This script searches, filters, and downloads Harmonized Landsat Sentinel-2 (HLS v2)
surface reflectance observations for the defined glacier study area during the 2025 ablation season.
"""

import os
import sys
import yaml
import argparse

def acquire_hls_scenes(config_path: str = "config/study_area.yaml", dry_run: bool = False):
    with open(config_path, "r") as f:
        cfg = yaml.safe_load(f)

    glacier_name = cfg["glacier"]["name"]
    bbox = cfg["glacier"]["coordinates"]["bbox"]
    start_date = cfg["temporal"]["ablation_season"]["start_date"]
    end_date = cfg["temporal"]["ablation_season"]["end_date"]
    max_cloud = cfg["temporal"]["cloud_threshold_percent"]

    print("=" * 65)
    print(f"🛰️ NASA HLS v2 2025 DATA ACQUISITION: {glacier_name}")
    print("=" * 65)
    print(f"Target Bounding Box: {bbox} [min_lon, min_lat, max_lon, max_lat]")
    print(f"Temporal Window:     {start_date} to {end_date}")
    print(f"Max Cloud Threshold: {max_cloud}%")
    print("-" * 65)

    try:
        import ee
        # Check if initialized
        roi = ee.Geometry.BBox(bbox[0], bbox[1], bbox[2], bbox[3])
    except Exception as e:
        print(f"[!] GEE not initialized: {e}")
        print("[*] Please run 'python scripts/01_gee_auth.py --project <YOUR_PROJECT_ID>' first.")
        return None

    # Query Sentinel-2 (HLSS30)
    print("\n[1/2] Querying NASA/HLS/HLSS30/v002 (Sentinel-2 Harmonized)...")
    s30_col = (ee.ImageCollection("NASA/HLS/HLSS30/v002")
               .filterBounds(roi)
               .filterDate(start_date, end_date)
               .filter(ee.Filter.lt("CLOUD_COVERAGE", max_cloud))
               .sort("CLOUD_COVERAGE"))

    s30_size = s30_col.size().getInfo()
    print(f"  Found {s30_size} candidate Sentinel-2 scenes with cloud cover < {max_cloud}%")

    # Query Landsat (HLSL30)
    print("\n[2/2] Querying NASA/HLS/HLSL30/v002 (Landsat 8/9 Harmonized)...")
    l30_col = (ee.ImageCollection("NASA/HLS/HLSL30/v002")
               .filterBounds(roi)
               .filterDate(start_date, end_date)
               .filter(ee.Filter.lt("CLOUD_COVERAGE", max_cloud))
               .sort("CLOUD_COVERAGE"))

    l30_size = l30_col.size().getInfo()
    print(f"  Found {l30_size} candidate Landsat 8/9 scenes with cloud cover < {max_cloud}%")

    if s30_size == 0 or l30_size == 0:
        print("[WARNING] Zero candidate scenes found within the strict cloud threshold.")
        print("Relaxing temporal window or cloud threshold may be required.")
        return None

    # Fetch top candidate metadata
    best_s30 = ee.Image(s30_col.first())
    best_l30 = ee.Image(l30_col.first())

    s30_meta = best_s30.getInfo()
    l30_meta = best_l30.getInfo()

    s30_date = s30_meta['properties'].get('system:time_start', 'N/A')
    l30_date = l30_meta['properties'].get('system:time_start', 'N/A')
    
    print("\n" + "=" * 65)
    print("🏆 BEST CO-TEMPORAL SCENE PAIR SELECTED:")
    print(f"Sentinel-2 (HLSS30): ID = {s30_meta['id']}, Cloud = {s30_meta['properties'].get('CLOUD_COVERAGE', 'N/A')}%")
    print(f"Landsat (HLSL30):    ID = {l30_meta['id']}, Cloud = {l30_meta['properties'].get('CLOUD_COVERAGE', 'N/A')}%")
    print("=" * 65)

    return {
        "s30_image": best_s30,
        "l30_image": best_l30,
        "roi": roi,
        "s30_id": s30_meta['id'],
        "l30_id": l30_meta['id']
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query NASA HLS 2025 imagery")
    parser.add_argument("--config", type=str, default="config/study_area.yaml")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    acquire_hls_scenes(args.config, args.dry_run)
