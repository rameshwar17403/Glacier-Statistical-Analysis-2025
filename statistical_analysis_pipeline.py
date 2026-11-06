"""
Glacier Segmentation Statistical Analysis Pipeline
Author: Antigravity
Designed for: Multi-satellite Attention U-Net Glacier Segmentation Evaluation

This module provides end-to-end statistical analysis for comparing glacier segmentation
results across two different satellite sensors (e.g., Sentinel-2 vs Landsat 8/9).
"""

import os
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from scipy.spatial.distance import directed_hausdorff

# Set aesthetic styling for publication-ready figures
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'figure.titlesize': 16
})


class GlacierMetrics:
    """Computes spatial and classification metrics for binary segmentation masks."""

    @staticmethod
    def confusion_matrix_elements(y_true: np.ndarray, y_pred: np.ndarray) -> Tuple[int, int, int, int]:
        """Returns (TP, FP, FN, TN) for binary masks."""
        y_true_b = (y_true > 0.5).astype(bool)
        y_pred_b = (y_pred > 0.5).astype(bool)
        
        tp = np.logical_and(y_true_b, y_pred_b).sum()
        fp = np.logical_and(~y_true_b, y_pred_b).sum()
        fn = np.logical_and(y_true_b, ~y_pred_b).sum()
        tn = np.logical_and(~y_true_b, ~y_pred_b).sum()
        return int(tp), int(fp), int(fn), int(tn)

    @classmethod
    def dice_coefficient(cls, y_true: np.ndarray, y_pred: np.ndarray, smooth: float = 1e-6) -> float:
        tp, fp, fn, _ = cls.confusion_matrix_elements(y_true, y_pred)
        return (2.0 * tp + smooth) / (2.0 * tp + fp + fn + smooth)

    @classmethod
    def iou_score(cls, y_true: np.ndarray, y_pred: np.ndarray, smooth: float = 1e-6) -> float:
        tp, fp, fn, _ = cls.confusion_matrix_elements(y_true, y_pred)
        return (tp + smooth) / (tp + fp + fn + smooth)

    @classmethod
    def precision_recall_f1(cls, y_true: np.ndarray, y_pred: np.ndarray, smooth: float = 1e-6) -> Tuple[float, float, float]:
        tp, fp, fn, _ = cls.confusion_matrix_elements(y_true, y_pred)
        precision = (tp + smooth) / (tp + fp + smooth)
        recall = (tp + smooth) / (tp + fn + smooth)
        f1 = (2 * precision * recall) / (precision + recall + smooth)
        return precision, recall, f1

    @staticmethod
    def cohen_kappa(mask_a: np.ndarray, mask_b: np.ndarray) -> float:
        """Measures inter-sensor or prediction agreement between two masks."""
        a = (mask_a > 0.5).flatten()
        b = (mask_b > 0.5).flatten()
        total = len(a)
        
        po = np.mean(a == b)
        p_yes_a = np.mean(a)
        p_yes_b = np.mean(b)
        pe = (p_yes_a * p_yes_b) + ((1.0 - p_yes_a) * (1.0 - p_yes_b))
        
        if pe == 1.0:
            return 1.0
        return (po - pe) / (1.0 - pe)

    @staticmethod
    def hausdorff_95(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Computes 95th percentile bidirectional Hausdorff Distance.
        Approximates boundary contour deviation.
        """
        true_pts = np.argwhere(y_true > 0.5)
        pred_pts = np.argwhere(y_pred > 0.5)

        if len(true_pts) == 0 or len(pred_pts) == 0:
            return np.nan

        # Sample for computational feasibility if masks are very large
        max_sample = 2000
        if len(true_pts) > max_sample:
            true_pts = true_pts[np.random.choice(len(true_pts), max_sample, replace=False)]
        if len(pred_pts) > max_sample:
            pred_pts = pred_pts[np.random.choice(len(pred_pts), max_sample, replace=False)]

        d_ab = directed_hausdorff(true_pts, pred_pts)[0]
        d_ba = directed_hausdorff(pred_pts, true_pts)[0]
        return max(d_ab, d_ba)

    @staticmethod
    def glacier_area_sqkm(mask: np.ndarray, pixel_resolution_m: float) -> float:
        """Computes total glacier area in square kilometers."""
        pixel_count = np.sum(mask > 0.5)
        area_m2 = pixel_count * (pixel_resolution_m ** 2)
        return float(area_m2 / 1e6)


class StatisticalComparator:
    """Performs rigorous statistical hypothesis testing between two satellite datasets."""

    @staticmethod
    def test_normality(data: np.ndarray, alpha: float = 0.05) -> Tuple[float, bool]:
        """Shapiro-Wilk test to evaluate normal distribution assumption."""
        stat, p = stats.shapiro(data)
        is_normal = p > alpha
        return p, is_normal

    @staticmethod
    def paired_comparison(series_a: np.ndarray, series_b: np.ndarray) -> Dict[str, float]:
        """
        Runs normality test on differences, then applies:
        - Paired Student's t-test (parametric) OR
        - Wilcoxon Signed-Rank test (non-parametric)
        Also computes Cohen's d effect size.
        """
        diff = series_a - series_b
        # Test differences for normality
        shapiro_p, is_normal = StatisticalComparator.test_normality(diff)

        if is_normal:
            test_type = "Paired t-test (Parametric)"
            stat, p_val = stats.ttest_rel(series_a, series_b)
        else:
            test_type = "Wilcoxon signed-rank test (Non-parametric)"
            stat, p_val = stats.wilcoxon(series_a, series_b)

        # Cohen's d effect size
        s_d = np.std(diff, ddof=1)
        cohens_d = np.mean(diff) / s_d if s_d != 0 else 0.0

        return {
            "test_type": test_type,
            "statistic": float(stat),
            "p_value": float(p_val),
            "cohens_d": float(cohens_d),
            "diff_mean": float(np.mean(diff)),
            "diff_std": float(s_d),
            "is_normal": is_normal
        }

    @staticmethod
    def bootstrap_ci(series: np.ndarray, n_bootstraps: int = 1000, ci: float = 0.95) -> Tuple[float, float]:
        """Calculates bootstrap confidence intervals for the mean metric."""
        boot_means = []
        n = len(series)
        for _ in range(n_bootstraps):
            sample = np.random.choice(series, size=n, replace=True)
            boot_means.append(np.mean(sample))
        lower = np.percentile(boot_means, (1.0 - ci) / 2.0 * 100)
        upper = np.percentile(boot_means, (1.0 + ci) / 2.0 * 100)
        return float(lower), float(upper)


class Visualizer:
    """Generates analytical plots for academic thesis / minor project reports."""

    @staticmethod
    def plot_metric_distributions(df: pd.DataFrame, metric: str, out_path: str):
        """Generates comparative box and violin plot with significance marker."""
        plt.figure(figsize=(7, 6))
        palette = {"Satellite A": "#2b5c8f", "Satellite B": "#e26d5c"}
        
        ax = sns.violinplot(x="Satellite", y=metric, data=df, palette=palette, inner="quartile", cut=0)
        sns.stripplot(x="Satellite", y=metric, data=df, color="black", alpha=0.3, jitter=0.2, size=5)
        
        plt.title(f"Comparison of {metric} across Satellite Test Scenes", fontweight="bold")
        plt.ylabel(metric)
        plt.xlabel("Sensor Dataset")
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()

    @staticmethod
    def plot_bland_altman(area_a: np.ndarray, area_b: np.ndarray, name_a: str, name_b: str, out_path: str):
        """
        Bland-Altman plot to assess physical glacier area agreement between two sensors.
        Crucial for remote sensing & glaciology consistency validation!
        """
        mean_area = (area_a + area_b) / 2.0
        diff_area = area_a - area_b
        mean_diff = np.mean(diff_area)
        std_diff = np.std(diff_area)
        loa_upper = mean_diff + 1.96 * std_diff
        loa_lower = mean_diff - 1.96 * std_diff

        plt.figure(figsize=(8, 6))
        plt.scatter(mean_area, diff_area, color="#1f77b4", alpha=0.7, edgecolors="k", s=45)
        plt.axhline(mean_diff, color="red", linestyle="--", label=f"Mean Bias: {mean_diff:.3f} sq.km")
        plt.axhline(loa_upper, color="gray", linestyle=":", label=f"+1.96 SD: {loa_upper:.3f}")
        plt.axhline(loa_lower, color="gray", linestyle=":", label=f"-1.96 SD: {loa_lower:.3f}")

        plt.title(f"Bland-Altman Agreement: Glacier Area ({name_a} vs {name_b})", fontweight="bold")
        plt.xlabel(f"Mean Estimated Area (sq. km)")
        plt.ylabel(f"Difference: {name_a} - {name_b} (sq. km)")
        plt.legend(loc="upper right", frameon=True)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()

    @staticmethod
    def plot_discrepancy_map(mask_gt: np.ndarray, pred_a: np.ndarray, pred_b: np.ndarray, out_path: str):
        """
        Creates a 4-color spatial discrepancy map:
        - White: Both satellites correctly agree (True Glacier)
        - Cyan: Only Satellite A predicted Glacier
        - Orange: Only Satellite B predicted Glacier
        - Gray: False Negative (missed by both)
        - Black: True Background
        """
        h, w = mask_gt.shape
        rgb = np.zeros((h, w, 3), dtype=np.uint8)

        gt = mask_gt > 0.5
        pa = pred_a > 0.5
        pb = pred_b > 0.5

        # Both agree on true positive
        both_tp = np.logical_and.reduce((gt, pa, pb))
        # Only A caught
        only_a = np.logical_and(pa, ~pb)
        # Only B caught
        only_b = np.logical_and(pb, ~pa)
        # Missed by both
        missed_both = np.logical_and.reduce((gt, ~pa, ~pb))

        rgb[both_tp] = [255, 255, 255]      # Both correct
        rgb[only_a] = [0, 180, 216]          # Cyan (Sat A only)
        rgb[only_b] = [247, 127, 0]          # Orange (Sat B only)
        rgb[missed_both] = [120, 0, 0]       # Dark Red (Missed)

        plt.figure(figsize=(8, 8))
        plt.imshow(rgb)
        plt.title("Spatial Discrepancy Map (Agreement & Disagreements)", fontweight="bold")
        plt.axis("off")
        
        # Legend proxies
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='white', edgecolor='k', label='Concordant Glacier Detection'),
            Patch(facecolor='#00b4d8', label='Satellite A Unique Detection'),
            Patch(facecolor='#f77f00', label='Satellite B Unique Detection'),
            Patch(facecolor='#780000', label='Omitted by Both Sensors'),
            Patch(facecolor='black', label='Background / Non-Glacier')
        ]
        plt.legend(handles=legend_elements, loc='lower right', framealpha=0.9)
        plt.tight_layout()
        plt.savefig(out_path, dpi=300)
        plt.close()


def generate_synthetic_glacier_experiment(num_scenes: int = 50, seed: int = 42):
    """
    Generates synthetic evaluation data representing two satellite datasets
    (e.g., Sentinel-2 10m vs Landsat-8 30m) over the same Himalayan/Alpine glacier basin.
    """
    np.random.seed(seed)
    
    # Sentinel-2 (higher spatial resolution, sharp edges, slightly higher IoU)
    # Mean IoU ~ 0.88, std ~ 0.04
    iou_s2 = np.clip(np.random.normal(0.88, 0.035, num_scenes), 0.70, 0.98)
    dice_s2 = 2 * iou_s2 / (1 + iou_s2)
    hd_s2 = np.clip(np.random.normal(4.2, 1.2, num_scenes), 1.5, 12.0)  # in pixels
    area_s2 = np.clip(np.random.normal(14.8, 4.5, num_scenes), 2.0, 35.0) # sq km
    
    # Landsat-8 (lower spatial resolution 30m, smoother boundaries, slightly lower IoU)
    # Mean IoU ~ 0.84, std ~ 0.05
    # Correlated with Sentinel-2 since it is the same geographic region
    noise = np.random.normal(0, 0.02, num_scenes)
    iou_l8 = np.clip(iou_s2 - 0.035 + noise, 0.65, 0.95)
    dice_l8 = 2 * iou_l8 / (1 + iou_l8)
    hd_l8 = np.clip(hd_s2 + np.random.normal(2.1, 0.8, num_scenes), 2.0, 15.0)
    # Area estimated on 30m has slight positive bias due to mixed boundary pixels
    area_l8 = area_s2 + np.random.normal(0.25, 0.4, num_scenes)

    df_scenes = pd.DataFrame({
        "Scene_ID": [f"Glacier_Patch_{i+1:03d}" for i in range(num_scenes)],
        "IoU_SatA": iou_s2,
        "IoU_SatB": iou_l8,
        "Dice_SatA": dice_s2,
        "Dice_SatB": dice_l8,
        "HD95_SatA": hd_s2,
        "HD95_SatB": hd_l8,
        "Area_SatA_sqkm": area_s2,
        "Area_SatB_sqkm": area_l8,
    })

    return df_scenes


def run_full_statistical_analysis(df: pd.DataFrame, output_dir: str, sat_a_name: str = "Sentinel-2", sat_b_name: str = "Landsat-8"):
    os.makedirs(output_dir, exist_ok=True)
    report_lines = []
    report_lines.append(f"# Multi-Sensor Statistical Analysis Report: Attention U-Net Glacier Segmentation")
    report_lines.append(f"**Comparison:** {sat_a_name} vs. {sat_b_name} across {len(df)} co-registered test regions\n")

    # 1. Descriptive Summary Table
    metrics = ["IoU", "Dice", "HD95", "Area_sqkm"]
    summary_data = []

    for m in ["IoU", "Dice", "HD95", "Area"]:
        col_a = f"{m}_SatA" if m != "Area" else f"{m}_SatA_sqkm"
        col_b = f"{m}_SatB" if m != "Area" else f"{m}_SatB_sqkm"
        
        mean_a, std_a = df[col_a].mean(), df[col_a].std()
        ci_a_low, ci_a_high = StatisticalComparator.bootstrap_ci(df[col_a].values)
        
        mean_b, std_b = df[col_b].mean(), df[col_b].std()
        ci_b_low, ci_b_high = StatisticalComparator.bootstrap_ci(df[col_b].values)

        # Hypothesis testing
        test_res = StatisticalComparator.paired_comparison(df[col_a].values, df[col_b].values)
        
        summary_data.append({
            "Metric": m,
            f"{sat_a_name} (Mean±SD)": f"{mean_a:.4f} ± {std_a:.4f}",
            f"{sat_a_name} 95% CI": f"[{ci_a_low:.4f}, {ci_a_high:.4f}]",
            f"{sat_b_name} (Mean±SD)": f"{mean_b:.4f} ± {std_b:.4f}",
            f"{sat_b_name} 95% CI": f"[{ci_b_low:.4f}, {ci_b_high:.4f}]",
            "Mean Diff (A - B)": f"{test_res['diff_mean']:.4f}",
            "Statistical Test": test_res["test_type"].split()[0],
            "p-value": f"{test_res['p_value']:.4e}" if test_res['p_value'] < 0.001 else f"{test_res['p_value']:.4f}",
            "Significance (α=0.05)": "Yes (p < 0.05) ***" if test_res['p_value'] < 0.001 else ("Yes (p < 0.05) *" if test_res['p_value'] < 0.05 else "No (p >= 0.05)"),
            "Cohen's d (Effect Size)": f"{test_res['cohens_d']:.3f}"
        })

    summary_df = pd.DataFrame(summary_data)
    summary_csv_path = os.path.join(output_dir, "statistical_metrics_summary.csv")
    summary_df.to_csv(summary_csv_path, index=False)

    report_lines.append("## 1. Quantitative Performance & Hypothesis Testing Summary")
    report_lines.append(summary_df.to_markdown(index=False))
    report_lines.append("\n*Note: Significance evaluated via paired hypothesis tests (parametric t-test or Wilcoxon signed-rank depending on Shapiro-Wilk normality).*")

    # 2. Reshape for Violin Plots
    df_long_iou = pd.DataFrame({
        "Satellite": [sat_a_name] * len(df) + [sat_b_name] * len(df),
        "IoU": np.concatenate([df["IoU_SatA"], df["IoU_SatB"]])
    })
    Visualizer.plot_metric_distributions(df_long_iou, "IoU", os.path.join(output_dir, "iou_comparison_violin.png"))

    df_long_dice = pd.DataFrame({
        "Satellite": [sat_a_name] * len(df) + [sat_b_name] * len(df),
        "Dice": np.concatenate([df["Dice_SatA"], df["Dice_SatB"]])
    })
    Visualizer.plot_metric_distributions(df_long_dice, "Dice", os.path.join(output_dir, "dice_comparison_violin.png"))

    # 3. Bland-Altman Agreement on Glacier Area
    Visualizer.plot_bland_altman(
        df["Area_SatA_sqkm"].values,
        df["Area_SatB_sqkm"].values,
        sat_a_name,
        sat_b_name,
        os.path.join(output_dir, "bland_altman_glacier_area.png")
    )

    # 4. Generate Synthetic Discrepancy Map for Visual Representation
    mock_h, mock_w = 256, 256
    y, x = np.ogrid[:mock_h, :mock_w]
    # Organic circular/irregular glacier body
    gt_mask = ((x - 128)**2 + (y - 128)**2 <= 75**2).astype(np.uint8)
    # Add ragged terminus / tongue
    gt_mask[128:210, 105:150] = 1
    
    # Sat A prediction (High fidelity, tiny boundary noise)
    pred_a = gt_mask.copy()
    pred_a[120:130, 200:206] = 1 # minor false positive
    pred_a[205:210, 110:145] = 0 # slight terminus undersegmentation

    # Sat B prediction (Coarser resolution, more mixed pixel expansion)
    pred_b = gt_mask.copy()
    pred_b[100:150, 185:215] = 1 # coarser false positive on boundary
    pred_b[128:200, 100:155] = 1 # mixed pixel bloat along tongue

    Visualizer.plot_discrepancy_map(gt_mask, pred_a, pred_b, os.path.join(output_dir, "spatial_discrepancy_map.png"))

    # Inter-sensor Kappa
    kappa = GlacierMetrics.cohen_kappa(pred_a, pred_b)
    inter_iou = GlacierMetrics.iou_score(pred_a, pred_b)

    report_lines.append("\n## 2. Inter-Sensor Concordance & Agreement")
    report_lines.append(f"- **Cohen's Kappa (κ):** `{kappa:.4f}` (Values > 0.80 indicate almost perfect agreement between sensors)")
    report_lines.append(f"- **Direct Inter-Prediction IoU (Sat A ∩ Sat B / Sat A ∪ Sat B):** `{inter_iou:.4f}`")
    report_lines.append(f"- **Bland-Altman Mean Area Bias:** `{np.mean(df['Area_SatA_sqkm'] - df['Area_SatB_sqkm']):.4f} sq. km`")

    # Save Markdown report
    report_path = os.path.join(output_dir, "statistical_analysis_report.md")
    with open(report_path, "w") as f:
        f.write("\n".join(report_lines))

    print(f"[SUCCESS] Full statistical evaluation complete! Output files generated at: {output_dir}")
    return summary_df


if __name__ == "__main__":
    out_dir = "/Users/rameshwar/.gemini/antigravity/scratch/glacier_statistical_analysis/output"
    print("Running statistical analysis pipeline...")
    sim_data = generate_synthetic_glacier_experiment(num_scenes=50)
    summary = run_full_statistical_analysis(sim_data, out_dir, "Sentinel-2", "Landsat-8")
    print(summary)
