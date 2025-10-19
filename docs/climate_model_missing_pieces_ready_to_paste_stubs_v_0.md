Here’s a tight list of what’s still missing (or should be made explicit) to make the project turnkey + CI-enforceable—with ready-to-paste stubs. Focus: constants/units, coupler registry, artifact schemas, provenance, CI, and the four cross-module wiring hooks.

# 1) Shared constants & units (single source of truth)
**/shared/constants.yaml**
```yaml
# Canonical constants, units, and switches (single source of truth)
version: 0.1
numerics:
  calendar: "gregorian"
  seconds_per_year: 31557600        # 365.25 d * 86400 s
  earth_area_m2: 5.100656e14
  ocean_area_m2: 3.618e14
  sigma_SB_W_m2_K4: 5.670374419e-8

forcings:
  F2xCO2_RF_Wm2: 3.71               # Myhre RF, classic
  F2xCO2_ERF_Wm2: 3.93              # AR6 ERF best-estimate
  methane_lifetime_prior_years: [8.0, 12.0]
  tropospheric_O3_ERF_2019_Wm2: 0.47 # central anchor for QA only

seawater_teos10:
  use_teos10: true
  rho0_kg_m3: 1027

molecular_weights_g_mol:
  air: 28.97
  CO2: 44.01
  CH4: 16.04
  N2O: 44.01

sign_conventions:
  upward_radiative_flux_positive: true   # TOA/CERES
  ocean_freshwater_positive_down: true   # into ocean
  heat_flux_positive_into_ocean: true

units:
  heat_flux: "W m-2"
  freshwater_flux: "kg m-2 s-1"
  sea_level: "mm"
  tendency_heat_content: "W m-2"
  carbon_flux: "GtCO2 yr-1"
```

# 2) Coupler field registry (make conservation explicit)
**/coupler/field_registry.yaml**
```yaml
version: 0.1
grid_exchange:
  algorithm: "conservative-second-order"
  restart_policy: "bit-for-bit"

bulk_flux:
  algorithm: "COARE3.6"       # single source used both sides
  neutral_adjustment: true
  gustiness: true

fields:
  - name: heat_flux
    units: "W m-2"
    conservative: true
    sign: "into_ocean"
    src: atmosphere
    dst: ocean
    diagnostics: ["global_sum", "per_basin_sum"]
  - name: freshwater_flux
    units: "kg m-2 s-1"
    conservative: true
    sign: "into_ocean"
    src: atmosphere
    dst: ocean
    diagnostics: ["global_sum", "per_basin_sum"]
  - name: shortwave_down
    units: "W m-2"
    conservative: false
    src: atmosphere
    dst: ocean
  - name: runoff
    units: "kg m-2 s-1"
    conservative: true
    src: land
    dst: ocean
    diagnostics: ["per_basin_sum"]
  - name: ice_melt_freshwater
    units: "kg m-2 s-1"
    conservative: true
    src: sea_ice
    dst: ocean

provenance:
  checksum_on_exchange: "sha256"
  ledger_outputs: "coupler/conservation_ledger.json"
```

# 3) Artifact schemas (what the tests expect, formally)
Create a small folder of JSON Schemas so producers/consumers agree.

**/docs/artifact_schemas/chem_diagnostics.schema.json**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "chem/diagnostics.json",
  "type": "object",
  "required": ["industrial_era_ERF_total", "ch4_lifetime_years"],
  "properties": {
    "industrial_era_ERF_total": { "type": "number", "description": "ERF_total for aerosols (1750→2019), W m-2" },
    "ch4_lifetime_years": { "type": "number", "minimum": 5, "maximum": 20 }
  },
  "additionalProperties": true
}
```

**/docs/artifact_schemas/ebm_posteriors_and_fit.schema.json**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ebm/posteriors_and_fit.json",
  "type": "object",
  "required": ["ECS_median", "TCR_median", "EEI_2005_2020_mean_Wm2"],
  "properties": {
    "ECS_median": { "type": "number", "minimum": 0.5, "maximum": 8.0 },
    "TCR_median": { "type": "number", "minimum": 0.3, "maximum": 4.0 },
    "EEI_2005_2020_mean_Wm2": { "type": "number" }
  },
  "additionalProperties": true
}
```

