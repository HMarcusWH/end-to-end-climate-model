# Module 11 — Sea Level (Total & Components) Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Reconstruct and project **global mean sea level (GMSL)** and **relative sea level (RSL)** with transparent **component attribution**:
- **Barystatic (mass)** from land ice (Greenland, Antarctica, glaciers) + terrestrial water storage (TWS),
- **Steric** (thermosteric + halosteric) from ocean warming/freshening (TEOS‑10),
- **Dynamic + gravitational/rotational/elastic** (GRD) fingerprints for regional change.
Ensure **budget closure** over the satellite era (altimetry ≈ steric + mass within uncertainty), quantify **acceleration**, and provide **emulator hooks** for scenario projections.

---

## Scope & Interfaces
- **Inputs**  Ocean heat content & MLD (Module 6); ice‑sheet/glacier/TWS mass change (Module 8); atmospheric/oceanic forcing (Modules 1–3); vertical land motion (VLM) fields for tide‑gauge corrections; GIA models.
- **Outputs**  GMSL & component time series (monthly/annual); **steric (0–700/0–2000 m & full‑depth)**; ocean‑mass (GRACE‑consistent) and its partitions (GrIS/AIS/glaciers/TWS); **regional sea‑level projections** using GRD fingerprints + dynamic patterns; **acceleration** metrics; **closure diagnostics**.
- **Coupling**  To Module 6 (steric from OHC), Module 8 (mass), Module 12 (energy‑balance calibration uses EEI↔OHC↔SSL links), Module 14 (regionalization).

---

## Methods blueprint
1) **Altimetry GMSL**  Merge TOPEX/Jason/Sentinel along with drift/benchmark corrections; remove inverse‑barometer as needed; propagate uncertainties.
2) **Steric**  Compute density‑driven sea level from Argo (0–2000 m) + Deep Argo where available; implement **TEOS‑10** EOS; report **thermosteric** vs **halosteric** contributions; fill deep‑ocean gap with constrained estimates.
3) **Mass (barystatic)**  From GRACE/GRACE‑FO ocean mass + partitions (Greenland, Antarctica, glaciers, TWS). Apply GIA corrections; provide consistency checks with Module 8.
4) **Budget closure**  Altimetry ≈ Steric + Mass within stated uncertainty; run closure both globally and per‑basin.
5) **Acceleration & variability**  Quadratic fits and windowed trends; attribute interannual wiggles (ENSO, volcanic) and decadal acceleration; provide event notes (e.g., La Niña 2010–11 drop/rebound).
6) **Regionalization**  Compose regional RSL = dynamic sterodynamic patterns (from OGCM/Module 6 or pattern scaling) + **GRD fingerprints** per mass source + local VLM + static equilibrium tide; provide coastal site diagnostics.
7) **Projections/emulator**  Probabilistic component‑wise emulator (steric from GMST/OHC; mass from calibrated ice‑sheet/glacier modules; TWS scenarios) → global and regional SLR with uncertainty and tail structure.

---

## Sliders (parameters & assumptions)

### A) Altimetry & reference
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Reference epoch | year | 1993.0 | Alt: 2005.0 baseline |
| Inverse‑barometer correction | – | on | off for sensitivity |
| Drift correction (TOPEX A/B) | – | vetted | Alt: legacy; affects early trend |
| GMSL smoothing window | months | 3 | 1–12; for variability diagnostics |

### B) Steric computation
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| EOS | – | TEOS‑10 | (required) |
| Depth range reported | m | 0–700 / 0–2000 / full | Expose all; deep‑ocean gap handling |
| Deep‑ocean infill method | – | constrained regression | Alt: Deep Argo blend; 0–4000 m tests |
| Halosteric include | – | on | Report thermo/halo split |

### C) Mass components & GIA
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| GIA model | – | Caron18 | Alt: ICE‑6G/VM5a … sensitivity ±0.2–0.3 mm yr⁻¹ |
| Greenland partition | % | from Module 8 | Live link to IMBIE/GRACE basins |
| Antarctic partition | % | from Module 8 | Shelf/grounded separation optional |
| Glaciers (RGI) | % | from Module 8 | Updates via WGMS/geodetic |
| TWS contribution | mm yr⁻¹ | model‑based | Hydrology/impoundment corrections |

