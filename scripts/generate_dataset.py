#!/usr/bin/env python3
"""Generate deterministic workshop data and reference summaries.

The dataset is published as one CSV per scenario. Its combined form is never
written to disk: ``metadata.json`` records the hash of the canonical CSV of the
concatenation, which is what the notebooks verify.
"""

from __future__ import annotations

import json
from pathlib import Path

from eu4m_workshop import (
    PART_NAMES,
    SimulationConfig,
    build_run_features,
    build_scenario_summary,
    dataframe_sha256,
    file_sha256,
    simulate_dataset,
    to_canonical_csv,
)


ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("nominal", "actuator_loss", "sensor_bias")


def main() -> None:
    data_dir = ROOT / "data"
    results_dir = ROOT / "results"
    data_dir.mkdir(exist_ok=True)
    results_dir.mkdir(exist_ok=True)

    cfg = SimulationConfig()
    dataset = simulate_dataset(cfg)
    features = build_run_features(dataset)
    summary = build_scenario_summary(features)

    part_paths: dict[str, Path] = {}
    for scenario, name in zip(SCENARIOS, PART_NAMES):
        part_path = data_dir / name
        part_path.write_bytes(to_canonical_csv(dataset.loc[dataset["scenario"] == scenario]))
        part_paths[name] = part_path
    features_path = results_dir / "run_features.csv"
    summary_path = results_dir / "scenario_summary.csv"
    features_path.write_bytes(to_canonical_csv(features))
    summary_path.write_bytes(to_canonical_csv(summary))

    metadata = {
        "purpose": "Synthetic teaching data; not an industrially validated actuator model.",
        "model": "PD-controlled point mass with viscous damping",
        "scenarios": list(SCENARIOS),
        "rows": int(len(dataset)),
        "runs": int(dataset["run_id"].nunique()),
        "config": cfg.to_dict(),
        "hash_convention": (
            "SHA-256 over UTF-8 CSV with LF line endings and floats written with "
            "eight decimals. combined_dataset is the hash of the three parts "
            "concatenated in the order of 'scenarios' under a single header."
        ),
        "sha256": {
            "combined_dataset": dataframe_sha256(dataset),
            **{name: file_sha256(path) for name, path in part_paths.items()},
            "run_features.csv": file_sha256(features_path),
            "scenario_summary.csv": file_sha256(summary_path),
        },
    }
    (data_dir / "metadata.json").write_bytes(
        (json.dumps(metadata, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    )
    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
