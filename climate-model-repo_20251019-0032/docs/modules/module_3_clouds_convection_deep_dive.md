# Module 3 — Clouds & Convection Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Represent cloud–radiation effects and precipitation realism using credible parameterizations for **shallow/deep convection, boundary‑layer clouds, and microphysics**, and quantify **cloud feedbacks** that dominate ECS/TCR uncertainty.

---

## Scope & Interfaces
- **Inputs**  Atmospheric state and RT from Module 2; external forcings & composition from Module 1; aerosol/chemistry (Nd, AOD/SSA, ERFari/ERFaci hooks) from Module 10; surface fluxes from Module 5; ocean/sea‑ice lower boundary from Modules 6–7.
- **Outputs**  Cloud fraction/optical properties (by type/level), convective tendencies (heat/moisture/momentum), precipitation/evaporation, **cloud radiative effect (CRE)** SW/LW partition, diagnostics for feedback analysis.
- **Interfaces**  Cloud fields feed Module 2 radiation; rain/evaporation feed Module 4 hydrology; aerosol–cloud couplings coordinated with Module 10; feedback kernels shared with Module 12.

---

## Reference anchors (targets we must hit)
- **Global CRE**: SW ≈ −50 W m⁻², LW ≈ +30 W m⁻², NET ≈ −20 W m⁻² (cooling), with credible zonal/regime patterns.
- **Assessed net cloud feedback**: central ~+0.4 W m⁻² K⁻¹; likely positive, with very‑likely range extending slightly negative. Partition into low‑, mid‑, high‑cloud contributions.
- **Low‑cloud (subtropical marine) feedback**: dominant source of spread; link to lower‑tropospheric stability (EIS) and convective mixing strength.
- **Tropical deep convection**: realistic diurnal cycle over land, mesoscale organization/cold‑pool impacts on timing and intensity.

---

## Methods blueprint
1) **Convection**  Use a unified EDMF/mass‑flux framework with closures for shallow and deep modes; include entrainment/detrainment scalings, downdrafts, and cold‑pool triggering for organization. Provide CAPE‑based or moisture‑quasi‑equilibrium closures.
2) **Microphysics**  Start with a 1–2 moment warm‑rain scheme (autoconversion/accretion/evaporation), optional mixed‑phase/ice hooks. Make autoconversion threshold and Nd‑sensitivity explicit (couples to Module 10).
3) **Cloud fraction/overlap**  Diagnose stratiform cloud fraction from subgrid variance/critical RH; use maximum‑random overlap with a decorrelation length. Provide regime‑specific optical depth/altitude tendencies to partition CRE SW/LW.
4) **Feedback diagnostics**  Implement cloud radiative‑kernel method to decompose feedback into amount, altitude, and optical depth components; compute rapid adjustments vs slow feedbacks.
5) **Evaluation loop**  Column/SCM tests for marine stratocumulus/shallow Cu/deep tropical cases, then short coupled hindcasts to evaluate CRE, precip distributions, diurnal cycle, and regime transitions.

---

## Sliders (parameters & assumptions)

### A) Convection (mass‑flux/EDMF)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Entrainment rate (deep updrafts) | 10⁻³ m⁻¹ | 0.7 | 0.2–2.0; controls lower‑tropospheric drying and low‑cloud feedback linkage |
| Detrainment rate (deep) | 10⁻³ m⁻¹ | 1.0 | 0.3–3.0; affects anvil/top‑heavy heating and LW CRE |
| Entrainment (shallow) | 10⁻³ m⁻¹ | 2.0 | 0.5–5.0; sets shallow Cu tops, BL coupling |
| CAPE removal timescale (deep) | hours | 2 | 1–6; closure strength; shorter = stronger convective adjustment |
| Trigger CIN threshold | J kg⁻¹ | 25 | 0–75; higher suppresses spurious deep convection |
| Cloud‑base mass flux closure | – | moist static energy (MSE) | Alt: moisture convergence or CAPE‑based |
| Downdraft fraction @ base | % of updraft | 15 | 5–30; influences cold‑pool generation and RH profiles |
| Rain evaporation fraction | – | 0.6 | 0.3–0.9; sets cold‑pool strength & organization |
| Cold‑pool gust‑front lift | m s⁻¹ | 1.0 | 0.5–2.0; triggers new cells; adds convective memory |
| Minimum plume number (EDMF) | count | 3 | 1–5; controls subgrid variability representation |
| Convective momentum transport | scale | 1.0 | 0.5–2.0; adjusts jet/monsoon interactions |