### D) Regionalization & VLM
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Fingerprint set | – | Mitrovica‑style | Alternatives allowed; per‑source patterns |
| Dynamic pattern source | – | Module 6 | OGCM or pattern‑scaled fields |
| VLM field | – | GNSS+InSAR blend | Alt: tide‑gauge‑only (higher uncertainty) |
| Frame (RSL vs GMSL) | – | site‑relative | Include GIA/static‑equilibrium corrections |

### E) Acceleration & emulator
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Acceleration fit window | years | full record | 10–30‑yr windows for robustness |
| Steric–GMST scaling | mm K⁻¹ | fit | Basin‑specific options |
| Mass component priors | – | Module 8 | Tail structure (AIS high‑end) toggle |

---

## Data feeds (preferred)
- **Altimetry**  NASA/NOAA/CNES multi‑mission GMSL; Copernicus C3S/CMEMS L4 SLA products.
- **Ocean steric**  Argo (0–2000 m) + Deep Argo pilots; TEOS‑10 libraries.
- **Ocean mass & partitions**  GRACE/GRACE‑FO (global ocean mass) + Greenland/Antarctica basin time series; glacier & TWS models/estimates.
- **Tide gauges & VLM**  PSMSL RLR tide‑gauge records; GNSS/INSAR VLM for RSL corrections and site diagnostics.

---

## Diagnostics & validation (targets/tests)
- **Budget closure (1993→present)**  Altimetry ≈ Steric + Mass within global uncertainty (∼≤0.2–0.3 mm yr⁻¹ trend residual); interannual residuals explained by observation gaps or known events.
- **Trend & acceleration**  GMSL trend and **acceleration** consistent with satellite‑era assessments; seasonal/interannual variability (ENSO) represented.
- **Component shares**  Recent decades: mass and steric contributions each O(1–2 mm yr⁻¹); basin/regional contrasts reasonable; deep‑ocean steric non‑negligible in recent years.
- **Regional RSL**  Fingerprint patterns (e.g., near‑field fall around mass‑losing ice sheets) + dynamic patterns reproduce observed coastal/tide‑gauge trends after VLM correction.

**Initial acceptance thresholds**  
- Global budget residual trend |≤| 0.3 mm yr⁻¹;
- GMSL acceleration detected and within literature ranges;
- Regional RSL skill comparable to recent reconstructions;
- Component partitions (GrIS/AIS/glaciers/TWS vs steric) consistent with Module 8 & Argo.

---

## Implementation plan (repo wiring)
- `/sealevel/altimetry/`  Multi‑mission merge, IB/drift corrections, GMSL series.
- `/sealevel/steric/`  TEOS‑10 steric from Argo/Deep Argo; thermo/halo split; deep‑ocean infill.
- `/sealevel/mass/`  GRACE‑FO ocean‑mass; partitions (GrIS/AIS/glaciers/TWS) linked to Module 8; GIA options.
- `/sealevel/closure/`  Budget closure calculators & plots (global/basin); acceleration diagnostics; ENSO/volcanic notes.
- `/sealevel/regional/`  GRD fingerprints + dynamic patterns + VLM to produce site‑level RSL projections; coastal dashboards.
- `/tests/`  Regression tests for closure residual; acceleration range; component‑share sanity; VLM correction logic.

---

## Pitfalls & guardrails
- Use **TEOS‑10** (not fixed coefficients) for steric; handle halosteric carefully.
- Track **GIA/VLM** assumptions—dominant source of local uncertainty; do not conflate RSL and GMSL.
- Avoid absorbing residuals into any single component; diagnose altimeter drifts, GIA choices, and deep‑ocean gaps explicitly.
- Document **fingerprint set** and dynamic pattern source; coastal planning depends on them.

---

## QA checklist (quick)
- [ ] Satellite‑era budget closes within uncertainty (global & basin).  
- [ ] GMSL trend and acceleration agree with authoritative assessments.  
- [ ] Component partitions consistent with Module 8 & Argo/Deep Argo.  
- [ ] Regional RSL projections pass site‑level plausibility with VLM corrections.

---

## Next actions
1) Wire altimetry + Argo + GRACE‑FO loaders and compute historical closure + acceleration metrics.  
2) Validate component shares against Module 8 (IMBIE/GRACE) and Module 6 steric.  
3) Build regional fingerprint engine (GRD + dynamics) and prototype coastal site dashboards (with VLM).  
4) Expose projection emulator with scenario hooks and component‑wise uncertainty sampling.

