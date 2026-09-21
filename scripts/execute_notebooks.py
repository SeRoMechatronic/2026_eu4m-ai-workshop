#!/usr/bin/env python3
"""Execute the notebooks without requiring a Jupyter server.

The inline runner is deliberately small: workshop notebooks contain ordinary
Python cells and do not depend on magics. GitHub Actions additionally performs
a real kernel execution, so both the portable fallback and the Jupyter path are
covered.
"""

from __future__ import annotations

import os
from pathlib import Path

import matplotlib
import nbformat


matplotlib.use("Agg")


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_NAMES = (
    "00_access_check.ipynb",
    "03_actuator_case_student.ipynb",
    "03_actuator_case_solution.ipynb",
)


def run_notebook(path: Path, cwd: Path = ROOT) -> dict[str, object]:
    """Run every code cell in ``cwd`` and return the resulting namespace."""
    notebook = nbformat.read(path, as_version=4)
    # ``__main__`` existe en sys.modules; dataclasses lo necesita para resolver
    # anotaciones cuando el código usa ``from __future__ import annotations``.
    namespace: dict[str, object] = {"__name__": "__main__"}
    old_cwd = Path.cwd()
    try:
        os.chdir(cwd)
        for index, cell in enumerate(notebook.cells, start=1):
            if cell.cell_type != "code":
                continue
            try:
                exec(compile(cell.source, f"{path.name}:cell-{index}", "exec"), namespace)
            except Exception as exc:
                raise RuntimeError(f"{path.name}: error in cell {index}") from exc
    finally:
        os.chdir(old_cwd)
    return namespace


def main() -> None:
    for name in NOTEBOOK_NAMES:
        run_notebook(ROOT / "notebooks" / name)
        print(f"PASS {name} (inline)")


if __name__ == "__main__":
    main()
