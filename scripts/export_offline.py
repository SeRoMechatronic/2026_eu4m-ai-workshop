#!/usr/bin/env python3
"""Export the material that works without Internet or a projector adapter.

* Notebooks executed with a real Jupyter kernel and saved as standalone HTML.
* Slides as PDF when PowerPoint is available.
* Speaker notes as plain Markdown, extracted from the decks (PowerPoint cannot export
  notes pages reliably through COM).
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from build_agenda import MODULES, read_deck


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
HTML_NAMES = {
    "00_access_check.ipynb": "00_access_check_ejecutado.html",
    "03_actuator_case_student.ipynb": "03_actuator_case_student_ejecutado.html",
    "03_actuator_case_solution.ipynb": "03_actuator_case_solution_ejecutado.html",
}


def register_current_interpreter(directory: Path) -> str:
    """Register a throwaway kernel that runs with this very interpreter.

    A user-level ``python3`` kernelspec (common on Windows with several Pythons)
    would otherwise shadow the active environment and run the notebooks elsewhere.
    """
    from ipykernel.kernelspec import write_kernel_spec

    write_kernel_spec(directory / "kernels" / "eu4m-export")
    os.environ["JUPYTER_PATH"] = os.pathsep.join(
        filter(None, [str(directory), os.environ.get("JUPYTER_PATH")])
    )
    return "eu4m-export"


def execute_notebook(path: Path, kernel_name: str):
    import nbformat
    from nbclient import NotebookClient

    notebook = nbformat.read(path, as_version=4)
    NotebookClient(
        notebook,
        timeout=180,
        kernel_name=kernel_name,
        resources={"metadata": {"path": str(path.parent)}},
    ).execute()
    return notebook


def export_html(out_dir: Path) -> None:
    """Execute every notebook in ``notebooks/`` and store it as HTML."""
    from nbconvert import HTMLExporter

    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as scratch:
        kernel_name = register_current_interpreter(Path(scratch))
        for name, target in HTML_NAMES.items():
            notebook = execute_notebook(NOTEBOOKS / name, kernel_name)
            body, _ = HTMLExporter().from_notebook_node(notebook)
            (out_dir / target).write_bytes(body.encode("utf-8"))
            print(f"HTML {target}")


def export_notes(out_dir: Path) -> None:
    """Write the speaker notes of every deck as Markdown."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for filename, heading in MODULES:
        lines = [f"# {heading}: notas del orador", ""]
        elapsed = 0
        for slide in read_deck(ROOT / "slides" / filename):
            lines += [
                f"## Diapositiva {slide.number}. {slide.title}",
                f"*Minutos {elapsed}–{elapsed + slide.minutes} ({slide.minutes} min)*",
                "",
                slide.note,
                "",
            ]
            elapsed += slide.minutes
        target = out_dir / f"{Path(filename).stem}_notas.md"
        target.write_bytes("\n".join(lines).encode("utf-8"))
        print(f"NOTAS {target.name}")


def export_pdfs(out_dir: Path) -> None:
    """Export the slides through PowerPoint; skip with a warning when unavailable."""
    powershell = shutil.which("powershell")
    if powershell is None:
        print("AVISO: PowerShell no está disponible; exporte los PDF a mano desde PowerPoint.")
        return
    result = subprocess.run(
        [
            powershell,
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-File",
            str(ROOT / "scripts" / "export_slides_pdf.ps1"),
            "-OutDir",
            str(out_dir),
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print("AVISO: no se pudieron exportar los PDF (¿PowerPoint instalado?). Exporte a mano.")
        print(result.stderr.strip())


def main() -> int:
    out_dir = ROOT / "dist" / "offline"
    export_html(out_dir)
    export_notes(out_dir)
    export_pdfs(out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
