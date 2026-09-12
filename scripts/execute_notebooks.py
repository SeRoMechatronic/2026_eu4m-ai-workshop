#!/usr/bin/env python3
"""Execute both notebooks without requiring a Jupyter server.

The inline runner is deliberately small: workshop notebooks contain ordinary
Python cells and do not depend on magics. GitHub Actions additionally performs
a real kernel execution, so both the portable fallback and the Jupyter path are
covered.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib
import nbformat


matplotlib.use("Agg")


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    for name in ("03_actuator_case_student.ipynb", "03_actuator_case_solution.ipynb"):
        path = ROOT / "notebooks" / name
        notebook = nbformat.read(path, as_version=4)
        namespace: dict[str, object] = {"__name__": "__notebook__"}
        old_cwd = Path.cwd()
        try:
            import os

            os.chdir(ROOT)
            for index, cell in enumerate(notebook.cells, start=1):
                if cell.cell_type != "code":
                    continue
                try:
                    exec(compile(cell.source, f"{name}:cell-{index}", "exec"), namespace)
                except Exception as exc:
                    raise RuntimeError(f"{name}: error in cell {index}") from exc
        finally:
            os.chdir(old_cwd)
        print(f"PASS {name} (inline)")


if __name__ == "__main__":
    main()
