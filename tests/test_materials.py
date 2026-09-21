from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path

import pandas as pd

from build_agenda import GUIDE, updated_guide
from eu4m_workshop import PART_NAMES, dataframe_sha256, file_sha256, load_dataset

ROOT = Path(__file__).resolve().parents[1]
BASELINE_SHA256 = "faa229bd6660f8677c9c5b3e4c76cdea9b2bcc79c2cda8df61d587366a8f81a1"


def read_notebook(name: str) -> dict:
    return json.loads((ROOT / "notebooks" / name).read_text(encoding="utf-8"))


def notebook_text(name: str) -> str:
    notebook = read_notebook(name)
    return "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])


def test_dataset_matches_reviewed_baseline() -> None:
    assert dataframe_sha256(load_dataset(ROOT / "data")) == BASELINE_SHA256


def test_metadata_hashes_match_materials() -> None:
    metadata = json.loads((ROOT / "data" / "metadata.json").read_text(encoding="utf-8"))
    recorded = metadata["sha256"]
    assert recorded["combined_dataset"] == BASELINE_SHA256
    paths = {name: ROOT / "data" / name for name in PART_NAMES}
    paths["run_features.csv"] = ROOT / "results" / "run_features.csv"
    paths["scenario_summary.csv"] = ROOT / "results" / "scenario_summary.csv"
    assert {k: v for k, v in recorded.items() if k != "combined_dataset"} == {
        name: file_sha256(path) for name, path in paths.items()
    }


def test_hashes_do_not_depend_on_line_endings(tmp_path: Path) -> None:
    source = ROOT / "data" / PART_NAMES[0]
    windows_copy = tmp_path / "copy.csv"
    windows_copy.write_bytes(source.read_bytes().replace(b"\n", b"\r\n"))
    assert file_sha256(windows_copy) == file_sha256(source)


def test_tracked_data_files_use_lf() -> None:
    for name in PART_NAMES:
        assert b"\r" not in (ROOT / "data" / name).read_bytes(), name


def test_reserialized_dataset_keeps_the_recorded_hash() -> None:
    """Reading the CSV back and writing it again must not change a single byte."""
    parts = load_dataset(ROOT / "data")
    assert dataframe_sha256(parts) == BASELINE_SHA256


def test_challenge_files_match_key_and_do_not_leak_answers() -> None:
    key = json.loads((ROOT / "instructor" / "challenge_key.json").read_text(encoding="utf-8"))
    allowed = {
        "time_s",
        "reference_m",
        "position_measured_m",
        "velocity_measured_m_s",
        "force_command_n",
    }
    forbidden = {"scenario", "seed", "position_true_m", "velocity_true_m_s", "force_applied_n"}
    labeled = load_dataset(ROOT / "data")
    reference_runs = [
        group["position_measured_m"].to_numpy() for _, group in labeled.groupby("run_id")
    ]
    assert set(key["mapping"]) == {"case_A", "case_B", "case_C"}
    for case in key["mapping"]:
        path = ROOT / "data" / f"{case}.csv"
        assert file_sha256(path) == key["sha256"][path.name]
        frame = pd.read_csv(path)
        assert set(frame.columns) == allowed
        assert set(frame.columns).isdisjoint(forbidden)
        measured = frame["position_measured_m"].to_numpy()
        # Ningún caso puede ser una ejecución del dataset que reciben los estudiantes.
        assert not any(
            len(run) == len(measured) and abs(run - measured).max() < 1e-6
            for run in reference_runs
        ), f"{case} coincide con una ejecución etiquetada del dataset"


def test_student_notebook_does_not_embed_solution() -> None:
    text = notebook_text("03_actuator_case_student.ipynb")
    assert '"decision": "PENDIENTE"' in text
    assert '"decision": "aceptar"' not in text
    assert "largest ==" not in text
    assert "challenge_key" not in text


def test_notebooks_have_no_saved_outputs() -> None:
    for name in (
        "00_access_check.ipynb",
        "03_actuator_case_student.ipynb",
        "03_actuator_case_solution.ipynb",
    ):
        for cell in read_notebook(name)["cells"]:
            if cell["cell_type"] == "code":
                assert cell["outputs"] == [] and cell["execution_count"] is None, name


