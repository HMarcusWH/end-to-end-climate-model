# Climate E2E — 16 Silos Research Plan

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

This document outlines objectives, key questions, data, methods, validation, and deliverables for **16 core modules** of a logically complete end‑to‑end climate model. Use this as the master checklist/roadmap.

---

## 1) External Forcings (GHGs, Aerosols, Solar, Volcanic)
**Objective**  Build a defensible historical + scenario ERF time series by agent (1750→present→2100+).  
**Key questions**  ERF best estimates & uncertainty; harmonization of historical→SSP; overlap terms; aerosol split (ERFari/ERFaci).  
**Priority data**  CEDS emissions; concentrations (SSP/MAGICC/FaIR); AR6 ERF tables; solar TSI; volcanic SAOD.  
**Methods & tools**  Emissions→concs→ERF conversions; Etminan coefficients; offline RT sanity checks; harmonize to AR6 taxonomy; propagate uncertainties (MC).  
**Validation**  Net ERF reproduces AR6; closure against observed EEI (CERES+Argo).  
**Deliverables**  Versioned ERF bundle (CSV/NetCDF) + notebook regen; uncertainty envelopes.

---

## 2) Atmosphere — Dynamics & Radiation
**Objective**  Achieve realistic circulation and radiative fluxes for global energy balance fidelity.  
**Key questions**  TOA/SFC flux bias; cloud‑radiative effects (CRE); jets/Hadley cell structure.  
**Data**  CERES EBAF; ERA5 (winds, T, q).  
**Methods & tools**  Column RT (RRTMG) tests; zonal flux diagnostics; mean‑state + variability checks vs ERA5.  
**Validation**  Net TOA flux bias < ~0.2 W m⁻²; realistic zonal CRE patterns; wind/jet metrics.  
**Deliverables**  Atmos radiation test suite + diagnostics pack.

---

## 3) Clouds & Convection
**Objective**  Capture CRE magnitude/partition and precipitation efficiency via microphysics + convective parameterizations.  
**Key questions**  LW/SW CRE split; shallow vs deep convection balance; emergent constraints.  
**Data**  CERES CRE; ERA5 cloud proxies; field campaign composites (optional).  
**Methods & tools**  SCM/column tuning; sensitivity sweeps; emulator for uncertainty.  
**Validation**  CRE biases and diurnal cycle over land/ocean; precipitation phase/efficiency stats.  
**Deliverables**  Tuned cloud/convection configs + uncertainty ranges.

---

## 4) Hydrological Cycle (P–E–R, Extremes)
**Objective**  Close global water budget and represent extremes scaling.  
**Key questions**  Clausius–Clapeyron scaling (~7%/K) for heavy precip; drought metrics; runoff closure.  
**Data**  GPCP/GPCC precip; reanalysis evap/soil moisture.  
**Methods & tools**  Global P≈E checks; Rx1day/TXx diagnostics; return‑period analysis.  
**Validation**  Seasonal cycles; extreme‑tail scaling vs obs.  
**Deliverables**  Hydrology dashboard + extremes benchmarks.

---

## 5) Land Surface, Vegetation & Albedo (incl. LULCC)
**Objective**  Represent land energy/water exchange and albedo/ET responses to land‑use change.  
**Key questions**  Magnitude/timing of LULCC forcing; ET–albedo trade‑offs by biome.  
**Data**  Land cover histories; flux tower networks; albedo climatologies.  
**Methods & tools**  Offline land model; LULCC forcing derivation; coupling tests.  
**Validation**  Surface fluxes vs towers/reanalyses; albedo biases.  
**Deliverables**  Land parameter set + LULCC forcing file + uncertainty.

---

## 6) Ocean Circulation & Heat Uptake
**Objective**  Match OHC growth, mixed‑layer depth, and overturning patterns.  
**Key questions**  Vertical diffusivity and ocean heat‑uptake efficiency; basin heat partitioning; AMOC sensitivity.  
**Data**  Argo profiles; NOAA/NCEI OHC; ocean reanalyses.  
**Methods & tools**  Constrain κ and Kz; compare MLD, transports; steric sea‑level from OHC.  
**Validation**  OHC trend/variability; steric SLR consistency.  
**Deliverables**  Ocean tuning dossier + heat‑budget closure notebooks.

---

## 7) Sea Ice
**Objective**  Simulate extent, thickness, seasonality, albedo feedbacks.  
**Key questions**  Thermodynamics vs dynamics; melt‑pond/albedo calibration.  
**Data**  NSIDC sea ice index; thickness proxies (ICESat‑2/PIOMAS).  
**Methods & tools**  Stand‑alone CICE tests; coupled runs; rheology/albedo parameter sweeps.  
**Validation**  Trend & seasonal cycle skill by basin; thickness distributions.  
**Deliverables**  Sea‑ice parameter set + evaluation pack.

---

## 8) Ice Sheets, Glaciers & Permafrost
**Objective**  Quantify cryosphere contributions to sea level and carbon feedbacks.  
**Key questions**  AIS/GrIS SMB & dynamics; glacier mass‑balance; permafrost carbon release pathways.  
**Data**  ISMIP protocols; Randolph Glacier Inventory; permafrost maps.  
**Methods & tools**  Downscaled SMB forcing; simple ISM coupling/emulation; permafrost response parameterization.  
**Validation**  Mass‑balance vs GRACE/altimetry; literature‑consistent permafrost ranges.  
**Deliverables**  Component SLR time series + permafrost feedback scenarios.

---

