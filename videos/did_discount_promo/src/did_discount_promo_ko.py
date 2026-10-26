"""할인 기획전의 관찰된 증가와 인과 효과를 구분하는 Manim 러프컷."""

import json
from pathlib import Path

import numpy as np
from manim import *


config.frame_width = 16
config.frame_height = 9
config.background_color = "#0D0F1F"

ROOT = Path(__file__).resolve().parents[1]
FONT = "Pretendard Variable"
BG = "#0D0F1F"
WHITE = "#FFFFFF"
MUTED = "#9CA3AF"
GRID = "#374151"
TEAL = "#4DD0C4"
CONTROL = "#8AA6B2"
GOLD = "#C8A630"
RED = "#EF4444"

# 두 집단 모두 100곳. 마지막 두 사전 주와 진행 두 주의 합계가 DID 계산과 일치한다.
PRE_T = [4500, 4800, 4750, 5250, 4900, 5100]
PRE_C = [3400, 3750, 3800, 4050, 3900, 4100]
POST_T = [5900, 6100]
POST_C = [4400, 4600]
CF_T = [5400, 5600]
assert sum(PRE_T[-2:]) == 10000 and sum(PRE_C[-2:]) == 8000
assert sum(POST_T) == 12000 and sum(POST_C) == 9000 and sum(CF_T) == 11000
assert (sum(POST_T) - sum(PRE_T[-2:])) - (sum(POST_C) - sum(PRE_C[-2:])) == 1000


def label(text, size=32, color=WHITE, bold=False):
    args = {"font": FONT, "font_size": size, "color": color}
    if bold:
        args["weight"] = "BOLD"
    return Text(text, **args)


def polyline(points, color, width=5):
    line = VMobject().set_points_as_corners([np.array([x, y, 0]) for x, y in points])
    line.set_stroke(color, width=width)
    dots = VGroup(*[Dot([x, y, 0], radius=0.075, color=color) for x, y in points])
    return VGroup(line, dots)


