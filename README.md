# End-to-End Climate Model Scaffold

This repository bootstraps an end-to-end (E2E) climate model pipeline. The goal for
version 0.5 is to lock down naming conventions, provision the Python package, pin the
toolchain, and deliver the first CI-enforced artifacts that future modules must
respect.

## Package layout

```
climate_e2e/           Core Python package (currently the simple EBM utilities)
artifacts/             Version-controlled CI gate inputs
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
| `artifacts/chem/diagnostics.json` | `docs/artifact_schemas/chem_diagnostics.schema.json` | `industrial_era_ERF_total`, `ch4_lifetime_years` | W·m⁻², years |
| `artifacts/ocean/ohc_summary.json` | `docs/artifact_schemas/ocean_ohc_summary.schema.json` | `dHdt_Wm2` | W·m⁻² |
| `artifacts/sealevel/closure.json` | `docs/artifact_schemas/sealevel_closure.schema.json` | `residual_trend_mm_per_yr` | mm·yr⁻¹ |
| `artifacts/coupler/conservation_ledger.json` | `docs/artifact_schemas/coupler_conservation_ledger.schema.json` | `global_energy_leak_Wm2`, `global_water_leak_kgm2s` | W·m⁻², kg·m⁻²·s⁻¹ |
| `artifacts/ebm/posteriors_and_fit.json` | `docs/artifact_schemas/ebm_posteriors_and_fit.schema.json` | `ECS_median`, `TCR_median`, `EEI_2005_2020_mean_Wm2` | K, K, W·m⁻² |

All placeholder values are physically plausible and aligned with IPCC AR6 ranges.
Future modules can swap in dynamically generated outputs so long as they continue to
validate against the same schemas.

## Acceptance gates

The CI checks in `tests/test_acceptance_gates.py` load `acceptance_gates.yaml` and the
artifacts listed above to guarantee:

- Aerosol ERF remains within the historical AR6 likely range (−2.0 to −0.6 W·m⁻²).
- The planetary energy imbalance (EEI) matches the ocean heat content trend within
  0.2 W·m⁻² and retains the correct sign.
- The global sea-level budget closes to within 0.3 mm·yr⁻¹.

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
