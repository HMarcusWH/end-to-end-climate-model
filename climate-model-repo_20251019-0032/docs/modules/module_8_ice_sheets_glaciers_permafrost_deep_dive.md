# Module 8 — Ice Sheets, Glaciers & Permafrost Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Quantify cryosphere contributions to **sea level** (ice sheets + glaciers) and **carbon–climate feedbacks** (permafrost), consistent with assessed observations and model protocols. Provide calibrated emulators/couplings for scenarios.

---

## Scope & Interfaces
- **Inputs**  Atmospheric/oceanic forcings (Modules 1–3,10), ocean mixed layer & circulation (Module 6), sea‑ice state (Module 7), regionalization (Module 14).
- **Outputs**  AIS/GrIS mass balance and component fluxes (SMB, discharge, basal melt), glacier mass change, permafrost metrics (active layer depth, thaw area) and **carbon fluxes (CO₂/CH₄)**; sea‑level components to Module 11; carbon‑cycle hooks to Module 9.
- **Coupling**  SMB downscaling from reanalyses/RCMs; sub‑ice‑shelf melt from ocean thermal forcing; carbon fluxes to Module 9; freshwater to Module 6.

---

## Methods blueprint

### A) Ice sheets (AIS & GrIS)
1) **Geometry & physics**  Hybrid SIA/SSA or higher‑order stress balance; Glen–Nye rheology (n≈3) with Arrhenius temperature dependence; basal sliding law (plastic/Coulomb or Weertman‑type); thermomechanical coupling.
2) **Mass budget**  Surface Mass Balance (SMB) from downscaled RCMs (e.g., RACMO/MAR) or emulator; dynamic discharge via stress balance; ice‑shelf buttressing (stress‑coupled); grounding‑line migration with subgrid interpolation; sub‑shelf melt via **thermal forcing** parameterization; calving law (e.g., eigencalving/fracture‑threshold); optional hydrofracture & mélange buttressing factors.
3) **Forcing protocols**  Follow **ISMIP6** methods for ocean thermal forcing anomalies and basal melt calculation; use multi‑GCM ensembles for spread. 
4) **Data assimilation (optional)**  Inversion for basal friction; weak constraint assimilation of altimetry/velocity for reanalysis‑quality hindcasts.

### B) Global glaciers (outside ice sheets)
1) **Inventory & hypsometry**  Use **RGI v7.0** outlines + hypsometry; region masks = 19 RGI regions.
2) **Mass‑balance model**  Degree‑day or energy‑balance emulator constrained by observations; precipitation–temperature scaling with lapse‑rate correction; debris‑cover modifier optional.
3) **Calibration**  Fit to WGMS mass‑balance series and geodetic changes; infer regional sensitivities to climate.

### C) Permafrost (carbon feedback)
1) **Ground thermal model**  1‑D heat diffusion with phase change (snow, soil moisture, conductivity); simulate **active layer thickness (ALT)** and permafrost extent.
2) **Carbon pools & fluxes**  Multi‑pool soil carbon with temperature‑moisture dependent decomposition (Q₁₀/Arrhenius); partition to **CO₂ vs CH₄** via wetland fraction, water table, and oxidation; include **abrupt thaw/thermokarst** pathway fraction and fire disturbance.
3) **Coupling**  Emit fluxes to Module 9 carbon budget; feedback to Module 1 (small ERF via CH₄/O₃ handled in Module 10/1) if desired.

---

## Sliders (parameters & assumptions)

### A1) Ice rheology & sliding (AIS/GrIS)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Glen exponent (n) | – | 3.0 | 2.5–4.0; rheology sensitivity tests |
| Rate factor Arrhenius pre‑exp. (A₀) | Pa⁻ⁿ s⁻¹ | model‑specific | Calibrate to temp field; anisotropy option |
| Basal sliding law | – | Coulomb‑plastic | Alt: Weertman; effective pressure‑dependent |
| Till yield stress (τ_c) | kPa | 50 | 20–150; inversions provide spatial maps |
| Enhancement factor (E) | – | 1.0 | 0.5–3.0; fabric/damage proxy |

### A2) Shelves, calving & grounding lines
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Sub‑shelf melt sensitivity (γ_T) | m yr⁻¹ K⁻¹ | 20 | 5–50; **ISMIP6 thermal forcing** based |
| Lateral melt/recirculation factor | – | 1.0 | 0.5–2.0; plume/2‑D effects proxy |
| Calving law | – | eigencalving | Alt: von Mises/fracture/strain‑rate |
| Hydrofracture threshold (pond depth) | m | 1.0 | 0.5–2.0; if enabled |
| Mélange buttressing factor | – | 0.5 | 0–1; seasonal |
| Grounding‑line subgrid interp. | – | on | SISL/flux‑limiting to reduce bias |

### B) SMB & downscaling
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Lapse rate (dT/dz) | K km⁻¹ | 6.5 | 5–7; regional |
| Precip scaling per K | % K⁻¹ | 7 | 2–10; Clausius–Clapeyron proxy |
| Degree‑day factors (snow/ice) | mm w.e. d⁻¹ K⁻¹ | 3/7 | debris/impurity modifiers optional |
| Drift & refreezing fraction | – | 0.4 | 0.2–0.6; affects runoff & SMB |

### C) Glaciers (RGI regions)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Mass‑balance sensitivity dM/dT | m w.e. yr⁻¹ K⁻¹ | region‑fit | Fit per RGI region to WGMS/remote sensing |
| Precip. elasticity dM/dP | – | region‑fit | |
| Debris‑cover effect | – | 1.0 | 0.8–1.2; slows ablation |

