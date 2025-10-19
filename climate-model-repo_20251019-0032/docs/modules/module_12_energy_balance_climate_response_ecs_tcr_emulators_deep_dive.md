# Module 12 — Energy Balance & Climate Response (ECS/TCR, Emulators) Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Calibrate a transparent **energy‑balance core** that turns ERF (Module 1) into **global‑mean surface temperature** (GMST), **Earth Energy Imbalance** (EEI), and **ocean heat uptake** (OHU/OHC, Module 6), yielding defensible posteriors for **ECS** and **TCR** and a fast emulator for scenarios.

---

## Scope & Interfaces
- **Inputs**  ERF by agent (Module 1); GMST observations (HadCRUT5/Berkeley/ERA5); OHC & steric SLR (Module 6/11); EEI from CERES (Module 2).  
- **Outputs**  Calibrated parameters (\(\lambda,\kappa, C_u, C_d, \gamma, \epsilon\)); posterior ECS/TCR; partition of warming (forced vs internal); hindcast/forecast GMST & EEI; skill metrics.

---

## Methods blueprint
1) **Two‑layer Energy Balance Model (EBM)**  Linear global energy budget with **upper‑mixed layer** and **deep ocean** temperatures (\(T_u, T_d\)):
\[ C_u \, \dot T_u = F(t) - \lambda \, T_u - \kappa (T_u - T_d) \]
\[ C_d \, \dot T_d = \kappa (T_u - T_d) \]
Add optional **efficacy** \(\epsilon\) on deep‑ocean uptake and a **time‑varying feedback** \(\lambda(t)\) to reflect pattern effects. Calibrate to GMST+OHC using MLE or Bayesian MCMC.  
2) **FaIR‑equivalence**  Provide a mapping between the EBM and the FaIR thermal impulse‑response to ensure drop‑in compatibility for scenarios.  
3) **Internal variability**  Treat as AR(1)/seasonal red noise on GMST residuals; optionally regress out ENSO/PDO indices for sensitivity.  
4) **Cross‑checks**  Close EEI with CERES and OHC; verify transient metrics (TCR) using the 1% yr⁻¹ CO₂ definition.

---

## Sliders (parameters & priors)

### A) Core thermal parameters
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Feedback parameter **\(\lambda\)** | W m⁻² K⁻¹ | −1.0 | −0.6…−1.8; maps to ECS via \(ECS = F_{2x}/|\lambda|\) |
| Ocean heat‑uptake **\(\kappa\)** | W m⁻² K⁻¹ | 0.8 | 0.4–1.5; controls TCR and EEI |
| Mixed‑layer heat capacity **\(C_u\)** | W yr m⁻² K⁻¹ | 8 | 5–12; \(~50–80\) m MLD equivalent |
| Deep‑ocean heat capacity **\(C_d\)** | W yr m⁻² K⁻¹ | 100 | 50–200; abyssal reservoir |
| Deep‑uptake efficacy **\(\epsilon\)** | – | 1.0 | 0.8–1.3; modifies effective feedback in transient |
| Pattern‑effect \(\lambda(t)\) | – | off | Optional linear or kernel‑based evolution |

### B) Derived climate metrics & priors
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| **ECS prior (AR6)** | °C | 3.0 | Likely 2.5–4.0; very likely 2.0–5.0 |
| **TCR prior (AR6)** | °C | 1.8 | Likely 1.4–2.2 |
| \(F_{2x}\) (CO₂ doubling ERF) | W m⁻² | 3.93 | FaIR/Etminan‑consistent |

### C) Observation/model links
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| GMST dataset | – | HadCRUT5 | Alt: Berkeley, ERA5 (with cautions) |
| OHC layers used | m | 0–700 & 0–2000 | Optional full‑depth constraints |
| EEI constraint weight | – | medium | Low/med/high; balances CERES vs OHC |

