#!/usr/bin/env python3
"""Create exact, source-controlled figures from the teaching dataset."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from eu4m_workshop import load_dataset


ROOT = Path(__file__).resolve().parents[1]
PALETTE = {
    "nominal": "#2A6F97",
    "actuator_loss": "#C14953",
    "sensor_bias": "#E09F3E",
}
LABELS = {
    "nominal": "nominal",
    "actuator_loss": "pérdida_actuador",
    "sensor_bias": "sesgo_sensor",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "assets", help="carpeta de salida")
    out = parser.parse_args().out
    data = load_dataset(ROOT / "data")
    summary = pd.read_csv(ROOT / "results" / "scenario_summary.csv")
    out.mkdir(exist_ok=True)

    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)
    for scenario, color in PALETTE.items():
        run = data[data["run_id"] == f"{scenario}_00"]
        axes[0].plot(run["time_s"], run["position_measured_m"], color=color, label=LABELS[scenario])
        axes[1].plot(run["time_s"], run["position_true_m"], color=color, label=LABELS[scenario])
        axes[2].plot(run["time_s"], run["force_command_n"], color=color, label=LABELS[scenario])
    reference = data[data["run_id"] == "nominal_00"]
    axes[0].plot(reference["time_s"], reference["reference_m"], "k--", lw=1.4, label="referencia")
    axes[1].plot(reference["time_s"], reference["reference_m"], "k--", lw=1.4, label="referencia")
    axes[0].set_ylabel("Posición medida [m]")
    axes[1].set_ylabel("Posición real [m]")
    axes[2].set_ylabel("Orden de fuerza [N]")
    axes[2].set_xlabel("Tiempo [s]")
    for ax in axes:
        ax.grid(alpha=0.25)
    axes[0].legend(ncol=4, fontsize=8, loc="upper left")
    fig.suptitle("Ejecuciones deterministas representativas")
    fig.tight_layout()
    fig.savefig(out / "representative_runs.png", dpi=180, bbox_inches="tight")
    plt.close(fig)

    metrics = [
        ("tracking_rmse_true_m", "RMSE real de seguimiento [m]"),
        ("mean_sensor_residual_m", "Residual medio del sensor [m]"),
        ("force_command_rms_n", "RMS de la orden [N]"),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.5))
    for ax, (column, title) in zip(axes, metrics):
        values = summary.set_index("scenario").loc[list(PALETTE), column]
        ax.bar([LABELS[x] for x in values.index], values.values, color=[PALETTE[x] for x in values.index])
        ax.set_title(title, fontsize=10)
        ax.tick_params(axis="x", labelrotation=25, labelsize=8)
        ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    fig.savefig(out / "scenario_features.png", dpi=180, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
