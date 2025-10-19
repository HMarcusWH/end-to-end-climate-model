# Module 4 — Hydrological Cycle (P–E–R & Extremes) Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Close the **global water budget** (precipitation P, evapotranspiration/evaporation E, runoff R, terrestrial water storage ΔS) and capture the **intensification of extremes** with warming. Provide robust diagnostics and tunable analysis settings for means, variability, and tails, consistent with assessed thermodynamic/energetic constraints.

---

## Scope & Interfaces
- **Inputs**  From Modules 2–3 (atmospheric state, clouds/convection, precip), Module 5 (land ET/runoff), Module 6 (ocean surface fluxes), Module 1 (forcings). Optional observational products for assimilation/validation.
- **Outputs**  Global & regional P, E, P−E, R, ΔS diagnostics; closure metrics; extremes indices (Rx1day, Rx5day, R95p, CDD, etc.); scaling of means & extremes vs global warming; hydrological storyline summaries per region.

---

## Reference anchors (used for model evaluation)
- **Energetic constraint**  Global‑mean precipitation sensitivity ≈ **+1–3% per °C** warming (limited by radiative cooling/latent heating balance), while **water‑vapour capacity** scales ≈ **+7% per °C** (Clausius–Clapeyron). Extremes often scale near CC, with local short‑duration events sometimes **super‑CC (10–14% per °C)**.
- **Global budget**  Long‑term global P ≈ E; over **land:** P ≈ E + R + ΔS, **ocean:** E ≈ P + (R + runoff from land). Budgets must close within stated uncertainty.
- **Observed CRE/energy constraints** from Module 2 must be mutually consistent with P‑E changes.

---

## Methods blueprint
1) **Budget & closure**  Compute P, E, R, ΔS at global/land/ocean scales and major basins; check long‑term closure (|residual| thresholds) and interannual variability coherence (ENSO response).
2) **Means & variability**  Seasonal cycles; ENSO composites; moisture budget decomposition (thermodynamic vs dynamic vs residual) using q, ∇·(vq) diagnostics.
3) **Extremes**  Implement standardized indices (ETCCDI family): Rx1day, Rx5day, R95p/R99p, SDII, CDD/CWD, R10/R20, and peaks‑over‑threshold (POT) with GEV/GPD fits. Provide configurable windowing and thresholds.
4) **Scaling with warming**  Quantify d(precip mean)/dT and d(extremes)/dT by region and percentile; separate **thermodynamic scaling** from **dynamics** via circulation proxies; report CC‑like vs super‑CC behavior.
5) **Drought metrics**  Compute SPEI/PDSI variants with configurable PET method (Penman–Monteith, Priestley–Taylor, Thornthwaite); provide timescale tuning (1–24 months).
6) **Data assimilation (optional)**  Blend to observations (GPCP/GPCC for P, GLEAM/ERA5‑Land for E, GRACE‑FO for ΔS, GRDC for R) using simple bias‑correction or Kalman‑style nudging for diagnostics.

---

## Sliders (parameters & analysis settings)

### A) Global constraints & closure
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Global precip sensitivity dP/dT | % K⁻¹ | 2.0 | 1–3; energetic constraint on mean precipitation |
| Extremes sensitivity d(Rx1day)/dT | % K⁻¹ | 7.0 | 5–10; allow super‑CC up to ~14 for short‑duration/local POT |
| Closure tolerance (global/land/ocean) | mm yr⁻¹ | 15 | 5–30; max residual allowed for P−E−R−ΔS |
| Basin closure tolerance | mm yr⁻¹ | 25 | 10–50; relaxed at basin scale |
| ENSO coherence threshold | corr | 0.5 | 0.3–0.7; P anomalies vs Niño3.4 |

### B) Observational product weights (for validation/assimilation)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Precip product weight | % | GPCP 50 / GPCC 50 | Adjust vs IMERG/TRMM; ocean vs land weighting |
| Evap product weight | % | GLEAM 70 / ERA5‑Land 30 | Swap to MERRA‑2/FLUXCOM depending on region |
| Storage product weight | % | GRACE‑FO 100 | Optionally include land hydrology reanalysis |
| Runoff product weight | % | GRDC 100 | Basin‑wise station coverage dependent |

### C) Extremes detection & fitting
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Block maxima window | years | 1 | 1 (annual) or seasonal blocks |
| POT threshold quantile | q | 0.95 | 0.90–0.99; for GPD tail fits |
| Return periods | years | 10, 50 | Configurable set (e.g., 2, 5, 10, 50, 100) |
| Wet‑day cutoff | mm day⁻¹ | 1.0 | 0.1–1.0; affects SDII, R10/R20 |
| Consecutive dry‑day (CDD) threshold | mm day⁻¹ | 1.0 | 0.1–1.0; affects drought metrics |

