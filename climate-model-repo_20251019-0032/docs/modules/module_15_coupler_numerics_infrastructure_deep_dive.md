# Module 15 — Coupler, Numerics & Infrastructure Deep Dive

_Last updated:_ 2025‑10‑18 (Europe/Stockholm)

## Purpose
Provide a robust, conservative, and portable **coupling/infrastructure layer** that glues all modules together with:
- **Correctness** (energy, water, tracer conservation; consistent calendars/time; restart integrity),
- **Reproducibility** (bit‑for‑bit where appropriate; statistical equivalence otherwise),
- **Performance/portability** (MPI/OpenMP/GPU‑capable; containerized builds), and
- **Provenance** (CF‑compliant outputs; end‑to‑end audit trails).

---

## Scope & Interfaces
- **Coupled components**  Atmosphere (2–4), Land (5), Ocean (6), Sea ice (7), Cryosphere (8), Biogeochem (9–10), Sea level diagnostics (11), EBM/emulator (12), D&A hooks (13), Regionalization (14), Scenarios (16).
- **Coupler role**  Time management; field registry; regridding & masking; flux accumulation & unit conversions; conservation diagnostics; run‑sequence orchestration; I/O and restart management.

---

## Architecture blueprint
### A) Coupler choices (primary + alternates)
1) **ESMF/NUOPC mediator (CMEPS)** — primary path. Provides NUOPC caps per component; central mediator handles field transforms and sequencing.  
2) **OASIS3‑MCT** — alternate path for legacy/RCM stacks; high‑performance parallel exchanges and remapping; simple namelist‑style configuration.  
3) **SCRIP/ESMF weight files** — interchangeable weight generation for regridding (conservative, bilinear, patch), stored and versioned under `/weights/`.

### B) Run sequence & time
- Canonical sequence (example): **ATM → CICE ↔ OCN → LND → BIOGEO → DIAG** per coupling step `Δt_cpl` (e.g., 1 h).  
- **Time management**  Proleptic Gregorian calendar; exact leap handling; restart boundaries aligned with coupling step; sub‑stepping permitted inside components; lag options documented.  
- **Flux handling**  Accumulate tendencies to the exchange interval; mediator performs unit conversions; enforce sign conventions.

### C) Exchanges & field registry (minimum viable set)
- **Atmos → Ocean/Ice**: wind stress, heat flux, freshwater/precip + runoff, radiation components, tracers (CO₂ flux tendency), sea‑level pressure.  
- **Ocean → Atmos/Ice**: SST/skin temp, sea‑ice fraction/thickness/surface temperature, surface currents, surface roughness; diagnostic bulk fluxes.  
- **Land ↔ Atmos**: sensible/latent heat, runoff/river discharge, snow properties, albedo/LULCC masks.  
- **Cryo ↔ Ocean**: basal melt rates, calving fluxes, freshwater/heat; **fingerprint hooks** for Module 11.  
- **Carbon/chem**: air–sea CO₂ flux, land NEE/fire, aerosol optical properties/AOD and Nd tendencies for radiation.

---

## Regridding, masking & conservation
- **Methods**  First/second‑order **conservative** for extensive quantities (fluxes, mass/heat), **bilinear/patch** for intensive states; normalize per ESMF scheme; persist weight files with checksums.  
- **Masks & coastlines**  Consistent wet/dry and land/sea/ice masks; explicit handling of **unmapped** destination cells; conservative holes treatment documented.  
- **Area/units**  All fluxes in **W m⁻²** / **kg m⁻² s⁻¹** on the **destination cell area** after regridding; mediator ensures conversions.  
- **Diagnostics**  Per‑step **conservation ledger** for water/energy/tracers (global and basin budgets); leakage < O(10⁻¹⁰) relative.  
- **Restart integrity**  Bit‑for‑bit restart across stop/start at arbitrary boundaries (within same build + layout), with unit tests.

---

## Numerics & stability guardrails
- **Coupling frequency**  Start at 1 h (global), 15 min for strong feedback tests; document sensitivity.  
- **Order of operations**  Deterministic reductions for global sums where needed; optional compensated summation for budgets.  
- **Lag options**  Single‑step lag for ocean/ice acceptable; flag where it changes effective feedback.  
- **Bulk formulas**  Single source of truth for air–sea flux bulk algorithm; passed as a library to both sides to avoid drift.

---

