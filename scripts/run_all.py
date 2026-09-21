#!/usr/bin/env python3
"""Rebuild data, notebooks and figures, execute notebooks, and run the tests."""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    print("+", " ".join(args))
    # Permite ejecutar sin instalar el paquete (pip install -e .).
    src = str(ROOT / "src")
    env = {**os.environ, "PYTHONPATH": os.pathsep.join(filter(None, [src, os.environ.get("PYTHONPATH")]))}
    subprocess.run(args, cwd=ROOT, check=True, env=env)


def main() -> None:
    run(sys.executable, "scripts/generate_dataset.py")
    run(sys.executable, "instructor/generate_challenge_cases.py")
    run(sys.executable, "scripts/build_notebooks.py")
    run(sys.executable, "scripts/build_agenda.py")
    # Las figuras versionadas en assets/ se regeneran a mano; aquí solo se comprueba
    # que el script funciona, sin reescribir PNG con otra versión de matplotlib.
    with tempfile.TemporaryDirectory() as figures:
        run(sys.executable, "scripts/make_figures.py", "--out", figures)
    run(sys.executable, "scripts/execute_notebooks.py")
    run(sys.executable, "-m", "pytest", "-q")
    run(sys.executable, "scripts/preflight.py")


if __name__ == "__main__":
    main()
