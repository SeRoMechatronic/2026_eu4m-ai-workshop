"""Deterministic teaching case for the EU4M AI workshop."""

from .analysis import build_run_features, build_scenario_summary
from .dataset import (
    PART_NAMES,
    dataframe_sha256,
    file_sha256,
    load_dataset,
    to_canonical_csv,
)
from .simulation import SimulationConfig, simulate_dataset, simulate_run

__all__ = [
    "PART_NAMES",
    "SimulationConfig",
    "simulate_run",
    "simulate_dataset",
    "build_run_features",
    "build_scenario_summary",
    "dataframe_sha256",
    "file_sha256",
    "load_dataset",
    "to_canonical_csv",
]
