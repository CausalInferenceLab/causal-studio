from manim import *

from videos.fuzzy_rdd.shared.common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
)


class Scene07Recap(Scene):
    """
    Scene 07: recap (English port of Scene07Recap)
    스크립트: narration/07_recap.txt
    타이밍: build/audio/07_recap.timings.json (총 25.15s, 3 chunks)

    한국어 최종본과 동일한 3비트 구조(정의 → 왈드 점추정 → 2SLS 신뢰구간 → 마무리)를
    그대로 포팅. Beat2/3의 왈드→2SLS 전환, 마무리 문장 등장 시점은 한국어 버전에서도
    문장 길이 비율로 추정한 값이었으므로, 같은 방식(구 청크 내 비율 → 새 청크 길이)으로
    재추정했다: 전환 ≈13.49s(청크2 내), 마무리 문장 ≈22.16s(청크3 내).

    Beat1 chunk1 ( 0.00~10.50)  Fuzzy RDD one-line definition (recap)
    Beat2 chunk2 (10.50~17.09)  Wald (point estimate, no CI) -> 2SLS (same point + CI)
        Scene06 Beat3/4 visual grammar reused: TEAL dot = point estimate, RED = no CI,
        GOLD bar+caps = CI, TEAL dashed connector = "interval centered on that point".
    Beat3 chunk3 (17.09~25.15)  closing: Sharp RDD checked, Fuzzy RDD checked -> next video (WAIT_TAIL)
    """

    def construct(self):
        import numpy as np

        # ── Beat 1 (chunk1, 0->10.50) Fuzzy RDD one-line definition (recap) ──
        defn = VGroup(
            Text("Fuzzy RDD", font=FONT, font_size=40, color=TEAL_MAIN),
            Text("When the cutoff doesn't fully determine treatment,", font=FONT, font_size=24, color=WHITE),
            Text("using eligibility as an instrument", font=FONT, font_size=24, color=GOLD_MAIN),
            Text("to estimate LATE on compliers", font=FONT, font_size=24, color=WHITE,
                 t2c={"LATE": GOLD_MAIN}),
        ).arrange(DOWN, buff=0.38).move_to(ORIGIN)
        self.play(FadeIn(defn[0], shift=UP * 0.2), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in defn[1:]], lag_ratio=0.4), run_time=1.4)
        self.wait(8.4954)

        # ── Beat 2 (chunk2, 10.50->17.09) Wald(point) -> 2SLS(point+CI) ──
        label = Text("Wald Estimator", font=FONT, font_size=32, color=TEAL_MAIN).move_to(UP * 1.7)
        underline = Line(label.get_corner(DL), label.get_corner(DR), color=TEAL_MAIN, stroke_width=2.5).shift(DOWN * 0.12)
        point = Dot(UP * 0.5, radius=0.13, color=TEAL_MAIN)
        value_lab = MathTex(r"\hat{\tau}", font_size=36).set_color(TEAL_MAIN).next_to(point, RIGHT, buff=0.35)
        dot_cap = Text("point estimate", font=FONT, font_size=16, color=TEAL_MAIN).next_to(point, LEFT, buff=0.35)
        blocked = Text("can't get a confidence interval", font=FONT, font_size=20, color=RED_MAIN).next_to(point, DOWN, buff=0.9)
        self.play(FadeOut(defn, run_time=0.4),
                  FadeIn(label, run_time=0.5), Create(underline, run_time=0.5), FadeIn(point, run_time=0.5),
                  FadeIn(value_lab, run_time=0.5), FadeIn(dot_cap, run_time=0.5),
                  FadeIn(blocked, run_time=0.5))
        self.wait(2.498)
        # Wald -> 2SLS: point/value/caption (TEAL) stay put; label is erased then rewritten
        # (fade out with underline, then Write back in) instead of an instant swap.
        label2 = Text("2SLS", font=FONT, font_size=32, color=GOLD_MAIN).move_to(label)
        underline2 = Line(label2.get_corner(DL), label2.get_corner(DR), color=GOLD_MAIN, stroke_width=2.5).shift(DOWN * 0.12)
        self.play(FadeOut(VGroup(label, underline), shift=UP * 0.15, run_time=0.4))
        self.play(Write(label2, run_time=0.5), Create(underline2, run_time=0.5))
        # red text is replaced by a GOLD CI bar + TEAL dashed connector; add a "confidence
        # interval" caption and a Flash on the point for a fuller closing-scene payoff.
        cx, py = point.get_center()[0], point.get_center()[1]
        ci_cy = py - 1.0
        ci_half = 0.85
        ci_bar = Line(np.array([cx - ci_half, ci_cy, 0]), np.array([cx + ci_half, ci_cy, 0]), color=GOLD_MAIN, stroke_width=5)
        ci_capL = Line(np.array([cx - ci_half, ci_cy - 0.16, 0]), np.array([cx - ci_half, ci_cy + 0.16, 0]), color=GOLD_MAIN, stroke_width=5)
        ci_capR = Line(np.array([cx + ci_half, ci_cy - 0.16, 0]), np.array([cx + ci_half, ci_cy + 0.16, 0]), color=GOLD_MAIN, stroke_width=5)
        ci_center = Dot(np.array([cx, ci_cy, 0]), radius=0.09, color=TEAL_MAIN)
        connector = DashedLine(point.get_bottom() + DOWN * 0.05, np.array([cx, ci_cy + 0.2, 0]),
                               color=TEAL_MAIN, stroke_width=1.6, dash_length=0.08)
        ci_fig = VGroup(ci_bar, ci_capL, ci_capR, ci_center)
        ci_cap = Text("confidence interval", font=FONT, font_size=18, color=GOLD_MAIN).next_to(ci_bar, DOWN, buff=0.28)
        self.play(FadeOut(blocked, run_time=0.3),
                  Create(connector, run_time=0.5), Create(ci_fig, run_time=0.6), FadeIn(ci_cap, run_time=0.6),
                  Flash(point, color=GOLD_MAIN, flash_radius=0.4, line_length=0.22, num_lines=10, run_time=0.6))
        self.wait(2.097)

        # ── Beat 3 (chunk3, 17.09->25.15) closing (WAIT_TAIL) ─────
        done = VGroup(
            Text("Sharp RDD  ✓", font=FONT, font_size=32, color=GREEN_MAIN),
            Text("Fuzzy RDD  ✓", font=FONT, font_size=32, color=GREEN_MAIN),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        nextv = Text("See you in the next video with another causal inference method", font=FONT, font_size=22, color=GRAY_MID).move_to(DOWN * 1.3)
        self.play(FadeOut(VGroup(label2, underline2, point, value_lab, dot_cap, connector, ci_fig, ci_cap), run_time=0.4),
                  FadeIn(done, shift=UP * 0.15, run_time=0.6))
        self.wait(4.467)
        self.play(FadeIn(nextv, shift=UP * 0.1, run_time=0.5))
        # WAIT_TAIL = (25.150 + 0.45) - 22.157 - 0.5 = 2.943
        self.wait(2.943)
