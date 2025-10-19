# Module 6 — Ocean Circulation & Heat Uptake Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Simulate and/or emulate the ocean’s uptake, storage, and redistribution of heat (and carbon) in a way that closes the **Earth Energy Imbalance (EEI)** and matches observed **ocean heat content (OHC)** trends, **mixed‑layer depth (MLD)**, overturning variability (e.g., **AMOC**), and **thermosteric sea‑level** contributions.

---

## Scope & Interfaces
- **Inputs**  External forcings (Module 1), atmospheric fluxes & state (Module 2), sea‑ice coupling (Module 7), land freshwater inputs (Modules 4–5), reanalysis/observations for evaluation.
- **Outputs**  3‑D ocean temperature/salinity, surface fluxes, **OHC** (layered & basin‑wise), **MLD** climatology/variability, ocean heat uptake (OHU), meridional heat transport, **thermosteric sea‑level (SSL)**, AMOC index/streamfunction diagnostics.
- **Coupling**  Atmos–ocean exchange via coupler (Module 15); optional carbon uptake hooks to Module 9.

---

## Design goals
1) **Energy closure**  Reproduce observed EEI via OHU/OHC growth, keeping TOA fluxes (Module 2) consistent.  
2) **Vertical structure**  Realistic partition of heat between upper‑ocean (0–700/0–2000 m) and deep ocean.  
3) **Regional realism**  Basin‑wise heat uptake (Atlantic, Pacific, Indian, Southern) and Southern Ocean dominance; credible AMOC variability.  
4) **Sea‑level link**  Convert simulated temperature/salinity fields into **thermosteric** and **halosteric** sea‑level for Module 11.

---

## Methods blueprint
**Path A — Full OGCM (preferred when feasible)**  
- Eddy‑permitting or parameterized ocean GCM with K‑profile vertical mixing, isopycnal/slopes diffusion + Gent–McWilliams (GM) eddy parameterization, bulk formula surface fluxes from Module 2, and data assimilation for reanalyses (optional).

**Path B — Calibrated emulator (for scenarios & ensembles)**  
- Two‑layer or multi‑box ocean heat uptake model calibrated to observed OHC, with explicit **upper‑layer heat capacity (C₁)**, **deep‑layer heat capacity (C₂)**, and **exchange/uptake coefficient (γ)**. Pattern scaling hooks for regionalization.

**Diagnostics implemented in both paths**  
- OHC time series (global, 0–700/0–2000 m and full depth); OHU; meridional heat transport; MLD climatologies; AMOC indices; SSL from TEOS‑10 equation of state.

---

## Sliders (parameters & assumptions)

### A) Vertical & lateral mixing
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Interior diapycnal diffusivity (κ) | m² s⁻¹ | 1.0e‑5 | 3e‑6…3e‑5; latitude/stratification‑dependent maps allowed |
| Isopycnal diffusivity (K_iso) | m² s⁻¹ | 1000 | 500–2500; sets lateral mixing along density surfaces |
| GM eddy thickness diffusivity (K_GM) | m² s⁻¹ | 800 | 400–2000; eddy heat transport proxy |
| Surface mixed‑layer entrainment coeff. | – | 0.7 | 0.4–1.2; interacts with MLD seasonal cycle |

### B) Heat‑uptake & capacity (emulator path)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Upper‑layer heat capacity C₁ | W·yr m⁻² K⁻¹ | 70 | 50–100; ties to mean MLD (~50–100 m) |
| Deep‑layer heat capacity C₂ | W·yr m⁻² K⁻¹ | 900 | 500–1500; integrates abyssal storage |
| Exchange/uptake coefficient γ | W m⁻² K⁻¹ | 1.0 | 0.6–1.6; controls TCR/ECS partition |
| Upwelling/ventilation factor | – | 1.0 | 0.5–1.5; mimics Southern Ocean ventilation efficacy |

### C) Boundary & numerical controls
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Bulk formula set | – | COARE‑like | Sensible/latent fluxes; consistency with Module 2 |
| Freshwater flux scaling | % | 100 | 80–120; runoff/precip adjustments (closure tests) |
| Time step (ocean) | min | 60 | 20–180; stability/accuracy balance |
| Lateral viscosity | m² s⁻¹ | 1000 | 200–3000; sets numerical damping |

