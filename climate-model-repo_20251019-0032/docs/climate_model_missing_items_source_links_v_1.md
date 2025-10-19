# Climate Model — Missing Items & Source Links (v1.0)

A single page you can work down from top to bottom. Each missing item lists the *exact* upstream source(s) to pull from. Where helpful, I’ve noted filepaths we expect in-repo and what CI will validate.

---

## A) Registries (single sources of truth)

**1) Field Registry (`coupler/field_registry.yaml`)**  
What: complete list of exchanged fields, names, units, dims, CF `standard_name`, sign conventions, conservation flags, and provenance tags.  
Get standards from:
- CF Standard Name Table: https://cfconventions.org/standard-names.html
- CF Conventions (metadata rules): https://cfconventions.org/
- UDUNITS (units & validation): https://www.unidata.ucar.edu/software/udunits/

**2) Constants Registry (`shared/constants.yaml`)**  
What: physical constants, calendars, spherical geometry constants, Earth radius(s), baseline years, canonical units, sign conventions.  
Use same standards as above (CF + UDUNITS) and pin baseline years (e.g., ERF vs 1750) explicitly.

---

## B) Artifact Schemas (what CI will validate)
Create JSON/YAML schema files under `docs/artifact_schemas/` that define columns, units, dtypes, and required provenance fields (`source_url`, `citation`, `dataset_version`, `processing_history`).

- `chem_diagnostics.schema.json`  
  AER/AOD/AAOD/SSA, CH₄ lifetime, trend metrics.  
  Sources: AERONET, MODIS MAIAC, MISR (links below), NOAA GML CH₄.

- `ebm_posteriors_and_fit.schema.json`  
  Posterior draws for ECS, TCR, heat-uptake, fit diagnostics vs GMST/EEI/OHC.  
  Reference: FaIR/EBM outputs (link below) and CERES/IAP datasets.

- `ocean_ohc_summary.schema.json`  
  Basin/global OHC, MLD, uncertainties, vintages.  
  Source: IAP OHC (Cheng et al.)

- `sealevel_closure.schema.json`  
  GMSL components: steric (from OHC), ocean mass (GRACE), land water, ice mass (IMBIE); closure residual.  
  Sources: NASA/JPL GMSL, GRACE Mascons, IMBIE.

- `atmos_ceres_eval.schema.json`  
  TOA net/all-sky/clear-sky SW/LW, CRE, EEI with uncertainties.  
  Source: CERES EBAF.

- `carbon_budget_summary.schema.json`  
  Anthropogenic emissions, land/ocean sinks, atmospheric growth, residual ~0.  
  Sources: Global Carbon Budget / NOAA GML (CH₄), CEDS for emissions.

- `coupler_conservation_ledger.schema.json`  
  Per-exchange energy/water/tracer budgets and checksums.

- `erf_by_agent_annual.csv.md`  
  Column spec for ERF CSV (agent, year, ERF_Wm2, uncertainty_lo/hi, baseline_year, notes).

---

## C) Provenance + CI glue

**Provenance template**  
- `docs/provenance_template.yaml` — one per artifact, with `inputs`, `code_version`, `dataset_versions`, `license`, `checksum`, `processing_history`.

**CI workflow**  
- `.github/workflows/ci.yml` — smoke run, schema validation, conservation tests, scorecard build, and badges.

---

## D) Cross‑Module Wiring Contracts (short docs)
Place alongside modules:
- `land/EXPORTS.md` — defines LULCC→ERF export (albedo/radiative kernel treatment, units, baseline).
- `chem/EXPORTS.md` — aerosol trend weakening metric post‑2010; required AOD/AAOD/SSA diagnostics; CH₄ lifetime.
- `carbon/CONTRACT.md` — modern carbon budget JSON (columns/units); who consumes it.
- `ebm/CONTRACT.md` — how EBM ingests ERF & steric constraint; outputs posteriors/fit.

---

## E) Configs & Indices
- `hydro/basin_closure_config.yaml` — basin IDs/masks; links to HydroBASINS/HydroATLAS.
- `scenarios/index.yaml` — registry of SSPs and variants with provenance.

**Masks & Hydrology sources**
- HydroBASINS: https://www.hydrosheds.org/products/hydrobasins  
- HydroATLAS: https://www.hydrosheds.org/products/hydroatlas

**Scenario sources**
- IIASA SSP Public Database (official): https://data.ece.iiasa.ac.at/ssp/
- IAMC 1.5°C Scenario Explorer (for cross‑checks): https://data.ece.iiasa.ac.at/iamc-1.5c-explorer/
- Indicators of Global Climate Change (annual update): https://doi.org/10.5194/essd-15-2295-2023 (landing: https://www.globalcarbonproject.org/carbonbudget/)

---

## F) Sensitivity Panels (scripts CI should run)
- `scripts/sensitivity_ecs_aerosol.py` → `artifacts/ebm/ecs_aerosol_sensitivity.json`  
  Bound ECS posteriors under wide vs narrow aerosol priors.
- `scripts/sensitivity_ch4_lifetime.py` → `artifacts/carbon/ch4_tau_sensitivity.json`  
  Run τ_CH4 ±1 yr and report ΔERF/ΔGMST in emulator lane.

---

