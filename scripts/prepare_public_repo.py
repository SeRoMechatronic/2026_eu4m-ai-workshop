#!/usr/bin/env python3
"""Prepare the public student repository locally: build, verify, commit and tag.

Nothing is pushed. Create the empty public repository on GitHub first, then run
the commands this script prints. Publishing is deliberately left to a person.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from build_packs import build_student_pack, check_student_pack
from course_config import DATA_REF, PUBLIC_REPOSITORY


def git(*args: str, cwd: Path) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path, help="carpeta NUEVA donde crear el repositorio")
    out = parser.parse_args().out.resolve()
    if out.exists():
        # build_student_pack borra su destino: no permitimos que apunte a algo existente.
        print(f"{out} ya existe. Elija una carpeta que no exista.")
        return 1

    build_student_pack(out)
    problems = check_student_pack(out)
    if problems:
        print("El paquete de estudiantes NO es seguro:")
        print("\n".join(f"  - {problem}" for problem in problems))
        return 1

    git("init", "-b", "main", cwd=out)
    git("add", "-A", cwd=out)
    git("commit", "-m", f"Paquete de estudiantes {DATA_REF}", cwd=out)
    git("tag", DATA_REF, cwd=out)

    print(
        f"""
Repositorio local listo en {out}
(1 commit, etiqueta {DATA_REF}, sin soluciones ni casos del reto).

1. En GitHub, cree el repositorio PÚBLICO y VACÍO: {PUBLIC_REPOSITORY}
   (sin README, sin licencia y sin .gitignore).
2. Publique:

   cd "{out}"
   git remote add origin https://github.com/{PUBLIC_REPOSITORY}.git
   git push -u origin main
   git push origin {DATA_REF}

3. Compruebe la publicación:  python scripts/check_public_urls.py
"""
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
