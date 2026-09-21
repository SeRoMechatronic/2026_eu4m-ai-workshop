#!/usr/bin/env python3
"""Check that the public student repository serves what the notebooks expect.

Run it after publishing ``dist/student_pack/`` and creating the ``DATA_REF`` tag.
It needs Internet access and exits with status 1 if any check fails.
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

from course_config import DATA_REF, PUBLIC_REPOSITORY
from eu4m_workshop.dataset import PART_NAMES, sha256_bytes


ROOT = Path(__file__).resolve().parents[1]
RAW = f"https://raw.githubusercontent.com/{PUBLIC_REPOSITORY}"
NOTEBOOKS = ("00_access_check.ipynb", "03_actuator_case_student.ipynb")


def fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=20) as response:
        return response.read()


def lf_sha256(payload: bytes) -> str:
    return sha256_bytes(payload.replace(b"\r\n", b"\n"))


def main() -> int:
    recorded = json.loads((ROOT / "data" / "metadata.json").read_text(encoding="utf-8"))["sha256"]
    expected: list[tuple[str, str, str]] = []
    for ref in (DATA_REF, "main"):
        expected.append((f"{ref}/data/metadata.json", f"{RAW}/{ref}/data/metadata.json", lf_sha256((ROOT / "data" / "metadata.json").read_bytes())))
        expected += [(f"{ref}/data/{name}", f"{RAW}/{ref}/data/{name}", recorded[name]) for name in PART_NAMES]
    for name in NOTEBOOKS:
        payload = (ROOT / "notebooks" / name).read_bytes()
        expected.append((f"main/notebooks/{name}", f"{RAW}/main/notebooks/{name}", lf_sha256(payload)))

    failures = 0
    for label, url, sha in expected:
        try:
            status = "PASS" if lf_sha256(fetch(url)) == sha else "FAIL  contenido distinto del local"
        except urllib.error.HTTPError as error:
            status = f"FAIL  HTTP {error.code}"
        except OSError as error:
            status = f"FAIL  {type(error).__name__}: {error}"
        failures += not status.startswith("PASS")
        print(f"{status:<40} {label}")
    print(json.dumps({"repository": PUBLIC_REPOSITORY, "data_ref": DATA_REF, "fail": failures}))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
