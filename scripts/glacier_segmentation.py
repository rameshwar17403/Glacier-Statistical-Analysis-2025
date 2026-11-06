"""
Standardized Glacier Mask Generation & Surface Area Computation
Author: Antigravity Glacier Statistical Analysis Suite

This script generates binary glacier masks from harmonized surface reflectance cubes
(Sentinel-2 HLSS30 and Landsat-8/9 HLSL30) and calculates real physical glacier area in sq. km.
"""

import numpy as np
import pandas as pd
from scipy import ndimage
from typing import Dict, Tuple

class GlacierSegmenter:
    """Standardized cryospheric glacier delineator and spatial area calculator."""

    def __init__(self, ndsi_thresh: float = 0.40, nir_thresh: float = 0.11, pixel_res_m: float = 30.0):
        self.ndsi_thresh = ndsi_thresh
        self.nir_thresh = nir_thresh
        self.pixel_res_m = pixel_res_m
        self.pixel_area_km2 = (pixel_res_m ** 2) / 1e6 # 0.0009 km2 for 30m

    def generate_mask(self, processed_cube: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Delineates glacier ice and snow using standard NDSI and NIR reflectance thresholds.
        NDSI >= 0.40 isolates clean snow/ice from rock/soil.
        NIR >= 0.11 avoids deep shadow and water confusion.
        """
        ndsi = processed_cube['ndsi']
        nir = processed_cube['nir']
        valid = processed_cube['valid_mask']

        raw_mask = (ndsi >= self.ndsi_thresh) & (nir >= self.nir_thresh) & valid
        
        # Morphological cleanup: remove single isolated noise pixels and close micro-voids
        cleaned = ndimage.binary_opening(raw_mask, structure=np.ones((2, 2)))
        cleaned = ndimage.binary_closing(cleaned, structure=np.ones((2, 2)))
        return cleaned.astype(np.uint8)

    def calculate_glacier_area(self, mask: np.ndarray, name: str) -> Dict[str, float]:
        """Calculates total pixel count and surface area in square kilometers."""
        pixel_count = int(np.sum(mask > 0))
        area_km2 = float(pixel_count * self.pixel_area_km2)
        return {
            "Sensor": name,
            "Glacier_Pixels": pixel_count,
            "Area_sqkm": area_km2,
            "Resolution_m": self.pixel_res_m
        }

    @staticmethod
    def inter_sensor_agreement(mask_a: np.ndarray, mask_b: np.ndarray, valid_mask: np.ndarray) -> Dict[str, float]:
        """Computes Cohen's Kappa, Jaccard Index (IoU), and spatial overlap fractions."""
        a = mask_a[valid_mask] > 0
        b = mask_b[valid_mask] > 0
        
        tp = np.sum(a & b)
        fp = np.sum(a & ~b) # In A only
        fn = np.sum(~a & b) # In B only
        tn = np.sum(~a & ~b)
        total = len(a)

        iou = tp / (tp + fp + fn + 1e-8)
        dice = (2 * tp) / (2 * tp + fp + fn + 1e-8)

        # Cohen's Kappa
        po = (tp + tn) / total
        p_a = np.sum(a) / total
        p_b = np.sum(b) / total
        pe = (p_a * p_b) + ((1 - p_a) * (1 - p_b))
        kappa = (po - pe) / (1 - pe + 1e-8)

        return {
            "IoU": float(iou),
            "Dice": float(dice),
            "Cohen_Kappa": float(kappa),
            "Overlap_Pixels": int(tp),
            "Only_Sensor_A_Pixels": int(fp),
            "Only_Sensor_B_Pixels": int(fn),
            "Agreement_Percentage": float(po * 100.0)
        }

if __name__ == "__main__":
    print("[*] Glacier Segmenter & Area Calculator module compiled successfully.")
