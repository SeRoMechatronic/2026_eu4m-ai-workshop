"""The public student pack must never carry solutions, keys or broken links."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

import prepare_public_repo
from build_packs import (
    build_instructor_kit,
    build_student_pack,
    check_student_pack,
)
from eu4m_workshop import PART_NAMES, dataframe_sha256
from course_config import DATA_REF, PUBLIC_REPOSITORY
from execute_notebooks import run_notebook


ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA256 = "faa229bd6660f8677c9c5b3e4c76cdea9b2bcc79c2cda8df61d587366a8f81a1"


@pytest.fixture(scope="module")
def student_pack(tmp_path_factory: pytest.TempPathFactory) -> Path:
    return build_student_pack(tmp_path_factory.mktemp("student") / "pack")


def test_student_pack_passes_its_own_safety_check(student_pack: Path) -> None:
    assert check_student_pack(student_pack) == []


def test_student_pack_has_no_instructor_or_challenge_material(student_pack: Path) -> None:
    files = {p.relative_to(student_pack).as_posix() for p in student_pack.rglob("*") if p.is_file()}
    assert not [f for f in files if f.startswith(("instructor/", "slides/", "tests/", "scripts/", "results/"))]
    assert not [f for f in files if "case_" in Path(f).name and Path(f).suffix == ".csv"]
    assert "notebooks/03_actuator_case_solution.ipynb" not in files
    assert {f"data/{name}" for name in PART_NAMES}.issubset(files)


def test_student_pack_readme_links_to_the_public_repository(student_pack: Path) -> None:
    readme = (student_pack / "README.md").read_text(encoding="utf-8")
    assert "@@" not in readme
    assert "colab.research.google.com/github/" in readme


def test_student_notebook_runs_inside_the_pack(student_pack: Path) -> None:
    namespace = run_notebook(student_pack / "notebooks" / "03_actuator_case_student.ipynb", cwd=student_pack)
    assert namespace["source"] == "archivos locales"
    assert dataframe_sha256(namespace["data"]) == BASELINE_SHA256


def test_safety_check_detects_a_leak(tmp_path: Path) -> None:
    pack = build_student_pack(tmp_path / "pack")
    (pack / "instructor").mkdir()
    (pack / "instructor" / "challenge_key.json").write_text("{}", encoding="utf-8")
    (pack / "data" / "case_A.csv").write_text("time_s\n", encoding="utf-8")
    (pack / "docs" / "student_guide.md").write_text("[roto](no_existe.md) 7319051", encoding="utf-8")
    problems = "\n".join(check_student_pack(pack))
    assert "instructor/challenge_key.json" in problems
    assert "case_A.csv" in problems
    assert "enlace roto (no_existe.md)" in problems
    assert "7319051" in problems


def test_instructor_kit_includes_handouts_and_solutions(tmp_path: Path) -> None:
    kit = build_instructor_kit(tmp_path / "kit")
    for name in ("case_A.csv", "case_B.csv", "case_C.csv"):
        assert (kit / "handouts" / name).is_file()
    assert (kit / "instructor" / "challenge_key.json").is_file()
    assert (kit / "notebooks" / "03_actuator_case_solution.ipynb").is_file()
    assert not (kit / ".git").exists()


def test_public_repository_name_is_consistent() -> None:
    """El repositorio público no puede coincidir con el maestro privado."""
    for name in ("CITATION.cff", "docs/colab_setup.md"):
        assert PUBLIC_REPOSITORY in (ROOT / name).read_text(encoding="utf-8"), name
    assert PUBLIC_REPOSITORY.endswith("-student")


def git_output(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def test_prepare_public_repo_makes_a_tagged_clean_repository(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    for variable in ("GIT_AUTHOR", "GIT_COMMITTER"):
        monkeypatch.setenv(f"{variable}_NAME", "Test")
        monkeypatch.setenv(f"{variable}_EMAIL", "test@example.org")
    repo = tmp_path / "public"
    monkeypatch.setattr(sys, "argv", ["prepare_public_repo.py", str(repo)])
    assert prepare_public_repo.main() == 0

    assert git_output(repo, "tag") == DATA_REF
    assert git_output(repo, "rev-list", "--count", "HEAD") == "1"
    tracked = git_output(repo, "ls-files").splitlines()
    assert "notebooks/03_actuator_case_student.ipynb" in tracked
    assert not [f for f in tracked if f.startswith(("instructor/", "slides/", "tests/"))]
    assert f"git push origin {DATA_REF}" in capsys.readouterr().out


def test_prepare_public_repo_refuses_an_existing_folder(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    (tmp_path / "keep.txt").write_text("importante", encoding="utf-8")
    monkeypatch.setattr(sys, "argv", ["prepare_public_repo.py", str(tmp_path)])
    assert prepare_public_repo.main() == 1
    assert (tmp_path / "keep.txt").exists()
