#!/usr/bin/env python3
"""Fast environment and material check for instructors and CI."""

from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pandas as pd

from eu4m_workshop import PART_NAMES, dataframe_sha256, file_sha256, load_dataset


ROOT = Path(__file__).resolve().parents[1]


def check(name: str, condition: bool, detail: str = "") -> dict[str, str]:
    return {
        "name": name,
        "status": "PASS" if condition else "FAIL",
        "detail": detail,
    }


def main() -> int:
    checks: list[dict[str, str]] = []
    checks.append(check("Python version", sys.version_info >= (3, 10), sys.version.split()[0]))
    for package in ("numpy", "pandas", "matplotlib", "pytest", "nbformat", "nbclient"):
        try:
            module = importlib.import_module(package)
            checks.append(check(f"Import {package}", True, getattr(module, "__version__", "")))
        except Exception as exc:
            checks.append(check(f"Import {package}", False, str(exc)))

    required = [
        *(ROOT / "data" / name for name in PART_NAMES),
        ROOT / "data" / "metadata.json",
        ROOT / "results" / "run_features.csv",
        ROOT / "notebooks" / "00_access_check.ipynb",
        ROOT / "notebooks" / "03_actuator_case_student.ipynb",
        ROOT / "notebooks" / "03_actuator_case_solution.ipynb",
        ROOT / "templates" / "pvrd_log.csv",
        ROOT / "templates" / "source_matrix.csv",
    ]
    for path in required:
        checks.append(check(f"File {path.relative_to(ROOT)}", path.exists()))

    metadata_path = ROOT / "data" / "metadata.json"
    if all(path.exists() for path in required):
        df = load_dataset(ROOT / "data")
        recorded = json.loads(metadata_path.read_text(encoding="utf-8"))["sha256"]
        checks.extend(
            [
                check("Dataset rows", len(df) == 9600, str(len(df))),
                check("Dataset runs", df["run_id"].nunique() == 24, str(df["run_id"].nunique())),
                check("Dataset classes", set(df["scenario"]) == {"nominal", "actuator_loss", "sensor_bias"}),
                check("Dataset finite", not df.isna().any().any()),
                check("Dataset SHA-256", dataframe_sha256(df) == recorded["combined_dataset"]),
                *(
                    check(f"SHA-256 {name}", file_sha256(ROOT / "data" / name) == recorded[name])
                    for name in PART_NAMES
                ),
            ]
        )

    width = max(len(item["name"]) for item in checks)
    for item in checks:
        suffix = f"  {item['detail']}" if item["detail"] else ""
        print(f"{item['status']:4}  {item['name']:<{width}}{suffix}")
    failed = sum(item["status"] == "FAIL" for item in checks)
    print(json.dumps({"pass": len(checks) - failed, "fail": failed}))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
