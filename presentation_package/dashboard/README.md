# Gangotri Glacier Multi-Satellite Analytics Dashboard

An interactive remote-sensing web application built with Streamlit, Plotly, and Folium for comparative statistical analysis of NASA Harmonized Landsat Sentinel-2 (HLS v2 at 30 m) surface reflectance over Gangotri Glacier in 2025.

---

## 🚀 1. Local Run Instructions

### Step 1: Activate the Virtual Environment
```bash
# From the project root
source /Users/rameshwar/.gemini/antigravity/scratch/glacier_statistical_analysis/venv/bin/activate
```

### Step 2: Navigate to Dashboard Directory
```bash
cd /Users/rameshwar/.gemini/antigravity/scratch/glacier_statistical_analysis/presentation_package/dashboard
```

### Step 3: Launch Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## ☁️ 2. Streamlit Community Cloud Deployment Guide

To deploy this interactive dashboard publicly on [Streamlit Community Cloud](https://streamlit.io/cloud):

1. **Push the Dashboard to GitHub:**
   - Create a new public repository (e.g., `gangotri-glacier-dashboard`).
   - Push the contents of the `presentation_package/dashboard/` folder (including `app.py`, `requirements.txt`, `.streamlit/config.toml`, `data/`, and `figures/`).
   
2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
   - Click **"Create app"** &rarr; **"I already have an app"**.
   - Select your repository and branch (`main`).
   - Set **Main file path** to `app.py`.
   - Click **"Deploy!"**.

3. **Zero Configuration Needed:**
   - The application does **not** require Google Earth Engine credentials or environment secrets. All verified 2025 satellite analysis outputs and figures are pre-bundled in the `data/` and `figures/` directories.

---

## 📁 3. Directory Layout
```
dashboard/
├── app.py                      # Core Streamlit multi-page interface
├── requirements.txt            # Minimal pip dependencies for cloud deployment
├── README.md                   # Setup and deployment documentation
├── .streamlit/
│   └── config.toml             # Custom glacier-themed styling
├── data/                       # Pre-bundled CSV outputs (Zero-GEE standalone)
│   ├── spectral_reflectance_statistics.csv
│   ├── glacier_area_summary.csv
│   ├── patch_level_statistical_comparison.csv
│   ├── regression_and_error_metrics.csv
│   └── hypothesis_testing_results.csv
└── figures/                    # Pre-bundled high-resolution figures
    ├── bland_altman_glacier_area.png
    ├── ndsi_regression_scatter.png
    ├── glacier_area_regression_scatter.png
    ├── spatial_discrepancy_map.png
    └── spectral_distributions_violin.png
```
