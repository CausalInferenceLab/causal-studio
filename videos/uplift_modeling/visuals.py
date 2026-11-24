from dataclasses import dataclass
from pathlib import Path

import numpy as np
from manim import Circle, DashedLine, Dot, DOWN, LEFT, Line, MathTex, RIGHT, Scene, Text, UP, VGroup
from manimpango import list_fonts
from manim_timing import BeatClock


BACKGROUND = "#000000"
INK = "#FFFFFF"
MUTED = "#AAAAAA"
TRACK = "#35434A"
GUIDE = "#66767E"
COUPON = "#F4D345"
CONTROL = "#58C4DD"
LIFT = "#83C167"
FONTS = set(list_fonts())
FONT = next((f for f in ("Apple SD Gothic Neo", "Noto Sans CJK KR", "Noto Sans KR") if f in FONTS), "sans-serif")


@dataclass(frozen=True)
class Audience:
    name: str
    center: float
    control: int
    treated: int

    @property
    def lift(self):
        return self.treated - self.control


LOYAL = Audience("단골", -3.38, 70, 75)
HESITANT = Audience("구매 고민층", 3.38, 25, 45)
AUDIENCES = (LOYAL, HESITANT)


def at(x, y):
    return np.array([x, y, 0.0])


def label(text, size=31, color=INK):
    return Text(text, font=FONT, font_size=size, color=color)


def number(text, size=57, color=INK):
    return MathTex(text, font_size=size, color=color)


def title(text, y=3.02):
    return label(text, 39).move_to(at(0, y))


def audience_name(audience, y):
    return label(audience.name, 34).move_to(at(audience.center, y))


def cohort_cells(audience, filled):
    cells = []
    for index in range(100):
        row, column = divmod(index, 10)
        point = at(audience.center + (column - 4.5) * 0.238, 0.03 + (4.5 - row) * 0.238)
        if index < filled:
            mark = Dot(point, radius=0.061, color=COUPON)
        else:
            mark = Circle(radius=0.061, stroke_width=1.55, color=GUIDE).move_to(point)
        cells.append(mark)
    return VGroup(*cells)


def dot_block(audience):
    score = number(f"{audience.treated}\\%", 64, COUPON).move_to(at(audience.center, 1.63))
    name = audience_name(audience, -1.65)
    return VGroup(cohort_cells(audience, audience.treated), score, name)


def opening_comparison():
    blocks = VGroup(*(dot_block(a) for a in AUDIENCES))
    header = title("쿠폰을 받으면 얼마나 살까?")
    relation = number(">", 68).move_to(at(0, 1.63))
    return blocks, header, relation


class RatePanel:
    def __init__(self, audience):
        center = audience.center
        left = center - 2.45
        width = 4.78
        self.heading = audience_name(audience, 2.15)
        self.treated = self.rate(left, width, 0.73, audience.treated, COUPON, "쿠폰 있음")
        self.control = self.rate(left, width, -0.61, audience.control, CONTROL, "쿠폰 없음")
        high = left + width * audience.treated / 100
        low = left + width * audience.control / 100
        y = -1.70
        self.guides = VGroup(
            DashedLine(at(high, 0.63), at(high, y), color=GUIDE, stroke_width=1.8, dash_length=0.10),
            DashedLine(at(low, -0.71), at(low, y), color=GUIDE, stroke_width=1.8, dash_length=0.10),
        ).set_z_index(-1)
        self.interval = Line(at(low, y), at(high, y), color=LIFT, stroke_width=5.0)
        self.delta = number(f"+{audience.lift}\\%\\mathrm{{p}}", 53, LIFT).next_to(self.interval, DOWN, buff=0.18)
        self.readout = VGroup(self.guides, self.interval, self.delta)
        self.full = VGroup(self.heading, self.treated, self.control, self.readout)

    @staticmethod
    def rate(left, width, y, rate, color, condition):
        endpoint = left + width * rate / 100
        track = Line(at(left, y), at(left + width, y), color=TRACK, stroke_width=1.8)
        fill = Line(at(left, y), at(endpoint, y), color=color, stroke_width=6.0)
        name = label(condition, 25, color).next_to(at(left, y), UP, buff=0.15).align_to(at(left, y), LEFT)
        score = number(f"{rate}\\%", 43, color).next_to(fill.get_end(), RIGHT, buff=0.15)
        score.add_background_rectangle(color=BACKGROUND, opacity=1, buff=0.045)
        return VGroup(track, fill, name, score)


def ranked_change(audience, y):
    x = -2.70
    end = x + audience.lift * 0.32
    bar = Line(at(x, y), at(end, y), color=LIFT, stroke_width=7.0)
    name = label(audience.name, 34).next_to(at(x, y), LEFT, buff=0.47)
    value = number(f"+{audience.lift}", 60, LIFT).next_to(bar.get_end(), RIGHT, buff=0.22)
    return VGroup(name, bar, value)


class UpliftScene(Scene):
    def construct(self):
        self.camera.background_color = BACKGROUND
        path = Path(__file__).resolve().parent / "build" / "audio" / f"{self.script}.timings.json"
        self.clock = BeatClock(self, path, self.preview_durations)
        self.explain()
        self.clock.finish(tail=0.72)
