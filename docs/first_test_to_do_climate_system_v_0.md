# First Test To‑Do — Climate System v0

A single, tick‑down checklist to get the **first smoke test** running: a short coupled run that checks **energy/water/tracer budgets**, **bit‑for‑bit restart**, and produces the minimal artifacts for gates. It leans on the wiring & synthesis plans already in the repo.

---

## 0) One‑time repo setup (shared registries & CI skeleton)
- [ ] Add **shared constants registry** → `shared/constants.yaml` (use stub in *Missing Pieces* doc).  
  Sources: [CF Standard Names](https://cfconventions.org/standard-names.html), [UDUNITS](https://www.unidata.ucar.edu/software/udunits/).
- [ ] Add **coupler field registry** → `coupler/field_registry.yaml` (make conservation flags & sign conventions explicit).  
  See stub in `climate_model_missing_pieces_ready_to_paste_stubs_v_0.md`.
- [ ] Add **artifact schemas** (what CI expects) → `docs/artifact_schemas/…` (chem/ebm/ocean/sealevel/atmos/carbon/coupler).  
  Stubs in `climate_model_missing_pieces_ready_to_paste_stubs_v_0.md`.
- [ ] Add **provenance template** → `docs/provenance_template.yaml`.
- [ ] Add **dataset registry** → `registry/datasets.yaml` (use pull‑list & links in `climate_model_missing_items_source_links_v_1.md`).
- [ ] Add **CI workflow** → `.github/workflows/ci.yml` (schema validation + acceptance tests).  
  Stub in `climate_model_missing_pieces_ready_to_paste_stubs_v_0.md`.
- [ ] Verify `acceptance_gates.yaml` reflects thresholds you want for v0 (EEI/OHC/SLR closure, aerosol ERF range, budgets).

---

## 1) Close the four wiring hooks (must‑have before smoke)
- [ ] **Land → Forcings (LULCC ERF)**  
  Export `land/erf_lulcc_timeseries.csv` and have Module 1 read it (no hardcoded −0.20 W m⁻²).  
  Contract: `land/EXPORTS.md`.
- [ ] **Chem → Forcings (post‑2010 aerosol weakening)**  
  Write `chem/erf/post2010_weakening_metric.json { weakening_percent_since_2010 }`; Module 1 consumes it.  
  Contract: `chem/EXPORTS.md`.
- [ ] **Chem ↔ Carbon (CH₄ lifetime)**  
  `chem/diagnostics.json` must include `ch4_lifetime_years`; Module 9 ingests & echoes `assumed_ch4_lifetime_years` in its diagnostics.  
  Contract: `carbon/CONTRACT.md`.
- [ ] **Sea level/steric → EBM**  
  EBM calibration reads `ocean/ohc_summary.json` and/or `sealevel/closure.json` for a steric consistency check.  
  Contract: `ebm/CONTRACT.md`.

> All four are spelled out (with ready‑to‑paste stubs) in `climate_model_missing_pieces_ready_to_paste_stubs_v_0.md` and the source links in `climate_model_missing_items_source_links_v_1.md`.

---

## 2) Minimum data needed (exact upstreams)
- **Radiation/EEI**: CERES EBAF → [https://ceres.larc.nasa.gov/data/ebaf/](https://ceres.larc.nasa.gov/data/ebaf/)
- **Ocean heat content (OHC)**: IAP/NOAA (0–700/0–2000 m) → see IAP portal in the links doc.  
- **Sea level components**:
  - GMSL (altimetry): NASA/JPL → [https://sealevel.nasa.gov/…/global-mean-sea-level](https://sealevel.nasa.gov/understanding-sea-level/key-indicators/global-mean-sea-level)  
  - Ocean mass: GRACE/GRACE‑FO mascons → [https://grace.jpl.nasa.gov/data/get-data/jpl_global_mascons/](https://grace.jpl.nasa.gov/data/get-data/jpl_global_mascons/)  
  - Ice sheets: IMBIE → [https://imbie.org/](https://imbie.org/)
- **Aerosol/chem eval**: AERONET → [https://aeronet.gsfc.nasa.gov/](https://aeronet.gsfc.nasa.gov/), MODIS MAIAC AOD → [https://lpdaac.usgs.gov/products/mcd19a2v006/](https://lpdaac.usgs.gov/products/mcd19a2v006/)
- **Standards**: CF Conventions → [https://cfconventions.org/](https://cfconventions.org/), UDUNITS → link above.

> Register each dataset (name, URL, version, license, checksum) in `registry/datasets.yaml` before first run.

---

## 3) Build & run — the **smoke test** (first test)
**Goal:** a short (e.g., 5–10 day) coupled run that (i) closes budgets each coupling step, (ii) passes exact restart, and (iii) produces base artifacts under `artifacts/`.

1) **Build environment**  
   - [ ] Install with Spack or containers (Apptainer). Pin compilers, MPI, NetCDF, ESMF/ESMPy.  
   - [ ] Confirm `coupler/driver` builds; RRTMG/RTE+RRTMGP (Module 2) compiled; minimal stubs for Modules 6–7–9–10 present.

2) **Case file**  
   - [ ] Create `cases/smoke_10day.yaml` with:
     - `Δt_cpl: 3600 s` (1‑hour coupling), conservative regridding for fluxes, bilinear for states.
     - Start date: recent year with data coverage.
     - Enable conservation ledger + restart at day 5 to test B4B.

3) **Run**  
   - [ ] `./run_case cases/smoke_10day.yaml` (or your launcher wrapper).
   - [ ] On day 5: stop, write restart, resume → verify bit‑for‑bit.

4) **Export minimal artifacts to `artifacts/`**  
   - [ ] `coupler/conservation_ledger.json`  
   - [ ] `atmos/ceres_eval.json` (TOA net bias, CRE SW/LW/NET)  
   - [ ] `ocean/ohc_summary.json` (dH/dt)  
   - [ ] `sealevel/closure.json` (trend residual)  
   - [ ] `chem/diagnostics.json` (incl. `ch4_lifetime_years`)  
   - [ ] `land/erf_lulcc_timeseries.csv`  
   - [ ] `chem/erf/post2010_weakening_metric.json`

5) **CI/pytest**  
   - [ ] `pytest -q` (runs acceptance tests + JSON‑schema validation).

---

## 4) Pass/fail gates for the smoke
- **Budgets (per coupling step)**: global energy/water/tracers leak ≈ 0 (within numeric tolerance).  
- **Restart**: bit‑for‑bit equality around the day‑5 boundary.  
- **Radiation/CRE sanity**: TOA net bias |≤| ~0.2 W m⁻²; CRE SW≈−50, LW≈+30, NET≈−20 W m⁻² (tolerance wide for smoke).  
- **OHC/EEI link**: `ocean/ohc_summary.json.dHdt_Wm2` sensible vs CERES EEI sign.  
- **Sea‑level closure**: altimetry ≈ steric + mass residual trend ≤ 0.3 mm yr⁻¹ (trend check only if timespan permits).  
- **Chemistry diagnostics**: CH₄ lifetime 8–12 years reported; aerosol ERF in assessed range once full Module 10 is on.

All thresholds configurable in `acceptance_gates.yaml` (start loose for v0).

---

## 5) Common pitfalls (fix before re‑running)
- **RF vs ERF mismatch**: Ensure the EBM ingests **ERF** only; unit test exists in Module 12.  
- **Hardcoded LULCC ERF**: Must be replaced by land export time‑series.  
- **Aerosol weakening not wired**: `chem/erf/post2010_weakening_metric.json` missing.  
- **CH₄ lifetime not propagated**: Carbon budget still using a default τ — wire Module 10 value.  
- **Mask/regridding holes**: Any unmapped dest cells must be logged/handled by the mediator.

---

## 6) Quick links (sources & docs)
- **Wiring checklist** (what to close): see `wiring_checklist.md` in repo.  
- **End‑to‑end synthesis plan** (what the test enforces): `synthesis_end_to_end_climate_model_integration_evaluation_plan.md`.
- **Missing pieces — stubs**: `climate_model_missing_pieces_ready_to_paste_stubs_v_0.md`.  
- **Missing items — source links**: `climate_model_missing_items_source_links_v_1.md`.

External data portals (register in `registry/datasets.yaml`):
- CERES EBAF — https://ceres.larc.nasa.gov/data/ebaf/  
- IAP/NOAA OHC — (see IAP portal)  
- NASA/JPL GMSL — https://sealevel.nasa.gov/understanding-sea-level/key-indicators/global-mean-sea-level  
- GRACE Mascons — https://grace.jpl.nasa.gov/data/get-data/jpl_global_mascons/  
- IMBIE — https://imbie.org/  
- AERONET — https://aeronet.gsfc.nasa.gov/  
- MODIS MAIAC AOD — https://lpdaac.usgs.gov/products/mcd19a2v006/

---

## 7) Definition of done (for the first test)
- [ ] CI is green on the smoke (budgets, restart, schemas).  
- [ ] Gate artifacts produced in `artifacts/` with provenance attached.  
- [ ] Four wiring hooks verified by tests.  
- [ ] Brief run log archived (MPI layout, timing, conservation ledger) and linked to the commit SHA.

> Once this passes, the next rung is the **“historical skim”** (2‑year hindcast slices + scorecards via ESMValTool/PMP).