### B) Microphysics (warm rain; mixed‑phase optional)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Autoconversion threshold \(q_c^*\) | g kg⁻¹ | 0.5 | 0.2–1.0; classic Kessler‑type threshold |
| Autoconversion rate coeff. | – | KK00 | Alt: Kessler/Sundqvist/Beheng; choose scheme & coefficients |
| Accretion efficiency | – | 1.0 | 0.7–1.5; removes cloud water via rain collection |
| Rain evaporation rate | s⁻¹ | 1e‑4 | 5e‑5–5e‑4; sets cold‑pool production & subcloud RH |
| Cloud droplet number \(N_d\) sensitivity | – | coupled to Module 10 | Strengthens/weakens warm‑rain formation (AIE linkage) |
| Ice fraction & fall speeds | – | scheme default | Hooks for mixed‑phase/ice; affects LW CRE & anvil residence |

### C) Stratiform cloud fraction & overlap
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Critical RH (mid/upper) | % | 80/70 | 70–90; controls thin cirrus and mid‑level cloud amount |
| Subgrid variance (BL) | – | prognostic | Scales marine Sc/LtCu coverage; tied to BL TKE |
| Overlap method | – | max‑random | With decorrelation length 1–3 km (tunable) |
| Anvil spreading rate | m s⁻¹ | 0.5 | 0.2–1.0; sets high‑cloud extent/altitude and LW CRE |

### D) Feedback/diagnostic settings
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Cloud kernel set | – | CMIP‑style | Amount/altitude/optical‑depth kernels; pick kernel vintage |
| Rapid adjustment partition | – | on | Separate adjustments (fast) vs slow feedback for clarity |
| Regime masks | – | EIS‑based | Stratocumulus, trade Cu, deep tropics, extratropics |

---

## Data (evaluation/constraints)
- **TOA/SFC fluxes & CRE**  CERES‑EBAF (global, zonal, regime composites).
- **Cloud amount/type/altitude**  ISCCP/HIRS; CloudSat/CALIPSO (GOCCP); MODIS optical depth & \(N_d\) proxies.
- **Precipitation**  GPCP, TRMM/GPM for intensity distributions & diurnal cycle.
- **Reanalysis**  ERA5 for EIS/LTS, humidity, jets; diagnostics for emergent‑constraint regressions.
- **Field campaigns (optional)**  ARM marine Sc, RICO (trade Cu), TWP/GoAmazon (deep convection) for case studies.

---

## Diagnostics & validation (with acceptance thresholds)
- **Global means**  CRE SW/LW/NET within canonical ranges; TOA flux closure inherited from Module 2.
- **Regime metrics**  Stratocumulus decks: correct shortwave reflection; trade‑cumuli fraction vs EIS; anvil altitude/extent distributions.
- **Precipitation**  Mean, variance, and **frequency–intensity** histograms near GPCP/TRMM; realistic **diurnal cycle** (afternoon land peak, nocturnal maritime MCSs).
- **Emergent‑constraint checks**  Positive link between lower‑tropospheric mixing/EIS changes and low‑cloud feedback; diagnose implied cloud‑feedback against assessed ranges.
- **Organization**  Cold‑pool parameterization improves timing and spatial clustering of deep convection; reduced premature morning convection over land.

**Initial acceptance**  
- Global NET CRE within −17 to −23 W m⁻²; SW CRE −45 to −55; LW CRE +25 to +35.  
- Tropics (20°S–20°N) precipitation diurnal amplitude/phase within observational spread; improvement over a no‑cold‑pool control.  
- Low‑cloud fraction/EIS slope consistent with satellite‑derived relationships.

---

## Implementation plan (repo wiring)
- `/clouds/convection/`  EDMF mass‑flux scheme with deep/shallow modes, downdrafts, cold‑pool trigger; CAPE/MSE closures.
- `/clouds/microphysics/`  Warm‑rain (KK00/Kessler/Beheng toggles); Nd coupling hooks; optional mixed‑phase.
- `/clouds/frac_overlap/`  Critical‑RH + subgrid variance; max‑random overlap with decorrelation length.
- `/diagnostics/cloud_kernels/`  Kernel code & notebooks to compute amount/altitude/optical‑depth feedbacks; rapid‑adjustment partitioning.
- `/cases/`  SCM/LES‑forced cases for marine Sc, trade Cu, tropical deep convection (including cold‑pool tests).
- `/tests/`  Unit tests for closures; regression tests on CRE partitions and precipitation statistics.

---

## Pitfalls & guardrails
- Avoid compensating errors: don’t tune microphysics to offset radiation or aerosol biases; coordinate with Modules 1, 2, 10.
- Ensure true clear‑sky sampling for CRE; document kernel vintage and assumptions.
- Keep organization physics (cold pools) modular so it can be disabled for attribution experiments.
- Track how entrainment/detrainment choices co‑vary with low‑cloud feedback to remain within assessed ranges.

---

## Next actions
1) Stand up EDMF with deep/shallow and cold‑pool triggers; run SCM cases.  
2) Select microphysics default (KK00) and expose autoconversion/evaporation sliders; wire Nd coupling to Module 10.  
3) Implement cloud kernels; compute baseline feedback partitions from 4×CO₂ and historical.
4) Validate CRE, precip distributions, diurnal cycle, and regime‑based metrics; iterate on entrainment/closure and cold‑pool parameters.

