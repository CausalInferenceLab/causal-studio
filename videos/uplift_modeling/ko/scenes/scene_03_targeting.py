from manim import Create, Dot, DOWN, FadeIn, FadeOut, Line, ReplacementTransform, RIGHT, UP, VGroup

from videos.uplift_modeling.shared.common import (
    AUDIENCES, CONTROL, COUPON, LIFT, MUTED, TRACK, UpliftScene,
    at, label, number, ranked_change, RatePanel, title,
)


class Targeting(UpliftScene):
    script = "03_targeting"
    preview_durations = (9.0, 8.4, 9.2)

    def explain(self):
        panels = [RatePanel(a) for a in AUDIENCES]
        header = title("업리프트", y=3.05)
        self.add(header, *(p.full for p in panels))
        left, right = panels
        first, second = (ranked_change(a, y) for a, y in zip(AUDIENCES, (0.65, -0.64)))
        marker = Line(at(-2.70, -1.34), at(-2.70, 1.32), color=TRACK, stroke_width=1.7)
        zero = number("0", 33, MUTED).move_to(at(-2.70, -1.58))
        unit = label("쿠폰 100건당 추가 구매", 37).move_to(at(0, 2.20))
        formula = number(r"\widehat{p}_{\mathrm{coupon}}(x)-\widehat{p}_{\mathrm{no\ coupon}}(x)", 44)
        formula.move_to(at(0, -2.54))
        score = title("높은 업리프트부터", y=2.20)

        with self.clock.beat() as beat:
            self.play(
                FadeOut(header), FadeIn(unit), Create(marker), FadeIn(zero),
                FadeOut(VGroup(left.treated, left.control, left.guides, right.treated, right.control, right.guides)),
                ReplacementTransform(left.heading, first[0]), ReplacementTransform(right.heading, second[0]),
                ReplacementTransform(left.interval, first[1]), ReplacementTransform(right.interval, second[1]),
                ReplacementTransform(left.delta, first[2]), ReplacementTransform(right.delta, second[2]),
                run_time=1.40,
            )
            self.wait(beat * 0.24)

        with self.clock.beat() as beat:
            self.play(FadeIn(formula, shift=DOWN * 0.12), run_time=0.73)
            self.wait(beat * 0.35)
            row_gap = 1.29 * UP
            self.play(FadeOut(unit), FadeIn(score), FadeOut(first), run_time=0.48)
            self.play(second.animate.shift(row_gap), run_time=0.73)
            first.shift(-row_gap).set_opacity(0.40)
            self.play(FadeIn(first), run_time=0.38)

        with self.clock.beat() as beat:
            outcome = label("별도 무작위 실험에서 검증", 40).move_to(at(0, 2.26))
            high = label("업리프트 점수가 높은 고객", 33).move_to(at(0, 0.88))
            sent = VGroup(Dot(radius=0.085, color=COUPON), label("발송군", 35, COUPON)).arrange(RIGHT, buff=0.18).move_to(at(-2.28, -0.70))
            held = VGroup(Dot(radius=0.085, color=CONTROL), label("미발송군", 35, CONTROL)).arrange(RIGHT, buff=0.18).move_to(at(2.28, -0.70))
            branches = VGroup(
                Line(at(0, 0.56), at(-2.28, -0.24), color=TRACK, stroke_width=2.0),
                Line(at(0, 0.56), at(2.28, -0.24), color=TRACK, stroke_width=2.0),
            )
            test = label("두 그룹의 구매율 차이 확인", 34, LIFT).move_to(at(0, -2.06))
            self.play(
                FadeOut(VGroup(score, first, second, marker, zero, formula)),
                FadeIn(outcome), FadeIn(high), run_time=0.83,
            )
            self.wait(beat * 0.27)
            self.play(Create(branches), FadeIn(sent), FadeIn(held), run_time=0.77)
            self.wait(beat * 0.14)
            self.play(FadeIn(test), run_time=0.62)
