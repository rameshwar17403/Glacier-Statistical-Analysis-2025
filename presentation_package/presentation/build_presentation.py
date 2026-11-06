"""
Professional 12-Slide Academic PowerPoint Presentation Generator
Author: Antigravity Glacier Statistical Analysis Suite

Generates a publication-grade 16:9 widescreen PowerPoint presentation (.pptx)
for: Multi-Satellite Glacier Statistical Analysis (Gangotri Glacier, 2025)
Includes slide layouts, scientific color palettes, high-res figures, tables,
and comprehensive speaker notes for every single slide.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Primary Color Palette
NAVY = RGBColor(29, 53, 87)       # #1d3557
TEAL = RGBColor(42, 157, 143)     # #2a9d8f
DARK = RGBColor(38, 70, 83)       # #264653
CORAL = RGBColor(231, 111, 81)    # #e76f51
BG_LIGHT = RGBColor(248, 250, 252)# #f8fafc
WHITE = RGBColor(255, 255, 255)
GRAY = RGBColor(100, 116, 139)    # #64748b
BORDER_GRAY = RGBColor(203, 213, 225)

def add_header(slide, title_text, category="RESEARCH PRESENTATION"):
    """Adds a standardized top banner and title block to content slides."""
    # Top banner bar
    top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.15))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = NAVY
    top_bar.line.fill.background()

    # Category tracker
    cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.12), Inches(10), Inches(0.3))
    tf_c = cat_box.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.size = Pt(10)
    p_c.font.bold = True
    p_c.font.color.rgb = TEAL

    # Main slide title
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11), Inches(0.65))
    tf_t = title_box.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title_text
    p_t.font.size = Pt(22)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    # Thin accent line under header
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.15), Inches(13.333), Inches(0.06))
    line.fill.solid()
    line.fill.fore_color.rgb = TEAL
    line.line.fill.background()

def create_presentation(output_pptx_path: str, figures_dir: str):
    os.makedirs(os.path.dirname(output_pptx_path), exist_ok=True)
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # ========================================================
    # SLIDE 1: Title & Project Team
    # ========================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Center card
    card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    card.fill.solid()
    card.fill.fore_color.rgb = DARK
    card.line.color.rgb = TEAL
    card.line.width = Pt(2)

    tb = s1.shapes.add_textbox(Inches(1.6), Inches(1.4), Inches(10.133), Inches(4.7))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "B.Tech Minor Project • Department of Information Technology • NIT Raipur"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = TEAL
    p0.space_after = Pt(14)

    p1 = tf.add_paragraph()
    p1.text = "Multi-Satellite Glacier Statistical Analysis"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "A Comparative Remote-Sensing Evaluation of Sentinel-2 vs. Landsat 8/9 over Gangotri Glacier (2025)"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(226, 232, 240)
    p2.space_after = Pt(28)

    p3 = tf.add_paragraph()
    p3.text = "Project Team: Rameshwar Chandravanshi • Piyush Verma • Deepanshu Sahu\n" \
              "Architecture: 8-Channel Attention U-Net Framework | Sensor Suite: NASA HLS v2 (HLSS30 & HLSL30)\n" \
              "Target Region: Gangotri Glacier Basin (RGI 14: South Asia West) | Year of Study: 2025"
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(148, 163, 184)

    s1.notes_slide.notes_text_frame.text = (
        "Good morning everyone. Today we present our minor project research on 'Multi-Satellite Glacier Statistical "
        "Analysis for Gangotri Glacier in 2025'. Our project extends our existing 8-Channel Attention U-Net glacier "
        "segmentation pipeline by answering a crucial scientific question: How consistent and interchangeable are "
        "orbital observations between Copernicus Sentinel-2 and Landsat 8/9 when monitoring the exact same glacier region?"
    )

    # ========================================================
    # SLIDE 2: Introduction & Research Objectives
    # ========================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "1. Research Motivation & Core Objectives", "Introduction")

    tb2 = s2.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.6))
    tf2 = tb2.text_frame
    tf2.word_wrap = True

    p = tf2.paragraphs[0]
    p.text = "The Cryospheric Challenge in the Himalayas"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(6)

    p = tf2.add_paragraph()
    p.text = "• Himalayan glaciers feed major Asian river systems but are undergoing accelerated retreat due to climate change.\n" \
             "• High mountain terrain presents severe computer vision challenges: supraglacial debris cover, deep shadows, and ephemeral seasonal snow.\n" \
             "• Deep learning models (Attention U-Net) automate delineation, but operational monitoring depends on data from multiple satellite constellations."
    p.font.size = Pt(13.5)
    p.font.color.rgb = DARK
    p.space_after = Pt(20)

    p = tf2.add_paragraph()
    p.text = "Four Primary Research Objectives"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(6)

    p = tf2.add_paragraph()
    p.text = "1. Radiometric Harmonization: Verify cross-sensor surface reflectance consistency between Sentinel-2 and Landsat 8/9.\n" \
             "2. Cryospheric Indices: Calculate and correlate Normalized Difference Snow Index (NDSI) and NDVI across both sensors.\n" \
             "3. Extent & Area Agreement: Quantify glacier surface area in km² and evaluate spatial overlap (IoU, Cohen's Kappa).\n" \
             "4. Statistical Hypothesis Testing: Run paired tests and Bland-Altman agreement analysis to prove sensor interchangeability."
    p.font.size = Pt(13.5)
    p.font.color.rgb = DARK

    s2.notes_slide.notes_text_frame.text = (
        "On this slide, we outline the motivation. Remote sensing of Himalayan glaciers is complicated by debris and shadows. "
        "When tracking glacier changes over decades, researchers combine Sentinel-2 and Landsat imagery. Our four objectives "
        "ensure that differences between sensors are rigorously quantified so sensor noise is never mistaken for true glacier retreat."
    )

    # ========================================================
    # SLIDE 3: Gangotri Glacier Study Area
    # ========================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "2. Study Area: Gangotri Glacier Basin (RGI 14)", "Geographical Setting")

    tb3_left = s3.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(6.2), Inches(5.6))
    tf3_l = tb3_left.text_frame
    tf3_l.word_wrap = True

    p = tf3_l.paragraphs[0]
    p.text = "Geographical & Glaciological Profile"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    p = tf3_l.add_paragraph()
    p.text = "• Location: Uttarkashi District, Uttarakhand, India (Garhwal Himalaya).\n" \
             "• Glacier Classification: Valley glacier; primary source of the Bhagirathi River (Ganga headwaters).\n" \
             "• Dimensions: ~30 km length, 2 to 4 km width, covering ~140 km² entire basin.\n" \
             "• Elevation Range: ~4,000 m a.s.l. (Gaumukh terminus) to >7,000 m (Chaukhamba peaks).\n" \
             "• RGI Reference: Region 14 (South Asia West).\n" \
             "• Bounding Box: [79.05°E, 30.80°N, 79.30°E, 31.05°N].\n" \
             "• Terrain Difficulties: Extensive supraglacial debris on the ablation tongue and steep granite valley walls casting deep shadows."
    p.font.size = Pt(13)
    p.font.color.rgb = DARK

    # Right side: Embed Discrepancy / Study Area Map
    disc_img = os.path.join(figures_dir, "spatial_discrepancy_map.png")
    if os.path.exists(disc_img):
        s3.shapes.add_picture(disc_img, Inches(7.3), Inches(1.5), width=Inches(5.2))

    s3.notes_slide.notes_text_frame.text = (
        "Here is our study area: Gangotri Glacier in Uttarakhand. It is one of the largest valley glaciers in the Himalayas "
        "and forms the source of the Ganges. As you can see on the right map, the glacier body spans high accumulation snowfields "
        "down to the heavily debris-covered snout at Gaumukh. This complex terrain makes it the ideal benchmark for our study."
    )

    # ========================================================
    # SLIDE 4: Sentinel-2 vs. Landsat 8/9 Sensor Comparison
    # ========================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "3. Sensor Comparison: Sentinel-2 MSI vs. Landsat 8/9 OLI", "Remote Sensing Instrumentation")

    # Table comparing the sensors
    rows, cols = 8, 4
    left, top, width, height = Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.3)
    tbl_shape = s4.shapes.add_table(rows, cols, left, top, width, height)
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.2)
    tbl.columns[1].width = Inches(3.2)
    tbl.columns[2].width = Inches(3.2)
    tbl.columns[3].width = Inches(3.133)

    headers = ["Feature / Spec", "Copernicus Sentinel-2 (MSI)", "Landsat 8/9 (OLI)", "Harmonization in HLS v2"]
    for c_idx, h in enumerate(headers):
        cell = tbl.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        cell.text_frame.paragraphs[0].text = h
        cell.text_frame.paragraphs[0].font.size = Pt(12)
        cell.text_frame.paragraphs[0].font.bold = True
        cell.text_frame.paragraphs[0].font.color.rgb = WHITE

    data = [
        ("Agency & Constellation", "ESA (Sentinel-2A / 2B)", "NASA / USGS (Landsat 8 & 9)", "Joint NASA Harmonization"),
        ("Optical Sensor", "MultiSpectral Instrument (MSI)", "Operational Land Imager (OLI)", "Cross-calibrated Level-2A"),
        ("Native Spatial Resolution", "10 m (Vis/NIR), 20 m (SWIR)", "30 m (Vis/NIR/SWIR)", "Both resampled to 30 m grid"),
        ("Orbital Revisit Cycle", "5 days (with 2 satellites)", "8 days (Landsat 8 + 9 combined)", "Combined revisit ~2 to 3 days"),
        ("Key NIR Band", "Band 8A (865 nm, narrow)", "Band 5 (865 nm, narrow)", "Atmospherically corrected"),
        ("Key SWIR1 Band", "Band 11 (1610 nm)", "Band 6 (1610 nm)", "Identical ice absorption center"),
        ("Radiometric Resolution", "12-bit dynamic range", "12-bit (L8) / 14-bit (L9)", "16-bit Surface Reflectance (DN/10000)")
    ]

    for r_idx, row in enumerate(data):
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = BG_LIGHT if r_idx % 2 == 0 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.color.rgb = DARK

    s4.notes_slide.notes_text_frame.text = (
        "This slide compares the two satellite systems. Sentinel-2 has a 5-day revisit and 10 to 20m resolution, "
        "while Landsat has a 30m resolution and 8-day combined revisit. NASA's Harmonized Landsat Sentinel-2 (HLS) "
        "pipeline re-grids both to a common 30m UTM grid and performs BRDF solar zenith normalization, enabling direct comparison."
    )

    # ========================================================
    # SLIDE 5: Satellite Data Acquisition Pipeline
    # ========================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "4. 2025 Satellite Observation Acquisition Pipeline", "Data Acquisition")

    tb5 = s5.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.6))
    tf5 = tb5.text_frame
    tf5.word_wrap = True

    p = tf5.paragraphs[0]
    p.text = "Targeting the 2025 Ablation Season"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(6)

    p = tf5.add_paragraph()
    p.text = "• Temporal Filter: August 1 – October 31, 2025. This window represents the annual minimum snowpack in the Garhwal Himalaya, exposing the actual permanent glacier ice boundary and minimizing seasonal snow confusion.\n" \
             "• Cloud Threshold: Filtered scenes with < 25% regional cloud cover over UTM Tile 44RKR / 44RLR.\n" \
             "• NASA HLS Product Collections:\n" \
             "    - NASA/HLS/HLSS30/v002 (Sentinel-2 Harmonized Surface Reflectance)\n" \
             "    - NASA/HLS/HLSL30/v002 (Landsat 8/9 Harmonized Surface Reflectance)"
    p.font.size = Pt(13)
    p.font.color.rgb = DARK
    p.space_after = Pt(20)

    p = tf5.add_paragraph()
    p.text = "Automated Acquisition Protocol"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(6)

    p = tf5.add_paragraph()
    p.text = "1. Google Earth Engine Authentication: Configured via ee.Initialize(project='<gcp_project_id>').\n" \
             "2. Spatial Clipping: Subsets the raw scenes precisely to the Gangotri bounding box [79.05, 30.80, 79.30, 31.05].\n" \
             "3. Near-Synchronous Pairing: Pairs acquisitions closest in solar time to minimize atmospheric and diurnal melt divergence.\n" \
             "4. Zero-GEE Export Architecture: Pre-exports processed tensors and tabular summaries to ensure our dashboard and reports run completely offline."
    p.font.size = Pt(13)
    p.font.color.rgb = DARK

    s5.notes_slide.notes_text_frame.text = (
        "On slide 5, we detail our acquisition protocol. We target late summer 2025 because winter snow melts away, "
        "leaving only the true glacier ice exposed. We query both HLS S30 and L30 products through Earth Engine API, "
        "clip them to our ROI, and bundle the resulting data locally so our deliverables run without cloud dependencies."
    )

    # ========================================================
    # SLIDE 6: Preprocessing & Fmask Cloud QA Filtering
    # ========================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "5. Image Preprocessing & Cloud QA Bitmasking", "Radiometric Processing")

    tb6 = s6.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.733), Inches(5.6))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    p = tf6.paragraphs[0]
    p.text = "The Critical Challenge: Preserving Glacier Ice from Cloud Masking"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(6)

    p = tf6.add_paragraph()
    p.text = "A frequent pitfall in remote sensing is using automated cloud masks that mistake high-albedo glacier ice for clouds. " \
             "To avoid accidentally deleting glaciers, we decoded the NASA HLS Fmask QA bitmask at the individual bit level:"
    p.font.size = Pt(13)
    p.font.color.rgb = DARK
    p.space_after = Pt(14)

    # QA Table
    qa_rows, qa_cols = 6, 3
    qa_shape = s6.shapes.add_table(qa_rows, qa_cols, Inches(0.8), Inches(2.9), Inches(11.733), Inches(3.8))
    qa_tbl = qa_shape.table
    qa_tbl.columns[0].width = Inches(2.2)
    qa_tbl.columns[1].width = Inches(5.0)
    qa_tbl.columns[2].width = Inches(4.533)

    qa_heads = ["Fmask Bit Index", "Condition & Flag Description", "Action Taken in Pipeline"]
    for c_idx, h in enumerate(qa_heads):
        c = qa_tbl.cell(0, c_idx)
        c.fill.solid()
        c.fill.fore_color.rgb = NAVY
        c.text_frame.paragraphs[0].text = h
        c.text_frame.paragraphs[0].font.size = Pt(11)
        c.text_frame.paragraphs[0].font.bold = True
        c.text_frame.paragraphs[0].font.color.rgb = WHITE

    qa_data = [
        ("Bit 0", "Cirrus Cloud", "Masked (Set to Invalid)"),
        ("Bit 1", "Opaque Cloud", "Masked (Set to Invalid)"),
        ("Bit 2 & 3", "Adjacent Cloud / Cloud Shadow", "Masked (Set to Invalid)"),
        ("Bit 4", "Snow / Ice (True Glacier Surface)", "EXPLICITLY PRESERVED & RETAINED"),
        ("Bit 5", "Water Bodies", "Retained for proglacial lake analysis")
    ]

    for r_idx, (b, desc, act) in enumerate(qa_data):
        for c_idx, val in enumerate([b, desc, act]):
            cell = qa_tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            if "PRESERVED" in val:
                cell.fill.fore_color.rgb = RGBColor(209, 250, 229)
            else:
                cell.fill.fore_color.rgb = BG_LIGHT if r_idx % 2 == 0 else WHITE
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(11)
            p.font.bold = "PRESERVED" in val
            p.font.color.rgb = TEAL if "PRESERVED" in val else DARK

    s6.notes_slide.notes_text_frame.text = (
        "Slide 6 covers preprocessing. Notice Bit 4: snow and ice. Generic cloud masking tools often classify white glacier "
        "ice as clouds. By decoding Fmask bits directly, we filter out cirrus, cloud, and shadow while strictly preserving "
        "true glacier snow and ice. All surface reflectance values are then converted to physical reflectance with scale factor 0.0001."
    )

    # ==========================================
    # SLIDE 7: Glacier Segmentation & Spectral Indices
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "6. Glacier Segmentation Methodology & Spectral Indices", "Segmentation Pipeline")

    tb7_l = s7.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(6.0), Inches(5.6))
    tf7_l = tb7_l.text_frame
    tf7_l.word_wrap = True

    p = tf7_l.paragraphs[0]
    p.text = "Mathematical Formulations"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    p = tf7_l.add_paragraph()
    p.text = "• Normalized Difference Snow Index (NDSI):\n" \
             "    NDSI = (Green - SWIR1) / (Green + SWIR1 + ε)\n" \
             "    Isolates clean ice/snow through high green reflectance and strong SWIR absorption.\n\n" \
             "• Normalized Difference Vegetation Index (NDVI):\n" \
             "    NDVI = (NIR - Red) / (NIR + Red + ε)\n" \
             "    Discriminates lateral moraine vegetation from ice.\n\n" \
             "• Standardized Glacier Delineation Thresholds:\n" \
             "    NDSI ≥ 0.40  AND  NIR ≥ 0.11 (eliminates water & shadows)\n\n" \
             "• Morphological Refinement:\n" \
             "    Binary opening & closing (2x2 kernel) removes isolated noise speckles and closes crevasse micro-voids."
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK

    # Right side: embed violin plot of distributions
    viol_img = os.path.join(figures_dir, "spectral_distributions_violin.png")
    if os.path.exists(viol_img):
        s7.shapes.add_picture(viol_img, Inches(7.1), Inches(1.8), width=Inches(5.4))

    s7.notes_slide.notes_text_frame.text = (
        "Here we show our segmentation methodology. NDSI exploits the fact that ice reflects green light but strongly absorbs "
        "shortwave-infrared. NIR thresholding at 0.11 prevents water bodies and mountain shadows from being misclassified. "
        "On the right, our split violin plots show that Sentinel-2 and Landsat exhibit almost identical bimodal NDSI distributions."
    )

    # ==========================================
    # SLIDE 8: Glacier Area Comparison
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "7. Glacier Surface Area Comparison (km²)", "Glaciological Results")

    tb8_l = s8.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.6))
    tf8_l = tb8_l.text_frame
    tf8_l.word_wrap = True

    p = tf8_l.paragraphs[0]
    p.text = "Total Mapped Catchment Extent"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    p = tf8_l.add_paragraph()
    p.text = "• Sentinel-2 (HLSS30): 17.429 km² (19,366 glacier pixels)\n" \
             "• Landsat 8/9 (HLSL30): 16.329 km² (18,143 glacier pixels)\n" \
             "• Absolute Discrepancy: 1.101 km² (6.32% relative difference)\n\n" \
             "Spatial Concordance & Boundary Accuracy:\n" \
             "• Cohen's Kappa (κ): 0.8967 (Almost Perfect Agreement)\n" \
             "• Jaccard Index (IoU): 0.8252\n" \
             "• Dice Similarity Coefficient (F1): 0.9042\n" \
             "• Total Pixel Classification Agreement: 98.61%\n\n" \
             "Glaciological Interpretation:\n" \
             "The 6.32% divergence is localized exclusively to mixed-pixel lateral moraines and shaded terminus margins, not central ice bodies."
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK

    # Right side: Embed catchment area regression
    area_reg_img = os.path.join(figures_dir, "glacier_area_regression_scatter.png")
    if os.path.exists(area_reg_img):
        s8.shapes.add_picture(area_reg_img, Inches(7.0), Inches(1.5), width=Inches(5.5))

    s8.notes_slide.notes_text_frame.text = (
        "Slide 8 presents our primary area comparison. Sentinel-2 mapped 17.43 sq km while Landsat mapped 16.33 sq km. "
        "The absolute difference is just 1.1 sq km, or 6.3%. Cohen's kappa is 0.897 and Dice F1 is 0.904. The scatter plot "
        "on the right shows that sub-basin patch area estimates line up almost perfectly along the 1:1 identity line with R² of 0.995."
    )

    # ==========================================
    # SLIDE 9: NDSI & NDVI Statistical Analysis
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "8. NDSI & NDVI Correlation & Regression Analysis", "Spectral Analysis")

    tb9_l = s9.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.6))
    tf9_l = tb9_l.text_frame
    tf9_l.word_wrap = True

    p = tf9_l.paragraphs[0]
    p.text = "Pixel-Level OLS Linear Regression"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    p = tf9_l.add_paragraph()
    p.text = "• Pearson Correlation (r): 0.9937 (p < 10⁻¹⁰⁰)\n" \
             "• Spearman Rank Correlation (ρ): 0.9379\n" \
             "• Coefficient of Determination (R²): 0.9875\n" \
             "• Regression Equation: NDSI_L8 = 1.006 · NDSI_S2 - 0.007\n" \
             "• Slope (m): 1.0055 ± 0.0016 (Near-ideal unity)\n" \
             "• Intercept (c): -0.0072 (Negligible baseline offset)\n" \
             "• Root Mean Squared Error (RMSE): 0.0410\n" \
             "• Mean Absolute Error (MAE): 0.0322\n\n" \
             "Conclusion: NASA HLS atmospheric and BRDF corrections achieve near-perfect spectral index harmony."
    p.font.size = Pt(12.5)
    p.font.color.rgb = DARK

    # Right side: Embed NDSI regression scatter
    ndsi_reg_img = os.path.join(figures_dir, "ndsi_regression_scatter.png")
    if os.path.exists(ndsi_reg_img):
        s9.shapes.add_picture(ndsi_reg_img, Inches(7.0), Inches(1.5), width=Inches(5.5))

    s9.notes_slide.notes_text_frame.text = (
        "Slide 9 evaluates spectral index correlation. Pixel-level NDSI exhibits a Pearson correlation of 0.9937 and R² of 0.9875. "
        "The regression slope is 1.006 with an intercept of minus 0.007, virtually identical to the theoretical 1:1 identity line. "
        "RMSE is just 0.041, validating that the NASA HLS pipeline effectively harmonizes surface reflectance."
    )

    # ==========================================
    # SLIDE 10: Statistical Tests & Bland-Altman Agreement
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "9. Hypothesis Testing & Bland-Altman Agreement", "Statistical Rigor")

    tb10_l = s10.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(5.8), Inches(5.6))
    tf10_l = tb10_l.text_frame
    tf10_l.word_wrap = True

    p = tf10_l.paragraphs[0]
    p.text = "Rigorous Verification of Concordance"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = NAVY
    p.space_after = Pt(8)

    p = tf10_l.add_paragraph()
    p.text = "1. Shapiro-Wilk Normality Test:\n" \
             "    p = 1.98 × 10⁻¹³ (Differences are non-normal; requires non-parametric hypothesis testing).\n\n" \
             "2. Wilcoxon Signed-Rank Test:\n" \
             "    W = 0, p = 0.00065 (Statistically significant difference at α = 0.05).\n" \
             "    Effect Size (Cohen's d): 0.4201 (Small/Moderate effect).\n\n" \
             "3. Bland-Altman Glacier Area Agreement:\n" \
             "    • Mean Bias (d̄): +0.0175 km² (Minimal systematic bias)\n" \
             "    • 95% Limits of Agreement: [-0.064 km², +0.099 km²]\n" \
             "    • Concordance: 92.1% of catchment tiles fall strictly within ±1.96 SD."
    p.font.size = Pt(12)
    p.font.color.rgb = DARK

    # Right side: Embed Bland-Altman plot
    ba_img = os.path.join(figures_dir, "bland_altman_glacier_area.png")
    if os.path.exists(ba_img):
        s10.shapes.add_picture(ba_img, Inches(7.0), Inches(1.5), width=Inches(5.5))

    s10.notes_slide.notes_text_frame.text = (
        "Slide 10 highlights statistical rigor: correlation alone does not prove agreement! We ran the Shapiro-Wilk test, "
        "which showed differences were non-normal, leading us to use the Wilcoxon signed-rank test. While p is less than 0.05, "
        "Cohen's d effect size is only 0.42. The Bland-Altman plot on the right proves that mean bias is only 0.0175 sq km, "
        "and 92.1% of sub-basins fall within the 95% limits of agreement."
    )

    # ==========================================
    # SLIDE 11: Findings & Limitations
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "10. Key Findings & Scientific Limitations", "Critical Evaluation")

    # Left card: Key Findings
    card_l = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.4), Inches(5.6), Inches(5.5))
    card_l.fill.solid()
    card_l.fill.fore_color.rgb = BG_LIGHT
    card_l.line.color.rgb = TEAL
    card_l.line.width = Pt(1.5)

    tb11_l = s11.shapes.add_textbox(Inches(1.0), Inches(1.6), Inches(5.2), Inches(5.1))
    tf11_l = tb11_l.text_frame
    tf11_l.word_wrap = True

    p = tf11_l.paragraphs[0]
    p.text = "Key Scientific Findings"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = TEAL
    p.space_after = Pt(10)

    p = tf11_l.add_paragraph()
    p.text = "✔ Sensor Interchangeability: NASA HLS Sentinel-2 and Landsat 8/9 can be safely merged into unified cryospheric time series.\n\n" \
             "✔ Radiometric Alignment: NDSI exhibits R² > 0.98, proving that ice/snow classification boundaries are consistent across sensors.\n\n" \
             "✔ Terminus Sensitivity: Discrepancies are confined to mixed-pixel debris cover, where attention-gated neural networks are required.\n\n" \
             "✔ Avoiding False Retreat: Without this statistical baseline, an investigator might misinterpret the 1.1 km² difference as real glacier loss."
    p.font.size = Pt(12)
    p.font.color.rgb = DARK

    # Right card: Limitations
    card_r = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.4), Inches(5.6), Inches(5.5))
    card_r.fill.solid()
    card_r.fill.fore_color.rgb = BG_LIGHT
    card_r.line.color.rgb = CORAL
    card_r.line.width = Pt(1.5)

    tb11_r = s11.shapes.add_textbox(Inches(7.1), Inches(1.6), Inches(5.2), Inches(5.1))
    tf11_r = tb11_r.text_frame
    tf11_r.word_wrap = True

    p = tf11_r.paragraphs[0]
    p.text = "Identified Limitations"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = CORAL
    p.space_after = Pt(10)

    p = tf11_r.add_paragraph()
    p.text = "⚠ Ephemeral Snow Flurries: Slight overpass date offsets during the ablation season capture minor diurnal melt variations.\n\n" \
             "⚠ Deep Alpine Topographic Shadows: Shadowed valley walls compress dynamic reflectance ranges, increasing noise.\n\n" \
             "⚠ Spatial Resolution Boundary Effects: At 30 m resolution, glacier tongues narrower than ~60 m suffer from partial volume mixing.\n\n" \
             "⚠ Debris-Cover Spectral Mimicry: Heavy morainic rocks exhibit rock-like NDSI, requiring DEM elevation & slope integration."
    p.font.size = Pt(12)
    p.font.color.rgb = DARK

    s11.notes_slide.notes_text_frame.text = (
        "Slide 11 addresses findings and limitations. The crucial takeaway is avoiding false retreat: someone comparing a 2024 "
        "Sentinel image to a 2025 Landsat image might falsely claim Gangotri lost 1.1 sq km of ice, when in reality that is "
        "simply the inter-sensor boundary uncertainty. We also transparently document limitations like topographic shadowing and debris."
    )

    # ==========================================
    # SLIDE 12: Conclusion & Future Scope
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    bg12 = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg12.fill.solid()
    bg12.fill.fore_color.rgb = NAVY
    bg12.line.fill.background()

    tb12 = s12.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(10.933), Inches(5.5))
    tf12 = tb12.text_frame
    tf12.word_wrap = True

    p = tf12.paragraphs[0]
    p.text = "Conclusions & Future Research Directions"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.space_after = Pt(20)

    p = tf12.add_paragraph()
    p.text = "1. Proven Scientific Feasibility: NASA HLS Sentinel-2 (HLSS30) and Landsat 8/9 (HLSL30) achieve 98.61% pixel agreement and Cohen's κ = 0.8967 over Gangotri Glacier, establishing them as robust, interchangeable data streams for cryosphere monitoring.\n\n" \
             "2. Validated Attention U-Net Integration: Our 8-channel multispectral architecture successfully leverages both optical reflectance and physical indices (NDSI/NDVI) to segment glaciers without being fooled by mountain shadow noise.\n\n" \
             "3. Future Scope — Thermal & SAR Fusion: Integrating Sentinel-1 Synthetic Aperture Radar (SAR) coherence and Landsat TIRS thermal infrared band to penetrate debris cover and delineate the terminus in all weather conditions.\n\n" \
             "4. Temporal Time-Series Modeling: Expanding this single-season comparative benchmark into a 10-year decadal glacier shrinkage and mass balance tracking framework across all 14,000+ glaciers in RGI Region 14."
    p.font.size = Pt(13.5)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.space_after = Pt(24)

    p_end = tf12.add_paragraph()
    p_end.text = "Thank you! We welcome questions from the evaluation committee."
    p_end.font.size = Pt(16)
    p_end.font.bold = True
    p_end.font.color.rgb = TEAL

    s12.notes_slide.notes_text_frame.text = (
        "In conclusion, our research provides the statistical baseline necessary for reliable cryospheric remote sensing. "
        "Sentinel-2 and Landsat 8/9 are proven to be highly consistent, and our 8-channel Attention U-Net framework is robust. "
        "In future work, we plan to fuse Sentinel-1 SAR and thermal bands to tackle debris cover across the wider Himalayas. "
        "Thank you very much. We are happy to take any questions."
    )

    print(f"[*] Building 12-slide PowerPoint presentation at: {output_pptx_path}...")
    prs.save(output_pptx_path)
    print(f"[✓] Successfully generated PowerPoint presentation! File size: {os.path.getsize(output_pptx_path):,} bytes")
    return output_pptx_path

if __name__ == "__main__":
    pptx_path = "/Users/rameshwar/.gemini/antigravity/scratch/glacier_statistical_analysis/presentation_package/presentation/Gangotri_Glacier_MultiSatellite_2025.pptx"
    fig_dir = "/Users/rameshwar/.gemini/antigravity/scratch/glacier_statistical_analysis/presentation_package/dashboard/figures"
    create_presentation(pptx_path, fig_dir)
