# Module 13 — Detection & Attribution (D&A) Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Quantify the **human contribution** to observed climate changes using statistically robust, physically interpretable methods. Provide:
- Multi‑variable **scaling factors** for **GHG**, **aerosol**, and **natural** fingerprints.
- **Counterfactual reconstructions** (world‑that‑wasn’t) for trends and extremes.
- Ready‑to‑use **event‑attribution** tools (risk‑based) and uncertainty propagation for scenarios.

---

## Scope & Interfaces
- **Inputs**  Observations/reanalyses (GMST, SAT, precipitation, OHC, sea level, sea ice, circulation indices); **single‑forcing fingerprints** from DAMIP/CMIP6 or Module 12 emulator; ERF histories (Module 1).  
- **Outputs**  Scaling factors with uncertainties; detection/consistency tests; counterfactual time series/maps; event‑attribution risk ratios (RR) and fractions attributable (FAR); regional attribution briefs for Module 14.

---

## Methods blueprint
1) **Optimal Fingerprinting (OF)**  Linear model y = Xβ + ε where y are observed changes, X are model fingerprints (GHG, AER, NAT), β the **scaling factors**. Use **Total Least Squares** with control‑run covariance; implement **Regularized Optimal Fingerprinting (ROF)** to stabilize covariance and truncation.  
2) **Experiment design (DAMIP)**  Use single‑forcing historical ensembles (historical, hist‑GHG, hist‑aer, hist‑nat) to form fingerprints; ensure ≥3 members per model; build multi‑model mean + uncertainty.  
3) **Residual & consistency tests**  Verify model variability vs observations; run **residual consistency** χ² tests; detectability = β’s confidence intervals exclude 0; **attribution** when β includes 1 and excludes 0 (or via joint constraints).  
4) **Multi‑variable D&A**  Joint fits for **GMST + OHC + SLP + precipitation** (and/or regional SAT) to reduce degeneracy (aerosol vs GHG) and leverage complementary physics.  
5) **Counterfactual reconstructions**  y_cf = y − X_ANT β_ANT for trend‑level counterfactuals; propagate covariance to uncertainty; generate maps and regional series.
6) **Event attribution (risk‑based)**  Two‑world framework: estimate probability of event in **factual** world (p1) and **counterfactual** (p0) from large ensembles/conditioned simulations; report **Risk Ratio (RR = p1/p0)** and **FAR = 1 − p0/p1**; provide storyline diagnostics (thermodynamic/dynamic contributors).  
7) **Robustness suite**  EOF truncation sensitivity, covariance shrinkage, leave‑one‑model‑out, alternative baselines, observational dataset swaps, ENSO‑regressed variants.

---

## Sliders (parameters & assumptions)

### A) Fingerprints & regression
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Fingerprint set | – | DAMIP MMmean | hist‑GHG, hist‑aer, hist‑nat; multi‑model mean + spread |
| EOF truncation (space/time) | modes | 20 | 10–60; per‑variable tuning |
| ROF regularization λ | – | auto | Cross‑validated; 0–1 manual override |
| Control‑run length (per model) | years | 500 | ≥ 300; pooled covariance |
| Regression domain | – | global + land‑only | Toggle basins/regions |
| Variables in joint fit | – | GMST+OHC | +SLP, precip, regional SAT, sea ice |

### B) DAMIP/forcing options
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Models included | count | all available | Mask low‑skill models; sensitivity sets |
| Historical period | years | 1850–2024 | Sub‑periods 1900+, 1950+ |
| Forcing split | – | GHG + AER + NAT | Optionally GHG sub‑splits (WMGHG vs O₃) |

### C) Event attribution
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Event definition | – | user‑spec | Percentile threshold, return period, spatial mask |
| Conditioning | – | ENSO‑aware | Circulation indices or flow‑analogues |
| Ensemble source | – | large‑N | SMILEs, hindcast ensembles, emulator augmentation |
| Metric | – | RR & FAR | Provide both with CIs |

### D) Robustness & uncertainty
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Covariance shrinkage | – | Ledoit–Wolf | Alt: ridge; per‑variable |
| Observation dataset choice | – | HadCRUT5 | Alt: Berkeley/ERA5/NOAA; swap tests |
| Internal variability model | – | control‑based | AR(1)/ARMA sensitivity |

