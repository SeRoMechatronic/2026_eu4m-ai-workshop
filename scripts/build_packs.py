#!/usr/bin/env python3
"""Assemble the public student pack and the private instructor kit.

The student pack is built from an explicit allowlist, so a new file never reaches
students by accident. ``check_student_pack`` re-verifies the result: no solution,
key, slide or test may be present, and every relative link must resolve.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import time
from pathlib import Path

from course_config import DATA_REF, PUBLIC_REPOSITORY


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

STUDENT_FILES = [
    ".gitattributes",
    "CITATION.cff",
    "LICENSE",
    "LICENSE-CODE",
    "docs/student_guide.md",
    "docs/syllabus.md",
    "docs/tool_policy.md",
    "docs/accessibility.md",
    "docs/references.md",
    "docs/source_packet.md",
    "activities/module_1_claim_audit.md",
    "activities/module_2_source_verification.md",
    "activities/module_3_engineering_case.md",
    "activities/module_4_integrated_challenge.md",
    "templates/pvrd_log.csv",
    "templates/source_matrix.csv",
    "templates/engineering_brief.md",
    "templates/ai_use_declaration.md",
    "notebooks/00_access_check.ipynb",
    "notebooks/03_actuator_case_student.ipynb",
    "data/actuator_signals_nominal.csv",
    "data/actuator_signals_actuator_loss.csv",
    "data/actuator_signals_sensor_bias.csv",
    "data/metadata.json",
    "src/eu4m_workshop/__init__.py",
    "src/eu4m_workshop/analysis.py",
    "src/eu4m_workshop/dataset.py",
    "src/eu4m_workshop/simulation.py",
]
# Archivos con otro nombre dentro del paquete: origen -> destino.
STUDENT_RENAMES = {
    "packs/student_README.md": "README.md",
    "packs/requirements-student.txt": "requirements.txt",
}

FORBIDDEN_PATH_PARTS = (
    "instructor",
    "solution",
    "challenge_key",
    "prepared_ai",
    "rubric",
    "exit_ticket",
    "grading",
    "slides",
    "tests",
    "scripts",
    ".github",
    "release_checklist",
    "contingency",
    "results",
)
FORBIDDEN_TEXT = ("challenge_key", "7319051", "instructor/")
CASE_FILE = re.compile(r"(^|/)case_[A-Z]\.csv$")

LINK = re.compile(r"\]\(([^)\s#]+)(?:#[^)]*)?\)")
KIT_IGNORE = shutil.ignore_patterns(
    ".git", "dist", ".venv", "__pycache__", ".pytest_cache", ".claude",
    "*.egg-info", ".ipynb_checkpoints",
)


def remove_tree(path: Path, attempts: int = 6) -> None:
    """Delete a folder, retrying: OneDrive and antivirus briefly lock new files on Windows."""
    for attempt in range(attempts):
        try:
            shutil.rmtree(path)
            return
        except PermissionError:
            if attempt == attempts - 1:
                raise
            time.sleep(1.5)


def _fill(text: str) -> str:
    return text.replace("@@REPOSITORY@@", PUBLIC_REPOSITORY).replace("@@DATA_REF@@", DATA_REF)


def build_student_pack(out: Path) -> Path:
    if out.exists():
        remove_tree(out)
    for name in STUDENT_FILES:
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    for source, name in STUDENT_RENAMES.items():
        target = out / name
        target.parent.mkdir(parents=True, exist_ok=True)
        text = (ROOT / source).read_text(encoding="utf-8")
        target.write_bytes(_fill(text).encode("utf-8"))
    return out


def check_student_pack(pack: Path) -> list[str]:
    """Return the problems found; an empty list means the pack is safe to publish."""
    problems: list[str] = []
    for path in sorted(p for p in pack.rglob("*") if p.is_file()):
        relative = path.relative_to(pack).as_posix()
        lowered = relative.lower()
        for part in FORBIDDEN_PATH_PARTS:
            if part in lowered:
                problems.append(f"{relative}: ruta prohibida ({part})")
        if CASE_FILE.search(relative):
            problems.append(f"{relative}: los casos del reto se entregan en clase")
        if path.suffix in {".md", ".json", ".py", ".ipynb", ".txt", ".csv"}:
            text = path.read_text(encoding="utf-8")
            problems.extend(
                f"{relative}: contiene «{token}»" for token in FORBIDDEN_TEXT if token in text
            )
            if path.suffix == ".md":
                for target in LINK.findall(text):
                    if target.startswith(("http://", "https://", "mailto:")):
                        continue
                    if not (path.parent / target).resolve().exists():
                        problems.append(f"{relative}: enlace roto ({target})")
    return problems


def build_instructor_kit(out: Path) -> Path:
    if out.exists():
        remove_tree(out)
    target = out.resolve()

    def ignore(directory: str, names: list[str]) -> set[str]:
        skipped = set(KIT_IGNORE(directory, names))
        # Evita copiarse a sí mismo si la salida está dentro del repositorio.
        skipped |= {name for name in names if (Path(directory) / name).resolve() == target}
        return skipped

    shutil.copytree(ROOT, out, ignore=ignore)
    # El duplicado suelto en la raíz no forma parte del kit.
    for stray in out.glob("*.docx"):
        stray.unlink()
    handouts = out / "handouts"
    handouts.mkdir()
    for name in ("case_A.csv", "case_B.csv", "case_C.csv"):
        shutil.copyfile(ROOT / "data" / name, handouts / name)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--offline", action="store_true", help="añade HTML ejecutado y PDF al kit")
    parser.add_argument("--zip", action="store_true", help="crea los ZIP en la carpeta de salida")
    parser.add_argument(
        "--out",
        type=Path,
        default=DIST,
        help="carpeta de salida (por defecto dist/); fuera de OneDrive evita bloqueos de archivos",
    )
    args = parser.parse_args()
    out = args.out.resolve()

    student = build_student_pack(out / "student_pack")
    problems = check_student_pack(student)
    if problems:
        print("El paquete de estudiantes NO es seguro:")
        print("\n".join(f"  - {problem}" for problem in problems))
        return 1
    kit = build_instructor_kit(out / "instructor_kit")
    print(f"Paquete de estudiantes: {student}")
    print(f"Kit de instructor:      {kit}")

    if args.offline:
        from export_offline import export_html, export_notes, export_pdfs

        export_html(kit / "offline")
        export_notes(kit / "offline")
        export_pdfs(kit / "offline")
    if args.zip:
        student_zip = shutil.make_archive(str(out / student.name), "zip", root_dir=student)
        # El kit lleva su propia copia para compartirla sin GitHub.
        shutil.copyfile(student_zip, kit / "student_pack.zip")
        kit_zip = shutil.make_archive(str(out / kit.name), "zip", root_dir=kit)
        print(f"ZIP: {student_zip}")
        print(f"ZIP: {kit_zip}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
