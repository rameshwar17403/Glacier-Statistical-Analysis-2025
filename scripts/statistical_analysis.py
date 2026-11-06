"""
Comprehensive Statistical Analysis Engine
Author: Antigravity Glacier Statistical Analysis Suite

This module performs statistical evaluations comparing Sentinel-2 and Landsat 8/9:
- Descriptive Statistics (Mean, SD, Median, IQR)
- Pearson & Spearman Correlation
- Ordinary Least Squares (OLS) Linear Regression (Slope, Intercept, R2, p-value, Std Error)
- Error Metrics (RMSE, MAE, Mean Bias Error)
- Normality Verification (Shapiro-Wilk)
- Paired Hypothesis Testing (Paired Student's t-test or Wilcoxon Signed-Rank Test)
- Bland-Altman Agreement Analysis (Mean bias, 95% Limits of Agreement)
- Bootstrap 95% Confidence Intervals
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error
from typing import Dict, List, Tuple, Any

class StatisticalAnalysisEngine:
    """Executes all requested statistical and hypothesis tests."""

    @staticmethod
    def descriptive_stats(data: np.ndarray) -> Dict[str, float]:
        """Calculates central tendency and dispersion metrics."""
        return {
            "mean": float(np.mean(data)),
            "std": float(np.std(data, ddof=1)),
            "median": float(np.median(data)),
            "iqr": float(np.percentile(data, 75) - np.percentile(data, 25)),
            "min": float(np.min(data)),
            "max": float(np.max(data))
        }

    @staticmethod
    def correlation_and_regression(x: np.ndarray, y: np.ndarray) -> Dict[str, float]:
        """
        Computes:
        - Pearson correlation coefficient (r) and p-value
        - Spearman rank correlation (rho)
        - OLS Linear Regression: Slope, Intercept, R-squared, Standard Error, p-value
        - Error metrics: RMSE, MAE, Mean Bias Error (MBE)
        """
        pearson_r, p_val_r = stats.pearsonr(x, y)
        spearman_rho, p_val_rho = stats.spearmanr(x, y)
        
        # Linear regression y = mx + c
        reg = stats.linregress(x, y)
        
        y_pred = reg.slope * x + reg.intercept
        rmse = float(np.sqrt(mean_squared_error(y, y_pred)))
        mae = float(mean_absolute_error(y, y_pred))
        mbe = float(np.mean(y - x)) # Mean Bias Error

        return {
            "pearson_r": float(pearson_r),
            "pearson_p": float(p_val_r),
            "spearman_rho": float(spearman_rho),
            "r_squared": float(reg.rvalue ** 2),
            "slope": float(reg.slope),
            "intercept": float(reg.intercept),
            "std_err": float(reg.stderr),
            "reg_p_value": float(reg.pvalue),
            "rmse": rmse,
            "mae": mae,
            "mbe": mbe
        }

    @staticmethod
    def hypothesis_test_paired(series_a: np.ndarray, series_b: np.ndarray, alpha: float = 0.05) -> Dict[str, Any]:
        """
        Tests whether the paired differences between Sensor A and Sensor B are statistically significant.
        1. Evaluates difference normality via Shapiro-Wilk.
        2. Applies Paired Student's t-test (if normal) OR Wilcoxon signed-rank test (if non-normal).
        3. Computes Cohen's d effect size.
        """
        diff = series_a - series_b
        n = len(diff)
        
        # Test sample size limit for Shapiro-Wilk (max 5000 in scipy)
        sample_diff = diff if n <= 5000 else np.random.choice(diff, 5000, replace=False)
        shapiro_stat, shapiro_p = stats.shapiro(sample_diff)
        is_normal = bool(shapiro_p > alpha)

        if is_normal:
            test_name = "Paired Student's t-test"
            stat, p_val = stats.ttest_rel(series_a, series_b)
        else:
            test_name = "Wilcoxon Signed-Rank Test"
            stat, p_val = stats.wilcoxon(series_a, series_b)

        # Cohen's d effect size
        sd_diff = np.std(diff, ddof=1)
        cohens_d = float(np.mean(diff) / sd_diff) if sd_diff != 0 else 0.0

        return {
            "test_name": test_name,
            "is_normal": is_normal,
            "shapiro_p": float(shapiro_p),
            "statistic": float(stat),
            "p_value": float(p_val),
            "is_significant": bool(p_val < alpha),
            "mean_difference": float(np.mean(diff)),
            "std_difference": float(sd_diff),
            "cohens_d": cohens_d
        }

    @staticmethod
    def bland_altman_analysis(series_a: np.ndarray, series_b: np.ndarray) -> Dict[str, float]:
        """
        Bland-Altman Agreement Analysis:
        - Mean difference (systematic bias): d_bar
        - Limits of Agreement (LoA): [d_bar - 1.96 * s_d, d_bar + 1.96 * s_d]
        - Percentage of observations within 95% LoA
        """
        mean_vals = (series_a + series_b) / 2.0
        diff = series_a - series_b
        mean_diff = float(np.mean(diff))
        std_diff = float(np.std(diff, ddof=1))
        
        loa_upper = float(mean_diff + 1.96 * std_diff)
        loa_lower = float(mean_diff - 1.96 * std_diff)

        in_bounds = np.sum((diff >= loa_lower) & (diff <= loa_upper))
        pct_within_loa = float((in_bounds / len(diff)) * 100.0)

        return {
            "mean_bias": mean_diff,
            "std_diff": std_diff,
            "loa_upper_95": loa_upper,
            "loa_lower_95": loa_lower,
            "pct_within_loa": pct_within_loa
        }

    @staticmethod
    def bootstrap_confidence_interval(data: np.ndarray, n_bootstraps: int = 1000, ci: float = 0.95) -> Tuple[float, float]:
        """Calculates 95% bootstrap confidence interval of the mean."""
        n = len(data)
        boot_means = []
        for _ in range(n_bootstraps):
            sample = np.random.choice(data, size=n, replace=True)
            boot_means.append(np.mean(sample))
        lower = float(np.percentile(boot_means, (1.0 - ci) / 2.0 * 100))
        upper = float(np.percentile(boot_means, (1.0 + ci) / 2.0 * 100))
        return lower, upper

if __name__ == "__main__":
    print("[*] Statistical Analysis Engine module compiled successfully.")
