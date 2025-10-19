# Module 5 — Land Surface, Vegetation & Albedo (LULCC) Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Represent land–atmosphere exchange of **energy, water, and momentum**, and quantify the **radiative and non‑radiative effects of land‑use/land‑cover change (LULCC)**. Provide tunable parameters and diagnostics for **surface albedo**, **evapotranspiration (ET)**, **soil moisture & runoff**, and **biogeophysical feedbacks** that affect climate and extremes.

---

## Scope & Interfaces
- **Inputs**  Forcings/composition (Module 1: GHGs/aerosols; Module 10: aerosol–cloud microphysics hooks), meteorology from Atmosphere (Module 2), cloud/convection tendencies (Module 3), ocean/ice lower‑boundary conditions (Modules 6–7), and scenarios (Module 16, via LUH2 land‑use transitions).
- **Outputs**  Surface radiative properties (shortwave/longwave albedo & emissivity), surface fluxes (LH/SH, net radiation), soil moisture/temperature, runoff & baseflow, canopy properties (LAI, roughness, \(N_d\) proxies), and **ERF(LULCC)** for coupling to Module 1.

---

## Design goals
1) **Physically consistent energy–water closure** over land at grid scale and aggregated regional scales.  
2) **Bidirectional LULCC impacts**: capture both **radiative (albedo)** and **non‑radiative** (ET, roughness, boundary‑layer) effects.  
3) **Scenario‑aware**: ingest LUH2‑style transitions (crop/forest/pasture/urban; wood harvest, shifting cultivation) for historical and SSP futures.  
4) **Evaluation‑ready**: native diagnostics against flux towers, satellite albedo products, and reanalysis.

---

## Methods blueprint
1) **Land surface core**  Multi‑tile canopy/soil/snow with canopy radiative transfer; prognostic soil moisture/temperature, snowpack, and canopy water.  
2) **Albedo**  Spectral (VIS/NIR) white‑sky/black‑sky albedo, BRDF‑aware; biome‑specific base values and dynamic adjustments for snow cover, soil moisture, and leaf phenology.  
3) **ET partitioning**  Penman–Monteith canopy transpiration + soil evaporation + interception evaporation; stomatal conductance linked to VPD, CO₂, soil moisture; optional plant hydraulics switch.  
4) **Runoff & baseflow**  Infiltration‑excess and saturation‑excess schemes; TOPMODEL or CLM‑style subsurface drainage with tunable hydraulic parameters; river routing hook.  
5) **LULCC implementation**  Annual area‑fraction changes per tile (crop/forest/pasture/urban) with wood‑harvest bookkeeping; compute **Δalbedo** and **Δfluxes**; provide a consistent **ERF(LULCC)** time series to Module 1.  
6) **Urban tile (optional)**  Prescribed albedo/emissivity and anthropogenic heat release; roughness/impervious runoff parameters.

---

## Sliders (parameters & assumptions)

### A) Surface radiative properties
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Forest shortwave albedo (VIS/NIR) | – | 0.12/0.18 | Biome‑specific; snow & SZA modifiers |
| Grass/cropland albedo (VIS/NIR) | – | 0.18/0.23 | Seasonally variable with LAI/soil moisture |
| Bare soil albedo | – | 0.25 | Texture/soil‑color dependent; moisture modifier |
| Snow albedo (fresh/aged) | – | 0.85/0.60 | Grain‑size and impurity (BC‑on‑snow) modifiers |
| Urban albedo | – | 0.12 | High‑albedo scenario variant |
| Albedo BRDF kernel | – | Ross–Li | Alt: isotropic; zenith‑angle sensitivity control |

### B) Canopy & stomata
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Maximum stomatal conductance | mol m⁻² s⁻¹ | 0.3 | 0.1–0.6; species/biome dependent |
| VPD sensitivity (Medlyn/Ball–Berry slope) | – | 9 | 5–12; alters transpiration response |
| CO₂ effect on stomata | – | enabled | Reduces \(g_s\) with rising CO₂; affects ET and WUE |
| Plant hydraulics switch | – | off | On enables xylem limitation & drought response |
| LAI phenology method | – | prognostic | Alt: prescribed climatology; ties to surface albedo |

### C) Soil hydrology & runoff
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Saturated hydraulic conductivity \(K_{sat}\) | mm day⁻¹ | map‑based | ± order‑of‑magnitude; sensitivity on runoff |
| Soil porosity | – | map‑based | Texture‑dependent; affects soil water holding |
| Soil matric potential (sat) | kPa | −10 | −2…−20; retention curve parameter |
| Brooks–Corey/van Genuchten shape | – | map‑based | Controls soil water retention curve |
| Infiltration partition method | – | Green–Ampt | Alt: Horton; runoff sensitivity |
| Baseflow parameter | – | 0.01 | 0.001–0.05; sets drainage timescale |

