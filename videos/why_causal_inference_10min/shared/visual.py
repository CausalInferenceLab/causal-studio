"""Visual conventions and narration timing for the Why Causal Inference lesson."""

from functools import cache
from pathlib import Path
from shutil import copyfile
from tempfile import TemporaryDirectory

from manimpango import list_fonts
import numpy as np
from manim import Arrow, Circle, Dot, DOWN, LEFT, Line, MovingCameraScene, SVGMobject, Text, UP, VGroup

from manim_timing import BeatClock
from speech import parse_narration


TOPIC = Path(__file__).resolve().parents[1]
EDITION = TOPIC / "en"
ICONS = TOPIC.parent / "assets" / "tabler-icons" / "icons" / "outline"


BG = "#10151F"
INK = "#F4F1E9"
MUTED = "#A0ACBB"
GRAY = "#8A98AA"
GRID = "#3B4657"
TREATED = "#6AD9C2"
GHOST = "#BBA9F2"
GOLD = "#EFCB74"


@cache
def lesson_font():
    fonts = list_fonts()
    return next((name for name in ("Avenir Next", "DejaVu Sans") if name in fonts), "sans-serif")


def ink(text, size=34, color=INK):
    return Text(text, font=lesson_font(), font_size=size, color=color)


@cache
def _source_icon(name):
    source = ICONS / f"{name}.svg"
    if not source.is_file():
        raise FileNotFoundError(f"Missing {source.name}. Run bash scripts/setup_video_assets.sh --ensure.")
    # Manim writes a normalized SVG next to the input while loading it.
    with TemporaryDirectory(prefix="causal-svg-") as directory:
        local = copyfile(source, Path(directory) / source.name)
        return SVGMobject(local)


def tabler_icon(name):
    return _source_icon(name).copy()


class LessonScene(MovingCameraScene):
    def setup(self):
        super().setup()
        self.camera.background_color = BG

    def clock(self, stem):
        script = EDITION / "narration" / f"{stem}.txt"
        paragraphs = list(parse_narration(script.read_text(encoding="utf-8")))
        estimated = [len(paragraph.split()) / 2.0 for paragraph in paragraphs]
        timings = EDITION / "build" / "audio" / f"{stem}.timings.json"
        return BeatClock(self, timings, estimated)


class ScoreRuler:
    AXIS_Y = -1.83
    UPPER_ROW = 1.20
    LOWER_ROW = 0.04

    def at(self, score, y):
        return np.array([-3.26 + (score - 500) * 0.027, y, 0])

    def axis(self):
        y = self.AXIS_Y
        group = VGroup(Line(self.at(490, y), self.at(820, y), color=GRID, stroke_width=2))
        for score in (500, 600, 700, 800):
            p = self.at(score, y)
            tick = Line(p + 0.07 * UP, p + 0.07 * DOWN, color=GRID, stroke_width=1.6)
            group.add(tick, ink(str(score), 21, MUTED).next_to(tick, DOWN, buff=0.35))
        return group

    def mark(self, score, y, color, hollow=False):
        position = self.at(score, y)
        if hollow:
            return Circle(radius=0.087, color=color, stroke_width=3.2).move_to(position)
        return Dot(position, radius=0.081, color=color)

    def point(self, score, y, color, hollow=False):
        marker = self.mark(score, y, color, hollow)
        label = ink(str(score), 29, color).next_to(marker, UP, buff=0.12)
        return VGroup(marker, label)

    def lane(self, label, y, color=INK):
        return ink(label, 26, color).move_to([-6.10, y, 0], aligned_edge=LEFT)

    def mean(self, score, color, hollow=False):
        marker = self.mark(score, self.AXIS_Y, color, hollow).set_z_index(2)
        label = ink(str(score), 30, color).next_to(marker, DOWN, buff=0.15)
        return VGroup(marker, label)

    def contrast(self, start, end, label=None, color=GOLD, y=-0.93):
        arrow = Arrow(self.at(start, y), self.at(end, y), buff=0.04, color=color, stroke_width=4.2)
        if label is None:
            delta = end - start
            sign = "+" if delta >= 0 else "−"
            label = f"{sign}{abs(delta):g}"
        return VGroup(arrow, ink(label, 49, color).next_to(arrow, UP, buff=0.12))