**/docs/artifact_schemas/ocean_ohc_summary.schema.json**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ocean/ohc_summary.json",
  "type": "object",
  "required": ["dHdt_Wm2"],
  "properties": { "dHdt_Wm2": { "type": "number" } }
}
```

**/docs/artifact_schemas/sealevel_closure.schema.json**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "sealevel/closure.json",
  "type": "object",
  "required": ["residual_trend_mm_per_yr"],
  "properties": { "residual_trend_mm_per_yr": { "type": "number" } }
}
```

**/docs/artifact_schemas/atmos_ceres_eval.schema.json**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "atmos/ceres_eval.json",
  "type": "object",
  "required": ["TOA_net_bias_Wm2","CRE_SW_global_Wm2","CRE_LW_global_Wm2","CRE_NET_global_Wm2"],
  "properties": {
    "TOA_net_bias_Wm2": { "type": "number" },
    "CRE_SW_global_Wm2": { "type": "number" },
    "CRE_LW_global_Wm2": { "type": "number" },
    "CRE_NET_global_Wm2": { "type": "number" }
  }
}
```

**/docs/artifact_schemas/carbon_budget_summary.schema.json**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "carbon/budget_summary.json",
  "type": "object",
  "required": ["residual_GtCO2_per_yr_decadal","airborne_fraction_multidecadal"],
  "properties": {
    "residual_GtCO2_per_yr_decadal": { "type": "number" },
    "airborne_fraction_multidecadal": { "type": "number", "minimum": 0, "maximum": 1 }
  }
}
```

**/docs/artifact_schemas/coupler_conservation_ledger.schema.json**
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "coupler/conservation_ledger.json",
  "type": "object",
  "required": ["global_energy_leak_Wm2","global_water_leak_kgm2s"],
  "properties": {
    "global_energy_leak_Wm2": { "type": "array", "items": { "type": "number" } },
    "global_water_leak_kgm2s": { "type": "array", "items": { "type": "number" } }
  }
}
```

> For the single CSV the tests touch, add a tiny schema doc:
**/docs/artifact_schemas/erf_by_agent_annual.csv.md**
```markdown
# forcings/erf_by_agent_annual.csv
Required columns:
- year (int)
- CO2_cum1750 (float, W m-2)
- O3_trop (float, W m-2)
- Aerosols_total (float, W m-2)
- LULCC_albedo (float, W m-2)
- Anthropogenic_total (float, W m-2)
Must include a row for 2019.
```

# 4) Provenance (pin choices that move numbers)
**/docs/provenance_template.yaml**
```yaml
run:
  id: "YYYYMMDD-hhmm"
  model_tag: "v0.5"
forcings:
  datasets:
    solar: "SATIRE-v2 @ version X"
    volcanic: "GISS vYYYYMM"
    ghg: "NOAA GML vX.Y"
    aerosols: "CMIP6-histAER vX"
  ERF_method: "double-call, APRP-check"
chemistry:
  OH_source: "Module10 @ commit <hash>"
  methane_lifetime_years: 9.3
land:
  LULCC_mask: "LUH2 v2h @ YYYY"
  albedo_method: "SNICAR-2 / 2-stream"
sea_level:
  GIA_model: "ICE-6G_D (VM5a)"
  VLM_source: "GPS+GRD-corrected, dataset XYZ"
  steric_method: "TEOS-10"
ocean:
  basins_mask: "WCRP-standard vX"
coupler:
  bulk_flux: "COARE3.6"
  regrid: "conservative-2nd"
constants_file: "shared/constants.yaml@<hash>"
```

# 5) CI: run tests + (optional) JSON Schema checks
**/.github/workflows/ci.yml**
```yaml
name: climate-acceptance-ci
on:
  push: { branches: ["main"] }
  pull_request: {}
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install pytest jsonschema
      - name: Validate artifact schemas (optional)
        run: |
          python - << 'PY'
import json,glob,sys,jsonschema, pathlib
schemas = glob.glob("docs/artifact_schemas/*.schema.json")
# Skip if no artifacts dir yet (CI can still run unit tests)
art = pathlib.Path("artifacts")
if art.exists():
    for s in schemas:
        name = pathlib.Path(s).name.replace(".schema.json","")
        # naive mapping; adapt as needed
        target = {
            "chem_diagnostics": "chem/diagnostics.json",
            "ebm_posteriors_and_fit": "ebm/posteriors_and_fit.json",
            "ocean_ohc_summary": "ocean/ohc_summary.json",
            "sealevel_closure": "sealevel/closure.json",
            "atmos_ceres_eval": "atmos/ceres_eval.json",
            "carbon_budget_summary": "carbon/budget_summary.json",
            "coupler_conservation_ledger": "coupler/conservation_ledger.json"
        }.get(name)
        if not target: continue
        p = art/target
        if not p.exists(): continue
        schema = json.load(open(s))
        doc = json.load(open(p))
        jsonschema.validate(instance=doc, schema=schema)
