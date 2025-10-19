# Module 7 — Sea Ice Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Simulate sea‑ice **thermodynamics, dynamics, and radiative properties** to reproduce historical trends and variability in **extent, area, thickness, drift, and seasonality**, and to project future evolution consistent with the coupled ocean–atmosphere state.

---

## Scope & Interfaces
- **Inputs**  Surface fluxes & winds (Module 2), ocean state & mixed‑layer properties (Module 6), aerosols/BC‑on‑snow radiative perturbations (Module 1/10), land freshwater (river discharge; Modules 4–5).
- **Outputs**  Sea‑ice concentration/area/extent, thickness & thickness distribution (ITD), drift & deformation fields, **albedo & surface radiative fluxes**, melt‑pond diagnostics, lead fraction, snow depth, and bulk momentum/heat/salt fluxes to ocean/atmosphere.
- **Coupling**  Fluxes exchanged via the coupler (Module 15); steric/halosteric sea‑level and freshwater closure feed Module 11.

---

## Design goals
1) **Realistic climatology & trends** of Arctic/Antarctic extent, area, thickness, and seasonal cycle.
2) **Credible mechanics** (rheology & ridging) and **surface optics** (albedo/melt ponds/snow) to capture feedbacks.
3) **Energy/water/salt closure** with ocean and atmosphere; conservative numerics; reproducible tuning knobs.

---

## Methods blueprint
1) **Thermodynamics**  Multi‑layer conductive growth/melt with snow cover; brine rejection/salt exchange; lateral melt at floe edges; shortwave penetration in ponded/dry states.
2) **Dynamics**  Elastic–viscous–plastic (EVP) rheology; momentum balance with air/ocean drag; ridging/rafting redistribution in an **ice thickness distribution (ITD)** framework; incremental remapping advection.
3) **Surface optics & ponds**  Spectral albedo parameterization with melt‑pond effects (pond fraction, depth, and optical properties); snow grain‑size/aging and impurity (BC) modifiers.
4) **Data assimilation (optional)**  Concentration/drift nudging for reanalysis‑grade hindcasts; no assimilation for free‑running projections.
5) **Diagnostics**  Extent/area, thickness climatologies, drift/deformation, lead fraction, pond fraction proxies, radiation budgets; per‑basin scores.

---

## Sliders (parameters & assumptions)

### A) Thermodynamics & snow
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Sea‑ice thermal conductivity | W m⁻¹ K⁻¹ | 2.03 | 1.8–2.4; salinity/temp dependent |
| Snow thermal conductivity | W m⁻¹ K⁻¹ | 0.31 | 0.2–0.4; grain‑size/ρsnow dependent |
| Albedo (cold/dry ice) VIS/NIR | – | 0.72/0.55 | 0.6–0.8 / 0.45–0.65 |
| Albedo (warm/ponded) VIS/NIR | – | 0.45/0.35 | 0.35–0.55 / 0.25–0.45 |
| Snow albedo (fresh/aged) | – | 0.85/0.65 | Grain‑size & impurity dependent |
| Shortwave extinction depth in ice | m | 0.8 | 0.5–1.5; ponded ice shallower |
| Ocean‑ice turbulent heat flux coeff. | W m⁻² K⁻¹ | 10 | 5–30; couples to ML temp/shear |
| Lateral melt coefficient | m s⁻¹ (W m⁻²)⁻¹ | 1e‑7 | 0.5–2e‑7; controls floe‑edge melt |

### B) Melt ponds & surface state
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Melt‑pond fraction (diagnostic max) | – | 0.25 | 0.1–0.4; regime dependent |
| Pond depth (effective) | cm | 10 | 5–20; affects albedo & SW penetration |
| Pond drainage threshold | cm | 5 | 2–10; controls pond persistence |

### C) Dynamics, rheology & redistribution
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Air–ice drag coeff. (Cd_ai) | – | 1.5e‑3 | 1.0–2.0e‑3; wind stress sensitivity |
| Ice–ocean drag coeff. (Cd_io) | – | 5.5e‑3 | 3–8e‑3; shear‑dependent option |
| EVP elastic time step factor | – | 0.6 | 0.3–0.8; numerical stability/realism |
| Plastic yield curve eccentricity (e) | – | 2.0 | 1.5–2.5; shape of failure envelope |
| Compressive strength (P*) | N m⁻² | 27,500 | 15–40 kPa; scales ridging resistance |
| Ridging redistribution rate | – | 1.0 | 0.5–2.0; ITD category transfer |
| ITD categories (N) | count | 5 | 5–7; resolution of thickness spectrum |

