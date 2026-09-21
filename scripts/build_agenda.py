#!/usr/bin/env python3
"""Regenerate the slide-by-slide agenda of the instructor guide from the decks.

The speaker notes of ``slides/*.pptx`` are the single source of truth for timing.
``--check`` exits with status 1 when ``docs/instructor_guide.md`` is out of date.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GUIDE = ROOT / "docs" / "instructor_guide.md"
START = "<!-- agenda:start -->"
END = "<!-- agenda:end -->"
MODULES = [
    ("module_1_ai_with_criteria.pptx", "Módulo 1  Usar IA con criterio"),
    ("module_2_academic_research.pptx", "Módulo 2  Investigación y comunicación académica"),
    ("module_3_mechatronics_case.pptx", "Módulo 3  IA en una tarea mecatrónica"),
    ("module_4_integrated_challenge.pptx", "Módulo 4  Reto integrado"),
]
TIMING = re.compile(r"\[Tiempo: (\d+) min\]\s*")


@dataclass(frozen=True)
class Slide:
    number: int
    title: str
    minutes: int
    action: str
    note: str


def _texts(xml: str) -> list[str]:
    paragraphs = re.findall(r"<a:p[ >].*?</a:p>", xml, flags=re.S)
    joined = ("".join(re.findall(r"<a:t>(.*?)</a:t>", p, flags=re.S)) for p in paragraphs)
    return [html.unescape(t).strip() for t in joined if t.strip()]


def read_deck(deck: Path) -> list[Slide]:
    slides: list[Slide] = []
    with zipfile.ZipFile(deck) as package:
        count = len([n for n in package.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)])
        for number in range(1, count + 1):
            texts = _texts(package.read(f"ppt/slides/slide{number}.xml").decode("utf-8"))
            note = " ".join(_texts(package.read(f"ppt/notesSlides/notesSlide{number}.xml").decode("utf-8")))
            timing = TIMING.match(note)
            if not timing:
                raise ValueError(f"{deck.name}: la diapositiva {number} no tiene «[Tiempo: N min]»")
            # La portada empieza con el número del módulo; el resto, con la etiqueta del módulo.
            title = texts[2] if re.fullmatch(r"\d{2}", texts[0]) else texts[1]
            note = TIMING.sub("", note, count=1)
            action = re.split(r"(?<!et al\.)(?<=[.!?])\s", note, maxsplit=1)[0]
            slides.append(Slide(number, title, int(timing.group(1)), action, note))
    return slides


def _cell(text: str) -> str:
    return text.replace("|", "/").replace("\n", " ")


def render() -> str:
    parts: list[str] = []
    for filename, heading in MODULES:
        slides = read_deck(ROOT / "slides" / filename)
        total = sum(s.minutes for s in slides)
        parts += [f"### {heading}  ({total} min)", "", "| Minutos | Diapositiva | Contenido | Acción docente |", "|---:|---:|---|---|"]
        elapsed = 0
        for slide in slides:
            parts.append(
                f"| {elapsed}–{elapsed + slide.minutes} | {slide.number} | "
                f"{_cell(slide.title)} | {_cell(slide.action)} |"
            )
            elapsed += slide.minutes
        parts.append("")
    return "\n".join(parts).rstrip("\n")


def updated_guide(text: str) -> str:
    start, end = text.index(START), text.index(END)
    return f"{text[:start + len(START)]}\n\n{render()}\n\n{text[end:]}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="falla si la guía no está actualizada")
    args = parser.parse_args()
    current = GUIDE.read_text(encoding="utf-8")
    fresh = updated_guide(current)
    if args.check:
        if fresh != current:
            print("docs/instructor_guide.md no coincide con las diapositivas: ejecute scripts/build_agenda.py")
            return 1
        return 0
    GUIDE.write_bytes(fresh.encode("utf-8"))
    print(f"Agenda actualizada en {GUIDE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
