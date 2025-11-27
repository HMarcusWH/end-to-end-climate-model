"""Simple two-layer energy balance model utilities."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np

SECONDS_PER_YEAR = 31_557_600.0


@dataclass
class TwoLayerEBMConfig:
    """Configuration for the two-layer EBM."""

    heat_capacity_upper: float = 4.18e7  # J m^-2 K^-1 (~50 m mixed layer)
    heat_capacity_deep: float = 3.3e8  # J m^-2 K^-1 (~700 m equivalent)
    feedback_parameter: float = 1.05  # W m^-2 K^-1 (positive magnitude)
    ocean_heat_uptake_efficiency: float = 0.65  # W m^-2 K^-1

    @property
    def lambda_mag(self) -> float:
        """Return the magnitude of the feedback parameter."""

        return abs(self.feedback_parameter)


@dataclass
class EBMDiagnostics:
    """Outputs from a two-layer EBM integration."""

    surface_temperature: np.ndarray
    deep_temperature: np.ndarray
    eei: np.ndarray
    configured_feedback_parameter: float | None = None

    def equilibrium_climate_sensitivity(self, forcing_2xco2: float = 3.93) -> float:
        """Return the ECS implied by the feedback parameter."""

        return forcing_2xco2 / self.feedback_parameter

    @property
    def feedback_parameter(self) -> float:
        """Return the configured feedback parameter, falling back to a diagnostic estimate."""

        if self.configured_feedback_parameter is not None and np.isfinite(
            self.configured_feedback_parameter
        ):
            return abs(self.configured_feedback_parameter)

        surface_delta = self.surface_temperature[-1] - self.surface_temperature[0]
        eei_delta = self.eei[-1] - self.eei[0]
        if np.isclose(surface_delta, 0.0):
            return np.nan
        estimate = abs(eei_delta / surface_delta)
        return max(1e-6, estimate)


def _validate_initial_conditions(initial_surface_temp: float, initial_deep_temp: float) -> None:
    if not np.isfinite(initial_surface_temp) or not np.isfinite(initial_deep_temp):
        raise ValueError("Initial temperatures must be finite values.")


def _validate_forcing(forcing: np.ndarray) -> None:
    if forcing.size == 0:
        raise ValueError("Forcing series must contain at least one entry.")
    if not np.all(np.isfinite(forcing)):
        raise ValueError("Forcing series must contain only finite values.")


def integrate_two_layer_ebm(
    forcing: Iterable[float],
    config: TwoLayerEBMConfig | None = None,
    dt_years: float = 1.0,
    initial_surface_temp: float = 0.0,
    initial_deep_temp: float = 0.0,
) -> EBMDiagnostics:
    """Integrate a two-layer energy balance model.

    Parameters
    ----------
    forcing:
        Iterable of effective radiative forcing values (W m^-2).
    config:
        Optional :class:`TwoLayerEBMConfig` overriding the default parameters.
    dt_years:
        Timestep in years. A value of 1.0 corresponds to annual forcing.
    initial_surface_temp, initial_deep_temp:
        Initial temperature anomalies for the surface and deep layers in kelvin.

    Returns
    -------
    EBMDiagnostics
        Time series of surface temperature, deep temperature, and Earth's energy imbalance.
    """

    if dt_years <= 0:
        raise ValueError("dt_years must be positive.")

    cfg = config or TwoLayerEBMConfig()
    forcing = np.asarray(list(forcing), dtype=float)
    _validate_forcing(forcing)
    _validate_initial_conditions(initial_surface_temp, initial_deep_temp)

    n_steps = forcing.size
    surface_temp = np.zeros(n_steps, dtype=float)
    deep_temp = np.zeros(n_steps, dtype=float)
    eei = np.zeros(n_steps, dtype=float)

    surface_temp[0] = initial_surface_temp
    deep_temp[0] = initial_deep_temp

    dt_seconds = dt_years * SECONDS_PER_YEAR

    lambda_eff = cfg.lambda_mag
    gamma = cfg.ocean_heat_uptake_efficiency

    for i in range(1, n_steps):
        q = forcing[i - 1]
        delta_surface = (
            (
                q
                - lambda_eff * surface_temp[i - 1]
                - gamma * (surface_temp[i - 1] - deep_temp[i - 1])
            )
            * dt_seconds
            / cfg.heat_capacity_upper
        )
        delta_deep = (
            gamma * (surface_temp[i - 1] - deep_temp[i - 1]) * dt_seconds / cfg.heat_capacity_deep
        )
        surface_temp[i] = surface_temp[i - 1] + delta_surface
        deep_temp[i] = deep_temp[i - 1] + delta_deep
        eei[i - 1] = (
            q - lambda_eff * surface_temp[i - 1] - gamma * (surface_temp[i - 1] - deep_temp[i - 1])
        )

    # Last time step EEI assumes steady forcing of the final entry.
    eei[-1] = (
        forcing[-1] - lambda_eff * surface_temp[-1] - gamma * (surface_temp[-1] - deep_temp[-1])
    )

    return EBMDiagnostics(
        surface_temperature=surface_temp,
        deep_temperature=deep_temp,
        eei=eei,
        configured_feedback_parameter=lambda_eff,
    )


def _make_onepct_erf_series(
    n_years: float = 140.0, forcing_2xco2: float = 3.93, dt_years: float = 1.0
) -> np.ndarray:
    """Generate an ERF path for a 1 % per year CO₂ increase experiment."""

    if dt_years <= 0:
        raise ValueError("dt_years must be positive.")

    years = np.arange(0.0, n_years, dt_years, dtype=float)
    co2_ratio = np.power(1.01, years)
    return (forcing_2xco2 / np.log(2.0)) * np.log(co2_ratio)


def _synthesize_tcr(
    config: TwoLayerEBMConfig, feedback_parameter: float, dt_years: float
) -> float:
    synthetic_cfg = TwoLayerEBMConfig(
        heat_capacity_upper=config.heat_capacity_upper,
        heat_capacity_deep=config.heat_capacity_deep,
        feedback_parameter=feedback_parameter,
        ocean_heat_uptake_efficiency=config.ocean_heat_uptake_efficiency,
    )
    synthetic = integrate_two_layer_ebm(
        _make_onepct_erf_series(dt_years=dt_years), config=synthetic_cfg, dt_years=dt_years
    )
    tcr_index = min(synthetic.surface_temperature.size - 1, int(round(70.0 / dt_years)))
    return synthetic.surface_temperature[tcr_index]


def estimate_thermal_response(
    forcing: Iterable[float],
    gmst_observations: Iterable[float],
    config: TwoLayerEBMConfig | None = None,
    dt_years: float = 1.0,
) -> tuple[float, float]:
    """Estimate ECS and TCR given forcing and GMST observations."""

    if dt_years <= 0:
        raise ValueError("dt_years must be positive.")

    base_config = config or TwoLayerEBMConfig()
    forcing_arr = np.asarray(list(forcing), dtype=float)
    observations = np.asarray(list(gmst_observations), dtype=float)

    _validate_forcing(forcing_arr)
    if observations.size != forcing_arr.size:
        raise ValueError("Forcing and observation series must have the same length.")
    if not np.all(np.isfinite(observations)):
        raise ValueError("Observation series must contain only finite values.")

    lower = max(1e-3, 0.25 * base_config.lambda_mag)
    upper = 4.0 * base_config.lambda_mag
    candidates = np.linspace(lower, upper, num=50)

    best_lambda = None
    best_rmse = np.inf
    best_diag: EBMDiagnostics | None = None

    for lambda_candidate in candidates:
        trial_config = TwoLayerEBMConfig(
            heat_capacity_upper=base_config.heat_capacity_upper,
            heat_capacity_deep=base_config.heat_capacity_deep,
            feedback_parameter=lambda_candidate,
            ocean_heat_uptake_efficiency=base_config.ocean_heat_uptake_efficiency,
        )
        diag = integrate_two_layer_ebm(forcing_arr, config=trial_config, dt_years=dt_years)
        bias = float(np.mean(observations - diag.surface_temperature))
        rmse = float(np.sqrt(np.mean(np.square(diag.surface_temperature + bias - observations))))
        if rmse < best_rmse:
            best_rmse = rmse
            best_lambda = lambda_candidate
            best_diag = diag

    assert best_lambda is not None and best_diag is not None  # for type checkers

    ecs = best_diag.equilibrium_climate_sensitivity()

    onepct_forcing = _make_onepct_erf_series(
        n_years=best_diag.surface_temperature.size * dt_years, dt_years=dt_years
    )
    if np.allclose(forcing_arr, onepct_forcing, rtol=0.05, atol=0.05):
        tcr_index = min(best_diag.surface_temperature.size - 1, int(round(70.0 / dt_years)))
        tcr = best_diag.surface_temperature[tcr_index]
    else:
        tcr = _synthesize_tcr(base_config, best_lambda, dt_years)

    return ecs, tcr


__all__ = [
    "SECONDS_PER_YEAR",
    "TwoLayerEBMConfig",
    "EBMDiagnostics",
    "integrate_two_layer_ebm",
    "_make_onepct_erf_series",
    "estimate_thermal_response",
]
