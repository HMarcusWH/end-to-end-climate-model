# Module 9 — Carbon Cycle (Land & Ocean) + Other Biogeochem Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Close the **modern carbon budget** and provide calibrated emulators of **land and ocean CO₂ sinks** (plus CH₄ and N₂O budgets for completeness) suitable for scenarios. Ensure consistency with observed atmospheric growth rates, **Global Carbon Budget (GCB)** assessments, and ocean/land constraints. Expose parameters that map cleanly to IPCC AR6 concepts (e.g., **TCRE**, **β** fertilization, **γ** climate–carbon feedback).

---

## Scope & Interfaces
- **Inputs**  ERF & composition (Module 1), atmospheric state & fluxes (Module 2), clouds & hydrology (Modules 3–4), land LULCC & albedo (Module 5), ocean state (Module 6), cryosphere fluxes (permafrost CH₄/CO₂ from Module 8), scenarios (Module 16).
- **Outputs**  Annual **atmospheric growth rate** (G_ATM), **land sink** S_LAND, **ocean sink** S_OCEAN, **airborne fraction** AF, **residual budget**; ocean **pCO₂**, **DIC/TA** changes and **pH**; land carbon stocks/fluxes (NEE, GPP, fire), wetland CH₄ and N₂O budgets; calibrated parameter posteriors for scenario runs.

---

## Design goals
1) **Budget closure**  EFOS + ELUC − (S_OCEAN + S_LAND) − G_ATM ≈ 0 within assessed residuals.
2) **Interannual variability**  Capture ENSO‑linked variability (land sink swings, ocean outgassing) and decadal trends in sinks.
3) **Scenario fidelity**  Match AR6‑consistent **TCRE** and reproduce historical pCO₂, ocean pH decline, and sink partitioning.

---

## Methods blueprint
### A) Core CO₂ cycle (reduced‑complexity, AR6‑consistent)
- **Impulse response (IRF) carbon box** with 3–4 timescales for atmospheric CO₂ decay/uptake; parameters temperature‑ and concentration‑dependent (FaIR‑style).  
- **Land sink S_LAND** = **β_CO₂** × f(N, P, water) − **γ_T** × ΔT + disturbance terms (fire, LUC legacy). β captures CO₂ fertilization; γ is climate–carbon feedback (warming‑induced respiration, drought/heat).  
- **Ocean sink S_OCEAN** via air–sea gas exchange (piston velocity k, Schmidt number), solubility (ΔT), and **buffer (Revelle) factor** from carbonate chemistry; optional biological pump efficiency & remineralization lengthscale for sensitivity.  
- **Consistency link**  Calibrate to **GCB** time series (EFOS, ELUC, S_LAND, S_OCEAN, G_ATM) with priors from AR6.

### B) Ocean carbonate system (diagnostic)
- Compute seawater **CO₂ system** (DIC, TA → pCO₂, pH, Ω_arag) for each basin using TEOS‑10 + CO2SYS routines; benchmark against **SOCAT‑constrained pCO₂** and **GLODAP** interior carbon trends.

### C) Land biogeochemistry (diagnostic)
- Track **GPP, NPP, heterotrophic respiration**, soil/biomass pools (multi‑pool turnover) and **fire** emissions; nitrogen constraint scalar for β; drought/heat stress via VPD/soil moisture from Modules 2, 5.

### D) Methane & nitrous oxide (other biogeochem)
- **CH₄**  Emissions from wetlands (temperature/wetness response), agriculture/waste, fossil; **OH‑controlled lifetime** (and OH feedback) set by Module 10 chemistry; partition to atmospheric growth & sinks (soil, tropospheric OH).  
- **N₂O**  Soil/agricultural + industry emissions; stratospheric loss lifetime; small climate sensitivity.  
- Provide consistent annual budgets and growth rates aligned with WMO/GCP assessments; feed radiative forcing to Module 1.

---

## Sliders (parameters & priors)

### A) Carbon cycle core
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| **TCRE** (informative prior) | °C / 1000 GtCO₂ | 0.45 | 0.27–0.63 (AR6 likely range) |
| IRF time constants (τ₁…τ₄) | years | 4/36/390/∞ | FaIR‑style; calibrated |
| IRF partition coefficients (a₁…a₄) | – | 0.22/0.28/0.24/0.26 | Sum=1; calibrated |
| Land CO₂ fertilization **β_CO₂** | % ΔNPP / 100 ppm | 10 | 5–20; down‑weighted by N/P limits |
| Climate–carbon feedback **γ_T** | PgC yr⁻¹ K⁻¹ | 40 | 20–80; positive reduces sink |
| Disturbance/fires sensitivity | % per K | 5 | 0–10; interacts with drought |
| Ocean gas‑exchange **k** (10 m s⁻¹) | cm h⁻¹ | 15 | 10–25; wind‑speed scaling |
| Revelle buffer factor **β_buf** | – | 10 | 8–14; basin/temperature dependent |
| Export rain ratio (CaCO₃:POC) | – | 0.07 | 0.04–0.12; affects alkalinity & pCO₂ |
| Remineralization length scale | m | 1000 | 600–1400; biological pump sensitivity |

### B) Methane (CH₄)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Wetland T‑sensitivity | % K⁻¹ | 7 | 3–12; super‑CC local scaling possible |
| Wetland wetness sensitivity | % per +100 mm | 4 | 1–8; hydrology link |
| Anthropogenic CH₄ emissions | Tg yr⁻¹ | GCB series | Scenario‑driven |
| **CH₄ lifetime τ** | years | 9.1 | 8–12; OH‑controlled (Module 10) |
| Soil sink fraction | % | 5 | 3–7 |