## 9) Carbon Cycle (Land & Ocean) + Other Biogeochem
**Objective**  Close the modern carbon budget and emulate sinks under scenarios.  
**Key questions**  Partitioning (atm/land/ocean); TCRE consistency; sensitivity to warming/CO₂.  
**Data**  Global Carbon Budget (annual); CO₂ growth rate; ocean pCO₂; LAI/biome data.  
**Methods & tools**  Calibrate simple carbon cycle (e.g., FaIR/MAGICC IRF) to observed sinks; ENSO‑linked variability checks.  
**Validation**  Budget residual ~0; interannual variability captured.  
**Deliverables**  Calibrated carbon‑cycle emulator + update script.

---

## 10) Atmospheric Composition & Aerosols/Chemistry
**Objective**  Capture aerosol optical properties and cloud interactions with uncertainty.  
**Key questions**  Regional AOD/SSA/AE biases; ERFari vs ERFaci apportionment.  
**Data**  CEDS emissions; MODIS/AERONET AOD; ozone/NOx/VOC datasets.  
**Methods & tools**  Chemistry/aerosol module driven by emissions; AOD validation; ERF inference with uncertainty.  
**Validation**  AOD RMSE; aerosol ERF within assessed ranges.  
**Deliverables**  Aerosol forcing dataset + regional diagnostics.

---

## 11) Sea Level (Total & Components)
**Objective**  Reconstruct and project GMSL with component attribution.  
**Key questions**  Thermosteric vs land‑ice mass contributions; acceleration and closure.  
**Data**  Satellite altimetry (TOPEX/Jason/CryoSat‑2); GRACE/GRACE‑FO; tide gauges.  
**Methods & tools**  Decompose GMSL into steric + mass; regional sea‑level fingerprints.  
**Validation**  Trend & acceleration within observational bounds; closure with OHC/cryosphere.  
**Deliverables**  SLR component series + projection emulator hooks.

---

## 12) Energy Balance & Climate Response (ECS/TCR, Emulators)
**Objective**  Constrain ECS/TCR and heat‑uptake using GMST + OHC + ERF.  
**Key questions**  Posteriors for λ, κ, Cs, Cd; implied ECS/TCR; EEI consistency.  
**Data**  GMST (HadCRUT/Berkeley/ERA5); CERES EEI; OHC.  
**Methods & tools**  Two‑layer EBM & FaIR calibration (Bayesian/MC); energy‑closure penalty.  
**Validation**  ECS/TCR within assessed ranges; skill on withheld periods; EEI ~0.7–1.0 W m⁻² in 2010s.  
**Deliverables**  Calibrated emulator + parameter posteriors.

---

## 13) Detection & Attribution
**Objective**  Attribute observed changes to forcings and quantify scaling.  
**Key questions**  GHG vs aerosol vs natural fingerprints; regional attributions; counterfactuals.  
**Data**  Observations/reanalyses; single‑forcing ensembles (from emulator).  
**Methods & tools**  Optimal fingerprinting/regression; pattern‑based attribution; uncertainty decomposition.  
**Validation**  Robust detectability of anthropogenic signals across variables.  
**Deliverables**  D&A report with scaling factors + counterfactual diagnostics.

---

## 14) Regionalization & Downscaling
**Objective**  Translate global signals to regional means & extremes.  
**Key questions**  When to use pattern scaling vs statistical/dynamical downscaling; bias correction schemes.  
**Data**  Observational grids (temp/precip), station networks; AR6 regional guidance.  
**Methods & tools**  Pattern‑scaling pipeline; quantile mapping; RCM gateway (optional).  
**Validation**  Cross‑validation vs historical regional obs; extremes skill.  
**Deliverables**  Region packs (time series, extremes, narratives).

---

## 15) Coupler, Numerics & Infrastructure
**Objective**  Ensure stable, conservative coupling and reproducible workflows.  
**Key questions**  Exchange frequencies; conservation; performance/portability.  
**Data**  Coupler/ESMF docs; CI/CD logs.  
**Methods & tools**  Spin‑up protocol; conservation checks; containerized builds; regression tests.  
**Validation**  Energy/water conservation across interfaces; bit‑reproducible runs.  
**Deliverables**  Coupling spec + CI tests & containers.

---

## 16) Scenarios, Socio‑economics & Integrations
**Objective**  Drive futures using SSPs & sectoral pathways; keep inputs harmonized.  
**Key questions**  Scenario selection & alignment; extension beyond 2100; mitigation/CDR pathways.  
**Data**  SSP database; ScenarioMIP; concentration/forcing sets.  
**Methods & tools**  Emissions→concs→ERF via emulator; scenario registry; stress‑test variants.  
**Validation**  Consistency vs official ScenarioMIP datasets.  
**Deliverables**  Scenario catalog + precomputed emulator outputs.

---

## Cross‑cutting Practices (apply to all 16)
- **Provenance & versioning**  NetCDF + JSON metadata, DOIs, reproducible notebooks.
- **Uncertainty**  Parametric & structural ensembles; propagate to impacts; AR6 likelihood language.
- **Annual refresh hooks**  GMST, OHC, GMSL, emissions, carbon budget.
- **Governance**  Owners, milestones, status tags; decision logs.

---

## Project Kanban (starter)
- **Backlog**  1, 3, 5, 8, 13  
- **In progress**  2, 6, 12, 15  
- **Next up**  4, 7, 9, 10, 11, 14, 16  

> Replace with live status as we staff modules. Add links to repos/notebooks per module.

