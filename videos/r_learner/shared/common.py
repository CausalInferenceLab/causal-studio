from inspect import getfile
from pathlib import Path

import numpy as np
from manim import (
    Arrow, Axes, DashedLine, Dot, DOWN, LEFT, Line, MathTex, RIGHT, Scene, Square,
    Text, UP, VGroup,
)
from manimpango import list_fonts
from manim_timing import BeatClock


BACKGROUND = "#000000"
INK = "#FFFFFF"
MUTED = "#AAAAAA"
GUIDE = "#424E56"
TREATMENT = "#FFFF00"
OUTCOME = "#EC92AB"
LARGE_FIT = "#5CD0B3"
SMALL_FIT = "#58C4DD"
FONTS = set(list_fonts())
FONT = next(
    (name for name in ("Apple SD Gothic Neo", "Noto Sans CJK KR", "Noto Sans KR") if name in FONTS),
    "sans-serif",
)
EXAMPLE = (0.25, 4)
LARGE = ((-0.75, -13.2), (-0.75, -12), (-0.75, -10.8), (0.25, 2.8), EXAMPLE, (0.25, 5.2))
SMALL = ((-0.25, -3.2), (-0.25, -2), (-0.25, -0.8), (0.75, 4.8), (0.75, 6), (0.75, 7.2))


def at(x, y):
    return np.array([x, y, 0.0])


def label(string, size=31, color=INK):
    return Text(string, font=FONT, font_size=size, color=color)


def math(*parts, size=48, color=INK):
    return MathTex(*parts, font_size=size, color=color)


def squared_loss(points, slope):
    return sum((y - slope * x) ** 2 for x, y in points)


class ResidualRuler:
    def __init__(self, y, name, expected, actual, difference, color):
        start, end = at(-1.8, y), at(2.65, y)
        self.title = label(name, 36, color).move_to(at(-5.0, y + 0.10), aligned_edge=LEFT)
        self.baseline = Line(at(-2.93, y), at(4.30, y), color=GUIDE, stroke_width=2.1)
        self.expected = self.marker(start, expected, "예상", MUTED, hollow=True)
        self.actual = self.marker(end, actual, "실제", color)
        self.span = Arrow(start, end, buff=0.10, color=color, stroke_width=5, max_tip_length_to_length_ratio=0.065)
        self.amount = math(difference, size=62, color=color).move_to(at((start[0] + end[0]) / 2, y + 0.64))
        self.body = VGroup(self.baseline, self.title, self.expected, self.actual)

    @staticmethod
    def marker(point, value, caption, color, hollow=False):
        dot = Dot(point, radius=0.077, color=color)
        if hollow:
            dot.set_fill(BACKGROUND, opacity=1).set_stroke(color, width=2.5)
        number = math(value, size=47, color=color).next_to(dot, UP, buff=0.20)
        note = label(caption, 25, color).next_to(dot, DOWN, buff=0.16)
        return VGroup(dot, number, note).set_z_index(2)


def outcome_ruler():
    return ResidualRuler(1.0, "주문량", "76", "80", "+4", OUTCOME)


def treatment_ruler():
    return ResidualRuler(-1.46, "쿠폰 지급", "0.75", "1", "+0.25", TREATMENT)


def store_title():
    return label("큰 매장", 36).move_to(at(-5.0, 2.74), aligned_edge=LEFT)


class ResidualPlot:
    def __init__(self):
        self.axes = Axes(
            x_range=[-1, 1, 0.25], y_range=[-16, 12, 4],
            x_length=7.55, y_length=4.82, tips=False,
            axis_config={"color": GUIDE, "stroke_width": 2.15, "include_ticks": False},
        ).move_to(at(-1.80, -0.14))
        guides = VGroup(*(
            Line(self.point(-1, y), self.point(1, y), stroke_width=1.1, color=GUIDE).set_opacity(0.48)
            for y in (-12, -6, 6, 12)
        ))
        x_axis_label = label("지급 잔차", 28, TREATMENT).next_to(self.axes.x_axis.get_end(), DOWN, buff=0.18)
        y_axis_label = label("주문 잔차", 28, OUTCOME).next_to(self.axes.y_axis.get_end(), UP, buff=0.16)
        zero = math("0", size=28, color=MUTED).next_to(self.point(0, 0), DOWN + LEFT, buff=0.09)
        self.frame = VGroup(guides, self.axes, x_axis_label, y_axis_label, zero)

    def point(self, x, y):
        return self.axes.c2p(x, y)

    def example_marks(self):
        x, y = EXAMPLE
        origin, edge, point = self.point(0, 0), self.point(x, 0), self.point(x, y)
        horizontal = Line(origin, edge, color=TREATMENT, stroke_width=4)
        vertical = DashedLine(edge, point, color=OUTCOME, stroke_width=3.0, dash_length=0.09)
        x_label = math("0.25", size=36, color=TREATMENT).next_to(edge, DOWN, buff=0.16)
        y_label = math("4", size=36, color=OUTCOME).next_to(point, RIGHT, buff=0.17)
        return VGroup(horizontal, vertical, x_label, y_label)

    def dots(self, observations, color=INK, *, squares=False):
        if squares:
            return VGroup(*(Square(side_length=0.13, color=color, stroke_width=1.8).move_to(self.point(x, y))
                            for x, y in observations)).set_z_index(3)
        return VGroup(*(Dot(self.point(x, y), radius=0.065, color=color)
                        for x, y in observations)).set_z_index(3)

    def fit(self, slope, color=LARGE_FIT, domain=(-0.88, 0.66)):
        start, end = domain
        return Line(self.point(start, slope * start), self.point(end, slope * end), color=color, stroke_width=3.7)

    def errors(self, observations, slope):
        return VGroup(*(
            Line(self.point(x, y), self.point(x, slope * x), color=OUTCOME, stroke_width=2.5)
            for x, y in observations if abs(y - slope * x) > 0.001
        ))


def large_summary():
    return VGroup(label("큰 매장", 34), math(r"\hat{\tau}=16", size=59, color=LARGE_FIT)).arrange(DOWN, buff=0.24).move_to(at(4.8, 1.48))


def example_readout():
    coordinates = math("(", "0.25", ",", "4", ")", size=56)
    coordinates[1].set_color(TREATMENT)
    coordinates[3].set_color(OUTCOME)
    return VGroup(label("한 매장의 두 잔차", 28, MUTED), coordinates).arrange(DOWN, buff=0.24).move_to(at(4.8, 1.23))


class LearnerScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        edition = Path(getfile(type(self))).resolve().parents[1]
        filename = f"{self.script}.timings.json"
        path = edition / "build" / "audio" / filename
        if not path.is_file():
            path = edition.parent / "build" / "audio" / filename
        self.clock = BeatClock(self, path, self.preview_durations)
        self.explain()
        self.clock.finish(tail=0.75)