def test_notebook_embeds_the_reviewed_simulator() -> None:
    source = (ROOT / "src" / "eu4m_workshop" / "simulation.py").read_text(encoding="utf-8").strip()
    for name in ("03_actuator_case_student.ipynb", "03_actuator_case_solution.ipynb"):
        assert source in notebook_text(name), f"{name} no contiene el simulador de referencia"


def test_notebook_expected_hash_matches_metadata() -> None:
    text = notebook_text("03_actuator_case_student.ipynb")
    assert f'EXPECTED_SHA256 = "{BASELINE_SHA256}"' in text


def test_required_teaching_materials_exist() -> None:
    required = [
        "docs/syllabus.md",
        "docs/student_guide.md",
        "docs/instructor_guide.md",
        "docs/tool_policy.md",
        "docs/contingency_plan.md",
        "docs/accessibility.md",
        "docs/references.md",
        "docs/provenance.md",
        "docs/colab_setup.md",
        "docs/Propuesta_final_EU4M_IA_verificada.docx",
        "activities/module_1_claim_audit.md",
        "activities/module_2_source_verification.md",
        "activities/module_3_engineering_case.md",
        "activities/module_4_integrated_challenge.md",
        "templates/pvrd_log.csv",
        "templates/source_matrix.csv",
        "templates/engineering_brief.md",
        "templates/ai_use_declaration.md",
        "instructor/module_1_solution.md",
        "instructor/module_2_solution.md",
        "instructor/module_4_model_brief.md",
        "instructor/rubric.md",
        "instructor/exit_ticket.md",
        "instructor/exit_ticket_solution.md",
        "instructor/prepared_ai_responses.md",
        "instructor/generate_challenge_cases.py",
        "notebooks/00_access_check.ipynb",
        "packs/student_README.md",
    ]
    assert not [name for name in required if not (ROOT / name).is_file()]


def slide_notes(deck: Path) -> list[tuple[int, str]]:
    """Return (slide number, note text) pairs in slide order."""
    with zipfile.ZipFile(deck) as package:
        names = package.namelist()
        numbers = sorted(
            int(m.group(1))
            for name in names
            if (m := re.fullmatch(r"ppt/notesSlides/notesSlide(\d+)\.xml", name))
        )
        return [
            (
                number,
                " ".join(
                    re.findall(
                        r"<a:t>(.*?)</a:t>",
                        package.read(f"ppt/notesSlides/notesSlide{number}.xml").decode("utf-8"),
                    )
                ),
            )
            for number in numbers
        ]


def test_slide_decks_have_twelve_slides_and_120_minutes() -> None:
    decks = sorted((ROOT / "slides").glob("module_*.pptx"))
    assert len(decks) == 4
    for deck in decks:
        with zipfile.ZipFile(deck) as package:
            slides = [
                name
                for name in package.namelist()
                if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)
            ]
        notes = slide_notes(deck)
        assert len(slides) == 12
        assert len(notes) == 12
        minutes: list[int] = []
        for number, text in notes:
            match = re.search(r"Tiempo: (\d+) min", text)
            assert match, f"Missing timing note in {deck.name}/slide {number}"
            minutes.append(int(match.group(1)))
        assert sum(minutes) == 120, (deck.name, minutes)


def test_module_4_slide_timing_follows_the_instructor_guide() -> None:
    """15 min de encuadre, 65 de trabajo, 20 de defensas, 15 de prueba y 5 de cierre."""
    deck = ROOT / "slides" / "module_4_integrated_challenge.pptx"
    minutes = [
        int(re.search(r"Tiempo: (\d+) min", text).group(1)) for _, text in slide_notes(deck)
    ]
    blocks = [sum(minutes[0:4]), sum(minutes[4:8]), minutes[8], minutes[9], sum(minutes[10:12])]
    assert blocks == [15, 65, 20, 15, 5]


def test_template_headers_are_stable() -> None:
    pvrd = pd.read_csv(ROOT / "templates" / "pvrd_log.csv")
    matrix = pd.read_csv(ROOT / "templates" / "source_matrix.csv")
    assert {"prompt_v1", "acceptance_criterion", "verification_method", "decision"}.issubset(pvrd.columns)
    assert {"doi_or_url", "metadata_verified_at", "evidence_used", "claim_supported"}.issubset(matrix.columns)


def test_instructor_agenda_matches_the_slide_notes() -> None:
    """Si falla, ejecute ``python scripts/build_agenda.py``."""
    current = GUIDE.read_text(encoding="utf-8")
    assert updated_guide(current) == current

