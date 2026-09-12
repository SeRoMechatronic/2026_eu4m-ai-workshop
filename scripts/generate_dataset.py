#!/usr/bin/env python3
"""Generate deterministic workshop data and reference summaries."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from eu4m_workshop import (
    SimulationConfig,
    build_run_features,
    build_scenario_summary,
    simulate_dataset,
)


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    data_dir = ROOT / "data"
    results_dir = ROOT / "results"
    data_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    cfg = SimulationConfig()
    dataset = simulate_dataset(cfg)
    features = build_run_features(dataset)
    summary = build_scenario_summary(features)

    dataset_path = data_dir / "actuator_signals.csv"
    features_path = results_dir / "run_features.csv"
    summary_path = results_dir / "scenario_summary.csv"
    dataset.to_csv(dataset_path, index=False, float_format="%.8f")
    part_paths: dict[str, Path] = {}
    for scenario in ("nominal", "actuator_loss", "sensor_bias"):
        part_path = data_dir / f"actuator_signals_{scenario}.csv"
        dataset.loc[dataset["scenario"] == scenario].to_csv(
            part_path, index=False, float_format="%.8f"
        )
        part_paths[part_path.name] = part_path
    features.to_csv(features_path, index=False, float_format="%.8f")
    summary.to_csv(summary_path, index=False, float_format="%.8f")

    operational_columns = [
        "time_s",
        "reference_m",
        "position_measured_m",
        "velocity_measured_m_s",
        "force_command_n",
    ]
    challenge_map = {
        "case_A": "actuator_loss_07",
        "case_B": "sensor_bias_07",
    }
    for case_name, source_run in challenge_map.items():
        challenge = dataset.loc[dataset["run_id"] == source_run, operational_columns]
        challenge.to_csv(
            data_dir / f"{case_name}.csv", index=False, float_format="%.8f"
        )
    instructor_dir = ROOT / "instructor"
    instructor_dir.mkdir(exist_ok=True)
    (instructor_dir / "challenge_key.json").write_text(
        json.dumps(
            {
                "warning": "Do not distribute before the assessed activity.",
                "mapping": challenge_map,
                "important_limit": (
                    "The operational files do not contain independent ground truth. "
                    "A student must not claim a definitive diagnosis from them alone."
                ),
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    metadata = {
        "purpose": "Synthetic teaching data; not an industrially validated actuator model.",
        "model": "PD-controlled point mass with viscous damping",
        "scenarios": ["nominal", "actuator_loss", "sensor_bias"],
        "rows": int(len(dataset)),
        "runs": int(dataset["run_id"].nunique()),
        "config": cfg.to_dict(),
        "sha256": {
            "actuator_signals.csv": sha256(dataset_path),
            **{name: sha256(path) for name, path in part_paths.items()},
            "run_features.csv": sha256(features_path),
            "scenario_summary.csv": sha256(summary_path),
            "case_A.csv": sha256(data_dir / "case_A.csv"),
            "case_B.csv": sha256(data_dir / "case_B.csv"),
        },
    }
    (data_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
