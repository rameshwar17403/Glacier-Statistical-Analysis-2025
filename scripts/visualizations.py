"""
Publication-Quality Geospatial & Statistical Visualization Suite
Author: Antigravity Glacier Statistical Analysis Suite

This script generates figures and maps for academic papers and project reports:
1. Bland-Altman Glacier Area Agreement Plot
2. Linear Regression & Correlation Scatter Plot (with 1:1 line)
3. Spatial Overlap & Discrepancy Map
4. Spectral Index & Reflectance Distribution (Violin & KDE plots)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Patch
from typing import Dict, Optional

# Publication styling
sns.set_theme(style="ticks")
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.labelsize': 13,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 10,
    'figure.titlesize': 15
})

class GlacierVisualizer:
    """Produces publication-ready charts and comparative maps."""

    @staticmethod
    def plot_bland_altman(series_a: np.ndarray, series_b: np.ndarray, label_a: str, label_b: str, out_path: str, unit: str = "sq. km"):
        """Generates standard Bland-Altman plot with 95% limits of agreement."""
        mean_vals = (series_a + series_b) / 2.0
        diff = series_a - series_b
        mean_diff = np.mean(diff)
        std_diff = np.std(diff, ddof=1)
        loa_upper = mean_diff + 1.96 * std_diff
        loa_lower = mean_diff - 1.96 * std_diff

        fig, ax = plt.subplots(figsize=(8, 6), dpi=300)
        ax.scatter(mean_vals, diff, color="#1d3557", alpha=0.75, edgecolors="white", linewidths=0.8, s=55, zorder=3)
        
        ax.axhline(mean_diff, color="#e63946", linestyle="--", linewidth=1.8, label=f"Mean Bias: {mean_diff:+.3f} {unit}", zorder=2)
        ax.axhline(loa_upper, color="#457b9d", linestyle=":", linewidth=1.5, label=f"+1.96 SD: {loa_upper:+.3f} {unit}", zorder=2)
        ax.axhline(loa_lower, color="#457b9d", linestyle=":", linewidth=1.5, label=f"-1.96 SD: {loa_lower:+.3f} {unit}", zorder=2)
        ax.axhline(0, color="gray", linestyle="-", linewidth=0.8, alpha=0.5, zorder=1)

        ax.set_title(f"Bland-Altman Agreement: Glacier Area ({label_a} vs {label_b})", fontweight="bold", pad=12)
        ax.set_xlabel(f"Mean Estimated Area ({unit})")
        ax.set_ylabel(f"Difference: {label_a} - {label_b} ({unit})")
        ax.legend(loc="upper right", frameon=True, framealpha=0.9)
        
        # Add background span for LoA
        ax.axhspan(loa_lower, loa_upper, color="#a8dadc", alpha=0.15)
        
        sns.despine()
        plt.tight_layout()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path)
        plt.close()
        print(f"[✓] Saved Bland-Altman plot: {out_path}")

    @staticmethod
    def plot_regression(x: np.ndarray, y: np.ndarray, label_x: str, label_y: str, reg_results: Dict[str, float], out_path: str, title: str):
        """Generates scatter plot with fitted regression line and 1:1 identity line."""
        fig, ax = plt.subplots(figsize=(7, 6.5), dpi=300)
        
        # Scatter
        ax.scatter(x, y, color="#2a9d8f", alpha=0.7, edgecolors="k", linewidths=0.5, s=40, label="Paired Observations")

        # 1:1 Line
        min_val = min(np.min(x), np.min(y))
        max_val = max(np.max(x), np.max(y))
        ax.plot([min_val, max_val], [min_val, max_val], color="black", linestyle="--", linewidth=1.2, label="1:1 Identity Line")

        # Regression line
        slope = reg_results["slope"]
        intercept = reg_results["intercept"]
        x_line = np.linspace(min_val, max_val, 100)
        y_line = slope * x_line + intercept
        ax.plot(x_line, y_line, color="#e76f51", linewidth=2.0, label=f"OLS Fit: y = {slope:.3f}x + {intercept:.3f}")

        # Metrics box
        r2 = reg_results["r_squared"]
        r = reg_results["pearson_r"]
        rmse = reg_results["rmse"]
        mae = reg_results["mae"]
        metrics_text = (f"$R^2 = {r2:.4f}$\n"
                        f"Pearson $r = {r:.4f}$\n"
                        f"RMSE = {rmse:.4f}\n"
                        f"MAE = {mae:.4f}")
        
        ax.text(0.05, 0.95, metrics_text, transform=ax.transAxes, fontsize=10.5,
                verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.85, edgecolor='gray'))

        ax.set_title(title, fontweight="bold", pad=12)
        ax.set_xlabel(label_x)
        ax.set_ylabel(label_y)
        ax.legend(loc="lower right", frameon=True)
        
        sns.despine()
        plt.tight_layout()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path)
        plt.close()
        print(f"[✓] Saved Regression plot: {out_path}")

    @staticmethod
    def plot_discrepancy_map(mask_a: np.ndarray, mask_b: np.ndarray, label_a: str, label_b: str, out_path: str):
        """
        Creates a high-contrast 4-category classification overlap map:
        - White: Concordant Glacier Detection (Both detect ice)
        - Cyan: Only Sensor A detected Glacier
        - Orange: Only Sensor B detected Glacier
        - Dark Charcoal: Background / Non-glacier
        """
        h, w = mask_a.shape
        rgb = np.zeros((h, w, 3), dtype=np.uint8)
        
        a = mask_a > 0
        b = mask_b > 0

        both = a & b
        only_a = a & ~b
        only_b = ~a & b
        neither = ~a & ~b

        rgb[neither] = [30, 30, 30]       # Dark Charcoal
        rgb[both] = [255, 255, 255]       # Bright White
        rgb[only_a] = [0, 180, 216]       # Cyan
        rgb[only_b] = [247, 127, 0]       # Orange

        fig, ax = plt.subplots(figsize=(8, 8), dpi=300)
        ax.imshow(rgb)
        ax.set_title(f"Glacier Delineation Spatial Agreement Map\n({label_a} vs. {label_b})", fontweight="bold", pad=12)
        ax.axis("off")

        legend_elements = [
            Patch(facecolor='white', edgecolor='black', label=f'Concordant Glacier ({label_a} ∩ {label_b})'),
            Patch(facecolor='#00b4d8', label=f'Unique to {label_a}'),
            Patch(facecolor='#f77f00', label=f'Unique to {label_b}'),
            Patch(facecolor='#1e1e1e', label='Barren Terrain / Background')
        ]
        ax.legend(handles=legend_elements, loc='lower right', framealpha=0.9, facecolor='white')

        plt.tight_layout()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path)
        plt.close()
        print(f"[✓] Saved Discrepancy map: {out_path}")

    @staticmethod
    def plot_spectral_distributions(df_a: Dict[str, np.ndarray], df_b: Dict[str, np.ndarray],
                                    label_a: str, label_b: str, out_path: str):
        """Compares NDSI, NDVI, Green, and NIR distributions using split violin plots."""
        import pandas as pd
        
        rows = []
        indices = ['ndsi', 'ndvi', 'green', 'nir']
        for idx in indices:
            va = df_a[idx][df_a['valid_mask']]
            vb = df_b[idx][df_b['valid_mask']]
            
            # Subsample for plotting efficiency
            sub_n = min(len(va), len(vb), 5000)
            sub_va = np.random.choice(va, sub_n, replace=False)
            sub_vb = np.random.choice(vb, sub_n, replace=False)

            for v in sub_va:
                rows.append({"Channel": idx.upper(), "Value": float(v), "Sensor": label_a})
            for v in sub_vb:
                rows.append({"Channel": idx.upper(), "Value": float(v), "Sensor": label_b})

        df_plot = pd.DataFrame(rows)

        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
        palette = {label_a: "#2a9d8f", label_b: "#e76f51"}
        
        sns.violinplot(x="Channel", y="Value", hue="Sensor", data=df_plot,
                       split=True, inner="quartile", palette=palette, cut=0, ax=ax)
        
        ax.set_title("Spectral Reflectance and Cryospheric Index Distributions", fontweight="bold", pad=12)
        ax.set_ylabel("Reflectance / Index Value")
        ax.set_xlabel("Spectral Channel / Index")
        ax.legend(loc="upper right", frameon=True)
        
        sns.despine()
        plt.tight_layout()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        plt.savefig(out_path)
        plt.close()
        print(f"[✓] Saved Spectral Distribution violin plot: {out_path}")

if __name__ == "__main__":
    print("[*] Glacier Visualizer module compiled successfully.")