### D) Overturning & regions
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| AMOC sensitivity factor | – | 1.0 | 0.7–1.3; scales overturning strength/variability |
| Southern Ocean uptake efficacy | – | 1.0 | 0.7–1.5; partitions basin heat uptake |
| Basin masks & weights | – | AR6 | Alt: user‑defined basins for diagnostics |

### E) Sea‑level conversion
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| EOS for steric calc. | – | TEOS‑10 | Computes SSL from T/S; avoids fixed coefficients |
| Halosteric inclusion | – | on | Compute and report SSL & halosteric separately |
| Reference depth for SSL | m | full depth | Alt: 0–2000 m steric for comparison |

---

## Data feeds (preferred)
- **OHC / EEI**  NOAA/NCEI 0–700/0–2000 m & full‑depth OHC; annual updates; Indicators of Global Climate Change links.  
- **Profiles/MLD**  **Argo** profiles (temperature/salinity) for OHC and **Holte–Talley** MLD climatologies; optional ship/ice supplements at high latitudes.  
- **Reanalyses**  **ORAS5** (ECMWF OCEAN5) and related ocean reanalyses for cross‑checks.  
- **Sea level**  Steric SSL from simulated T/S; compare to altimetry + GRACE mass for closure (Module 11).

---

## Diagnostics & validation
- **OHC trends**  Match observed global OHC growth (0–700/0–2000 m and full depth); basin partitions reasonable.  
- **EEI closure**  OHU consistent with CERES‑derived EEI when coupled (Module 2); no spurious long‑term drift.  
- **MLD**  Seasonal cycle & regional patterns consistent with Holte–Talley and de Boyer Montégut climatologies.  
- **Overturning**  AMOC index variability (subpolar/subtropical) within observational ranges (OSNAP/EOF‑based proxies).  
- **SSL**  Thermosteric sea level from T/S reproduces observed steric contribution; land‑ice mass + halosteric added in Module 11 for total GMSL closure.

**Initial acceptance thresholds**  
- Simulated OHC trend within observational uncertainty over 1993→present; layer partition (0–700 vs 700–2000 m) within assessed ranges.  
- Global OHU within ±0.2 W m⁻² of EEI over the satellite era mean.  
- MLD RMSE vs climatologies comparable to modern OGCMs; credible subtropical & subpolar contrasts.

---

## Implementation plan (repo wiring)
- `/ocean/ogcm/`  OGCM configuration (mixing/GM parameters, bulk fluxes, runoff coupling); optional data‑assimilation hooks.  
- `/ocean/emulator/`  Two‑layer (C₁/C₂/γ) and multi‑box models with calibration utilities to OHC/EEI; regional scaling options.  
- `/ocean/diagnostics/`  OHC/OHU calculators, MLD climatology (Holte–Talley & density criteria), meridional heat transport, AMOC index, TEOS‑10 steric sea‑level.  
- `/ocean/datafeeds/`  NCEI OHC loaders, Argo profile handlers, ORAS5 reanalysis reader.  
- `/tests/`  Regression tests on OHC and SSL; conservation & drift checks.

---

## Pitfalls & guardrails
- Avoid compensating flux adjustments to hide mixing or circulation biases; tune physics first.  
- Use **TEOS‑10** for steric sea‑level; avoid fixed thermal‑expansion coefficients.  
- Track numerical mixing (viscosity/diffusivity) to prevent over‑damped currents and blurred MLD.  
- Ensure freshwater budget closure (precip/evap/runoff) to avoid artificial halosteric trends.  
- Document calibration priors for C₁/C₂/γ and retain physical interpretability.

---

## QA checklist (quick)
- [ ] OHC trends (0–700/0–2000 m, full depth) within observed uncertainty; reasonable basin partition.  
- [ ] Global OHU consistent with EEI; no long‑term drift.  
- [ ] MLD climatology within accepted RMSE vs Holte–Talley / de Boyer Montégut.  
- [ ] SSL reproduces observed steric contribution; Module 11 closes total GMSL with mass components.

---

## Next actions
1) Stand up NCEI OHC and Argo loaders; compute historical OHC/MLD diagnostics.  
2) Calibrate emulator (C₁/C₂/γ) to OHC + EEI; produce posterior ranges.  
3) Choose OGCM parameter set (κ, K_iso, K_GM) and validate against OHC/MLD/AMOC targets.  
4) Implement TEOS‑10 SSL calculator and compare steric contribution to altimetry‑based GMSL decomposition (with Module 11).