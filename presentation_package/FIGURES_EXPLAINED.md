# Comprehensive Guide to All 5 Statistical Figures
**Project:** Multi-Satellite Glacier Statistical Analysis: Gangotri Glacier (2025)  
**Authors:** Rameshwar Chandravanshi • Piyush Verma • Deepanshu Sahu (NIT Raipur)

---

## 1. Bland-Altman Agreement Plot
**File:** `bland_altman_glacier_area.png`  
**Location:** Slide 10 in PPTX | Figure 2 in PDF Report | "🔍 Regression & Bland-Altman" in Dashboard

![Bland-Altman Agreement Plot](/Users/rameshwar/.gemini/antigravity/brain/208fa0aa-b181-481b-bac3-615121f02011/figures/bland_altman_glacier_area.png)

### Anatomy of the Plot:
* **X-axis (Horizontal):** Mean Estimated Glacier Area: $\frac{\text{Area}_{\text{Sentinel-2}} + \text{Area}_{\text{Landsat}}}{2}$ (in $\text{km}^2$). Represents the average size of each catchment patch.
* **Y-axis (Vertical):** Difference in Glacier Area: $\text{Area}_{\text{Sentinel-2}} - \text{Area}_{\text{Landsat}}$ (in $\text{km}^2$).
* **Blue Scatter Dots:** Each of the 63 evaluated sub-basin patches across the Gangotri catchment.
* **Red Dashed Line ($\bar{d}$):** **Mean Systematic Bias = $+0.0175 \text{ km}^2$**.
* **Gray Dotted Lines:** **95% Limits of Agreement (LoA)**:
  * Upper Limit: $+0.099 \text{ km}^2$ ($\bar{d} + 1.96 \cdot s_d$)
  * Lower Limit: $-0.064 \text{ km}^2$ ($\bar{d} - 1.96 \cdot s_d$)
* **Light Blue Shaded Region:** The 95% Confidence Interval envelope.

### Scientific Interpretation:
1. **Zero Proximity:** The mean bias line ($+0.0175 \text{ km}^2$) is nearly indistinguishable from zero, demonstrating that Sentinel-2 has only a microscopic positive bias over Landsat per patch (~0.018 km²).
2. **Homoscedasticity:** Notice that the scatter of dots does not flare out into a cone as patch size increases along the X-axis. This proves that sensor agreement does not degrade on larger, deeper glacier sections.
3. **92.1% In-Bounds Concordance:** 58 out of 63 tiles fall strictly inside the limits of agreement, meeting remote-sensing interchangeability criteria.

### What to Say to Examiners:
> *"Respected professors, Figure 1 is our Bland-Altman agreement plot. While correlation only tests linear association, Bland-Altman tests true measurement agreement. The Y-axis plots the difference between Sentinel-2 and Landsat area against their mean. Notice that the red dashed bias line is almost zero (+0.0175 km²), and over 92% of sub-basins fall cleanly inside the ±1.96 standard deviation limits. This proves that both sensors can be used interchangeably without systematic distortion."*

---

## 2. NDSI Linear Regression & 1:1 Identity Scatter
**File:** `ndsi_regression_scatter.png`  
**Location:** Slide 9 in PPTX | Figure 3 (Left) in PDF Report | "🔍 Regression & Bland-Altman" in Dashboard

![NDSI Linear Regression Scatter](/Users/rameshwar/.gemini/antigravity/brain/208fa0aa-b181-481b-bac3-615121f02011/figures/ndsi_regression_scatter.png)

### Anatomy of the Plot:
* **X-axis:** Sentinel-2 (HLSS30) NDSI $[-1.0, 1.0]$.
* **Y-axis:** Landsat 8/9 (HLSL30) NDSI $[-1.0, 1.0]$.
* **Teal Dots:** 5,000 randomly sampled co-registered terrain pixels across Gangotri Glacier.
* **Black Dashed Line:** The **1:1 Identity Line** ($y = x$). Represents perfect theoretical equivalence.
* **Coral Solid Line:** The **Ordinary Least Squares (OLS) Linear Fit** ($y = 1.0055x - 0.0072$).
* **Metrics Inset Box:**
  * Pearson Correlation: $r = \mathbf{0.9937}$ ($p < 10^{-100}$)
  * Coefficient of Determination: $R^2 = \mathbf{0.9875}$
  * Root Mean Squared Error: $\text{RMSE} = \mathbf{0.0410}$
  * Mean Absolute Error: $\text{MAE} = \mathbf{0.0322}$

