from __future__ import annotations

import hashlib
import json
import re
import zipfile
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_dataset_matches_reviewed_baseline() -> None:
    assert sha256(ROOT / "data" / "actuator_signals.csv") == (
        "faa229bd6660f8677c9c5b3e4c76cdea9b2bcc79c2cda8df61d587366a8f81a1"
    )


def test_metadata_hashes_match_materials() -> None:
    metadata = json.loads((ROOT / "data" / "metadata.json").read_text())
    paths = {
        "actuator_signals.csv": ROOT / "data" / "actuator_signals.csv",
        "actuator_signals_nominal.csv": ROOT / "data" / "actuator_signals_nominal.csv",
        "actuator_signals_actuator_loss.csv": ROOT / "data" / "actuator_signals_actuator_loss.csv",
        "actuator_signals_sensor_bias.csv": ROOT / "data" / "actuator_signals_sensor_bias.csv",
        "run_features.csv": ROOT / "results" / "run_features.csv",
        "scenario_summary.csv": ROOT / "results" / "scenario_summary.csv",
        "case_A.csv": ROOT / "data" / "case_A.csv",
        "case_B.csv": ROOT / "data" / "case_B.csv",
    }
    assert metadata["sha256"] == {name: sha256(path) for name, path in paths.items()}


def test_repository_parts_reconstruct_combined_dataset() -> None:
    parts = pd.concat(
        [
            pd.read_csv(ROOT / "data" / f"actuator_signals_{scenario}.csv")
            for scenario in ("nominal", "actuator_loss", "sensor_bias")
        ],
        ignore_index=True,
    )
    combined = pd.read_csv(ROOT / "data" / "actuator_signals.csv")
    pd.testing.assert_frame_equal(parts, combined)


def test_challenge_files_do_not_leak_answers() -> None:
    allowed = {
        "time_s",
        "reference_m",
        "position_measured_m",
        "velocity_measured_m_s",
        "force_command_n",
    }
    forbidden = {"scenario", "seed", "position_true_m", "velocity_true_m_s", "force_applied_n"}
    for name in ("case_A.csv", "case_B.csv"):
        columns = set(pd.read_csv(ROOT / "data" / name, nrows=2).columns)
        assert columns == allowed
        assert columns.isdisjoint(forbidden)


def test_student_notebook_does_not_embed_solution() -> None:
    notebook = json.loads((ROOT / "notebooks" / "03_actuator_case_student.ipynb").read_text())
    text = "\n".join("".join(cell.get("source", [])) for cell in notebook["cells"])
    assert '"decision": "PENDIENTE"' in text
    assert '"decision": "aceptar"' not in text
    assert "largest ==" not in text


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
    ]
    assert not [name for name in required if not (ROOT / name).is_file()]


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
            notes = [
                name
                for name in package.namelist()
                if re.fullmatch(r"ppt/notesSlides/notesSlide\d+\.xml", name)
            ]
            assert len(slides) == 12
            assert len(notes) == 12
            minutes: list[int] = []
            for name in notes:
                xml = package.read(name).decode("utf-8")
                text = " ".join(re.findall(r"<a:t>(.*?)</a:t>", xml))
                match = re.search(r"Tiempo: (\d+) min", text)
                assert match, f"Missing timing note in {deck.name}/{name}"
                minutes.append(int(match.group(1)))
            assert sum(minutes) == 120, (deck.name, minutes)


def test_template_headers_are_stable() -> None:
    pvrd = pd.read_csv(ROOT / "templates" / "pvrd_log.csv")
    matrix = pd.read_csv(ROOT / "templates" / "source_matrix.csv")
    assert {"prompt_v1", "acceptance_criterion", "verification_method", "decision"}.issubset(pvrd.columns)
    assert {"doi_or_url", "metadata_verified_at", "evidence_used", "claim_supported"}.issubset(matrix.columns)
