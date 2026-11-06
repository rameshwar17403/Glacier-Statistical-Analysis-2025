"""
Interactive Multi-Satellite Glacier Remote Sensing Dashboard
Project: Multi-Satellite Glacier Statistical Analysis (Gangotri Glacier, 2025)
Author: Antigravity Glacier Statistical Analysis Suite

An enterprise-grade Streamlit application for analyzing remote sensing observations:
- Sentinel-2 (NASA HLS HLSS30 v002) vs Landsat 8/9 (NASA HLS HLSL30 v002)
- Interactive Folium satellite basemap with Gangotri bounding box
- Plotly interactive regression, spectral distributions, and Bland-Altman agreement
- Dynamic filtering, interactive tables, and one-click data/report download center
- 100% Standalone: Operates with zero GEE credentials required!
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import folium
from folium import plugins
from streamlit_folium import st_folium

# 1. Page Configuration
st.set_page_config(
    page_title="Gangotri Glacier Multi-Satellite Analytics (2025)",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Base Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
FIG_DIR = os.path.join(BASE_DIR, "figures")
PKG_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
REPORT_PDF = os.path.join(PKG_DIR, "report", "Gangotri_Glacier_Research_Report.pdf")
PPTX_FILE = os.path.join(PKG_DIR, "presentation", "Gangotri_Glacier_MultiSatellite_2025.pptx")

# 2. Data Loader with Caching
@st.cache_data
def load_datasets():
    data = {}
    csv_files = {
        "area": "glacier_area_summary.csv",
        "patches": "patch_level_statistical_comparison.csv",
        "regression": "regression_and_error_metrics.csv",
        "hypothesis": "hypothesis_testing_results.csv",
        "spectral": "spectral_reflectance_statistics.csv"
    }
    for key, fname in csv_files.items():
        fpath = os.path.join(DATA_DIR, fname)
        if os.path.exists(fpath):
            data[key] = pd.read_csv(fpath)
        else:
            data[key] = pd.DataFrame()
    return data

datasets = load_datasets()

# 3. Sidebar Navigation & Global Filters
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/glacier.png", width=64)
    st.title("Glacier Analytics")
    st.markdown("**Gangotri Glacier (2025)**  \n*RGI 14: South Asia West*")
    st.markdown("---")

    nav_selection = st.radio(
        "Navigation Sections:",
        [
            "🏠 Overview & Study Area",
            "🛰️ Satellite Comparison",
            "📏 Glacier Area & Concordance",
            "📈 Spectral NDSI & NDVI",
            "🔍 Regression & Bland-Altman",
            "📊 Hypothesis Tests & Significance",
            "📥 Export & Download Center"
        ]
    )

    st.markdown("---")
    st.markdown("### 🛰️ Sensor Filter")
    sensor_filter = st.multiselect(
        "Select Constellations:",
        ["Sentinel-2 (HLSS30)", "Landsat-8/9 (HLSL30)"],
        default=["Sentinel-2 (HLSS30)", "Landsat-8/9 (HLSL30)"]
    )
    
    st.caption("Framework: 8-Channel Attention U-Net  \nAuthors: Rameshwar C. • Piyush V. • Deepanshu S.")

# ==============================================================================
# SECTION 1: OVERVIEW & STUDY AREA
# ==============================================================================
if nav_selection == "🏠 Overview & Study Area":
    st.title("🧊 Multi-Satellite Glacier Statistical Analysis (2025)")
    st.markdown("### High-Resolution Cryospheric Monitoring: Sentinel-2 vs. Landsat 8/9 over Gangotri Glacier")
    st.markdown(
        "This interactive dashboard presents the complete findings of our comparative remote-sensing study "
        "evaluating the consistency of NASA Harmonized Landsat Sentinel-2 (HLS v2 at 30 m resolution) observations "
        "over the **Gangotri Glacier basin in Uttarakhand, India** during the 2025 ablation season."
    )

    # KPI Top Metrics Banner
    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Sentinel-2 Extent", "17.43 km²", "+1.10 km² bias")
    kpi2.metric("Landsat 8/9 Extent", "16.33 km²", "-1.10 km² bias")
    kpi3.metric("Cohen's Kappa (κ)", "0.8967", "Almost Perfect")
    kpi4.metric("NDSI Correlation (r)", "0.9937", "p < 10⁻¹⁰⁰")
    kpi5.metric("Bland-Altman Bias", "+0.018 km²", "92.1% in 95% LoA")

    st.markdown("---")

    col_map, col_info = st.columns([3, 2])
    with col_map:
        st.subheader("Interactive Satellite Map: Gangotri Glacier Basin")
        # Center coordinates of Gangotri
        center_lat, center_lon = 30.925, 79.175
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=11,
            tiles=None
        )

        # Base Tile Layers
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri World Imagery',
            name='Esri Satellite Imagery',
            overlay=False,
            control=True
        ).add_to(m)

        folium.TileLayer(
            tiles='OpenStreetMap',
            name='OpenStreetMap (Terrain/Roads)',
            overlay=False,
            control=True
        ).add_to(m)

        # Gangotri Bounding Box [min_lon, min_lat, max_lon, max_lat] = [79.05, 30.80, 79.30, 31.05]
        bbox_bounds = [[30.80, 79.05], [31.05, 79.30]]
        folium.Rectangle(
            bounds=bbox_bounds,
            color="#2a9d8f",
            weight=2.5,
            fill=True,
            fill_color="#2a9d8f",
            fill_opacity=0.15,
            popup="Target ROI Bounding Box: [79.05°E, 30.80°N, 79.30°E, 31.05°N]"
        ).add_to(m)

        # Key Landmarks
        folium.Marker(
            [30.926, 79.080],
            popup="<b>Gaumukh Glacier Terminus</b><br/>Elevation: ~4,000 m a.s.l.<br/>Primary terminus and Bhagirathi source.",
            icon=folium.Icon(color="red", icon="flag")
        ).add_to(m)

        folium.Marker(
            [30.835, 30.835 + 48.44], # ~79.28°E
            popup="<b>Chaukhamba Peaks</b><br/>Elevation: 7,138 m a.s.l.<br/>Accumulation zone headwaters.",
            icon=folium.Icon(color="blue", icon="certificate")
        ).add_to(m)

        folium.LayerControl().add_to(m)
        st_folium(m, width="100%", height=480)

    with col_info:
        st.subheader("Glacier Catchment Profile")
        st.markdown(
            """
            * **Glacier Name:** Gangotri Glacier (गंगोत्री हिमनद)
            * **Region:** Garhwal Himalaya, Uttarakhand, India
            * **Inventory:** Randolph Glacier Inventory (RGI 14: South Asia West)
            * **Glacier Type:** Valley Glacier with extensive supraglacial debris cover
            * **Length & Width:** ~30 km long; 2 to 4 km wide
            * **Elevation Range:** ~4,000 m (Snout at Gaumukh) to 7,138 m (Chaukhamba)
            * **Drainage Basin:** Bhagirathi River (Headwaters of the Ganges)
            * **Ablation Season Window:** August – October (Minimal snowpack)
            * **Primary Challenge:** Supraglacial morainic debris mimics surrounding bedrock, requiring attention-gated feature filtering.
            """
        )
        st.info("💡 **Scientific Note:** All statistical results and maps displayed on this dashboard reflect the verified 2025 satellite analysis outputs.")

# ==============================================================================
# SECTION 2: SATELLITE COMPARISON
# ==============================================================================
elif nav_selection == "🛰️ Satellite Comparison":
    st.title("🛰️ Satellite Dataset Comparison & Preprocessing")
    st.markdown("### Harmonized Landsat Sentinel-2 (NASA HLS v2 at 30 m)")

    col_s2, col_l8 = st.columns(2)
    with col_s2:
        st.subheader("Copernicus Sentinel-2 (HLSS30)")
        st.markdown(
            """
            * **Collection ID:** `NASA/HLS/HLSS30/v002`
            * **Sensor:** MultiSpectral Instrument (MSI) on Sentinel-2A/2B
            * **Native Resolution:** 10 m (Vis/NIR), 20 m (SWIR)
            * **Harmonized Grid:** Gridded to 30 m UTM Zone 44N
            * **Spectral Bands Used:** B02 (Blue), B03 (Green), B04 (Red), B8A (Narrow NIR), B11 (SWIR1), B12 (SWIR2)
            * **Revisit Cycle:** 5 days at equator (2 to 3 days over Himalayas)
            """
        )

    with col_l8:
        st.subheader("Landsat 8/9 (HLSL30)")
        st.markdown(
            """
            * **Collection ID:** `NASA/HLS/HLSL30/v002`
            * **Sensor:** Operational Land Imager (OLI) on Landsat 8 & 9
            * **Native Resolution:** 30 m across all reflective bands
            * **Harmonized Grid:** Gridded to identical 30 m UTM Zone 44N
            * **Spectral Bands Used:** B02 (Blue), B03 (Green), B04 (Red), B05 (NIR), B06 (SWIR1), B07 (SWIR2)
            * **Revisit Cycle:** 8 days combined (Landsat 8 + Landsat 9)
            """
        )

    st.markdown("---")
    st.subheader("Spectral Band Alignment Matrix")
    band_df = pd.DataFrame([
        {"Channel": "Blue", "Wavelength": "~490 nm", "Sentinel-2 (HLSS30)": "B02", "Landsat 8/9 (HLSL30)": "B02", "Cryospheric Purpose": "Atmospheric scattering correction & water penetration"},
        {"Channel": "Green", "Wavelength": "~560 nm", "Sentinel-2 (HLSS30)": "B03", "Landsat 8/9 (HLSL30)": "B03", "Cryospheric Purpose": "Visible reflectance peak for ice; NDSI numerator"},
        {"Channel": "Red", "Wavelength": "~665 nm", "Sentinel-2 (HLSS30)": "B04", "Landsat 8/9 (HLSL30)": "B04", "Cryospheric Purpose": "Chlorophyll absorption; NDVI denominator"},
        {"Channel": "NIR", "Wavelength": "~865 nm", "Sentinel-2 (HLSS30)": "B8A", "Landsat 8/9 (HLSL30)": "B05", "Cryospheric Purpose": "Clean ice/snow peak; NDVI numerator"},
        {"Channel": "SWIR1", "Wavelength": "~1610 nm", "Sentinel-2 (HLSS30)": "B11", "Landsat 8/9 (HLSL30)": "B06", "Cryospheric Purpose": "Strong ice absorption band; NDSI denominator"},
        {"Channel": "SWIR2", "Wavelength": "~2200 nm", "Sentinel-2 (HLSS30)": "B12", "Landsat 8/9 (HLSL30)": "B07", "Cryospheric Purpose": "Discriminates snow from morainic rock and soil"},
    ])
    st.dataframe(band_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Cloud & Shadow QA Filtering: Fmask Bit Decoding")
    st.markdown(
        """
        To avoid the catastrophic error of masking glacier snow as clouds, the pipeline parses individual bits of the 8-bit `Fmask` layer:
        * **Bit 0 (Cirrus Cloud):** Masked out
        * **Bit 1 (Opaque Cloud):** Masked out
        * **Bit 2 & 3 (Adjacent Cloud & Cloud Shadow):** Masked out
        * **Bit 4 (Snow / Ice):** **EXPLICITLY RETAINED & PROTECTED**
        * **Bit 5 (Water):** Retained for proglacial lake analysis
        """
    )

# ==============================================================================
# SECTION 3: GLACIER AREA & CONCORDANCE
# ==============================================================================
elif nav_selection == "📏 Glacier Area & Concordance":
    st.title("📏 Glacier Surface Area & Spatial Concordance")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Total Catchment Extent Comparison")
        area_df = datasets["area"]
        if not area_df.empty:
            st.dataframe(area_df, use_container_width=True)
            
            fig_bar = px.bar(
                area_df,
                x="Sensor",
                y="Area_sqkm",
                color="Sensor",
                color_discrete_map={"Sentinel-2 (HLSS30)": "#2a9d8f", "Landsat-8/9 (HLSL30)": "#e76f51"},
                title="Mapped Glacier Extent (km²)",
                text_auto='.3f'
            )
            fig_bar.update_layout(yaxis_title="Total Surface Area (sq. km)", showlegend=False)
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.warning("Glacier area summary data not found.")

    with col2:
        st.subheader("Inter-Sensor Concordance Metrics")
        st.markdown(
            """
            * **Cohen's Kappa (κ):** `0.8967`  
              *(Values above 0.81 indicate almost perfect inter-rater agreement)*
            * **Jaccard Similarity Index (IoU):** `0.8252`
            * **Dice Similarity Coefficient (F1):** `0.9042`
            * **Overall Pixel Concordance:** `98.61%`
            * **Absolute Extent Discrepancy:** `1.101 km²` (`6.32%` relative difference)
            """
        )
        st.info(
            "📌 **Glaciological Insight:** The 6.32% discrepancy between sensors is concentrated along "
            "the steep lateral moraines and shadowed terminus boundaries where mixed-pixel effects occur, "
            "rather than on the central accumulation ice body."
        )

    st.markdown("---")
    st.subheader("Spatial Discrepancy Map (Four-Class Classified Overlap)")
    disc_img_path = os.path.join(FIG_DIR, "spatial_discrepancy_map.png")
    if os.path.exists(disc_img_path):
        st.image(
            disc_img_path,
            caption="Spatial Discrepancy Map: White = Concordant Glacier Ice; Cyan = Unique to Sentinel-2; Orange = Unique to Landsat; Dark = Barren Mountain Rock.",
            use_container_width=True
        )

# ==============================================================================
# SECTION 4: SPECTRAL NDSI & NDVI
# ==============================================================================
elif nav_selection == "📈 Spectral NDSI & NDVI":
    st.title("📈 Spectral Reflectance & Cryospheric Index Analytics")
    st.markdown("### NDSI & NDVI Distributions over Gangotri Glacier")

    spec_df = datasets["spectral"]
    if not spec_df.empty:
        # Filter by selected sensors
        filtered_spec = spec_df[spec_df["Sensor"].isin(sensor_filter)]
        
        st.subheader("Descriptive Band & Index Statistics")
        st.dataframe(filtered_spec, use_container_width=True)

        fig_spec = px.bar(
            filtered_spec,
            x="Band_Index",
            y="Mean",
            error_y="Std",
            color="Sensor",
            barmode="group",
            color_discrete_map={"Sentinel-2 (HLSS30)": "#2a9d8f", "Landsat-8/9 (HLSL30)": "#e76f51"},
            title="Mean Surface Reflectance & Spectral Indices (with ±1 SD error bars)"
        )
        fig_spec.update_layout(yaxis_title="Surface Reflectance / Index Value")
        st.plotly_chart(fig_spec, use_container_width=True)
    else:
        st.warning("Spectral reflectance data table not found.")

    st.markdown("---")
    st.subheader("Comparative Split Violin Distributions")
    viol_img_path = os.path.join(FIG_DIR, "spectral_distributions_violin.png")
    if os.path.exists(viol_img_path):
        st.image(
            viol_img_path,
            caption="Split Violin Distribution: NDSI, NDVI, Green, and NIR reflectance across Sentinel-2 (teal) and Landsat 8/9 (coral).",
            use_container_width=True
        )

# ==============================================================================
# SECTION 5: REGRESSION & BLAND-ALTMAN
# ==============================================================================
elif nav_selection == "🔍 Regression & Bland-Altman":
    st.title("🔍 Linear Regression, Correlation & Bland-Altman Agreement")
    st.markdown("### Evaluating Radiometric Consistency vs. Physical Agreement")

    reg_df = datasets["regression"]
    if not reg_df.empty:
        st.subheader("Ordinary Least Squares (OLS) Regression & Error Parameters")
        st.dataframe(reg_df, use_container_width=True)

    col_reg1, col_reg2 = st.columns(2)
    with col_reg1:
        st.subheader("Pixel-Level NDSI Correlation")
        ndsi_img_path = os.path.join(FIG_DIR, "ndsi_regression_scatter.png")
        if os.path.exists(ndsi_img_path):
            st.image(ndsi_img_path, caption="NDSI Linear Regression (R² = 0.988, Pearson r = 0.994, RMSE = 0.041)", use_container_width=True)

    with col_reg2:
        st.subheader("Sub-Basin Area Correlation")
        area_reg_img_path = os.path.join(FIG_DIR, "glacier_area_regression_scatter.png")
        if os.path.exists(area_reg_img_path):
            st.image(area_reg_img_path, caption="Patch-Level Area Linear Regression (R² = 0.995, Pearson r = 0.998)", use_container_width=True)

    st.markdown("---")
    st.subheader("Bland-Altman Agreement Analysis (Glacier Extent)")
    st.markdown(
        """
        **Why Bland-Altman?** In clinical and remote-sensing science, high correlation does **not** prove agreement. 
        Bland-Altman analysis plots the difference between sensors against their mean to reveal systematic bias and limits of agreement.
        """
    )
    ba_img_path = os.path.join(FIG_DIR, "bland_altman_glacier_area.png")
    if os.path.exists(ba_img_path):
        st.image(ba_img_path, caption="Bland-Altman Plot: Mean Bias = +0.0175 km²; 95% Limits of Agreement = [-0.064 km², +0.099 km²]; 92.1% Concordance.", use_container_width=True)

    # Interactive Sub-Basin Scatter
    patches_df = datasets["patches"]
    if not patches_df.empty:
        st.markdown("---")
        st.subheader("Interactive Catchment Patch Explorer")
        st.markdown("Explore regional agreement across the 63 evaluated spatial tiles:")
        fig_patch = px.scatter(
            patches_df,
            x="Area_S2_sqkm",
            y="Area_L8_sqkm",
            color="Area_Diff_sqkm",
            color_continuous_scale="Viridis",
            hover_data=["Patch_ID", "Row", "Col", "NDSI_S2", "NDSI_L8"],
            title="Interactive Tile-by-Tile Glacier Area Agreement (Hover to inspect patches)"
        )
        fig_patch.update_layout(xaxis_title="Sentinel-2 Area (km²)", yaxis_title="Landsat 8/9 Area (km²)")
        st.plotly_chart(fig_patch, use_container_width=True)

# ==============================================================================
# SECTION 6: HYPOTHESIS TESTS & SIGNIFICANCE
# ==============================================================================
elif nav_selection == "📊 Hypothesis Tests & Significance":
    st.title("📊 Statistical Hypothesis Testing & Significance")
    st.markdown("### Determining Whether Discrepancies are Statistically Meaningful")

    hyp_df = datasets["hypothesis"]
    if not hyp_df.empty:
        st.subheader("Formal Paired Hypothesis Testing Results")
        st.dataframe(hyp_df, use_container_width=True)

    st.markdown("---")
    st.subheader("Scientific Interpretation of Statistical Results")
    st.markdown(
        """
        1. **Normality Testing (Shapiro-Wilk):**  
           The differences in glacier area across catchment tiles yielded $p = 1.98 \times 10^{-13} < 0.05$. 
           Because the distribution of differences rejects the assumption of normality, parametric paired t-tests are invalid; 
           non-parametric **Wilcoxon signed-rank tests** were appropriately applied.
        
        2. **Wilcoxon Signed-Rank Test:**  
           The test returned $p = 0.00065 < 0.05$, confirming that a statistically significant difference exists between Sentinel-2 
           and Landsat 8/9 area estimates.
        
        3. **Effect Size (Cohen's d):**  
           While statistically significant, the effect size is **$d = 0.4201$** (small to moderate). 
           In remote sensing, large sample sizes can yield tiny $p$-values for negligible physical differences. The effect size confirms 
           that the divergence between sensors is minor.
        
        4. **95% Bootstrap Confidence Intervals:**  
           * Sentinel-2 Area 95% CI: `[0.139, 0.440] km²` per patch  
           * Landsat 8/9 Area 95% CI: `[0.124, 0.427] km²` per patch  
           The overlapping confidence intervals substantiate sensor compatibility.
        """
    )

# ==============================================================================
# SECTION 7: EXPORT & DOWNLOAD CENTER
# ==============================================================================
elif nav_selection == "📥 Export & Download Center":
    st.title("📥 Export Center & Deliverables Download")
    st.markdown("### Access all Project Reports, Presentations, Raw Data Tables, and Graphics")

    st.subheader("1. Comprehensive Presentation Package Deliverables")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        if os.path.exists(REPORT_PDF):
            with open(REPORT_PDF, "rb") as f:
                pdf_bytes = f.read()
            st.download_button(
                label="📄 Download Academic Research Report (PDF)",
                data=pdf_bytes,
                file_name="Gangotri_Glacier_Research_Report.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            st.caption(f"Compiled ReportLab PDF • Size: {len(pdf_bytes):,} bytes")
        else:
            st.error("Report PDF not found.")

    with col_d2:
        if os.path.exists(PPTX_FILE):
            with open(PPTX_FILE, "rb") as f:
                pptx_bytes = f.read()
            st.download_button(
                label="📊 Download PowerPoint Presentation (PPTX)",
                data=pptx_bytes,
                file_name="Gangotri_Glacier_MultiSatellite_2025.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )
            st.caption(f"12 Widescreen Slides with Speaker Notes • Size: {len(pptx_bytes):,} bytes")
        else:
            st.error("PPTX file not found.")

    st.markdown("---")
    st.subheader("2. Exported Statistical Data Tables (CSV)")
    for name, df in datasets.items():
        if not df.empty:
            csv_str = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download {name.capitalize()} Dataset ({name}.csv)",
                data=csv_str,
                file_name=f"gangotri_glacier_{name}.csv",
                mime="text/csv",
                key=f"dl_{name}"
            )

    st.markdown("---")
    st.subheader("3. High-Resolution Visual Artifacts (PNG)")
    figures = [
        ("spatial_discrepancy_map.png", "Spatial Discrepancy Map"),
        ("bland_altman_glacier_area.png", "Bland-Altman Agreement Plot"),
        ("ndsi_regression_scatter.png", "NDSI Linear Regression Scatter"),
        ("glacier_area_regression_scatter.png", "Catchment Area Regression Scatter"),
        ("spectral_distributions_violin.png", "Spectral Distributions Violin Plot")
    ]
    for fig_file, label in figures:
        fig_path = os.path.join(FIG_DIR, fig_file)
        if os.path.exists(fig_path):
            with open(fig_path, "rb") as f:
                f_bytes = f.read()
            st.download_button(
                label=f"🖼️ Download {label} ({fig_file})",
                data=f_bytes,
                file_name=fig_file,
                mime="image/png",
                key=f"dl_fig_{fig_file}"
            )
