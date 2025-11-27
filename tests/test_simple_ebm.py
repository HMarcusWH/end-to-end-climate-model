"""Unit tests for the simple two-layer EBM utilities."""

from __future__ import annotations

import numpy as np

from climate_e2e.ebm.simple_ebm import (
    SECONDS_PER_YEAR,
    TwoLayerEBMConfig,
    _make_onepct_erf_series,
    estimate_thermal_response,
    integrate_two_layer_ebm,
)


def test_one_box_limit_matches_analytic_solution():
    """With no deep-ocean coupling the model should match a one-box analytic form."""

    config = TwoLayerEBMConfig(ocean_heat_uptake_efficiency=0.0)
    forcing = np.full(200, 3.7)
    diagnostics = integrate_two_layer_ebm(forcing, config=config)

    years = np.arange(forcing.size, dtype=float)
    lambda_mag = config.lambda_mag
    heat_capacity = config.heat_capacity_upper
    analytic = (forcing[0] / lambda_mag) * (
        1.0 - np.exp(-years * SECONDS_PER_YEAR * lambda_mag / heat_capacity)
    )

    assert np.isclose(diagnostics.surface_temperature[-1], forcing[0] / lambda_mag, rtol=5e-3)
    assert np.allclose(diagnostics.surface_temperature[::20], analytic[::20], atol=0.05)
    assert np.isclose(
        diagnostics.eei[-1], forcing[-1] - lambda_mag * diagnostics.surface_temperature[-1], atol=5e-3
    )


def test_estimate_thermal_response_detects_onepct_path():
    """TCR should be taken from a supplied 1 % yr⁻¹ experiment when present."""

    config = TwoLayerEBMConfig()
    forcing = _make_onepct_erf_series(140)
    diagnostics = integrate_two_layer_ebm(forcing, config=config)
    ecs, tcr = estimate_thermal_response(forcing, diagnostics.surface_temperature, config=config)

    assert np.isclose(ecs, 3.93 / config.lambda_mag, rtol=1e-6)
    assert 1.2 <= tcr <= 2.5


def test_estimate_thermal_response_synthesizes_onepct_when_missing():
    """If the forcing is not a 1 % path, synthesize one to report TCR."""

    config = TwoLayerEBMConfig()
    forcing = np.full(120, 2.0)
    diagnostics = integrate_two_layer_ebm(forcing, config=config)
    ecs, tcr = estimate_thermal_response(forcing, diagnostics.surface_temperature, config=config)

    synthetic = integrate_two_layer_ebm(_make_onepct_erf_series(), config=config)
    assert np.isclose(tcr, synthetic.surface_temperature[69], rtol=1e-6)
    assert np.isclose(ecs, 3.93 / config.lambda_mag, rtol=1e-6)
