"""Shared palette and helpers for this topic’s scenes."""

import json

from pathlib import Path
from manim import *


ACCENT_COLOR = YELLOW_E
TABLET_COLOR = TEAL_D
LIBRARY_COLOR = GOLD_D
QUESTION_COLOR = MAROON_D
NEUTRAL_COLOR = GREY_B
ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
TOPIC_DIR = Path(__file__).resolve().parents[1]


def load_icon(filename: str, color: str, height: float) -> SVGMobject:
    icon = SVGMobject(str(ASSET_DIR / filename))
    icon.set_stroke(color=color, width=2.6, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def load_scene_timing_durations(scene_basename: str, *, language: str) -> list[float]:
    filename = f"{scene_basename}.timings.json"
    timings = TOPIC_DIR / language / "build" / "audio" / filename
    if not timings.is_file():
        legacy_dir = TOPIC_DIR / "build" / "audio"
        if language == "en":
            legacy_dir /= "en"
        timings = legacy_dir / filename
    if not timings.is_file():
        return []

    payload = json.loads(timings.read_text())
    return [float(chunk["duration"]) for chunk in payload.get("chunks", [])]


def make_tablet_icon(color: str) -> SVGMobject:
    return load_icon("device-tablet.svg", color, 1.45)


def make_library_icon(color: str) -> SVGMobject:
    return load_icon("book.svg", color, 1.45)


def make_budget_icon(color: str = WHITE) -> SVGMobject:
    return load_icon("coin.svg", color, 1.05)


def make_person_icon(color: str = WHITE, height: float = 1.35) -> SVGMobject:
    return load_icon("user.svg", color, height)


def make_badge(icon: Mobject) -> VGroup:
    return VGroup(icon.copy())


def make_academic_outcome_icon(color: str = WHITE) -> VGroup:
    return VGroup(load_icon("school.svg", color, 1.1))


def make_relation_icons(left_icon: str, right_icon: str, color: str) -> VGroup:
    left = load_icon(left_icon, color, 0.9)
    right = load_icon(right_icon, color, 0.9)
    left.move_to(LEFT * 0.9)
    right.move_to(RIGHT * 0.9)
    arrow = Arrow(
        left.get_right(),
        right.get_left(),
        buff=0.12,
        stroke_width=4,
        color=color,
    )
    return VGroup(left, arrow, right)


def make_world_panel(
    treatment_icon: str,
    treatment_label: str,
    outcome_tex: str,
    color: str,
) -> VGroup:
    frame = RoundedRectangle(
        width=3.25,
        height=4.65,
        corner_radius=0.22,
        stroke_color=color,
        stroke_width=2.6,
    )
    treatment = MathTex(treatment_label).scale(0.88).set_color(color)
    treatment.next_to(frame.get_top(), DOWN, buff=0.34)

    person = make_person_icon(color, 1.1)
    person.move_to(frame.get_center() + UP * 0.62)

    icon = load_icon(treatment_icon, color, 0.92)
    icon.next_to(person, DOWN, buff=0.28)

    arrow = Arrow(
        person.get_bottom(),
        icon.get_top(),
        buff=0.12,
        stroke_width=3.2,
        color=color,
    )

    outcome = MathTex(outcome_tex).scale(1.08).set_color(WHITE)
    outcome.next_to(icon, DOWN, buff=0.42)

    school = load_icon("school.svg", WHITE, 0.78)
    school.next_to(outcome, DOWN, buff=0.28)

    return VGroup(frame, treatment, person, arrow, icon, outcome, school)