### C) Nitrous oxide (N₂O)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Agricultural N₂O emissions | TgN yr⁻¹ | inventory | Scenario‑driven |
| **N₂O lifetime** | years | 116 | 110–125; stratospheric loss |
| Climate sensitivity | % K⁻¹ | 1 | 0–3 |

### D) Constraints & diagnostics
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Airborne fraction **AF** target | – | 0.44 | 0.36–0.50; multi‑decadal mean |
| Budget residual tolerance | GtCO₂ yr⁻¹ | 0.3 | 0–0.6; diagnostic, not tuned |
| ENSO coherence (land sink) | corr | 0.6 | 0.4–0.8; vs Niño 3.4 |

---

## Data feeds (authoritative)
- **Global Carbon Budget (annual)**  EFOS, ELUC, S_LAND, S_OCEAN, G_ATM, AF, with 2024/2025 updates.  
- **WMO GHG Bulletin**  Annual growth rates and records for CO₂, CH₄, N₂O.  
- **SOCAT (surface ocean pCO₂)**  Basin/regional air–sea CO₂ flux constraints.  
- **GLODAPv2**  Interior DIC/TA changes for ocean sink evaluation; carbonate system trends.  
- **NOAA/ESRL CO₂**  Mauna Loa & global marine boundary layer composites for growth‑rate checks.  
- **FLUXCOM/FLUXNET**  Land flux benchmarks (GPP/NEE/LE) & drought responses for β/γ evaluation.

---

## Diagnostics & validation
- **Budget closure**  EFOS + ELUC − (S_OCEAN + S_LAND) − G_ATM = residual within tolerance; report AF and its stability.  
- **Sinks partition**  Multi‑decadal means of S_LAND vs S_OCEAN close to GCB assessed values; reproduce post‑1990 trends and 2010s acceleration.  
- **Interannual variability**  Land sink anti‑correlated with ΔT/ENSO; ocean outgassing during strong El Niño captured.  
- **Ocean chemistry**  pCO₂ seasonal cycles & trends vs SOCAT; DIC/TA & pH trends vs GLODAP; basin masks.  
- **Land responses**  β & γ within assessed ranges; drought‑year anomalies (e.g., 2010, 2015–16, 2023–24) reproduced in sign and magnitude.  
- **CH₄ & N₂O**  Growth rates consistent with WMO/GCP; lifetime‑consistent sinks.

**Initial acceptance thresholds**  
- Budget residual |≤| 0.3 GtCO₂ yr⁻¹ (decadal means).  
- AF within 0.36–0.50 (multi‑decadal).  
- Basin‑wise ocean pCO₂ & flux trends coherent with SOCAT; interior carbon increases within GLODAP uncertainty.  
- Land β/γ posteriors physically plausible; reproduce major drought/heat event anomalies.

---

## Implementation plan (repo wiring)
- `/carbon/core/`  IRF carbon box (FaIR‑style) with temperature/concentration dependence; parameter priors & posteriors.  
- `/carbon/ocean/`  Gas‑exchange + carbonate chemistry (CO2SYS) diagnostics; basin partition; SOCAT/GLODAP evaluators.  
- `/carbon/land/`  β/γ emulator with pools (GPP/respiration/fire); N/P limitation scalar; drought/heat stress functions.  
- `/carbon/ghg_other/`  CH₄ and N₂O budget modules (wetlands, agriculture, fossil; lifetime & sinks).  
- `/carbon/datafeeds/`  GCB annual series; WMO GHG bulletin; SOCAT; GLODAP; NOAA ESRL; FLUXCOM/FLUXNET.  
- `/diagnostics/carbon_eval.ipynb`  Budget closure, AF, variability, basin fluxes, event composites.  
- `/tests/`  Budget residual tests; AF range assertions; SOCAT/GLODAP comparison thresholds; CH₄/N₂O growth‑rate checks.

---

## Pitfalls & guardrails
- **No double counting**  Keep **LULCC CO₂ emissions (ELUC)** separate from **ERF(LULCC)** in Module 1; distinct physical pathways.  
- **Priors vs reality**  Do not hard‑tune to AF; fit to sinks and growth rates while respecting physical priors.  
- **OH feedback**  Coordinate CH₄ lifetime with Module 10 chemistry to avoid inconsistent τ.  
- **Nitrogen limitation**  Account for N (and P) constraints on β; fertilization without nutrients is unrealistic.  
- **Event sensitivity**  Validate against ENSO and mega‑drought/fire years; ensure emulator generalizes beyond calibration.

---

## QA checklist (quick)
- [ ] Budget residual within tolerance; AF stable over decades.  
- [ ] S_LAND/S_OCEAN partition matches assessed means and trends.  
- [ ] SOCAT/GLODAP constraints passed for basin fluxes and interior carbon.  
- [ ] Land β/γ posterior within literature; reproduces event anomalies.  
- [ ] CH₄ and N₂O budgets produce observed growth rates with plausible τ and sink partitioning.

---

## Next actions
1) Import latest GCB (2024/2025) and compute closure/AF diagnostics.  
2) Calibrate IRF + β/γ to observed growth rates and sinks; produce parameter posteriors.  
3) Add SOCAT/GLODAP evaluators for basin pCO₂ and interior carbon trends.  
4) Wire CH₄/N₂O budget modules and coordinate OH/stratospheric loss with Module 10.  
5) Generate scenario‑ready emulator with uncertainty sampling for Modules 12, 13, 16.