# Module 2 — Atmosphere (Dynamics & Radiation) Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Deliver a physically credible **atmospheric circulation + radiative transfer** core that closes the global energy and water budgets, provides TOA/SFC fluxes consistent with observations, and supplies winds/temperature/humidity/precip fields to other modules. (Cloud microphysics & convection parameter choices are treated in Module 3, but their radiative impacts are diagnosed here through CRE.)

---

## Scope & Interfaces
- **Inputs**  composition fields (well‑mixed GHGs, ozone, aerosols from Modules 1 & 10), solar & volcanic (Module 1), land surface states/fluxes (Module 5), sea‑ice/ocean surface (Modules 6–7).
- **Outputs**  3‑D atmospheric state (winds, T, q), surface fluxes (LH/SH, net SW/LW), **TOA SW/LW/NET**, cloud radiative effects (CRE), meridional heat transport, circulation diagnostics (Hadley cell/jet metrics).
- **Time step & coupling**  radiation sub‑stepping permitted; dynamics time step set by numerics (Module 15).

---

## Reference anchors (global energy budget & CRE)
- Planetary albedo ~0.29; absorbed shortwave ~240 W m⁻²; emitted longwave ~239 W m⁻²; net TOA **≈ +EEI** (small positive).  
- **Cloud Radiative Effect (CRE)**: typical global means **SW ≈ −50 W m⁻²**, **LW ≈ +30 W m⁻²**, **NET ≈ −20 W m⁻²** (cooling).  
- **EEI (recent decades)** small positive; must be consistent with Module 12 targets when forced by Module 1.

---

## Data feeds (authoritative)
- **Radiation/energy budget validation**  CERES‑EBAF (TOA & SFC fluxes, all‑/clear‑sky, CRE).  
- **Atmospheric state & circulation metrics**  ERA5 reanalysis (winds, T, q, MSLP, u/v at jet levels).  
- **Radiation codes & spectroscopy**  RRTMG / RTE+RRTMGP documentation; HITRAN/MT_CKD references (embedded in code docs).  

---

## Methods blueprint
1) **Radiation**  Implement a modern two‑stream band model (RRTMG or RTE+RRTMGP) with up‑to‑date spectroscopic coefficients; enable clear‑/all‑sky flux calculation to diagnose **CRE**; include cloud‑overlap method (maximum‑random) from Module 3.  
2) **Dynamics**  Hydrostatic primitive‑equation core (spectral or finite‑volume) with conservative transport; or leverage an existing dynamical core from a tested GCM.  
3) **Boundary layer & surface exchange**  MO similarity + turbulent diffusion; interacts with land/ocean modules for LH/SH and surface stress.  
4) **Diagnostics**  TOA/SFC flux closure; meridional energy transport from CERES‑EBAF; zonal wind/jet diagnostics; Hadley cell streamfunction; lapse‑rate & humidity structure; radiative kernels (optional) for feedback analysis.  
5) **Spin‑up**  Short (multi‑decade) hindcast with historical forcings to tune small biases before coupling tightly to Modules 3, 6, 5.

---

## Sliders (exposed parameters & assumptions)

### A) Radiation & optics
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Radiation code | – | RRTMG | Alt: RTE+RRTMGP (faster/more modular) |
| Spectral bands (SW/LW) | count | 14/16 (RRTMG) | Tunable (RRTMGP configurable); more bands → accuracy vs cost |
| Spectroscopic dataset | – | model default | HITRAN/MT_CKD version used by code build |
| Clear‑/all‑sky CRE calc | – | On | Needed for CRE and feedback diagnostics |
| Cloud overlap method | – | Max‑random | Controls vertical overlap for radiation (links to Module 3) |
| Gas optics subset | – | CO₂, H₂O, O₃, CH₄, N₂O (+ minor) | Keep consistent with Module 1 coefficients |
| Surface emissivity/BRDF | – | Presets by surface type | Land/ocean/ice spectral emissivity & albedo maps |
| Shortwave aerosol optics in RT | – | From Module 10 | Single‑scattering albedo, asymmetry, AOD (read‑only here) |

