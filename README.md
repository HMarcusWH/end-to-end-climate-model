# End-to-End Climate Model Scaffold

This repository bootsraps an end-to-end (E2E) climate model pipeline. It ships a small
but realistic set of artifacts and gates so that future model components can slot in
without breaking top-level physical constraints. Version 0.5 focuses on consistent
naming, package provisioning, toolchain pinning, and CI-enforced artifacts that each
module must honor.

## Project layout and scope

The codebase is intentionally modular to mirror typical Earth system model silos:

- `climate_e2e/` – Python package with reusable utilities. The current public module
  is `climate_e2e.ebm.simple_ebm` (two-layer energy balance model helpers), re-exported
  via `climate_e2e.ebm`.
- `artifacts/` – Version-controlled JSON inputs that act as acceptance-gate fixtures.
- `docs/` – Artifact schemas (`docs/artifact_schemas/`) plus deep-dive notes for the
  16 planned modules.
- `chem/`, `carbon/`, `ocean/`, `land/`, `sealevel/` – Stubs for chemistry,
  biogeochemistry, ocean heat uptake, land surface, and sea-level components whose
  outputs will eventually feed the coupler.
- `coupler/` – Field registry and conservation ledger contract for cross-module energy
  and water closure.
- `shared/` – Cross-module constants and placeholders for shared lookup tables.
- `tests/` – Regression tests (notably acceptance gates) that enforce the repository
  wiring.

## Installation

The scaffold targets Python 3.11+ and relies only on widely available scientific
packages.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
pre-commit install
```

Use the editable install to develop against the package; it exposes all subpackages
via `setuptools.find_packages()`. If you only need runtime dependencies, drop the
`[dev]` extra.

## Quick start: two-layer EBM utilities

The packaged EBM helpers live in `climate_e2e.ebm` and can be imported after
`pip install -e .`:

```python
from climate_e2e.ebm import (
    TwoLayerEBMConfig,
    integrate_two_layer_ebm,
    estimate_thermal_response,
)

forcing = [0.5, 1.0, 1.5]  # W m^-2
a_config = TwoLayerEBMConfig()
diagnostics = integrate_two_layer_ebm(forcing, config=a_config, dt_years=1.0)
print(diagnostics.surface_temperature.tolist())  # annual GMST anomaly path

# Estimate ECS/TCR using the same forcing and synthetic GMST observations
ecs, tcr = estimate_thermal_response(forcing, diagnostics.surface_temperature, config=a_config)
print(round(ecs, 3), round(tcr, 3))
```

Key outputs:

- `EBMDiagnostics.surface_temperature` / `.deep_temperature`: layer temperature
  anomalies (K).
- `EBMDiagnostics.eei`: Earth energy imbalance time series (W m⁻²).
- `EBMDiagnostics.equilibrium_climate_sensitivity()`: ECS implied by the configured or
  best-fit feedback parameter.

## Artifact inventories and schemas

Each artifact pairs with a JSON schema in `docs/artifact_schemas/` to ensure physical
plausibility and stable field names. Current fixtures include:

| Artifact | Schema | Purpose (key fields) |
| --- | --- | --- |
| `artifacts/chem/diagnostics.json` | `docs/artifact_schemas/chem_diagnostics.schema.json` | Aerosol and trace-gas diagnostics (`industrial_era_ERF_total`, `ch4_lifetime_years`). |
| `artifacts/ocean/ohc_summary.json` | `docs/artifact_schemas/ocean_ohc_summary.schema.json` | Ocean heat uptake trends (`dHdt_Wm2`). |
| `artifacts/sealevel/closure.json` | `docs/artifact_schemas/sealevel_closure.schema.json` | Global sea-level budget residuals (`residual_trend_mm_per_yr`). |
| `artifacts/coupler/conservation_ledger.json` | `docs/artifact_schemas/coupler_conservation_ledger.schema.json` | Energy and water leak bookkeeping (`global_energy_leak_Wm2`, `global_water_leak_kgm2s`). |
| `artifacts/ebm/posteriors_and_fit.json` | `docs/artifact_schemas/ebm_posteriors_and_fit.schema.json` | EBM posterior summaries and EEI (`ECS_median`, `TCR_median`, `EEI_2005_2020_mean_Wm2`). |

Validate artifacts after editing by running a quick JSON Schema check:

```bash
python - <<'PY'
import json
from pathlib import Path
from jsonschema import validate

