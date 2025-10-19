"""Simple two-layer energy balance model utilities."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import numpy as np


@dataclass
class TwoLayerEBMConfig:
    """Configuration for the two-layer EBM."""

    heat_capacity_upper: float = 4.18e7  # J m^-2 K^-1 (~50 m mixed layer)
    heat_capacity_deep: float = 3.3e8  # J m^-2 K^-1 (~700 m equivalent)
    feedback_parameter: float = 1.05  # W m^-2 K^-1 (positive magnitude)
    ocean_heat_uptake_efficiency: float = 0.65  # W m^-2 K^-1


@dataclass
class EBMDiagnostics:
    """Outputs from a two-layer EBM integration."""

    surface_temperature: np.ndarray
    deep_temperature: np.ndarray
    eei: np.ndarray

    def equilibrium_climate_sensitivity(self, forcing_2xco2: float = 3.93) -> float:
        """Return the ECS implied by the feedback parameter."""

        return forcing_2xco2 / self.feedback_parameter

    @property
    def feedback_parameter(self) -> float:
        """Infer the feedback parameter from the EEI and surface temperature time series."""

        # Avoid divide by zero by using the last non-zero temperature change.
        surface_delta = self.surface_temperature[-1] - self.surface_temperature[0]
        eei_delta = self.eei[-1] - self.eei[0]
        if np.isclose(surface_delta, 0.0):
            return np.nan
        return max(1e-6, abs(eei_delta / surface_delta))


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

    dt_seconds = dt_years * 31557600.0

    lambda_eff = cfg.feedback_parameter
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

    return EBMDiagnostics(surface_temperature=surface_temp, deep_temperature=deep_temp, eei=eei)


def estimate_thermal_response(
    forcing: Iterable[float],
    gmst_observations: Iterable[float],
    config: TwoLayerEBMConfig | None = None,
) -> tuple[float, float]:
    """Estimate ECS and TCR given forcing and GMST observations.

    The implementation is intentionally lightweight: it integrates the EBM using the
    supplied forcing, compares the transient response at the 70th step (approximate
    1% CO₂ per year experiment), and infers ECS from the feedback parameter.
    """

    diagnostics = integrate_two_layer_ebm(forcing, config=config)
    surface = diagnostics.surface_temperature
    obs = np.asarray(list(gmst_observations), dtype=float)
    if obs.size != surface.size:
        raise ValueError("Forcing and observation series must have the same length.")

    ecs = diagnostics.equilibrium_climate_sensitivity()
    tcr_index = min(69, surface.size - 1)
    tcr = surface[tcr_index]
    return ecs, tcr


__all__ = [
    "TwoLayerEBMConfig",
    "EBMDiagnostics",
    "integrate_two_layer_ebm",
    "estimate_thermal_response",
]
