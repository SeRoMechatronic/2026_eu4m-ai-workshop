"""Deterministic teaching case for the EU4M AI workshop."""

from .analysis import build_run_features, build_scenario_summary
from .simulation import SimulationConfig, simulate_dataset, simulate_run

__all__ = [
    "SimulationConfig",
    "simulate_run",
    "simulate_dataset",
    "build_run_features",
    "build_scenario_summary",
]