### Scientific Interpretation:
1. **Slope of Unity ($m = 1.006 \approx 1.00$):** The regression line lies directly on top of the black dashed 1:1 line. There is virtually zero scaling distortion between the green and SWIR1 bands of both satellites.
2. **Zero Offset ($c = -0.007 \approx 0.00$):** No baseline radiometric drift exists between MSI and OLI.
3. **Bimodal Clustering:** Points cluster at the lower left ($\text{NDSI} \approx -0.1$ to $0.1$ for barren moraine rock) and upper right ($\text{NDSI} \approx 0.6$ to $0.9$ for clean snow/ice), confirming that the $\text{NDSI} \ge 0.40$ threshold cleanly separates terrain in both sensors.

### What to Say to Examiners:
> *"Here in Figure 2, we evaluate pixel-level radiometric fidelity using the Normalized Difference Snow Index. The coral OLS regression line has a slope of 1.0055 and an intercept of minus 0.007, virtually overlapping the theoretical 1:1 identity line. With an R² of 0.9875 and an RMSE of just 0.041, this validates that the atmospheric and BRDF corrections applied by NASA HLS achieve near-perfect cross-sensor calibration."*

---

## 3. Catchment Area Regression Scatter
**File:** `glacier_area_regression_scatter.png`  
**Location:** Slide 8 in PPTX | Figure 3 (Right) in PDF Report | "📏 Glacier Area" in Dashboard

![Catchment Area Regression Scatter](/Users/rameshwar/.gemini/antigravity/brain/208fa0aa-b181-481b-bac3-615121f02011/figures/glacier_area_regression_scatter.png)

### Anatomy of the Plot:
* **X-axis:** Sentinel-2 Mapped Glacier Area per Patch (in $\text{km}^2$).
* **Y-axis:** Landsat 8/9 Mapped Glacier Area per Patch (in $\text{km}^2$).
* **Green Scatter Points:** All 63 evaluated sub-basin tiles across the glacier catchment.
* **Black Dashed Line:** 1:1 Identity Reference ($y = x$).
* **Coral Solid Line:** OLS Linear Fit ($y = 0.9838x - 0.0130$).
* **Metrics Inset Box:**
  * Pearson Correlation: $r = \mathbf{0.9977}$ ($p = 5.37 \times 10^{-73}$)
  * Coefficient of Determination: $R^2 = \mathbf{0.9954}$
  * $\text{RMSE} = \mathbf{0.0401 \text{ km}^2}$ | $\text{MAE} = \mathbf{0.0254 \text{ km}^2}$

### Scientific Interpretation:
1. **Catchment-Scale Robustness:** An $R^2$ of **0.9954** means that 99.5% of the variance in Landsat's glacier area is explained by Sentinel-2.
2. **Low-Area vs. High-Area Sub-basins:** Notice points near $(0, 0)$ representing barren rock valley patches, and points near $1.0 - 2.5 \text{ km}^2$ representing the central accumulation zones. Both regimes adhere tightly to the 1:1 line.

### What to Say to Examiners:
> *"Figure 3 tests our segmentation framework at the regional catchment scale across 63 spatial tiles. The correlation between Sentinel-2 and Landsat area measurements is 0.9977 with an R² of 0.9954. The Mean Absolute Error is only 0.025 square kilometers per tile. This confirms that whether examining small tributary arms or the massive accumulation zone, both sensors track glacier extent consistently."*

---

## 4. Spatial Discrepancy & Agreement Map
**File:** `spatial_discrepancy_map.png`  
**Location:** Slide 3 in PPTX | Figure 1 in PDF Report | "📏 Glacier Area" in Dashboard