### D) Drought/Aridity indices
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| PET method | – | Penman–Monteith | Alt: Priestley–Taylor, Thornthwaite |
| SPEI timescales | months | 1, 3, 6, 12 | 1–24; multi‑scale anomalies |
| PDSI algorithm | – | self‑calibrated (scPDSI) | Alt: classic PDSI |
| PET bias‑correction factor | – | 1.0 | 0.9–1.1; harmonize reanalysis vs station |

### E) Moisture budget decomposition
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Thermodynamic vs dynamic split method | – | q∇·v decomposition | Alt: moisture‑tracking/recycling |
| Moisture recycling method | – | Brubaker/Bosilovich | Alt: Lagrangian (FLEXPART‑style) |
| Recycling region mask | – | AR6 regions | User‑defined basins/regions |

---

## Data (authoritative feeds; choose per use‑case)
- **Precipitation (P)**  GPCP (monthly/daily); GPCC (gauge‑only land, monthly/daily); IMERG/GPM (3‑hourly to daily); TRMM (historical tropics).
- **Evapotranspiration (E)**  GLEAM (daily); ERA5‑Land/MERRA‑2 (reanalysis); FLUXCOM (machine‑learning ET from flux towers).
- **Runoff/Discharge (R)**  GRDC (daily/monthly discharge by station/basin).
- **Terrestrial Water Storage (ΔS)**  GRACE/GRACE‑FO (monthly), ESA CCI soil moisture (surface), ancillary snow/ice where needed.

---

## Diagnostics & validation (targets/tests)
- **Budget closure**  Global residual |P−E−R−ΔS| below tolerance; land/ocean partitions reasonable; basin closures within set thresholds with GRDC coverage caveats.
- **Scaling**  Mean P sensitivity near 1–3% K⁻¹; Rx1day/Rx5day scaling near ~7% K⁻¹ over many regions, with documented super‑CC pockets in convective regimes.
- **Extremes**  Return‑period intensities/ frequencies (10‑yr, 50‑yr) within observational spread; CDD/CWD, R95p/R99p, SDII consistent with products.
- **Variability**  ENSO teleconnections in P−E and ΔS; phase and amplitude close to observed composites.

**Initial acceptance**  
- Global closure residual ≤ 15 mm yr⁻¹; land closure ≤ 25 mm yr⁻¹.  
- Rx1day 10‑yr and 50‑yr event intensity changes align in sign and magnitude with assessed ranges for given warming levels.  
- Drought metrics (SPEI/PDSI) reproduce major observed events (2002–03, 2010, 2015–16, 2020–22).

---

## Implementation plan (repo wiring)
- `/hydro/budget.py`  budget/closure for P, E, R, ΔS at global/land/ocean/basin scales; ENSO composites; uncertainty.
- `/hydro/extremes.py`  ETCCDI indices; POT/GEV fitting; return‑level maps; scaling vs ΔT.
- `/hydro/drought.py`  SPEI/PDSI calculators with PET choices; timescale controls; drought atlas outputs.
- `/hydro/datafeeds.py`  loaders for GPCP/GPCC/IMERG, GLEAM/ERA5‑Land, GRDC, GRACE‑FO, ESA CCI SM; harmonization & bias‑correction.
- `/diagnostics/hydro_eval.ipynb`  closure plots, scaling regressions, extremes verification, event case studies.
- `/tests/`  unit tests for closures and indices; regression tests on Rx1day trends and basin closures.

---

## Pitfalls & guardrails
- Don’t force closure by arbitrary residual sinks; diagnose causes (P‑biases over ocean, ET bias over arid lands, GRACE leakage) and document adjustments.
- Keep extremes methods transparent: declare thresholds, wet‑day cutoffs, and fitting method; verify sample size sufficiency.
- Align hydrology diagnostics with Modules 2–3 physics (e.g., low‑cloud regimes affect SWCRE and hence precipitation) and with Module 5 land ET/runoff parameterizations.
- Document regional data quality; station density (GPCC/GRDC) varies by region.

---

## QA checklist (quick)
- [ ] Global/land/ocean P‑E‑R‑ΔS closure within tolerances.  
- [ ] Mean and extreme precipitation scaling vs warming within assessed ranges.  
- [ ] ENSO composites show expected wet/dry dipoles (e.g., Pacific, SA, Australia).  
- [ ] Drought metrics reproduce major events and trends.  

---

## Next actions
1) Wire data loaders (GPCP, GPCC, IMERG, GLEAM, GRACE‑FO, GRDC, ESA CCI SM).  
2) Run historical closure and scaling diagnostics (1901→present where available; 1979→present for satellites).  
3) Stand up extremes indices/POT fitting and validate against observational products.  
4) Produce region‑by‑region hydrological storylines and integrate with the dashboard.