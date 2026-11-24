from inspect import getfile
from pathlib import Path

from manim import (
    DashedLine, Dot, DOWN, LEFT, Line, ORIGIN, RIGHT, Scene, Text, UP, VGroup,
)
from manimpango import list_fonts
from manim_timing import BeatClock


# BLACK, WHITE, GREY_B, GREY_D, BLUE_C, and YELLOW_C from 3Blue1Brown's Manim palette.
BACKGROUND = "#000000"
INK = "#FFFFFF"
MUTED = "#BBBBBB"
GUIDE = "#444444"
CONTROL = "#58C4DD"
EFFECT = "#FFFF00"
TREAT_BEFORE, TREAT_AFTER = 100, 160
CONTROL_BEFORE, CONTROL_AFTER = 80, 100
TREAT_CHANGE = TREAT_AFTER - TREAT_BEFORE
CONTROL_CHANGE = CONTROL_AFTER - CONTROL_BEFORE
WITHOUT_SERVICE = TREAT_BEFORE + CONTROL_CHANGE
DID = TREAT_AFTER - WITHOUT_SERVICE
BEFORE_X, AFTER_X = -4.1, 2.5
MEASURE_X = 4.35
FONTS = set(list_fonts())
LABEL_FONT = next(
    (font for font in ("Apple SD Gothic Neo", "Noto Sans CJK KR", "Noto Sans KR") if font in FONTS),
    "sans-serif",
)
NUMBER_FONT = "Georgia" if "Georgia" in FONTS else "serif"


def label(value, size=28, color=INK):
    return Text(str(value), font=LABEL_FONT, font_size=size, color=color)


def numeral(value, size=42, color=INK):
    return Text(str(value), font=NUMBER_FONT, font_size=size, color=color)


def at(x, y):
    return ORIGIN + x * RIGHT + y * UP


def rides(x, value):
    return at(x, -2.0 + (value - 70) * 0.043)


def endpoint(x, value, color=INK, *, hollow=False, label_side=None):
    point = Dot(rides(x, value), radius=0.066, color=color)
    if hollow:
        point.set_fill(BACKGROUND, opacity=1).set_stroke(color, width=2.2)
    side = label_side if label_side is not None else (LEFT if x == BEFORE_X else RIGHT)
    number = numeral(value, color=color).next_to(point, side, buff=0.16)
    return VGroup(point, number).set_z_index(3)


def measure(x, low, high, color, *, draw_guides=True):
    bottom, top = rides(x, low), rides(x, high)
    tick = 0.08 * RIGHT
    span = VGroup(Line(bottom, top), Line(bottom - tick, bottom + tick), Line(top - tick, top + tick))
    span.set_stroke(color, width=2.2)
    amount = numeral(f"+{high - low}", size=51, color=color).next_to(span, RIGHT, buff=0.22)
    guides = VGroup()
    if draw_guides:
        for value in (low, high):
            guides.add(Line(rides(AFTER_X + 0.98, value), rides(x - 0.10, value), color=GUIDE, stroke_width=1.4))
    return VGroup(guides, span, amount)


class DidChart:
    def __init__(self):
        self.time_rule = Line(at(BEFORE_X, -2.23), at(AFTER_X, -2.23), color=GUIDE, stroke_width=2.2)
        self.guides = VGroup(
            Line(at(BEFORE_X, -2.23), rides(BEFORE_X, 155), color=GUIDE, stroke_width=1.2),
            Line(at(AFTER_X, -2.23), rides(AFTER_X, 169), color=GUIDE, stroke_width=1.2),
        )
        self.dates = VGroup(
            label("증편 전", color=MUTED).move_to(at(BEFORE_X, -2.57)),
            label("증편 후", color=MUTED).move_to(at(AFTER_X, -2.57)),
        )
        self.unit = label("하루 평균 탑승객 · 명", size=26, color=MUTED).move_to(at(-5.15, 2.47), aligned_edge=LEFT)
        self.treated_line = Line(rides(BEFORE_X, TREAT_BEFORE), rides(AFTER_X, TREAT_AFTER), color=INK, stroke_width=3.3)
        self.control_line = Line(
            rides(BEFORE_X, CONTROL_BEFORE), rides(AFTER_X, CONTROL_AFTER), color=CONTROL, stroke_width=3.3,
        )
        self.treated_from = endpoint(BEFORE_X, TREAT_BEFORE)
        self.treated_to = endpoint(AFTER_X, TREAT_AFTER)
        self.control_from = endpoint(BEFORE_X, CONTROL_BEFORE, CONTROL)
        self.control_to = endpoint(AFTER_X, CONTROL_AFTER, CONTROL)
        self.treated_name = label("증편 지역", size=29).move_to(at(-2.75, 0.45))
        self.control_name = label("비교 지역", size=29, color=CONTROL).move_to(at(-2.75, -1.92))
        self.treat_growth = measure(MEASURE_X, TREAT_BEFORE, TREAT_AFTER, INK)
        self.control_growth = measure(MEASURE_X, CONTROL_BEFORE, CONTROL_AFTER, CONTROL)
        self.observed = VGroup(
            self.treated_line, self.control_line, self.treated_from, self.treated_to,
            self.control_from, self.control_to, self.treated_name, self.control_name,
        )
        self.frame = VGroup(self.time_rule, self.guides, self.dates, self.unit)

    def estimate(self, value=WITHOUT_SERVICE):
        path = DashedLine(
            rides(BEFORE_X, TREAT_BEFORE), rides(AFTER_X, value),
            dash_length=0.18, dashed_ratio=0.56, color=CONTROL, stroke_width=3.3,
        )
        point = endpoint(AFTER_X, value, CONTROL, hollow=True)
        return path, point, measure(MEASURE_X, value, TREAT_AFTER, EFFECT)

    def comparison_change_at_treated_start(self):
        return measure(MEASURE_X, TREAT_BEFORE, WITHOUT_SERVICE, CONTROL)


class DidScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        self.chart = DidChart()
        edition = Path(getfile(type(self))).resolve().parents[1]
        filename = f"{self.script}.timings.json"
        path = edition / "build" / "audio" / filename
        if not path.is_file():
            path = edition.parent / "build" / "audio" / filename
        self.clock = BeatClock(self, path, self.preview_durations)
        self.animate_explanation()
        self.clock.finish(tail=self.tail)
