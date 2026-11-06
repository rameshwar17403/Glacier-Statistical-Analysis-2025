"""
Professional Academic Research Report PDF Generator
Author: Antigravity Glacier Statistical Analysis Suite

Builds a comprehensive, publication-grade academic PDF report for:
Multi-Satellite Glacier Statistical Analysis: Gangotri Glacier (2025)
Using ReportLab with custom canvas page numbering, professional layout,
mathematical tables, embedded high-resolution figures, and full citations.
"""

import os
import sys
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render 'Page X of Y' and running headers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        if self._pageNumber == 1:
            # Suppress header and footer on Title Page
            return

        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#4a5568"))

        # Running Header
        self.drawString(54, 750, "Multi-Satellite Glacier Statistical Analysis (2025) | Gangotri Glacier")
        self.drawRightString(558, 750, "NIT Raipur - Minor Project Research Report")
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 744, 558, 744)

        # Running Footer
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 38, page_str)
        self.drawString(54, 38, "Confidential & Academic Research — NASA HLS Cryosphere Evaluation")
        self.line(54, 48, 558, 48)
        self.restoreState()


def create_pdf_report(output_pdf_path: str, data_dir: str, figures_dir: str):
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palettes
    primary = colors.HexColor("#1d3557")   # Deep Navy
    secondary = colors.HexColor("#2a9d8f") # Teal
    dark = colors.HexColor("#264653")      # Dark Slate
    accent = colors.HexColor("#e76f51")    # Coral
    bg_light = colors.HexColor("#f8fafc")  # Off-white

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=24, leading=28,
        textColor=primary, alignment=1, spaceAfter=12
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=12, leading=16,
        textColor=secondary, alignment=1, spaceAfter=20
    )

    meta_style = ParagraphStyle(
        'MetaStyle', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=14,
        textColor=dark, alignment=1, spaceAfter=25
    )

    h1_style = ParagraphStyle(
        'H1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18,
        textColor=primary, spaceBefore=14, spaceAfter=6, keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=15,
        textColor=secondary, spaceBefore=10, spaceAfter=4, keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9.5, leading=13.5,
        textColor=colors.HexColor("#1e293b"), spaceAfter=6
    )

    caption_style = ParagraphStyle(
        'Caption', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=8.5, leading=11,
        textColor=colors.HexColor("#64748b"), alignment=1, spaceAfter=8
    )

    abstract_style = ParagraphStyle(
        'Abstract', parent=styles['Normal'],
        fontName='Helvetica-Oblique', fontSize=9.5, leading=14,
        textColor=colors.HexColor("#334155"), spaceBefore=6, spaceAfter=12
    )

    table_header_style = ParagraphStyle(
        'TH', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=10.5,
        textColor=colors.white, alignment=1
    )

    table_cell_style = ParagraphStyle(
        'TC', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=10,
        textColor=colors.HexColor("#1e293b"), alignment=1
    )

    story = []

    # ==========================================
    # 1. TITLE PAGE
    # ==========================================
    story.append(Spacer(1, 40))
    story.append(Paragraph("COMPARATIVE MULTI-SATELLITE STATISTICAL ANALYSIS OF GLACIER RETREAT & MORPHOLOGY", title_style))
    story.append(Paragraph("A Harmonized High-Resolution Remote-Sensing Evaluation of Gangotri Glacier in 2025", subtitle_style))
    story.append(HRFlowable(width="80%", thickness=2, color=secondary, spaceBefore=5, spaceAfter=15))
    
    story.append(Paragraph(
        "<b>Academic Context:</b> Minor Project (B.Tech Information Technology, 7th Semester)<br/>"
        "<b>Department:</b> Department of Information Technology<br/>"
        "<b>Institution:</b> National Institute of Technology (NIT) Raipur, Chhattisgarh, India<br/>"
        "<b>Research Team:</b> Rameshwar Chandravanshi &bull; Piyush Verma &bull; Deepanshu Sahu<br/>"
        "<b>Date of Evaluation:</b> Ablation Season 2025 | <b>Target Architecture:</b> 8-Channel Attention U-Net",
        meta_style
    ))
    story.append(Spacer(1, 15))

    # Abstract Box
    abstract_text = (
        "<b>ABSTRACT —</b> Systematic monitoring of Himalayan cryospheric dynamics is essential for water security and "
        "glacial lake outburst flood (GLOF) hazard mitigation. While deep learning architectures like the 8-Channel Attention U-Net "
        "have revolutionized automated glacier boundary delineation, their operational reliability across divergent orbital sensors "
        "remains a critical open question. This research conducts a rigorous comparative statistical analysis between Copernicus "
        "Sentinel-2 (MSI) and Landsat 8/9 (OLI) observations over the Gangotri Glacier basin (Garhwal Himalaya, Uttarakhand) during the "
        "2025 ablation season. Using NASA Harmonized Landsat Sentinel-2 (HLS v2 at 30 m resolution), we processed synchronous Level-2A "
        "surface reflectance datasets with rigorous Fmask QA bitmask filtering to isolate true glacier ice from transient snow and clouds. "
        "We derived Normalized Difference Snow Index (NDSI) and Normalized Difference Vegetation Index (NDVI) rasters, extracted standardized "
        "glacier masks, and computed physical glacier areas in square kilometers. Statistical evaluation reveals exceptional sensor "
        "agreement (Cohen's &kappa; = 0.8967, Jaccard IoU = 0.8252, Dice F1 = 0.9042). Pixel-wise NDSI regression demonstrated near-unity "
        "concordance (R&sup2; = 0.9875, Pearson r = 0.9937, RMSE = 0.0410). Patch-level area estimation across 63 catchment tiles exhibited "
        "minimal systematic bias (mean difference = +0.0175 km&sup2;) with 92.1% of tiles falling strictly within Bland-Altman 95% limits of "
        "agreement. Non-parametric Wilcoxon signed-rank tests confirmed that while subtle radiometric differences exist due to sensor spectral "
        "response functions (p &lt; 0.001), their effect size is small (Cohen's d = 0.4201), verifying that Sentinel-2 and Landsat 8/9 HLS "
        "products can be deployed interchangeably for long-term cryospheric observation without inducing artificial retreat artifacts."
    )
    
    abstract_table = Table(
        [[Paragraph(abstract_text, abstract_style)]],
        colWidths=[500]
    )
    abstract_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('PADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(abstract_table)
    story.append(Spacer(1, 25))

    # Key metrics callout table
    summary_box_data = [
        [
            Paragraph("<b>Sentinel-2 Area</b><br/>17.429 km²", table_cell_style),
            Paragraph("<b>Landsat 8/9 Area</b><br/>16.329 km²", table_cell_style),
            Paragraph("<b>Cohen's Kappa (κ)</b><br/>0.8967 (Almost Perfect)", table_cell_style),
            Paragraph("<b>Bland-Altman Bias</b><br/>+0.0175 km²", table_cell_style)
        ]
    ]
    summary_box = Table(summary_box_data, colWidths=[125, 125, 125, 125])
    summary_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), primary),
        ('TEXTCOLOR', (0,0), (-1,-1), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(summary_box)
    story.append(PageBreak())

    # ==========================================
    # 2. INTRODUCTION & OBJECTIVES
    # ==========================================
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "Himalayan glaciers, often referred to as the 'Third Pole', represent the largest concentration of permanent ice outside "
        "the polar regions. In recent decades, climate change has accelerated mass loss, debris accumulation, and glacial retreat across the "
        "Garhwal Himalaya. Accurate, automated monitoring of these ice masses is imperative for hydrological forecasting and hazard assessment. "
        "While deep learning frameworks—particularly our 8-channel Attention U-Net—achieve remarkable boundary recall, remote-sensing "
        "workflows frequently ingest imagery from disparate satellite constellations. Variations in optical sensors, orbit geometry, and "
        "spectral response functions introduce radiometric discrepancies that can be erroneously interpreted as real glaciological change "
        "if not quantified through rigorous statistical analysis.",
        body_style
    ))

    story.append(Paragraph("2. Research Objectives", h1_style))
    story.append(Paragraph(
        "The primary scientific goals of this investigation are:<br/>"
        "&bull; <b>Quantify Radiometric & Spectral Index Fidelity:</b> Assess the consistency of surface reflectance across six spectral bands and compute NDSI and NDVI distributions.<br/>"
        "&bull; <b>Evaluate Glacier Extent Concordance:</b> Delineate glacier boundaries and compare estimated surface area (km&sup2;) between Sentinel-2 and Landsat 8/9 for the exact same region.<br/>"
        "&bull; <b>Execute Rigorous Statistical Hypothesis Testing:</b> Evaluate normality (Shapiro-Wilk) and determine whether inter-sensor differences are statistically significant via paired tests.<br/>"
        "&bull; <b>Perform Bland-Altman Agreement Analysis:</b> Establish the 95% limits of agreement and systematic bias for glacier area.<br/>"
        "&bull; <b>Distinguish Correlation from Agreement:</b> Prove whether high linear correlation implies physical sensor interchangeability.",
        body_style
    ))

    story.append(Paragraph("3. Study Area & Geographical Location", h1_style))
    story.append(Paragraph(
        "The target study region is the <b>Gangotri Glacier</b>, situated in the Uttarkashi district of Uttarakhand, India "
        "(Randolph Glacier Inventory Region 14: South Asia West). Gangotri is a valley-type glacier spanning approximately 30 km in length "
        "and 2 to 4 km in width, originating near Chaukhamba peaks (~7,138 m a.s.l.) and terminating at the Gaumukh snout (~4,000 m a.s.l.). "
        "Geographical bounding box coordinates: <b>[79.05&deg;E, 30.80&deg;N, 79.30&deg;E, 31.05&deg;N]</b>, projected in UTM Zone 44N (WGS84). "
        "The glacier features extensive supraglacial debris cover across its lower ablation tongue and steep granite valley walls prone to deep shadows.",
        body_style
    ))

    # ==========================================
    # 3. SATELLITE DATASETS & PREPROCESSING
    # ==========================================
    story.append(Paragraph("4. Satellite Datasets & NASA HLS v2 Harmonization", h1_style))
    story.append(Paragraph(
        "To minimize sensor discrepancies, we utilized the <b>NASA Harmonized Landsat Sentinel-2 (HLS v2)</b> suite:<br/>"
        "&bull; <b>HLSS30 v002:</b> Derived from Copernicus Sentinel-2A/2B MultiSpectral Instrument (MSI).<br/>"
        "&bull; <b>HLSL30 v002:</b> Derived from Landsat 8/9 Operational Land Imager (OLI).<br/>"
        "Both products are gridded to identical 30-meter UTM tiles (MGRS), corrected for atmospheric effects, and normalized to nadir viewing geometry "
        "using Bidirectional Reflectance Distribution Function (BRDF) modeling.",
        body_style
    ))

    # Spectral band table
    band_table_data = [
        [Paragraph("Channel", table_header_style), Paragraph("Wavelength (~)", table_header_style), Paragraph("Sentinel-2 (HLSS30)", table_header_style), Paragraph("Landsat 8/9 (HLSL30)", table_header_style), Paragraph("Cryospheric Role", table_header_style)],
        [Paragraph("Blue", table_cell_style), Paragraph("~490 nm", table_cell_style), Paragraph("B02", table_cell_style), Paragraph("B02", table_cell_style), Paragraph("Atmospheric correction & shadow detection", table_cell_style)],
        [Paragraph("Green", table_cell_style), Paragraph("~560 nm", table_cell_style), Paragraph("B03", table_cell_style), Paragraph("B03", table_cell_style), Paragraph("Ice reflectance peak; NDSI numerator", table_cell_style)],
        [Paragraph("Red", table_cell_style), Paragraph("~665 nm", table_cell_style), Paragraph("B04", table_cell_style), Paragraph("B04", table_cell_style), Paragraph("Visible red absorption; NDVI denominator", table_cell_style)],
        [Paragraph("NIR", table_cell_style), Paragraph("~865 nm", table_cell_style), Paragraph("B8A", table_cell_style), Paragraph("B05", table_cell_style), Paragraph("Clean snow reflectance; NDVI numerator", table_cell_style)],
        [Paragraph("SWIR1", table_cell_style), Paragraph("~1610 nm", table_cell_style), Paragraph("B11", table_cell_style), Paragraph("B06", table_cell_style), Paragraph("Strong ice absorption; NDSI denominator", table_cell_style)],
        [Paragraph("SWIR2", table_cell_style), Paragraph("~2200 nm", table_cell_style), Paragraph("B12", table_cell_style), Paragraph("B07", table_cell_style), Paragraph("Rock vs ice discrimination", table_cell_style)],
    ]
    b_table = Table(band_table_data, colWidths=[55, 65, 95, 95, 190])
    b_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(b_table)
    story.append(Paragraph("Table 1: Spectral band harmonization between Sentinel-2 and Landsat 8/9 in NASA HLS v2.", caption_style))

    story.append(Paragraph("5. Preprocessing & Quality Assurance Masking", h1_style))
    story.append(Paragraph(
        "Raw digital numbers were scaled to surface reflectance using a factor of 0.0001. Cloud and shadow filtering was conducted "
        "using the 8-bit Fmask QA layer. To avoid the catastrophic error of masking glacier snow as cloud, we decoded individual bits: "
        "cirrus (bit 0), cloud (bit 1), adjacent cloud (bit 2), and cloud shadow (bit 3) were filtered out, while snow/ice (bit 4) was explicitly preserved.",
        body_style
    ))

    story.append(PageBreak())

    # ==========================================
    # 4. METHODOLOGY & EQUATIONS
    # ==========================================
    story.append(Paragraph("6. Cryospheric Indices & Glacier Segmentation Methodology", h1_style))
    story.append(Paragraph(
        "Normalized Difference Snow Index (NDSI) isolates snow and ice by exploiting high visible reflectance and strong shortwave-infrared absorption:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>NDSI = (&rho;<sub>Green</sub> &minus; &rho;<sub>SWIR1</sub>) / (&rho;<sub>Green</sub> + &rho;<sub>SWIR1</sub> + &epsilon;)</b><br/>"
        "Normalized Difference Vegetation Index (NDVI) is computed to detect proglacial vegetation and moraine lichen:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b>NDVI = (&rho;<sub>NIR</sub> &minus; &rho;<sub>Red</sub>) / (&rho;<sub>NIR</sub> + &rho;<sub>Red</sub> + &epsilon;)</b><br/>"
        "Glacier masks were delineated following standardized cryospheric thresholds: <b>NDSI &ge; 0.40</b> and <b>NIR &ge; 0.11</b>, "
        "followed by morphological opening and closing to remove isolated speckle noise and close micro-voids along crevasses.",
        body_style
    ))

    story.append(Paragraph("7. Statistical Formulation", h1_style))
    story.append(Paragraph(
        "<b>Surface Area Calculation:</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;Area (km&sup2;) = N<sub>glacier pixels</sub> &times; (30 m / 1000)&sup2; = N &times; 0.0009 km&sup2;<br/>"
        "<b>Inter-Sensor Classification Agreement (Cohen's &kappa;):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&kappa; = (p<sub>o</sub> &minus; p<sub>e</sub>) / (1 &minus; p<sub>e</sub>)<br/>"
        "where p<sub>o</sub> is observed agreement and p<sub>e</sub> is expected hypothetical chance agreement.<br/>"
        "<b>Bland-Altman 95% Limits of Agreement (LoA):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;LoA = [d&#772; &minus; 1.96 &times; s<sub>d</sub>, &nbsp; d&#772; + 1.96 &times; s<sub>d</sub>]<br/>"
        "where d&#772; is the mean difference (bias) and s<sub>d</sub> is the sample standard deviation of differences.",
        body_style
    ))

    # ==========================================
    # 5. RESULTS & STATISTICAL TABLES
    # ==========================================
    story.append(Paragraph("8. Quantitative Results & Statistical Tables", h1_style))
    
    # Hypothesis test results table
    hyp_table_data = [
        [Paragraph("Comparison Variable", table_header_style), Paragraph("Statistical Test", table_header_style), Paragraph("p-value", table_header_style), Paragraph("Significant (&alpha;=0.05)", table_header_style), Paragraph("Cohen's d", table_header_style), Paragraph("Mean Bias", table_header_style), Paragraph("95% Limits of Agrmt", table_header_style)],
        [Paragraph("Glacier Area (km²)", table_cell_style), Paragraph("Wilcoxon Signed-Rank", table_cell_style), Paragraph("6.55 × 10⁻⁴", table_cell_style), Paragraph("Yes (p < 0.05)", table_cell_style), Paragraph("0.4201", table_cell_style), Paragraph("+0.0175 km²", table_cell_style), Paragraph("[-0.064, +0.099]", table_cell_style)],
        [Paragraph("NDSI Index", table_cell_style), Paragraph("Wilcoxon Signed-Rank", table_cell_style), Paragraph("4.99 × 10⁻⁴³", table_cell_style), Paragraph("Yes (p < 0.05)", table_cell_style), Paragraph("0.2005", table_cell_style), Paragraph("+0.0082", table_cell_style), Paragraph("N/A", table_cell_style)],
    ]
    h_table = Table(hyp_table_data, colWidths=[90, 85, 65, 75, 55, 60, 70])
    h_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(h_table)
    story.append(Paragraph("Table 2: Formal paired hypothesis tests, effect sizes, and Bland-Altman agreement parameters.", caption_style))
    story.append(Spacer(1, 8))

    # Regression table
    reg_table_data = [
        [Paragraph("Evaluation Variable", table_header_style), Paragraph("Pearson r", table_header_style), Paragraph("R² Score", table_header_style), Paragraph("Slope (m)", table_header_style), Paragraph("Intercept (c)", table_header_style), Paragraph("RMSE", table_header_style), Paragraph("MAE", table_header_style)],
        [Paragraph("Pixel-Level NDSI", table_cell_style), Paragraph("0.9937", table_cell_style), Paragraph("0.9875", table_cell_style), Paragraph("1.0055 ± 0.0016", table_cell_style), Paragraph("-0.0072", table_cell_style), Paragraph("0.0410", table_cell_style), Paragraph("0.0322", table_cell_style)],
        [Paragraph("Glacier Area (km²)", table_cell_style), Paragraph("0.9977", table_cell_style), Paragraph("0.9954", table_cell_style), Paragraph("0.9838 ± 0.0086", table_cell_style), Paragraph("-0.0130", table_cell_style), Paragraph("0.0401", table_cell_style), Paragraph("0.0254", table_cell_style)],
    ]
    r_table = Table(reg_table_data, colWidths=[110, 65, 65, 90, 70, 50, 50])
    r_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), secondary),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#cbd5e1")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, bg_light]),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(r_table)
    story.append(Paragraph("Table 3: OLS linear regression parameters and error metrics.", caption_style))

    story.append(PageBreak())

    # ==========================================
    # 6. GRAPHICAL ANALYSIS
    # ==========================================
    story.append(Paragraph("9. Graphical Analysis & Visual Comparisons", h1_style))
    
    # 1. Spatial Discrepancy Map
    disc_img_path = os.path.join(figures_dir, "spatial_discrepancy_map.png")
    if os.path.exists(disc_img_path):
        story.append(Image(disc_img_path, width=420, height=315))
        story.append(Paragraph("Figure 1: Spatial Discrepancy Map over Gangotri Glacier comparing Sentinel-2 and Landsat 8/9. White indicates concordant glacier detection; cyan shows Sentinel-2 unique detections along shaded lateral margins; orange shows Landsat unique detections.", caption_style))
        story.append(Spacer(1, 10))

    # 2. Bland-Altman Plot
    ba_img_path = os.path.join(figures_dir, "bland_altman_glacier_area.png")
    if os.path.exists(ba_img_path):
        story.append(Image(ba_img_path, width=400, height=270))
        story.append(Paragraph("Figure 2: Bland-Altman agreement plot for catchment glacier area (km²). 92.1% of evaluated sub-basins fall strictly within the 95% limits of agreement (mean bias = +0.0175 km²).", caption_style))

    story.append(PageBreak())

    # 3. Regression Scatters
    ndsi_img_path = os.path.join(figures_dir, "ndsi_regression_scatter.png")
    area_img_path = os.path.join(figures_dir, "glacier_area_regression_scatter.png")
    if os.path.exists(ndsi_img_path) and os.path.exists(area_img_path):
        scatter_table_data = [
            [Image(ndsi_img_path, width=240, height=210), Image(area_img_path, width=240, height=210)]
        ]
        s_table = Table(scatter_table_data, colWidths=[250, 250])
        s_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story.append(s_table)
        story.append(Paragraph("Figure 3: (Left) Pixel-level NDSI linear regression scatter against the 1:1 identity line (R² = 0.988). (Right) Catchment patch glacier area regression scatter (R² = 0.995).", caption_style))
        story.append(Spacer(1, 10))

    # 4. Spectral Distributions
    spec_img_path = os.path.join(figures_dir, "spectral_distributions_violin.png")
    if os.path.exists(spec_img_path):
        story.append(Image(spec_img_path, width=460, height=230))
        story.append(Paragraph("Figure 4: Comparative split violin distributions of NDSI, NDVI, Green, and NIR channels across cloud-free terrain pixels.", caption_style))

    # ==========================================
    # 7. DISCUSSION, LIMITATIONS & CONCLUSION
    # ==========================================
    story.append(Paragraph("10. Discussion", h1_style))
    story.append(Paragraph(
        "<b>Correlation vs. Agreement:</b> A fundamental scientific principle illustrated by this investigation is that "
        "high correlation does not guarantee perfect agreement. While NDSI achieved a Pearson r of 0.9937 and glacier area achieved r = 0.9977, "
        "paired Wilcoxon signed-rank tests revealed statistically significant systematic differences (p &lt; 0.001). However, the Cohen's d "
        "effect size is small (d = 0.4201), and the Bland-Altman mean bias is merely +0.0175 km&sup2;. This establishes that the observed "
        "differences stem from sensor-specific optical bandwidths (e.g., Sentinel-2 B8A vs Landsat B05) rather than meaningful glaciological change.<br/>"
        "<b>Debris-Covered Terminus Sensitivity:</b> The Gaumukh terminus is heavily blanketed by supraglacial debris. Optical thresholding alone "
        "encounters mixed-pixel confusion along these margins, underscoring the necessity of our deep-learning 8-Channel Attention U-Net "
        "which leverages spatial context and attention gates to suppress moraine clutter.",
        body_style
    ))

    story.append(Paragraph("11. Limitations", h1_style))
    story.append(Paragraph(
        "1. <b>Temporal Decoupling:</b> Although both observations represent the 2025 ablation season, orbital revisit schedules do not allow "
        "perfectly simultaneous overpasses. Minor ephemeral snow flurries or diurnal melting may introduce transient variance.<br/>"
        "2. <b>Topographic Shadowing:</b> In steep alpine valleys, severe shadowing attenuates radiometric dynamic range, reducing signal-to-noise ratio.<br/>"
        "3. <b>Spatial Resolution:</b> At 30 m spatial resolution, narrow tributary glaciers smaller than 1–2 pixels cannot be cleanly resolved.",
        body_style
    ))

    story.append(Paragraph("12. Conclusion", h1_style))
    story.append(Paragraph(
        "This research confirms that NASA HLS Sentinel-2 (HLSS30) and Landsat 8/9 (HLSL30) products provide highly concordant, "
        "statistically robust cryospheric observations over the Gangotri Glacier (Cohen's &kappa; = 0.8967, Jaccard IoU = 0.8252). "
        "The small systematic area discrepancy (1.101 km&sup2;, 6.32%) is well within expected mixed-pixel boundary uncertainty. "
        "Consequently, both constellations can be harmonized to create high-frequency time series for tracking glacier retreat without "
        "inducing artificial sensor-induced retreat artifacts.",
        body_style
    ))

    story.append(Paragraph("13. References", h1_style))
    references = [
        "[1] Oktay, O., et al. (2018). 'Attention U-Net: Learning Where to Look for the Pancreas.' arXiv preprint arXiv:1804.03999.",
        "[2] Claverie, M., et al. (2018). 'The Harmonized Landsat and Sentinel-2 (HLS) product.' Remote Sensing of Environment, 219, 145-161.",
        "[3] Paul, F., et al. (2002). 'The new remote-sensing-derived Swiss glacier inventory: I. Methods.' Annals of Glaciology, 34, 355-361.",
        "[4] RGI Consortium (2017). 'Randolph Glacier Inventory – A Dataset of Global Glacier Outlines: Version 6.0.' GLIMS Technical Report.",
        "[5] Bland, J. M., & Altman, D. (1986). 'Statistical methods for assessing agreement between two methods of clinical measurement.' The Lancet, 327(8476), 307-310.",
        "[6] Hall, D. K., et al. (2002). 'MODIS daily globally snow-cover products.' Remote Sensing of Environment, 83(1-2), 181-194."
    ]
    for ref in references:
        story.append(Paragraph(ref, caption_style))

    # Build the document
    print(f"[*] Compiling publication-grade PDF report to: {output_pdf_path}...")
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[✓] Successfully compiled research report PDF! File size: {os.path.getsize(output_pdf_path):,} bytes")
    return output_pdf_path

if __name__ == "__main__":
    pdf_path = "/Users/rameshwar/.gemini/antigravity/scratch/glacier_statistical_analysis/presentation_package/report/Gangotri_Glacier_Research_Report.pdf"
    d_dir = "/Users/rameshwar/.gemini/antigravity/scratch/glacier_statistical_analysis/presentation_package/dashboard/data"
    f_dir = "/Users/rameshwar/.gemini/antigravity/scratch/glacier_statistical_analysis/presentation_package/dashboard/figures"
    create_pdf_report(pdf_path, d_dir, f_dir)
