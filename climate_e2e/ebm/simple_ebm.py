"""Simple two-layer energy balance model utilities."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np


@dataclass
class TwoLayerEBMConfig:
    """Configuration for the two-layer EBM."""

    heat_capacity_upper: float = 2.1e8  # J m^-2 K^-1 (~50 m mixed layer)
    heat_capacity_deep: float = 3.0e9  # J m^-2 K^-1 (~700 m equivalent)
    lambda_mag: float = 1.05  # W m^-2 K^-1 (positive magnitude)
    ocean_heat_uptake_efficiency: float = 0.65  # W m^-2 K^-1


@dataclass
class EBMDiagnostics:
    """Outputs from a two-layer EBM integration."""

    surface_temperature: np.ndarray
    deep_temperature: np.ndarray
    eei: np.ndarray
    lambda_mag: float

    def equilibrium_climate_sensitivity(self, forcing_2xco2: float = 3.93) -> float:
        """Return the ECS implied by the configured feedback magnitude."""

        return forcing_2xco2 / self.lambda_mag


SECONDS_PER_YEAR = 31557600.0


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

    cfg = config or TwoLayerEBMConfig()
    forcing = np.asarray(list(forcing), dtype=float)
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
        lambda_mag=lambda_eff,
    )


def estimate_thermal_response(
    forcing: Iterable[float],
    gmst_observations: Iterable[float],
    config: TwoLayerEBMConfig | None = None,
) -> tuple[float, float]:
    """Estimate ECS and TCR given forcing and GMST observations.

    The method integrates the supplied forcing, returning the ECS implied by the
    configured feedback magnitude. For the transient climate response it inspects the
    forcing series: if it resembles a 1 % yr⁻¹ CO₂ experiment the 70th-year response is
    returned; otherwise, a synthetic 1 % yr⁻¹ experiment is generated using the same
    EBM configuration to provide a comparable TCR metric.
    """

    forcing_array = np.asarray(list(forcing), dtype=float)
    cfg = config or TwoLayerEBMConfig()
    diagnostics = integrate_two_layer_ebm(forcing_array, config=cfg)
    surface = diagnostics.surface_temperature
    obs = np.asarray(list(gmst_observations), dtype=float)
    if obs.size != surface.size:
        raise ValueError("Forcing and observation series must have the same length.")

    ecs = diagnostics.equilibrium_climate_sensitivity()
    if _looks_like_onepct_forcing(forcing_array):
        tcr_index = min(69, surface.size - 1)
        tcr = surface[tcr_index]
    else:
        synthetic_forcing = _make_onepct_erf_series(n_years=70)
        synthetic_diag = integrate_two_layer_ebm(synthetic_forcing, config=cfg)
        tcr = synthetic_diag.surface_temperature[69]
    return ecs, tcr


def _looks_like_onepct_forcing(forcing: np.ndarray, forcing_2xco2: float = 3.93) -> bool:
    """Heuristic to detect 1 % yr⁻¹ CO₂ ERF experiments."""

    if forcing.size < 70 or not np.all(np.isfinite(forcing)):
        return False
    if np.any(np.diff(forcing) < -1e-6):
        return False
    if abs(forcing[0]) > 0.05:
        return False
    expected = forcing[min(69, forcing.size - 1)]
    return 0.7 * forcing_2xco2 <= expected <= 1.3 * forcing_2xco2


def _make_onepct_erf_series(n_years: int = 70, forcing_2xco2: float = 3.93) -> np.ndarray:
    """Generate an ERF time series for a 1 % yr⁻¹ CO₂ experiment."""

    years = np.arange(n_years, dtype=float)
    concentration_ratio = 1.01 ** years
    return forcing_2xco2 * np.log(concentration_ratio) / np.log(2.0)


__all__ = [
    "TwoLayerEBMConfig",
    "EBMDiagnostics",
    "integrate_two_layer_ebm",
    "estimate_thermal_response",
]
