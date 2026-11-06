# Gangotri Glacier Research Presentation Package (2025)

**Project Title:** Multi-Satellite Glacier Statistical Analysis  
**Study Area:** Gangotri Glacier, Uttarakhand, India (RGI Region 14: South Asia West)  
**Constellations:** NASA Harmonized Landsat Sentinel-2 (HLS v2 at 30 m): `HLSS30 v002` vs. `HLSL30 v002`  
**Team:** Rameshwar Chandravanshi • Piyush Verma • Deepanshu Sahu (NIT Raipur)  

---

## 📦 Package Deliverables Summary

This presentation package contains three primary academic deliverables:

```
presentation_package/
├── report/
│   ├── build_pdf_report.py                   # ReportLab automated compiler
│   └── Gangotri_Glacier_Research_Report.pdf  # Final academic PDF research report (1.35 MB)
│
├── presentation/
│   ├── build_presentation.py                 # python-pptx widescreen slide generator
│   └── Gangotri_Glacier_MultiSatellite_2025.pptx # Final 12-slide presentation with speaker notes (1.20 MB)
│
├── dashboard/
│   ├── app.py                                # Full-featured Streamlit interactive web app
│   ├── requirements.txt                      # Standalone deployment manifest
│   ├── README.md                             # Local & Streamlit Cloud deployment guide
│   ├── .streamlit/config.toml                # Custom theme configuration
│   ├── data/                                 # 5 exported CSV datasets
│   └── figures/                              # 5 publication-ready PNG figures
│
└── README.md                                 # Package index documentation
```

---

## 🎯 Verification & Deliverables Checklist

| Deliverable | Path | Format | Status | Notes |
| :--- | :--- | :---: | :---: | :--- |
| **Academic Report** | `report/Gangotri_Glacier_Research_Report.pdf` | PDF | **VERIFIED** | 1.35 MB, 17 sections, numbered canvas, embedded figures |
| **Slide Deck** | `presentation/Gangotri_Glacier_MultiSatellite_2025.pptx` | PPTX | **VERIFIED** | 1.20 MB, 12 widescreen slides, complete speaker notes |
| **Interactive Dashboard**| `dashboard/app.py` | Web App | **VERIFIED** | Streamlit + Plotly + Folium, zero-GEE standalone execution |
| **Statistical CSVs** | `dashboard/data/*.csv` | CSV | **VERIFIED** | 5 structured datasets (Area, Patches, Regression, Hypotheses, Bands) |
| **High-Res Figures** | `dashboard/figures/*.png` | PNG | **VERIFIED** | 5 figures (Bland-Altman, NDSI scatter, Area scatter, Map, Violin) |
