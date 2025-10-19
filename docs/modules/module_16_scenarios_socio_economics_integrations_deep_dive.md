# Module 16 — Scenarios, Socio‑economics & Integrations Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Provide a **scenario fabric** that links **socio‑economic drivers** (population, GDP, technology, policy) to **emissions, land use, air pollution**, and then to **concentrations, forcings, and temperatures** via Modules 1, 9–12. Deliver: (i) curated SSP/ScenarioMIP/IEA/NGFS pathways, (ii) a **policy‑lever sandbox** (carbon price, standards, subsidies, fossil phase‑out, land protection, CDR scale‑up), (iii) a **temperature/budget consistency** engine (FaIR/EBM), and (iv) reproducible hand‑offs to regional/sectoral impact models.

---

## Scope & Interfaces
- **Inputs**  Historical emissions (CEDS), concentrations (CMIP6), socio‑economic drivers (SSP), policy baselines (NDCs/IEA/NGFS), carbon‑cycle & climate emulators (Modules 9 & 12).  
- **Outputs**  Harmonized **emissions → concentrations → ERF → GMST/EEI**; sectoral & regional splits; land‑use/AFOLU flows; **remaining carbon budgets** and temperature outcomes per pathway; uncertainty ensembles.  
- **Coupling**  Emission & concentration time series to Module 1; land‑use and AFOLU to Modules 5/9; aerosols/precursors to Module 10; temperature/EEI to Modules 6/11/12; regionalization hooks to Module 14.

---

## Methods blueprint
1) **Scenario libraries**  Curate and version: **SSP‑RCP/ScenarioMIP** (SSP1‑1.9…SSP5‑8.5), **AR6 WGIII** scenario ensemble, **IEA WEO** (STEPS/APS/NZE), and **NGFS** transition pathways.
2) **Harmonization & downscaling**  Apply automated harmonization to ensure continuity with historical data; maintain sectoral coverage (energy/industry/transport/buildings/AFOLU/waste). Provide **country/regional** splits where available; aggregate consistently to global.  
3) **Emissions→Concentrations**  Use **FaIR** (and MAGICC as cross‑check) to convert multi‑gas emissions to **concentrations and ERF** with uncertainty samples; align with CMIP6 concentrations where appropriate.  
4) **Temperature/EEI**  Drive Module 12 EBM with ERF to produce GMST, **TCR/ECS‑consistent** trajectories, and **EEI/OHC** consistency checks.  
5) **Policy‑lever sandbox**  Parameterize levers: carbon price paths, coal/oil gas phase‑out dates, CCS/CDR scale‑up (DACCS/BECCS/afforestation), methane abatement, efficiency/electrification, renewables/nuclear build rates, land protection & diet shifts. Compute deltas vs baselines.  
6) **Budget & target checks**  Compute **remaining CO₂ budget** for temperature goals and **overshoot** metrics; flag feasibility tensions (CDR reliance, deployment rates, land competition).  
7) **Co‑pollutants & air quality**  Track SO₂/NOₓ/NH₃/BC/OC/VOCs to inform **aerosol forcing** and co‑benefits; include ship‑fuel sulfur and ammonia policy switches.  
8) **Documentation & provenance**  Every pathway tagged with source, version, harmonization choices, and emulator settings; reproducible notebooks.

---

## Sliders (scenario drivers & policy levers)

### A) Socio‑economics & demand
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Population trajectory | – | SSP2 | SSP1…SSP5; country/regional variants |
| GDP growth | % yr⁻¹ | SSP2 | SSP1…SSP5; alt: IEA/NGFS macro |
| Energy intensity decline | % yr⁻¹ | 2.0 | 1–3; sector‑specific options |
| Electrification rate (final energy) | % yr⁻¹ | 1.5 | 0.5–3; sector splits |

### B) Technology & systems
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| RE buildout max | GW yr⁻¹ | fit to IEA APS | region bounds; grid limits |
| Storage learning rate | % per doubling | 18 | 10–25; endogenous/exogenous |
| CCS capture rate | % | 90 | 85–98; sector‑specific |
| CDR scale (DACCS/BECCS/AF) | GtCO₂ yr⁻¹ | 0.5/2/1 | 0–5/0–10/0–4 by 2050 |

### C) Policy levers
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Carbon price growth | % yr⁻¹ | 5 | 3–10; Ramsey‑style consistent |
| Coal phase‑out (OECD/ROW) | year | 2030/2040 | ±10; unabated only |
| Methane abatement | % by 2030 | 30 | 0–75; oil&gas/ag/waste bundles |
| Zero‑emission vehicle sales share | % by 2030 | 60 | 30–100; light‑duty |
| Clean power share | % by 2030 | 75 | 60–95; regionally varied |

### D) AFOLU & land
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Deforestation end year | year | 2030 | 2025–2040 |
| Afforestation/reforestation | Mha | 200 | 0–500; constraints from Module 5 |
| Diet shift (beef −→ plant) | % kcal by 2050 | 10 | 0–30; affects CH₄/N₂O |
| Fertilizer efficiency gain | % by 2050 | 20 | 0–40; NH₃/N₂O linkage |

