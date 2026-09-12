"""Simple closed-loop actuator simulation used by the workshop.

The model is intentionally transparent. It is a teaching case, not a validated
digital twin of a particular industrial actuator.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd


SCENARIOS = {
    "nominal": {"actuator_gain": 1.0, "sensor_bias": 0.0},
    "actuator_loss": {"actuator_gain": 0.58, "sensor_bias": 0.0},
    "sensor_bias": {"actuator_gain": 1.0, "sensor_bias": 0.12},
}


@dataclass(frozen=True)
class SimulationConfig:
    dt_s: float = 0.02
    duration_s: float = 8.0
    mass_kg: float = 1.20
    damping_n_s_m: float = 2.00
    kp_n_m: float = 18.0
    kd_n_s_m: float = 5.0
    force_limit_n: float = 12.0
    position_noise_std_m: float = 0.003
    velocity_noise_std_m_s: float = 0.006
    runs_per_scenario: int = 8
    base_seed: int = 2609

    def to_dict(self) -> dict[str, float | int]:
        return asdict(self)


def reference_position(time_s: np.ndarray) -> np.ndarray:
    """Piecewise-constant reference shared by every run."""
    return np.select(
        [time_s < 1.0, time_s < 3.0, time_s < 5.0],
        [0.0, 0.50, -0.30],
        default=0.80,
    ).astype(float)


def simulate_run(
    scenario: str,
    run_index: int,
    config: SimulationConfig | None = None,
) -> pd.DataFrame:
    """Simulate one run and return logged controller and validation signals."""
    cfg = config or SimulationConfig()
    if scenario not in SCENARIOS:
        raise ValueError(f"Unknown scenario: {scenario}")
    if run_index < 0:
        raise ValueError("run_index must be non-negative")

    params = SCENARIOS[scenario]
    seed = cfg.base_seed + 100 * list(SCENARIOS).index(scenario) + run_index
    rng = np.random.default_rng(seed)

    time_s = np.arange(0.0, cfg.duration_s, cfg.dt_s)
    reference_m = reference_position(time_s)
    n = len(time_s)
    x_true = np.zeros(n)
    v_true = np.zeros(n)
    x_measured = np.zeros(n)
    v_measured = np.zeros(n)
    force_command = np.zeros(n)
    force_applied = np.zeros(n)

    mass = cfg.mass_kg * rng.uniform(0.96, 1.04)
    damping = cfg.damping_n_s_m * rng.uniform(0.94, 1.06)

    for k in range(n - 1):
        x_measured[k] = (
            x_true[k]
            + params["sensor_bias"]
            + rng.normal(0.0, cfg.position_noise_std_m)
        )
        v_measured[k] = v_true[k] + rng.normal(0.0, cfg.velocity_noise_std_m_s)
        raw_command = (
            cfg.kp_n_m * (reference_m[k] - x_measured[k])
            - cfg.kd_n_s_m * v_measured[k]
        )
        force_command[k] = np.clip(raw_command, -cfg.force_limit_n, cfg.force_limit_n)
        force_applied[k] = params["actuator_gain"] * force_command[k]
        acceleration = (force_applied[k] - damping * v_true[k]) / mass
        v_true[k + 1] = v_true[k] + acceleration * cfg.dt_s
        x_true[k + 1] = x_true[k] + v_true[k + 1] * cfg.dt_s

    x_measured[-1] = (
        x_true[-1]
        + params["sensor_bias"]
        + rng.normal(0.0, cfg.position_noise_std_m)
    )
    v_measured[-1] = v_true[-1] + rng.normal(0.0, cfg.velocity_noise_std_m_s)
    force_command[-1] = force_command[-2]
    force_applied[-1] = params["actuator_gain"] * force_command[-1]

    return pd.DataFrame(
        {
            "run_id": f"{scenario}_{run_index:02d}",
            "scenario": scenario,
            "seed": seed,
            "time_s": time_s,
            "reference_m": reference_m,
            "position_measured_m": x_measured,
            "velocity_measured_m_s": v_measured,
            "force_command_n": force_command,
            "position_true_m": x_true,
            "velocity_true_m_s": v_true,
            "force_applied_n": force_applied,
        }
    )


def simulate_dataset(config: SimulationConfig | None = None) -> pd.DataFrame:
    """Generate the complete balanced dataset in a stable row order."""
    cfg = config or SimulationConfig()
    frames = [
        simulate_run(scenario, run_index, cfg)
        for scenario in SCENARIOS
        for run_index in range(cfg.runs_per_scenario)
    ]
    return pd.concat(frames, ignore_index=True)