---

## Data feeds (preferred)
- **Observations**  HadCRUT5/Berkeley/NOAA SAT; ERA5 reanalysis; Argo OHC; CERES EEI; GPCP/GPCC precipitation; PSMSL/tide‑gauges & altimetry; NSIDC sea‑ice indices.  
- **Fingerprints**  CMIP6 **DAMIP** single‑forcing ensembles (hist‑GHG, hist‑aer, hist‑nat) + historical all‑forcing; emulator‑derived single‑forcing from Module 12 where needed.  
- **Controls**  CMIP6 piControl runs (≥300–500 years per model) pooled for covariance.  
- **Event attribution**  Large ensembles (SMILEs), hindcast systems, or weather@home/WWA datasets.

---

## Diagnostics & validation (targets/tests)
- **Global warming**  Detect/attribute anthropogenic signal (β_ANT > 0) with β_GHG ~ O(1) and β_AER < 0; residual test passed.  
- **Multi‑variable checks**  Joint fits reduce GHG–aerosol degeneracy; OHC scaling consistent with EEI/OHC constraints.  
- **Regional & variable detections**  Hot extremes ↑, cold extremes ↓, heavy precip ↑, OHC ↑, GMSL ↑, Arctic sea‑ice ↓ detected and attributed within assessed ranges.  
- **Counterfactuals**  Provide 1900→present maps/series showing anthropogenic fraction of change with uncertainty bands.  
- **Events**  RR and FAR with CIs; thermodynamic vs dynamic contributions discussed where feasible.

**Initial acceptance thresholds**  
- β_GHG includes 1 and excludes 0 at 5%–10% level; β_AER significantly < 0; β_NAT consistent with small contribution.  
- Residual‑consistency test not rejected at 5% (or documented reasons/adjustments).  
- Counterfactual reconstructions reproduce standard D&A figures in sign/magnitude.

---

## Implementation plan (repo wiring)
- `/da/fingerprints/`  Build fingerprints from DAMIP/MME; preprocessing & EOF truncation.
- `/da/optimal_fp.py`  OF/ROF solver with TLS, residual tests, multi‑var support; covariance tools.  
- `/da/counterfactuals.py`  Construct anthropogenic‑removed reconstructions with full uncertainty.  
- `/da/events/`  Risk‑based event attribution calculators (RR, FAR) with conditioning options.  
- `/da/datafeeds/`  Obs & reanalysis loaders; DAMIP interfaces; control‑pool builder.  
- `/diagnostics/da_eval.ipynb`  Scaling‑factor posteriors; residual tests; robustness suite; counterfactual maps; event examples.  
- `/tests/`  Unit tests (TLS math), regression tests (β targets), covariance sanity, leave‑one‑model‑out stability.

---

## Pitfalls & guardrails
- **Covariance misspecification** blows up CIs: use ROF, long controls, and robustness checks.  
- **Aerosol–GHG degeneracy**: rely on multi‑variable fits (OHC/precip/SLP) and DAMIP fingerprints to separate.  
- **Observational inhomogeneities**: test dataset swaps; use HadCRUT/Berkeley masks consistently.  
- **Over‑interpretation of single events**: keep RR/FAR context and uncertainties front‑and‑center; communicate assumptions.  
- **P‑hacking/selection bias**: predefine hypotheses/regions; guard with multiple‑testing controls for extremes.

---

## QA checklist (quick)
- [ ] β scaling factors satisfy detection/attribution criteria; residual test passed.  
- [ ] Joint multi‑variable fit improves separability vs temperature‑only.  
- [ ] Counterfactual reconstruction & uncertainty reproduced for headline variables.  
- [ ] Event‑attribution example replicates published RR/FAR within CIs.  
- [ ] All inputs/outputs versioned with provenance.

---

## Next actions
1) Assemble DAMIP fingerprints + pooled control covariance; stand up OF/ROF solver.  
2) Run global/land SAT + OHC joint attribution; publish β posteriors and counterfactual GMST.  
3) Add regional SAT/precip and extremes; deliver example event‑attribution notebook (heatwave & heavy rain cases).  
4) Wire outputs to Module 14 for regional narratives and to Module 16 for scenario‑conditioned attribution.