## G) Runtime Exports Required for Gates (produced by modules)
Place into `artifacts/` during runs; CI will fail if missing/out of schema.
- `land/erf_lulcc_timeseries.csv`
- `chem/erf/post2010_weakening_metric.json`
- `chem/diagnostics.json` (must include `ch4_lifetime_years`)
- `ocean/ohc_summary.json`
- `sealevel/closure.json`

---

## H) Dataset Registry — Pull-List with Links
Create `registry/datasets.yaml` with entries below (name, url, version, license, checksum, notes). These are the canonical upstreams for our artifacts.

### Energy Balance / Forcing
- **IPCC AR6 Ch.7 & SM (ERF definitions/kernels)**: https://www.ipcc.ch/report/ar6/wg1/  
- **CERES EBAF (TOA/EEI)**: https://ceres.larc.nasa.gov/data/ebaf/

### Surface Temperature (GMST/GSAT evaluation)
- **HadCRUT5**: https://www.metoffice.gov.uk/hadobs/hadcrut5/
- **GISTEMP v4**: https://data.giss.nasa.gov/gistemp/
- **Berkeley Earth**: http://berkeleyearth.org/data/

### Ocean Heat Content / Mixed Layer
- **IAP Global OHC (Cheng et al.)**: https://www.nature.com/subjects/ocean-heat-content (overview)  
  (Data portal reference: https://www.ocean.iap.ac.cn/ or author pages)

### Sea Level & Components
- **NASA/JPL GMSL Key Indicator**: https://sealevel.nasa.gov/understanding-sea-level/key-indicators/global-mean-sea-level
- **GRACE/GRACE‑FO Mascons (JPL Tellus)**: https://grace.jpl.nasa.gov/data/get-data/jpl_global_mascons/
- **IMBIE (reconciled ice‑sheet mass balance)**: https://imbie.org/

### Hydrology Closure (P, E, Runoff, ΔS)
- **ERA5 / ERA5‑Land**: https://cds.climate.copernicus.eu/

### Sea Ice
- **NSIDC Sea Ice Index**: https://nsidc.org/data/seaice_index

### Aerosols / Chemistry
- **CEDS Emissions**: https://github.com/JGCRI/CEDS
- **MACv2‑SP (simple plume patterns)**: https://doi.pangaea.de/10.1594/PANGAEA.904242
- **AERONET**: https://aeronet.gsfc.nasa.gov/
- **MODIS MAIAC AOD (MCD19A2)**: https://lpdaac.usgs.gov/products/mcd19a2v006/
- **MISR Aerosol Products**: https://misr.jpl.nasa.gov/getData/access/
- **NOAA GML Methane (global means)**: https://gml.noaa.gov/ccgg/trends_ch4/

### Downscaling / Regionalization
- **NASA NEX‑GDDP‑CMIP6**: https://www.nccs.nasa.gov/services/data-collections/land-based-products/nex-gddp-cmip6
- **scikit‑downscale**: https://github.com/ClimateImpactLab/downscale

### Evaluation Tooling
- **ESMValTool**: https://esmvaltool.org/
- **PCMDI Metrics Package (PMP)**: https://pcmdi.llnl.gov/metrics/
- **FaIR (emulator)**: https://github.com/OxfordMartinSchool/FAIR

### Standards
- **CF Standard Names**: https://cfconventions.org/standard-names.html
- **UDUNITS**: https://www.unidata.ucar.edu/software/udunits/

---

## I) CI Coverage Still To Implement
- Enforce **RF vs ERF** (EBM must ingest **ERF** only; fail if RF given).  
- Publish **uncertainty envelopes** (MC/ensembles) for ERF & EBM outputs.  
- **Coupler B4B + per‑exchange budget** assertions (energy/water/tracers).  
- **Acceptance gates** wired to schemas (EEI/OHC/SLR closure, aerosol ERF within assessed range) + badges.

---

## J) “One‑Sprint” Do‑Next
1) Seed `coupler/field_registry.yaml` from CF + UDUNITS and add a CI check for non‑CF/invalid units.  
2) Stand up `registry/datasets.yaml` with all links above + `version`, `license`, `checksum`.  
3) Add schema stubs for ERF/GMST/OHC/GMSL; include required provenance fields.  
4) Wire ESMValTool/PMP smoke recipes into CI so any new artifact triggers benchmark diffs.

---

## K) Notes on Baselines & Signs (quick pitfalls)
- ERF baseline: **1750** (AR6). Document conversions and store as W m⁻² (not TW).  
- Sea‑level closure residual target: **≤ 0.3 mm yr⁻¹**.  
- Use CF `cell_methods` to clarify temporal means vs. accumulations; enforce via schema.

---

### Working Paths (suggested)
```
shared/constants.yaml
coupler/field_registry.yaml
registry/datasets.yaml
scripts/sensitivity_ecs_aerosol.py
scripts/sensitivity_ch4_lifetime.py
artifacts/
  ebm/ecs_aerosol_sensitivity.json
  carbon/ch4_tau_sensitivity.json
  ocean/ohc_summary.json
  sealevel/closure.json
  land/erf_lulcc_timeseries.csv
  chem/erf/post2010_weakening_metric.json
  chem/diagnostics.json
```

If you want me to preload the `registry/*.yaml` and `docs/artifact_schemas/*.json` scaffolds here, say the word and I’ll paste the ready‑to‑fill templates.