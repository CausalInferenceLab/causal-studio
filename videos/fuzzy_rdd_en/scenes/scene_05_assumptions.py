from manim import *

from fuzzy_rdd_en_common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
)


class Scene05Assumptions(Scene):
    """
    Scene 05: assumptions (English port of Scene05Assumptions)
    스크립트: src/scripts/05_assumptions.txt
    타이밍: build/audio/05_assumptions.timings.json (총 62.26s, 6 chunks) — 전 체크포인트 청크 경계와 일치.

    Beat1 chunk1-2 ( 0.00~12.40)  Z = instrument (IV) -> 3 validity conditions (left list)
    Beat2 chunk3   (12.40~31.90)  relevance: Cov(Z,D)!=0, denominator!=0, F>10
    Beat3 chunk4   (31.90~43.98)  exclusion restriction: Z->D->Y, no direct path
    Beat4 chunk5   (43.98~56.29)  monotonicity: no defiers, D(Z=1)>=D(Z=0)
    Beat5 chunk6   (56.29~62.26)  3 conditions hold -> Wald = LATE (WAIT_TAIL)
    """

    def construct(self):
        import numpy as np
        # ── Beat 1 (chunk1-2) IV -> 3 conditions list ─────────────
        head = VGroup(
            Text("Eligibility Z = Instrumental Variable (IV)", font=FONT, font_size=34, color=TEAL_MAIN),
            Text("Fuzzy RDD is fundamentally an IV estimation problem", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(head, shift=UP * 0.2), run_time=0.6)
        self.wait(9.7524 - 0.6)

        top = Text("Three conditions for a valid instrument", font=FONT, font_size=24, color=GRAY_MID).to_edge(UP, buff=0.8)
        t1 = Text("1. Relevance", font=FONT, font_size=27, color=GRAY_MID)
        t2 = Text("2. Exclusion restriction", font=FONT, font_size=27, color=GRAY_MID)
        t3 = Text("3. Monotonicity", font=FONT, font_size=27, color=GRAY_MID)
        titles = VGroup(t1, t2, t3).arrange(DOWN, buff=0.9, aligned_edge=LEFT).move_to(LEFT * 4.0)
        sep = Line(UP * 1.9, DOWN * 1.9, color=GRAY_MID, stroke_width=1).move_to(LEFT * 1.6)

        self.play(FadeOut(head, run_time=0.4), FadeIn(top, run_time=0.5), FadeIn(titles, shift=RIGHT * 0.1, run_time=0.6), Create(sep, run_time=0.5))
        self.wait(12.3995 - 9.7524 - 0.4 - 0.6)

        detail_pos = RIGHT * 2.4

        # ── Beat 2 (chunk3) relevance ────────────────────────────
        d1 = VGroup(
            Text("Eligibility must actually raise treatment probability", font=FONT, font_size=22, color=WHITE),
            MathTex(r"\mathrm{Cov}(Z, D) \neq 0", font_size=34).set_color(TEAL_MAIN),
            Text("= Wald denominator != 0", font=FONT, font_size=20, color=GRAY_MID),
            Text("F-statistic > 10 -> strong instrument", font=FONT, font_size=20, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.4).move_to(detail_pos)
        self.play(t1.animate.set_color(TEAL_MAIN), FadeIn(d1, shift=UP * 0.1, run_time=0.6))
        self.wait(31.9042 - 12.3995 - 0.6)

        # ── Beat 3 (chunk4) exclusion restriction ────────────────
        diagram = self._iv_diagram_icons()
        d2 = VGroup(
            Text("Eligibility must affect the outcome only through treatment", font=FONT, font_size=22, color=WHITE),
            diagram,
            Text("No direct Z -> Y path allowed", font=FONT, font_size=20, color=RED_MAIN),
        ).arrange(DOWN, buff=0.45).move_to(detail_pos)
        self.play(t1.animate.set_color(GRAY_MID), t2.animate.set_color(TEAL_MAIN),
                  FadeOut(d1), FadeIn(d2, shift=UP * 0.1), run_time=0.5)
        self.wait(43.9786 - 31.9042 - 0.5)

        # ── Beat 4 (chunk5) monotonicity ──────────────────────────
        d3 = VGroup(
            Text("No one refuses treatment upon becoming eligible (no defiers)", font=FONT, font_size=22, color=WHITE),
            MathTex(r"D_i(Z{=}1) \geq D_i(Z{=}0)", font_size=32).set_color(TEAL_MAIN),
            Text("All the added treatment comes from compliers", font=FONT, font_size=20, color=GRAY_MID),
        ).arrange(DOWN, buff=0.45).move_to(detail_pos)
        self.play(t2.animate.set_color(GRAY_MID), t3.animate.set_color(TEAL_MAIN),
                  FadeOut(d2), FadeIn(d3, shift=UP * 0.1), run_time=0.5)
        self.wait(56.2852 - 43.9786 - 0.5)

        # ── Beat 5 (chunk6) conclusion ─────────────────────────────
        concl = VGroup(
            Text("If these three assumptions hold,", font=FONT, font_size=24, color=WHITE),
            Text("Wald estimator = LATE", font=FONT, font_size=32, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(detail_pos)
        self.play(t3.animate.set_color(GRAY_MID),
                  t1.animate.set_color(TEAL_MAIN), t2.animate.set_color(TEAL_MAIN),
                  FadeOut(d3), FadeIn(concl, shift=UP * 0.1), run_time=0.6)
        self.play(t3.animate.set_color(TEAL_MAIN), run_time=0.3)
        # WAIT_TAIL = (62.261 + 0.5) - 56.285 - 0.6 - 0.3 = 5.576
        self.wait(5.576)

    def _iv_diagram_icons(self) -> VGroup:
        """Z->D->Y icon diagram (clinical trial example, exclusion restriction)."""
        from pathlib import Path
        import numpy as np

        ICONS = Path(__file__).parent.parent.parent / "assets" / "tabler-icons" / "icons" / "outline"
        xs     = [-2.2,  0.0,  2.2]
        svgs   = ["vaccine-bottle.svg", "pill.svg", "heartbeat.svg"]
        vars_  = ["Z", "D", "Y"]
        colors = [GOLD_MAIN, TEAL_MAIN, WHITE]
        subs   = ["Trial assignment", "Taking the drug", "Health improves"]

        nodes = []
        for x, svg, var, color, sub in zip(xs, svgs, vars_, colors, subs):
            ico = SVGMobject(str(ICONS / svg), height=0.75)
            ico.set_stroke(color=color, width=2.0, family=True).set_fill(opacity=0)
            ico.move_to(np.array([x, 0.1, 0]))
            v = MathTex(var, font_size=24).set_color(color).next_to(ico, UP, buff=0.12)
            s = Text(sub, font=FONT, font_size=13, color=GRAY_MID).next_to(ico, DOWN, buff=0.12)
            nodes.append(VGroup(ico, v, s))

        a1 = Arrow(np.array([xs[0]+0.52, 0.1, 0]), np.array([xs[1]-0.52, 0.1, 0]),
                   buff=0, stroke_width=2.5, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        a2 = Arrow(np.array([xs[1]+0.52, 0.1, 0]), np.array([xs[2]-0.52, 0.1, 0]),
                   buff=0, stroke_width=2.5, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)

        arc = CurvedArrow(np.array([xs[0]+0.1, 0.85, 0]), np.array([xs[2]-0.1, 0.85, 0]),
                          angle=-PI / 4, color=RED_MAIN, stroke_width=2.5)
        cross = Text("x", font=FONT, font_size=22, color=RED_MAIN, weight=BOLD).move_to(np.array([0.0, 1.45, 0]))

        return VGroup(*nodes, a1, a2, arc, cross)
