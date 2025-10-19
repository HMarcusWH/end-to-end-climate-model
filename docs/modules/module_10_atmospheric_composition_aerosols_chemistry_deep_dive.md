# Module 10 — Atmospheric Composition & Aerosols/Chemistry Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Represent atmospheric composition (aerosols + reactive gases) and their **radiative forcing** via **aerosol–radiation interactions (ERFari)** and **aerosol–cloud interactions (ERFaci)**, plus chemically driven forcings (tropospheric/stratospheric O₃, stratospheric H₂O from CH₄). Deliver validated AOD/AAOD/SSA fields, Nd linkages, ozone fields, and a transparent ERF decomposition with uncertainty.

---

## Scope & Interfaces
- **Inputs**  Emissions of SO₂, NOₓ, NH₃, VOCs, BC/OC, dust/sea‑salt sources; well‑mixed GHGs (Module 1); meteorology from Atmosphere (Module 2); cloud microphysics hooks (Module 3); land/ocean precursors (Modules 5–6).
- **Outputs**  Aerosol mass/burden/optics (AOD, AAOD, SSA, Ångström exponent), cloud droplet number (Nd) tendencies/diagnostics, O₃/NO₂/SO₂/CO/HCHO fields, **ERFari**, **ERFaci**, and their sum; trend diagnostics and post‑2010 aerosol‑weakening indicators for Module 1.
- **Coupling**  
  - With **Module 2** radiation (optical properties, vertical profiles) and **Module 3** cloud microphysics (CCN–Nd activation curves).  
  - With **Module 9** (CH₄ lifetime via OH; N₂O/O₃ feedbacks).  
  - With **Module 12** (use ERF posteriors in energy‑balance calibration).

---

## Design goals
1) **ERF decomposition** that is traceable and reproducible (diagnostic double‑radiation calls or APRP backup).  
2) **Observation‑constrained optics** (AOD, AAOD, SSA) and trends; **regional skill** (e.g., Indo‑Pacific, NA/Europe, biomass‑burning belts).  
3) **Chemistry realism** for O₃/CH₄ lifetime and oxidants (OH/NOₓ/HO₂/RO₂) to ensure consistent forcing and budgets.

---

## Methods blueprint
1) **Aerosol module**  Species: sulfate, nitrate, ammonium, primary OC/BC, secondary organic aerosol (SOA), dust, sea salt. Hygroscopic growth, mixing‑state options (internal/externally mixed), Mie/lookup optical tables. Vertical profiles via transport + wet/dry deposition; microphysics for nucleation/coagulation/condensation (simplified if needed).
2) **Optics → radiation**  Compute layerwise extinction/scattering/absorption, SSA, asymmetry \(g\); pass to Module 2. **ERFari** via clean‑sky diagnostics; **ERFaci** via Nd/optical‑depth response (Twomey + adjustments in LWP/CF treated explicitly).
3) **ERF calculation**  Primary: double calls to radiation (aerosol‑present vs aerosol‑free) with clouds fixed and with aerosol removed from microphysics; secondary: **APRP** decomposition if double‑call not available.
4) **Chemistry**  Gas‑phase HOx–NOx–VOC–O₃ mechanism (reduced or CTM‑coupled). Compute CH₄ lifetime against OH; produce tropospheric O₃ fields and stratospheric H₂O from CH₄ oxidation (for Module 1 forcing split).  
5) **Assimilation/constraints (optional)**  AOD from MODIS MAIAC/MISR/VIIRS; AERONET direct AOD + inversions (SSA); CAMS analyses as an external check.
6) **Trend/attribution**  Quantify post‑2000 **aerosol ERF weakening** signals and regional drivers (SO₂ controls, ship‑fuel sulfur, clean‑air policies, wildfires).

---

## Sliders (parameters & assumptions)

### A) Aerosol emissions & sources
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Anthropogenic SO₂ scaling | % | 100 | 70–130; regional factors allowed |
| NH₃ scaling (nitrate sensitivity) | % | 100 | 70–150; controls nitrate burdens |
| BC/OC emission split | % | inventory | ±20%; region/sector specific |
| Ship SO₂ reduction onset | year | 2020 | 2018–2020; IMO sulfur cap impacts |
| Dust & sea‑salt source strength | – | scheme default | Wind‑/wave‑driven; ±50% for sensitivity |

### B) Optical properties & mixing state
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| BC absorption enhancement | – | 1.2 | 1.0–1.5; lensing/mixing‑state effect |
| Organic aerosol refractive index | – | 1.45+0.01i | Region/type dependent |
| Size distribution mode widths | – | scheme default | Affects Ångström exponent & SSA |
| Hygroscopic growth κ (sulfate/OC) | – | 0.6 / 0.1 | 0.4–0.8 / 0.0–0.2 |

### C) Cloud interaction (Nd & adjustments)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| CCN→Nd activation curve | – | log‑linear | Slope 0.2–0.5; regime‑dependent |
| Autoconversion (Nd sensitivity) | – | coupled to Module 3 | Controls Twomey vs LWP response |
| Precipitation susceptibility | – | 0.8 | 0.4–1.2; affects ERFaci magnitude |
| Overlap of aerosol–cloud fields | – | max‑random | Decorrelation length 1–3 km |