![Spatial Discrepancy Map](/Users/rameshwar/.gemini/antigravity/brain/208fa0aa-b181-481b-bac3-615121f02011/figures/spatial_discrepancy_map.png)

### Anatomy of the Colors:
* **Bright White:** **Concordant Glacier Detection** ($S2 \cap L8$) &mdash; Both Sentinel-2 and Landsat 8/9 agree on glacier ice. Forms the core glacier body.
* **Cyan (Light Blue):** **Unique to Sentinel-2** ($S2 \land \neg L8$) &mdash; Pixels detected as glacier only by Sentinel-2. Concentrated on steep lateral moraine boundaries and shaded margins.
* **Orange:** **Unique to Landsat 8/9** ($L8 \land \neg S2$) &mdash; Pixels detected as glacier only by Landsat.
* **Dark Charcoal / Black:** **Barren Terrain / Background** &mdash; Both sensors agree on rock, moraine, or valley floor.

### Scientific Interpretation:
1. **Terminus Snout Stability:** Look at the main curved trunk from southeast (Chaukhamba) to northwest (Gaumukh). The interior is completely solid white, showing **$98.61\%$ overall pixel concordance**.
2. **Where the 6.32% Discrepancy Occurs:** The cyan and orange pixels are **not** scattered randomly across the glacier; they form a thin 1-pixel fringe along the lateral moraines and shadowed valley cliffs.
3. **Glaciological Explanation:** Along moraines, partial volume mixing occurs: a 30 m pixel might contain 40% supraglacial rock debris, 30% ice, and 30% shadow. Sentinel-2's narrower NIR Band 8A has slightly higher sensitivity, causing it to cross the threshold along these boundary pixels.

### What to Say to Examiners:
> *"This is our spatial discrepancy map over the Gangotri basin. The white area represents concordant glacier ice where both satellites agree, achieving a 98.61% agreement rate and Cohen's Kappa of 0.8967. Crucially, the non-white pixels (cyan and orange) are strictly confined to a thin boundary fringe along the debris-covered lateral moraines. This visual evidence proves that the 1.1 km² difference between sensors is a mixed-pixel boundary effect, not an error in central glacier detection."*

---

## 5. Spectral Distributions (Split Violin Plots)
**File:** `spectral_distributions_violin.png`  
**Location:** Slide 7 in PPTX | Figure 4 in PDF Report | "📈 Spectral NDSI & NDVI" in Dashboard

![Spectral Distributions Violin](/Users/rameshwar/.gemini/antigravity/brain/208fa0aa-b181-481b-bac3-615121f02011/figures/spectral_distributions_violin.png)

### Anatomy of the Plot:
* **X-axis:** The four key remote-sensing channels: `NDSI`, `NDVI`, `GREEN`, `NIR`.
* **Y-axis:** Surface Reflectance and Index Values $[-1.0, 1.0]$.
* **Teal Half-Violin (Left):** Sentinel-2 (HLSS30).
* **Coral Half-Violin (Right):** Landsat 8/9 (HLSL30).
* **Horizontal Dashes inside Violins:** Quartiles (25th percentile, median, 75th percentile).

### Scientific Interpretation:
1. **NDSI Symmetry:** Notice the split violin for NDSI. The teal and coral halves match each other almost perfectly like a mirror. The bimodal shape captures the two distinct land types: barren rock (peak below 0.0) and clean ice/snow (peak above 0.70).
2. **NDVI Invariance:** Both sensors show NDVI centered near zero ($-0.05$ to $+0.10$), confirming the absence of dense vegetation in high-altitude alpine zones.
3. **NIR Reflectance:** NIR shows a long upper tail reaching $0.80 - 0.90$ for fresh accumulation snow at Chaukhamba peaks.

### What to Say to Examiners:
> *"Figure 5 compares the probability density distributions across four critical spectral channels using split violin plots—teal for Sentinel-2 and coral for Landsat. Notice the near-perfect bilateral symmetry in the NDSI column. Both sensors exhibit the exact same bimodal distribution, cleanly separating rock from snow/ice at the 0.40 mark. This demonstrates that sensor spectral response functions are well-aligned across the dynamic range."*
