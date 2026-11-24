"""Shared palette and helpers for this topic’s scenes."""

import json

from pathlib import Path
from manim import *


TOPIC_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
ACCENT = YELLOW_E
COIN_COLOR = YELLOW_E
TREAT_COLOR = TEAL_C
CONTROL_COLOR = BLUE_C
FORBIDDEN = MAROON_C
CLEAN_WATER = BLUE_C
DIRTY_WATER = MAROON_C
INSTRUMENT = ORANGE
COMPLIER = GREEN
ALWAYS_TAKER = RED_C
NEVER_TAKER = BLUE_E
SOFT = GREY_B


def load_icon(filename: str, color: str = WHITE, height: float = 1.0) -> SVGMobject:
    icon = SVGMobject(str(ASSET_DIR / filename))
    icon.set_stroke(color=color, width=2.6, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def load_scene_timing_durations(scene_basename: str) -> list[float]:
    payload = json.loads(
        (TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json").read_text()
    )
    return [float(chunk["duration"]) for chunk in payload["chunks"]]


def make_forbidden_card(label: str, width: float = 2.6, height: float = 1.6) -> VGroup:
    """금지된 시나리오 카드: 라벨 + 빨간 X 오버레이."""
    frame = RoundedRectangle(
        width=width, height=height,
        corner_radius=0.14,
        stroke_color=FORBIDDEN, stroke_width=2.4,
    )
    text = Text(label, font_size=22, color=WHITE, line_spacing=0.9)
    text.move_to(frame.get_center())
    x1 = Line(frame.get_corner(UL), frame.get_corner(DR), color=FORBIDDEN, stroke_width=4)
    x2 = Line(frame.get_corner(UR), frame.get_corner(DL), color=FORBIDDEN, stroke_width=4)
    return VGroup(frame, text, x1, x2)


def make_school_dot(color: str, radius: float = 0.20) -> Dot:
    return Dot(radius=radius, color=color)


def make_school_row(count: int, color: str, spacing: float = 0.45) -> VGroup:
    dots = VGroup(*[make_school_dot(color) for _ in range(count)])
    dots.arrange(RIGHT, buff=spacing)
    return dots


def make_lock(color: str = WHITE, height: float = 0.9) -> SVGMobject:
    icon = load_icon("lock.svg", color, height)
    return icon


def make_unlock(color: str = WHITE, height: float = 0.9) -> SVGMobject:
    icon = load_icon("lock-open.svg", color, height)
    return icon
