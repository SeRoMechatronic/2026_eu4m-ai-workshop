#!/usr/bin/env python3
"""Generate the unlabeled challenge cases for module 4 and the exit ticket.

INSTRUCTOR ONLY. Never copy this file or ``challenge_key.json`` to the student
repository. The cases use a private base seed, so they neither match a run of the
public dataset nor can be regenerated with the public seeds. Changing the seed or
the mapping invalidates the instructor solutions that describe the cases.
"""

from __future__ import annotations

import json
from pathlib import Path

from eu4m_workshop import SimulationConfig, file_sha256, simulate_run, to_canonical_csv


ROOT = Path(__file__).resolve().parents[1]

CHALLENGE_BASE_SEED = 7319051
OPERATIONAL_COLUMNS = [
    "time_s",
    "reference_m",
    "position_measured_m",
    "velocity_measured_m_s",
    "force_command_n",
]
# case_A y case_B: reto por parejas. case_C: prueba individual de salida.
CASES = {
    "case_A": {"scenario": "actuator_loss", "run_index": 0},
    "case_B": {"scenario": "sensor_bias", "run_index": 0},
    "case_C": {"scenario": "sensor_bias", "run_index": 1},
}


def main() -> None:
    cfg = SimulationConfig(base_seed=CHALLENGE_BASE_SEED)
    data_dir = ROOT / "data"
    hashes: dict[str, str] = {}
    for name, spec in CASES.items():
        run = simulate_run(spec["scenario"], spec["run_index"], cfg)
        path = data_dir / f"{name}.csv"
        path.write_bytes(to_canonical_csv(run[OPERATIONAL_COLUMNS]))
        hashes[path.name] = file_sha256(path)

    key = {
        "warning": "Do not distribute before the assessed activity.",
        "challenge_base_seed": CHALLENGE_BASE_SEED,
        "mapping": CASES,
        "sha256": hashes,
        "important_limit": (
            "The operational files do not contain independent ground truth. "
            "A student must not claim a definitive diagnosis from them alone."
        ),
    }
    (ROOT / "instructor" / "challenge_key.json").write_bytes(
        (json.dumps(key, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    )
    print(json.dumps(key, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
