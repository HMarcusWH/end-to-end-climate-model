# Module 14 — Regionalization & Downscaling Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Translate global climate signals into **regional to local** climate information (means & extremes) with **traceable methods** and **quantified uncertainty**, aligned with IPCC AR6 guidance. Provide a modular pipeline supporting:
- **Pattern‑/warming‑level scaling** for rapid assessments,
- **Statistical downscaling & bias adjustment** (trend‑aware, uni‑ and multivariate),
- **Dynamical downscaling** with RCMs and convection‑permitting nests,
- **Evaluation & calibration** against observations/reanalysis, and
- Robust **post‑processing** (bias/variance/temporal structure preservation) for impacts models.

---

## Scope & Interfaces
- **Inputs**  Global projections/forcing from Modules 1, 9–13; observational grids & station networks; reanalyses (ERA5/ERA5‑Land); orography/land‑use masks from Module 5.
- **Outputs**  Region‑specific time series/maps of temperature/precipitation/winds/humidity (daily ↔ sub‑daily), extremes diagnostics (e.g., **TXx, TNn, Rx1day/Rx5day**), and uncertainty envelopes. Deliver artifacts at common grids (e.g., 0.25°, 0.1°, 12 km, 4 km) with provenance.
- **Coupling**  Regional diagnostics feed Module 16 scenarios, Module 11 coastal RSL narratives, and impacts pipelines (hydrology, fire, energy demand, etc.).

---

## Methods blueprint

### Track A — Pattern / Warming‑Level Scaling
1) **Pattern extraction**  Build per‑model spatial patterns of ΔT, ΔP, and selected extremes relative to global‑mean warming (W/m² optional) using historical + scenario runs. Use EOF‑ or regression‑based methods; store **warming‑level patterns** (e.g., +1, +2, +3 °C).
2) **Scaling**  Apply **pattern scaling** to user‑defined warming levels or time slices; optionally include **non‑linear** terms (Herger‑style) and circulation indices for sensitive regions. Provide **consistency checks** against full model fields.
3) **Uncertainty**  Propagate spread across GCMs and warming levels; expose structural flags for regions/variables where pattern scaling underperforms (monsoons, some extremes).

### Track B — Statistical Downscaling & Bias Adjustment
1) **Predictors/targets**  Choose predictors (local large‑scale fields, lapse‑rate, humidity, circulation analogs) and targets (Tmin/Tmax, P, wind, RH).
2) **Bias‑adjust‑only**  For grid‑aligned GCM/RCM outputs, apply **trend‑preserving methods** such as **QDM** to daily fields; for multivariate consistency across T–P–RH–WS, use **MBCn** (after univariate adjustment) with dependence preservation.
3) **Statistical downscaling methods**  Options include **BCSD**, **LOCA** (analog‑based), quantile mapping variants (QM/EQM/QDM), generalized additive models, and ML (only with strict trend‑preserving constraints).
4) **Wet‑day & intermittency handling**  Use frequency adaptation and stochastic infill consistent with observed wet‑day statistics; do not invent events beyond method limits.
5) **Extremes & tails**  Calibrate high‑quantile behavior (Q95–Q99.9) with tail‑robust fits; ensure **delta‑preservation** from GCM in QDM‑style methods; avoid artificial variance damping.

### Track C — Dynamical Downscaling (RCMs & CPMs)
1) **RCM layer (∼50–12 km)**  Drive regional climate models with selected GCMs; run ensembles following **CORDEX/CORDEX‑CORE** protocols over domains of interest (e.g., EURO‑/NA‑/AFR‑/SEA‑CORDEX). Evaluate historical skill.
2) **Convection‑permitting nests (∼4 km)**  Optional CPM nests for heavy‑precipitation/convective extremes; run time‑slice experiments for select decades due to cost; bias‑adjust outputs minimally and trend‑aware.
3) **HighResMIP/HR‑GCMs**  Where available, integrate **HighResMIP** global runs as an intermediate fidelity source and for boundary condition sensitivity tests.

---

## Sliders (method choices & priors)

### A) Pattern/Warming‑level scaling
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Pattern source | – | CMIP6 MME | Subset by skill/independence; add HighResMIP option |
| Functional form | – | linear in ΔT_g | + quadratic / circulation term |
| Variable set | – | T, P | + Rx1day, TXx, TNn (where robust) |
| Emergence threshold | σ | 2 | 1.5–3; for masked display |

### B) Statistical downscaling / bias adjustment
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Bias‑adjust method | – | QDM | QM/EQM/QDM; **trend‑preserving preferred** |
| Multivariate correction | – | off | **MBCn on** for T–P–RH–WS sets |
| Downscaling scheme | – | BCSD | LOCA/BCSD/GAM/ML (with constraints) |
| Training period | years | 1981–2014 | 1971–2000 / 1995–2014; match obs availability |
| Cross‑validation | folds | 5 | K‑fold or block‑CV; ENSO‑aware |
| Wet‑day adjustment | – | on | Thresholding + drizzle correction |
| Tail fit method | – | empirical | GP/POT for Q>0.95 where sample permits |