### D) Snow & cold‑region processes
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Snow metamorphism rate | day⁻¹ | 0.02 | 0.01–0.05; drives albedo aging |
| Snow compaction | – | standard | Density & thermal effects |
| BC‑on‑snow albedo reduction | – | coupled | From Module 1; regional scaling allowed |

### E) LULCC mechanics & ERF
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| LUH2 scenario set | – | SSPx‑y | Historical + SSPs; transitions, harvest |
| Albedo Δ per land‑cover change | – | biome‑table | Data‑driven Δ between tiles |
| Irrigation albedo/flux effect | – | enabled | Adds small negative ERF + ET changes |
| ERF(LULCC) calibrator | W m⁻² | −0.20 | Accept −0.30…−0.10 at 2019 (QA target) |

### F) Urban & roughness (optional)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Anthropogenic heat flux | W m⁻² | 10 | 0–50; urban heat island experiments |
| Roughness length (urban/crop/forest) | m | 0.5/0.1/1.5 | Aerodynamic controls on fluxes |

---

## Data feeds (preferred)
- **Land‑use transitions**  LUH2 (historical + SSP); wood harvest and shifting cultivation included.  
- **Albedo**  MODIS BRDF/albedo (MCD43, daily 16‑day window, 500 m) for validation & bias calibration.  
- **Flux validation**  FLUXNET2015 & tailored tower syntheses (latent/sensible heat, radiation, CO₂ fluxes).  
- **Ancillary**  Soil texture/depth maps; land cover climatologies (ESA CCI/CGLS); snow products for cold‑region albedo checks.

---

## Diagnostics & validation
- **Energy balance**  Net radiation, LH/SH partitioning vs towers; Bowen ratio distributions per biome.  
- **Albedo**  Seasonal cycle and mean biases vs MODIS BRDF products by biome/latitude; snow‑albedo evolution metrics.  
- **Hydrology**  Soil moisture seasonal cycle; runoff/ET partition; river‑basin water balance sanity checks.  
- **LULCC ERF**  Time‑series reproduces assessed industrial‑era **ERF(LULCC) ≈ −0.20 W m⁻²** (with irrigation), within likely range; trend continuity across historical→SSP.

**Initial acceptance**  
- Global albedo bias < ±0.02 absolute by biome bands.  
- Tower‑site median LH/SH biases within ±15 W m⁻²; ET seasonal phase captured.  
- ERF(LULCC 1750→2019) within −0.30…−0.10 W m⁻² and consistent with Module 1 budget.

---

## Implementation plan (repo wiring)
- `/land/core/`  land surface model (tiles, canopy RT, soil/snow/ET).  
- `/land/lulcc/`  LUH2 ingestion; tile‑fraction updates; Δalbedo/Δflux calculators; ERF(LULCC) exporter.  
- `/land/params/`  biome albedo tables; soil hydraulic parameters; stomatal/phenology configs.  
- `/diagnostics/land_eval.py`  tower‑site evaluation; MODIS albedo comparison; basin water balance; ERF(LULCC) checks.  
- `/tests/`  unit tests for energy/water closure; regression tests vs MODIS albedo and ERF target.

---

## Pitfalls & guardrails
- Avoid compensating errors: don’t tune albedo to hide ET/runoff biases or vice‑versa.  
- Keep **radiative** (albedo) and **non‑radiative** (ET/roughness) LULCC effects explicit; report both.  
- Ensure historical→SSP **LUH2 continuity** (no jumps at 2015/2020); document versioning.  
- Propagate uncertainty from canopy optics, snow impurities, and soil hydraulics into ERF(LULCC) ranges.

---

## QA checklist (quick)
- [ ] Global/biome albedo within tolerance vs MODIS BRDF.  
- [ ] Energy balance and ET partition realistic vs FLUXNET towers.  
- [ ] LULCC ERF 1750→2019 within assessed likely range and consistent with Module 1 totals.  
- [ ] LUH2 transitions correctly applied across historical and chosen SSP.

---

## Next actions
1) Wire LUH2 ingestion and tile update logic; generate historical Δalbedo maps and ERF(LULCC) series.  
2) Calibrate biome albedo/phenology against MODIS; verify snow‑albedo seasonality in cold regions.  
3) Evaluate ET/LH/SH against FLUXNET2015/ONEFlux and targeted tower syntheses; adjust stomatal/VPD controls.  
4) Produce land‑sector diagnostics pack (albedo, ET, runoff, soil moisture) and couple ERF(LULCC) to Module 1.