class DIDDiscountPromoDraft(Scene):
    """
    핵심 주장: 예약 +2,000건이라는 관찰만으로 할인 기획전 효과를 알 수 없다.
    오해: 참여군의 단순 전후 차이가 곧 순증분이라는 생각.
    Visual pivot: 2주 합계의 참여군 → 대조군 → 주별 사전 추세 → 반사실 → 남는 면적.
    참고: book/why_causal_inference/why_causal_inference_ko.ipynb의 반사실 개념,
    3b1b/_2017/nn/part1.py의 어두운 바탕에서 선·숫자를 순차적으로 드러내는 방식.
    수치와 DID 사례는 사용자와 확정한 교육용 가상 설정이다.

    Beat 구성: src/scripts/ko/의 문장 한 줄이 build/timings.json의 같은 scene/beat와
    대응한다. 01 질문, 02 전후 비교의 함정, 03 대조군, 04 평행추세의 주의점,
    05 반사실과 순증분 계산을 순서대로 그린다.
    """

    def construct(self):
        data = json.loads((ROOT / "build" / "timings.json").read_text())
        self.beats = {(b["scene"], b["beat"]): b for b in data["beats"]}
        self.tag = label("교육용 가상 수치", 20, MUTED).to_corner(UR, buff=0.35)
        self.add(self.tag)
        self.scene_one()
        self.scene_two()
        self.scene_three()
        self.scene_four()
        self.scene_five()
        self.wait(max(0, data["total"] - self.time))

    def mark(self, scene, beat):
        start = self.beats[(scene, beat)]["start"]
        if self.time < start:
            self.wait(start - self.time)

    def finish(self, scene, beat):
        end = self.beats[(scene, beat)]["end"]
        if self.time < end:
            self.wait(end - self.time)
        elif self.time - end > 0.15:
            raise RuntimeError(f"화면 Beat {scene}-{beat}가 음성보다 {self.time-end:.2f}초 늦습니다")

    def clear_content(self):
        old = [mob for mob in self.mobjects if mob is not self.tag]
        if old:
            self.play(*[FadeOut(mob) for mob in old], run_time=0.35)

    def scene_one(self):
        # 01-01: 중앙에는 실제 예약 한 숫자만. 상단 짧은 사례명과 우측 가상 표기.
        self.mark(1, 1)
        topic = label("할인 기획전", 30, MUTED).move_to(UP * 2.6)
        context = label("참여 매장 100곳 / 진행 2주", 27, MUTED).move_to(UP * 0.85)
        observed = label("실제 예약 12,000건", 64, TEAL, True).move_to(DOWN * 0.15)
        self.play(FadeIn(topic), FadeIn(context), FadeIn(observed, shift=UP * 0.2), run_time=0.8)
        self.finish(1, 1)

        # 01-02: 실제 예약을 지우고 관찰된 증가를 단독으로 강조한다.
        self.mark(1, 2)
        inc_label = label("관찰된 증가", 30, MUTED).move_to(UP * 0.9)
        increase = label("+2,000건", 68, TEAL, True).move_to(DOWN * 0.15)
        caveat = label("기획전 효과로 바로 읽을 수 없음", 30, GOLD).move_to(DOWN * 1.25)
        self.play(FadeOut(context), FadeOut(observed), FadeIn(inc_label), FadeIn(increase), run_time=0.6)
        self.play(FadeIn(caveat), run_time=0.5)
        self.finish(1, 2)

        # 01-03: 원인 질문을 한 개의 빈칸으로 바꾼다.
        self.mark(1, 3)
        question = label("기획전이 없었다면?", 54, GOLD, True).move_to(UP * 0.45)
        blank = label("예상 예약  ?", 43, WHITE).move_to(DOWN * 0.6)
        self.play(FadeOut(inc_label), FadeOut(increase), FadeOut(caveat), FadeIn(question), run_time=0.6)
        self.play(FadeIn(blank), run_time=0.5)
        self.finish(1, 3)

    def total_axes(self, x_left=-4.7, x_right=4.7, y_base=-2.1, y_top=2.1):
        group = VGroup()
        for value, txt in [(0, "0"), (4000, "4천"), (8000, "8천"), (12000, "1만 2천")]:
            y = y_base + (value / 12000) * (y_top - y_base)
            group.add(Line([x_left, y, 0], [x_right, y, 0], color=GRID, stroke_width=1.5))
            group.add(label(txt, 21, MUTED).next_to([x_left, y, 0], LEFT, buff=0.18))
        group.add(label("이전 2주", 25, MUTED).move_to([x_left + 2.0, y_base - 0.48, 0]))
        group.add(label("진행 2주", 25, MUTED).move_to([x_right - 2.0, y_base - 0.48, 0]))
        return group, lambda value: y_base + (value / 12000) * (y_top - y_base)

    def scene_two(self):
        # 02-01: 축을 0부터 고정해 이전 2주 10,000건을 먼저 놓는다.
        self.mark(2, 1)
        self.clear_content()
        axes, y = self.total_axes()
        title = label("참여 매장 100곳 / 2주 합계", 27, MUTED).move_to(UP * 3.15)
        before = Rectangle(width=1.55, height=y(10000) - y(0), fill_color=CONTROL,
                           fill_opacity=0.65, stroke_width=0).move_to([-2.7, (y(10000)+y(0))/2, 0])
        before_number = label("10,000", 28, WHITE).next_to(before, UP, buff=0.15)
        self.play(FadeIn(title), FadeIn(axes), FadeIn(before), FadeIn(before_number), run_time=0.85)
        self.finish(2, 1)

        # 02-02: 같은 축에서 12,000건을 추가하고 +2,000건만 강조한다.
        self.mark(2, 2)
        after = Rectangle(width=1.55, height=y(12000) - y(0), fill_color=TEAL,
                          fill_opacity=0.9, stroke_width=0).move_to([2.7, (y(12000)+y(0))/2, 0])
        increase = label("+2,000", 38, TEAL, True).move_to([5.7, 0.25, 0])
        self.play(FadeIn(after), run_time=0.65)
        self.play(FadeIn(increase), run_time=0.35)
        self.finish(2, 2)

        # 02-03: 증가분을 만드는 다른 원인 가능성을 덧붙인다.
        self.mark(2, 3)
        other = label("계절 / 서비스 전체 수요", 30, GOLD).move_to([5.2, -1.0, 0])
        self.play(FadeIn(other), before.animate.set_fill(opacity=0.35),
                  after.animate.set_fill(opacity=0.55), run_time=0.6)
        self.finish(2, 3)

        # 02-04: 숫자를 걷고 관찰과 인과의 차이만 남긴다.
        self.mark(2, 4)
        self.clear_content()
        statement = VGroup(label("관찰된 증가", 49, TEAL, True), label("≠", 49, WHITE),
                           label("기획전 효과", 49, GOLD, True)).arrange(RIGHT, buff=0.28)
        self.play(FadeIn(statement, shift=UP * 0.2), run_time=0.6)
        self.finish(2, 4)

    def scene_three(self):
        # 03-01: 집단 규모를 같게 놓고 2주 합계의 공통 축을 제시한다.
        self.mark(3, 1)
        self.clear_content()
        axes, y = self.total_axes(x_left=-4.8, x_right=4.8)
        title = label("참여 100곳 / 대조군 100곳", 31, WHITE, True).move_to(UP * 3.2)
        unit = label("2주 합계, 같은 눈금", 23, MUTED).move_to(UP * 2.6)
        treated = polyline([(-2.8, y(10000)), (2.8, y(12000))], TEAL)
        treated_tag = label("참여", 25, TEAL).move_to([4.0, y(12000) + 0.22, 0])
        self.play(FadeIn(title), FadeIn(unit), FadeIn(axes), Create(treated[0]),
                  FadeIn(treated[1]), FadeIn(treated_tag), run_time=1.0)
        self.finish(3, 1)

        # 03-02: 대조군 8,000→9,000을 같은 축에 추가한다.
        self.mark(3, 2)
        control = polyline([(-2.8, y(8000)), (2.8, y(9000))], CONTROL)
        control_tag = label("대조군", 25, CONTROL).move_to([4.2, y(9000) - 0.2, 0])
        self.play(Create(control[0]), FadeIn(control[1]), FadeIn(control_tag), run_time=0.9)
        self.finish(3, 2)

        # 03-03: 대조군의 증가분 하나만 남긴다.
        self.mark(3, 3)
        delta = label("대조군도 +1,000건", 39, GOLD, True).move_to(DOWN * 3.35)
        self.play(FadeIn(delta), run_time=0.6)
        self.finish(3, 3)

    def weekly_axes(self, post=False):
        x0, x1 = (-6.5, 2.5) if post else (-5.1, 5.1)
        x_values = [x0 + (x1-x0)*i/(7 if post else 5) for i in range(8 if post else 6)]
        y0, y1 = -2.15, 1.75
        minimum, maximum = 3000, 6500
        y = lambda value: y0 + (value-minimum)/(maximum-minimum)*(y1-y0)
        grid = VGroup()
        for value in [3000, 4000, 5000, 6000]:
            yy = y(value)
            grid.add(Line([x0, yy, 0], [x1, yy, 0], color=GRID, stroke_width=1.3))
            grid.add(label(f"{value//1000}천", 20, MUTED).next_to([x0, yy, 0], LEFT, buff=0.15))
        names = ["6주 전", "5주 전", "4주 전", "3주 전", "2주 전", "직전 주"]
        if post:
            names += ["진행 1주", "진행 2주"]
        for x, name in zip(x_values, names):
            grid.add(label(name, 19 if post else 21, MUTED).move_to([x, y0-0.42, 0]))
        unit = label("주별 예약 / 집단당 100곳", 24, MUTED).move_to([-3.75 if post else -2.8, 2.65, 0])
        return grid, unit, x_values, y

    def scene_four(self):
        # 04-01: 숫자 비교를 치우고 대조군 선정 질문으로 시선을 옮긴다.
        self.mark(4, 1)
        self.clear_content()
        question = label("좋은 대조군인가?", 54, WHITE, True).move_to(UP * 0.5)
        hint = label("기획전 전 흐름을 살펴보자", 31, GOLD).move_to(DOWN * 0.75)
        self.play(FadeIn(question), FadeIn(hint), run_time=0.6)
        self.finish(4, 1)

        # 04-02: 2주 합계에서 주별 예약으로 단위를 명시적으로 바꾼다.
        self.mark(4, 2)
        self.play(FadeOut(question), FadeOut(hint), run_time=0.3)
        unit_switch = label("2주 합계  →  주별 예약", 33, GOLD, True).move_to(UP * 3.3)
        axes, unit, x, y = self.weekly_axes()
        self.play(FadeIn(unit_switch), FadeIn(unit), FadeIn(axes), run_time=0.8)
        self.finish(4, 2)

        # 04-03: 서로 완전히 일치하지 않는 사전 6주 선을 순서대로 그린다.
        self.mark(4, 3)
        treated = polyline(list(zip(x, map(y, PRE_T))), TEAL, width=4.5)
        control = polyline(list(zip(x, map(y, PRE_C))), CONTROL, width=4.5)
        legend_t = label("참여", 25, TEAL).move_to([2.7, 2.6, 0])
        legend_c = label("대조군", 25, CONTROL).move_to([4.35, 2.6, 0])
        self.play(Create(treated[0]), FadeIn(treated[1]), FadeIn(legend_t), run_time=1.0)
        self.play(Create(control[0]), FadeIn(control[1]), FadeIn(legend_c), run_time=1.0)
        self.finish(4, 3)

        # 04-04: 사전 추세가 가정의 증명이 아니라는 경계 문구를 보여준다.
        self.mark(4, 4)
        caution = label("평행추세 가정: 근거는 있어도 증명은 아님", 30, GOLD).move_to(DOWN * 3.55)
        self.play(FadeIn(caution), run_time=0.6)
        self.finish(4, 4)

        # 04-05: 대조군 선택의 추가 판단 요소를 남긴다.
        self.mark(4, 5)
        other = label("매장 특성 / 같은 시기의 다른 변화도 확인", 29, MUTED).move_to(DOWN * 3.55)
        self.play(FadeOut(caution), FadeIn(other), run_time=0.55)
        self.finish(4, 5)

    def scene_five(self):
        # 05-01: 주별 축을 이어받아 대조군의 진행 변화와 반사실 11,000건을 만든다.
        self.mark(5, 1)
        self.clear_content()
        axes, unit, x, y = self.weekly_axes(post=True)
        pre_t = polyline(list(zip(x[:6], map(y, PRE_T))), TEAL, width=4)
        all_c = polyline(list(zip(x, map(y, PRE_C + POST_C))), CONTROL, width=4)
        treatment_start = Dot([x[5], y(PRE_T[5]), 0], color=TEAL, radius=0.075)
        cf = polyline([(x[5], y(PRE_T[5])), (x[6], y(CF_T[0])), (x[7], y(CF_T[1]))], GOLD, width=4)
        cf[0].set_stroke(GOLD, width=4)
        cf_tag = label("기획전이 없었다면", 25, GOLD).move_to([5.1, 1.25, 0])
        cf_total = label("2주 약 11,000건", 35, GOLD, True).move_to([5.25, 0.35, 0])
        self.play(FadeIn(axes), FadeIn(unit), FadeIn(pre_t), FadeIn(all_c), FadeIn(treatment_start), run_time=0.8)
        self.play(Create(cf[0]), FadeIn(cf[1]), FadeIn(cf_tag), FadeIn(cf_total), run_time=0.9)
        self.finish(5, 1)

        # 05-02: 실제 진행 2주를 드러낸 뒤 추정 간격을 두 주의 면적으로 칠한다.
        self.mark(5, 2)
        actual = polyline([(x[5], y(PRE_T[5])), (x[6], y(POST_T[0])), (x[7], y(POST_T[1]))], TEAL, width=4.5)
        actual_total = label("실제 12,000건", 34, TEAL, True).move_to([5.25, -0.55, 0])
        areas = VGroup(*[
            Polygon([x[i]-0.25, y(CF_T[i-6]), 0], [x[i]+0.25, y(CF_T[i-6]), 0],
                    [x[i]+0.25, y(POST_T[i-6]), 0], [x[i]-0.25, y(POST_T[i-6]), 0],
                    stroke_width=0, fill_color=RED, fill_opacity=0.35)
            for i in [6, 7]
        ])
        net = label("2주 순증분 1,000건", 36, RED, True).move_to([5.3, -1.7, 0])
        self.play(Create(actual[0]), FadeIn(actual[1]), FadeIn(actual_total), run_time=0.85)
        self.play(FadeIn(areas), FadeIn(net), run_time=0.7)
        self.finish(5, 2)

        # 05-03: 색칠한 두 주를 500+500으로 읽게 한다.
        self.mark(5, 3)
        weekly = VGroup(*[
            label("+500", 24, RED, True).move_to([x[i], (y(CF_T[i-6])+y(POST_T[i-6]))/2, 0])
            for i in [6, 7]
        ])
        self.play(FadeIn(weekly[0]), run_time=0.4)
        self.play(FadeIn(weekly[1]), run_time=0.4)
        self.finish(5, 3)

        # 05-04: 2주 합계의 완전한 DID 계산식으로 환원한다.
        self.mark(5, 4)
        self.clear_content()
        formula = label("(12,000 − 10,000) − (9,000 − 8,000)", 45, WHITE, True)
        formula.scale_to_fit_width(13.8)
        formula.move_to(UP * 0.45)
        answer = label("= 1,000건", 53, RED, True).move_to(DOWN * 0.8)
        self.play(FadeIn(formula), run_time=0.6)
        self.play(FadeIn(answer), run_time=0.5)
        self.finish(5, 4)

        # 05-05: 방법 이름은 답을 만든 뒤에 붙인다.
        self.mark(5, 5)
        did = label("DID / 이중차분법", 31, GOLD).move_to(DOWN * 2.3)
        self.play(FadeIn(did), run_time=0.5)
        self.finish(5, 5)

        # 05-06: 과제의 Why로 돌아가 마무리한다.
        self.mark(5, 6)
        self.clear_content()
        observation = label("예약 증가  ≠  기획전 효과", 48, WHITE, True).move_to(UP * 0.65)
        why = label("그래서 인과추론이 필요합니다", 47, GOLD, True).move_to(DOWN * 0.7)
        self.play(FadeIn(observation), run_time=0.6)
        self.play(FadeIn(why), run_time=0.6)
        self.finish(5, 6)