### D) Floe, leads & radiation coupling
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Lead fraction minimum | – | 0.02 | 0–0.05; sets winter LW flux to atmosphere |
| Floe size distribution parameter | – | 2.5 | 2–3; affects lateral melt & waves |
| BC‑on‑snow albedo reduction | – | coupled | From Module 1; regional scaling allowed |

### E) Numerics & coupling
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Ice time step | minutes | 30 | 15–60; ties to EVP stability |
| Remapping scheme | – | incremental | Conservative, low‑diffusion advection |
| Coupling frequency (A‑I‑O) | hours | 3 | 1–6; exchange of stress/fluxes |

---

## Data feeds (preferred)
- **Concentration & extent/area**  Passive‑microwave climate records (NOAA/NSIDC CDR; OSI‑SAF interim CDR).  
- **Motion/drift**  Polar Pathfinder ice motion vectors (daily/weekly/monthly).  
- **Thickness**  ICESat‑2 freeboard (ATL07/ATL10) → thickness; CryoSat‑2 thickness (AWI); combined **CryoSat‑2 + SMOS** winter product.  
- **Modeled thickness baseline**  PIOMAS reanalysis for spatial/seasonal patterns (context only).  
- **Ancillary**  Reanalysis winds/fluxes (ERA5) for diagnostics; snow products where available.

---

## Diagnostics & validation
- **Extent/area**  Seasonal cycle amplitude/phase and trends (Arctic & Antarctic); area vs extent consistency.  
- **Thickness**  Spatial patterns & distributions vs ICESat‑2/CryoSat‑2; winter growth rates; multi‑year vs first‑year fractions.  
- **Drift/deformation**  Vector RMSE & deformation stats vs Pathfinder; export through Fram Strait.  
- **Surface radiation**  Regional/seasonal albedo; pond onset timing; SW absorption partitioning.  
- **Coupled impacts**  Mixed‑layer heat content and feedbacks (Module 6) and TOA/SFC flux impacts (Module 2).

**Initial acceptance thresholds**  
- Extent/area seasonal cycle errors within observational spread; linear trend signs and magnitudes in the Arctic captured (recognizing Antarctic variability).  
- Winter thickness and distribution within satellite product uncertainty envelopes; reasonable basin contrasts.  
- Drift RMSE comparable to modern CICE configurations; Fram export within literature ranges.

---

## Implementation plan (repo wiring)
- `/sea_ice/core/`  EVP rheology, ITD redistribution, thermodynamics, melt‑pond optics, incremental remapping.  
- `/sea_ice/params/`  Albedo tables (state‑dependent), drag coefficients, EVP/e/P* settings, pond parameters.  
- `/sea_ice/datafeeds/`  NSIDC/NOAA CDR & OSI‑SAF concentration, NSIDC Pathfinder motion, ICESat‑2 (ATL07/ATL10), CryoSat‑2 & CS2‑SMOS thickness, PIOMAS baseline.  
- `/sea_ice/diagnostics/`  Extent/area/thickness/drift metrics, pond timing, radiation budgets, Fram export; per‑basin scorecards.  
- `/tests/`  Regression tests for extent/area climatology & trends; thickness distribution checks; drift RMSE thresholds.

---

## Pitfalls & guardrails
- Keep **area vs extent** definitions consistent with observational products (grid‑cell thresholding matters).  
- Avoid over‑tuning albedo/ponds to fix thickness biases—check ocean mixed‑layer heat and snow properties first.  
- Document EVP/e/P* settings; rheology can mask numerical artifacts if over‑damped.  
- Treat PIOMAS as context, not ground truth; prioritize satellite thickness where available.

---

## QA checklist (quick)
- [ ] Extent/area seasonal cycle & trends match observed envelopes (Arctic/Antarctic).  
- [ ] Thickness patterns & distributions consistent with ICESat‑2/CryoSat‑2/CS2‑SMOS uncertainty.  
- [ ] Drift/deformation metrics within target RMSE; Fram export reasonable.  
- [ ] Sea‑ice optics produce credible regional albedo/pond seasonality and coupled feedbacks.

---

## Next actions
1) Wire concentration/drift thickness datafeeds and compute a historical metrics dashboard.  
2) Stand up default CICE‑style configuration (EVP, ITD=5, ponds on) and run hindcasts for 1993→present.  
3) Calibrate albedo/ponds and drag/rheology parameters to reduce mean/state biases without harming drift/thickness realism.  
4) Deliver per‑basin skill scorecards and couple diagnostics to Modules 2, 6, and 11.