### D) ERF computation & uncertainty
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| ERF method | – | double‑call | Alt: APRP decomposition |
| ERFari/ERFaci split | % | diagnostic | Reported, not tuned |
| Post‑2010 aerosol weakening | % | 15 | 0–30; global indicator exported to Module 1 |
| ERF total (industrial era) QA | W m⁻² | −1.3 | Accept −2.0…−0.6 (module test) |

### E) Chemistry & oxidants
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Global mean OH | 10⁵ molecules cm⁻³ | 10.5 | 9–12; sets CH₄ τ |
| CH₄ lifetime against OH (τ_CH₄) | years | 9.5 | 8–12; emergent from mechanism |
| Ozone production efficiency | – | scheme default | Sensitive to NOₓ/VOC regime |
| Halogen chemistry switch | – | off | On reduces O₃/changes OH regionally |

---

## Data feeds (preferred)
- **Emissions**  CEDS (historical anthropogenic); ship sulfur policy markers; GFAS/FINN for fires; natural dust/sea‑salt parameterizations.  
- **Aerosol observations**  **AERONET** AOD/SSA/AAOD (V3 inversions); **MODIS MAIAC** AOD (V6.1) at 1 km; MISR/VIIRS as cross‑checks; CALIPSO extinction (optional).  
- **Composition reanalyses**  **CAMS** analyses/reanalyses for aerosols and reactive gases as external performance checks.  
- **Chemistry baselines**  SOCAT/GLODAP not required here; use GEOS‑Chem (or equivalent) mechanism references for OH/CH₄ lifetime and O₃ budgets.

---

## Diagnostics & validation
- **Optics**  Global/regional **AOD RMSE** vs AERONET; **SSA/AAOD** correlations where available; trend consistency (2000→present).  
- **ERF**  Industrial‑era total aerosol ERF within **−2.0…−0.6 W m⁻²**; report **ERFari** and **ERFaci** separately; provide 5–95% uncertainty via parametric ensemble.  
- **Chemistry**  CH₄ lifetime within 8–12 years; tropospheric O₃ burden within literature ranges; reasonable NO₂/SO₂ columns vs satellites (optional).  
- **Regional skill**  Biomass‑burning, dust, pollution hotspots; ship‑track signal change post‑2020 where detectable.  
- **Coupled checks**  Consistency with Module 3 CRE partition changes; Module 1 aerosol forcing time series.

**Initial acceptance thresholds**  
- AOD bias |≤| 0.05 (global mean) and RMSE competitive with CAMS in key regions; SSA/AAOD correlation > 0.6 at high‑AOD sites.  
- ERF total in assessed range; **post‑2010 weakening** detectable in sign.  
- CH₄ τ in 8–12 years with plausible OH fields; O₃ seasonal cycles captured in major basins.

---

## Implementation plan (repo wiring)
- `/chem/core/`  Gas‑aerosol mechanism; oxidants; deposition; microphysics.  
- `/chem/optics/`  Mie/lookup; mixing‑state options; hygroscopic growth; layer optics to radiation.  
- `/chem/erf/`  Double‑call + APRP fallback; ERFari/ERFaci/ALB partition; uncertainty samplers; trend analyzer.  
- `/chem/datafeeds/`  CEDS/GFAS/FINN; AERONET; MODIS MAIAC; CAMS.  
- `/diagnostics/chem_eval.ipynb`  AOD/SSA/AAOD skill; O₃/NO₂/SO₂ checks; ERF audits; post‑2010 weakening tracker.  
- `/tests/`  Unit tests for optics; regression tests for AOD skill metrics; ERF range assertions; CH₄ lifetime check.

---

## Pitfalls & guardrails
- Keep **ERFari vs ERFaci** definitions consistent across modules (don’t mix with instantaneous RF).  
- Avoid tuning optics to fit ERF; prioritize emissions/process fidelity, then document ERF outcome.  
- Be explicit about **mixing state** and **hygroscopicity** assumptions; they strongly affect SSA/AAOD.  
- Treat CAMS as an external benchmark, not truth; prioritize AERONET and vetted satellite products.  
- Track ship‑fuel sulfur step‑changes and regional policy impacts; document any “post‑2010 aerosol weakening” assumptions.

---

## QA checklist (quick)
- [ ] Global AOD bias and RMSE within targets; SSA/AAOD correlations robust at high‑AOD sites.  
- [ ] ERF total and split within assessed ranges, with uncertainty quantified.  
- [ ] CH₄ lifetime and O₃ burdens within literature; oxidant fields plausible.  
- [ ] Clear post‑2010 aerosol‑weakening diagnostics delivered.  
- [ ] Consistency with Modules 1–3, 9, 12 verified.

---

## Next actions
1) Wire CEDS emissions + MODIS MAIAC/AERONET feeds; stand up optics evaluation.  
2) Implement double‑call ERF and APRP fallback; generate industrial‑era ERF with uncertainty.  
3) Add chemistry mechanism check for OH/CH₄ τ and O₃ burdens; align with Module 9.  
4) Produce **post‑2000 ERF trend** analysis and a ship‑sulfur case study; export diagnostics to Module 1 and Module 12.