## Reproducibility policy
- **B4B tiers**  (i) **Strict**: same compiler/MPI/layout → **bit‑for‑bit**; (ii) **Relaxed**: same layout → B4B in coupler but component‑level statistical equivalence allowed; (iii) **Portable**: cross‑machine statistical reproducibility with documented tolerances.  
- **Known non‑determinism**  OpenMP reductions, MPI reduction order, GPU kernels; mitigate with reproducible reductions where performance allows.  
- **Port validation**  Standard smoke + restart + climate **ensemble consistency** tests; tolerances documented per variable.

---

## Build, packaging & runtime
- **Build system**  CMake + component makefiles; Fortran/C/C++ with optional CUDA/HIP/OpenMP.  
- **Dependencies**  **Spack** recipes for compilers, MPI, NetCDF, ESMF/ESMPy, OASIS, TEOS‑10; lockfiles for exact versions.  
- **Containers**  **Apptainer/Singularity** images for portable runs on HPC; dev images with compilers + libraries + test data.  
- **Launch**  MPMD/ESMF driver (separate MPI executables) or SPMD with internal partitioning; YAML run cards under `/cases/`.

---

## I/O, metadata & provenance
- **File format & metadata**  **CF‑conventions** netCDF; enforce `standard_name`, units, `cell_methods`, `grid_mapping`, bounds; include UUIDs, Git SHAs, build hashes.  
- **Provenance trail**  `:history` attribute logs run card, container/Spack spec, compiler flags; store checksums for inputs/weights; DOI for tagged releases.  
- **Logging/telemetry**  Coupler log stream with per‑step budgets, timings, MPI layout, and warnings on unmapped cells.

---

## Tests & CI/CD
- **Unit tests**  Field unit conversions; regridding kernel checks; time manager and calendar math.  
- **Restart tests**  Exact restart (B4B) across multiple boundaries and processor layouts (where supported).  
- **Budget tests**  Energy/water/tracer closure over N days; tolerance thresholds with alarms.  
- **Performance**  Scaling tests (weak/strong); communication/computation split; roofline hints.  
- **Pipelines**  Git CI on PR: build + unit + short coupled sanity; nightly longer regression incl. ensemble‑consistency metric.

---

## Sliders (operations & infrastructure)
| Slider | Units | Default | Range / Notes |
|---|---:|---:|---|
| Coupling frequency `Δt_cpl` | min | 60 | 15–180; regional nests may need 10–15 |
| Regridding method (fluxes) | – | conservative | first/second‑order; norm type dst/frac area |
| Regridding method (states) | – | bilinear | patch/nearest as sensitivity |
| Mask treatment | – | src∧tgt mask | choices: source, target, both |
| Unmapped dest cells | – | error | options: mask, fill; log all occurrences |
| B4B mode | – | strict | relaxed/portable; per‑component overrides |
| MPI layout | ranks | auto | per‑component rank fractions; load‑balance |
| Reduction scheme | – | reproducible | alt: fast (non‑deterministic) |
| Containerization | – | on | off for bare‑metal tuning |

---

## Implementation plan (repo wiring)
- `/coupler/driver/`  ESMF/NUOPC driver + run‑sequence; CMEPS mediator configs; OASIS alt.  
- `/coupler/caps/`  NUOPC caps for each component; standard import/export states; metadata.  
- `/regrid/`  Weight generation (ESMF/ESMPy & SCRIP); QA plots; checksums; mask management.  
- `/provenance/`  CF templates; run‑card schema; history/audit utilities.  
- `/infra/build/`  CMake tooling; **Spack** recipes; container (Apptainer) definitions.  
- `/tests/`  Unit + restart + budget + scaling; PR and nightly workflows.  
- `/docs/`  Operator guide; porting and B4B policy; troubleshooting.

---

## QA checklist (quick)
- [ ] **Exact restart** B4B on same machine/layout;
- [ ] **Global budgets** within tolerance every coupling step;
- [ ] **Unmapped cells** explicitly handled and logged;
- [ ] **CF‑compliant** outputs with full provenance;
- [ ] **CI pipelines** green on PR and nightly.

---

## Next actions
1) Stand up **CMEPS** with NUOPC caps for ATM/OCN/ICE/LND; run a 10‑day smoke + restart test.
2) Generate and checksum **ESMF/SCRIP** weights (conservative + bilinear) for baseline grids; enable mask logic.
3) Wire conservation diagnostics and per‑step ledgers; validate closure on a 1‑month coupled test.
4) Package **Spack** environment + **Apptainer** container; record exact build provenance; enable CI smoke tests.
5) Document B4B tiers and tolerances; add deterministic reduction options where needed.

