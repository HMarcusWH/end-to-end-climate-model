"""Acceptance gate regression tests for the E2E scaffold."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_aerosol_erf_within_gate():
    gates = load_yaml(ROOT / "acceptance_gates.yaml")
    target_min, target_max = gates["globals"]["aerosol_erf_range"]["target_range_wm2"]
    chem = load_json(ROOT / "artifacts" / "chem" / "diagnostics.json")
    industrial_erf = chem["industrial_era_ERF_total"]
    assert (
        target_min <= industrial_erf <= target_max
    ), "Aerosol ERF must remain within the AR6 likely range; note this gate expects ERF, not RF."


def test_eei_matches_ohc_sign_and_magnitude():
    ohc = load_json(ROOT / "artifacts" / "ocean" / "ohc_summary.json")
    ebm = load_json(ROOT / "artifacts" / "ebm" / "posteriors_and_fit.json")

    dHdt = ohc["dHdt_Wm2"]
    eei = ebm["EEI_2005_2020_mean_Wm2"]

    assert dHdt * eei > 0, "EEI sign must agree with ocean heat uptake; ERF≠RF guard triggered."
    assert abs(dHdt - eei) <= 0.2, "EEI and ΔOHC must align within ±0.2 W m⁻²."


def test_sea_level_residual_within_tolerance():
    gates = load_yaml(ROOT / "acceptance_gates.yaml")
    tolerance = gates["globals"]["sea_level_closure"]["target_residual_mm_per_yr"]
    closure = load_json(ROOT / "artifacts" / "sealevel" / "closure.json")
    residual = closure["residual_trend_mm_per_yr"]

    assert abs(residual) <= tolerance, "Sea-level budget residual exceeds closure tolerance."
