# End-to-End Climate Model Scaffold

![CI](https://github.com/your-org/end-to-end-climate-model/actions/workflows/ci.yml/badge.svg)

This repository bootstraps an end-to-end (E2E) climate model pipeline. The goal for
version 0.5 is to lock down naming conventions, provision the Python package, pin the
toolchain, and deliver the first CI-enforced artifacts that future modules must
respect.

## Package layout

```
climate_e2e/           Core Python package (currently the simple EBM utilities)
artifacts/             Version-controlled CI gate inputs
land/                  Land-use change ERF handshake into the forcing module
chem/erf/              Post-2010 aerosol weakening metric for Module 1
coupler/               Field registry and conservation ledger contract
registry/              External dataset catalog
shared/                Cross-module constants
```

## Getting started

1. Install the pinned toolchain:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .[dev]
   pre-commit install
   ```
2. Run the acceptance gates locally:
   ```bash
   pytest
   ```
3. Ensure formatting and linting stay clean:
   ```bash
   pre-commit run --all-files
   ```

## Artifact wiring contracts

| Artifact | Schema | Key fields | Units |
| --- | --- | --- | --- |
| `artifacts/chem/diagnostics.json` | `docs/artifact_schemas/chem_diagnostics.schema.json` | `industrial_era_ERF_total`, `ch4_lifetime_years`, `forcing_convention` | W·m⁻², years, text |
| `chem/erf/post2010_weakening_metric.json` | _contract file_ | `weakening_percent_since_2010` | % |
| `land/erf_lulcc_timeseries.csv` | _contract file_ | `erf_wm2` | W·m⁻² |
| `artifacts/ocean/ohc_summary.json` | `docs/artifact_schemas/ocean_ohc_summary.schema.json` | `dHdt_Wm2` | W·m⁻² |
| `artifacts/sealevel/closure.json` | `docs/artifact_schemas/sealevel_closure.schema.json` | `residual_trend_mm_per_yr` | mm·yr⁻¹ |
| `artifacts/carbon/budget_summary.json` | `docs/artifact_schemas/carbon_budget_summary.schema.json` | `residual_GtCO2_per_yr_decadal`, `airborne_fraction_multidecadal` | Gt·CO₂·yr⁻¹, fraction |
| `artifacts/carbon/diagnostics.json` | _contract file_ | `assumed_ch4_lifetime_years` | years |
| `artifacts/coupler/conservation_ledger.json` | `docs/artifact_schemas/coupler_conservation_ledger.schema.json` | `global_energy_leak_Wm2`, `global_water_leak_kgm2s` | W·m⁻², kg·m⁻²·s⁻¹ |
| `artifacts/ebm/posteriors_and_fit.json` | `docs/artifact_schemas/ebm_posteriors_and_fit.schema.json` | `ECS_median`, `TCR_median`, `EEI_2005_2020_mean_Wm2` | K, K, W·m⁻² |

All placeholder values are physically plausible and aligned with IPCC AR6 ranges.
Future modules can swap in dynamically generated outputs so long as they continue to
validate against the same schemas.

## Acceptance gates

The CI checks in `tests/test_acceptance_gates.py` and
`tests/test_artifact_schemas.py` load `acceptance_gates.yaml`, the JSON Schemas,
and the artifacts listed above to guarantee:

- Aerosol ERF remains within the historical AR6 likely range (−2.0 to −0.6 W·m⁻²)
  and is explicitly tagged as ERF (never raw RF).
- The planetary energy imbalance (EEI) matches the ocean heat content trend within
  0.2 W·m⁻² and retains the correct sign.
- The global sea-level budget closes to within 0.3 mm·yr⁻¹.
- Carbon budget sanity checks keep the residual within 0.3 GtCO₂·yr⁻¹ and
  airborne fraction within AR6 likely bounds.
- JSON artifacts pass schema validation before the regression gates run.

## Cross-module hooks wired in v0.5

- **Land → Forcings:** `land/erf_lulcc_timeseries.csv` drives the land-use ERF
  component consumed by Module 1 and guards against hard-coded values.
- **Chemistry → Forcings:** `chem/erf/post2010_weakening_metric.json` surfaces
  the post-2010 aerosol weakening diagnostic required by Module 1 gates.
- **Chemistry ↔ Carbon:** `artifacts/carbon/diagnostics.json` echoes the
  `ch4_lifetime_years` assumption from chemistry for methane budget coherence.
- **Ocean ↔ EBM:** The EBM regression tests ingest the schema-validated ocean
  heat uptake and steric sea-level trends to enforce the EEI ≈ ΔOHC gate.

Failing any of these checks blocks merging to `main`, ensuring that upstream model
changes cannot silently violate top-level constraints.

## Wiring checklist

- [x] Package initialized as `climate_e2e` with semantic versioning in `__init__.py`.
- [x] Toolchain pinned via `pyproject.toml` and `.pre-commit-config.yaml`.
- [x] Shared constants and dataset registry documented.
- [x] Minimal artifacts and schemas synchronized.
- [x] CI workflow (`.github/workflows/ci.yml`) runs linting and gates.

## Next steps once CI is green

1. Replace placeholder artifacts with outputs generated from each module pipeline.
2. Tighten acceptance gate tolerances as diagnostics mature.
3. Add automated data pulls (Makefile or `tasks.py`) plus provenance notebooks for
   reproducibility.
