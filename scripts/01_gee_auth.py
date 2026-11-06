"""
Google Earth Engine Authentication & Diagnostic Verification Script
Author: Antigravity Glacier Statistical Analysis Suite

This script authenticates with Google Earth Engine (GEE), verifies the active
cloud project, and validates access to NASA HLS v2 collections.
"""

import sys
import argparse
import yaml

def verify_gee_connection(project_id: str = None):
    try:
        import ee
    except ImportError:
        print("[ERROR] 'earthengine-api' package is not installed.")
        print("Please run: pip install earthengine-api")
        sys.exit(1)

    print("=" * 65)
    print("🌍 GOOGLE EARTH ENGINE AUTHENTICATION & DIAGNOSTIC CHECK")
    print("=" * 65)

    # 1. Try to initialize
    try:
        if project_id:
            print(f"[*] Attempting ee.Initialize with Cloud Project: '{project_id}'...")
            ee.Initialize(project=project_id)
        else:
            print("[*] Attempting ee.Initialize with default credentials...")
            ee.Initialize()
        print("[SUCCESS] Successfully connected and initialized Earth Engine API!")
    except Exception as init_err:
        print(f"[!] Initialization failed: {init_err}")
        print("\n[*] Starting interactive authentication flow...")
        try:
            ee.Authenticate()
            if project_id:
                ee.Initialize(project=project_id)
            else:
                ee.Initialize()
            print("[SUCCESS] Authentication and initialization complete!")
        except Exception as auth_err:
            print(f"[ERROR] Failed to authenticate: {auth_err}")
            print("\nPlease ensure your Google Account has an active Google Cloud Project")
            print("registered for Earth Engine at: https://code.earthengine.google.com/")
            sys.exit(1)

    # 2. Test NASA HLS Dataset Access
    print("\n[*] Checking access to NASA HLS v2 Collections in Earth Engine...")
    try:
        s2_col = ee.ImageCollection("NASA/HLS/HLSS30/v002")
        l8_col = ee.ImageCollection("NASA/HLS/HLSL30/v002")
        
        s2_count = s2_col.filterDate("2025-08-01", "2025-08-10").size().getInfo()
        l8_count = l8_col.filterDate("2025-08-01", "2025-08-10").size().getInfo()
        
        print(f"  [✓] NASA/HLS/HLSS30/v002 accessible! (Sample count: {s2_count})")
        print(f"  [✓] NASA/HLS/HLSL30/v002 accessible! (Sample count: {l8_count})")
        print("=" * 65)
        print("🎉 All Earth Engine connections and satellite collections verified!")
        print("=" * 65)
        return True
    except Exception as query_err:
        print(f"[WARNING] Could not query HLS collections: {query_err}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Authenticate and verify GEE access")
    parser.add_argument("--project", type=str, default=None, help="Google Cloud Project ID")
    parser.add_argument("--config", type=str, default="config/study_area.yaml", help="Path to config")
    args = parser.parse_args()

    project = args.project
    if not project:
        try:
            with open(args.config, "r") as f:
                cfg = yaml.safe_load(f)
                project = cfg.get("gee", {}).get("project_id", None)
        except Exception:
            pass

    verify_gee_connection(project)
