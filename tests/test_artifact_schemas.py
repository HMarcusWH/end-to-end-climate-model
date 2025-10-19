"""Validate that version-controlled artifacts match their JSON Schemas."""

from __future__ import annotations

import json
from pathlib import Path

from jsonschema import validate

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "docs" / "artifact_schemas"


ARTIFACT_SCHEMA_PAIRS = {
    ROOT / "artifacts" / "chem" / "diagnostics.json": SCHEMA_DIR / "chem_diagnostics.schema.json",
    ROOT / "artifacts" / "ocean" / "ohc_summary.json": SCHEMA_DIR / "ocean_ohc_summary.schema.json",
    ROOT / "artifacts" / "sealevel" / "closure.json": SCHEMA_DIR / "sealevel_closure.schema.json",
    ROOT / "artifacts" / "ebm" / "posteriors_and_fit.json": SCHEMA_DIR / "ebm_posteriors_and_fit.schema.json",
    ROOT / "artifacts" / "coupler" / "conservation_ledger.json": SCHEMA_DIR
    / "coupler_conservation_ledger.schema.json",
    ROOT / "artifacts" / "carbon" / "budget_summary.json": SCHEMA_DIR / "carbon_budget_summary.schema.json",
}


def _load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_artifacts_conform_to_schema():
    for artifact_path, schema_path in ARTIFACT_SCHEMA_PAIRS.items():
        artifact = _load_json(artifact_path)
        schema = _load_json(schema_path)
        validate(instance=artifact, schema=schema)
