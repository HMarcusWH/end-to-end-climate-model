"""Acceptance gate regression tests for the E2E scaffold."""

from __future__ import annotations

import csv
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


def test_forcing_metadata_enforces_erf():
    chem = load_json(ROOT / "artifacts" / "chem" / "diagnostics.json")
    assert chem.get("forcing_convention") == "ERF", "Module 12 must ingest ERF, never RF."


def test_carbon_module_echoes_ch4_lifetime():
    chem = load_json(ROOT / "artifacts" / "chem" / "diagnostics.json")
    carbon = load_json(ROOT / "artifacts" / "carbon" / "diagnostics.json")
    assert carbon["assumed_ch4_lifetime_years"] == chem["ch4_lifetime_years"]


def test_carbon_budget_within_gate():
    gates = load_yaml(ROOT / "acceptance_gates.yaml")
    carbon_gates = gates["globals"]["carbon_budget_closure"]
    budget = load_json(ROOT / "artifacts" / "carbon" / "budget_summary.json")

    assert (
        abs(budget["residual_GtCO2_per_yr_decadal"]) <= carbon_gates["target_residual_GtCO2_per_yr"]
    )
    lower, upper = carbon_gates["airborne_fraction_range"]
    assert lower <= budget["airborne_fraction_multidecadal"] <= upper


def test_lulcc_erf_timeseries_present_and_reasonable():
    lulcc_path = ROOT / "land" / "erf_lulcc_timeseries.csv"
    assert lulcc_path.exists(), "Land module must export ERF timeseries for Module 1."

    with lulcc_path.open("r", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)

    assert rows, "LULCC ERF timeseries must not be empty."
    for row in rows:
        year = int(row["year"])
        value = float(row["erf_wm2"])
        assert 1850 <= year <= 2025
        assert -0.4 <= value <= 0.0


def test_steric_trend_consistent_with_ocean_heat():
    constants = load_yaml(ROOT / "shared" / "constants.yaml")
    coeff = constants["sea_level"]["steric_coefficient_mm_per_Wm2"]
    ohc = load_json(ROOT / "artifacts" / "ocean" / "ohc_summary.json")
    closure = load_json(ROOT / "artifacts" / "sealevel" / "closure.json")

    expected_steric = ohc["dHdt_Wm2"] * coeff
    assert abs(closure["steric_trend_mm_per_yr"] - expected_steric) <= 0.3
