"""
NASA HLS Preprocessing, QA Masking & Spectral Index Pipeline
Author: Antigravity Glacier Statistical Analysis Suite

This script processes NASA HLS surface reflectance tiles:
1. Applies precise Fmask QA cloud and shadow filtering without omitting snow/ice.
2. Applies 0.0001 radiometric scale factor.
3. Computes physical indices: NDSI and NDVI.
4. Generates comparative spectral reflectance statistics for valid pixels.
"""

import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional

class HLSPreprocessor:
    """Handles radiometric scaling, cloud/shadow masking, and cryospheric index calculations."""

    @staticmethod
    def decode_fmask(fmask: np.ndarray) -> np.ndarray:
        """
        Decodes NASA HLS Fmask QA band:
        Bit 0: Cirrus cloud
        Bit 1: Cloud
        Bit 2: Adjacent to cloud / shadow
        Bit 3: Cloud shadow
        Bit 4: Snow / Ice (DO NOT MASK)
        Bit 5: Water
        
        Returns:
            valid_mask (bool np.ndarray): True for clean, unobstructed terrain / ice.
        """
        fmask_int = fmask.astype(np.uint8)
        
        cirrus = (fmask_int >> 0) & 1
        cloud = (fmask_int >> 1) & 1
        adjacent = (fmask_int >> 2) & 1
        shadow = (fmask_int >> 3) & 1
        
        # Obscured pixels
        obscured = (cirrus | cloud | adjacent | shadow).astype(bool)
        
        # Valid terrain and ice pixels
        valid_mask = ~obscured
        return valid_mask

    @staticmethod
    def scale_reflectance(band_data: np.ndarray, scale_factor: float = 0.0001) -> np.ndarray:
        """Scales raw integer DNs to [0.0, 1.0] surface reflectance."""
        scaled = band_data.astype(np.float32) * scale_factor
        return np.clip(scaled, 0.0, 1.0)

    @staticmethod
    def compute_ndsi(green: np.ndarray, swir1: np.ndarray, eps: float = 1e-8) -> np.ndarray:
        """
        Normalized Difference Snow Index:
        NDSI = (Green - SWIR1) / (Green + SWIR1 + eps)
        """
        numerator = green - swir1
        denominator = green + swir1 + eps
        ndsi = numerator / denominator
        return np.clip(ndsi, -1.0, 1.0)

    @staticmethod
    def compute_ndvi(nir: np.ndarray, red: np.ndarray, eps: float = 1e-8) -> np.ndarray:
        """
        Normalized Difference Vegetation Index:
        NDVI = (NIR - Red) / (NIR + Red + eps)
        """
        numerator = nir - red
        denominator = nir + red + eps
        ndvi = numerator / denominator
        return np.clip(ndvi, -1.0, 1.0)

    @classmethod
    def process_scene_cube(cls, bands: Dict[str, np.ndarray], fmask: np.ndarray) -> Dict[str, np.ndarray]:
        """
        Takes raw band dict (blue, green, red, nir, swir1, swir2) and fmask.
        Returns scaled bands, NDSI, NDVI, and the valid mask.
        """
        valid_mask = cls.decode_fmask(fmask)
        
        scaled_bands = {}
        for b_name, b_arr in bands.items():
            scaled_bands[b_name] = cls.scale_reflectance(b_arr)

        ndsi = cls.compute_ndsi(scaled_bands['green'], scaled_bands['swir1'])
        ndvi = cls.compute_ndvi(scaled_bands['nir'], scaled_bands['red'])

        processed = {
            **scaled_bands,
            'ndsi': ndsi,
            'ndvi': ndvi,
            'valid_mask': valid_mask
        }
        return processed

    @staticmethod
    def compute_spectral_statistics(processed: Dict[str, np.ndarray], sensor_label: str) -> pd.DataFrame:
        """Calculates descriptive summary statistics for all channels across cloud-free pixels."""
        valid = processed['valid_mask']
        stats_rows = []

        channel_keys = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'ndsi', 'ndvi']
        for ch in channel_keys:
            vals = processed[ch][valid]
            stats_rows.append({
                "Sensor": sensor_label,
                "Band_Index": ch.upper(),
                "Mean": float(np.mean(vals)),
                "Std": float(np.std(vals)),
                "Median": float(np.median(vals)),
                "IQR": float(np.percentile(vals, 75) - np.percentile(vals, 25)),
                "Min": float(np.min(vals)),
                "Max": float(np.max(vals)),
                "Valid_Pixels": int(np.sum(valid))
            })

        return pd.DataFrame(stats_rows)

if __name__ == "__main__":
    print("[*] HLS Preprocessor module compiled successfully.")