### C) Dynamical downscaling
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Domain | – | EURO/NA | Any CORDEX domain |
| Resolution | km | 12 | 50–12 RCM; 4 CPM (time‑slice) |
| Physics set | – | RCM default | Convection on/off (CPM), microphysics choice |
| Boundary GCMs | count | 5 | 3–10; span warming & circulation |
| SST/sea‑ice BCs | – | interpolated | Consistent with Module 7 & 6 |

### D) Post‑processing & delivery
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Grid & resolution | – | 0.1° | 0.25°/0.1°/12 km/4 km |
| Bias‑adjust cadence | – | monthly | monthly/seasonal; daily for extremes |
| Quantile inflation guard | – | on | Prevent variance damping |
| Multivariate coherence | – | on | Preserve T–RH, P–WS dependencies |

---

## Data feeds (preferred)
- **Observations**  Regional high‑quality grids (e.g., **E‑OBS** Europe, **PRISM**/Livneh North America), station networks (**GHCN‑D**, national services), and **HadEX** extremes indices.
- **Reanalyses**  **ERA5** / **ERA5‑Land** for spatial/temporal structure; caution on trends.
- **GCMs/RCMs**  **CMIP6** (incl. HighResMIP where relevant), **CORDEX**/**CORDEX‑CORE** regional ensembles; domain masks and land–sea/orography from Module 5.

---

## Diagnostics & validation
- **Skill**  Bias, RMSE, correlation; distributional scores (**CRPS**, quantile score); wet‑day frequency, spell length; extremes (**Q‑Q slopes**, **Rx1day/Rx5day** biases).
- **Trend preservation**  Confirm that downscaling/bias adjustment **does not distort GCM trends** beyond method intent (QDM/MBCn checks).
- **Cross‑validation**  K‑fold or block‑CV across years/seasons; perfect‑model tests where feasible (RCM driven by reanalysis/other GCMs).
- **Added value**  Document when/where RCM/CPM resolution improves processes (or not); report against simple pattern‑scaling baselines.

**Initial acceptance thresholds**  
- Bias‑adjusted distributions match observed mean/variance/quantiles within predefined tolerances;
- Trend diagnostics pass (Δ means/quantiles preserved for QDM/MBCn);
- RCM historical skill competitive with CORDEX literature;
- Extremes metrics within observational uncertainty for regions with adequate station density.

---

## Implementation plan (repo wiring)
- `/regional/pattern_scaling/`  Pattern extraction per model; warming‑level library; scaling engine; masks of low‑robustness regions.
- `/regional/stat_down/`  QDM/QM/EQM, **MBCn** multivariate, **BCSD/LOCA** implementations; wet‑day adaptation; tail fits; CV tooling.
- `/regional/dyn_down/`  RCM orchestration (CORDEX‑style), CPM nests, boundary condition prep, job configs; skill dashboards.
- `/regional/obs/`  Data loaders for E‑OBS/PRISM/GHCN‑D/HadEX/ERA5; quality‑control hooks and homogenization notes.
- `/regional/diagnostics/`  Skill & distributional metrics, trend‑preservation tests, added‑value analyzers, perfect‑model tests.
- `/deliverables/`  Region packs (NetCDF + notebooks), extremes briefs, provenance JSON.

---

## Pitfalls & guardrails
- **Non‑stationarity**  Bias correction can’t reliably fix future trend errors; prefer **trend‑preserving** adjustments (QDM/MBCn) and document assumptions.
- **Over‑confidence**  RCMs add detail, not guaranteed skill; always compare to pattern‑scaling baselines.
- **Data limitations**  Sparse stations limit extremes calibration; communicate uncertainty explicitly.
- **Conservation & coherence**  Preserve water/energy balances and multivariate dependencies; avoid creating implausible T–P combinations.
- **Calendars & masks**  Handle calendars (365‑day/360‑day/leap) and changing land/sea/ice masks consistently.

---

## QA checklist (quick)
- [ ] Trend‑preserving bias adjustment validated (QDM/MBCn tests).  
- [ ] Cross‑validated skill & extremes metrics reported for each region.  
- [ ] RCM/CPM added value (or lack thereof) documented; perfect‑model tests run.  
- [ ] Pattern‑scaling products delivered with robustness flags.  
- [ ] All artifacts versioned with full provenance.

---

## Next actions
1) Stand up **pattern‑scaling** library with warming‑level products (+1/+2/+3 °C) and robustness masks.  
2) Implement **QDM** + **MBCn** pipelines; run benchmark on two pilot regions (Europe, North America).  
3) Spin up a **CORDEX‑style** mini‑ensemble (≥5 GCMs × 2 RCMs @ 12 km) for one domain; evaluate against observations and pattern‑scaling baselines.  
4) Deliver **Region Packs** (means & extremes) and document method limits for users.

