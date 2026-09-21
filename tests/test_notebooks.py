"""Behavioural tests of the self-contained notebooks."""

from __future__ import annotations

import shutil
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from eu4m_workshop import PART_NAMES, build_run_features, dataframe_sha256, load_dataset
from execute_notebooks import run_notebook


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = ROOT / "notebooks"
STUDENT = NOTEBOOKS / "03_actuator_case_student.ipynb"
SOLUTION = NOTEBOOKS / "03_actuator_case_solution.ipynb"
ACCESS = NOTEBOOKS / "00_access_check.ipynb"
BASELINE_SHA256 = "faa229bd6660f8677c9c5b3e4c76cdea9b2bcc79c2cda8df61d587366a8f81a1"


class FakeResponse:
    def __init__(self, payload: bytes) -> None:
        self.payload = payload

    def read(self) -> bytes:
        return self.payload

    def close(self) -> None:
        pass

    def __enter__(self) -> "FakeResponse":
        return self

    def __exit__(self, *exc: object) -> bool:
        return False


@pytest.fixture
def no_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def refuse(*args: object, **kwargs: object) -> None:
        raise OSError("network disabled in tests")

    monkeypatch.setattr(urllib.request, "urlopen", refuse)


@pytest.mark.parametrize("notebook", [ACCESS, STUDENT, SOLUTION], ids=lambda p: p.name)
def test_notebooks_execute_from_the_repository(notebook: Path, no_network: None) -> None:
    run_notebook(notebook)


def test_notebook_prefers_local_files(no_network: None) -> None:
    namespace = run_notebook(STUDENT)
    assert namespace["source"] == "archivos locales"
    assert dataframe_sha256(namespace["data"]) == BASELINE_SHA256


def test_notebook_regenerates_data_without_files_or_network(tmp_path: Path, no_network: None) -> None:
    """Capa 3: la sesión no falla aunque no haya archivos ni conexión."""
    namespace = run_notebook(STUDENT, cwd=tmp_path)
    assert namespace["source"] == "simulador integrado"
    assert dataframe_sha256(namespace["data"]) == BASELINE_SHA256
    pd.testing.assert_frame_equal(namespace["data"], load_dataset(ROOT / "data"))


def test_notebook_discards_a_corrupted_local_file(tmp_path: Path, no_network: None) -> None:
    """Un CSV alterado (por ejemplo, guardado desde una hoja de cálculo) se descarta."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    for name in PART_NAMES:
        shutil.copyfile(ROOT / "data" / name, data_dir / name)
    victim = data_dir / PART_NAMES[1]
    victim.write_text(victim.read_text(encoding="utf-8").replace("0.5", "0,5", 1), encoding="utf-8")
    namespace = run_notebook(STUDENT, cwd=tmp_path)
    assert namespace["source"] == "simulador integrado"


def test_notebook_accepts_the_verified_github_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    requested: list[str] = []

    def fake_urlopen(url: str, timeout: float | None = None) -> FakeResponse:
        requested.append(url)
        return FakeResponse((ROOT / "data" / url.rsplit("/", 1)[-1]).read_bytes())

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    namespace = run_notebook(STUDENT, cwd=tmp_path)
    assert str(namespace["source"]).startswith("GitHub")
    assert len(requested) == len(PART_NAMES)
    assert all("/v" in url for url in requested), "los datos deben venir de una etiqueta fija"


def test_notebook_rejects_a_tampered_github_source(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    def fake_urlopen(url: str, timeout: float | None = None) -> FakeResponse:
        payload = (ROOT / "data" / url.rsplit("/", 1)[-1]).read_bytes()
        return FakeResponse(payload.replace(b"0.00000000", b"0.00000001", 1))

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    namespace = run_notebook(STUDENT, cwd=tmp_path)
    assert namespace["source"] == "simulador integrado"


def test_notebook_features_match_the_package(no_network: None) -> None:
    namespace = run_notebook(SOLUTION)
    notebook_features = namespace["features"]
    package_features = build_run_features(namespace["data"])
    shared = [
        "tracking_rmse_measured_m",
        "tracking_rmse_true_m",
        "mean_sensor_residual_m",
        "force_command_rms_n",
        "force_saturation_fraction",
    ]
    assert notebook_features["run_id"].tolist() == package_features["run_id"].tolist()
    np.testing.assert_allclose(
        notebook_features[shared].to_numpy(dtype=float),
        package_features[shared].to_numpy(dtype=float),
        rtol=0,
        atol=1e-12,
    )


def test_access_check_reports_a_missing_network(no_network: None, capsys: pytest.CaptureFixture[str]) -> None:
    run_notebook(ACCESS)
    output = capsys.readouterr().out
    assert "ACCESO_OK" in output
    assert "GitHub: no" in output
    assert "simulador integrado" in output