### B) Dynamics & numerics
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Dynamical core | – | Finite‑volume | Alt: spectral/SE; must conserve mass/energy |
| Time step (atm) | minutes | 30 | 10–60; stability vs cost |
| Radiation call frequency | hours | 3 | 1–6; sub‑stepping allowed |
| Horizontal resolution | km | 100 | 25–200; affects jets/storm tracks |
| Vertical levels / top | levels / hPa | 72 / 0.1 | ≥ 60 levels; resolve UTLS & stratosphere |
| Orographic gravity‑wave drag | scale | 1.0 | 0.5–2.0; tunes jets/stratospheric winds |
| Non‑orographic GWD | scale | 1.0 | 0.5–2.0; tropical momentum budget |
| Diffusion/hyperviscosity | scale | 1.0 | Controls small‑scale damping |

### C) PBL & surface exchange
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| PBL scheme | – | Eddy‑diffusion mass‑flux | Alt: TKE‑based; affects diurnal cycle & low clouds |
| Surface roughness (land/sea/ice) | m | model defaults | Calibrate vs reanalyses; wind‑stress and fluxes |
| Stability functions (MO) | – | Standard | Variants affect LH/SH partitioning |

---

## Diagnostics & validation (targets/tests)
- **Energy closure (global)**  Mean TOA Net within ±0.2 W m⁻² of CERES‑EBAF over overlapping periods; zonal‑mean SW/LW patterns without large biases; CRE SW≈−50, LW≈+30, Net≈−20 W m⁻².  
- **Circulation**  Jet core latitude/speed by basin; Hadley cell width & strength; trade‑wind biases; MSLP patterns; QBO/stratospheric winds if resolved.  
- **Thermodynamics**  Temperature & humidity vertical structure vs ERA5; lapse‑rate in tropics; lower‑tropospheric stability over marine stratocumulus regions.  
- **Transport**  Implied meridional heat transport from TOA/SFC fluxes close to CERES‑derived estimates.  

**Acceptance thresholds (initial)**  
- TOA net bias |≤| 0.2 W m⁻²; zonal‑mean RMSD of SW/LW < model‑class medians; jet latitude bias < ~2–3°; Hadley width drift < ~2° vs ERA5 climatology. (Tighten after first tuning.)

---

## Implementation plan (repo wiring)
- `/atmos/radiation/`  RRTMG or RTE+RRTMGP build + config; gas optics tables; CRE diagnostics.  
- `/atmos/dynamics/`  chosen core configs; GWD settings; diffusion controls.  
- `/diagnostics/ceres_era5_eval.py`  pulls CERES‑EBAF/ERA5 and computes flux errors, CRE, jets, Hadley metrics, meridional heat transport.  
- `/tests/test_energy_closure.py`  asserts TOA net and CRE ranges; `/tests/test_circulation_metrics.py` jet latitude/speed, Hadley width.  

---

## Pitfalls & guardrails
- Don’t tune radiation to compensate aerosol or cloud microphysics biases (keep Modules 1 & 3 consistent).  
- Ensure clear‑sky diagnostics are true clears (avoid sampling artifacts) when computing CRE.  
- Keep spectroscopic datasets and gas sets synchronized with Module 1 forcing assumptions.  
- Avoid numerical diffusion that erodes jets/storm tracks; document any damping applied.

---

## QA checklist (quick)
- [ ] Global TOA net within ±0.2 W m⁻² of CERES‑EBAF over evaluation period.  
- [ ] CRE (SW, LW, NET) within canonical ranges; regional CRE patterns reasonable.  
- [ ] Jet cores and Hadley metrics within observational spread; no spurious trends.  
- [ ] Meridional heat transport consistent with CERES‑derived estimates.  

---

## Next actions
1) Stand up radiation code (RRTMG or RTE+RRTMGP) with CRE diagnostics; verify offline columns.  
2) Run a 10–20 yr historical hindcast; compute energy closure vs CERES‑EBAF and circulation metrics vs ERA5.  
3) Tune GWD, diffusion, PBL to reduce jet and flux biases without masking cloud/aerosol issues.  
4) Hand off radiative diagnostics (CRE kernels) to Module 3 for cloud/convection tuning.

