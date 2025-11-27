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


def test_integrate_two_layer_ebm_validates_inputs():
    """The integrator should guard against empty or invalid inputs."""

    config = TwoLayerEBMConfig()

    with np.testing.assert_raises(ValueError):
        integrate_two_layer_ebm([], config=config)

    with np.testing.assert_raises(ValueError):
        integrate_two_layer_ebm([1.0], config=config, dt_years=0.0)

    with np.testing.assert_raises(ValueError):
        integrate_two_layer_ebm([1.0], config=config, initial_surface_temp=np.inf)


def test_feedback_parameter_prefers_configuration():
    """Diagnostics should report the configured feedback parameter even with flat forcing."""

    config = TwoLayerEBMConfig(feedback_parameter=1.5)
    diagnostics = integrate_two_layer_ebm([0.0, 0.0, 0.0], config=config)

    assert np.isclose(diagnostics.feedback_parameter, config.lambda_mag)
    assert np.isclose(diagnostics.equilibrium_climate_sensitivity(), 3.93 / config.lambda_mag)


def test_estimate_thermal_response_uses_observations():
    """ECS estimation should fit to the supplied GMST observations."""

    true_config = TwoLayerEBMConfig(feedback_parameter=1.25)
    forcing = np.full(100, 3.0)
    synthetic_obs = integrate_two_layer_ebm(forcing, config=true_config).surface_temperature

    ecs, tcr = estimate_thermal_response(forcing, synthetic_obs)

    assert np.isclose(ecs, 3.93 / true_config.lambda_mag, rtol=0.05)
    assert tcr > 0.0


def test_estimate_thermal_response_synthesizes_onepct_when_missing():
    """If the forcing is not a 1 % path, synthesize one to report TCR."""

    config = TwoLayerEBMConfig()
    forcing = np.full(120, 2.0)
    diagnostics = integrate_two_layer_ebm(forcing, config=config)
    ecs, tcr = estimate_thermal_response(forcing, diagnostics.surface_temperature, config=config)

    synthetic = integrate_two_layer_ebm(_make_onepct_erf_series(), config=config)
    assert np.isclose(tcr, synthetic.surface_temperature[69], rtol=5e-2)
    assert np.isclose(ecs, 3.93 / config.lambda_mag, rtol=5e-2)