### E) Consistency & delivery
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Emulator choice | – | FaIR‑v2 | MAGICC‑v7 cross‑check |
| ERF prior width (aerosols) | – | AR6 | narrow/wide for sensitivity |
| Harmonization method | – | automated | manual overrides allowed |
| Uncertainty ensemble size | members | 200 | 50–1000 |

---

## Data feeds (authoritative)
- **SSP & ScenarioMIP**: SSP narratives & quantitative drivers; SSP‑GHG concentrations; harmonized scenario emissions.  
- **AR6 WGIII Scenario Database**: multi‑model mitigation pathways and temperature diagnostics.  
- **Historical emissions**: **CEDS** (anthropogenic gases/aerosols).  
- **Energy outlooks**: **IEA WEO** (STEPS/APS/NZE).  
- **Finance risk**: **NGFS** long‑term scenarios & macro indicators.  
- **Carbon budgets**: IPCC AR6 assessments; consistency with Module 12.

---

## Diagnostics & validation
- **Budget closure**  Emissions→concentrations→ERF→GMST reproduces historical **CO₂/CH₄/N₂O** trends and **GMST/OHC** within uncertainty;
- **Scenario integrity**  SSP‑RCP labels consistent (e.g., SSP2‑4.5); harmonization residuals small; sector/category sums match totals;
- **Targets & overshoot**  Report 50%/66% chance temperature outcomes; **remaining CO₂ budget** and any **overshoot** with CDR dependence and air‑quality side‑effects;
- **Plausibility checks**  Build rates, fuel phase‑outs, and AFOLU transitions within literature‑based feasible ranges;
- **Comparative framing**  Cross‑walk to IEA/NGFS classifications.

**Initial acceptance thresholds**  
- Historical replication errors within published uncertainty envelopes (concentrations, GMST);  
- Scenario names/metadata validated against sources;  
- Carbon‑budget estimates consistent with AR6 when driven by the same emulator settings;  
- IEA/NGFS cross‑walk reproduces headline indicators (energy mix, carbon price, macro paths) to within documented tolerances.

---

## Implementation plan (repo wiring)
- `/scenarios/catalog/`  YAML manifests for SSP/AR6/IEA/NGFS; provenance & licenses.  
- `/scenarios/harmonize/`  Automated emissions harmonization + sectoral reconciliation; country/regional roll‑ups.  
- `/scenarios/emulator/`  FaIR/MAGICC drivers (emissions→conc→ERF→T, EEI); uncertainty samplers.  
- `/scenarios/levers/`  Policy‑lever API (prices, phase‑outs, technology scalers, AFOLU switches); delta calculators.  
- `/diagnostics/scen_eval.ipynb`  Historical replication, temperature/budget checks, aerosol co‑benefit plots, feasibility dashboards.  
- `/deliverables/`  NetCDF/CSV packs; summary briefs; change logs.  
- `/tests/`  Unit tests for harmonization; regression tests on famous scenarios (SSP1‑1.9/SSP2‑4.5/SSP5‑8.5, IEA NZE/APS/STEPS); emulator cross‑checks.

---

## Pitfalls & guardrails
- **Scenario ≠ prediction**  Communicate that these are conditional pathways, not forecasts.  
- **Double counting**  Keep **LULUCF** emissions distinct from **ERF(LULCC)** (Module 1).  
- **Aerosol‑warming surprise**  Rapid SO₂ decline raises near‑term warming; quantify with Module 10 and report uncertainty.  
- **CDR reliance**  Flag pathways with large post‑2050 CDR and land competition; test DAC/BECCS feasibility bounds.  
- **Cross‑framework confusion**  Provide clear **SSP/ScenarioMIP ↔ IEA ↔ NGFS** mappings; document differences in macro drivers and policy assumptions.

---

## QA checklist (quick)
- [ ] Historical replication (conc/GMST) passes;  
- [ ] Scenario metadata & labels audit clean;  
- [ ] Temperature & remaining‑budget diagnostics consistent with AR6;  
- [ ] Feasibility dashboards (build rates, AFOLU) reviewed;  
- [ ] Cross‑walk to IEA/NGFS validated.

---

## Next actions
1) Ingest **SSP/ScenarioMIP** drivers + concentrations, **AR6 WGIII** scenarios, **CEDS** history, **IEA WEO 2024**, and **NGFS Phase IV/V** datasets.  
2) Run historical replication and calibrate FaIR/EBM settings to match AR6 baselines.  
3) Deliver a reference set (SSP1‑1.9, SSP2‑4.5, SSP3‑7.0, SSP5‑8.5) with uncertainty bands and remaining budgets.  
4) Build the **policy‑lever sandbox** and generate deltas vs. SSP2‑4.5 and IEA APS.  
5) Publish scenario packs and provenance with CI tests and change logs.