### D) Forcing/response options
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Volcanic efficacy | – | 1.0 | 0.8–1.2; transient response tuning |
| Aerosol ERF prior width | – | AR6 | Narrow/wide to test ECS–ERF degeneracy |
| Variability model | – | AR(1) | Alt: ARMA/ENSO‑regressed |

---

## Data feeds (authoritative)
- **GMST**  HadCRUT5 (global), Berkeley Earth, ERA5 (air‑temp‑based).  
- **OHC & steric**  NOAA/NCEI 0–700/0–2000 m time series; basin partitions.  
- **EEI**  CERES‑EBAF (TOA/SFC fluxes) and joint satellite–in situ EEI assessments.  
- **Forcing**  Module 1 ERF by agent; \(F_{2x}\) aligned with Etminan/FaIR.

---

## Diagnostics & validation (targets/tests)
- **Posterior ranges**  **ECS likely 2.5–4.0 °C**, **TCR likely 1.4–2.2 °C**.  
- **EEI closure**  2005→present mean EEI consistent with CERES/Argo (~O(0.5–1.0) W m⁻²); positive imbalance persists.  
- **OHC fit**  0–700 and 0–2000 m trends within NOAA/NCEI uncertainty; meridional partitions plausible.  
- **Hindcast skill**  Out‑of‑sample (e.g., 1880–1930 train, 1931–2024 test) GMST skill; volcanic responses realistic.  
- **Consistency**  Derived OHU = EEI − dH/dt consistent with observed OHC tendency.

**Initial acceptance thresholds**  
- Posterior medians within AR6 likely ranges for ECS & TCR.  
- Decadal‑mean EEI within published uncertainty envelopes; sign correctly positive.  
- OHC RMSE competitive with CMIP‑informed EBMs; no long‑term drift.

---

## Implementation plan (repo wiring)
- `/ebm/core.py`  Two‑layer EBM (\(C_u, C_d, \lambda, \kappa, \epsilon\), optional \(\lambda(t)\)); adjoint/gradients for fast calibration.  
- `/ebm/fair_bridge.py`  Thermal IRF mapping to FaIR parameters for scenario use.  
- `/ebm/calib.py`  Bayesian/MLE calibration to GMST+OHC+EEI; AR(1)/ENSO options; priors from AR6.  
- `/diagnostics/ebm_eval.ipynb`  Posterior plots, ECS/TCR histograms, EEI/OHC closure, hindcast skill.  
- `/tests/`  Unit tests (analytic solution checks) + regression tests for EEI/OHC/GMST fits.

---

## Pitfalls & guardrails
- **ECS–aerosol degeneracy**  Explore with prior width sliders; report sensitivity.  
- **Pattern effect**  Time‑varying \(\lambda\) can bias ECS if ignored; expose switch and document impact.  
- **Dataset blend**  GMST datasets differ (coverage, SST vs air); test robustness across choices.  
- **Double counting**  Align \(F_{2x}\) and ERF with Module 1; don’t mix RF and ERF.  
- **EEI constraints**  Reconcile CERES EEI with OHC tendency (Argo); investigate discrepancies, not tune them away.

---

## QA checklist (quick)
- [ ] Posterior ECS/TCR in AR6 likely ranges.  
- [ ] EEI matches CERES/Argo envelopes; positive in recent decades.  
- [ ] OHC trend/variability captured for 0–700/0–2000 m.  
- [ ] Hindcast skill verified; volcanic responses credible.  
- [ ] FaIR mapping validated; scenario emulator passes sanity checks.

---

## Next actions
1) Pull latest HadCRUT5/Berkeley/ERA5, NCEI OHC, and CERES‑EBAF.  
2) Calibrate EBM with and without \(\lambda(t)\); compare ECS/TCR posteriors and EEI fits.  
3) Validate OHU/OHC closure and decadal EEI; generate posterior priors for Module 16 scenarios.  
4) Package emulator (FaIR‑compatible) with parameter posteriors and uncertainty sampling.

