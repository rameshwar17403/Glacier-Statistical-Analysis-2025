# 🧊 Multi-Satellite Glacier Statistical Analysis (2025)

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg?style=flat&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg?style=flat&logo=streamlit)](https://streamlit.io/)
[![Earth Engine](https://img.shields.io/badge/Google%20Earth%20Engine-API-brightgreen.svg?style=flat&logo=googleearth)](https://earthengine.google.com/)
[![NASA HLS](https://img.shields.io/badge/NASA%20HLS-v002-orange.svg)](https://hls.gsfc.nasa.gov/)

A publication-grade remote-sensing and statistical evaluation suite comparing **Copernicus Sentinel-2** and **Landsat 8/9** surface reflectance observations over the **Gangotri Glacier Basin (Garhwal Himalaya, Uttarakhand, India)** during the 2025 ablation season.

- **Academic Context:** B.Tech Information Technology (7th Semester Minor Project), National Institute of Technology (NIT) Raipur.
- **Authors:** Rameshwar Chandravanshi • Piyush Verma • Deepanshu Sahu.
- **Upstream Framework:** Extension to the [8-Channel Attention U-Net Glacier Segmentation Framework](https://github.com/Piyushhvrma/Attention-U-Net-Glacier-Segmentation).

---

## 📑 Table of Contents

1. [Project Overview & Scientific Motivation](#-project-overview--scientific-motivation)
2. [Study Area: Gangotri Glacier Basin](#-study-area-gangotri-glacier-basin)
3. [Satellite Datasets: NASA HLS v2 Harmonization](#-satellite-datasets-nasa-hls-v2-harmonization)
4. [Methodology & Mathematical Formulations](#-methodology--mathematical-formulations)
5. [Key Quantitative Results & Verification](#-key-quantitative-results--verification)
6. [Repository Structure](#-repository-structure)
7. [Installation & Setup](#-installation--setup)
8. [Running the Statistical Pipeline](#-running-the-statistical-pipeline)
9. [Interactive Web Dashboard (Streamlit)](#-interactive-web-dashboard-streamlit)
10. [Academic Deliverables (PDF & PPTX)](#-academic-deliverables-pdf--pptx)
11. [Data Attribution & References](#-data-attribution--references)
12. [License](#-license)

---

## 🔭 1. Project Overview & Scientific Motivation

Automated semantic segmentation models (such as our 8-channel Attention U-Net) enable regional glacier mapping. However, multi-decadal retreat analysis requires fusing observations from divergent orbital sensors. Differences in optical bandwidths, orbits, and atmospheric response functions introduce radiometric offsets that risk being erroneously interpreted as physical retreat if not rigorously calibrated.

This project delivers a complete, reproducible statistical evaluation answering:
* **Radiometric Consistency:** How closely do surface reflectance and spectral indices (NDSI/NDVI) align between Sentinel-2 (MSI) and Landsat 8/9 (OLI)?
* **Boundary Concordance:** Does sensor spatial resolution introduce significant boundary discrepancies along debris-covered margins?
* **Statistical Interchangeability:** Does high correlation imply agreement? (Evaluated via OLS regression, Wilcoxon signed-rank testing, and Bland-Altman limits of agreement).

---

## 🏔️ 2. Study Area: Gangotri Glacier Basin

* **Geographical Region:** Garhwal Himalaya, Uttarkashi District, Uttarakhand, India.
* **Inventory Classification:** Randolph Glacier Inventory (RGI 7.0/6.0 Region 14: South Asia West).
* **Coordinates (WGS84):** `[79.05°E, 30.80°N, 79.30°E, 31.05°N]` | **Reference Grid:** UTM Zone 44N.
* **Morphology:** Valley glacier (~30 km length, 2 to 4 km width), spanning 4,000 m a.s.l. (Gaumukh snout) to >7,100 m a.s.l. (Chaukhamba accumulation basin).
* **Observation Target:** 2025 Ablation Season (August 1 – October 31) to isolate true glacier ice from transient seasonal winter snow.

---

## 🛰️ 3. Satellite Datasets: NASA HLS v2 Harmonization

We utilize the **NASA Harmonized Landsat Sentinel-2 (HLS v2)** at 30-meter spatial resolution:
* **HLSS30 v002:** Copernicus Sentinel-2A/2B MultiSpectral Instrument (MSI).
* **HLSL30 v002:** Landsat 8/9 Operational Land Imager (OLI).

### Spectral Band Cross-Alignment

| Spectral Channel | Sentinel-2 (HLSS30) | Landsat 8/9 (HLSL30) | Central Wavelength | Cryospheric Role |
| :---: | :---: | :---: | :---: | :--- |
| **Blue** | Band `B02` | Band `B02` | ~490 nm | Atmospheric correction & clear water penetration |
| **Green** | Band `B03` | Band `B03` | ~560 nm | Visible ice reflectance peak; NDSI numerator |
| **Red** | Band `B04` | Band `B04` | ~665 nm | Chlorophyll absorption; NDVI denominator |
| **NIR** | Band `B8A` (Narrow) | Band `B05` | ~865 nm | Clean snow reflectance; NDVI numerator |
| **SWIR1** | Band `B11` | Band `B06` | ~1610 nm | Strong ice absorption band; NDSI denominator |
| **SWIR2** | Band `B12` | Band `B07` | ~2200 nm | Distinguishes ice from lateral moraine bedrock |

---

## 📐 4. Methodology & Mathematical Formulations

### 4.1. Fmask Cloud QA Bitmask Filtering
To prevent automated cloud algorithms from erroneously deleting high-albedo glacier ice, we decode individual bits from the HLS `Fmask` layer:
$$\text{Mask}_{\text{invalid}} = \text{Bit}_0 (\text{Cirrus}) \lor \text{Bit}_1 (\text{Cloud}) \lor \text{Bit}_2 (\text{Adjacent Cloud}) \lor \text{Bit}_3 (\text{Shadow})$$
* **Bit 4 (Snow/Ice)** is **explicitly preserved and protected**.

### 4.2. Cryospheric Indices
$$\text{NDSI} = \frac{\rho_{\text{Green}} - \rho_{\text{SWIR1}}}{\rho_{\text{Green}} + \rho_{\text{SWIR1}} + \epsilon}, \quad \text{NDVI} = \frac{\rho_{\text{NIR}} - \rho_{\text{Red}}}{\rho_{\text{NIR}} + \rho_{\text{Red}} + \epsilon}$$

### 4.3. Standardized Glacier Delineation
Binary glacier masks are extracted via $\text{NDSI} \ge 0.40$ and $\text{NIR} \ge 0.11$ (eliminating deep mountain shadows and water bodies), followed by morphological opening and closing to remove isolated speckle noise.

### 4.4. Bland-Altman Agreement Analysis
$$\bar{d} = \frac{1}{N}\sum_{i=1}^N (A_i - B_i), \quad \text{LoA}_{95\%} = [\bar{d} - 1.96 s_d, \; \bar{d} + 1.96 s_d]$$

---

## 📊 5. Key Quantitative Results & Verification

All results are computed from the verified 2025 satellite observation outputs over the Gangotri catchment:

```
========================================================================================
           VERIFIED MULTI-SATELLITE STATISTICAL FINDINGS (GANGOTRI 2025)
========================================================================================
Evaluation Metric                   Sentinel-2 (HLSS30)    Landsat 8/9 (HLSL30)   Concordance
----------------------------------------------------------------------------------------
Total Glacier Extent (km²)          17.429 km²             16.329 km²             Δ = 1.101 km² (6.32%)
Cohen's Kappa (κ)                   —                      —                      0.8967 (Almost Perfect)
Jaccard Similarity Index (IoU)      —                      —                      0.8252
Dice Similarity Coefficient (F1)    —                      —                      0.9042
Total Pixel Concordance (%)         —                      —                      98.61%
NDSI Pearson Correlation (r)        —                      —                      0.9937 (p < 10⁻¹⁰⁰)
NDSI OLS Regression (R²)            —                      —                      0.9875 (Slope = 1.006)
NDSI RMSE / MAE                     —                      —                      RMSE = 0.0410 | MAE = 0.0322
Catchment Area Pearson r            —                      —                      0.9977 (p = 5.37 × 10⁻⁷³)
Catchment Area OLS Regression (R²)  —                      —                      0.9954 (Slope = 0.984)
Hypothesis Test (Area Difference)   —                      —                      Wilcoxon p = 0.00065*
Cohen's d Effect Size               —                      —                      0.4201 (Small/Moderate)
Bland-Altman Mean Bias (d̄)         —                      —                      +0.0175 km²
Bland-Altman 95% Limits of Agrmt    —                      —                      [-0.064 km², +0.099 km²]
Proportion within 95% LoA           —                      —                      92.1%
95% Bootstrap CI for Area (km²)     [0.139, 0.440]         [0.124, 0.427]         Overlapping CI
========================================================================================
```

---

## 📁 6. Repository Structure

```
Glacier-Statistical-Analysis-2025/
├── config/
│   └── study_area.yaml             # Coordinates, sensor IDs, time windows
├── scripts/
│   ├── gee_auth.py                 # Earth Engine initialization & project verification
│   ├── data_acquisition.py         # NASA HLS S30 & L30 query & export
│   ├── preprocessing.py            # Fmask QA bitmask filter & NDSI/NDVI indices
│   ├── glacier_segmentation.py     # Mask generation & area calculation (km²)
│   ├── statistical_analysis.py     # Hypothesis testing, OLS regression, Bland-Altman
│   ├── visualizations.py           # Publication-ready plots & discrepancy maps
│   └── run_analysis_pipeline.py    # Master end-to-end execution pipeline
├── outputs/
│   ├── tables/                     # Exported CSVs with metrics & statistical tests
│   ├── figures/                    # High-res 300 DPI analytical charts
│   └── REPORT.md                   # Full markdown research report
├── presentation_package/
│   ├── report/
│   │   ├── build_pdf_report.py
│   │   └── Gangotri_Glacier_Research_Report.pdf  # 1.35 MB Academic PDF
│   ├── presentation/
│   │   ├── build_presentation.py
│   │   └── Gangotri_Glacier_MultiSatellite_2025.pptx # 12-slide Widescreen PPTX + Notes
│   └── dashboard/
│       ├── app.py                  # Standalone Streamlit dashboard
│       ├── requirements.txt        # Deployment manifest
│       ├── README.md               # Cloud deployment guide
│       ├── data/                   # Bundled CSV datasets (Zero-GEE standalone)
│       └── figures/                # Bundled PNG graphics
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ 7. Installation & Setup

### Prerequisites
* Python 3.10+
* Git installed

```bash
# 1. Clone repository
git clone https://github.com/Piyushhvrma/Glacier-Statistical-Analysis-2025.git
cd Glacier-Statistical-Analysis-2025

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install core dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🚀 8. Running the Statistical Pipeline

```bash
# Execute master end-to-end pipeline (generates all tables, figures, and report)
python scripts/run_analysis_pipeline.py

# Optional: To authenticate live Google Earth Engine with your Google Cloud Project
python scripts/gee_auth.py --project <YOUR_GCP_PROJECT_ID>
```

---

## 🌐 9. Interactive Web Dashboard (Streamlit)

Launch the interactive remote-sensing dashboard locally:
```bash
cd presentation_package/dashboard
streamlit run app.py
```
Open `http://localhost:8501` to explore:
* **Interactive Folium Basemap:** Satellite basemap with Gangotri bounding box and landmarks.
* **Interactive Plotly Visualizations:** Dynamic regressions, Bland-Altman plots, and spectral distributions.
* **One-Click Export Center:** Direct download buttons for CSV tables, PNG figures, PDF report, and PPTX presentation.

---

## 📄 10. Academic Deliverables (PDF & PPTX)

* **Academic PDF Research Report:** [`presentation_package/report/Gangotri_Glacier_Research_Report.pdf`](presentation_package/report/Gangotri_Glacier_Research_Report.pdf) — Comprehensive 17-section paper with mathematical formulations, formatted tables, running headers/footers, and embedded high-res graphics.
* **12-Slide Widescreen Presentation:** [`presentation_package/presentation/Gangotri_Glacier_MultiSatellite_2025.pptx`](presentation_package/presentation/Gangotri_Glacier_MultiSatellite_2025.pptx) — Publication-grade slide deck complete with speaker notes on every slide explaining talking points for viva/evaluators.

---

## 📚 11. Data Attribution & References

* **Sentinel-2 & Landsat Data:** NASA Harmonized Landsat Sentinel-2 (HLS v2 at 30 m) accessed via Google Earth Engine (`NASA/HLS/HLSS30/v002`, `NASA/HLS/HLSL30/v002`).
* **Glacier Inventory:** Randolph Glacier Inventory (RGI Consortium, Version 6.0/7.0, Region 14: South Asia West).
* **Reference Literature:**
  * Claverie, M., et al. (2018). *The Harmonized Landsat and Sentinel-2 (HLS) product.* Remote Sensing of Environment, 219, 145-161.
  * Bland, J. M., & Altman, D. (1986). *Statistical methods for assessing agreement between two methods of clinical measurement.* The Lancet.
  * Oktay, O., et al. (2018). *Attention U-Net: Learning Where to Look for the Pancreas.* arXiv:1804.03999.

---

## 📜 12. License

This project is licensed under the [MIT License](LICENSE).
