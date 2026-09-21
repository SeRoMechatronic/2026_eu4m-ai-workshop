"""Reference feature calculations for the actuator teaching case."""

from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "run_id",
    "scenario",
    "time_s",
    "reference_m",
    "position_measured_m",
    "force_command_n",
    "position_true_m",
}


def _validate(df: pd.DataFrame) -> None:
    missing = REQUIRED_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {sorted(missing)}")
    if df.empty:
        raise ValueError("Dataset is empty")
    if df[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Dataset contains missing values")


def build_run_features(
    df: pd.DataFrame,
    ignore_before_s: float = 1.0,
    force_limit_n: float = 12.0,
) -> pd.DataFrame:
    """Calculate one transparent feature row for every simulated run."""
    _validate(df)
    saturation_threshold_n = force_limit_n - 0.001
    records: list[dict[str, float | str]] = []
    for run_id, group in df.groupby("run_id", sort=True):
        g = group.loc[group["time_s"] >= ignore_before_s].copy()
        measured_error = g["reference_m"] - g["position_measured_m"]
        true_error = g["reference_m"] - g["position_true_m"]
        sensor_residual = g["position_measured_m"] - g["position_true_m"]
        records.append(
            {
                "run_id": run_id,
                "scenario": str(g["scenario"].iloc[0]),
                "tracking_rmse_measured_m": float(np.sqrt(np.mean(measured_error**2))),
                "tracking_rmse_true_m": float(np.sqrt(np.mean(true_error**2))),
                "mean_sensor_residual_m": float(sensor_residual.mean()),
                "force_command_rms_n": float(np.sqrt(np.mean(g["force_command_n"] ** 2))),
                "force_saturation_fraction": float(
                    np.mean(np.abs(g["force_command_n"]) >= saturation_threshold_n)
                ),
                "final_true_error_m": float(true_error.iloc[-1]),
            }
        )
    return pd.DataFrame.from_records(records).sort_values("run_id").reset_index(drop=True)


def build_scenario_summary(features: pd.DataFrame) -> pd.DataFrame:
    """Aggregate medians by scenario without inventing statistical claims."""
    numeric = [c for c in features.columns if c not in {"run_id", "scenario"}]
    return features.groupby("scenario", sort=True)[numeric].median().reset_index()