PY
      - name: Run acceptance tests
        env:
          CLIMATE_RUN_DIR: artifacts
        run: pytest -q
```

# 6) Cross-module wiring contracts (interfaces)
**A. Land → Forcings (LULCC ERF)**  
**/land/EXPORTS.md**
```markdown
# LULCC ERF Export
File: land/erf_lulcc_timeseries.csv
Columns:
- year (int)
- erf (float, W m-2), global-mean effective radiative forcing from LULCC albedo

Consumer: Module 1 (forcings/erf_compute.py) must read this file; no hard-coded LULCC ERF allowed.
```

**B. Chemistry → Forcings (Aerosol weakening nowcast)**  
**/chem/EXPORTS.md**
```markdown
# Aerosol weakening metric
File: chem/erf/post2010_weakening_metric.json
Keys:
- weakening_percent_since_2010 (float, %)
Consumer: Module 1 uses this to update aerosol ERF time series for recent years.
```

**C. Chemistry ↔ Carbon (CH₄ lifetime)**  
**/carbon/CONTRACT.md**
```markdown
Carbon module must ingest methane lifetime (years) from chem/diagnostics.json key: ch4_lifetime_years.
Roundtrip: carbon/diagnostics.json should echo 'assumed_ch4_lifetime_years' for tests.
```

**D. Sea-level/steric → EBM calibration constraint**  
**/ebm/CONTRACT.md**
```markdown
EBM diagnostics should include a steric consistency check using ocean/ohc_summary.json and/or sealevel/closure.json.
```

# 7) Basin freshwater closure configuration
**/hydro/basin_closure_config.yaml**
```yaml
version: 0.1
basins: ["Atlantic","Pacific","Indian","Southern","Arctic","Global"]
inputs:
  P: "atmos/pr.nc"
  E: "atmos/evspsbl.nc"
  R: "land/runoff.nc"
  dS: "ocean/salinity_storage.nc"
masks: "masks/woa_basins.nc"
tolerance_mm_per_yr:
  Global: 15
  Land: 25
  default: 25
```

# 8) Scenario library index
**/scenarios/index.yaml**
```yaml
scenarios:
  - id: "SSP1-1.9"
    source: "CMIP6/SSP"
    notes: "AR6 harmonized"
  - id: "SSP2-4.5"
    source: "CMIP6/SSP"
  - id: "IEA-STEPS-2024"
    source: "IEA"
  - id: "NGFS-NetZero-2024"
    source: "NGFS"
metadata:
  emulator: "FaIR vX / MAGICC vX"
  remaining_budget_method: "AR6-consistent; 67%/50% variants"
```

# 9) Sensitivity panels (stubs)
**/scripts/sensitivity_ecs_aerosol.py**
```python
# Compute ECS posterior under wide vs narrow aerosol ERF priors; emit a small JSON panel
# Inputs: ebm config + aerosol prior settings; Output: ebm/ecs_aerosol_sensitivity.json
```

**/scripts/sensitivity_ch4_lifetime.py**
```python
# Re-run carbon cycle with tau_ch4 ±1 yr; write carbon/ch4_tau_sensitivity.json
```

# 10) Minimal runbook
**/docs/RUNBOOK.md**
```markdown
# Runbook (v0.5)
1. Build & run model (container or HPC), write diagnostics into `artifacts/`.
2. Ensure four wiring exports exist:
   - land/erf_lulcc_timeseries.csv
   - chem/erf/post2010_weakening_metric.json
   - chem/diagnostics.json (with ch4_lifetime_years)
   - sealevel/closure.json (and ocean/ohc_summary.json)
3. Validate schemas (optional), then run:
   ```bash
   export CLIMATE_RUN_DIR=artifacts
   pytest -q
   ```
4. If red, see failing gate, fix module or wiring, re-run.
5. Tag release and publish scorecard + provenance_template.yaml.
```