ROOT = Path(__file__).resolve().parents[0]
artifacts = [
    ("artifacts/chem/diagnostics.json", "docs/artifact_schemas/chem_diagnostics.schema.json"),
    ("artifacts/ocean/ohc_summary.json", "docs/artifact_schemas/ocean_ohc_summary.schema.json"),
    ("artifacts/sealevel/closure.json", "docs/artifact_schemas/sealevel_closure.schema.json"),
    ("artifacts/coupler/conservation_ledger.json", "docs/artifact_schemas/coupler_conservation_ledger.schema.json"),
    ("artifacts/ebm/posteriors_and_fit.json", "docs/artifact_schemas/ebm_posteriors_and_fit.schema.json"),
]
for artifact_path, schema_path in artifacts:
    artifact = json.loads(Path(artifact_path).read_text())
    schema = json.loads(Path(schema_path).read_text())
    validate(instance=artifact, schema=schema)
    print(f"validated {artifact_path} against {schema_path}")
PY
```

## Acceptance gates

CI enforces three top-level gates (see `tests/test_acceptance_gates.py` and
`acceptance_gates.yaml`):

1. **Aerosol ERF within AR6 likely range** – `industrial_era_ERF_total` in
   `artifacts/chem/diagnostics.json` must fall inside `[-2.0, -0.6]` W·m⁻² to avoid
   mixing RF/ERF definitions.
2. **EEI aligns with ocean heat uptake** – The EEI decadal mean from
   `artifacts/ebm/posteriors_and_fit.json` must match `dHdt_Wm2` in
   `artifacts/ocean/ohc_summary.json` within ±0.2 W·m⁻² and share the same sign.
3. **Sea-level budget closure** – The `residual_trend_mm_per_yr` in
   `artifacts/sealevel/closure.json` must lie within ±0.3 mm·yr⁻¹.

### Updating gates and artifacts

- Thresholds and metadata live in `acceptance_gates.yaml` (versioned with provenance).
  Adjust only when new science justifies it, and keep comments in sync.
- When regenerating artifacts from module outputs, re-run the JSON Schema validation
  snippet above and then `pytest` to catch coupling or sign mismatches early.
- If a gate fails:
  - Confirm units and ERF vs. RF definitions match the schema descriptions.
  - Check that decadal means are aligned (e.g., EEI 2005–2020) and that observational
    baselines are consistent across modules.
  - Tighten or relax tolerances only after updating `acceptance_gates.yaml` and citing
    the underlying literature in commit messages.

## Testing and quality checks

Run the full test suite (acceptance gates) and formatting hooks before opening a PR:

```bash
pytest
pre-commit run --all-files
```

The repository ships Ruff and Black configurations in `pyproject.toml`; the
pre-commit hooks will apply them automatically.

## Contributing and roadmap

- Start from the deep-dive module docs under `docs/modules/` to understand expected
  inputs/outputs for each silo (atmospheric dynamics, hydrology, carbon cycle, etc.).
- Keep artifacts and schemas paired: update schema fields first, regenerate artifacts
  from the producing module, then refresh tests.
- Extend `climate_e2e` utilities cautiously (avoid hidden state, keep dataclasses
  small, prefer explicit units in variable names).
- Roadmap highlights: replace placeholder artifacts with live outputs, tighten gate
  tolerances as diagnostics mature, and add provenance notebooks or automation (e.g.,
  Makefile/tasks) for reproducibility.