### D) Permafrost carbon
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Soil carbon stock (0–3 m / deep) | Pg C | dataset | From inventories; uncertainty ensemble |
| Q₁₀ (heterotrophic) | – | 2.0 | 1.5–2.7; pool‑specific allowed |
| Moisture scalar (f_wet) | – | 1.0 | 0.6–1.4; modifies CH₄ share |
| CH₄ oxidation fraction | – | 0.6 | 0.4–0.9; reduces net CH₄ |
| Abrupt thaw fraction by 2100 | % of region | 3 | 0–10; thermokarst corridor |
| Fire disturbance return time | years | 80 | 30–150; boosts emissions, reduces SOC |

---

## Data feeds (preferred)
**Ice sheets**  
- **Mass balance**  IMBIE reconciled AIS/GrIS mass change (1992→present); **GRACE/GRACE‑FO** basin time series.  
- **Altimetry & thickness**  ICESat/ICESat‑2, CryoSat‑2; BedMachine (GrIS) & BedMachine/BedMachine‑Antarctica equivalents when available.  
- **Velocity**  MEaSUREs/ITS_LIVE annual velocity maps (AIS/GrIS).  
- **Forcing**  ISMIP6 ocean thermal forcing fields; RACMO/MAR SMB climatologies for evaluation.

**Glaciers**  
- **Inventory**  **RGI v7.0** outlines & hypsometry.  
- **Observations**  WGMS FoG mass‑balance & geodetic change; Copernicus/WMO region indicators.

**Permafrost**  
- **Stocks**  Circumpolar soil‑carbon inventories with uncertainty (surface/deep/yedoma).  
- **Thermal state**  GTN‑P borehole temperatures; NOAA Arctic Report Card; ALT maps (where available).  
- **Flux context**  Regional CH₄/CO₂ budgets; wildfire emissions.

---

## Diagnostics & validation
**Ice sheets**  
- Compare AIS/GrIS mass change to **IMBIE** reconciled series (basin & total).  
- Check altimetry‑derived trends (freeboard/thickness) and grounding‑line migration vs remote sensing.  
- Partition mass budget: SMB vs discharge vs basal melt; shelf buttressing indices; AMOC‑linked Antarctic sensitivity via Module 6.

**Glaciers**  
- Reproduce regional mass‑balance trends and 2000→present loss within latest intercomparison uncertainty; validate hypsometry‑resolved responses.

**Permafrost**  
- ALT & permafrost extent trends vs GTN‑P; borehole temperature bias < ~0.5 °C regionally.  
- Carbon fluxes: sign and magnitude consistent with Arctic Report Card synthesis; CH₄ source persistence; fire‑year excursions.

**Initial acceptance thresholds**  
- 1992→present AIS+GrIS mass‑change RMSE within IMBIE uncertainty; 
- Glacier global loss rate consistent with 2000→2023 assessments; 
- ALT trend sign correct across sub‑regions; permafrost net carbon balance within assessed envelopes (including fire effects) over 21st‑century scenarios.

---

## Implementation plan (repo wiring)
- `/cryosphere/ice_sheets/`  Core solver (ISSM/PISM/CISM backend or emulated), calving & sub‑shelf melt, grounding‑line numerics, inversion tools.  
- `/cryosphere/glaciers/`  RGI ingest, region masks, mass‑balance emulator, calibration to WGMS/geodetic.  
- `/cryosphere/permafrost/`  1‑D ground thermal (ALT) + multi‑pool carbon module with CH₄ pathway; abrupt‑thaw and fire disturbance switches.  
- `/cryosphere/datafeeds/`  IMBIE, GRACE‑FO, ICESat‑2/CryoSat‑2, BedMachine, MEaSUREs/ITS_LIVE, RGI, WGMS, GTN‑P, ARC datasets.  
- `/cryosphere/diagnostics/`  Sea‑level components, basin scorecards, flux partitioning, permafrost carbon dashboards.  
- `/tests/`  Regression tests: AIS/GrIS trends vs IMBIE; glacier regional loss; ALT bias; carbon flux sanity.

---

## Pitfalls & guardrails
- Avoid compensating errors: do not tune calving/melt to hide SMB biases.  
- Use **ISMIP6** ocean‑melt protocols or documented alternatives; track uncertainty from sub‑shelf melt parameterization.  
- Quantify sensitivity to rheology (n, E) and sliding (τ_c); document inversions.  
- For permafrost, include **abrupt thaw** and **fire** processes; excluding them biases low.  
- Keep glacier mass‑balance constrained by both glaciological and geodetic data; respect debris‑cover and hypsometry effects.

---

## QA checklist (quick)
- [ ] AIS/GrIS mass‑change series match IMBIE within uncertainty; component fluxes partitioned plausibly.  
- [ ] Glacier regional trends consistent with RGI/WGMS and intercomparison ranges.  
- [ ] ALT & borehole temperatures within target errors; permafrost carbon flux sign/magnitude consistent with synthesis.  
- [ ] Sea‑level component hand‑off to Module 11 closes with steric + mass components.

---

## Next actions
1) Wire IMBIE, GRACE‑FO, BedMachine, MEaSUREs/ITS_LIVE, RGI v7, and WGMS feeders; build dashboards.  
2) Implement ISMIP6 basal‑melt emulator (γ_T, thermal forcing) and calibrate against observed shelf thinning.  
3) Calibrate glacier mass‑balance emulator per RGI region; validate against WGMS/geodetic.  
4) Stand up permafrost ALT + carbon module with abrupt thaw and fire; benchmark to Arctic Report Card & synthesis papers.  
5) Export sea‑level and carbon‑flux components to Modules 11 and 9, respectively.