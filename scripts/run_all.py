#!/usr/bin/env python3
"""Rebuild data and figures, execute notebooks, and run the test suite."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(*args: str) -> None:
    print("+", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> None:
    run(sys.executable, "scripts/generate_dataset.py")
    run(sys.executable, "scripts/make_figures.py")
    run(sys.executable, "scripts/execute_notebooks.py")
    run(sys.executable, "-m", "pytest", "-q")
    run(sys.executable, "scripts/preflight.py")


if __name__ == "__main__":
    main()

