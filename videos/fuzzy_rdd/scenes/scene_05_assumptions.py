from manim import *

from fuzzy_rdd_common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
)


class Scene05Assumptions(Scene):
    """
    Scene 05: assumptions  (ipynb §4 "핵심 가정")
    스크립트: src/scripts/05_assumptions.txt
    타이밍: build/audio/05_assumptions.timings.json (총 79.82s, 6 chunks)

    직전 Scene(04_complier_late) 마지막 문장: "...국소 평균 처치 효과인 LATE입니다."
    현재 Scene 첫 문장: "사실 우리가 지렛대로 삼은 자격 지는, 정확히 말하면 도구변수입니다..."

    Beat1 chunk1-2 ( 0.00~13.75)  Z = 도구변수(IV) → 유효 조건 3가지 (좌측 리스트 등장)
    Beat2 chunk3   (13.75~40.31)  관련성: Cov(Z,D)≠0, 분모≠0, F>10
    Beat3 chunk4   (40.31~59.63)  배제 제약: Z→D→Y, 직접 경로 없음
    Beat4 chunk5   (59.63~72.68)  단조성: 위반자 없음, D(Z=1)≥D(Z=0)
    Beat5 chunk6   (72.68~79.64)  3가지 성립 → Wald = LATE (WAIT_TAIL)
    """

    def construct(self):
        import numpy as np
        # ── Beat 1 (chunk1-2) IV → 3조건 리스트 ────────────────
        head = VGroup(
            Text("자격 Z = 도구변수 (IV)", font=FONT, font_size=36, color=TEAL_MAIN),
            Text("Fuzzy RDD는 본질적으로 도구변수 추정 문제", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(head, shift=UP * 0.2), run_time=0.6)
        self.wait(10.263 - 0.6)

        top = Text("유효한 도구변수의 3가지 조건", font=FONT, font_size=24, color=GRAY_MID).to_edge(UP, buff=0.8)
        t1 = Text("1. 관련성", font=FONT, font_size=27, color=GRAY_MID)
        t2 = Text("2. 배제 제약", font=FONT, font_size=27, color=GRAY_MID)
        t3 = Text("3. 단조성", font=FONT, font_size=27, color=GRAY_MID)
        titles = VGroup(t1, t2, t3).arrange(DOWN, buff=0.9, aligned_edge=LEFT).move_to(LEFT * 4.0)
        sep = Line(UP * 1.9, DOWN * 1.9, color=GRAY_MID, stroke_width=1).move_to(LEFT * 1.6)

        self.play(FadeOut(head, run_time=0.4), FadeIn(top, run_time=0.5), FadeIn(titles, shift=RIGHT * 0.1, run_time=0.6), Create(sep, run_time=0.5))
        self.wait(13.746 - 10.263 - 0.4 - 0.6)

        detail_pos = RIGHT * 2.4

        # ── Beat 2 (chunk3) 관련성 ─────────────────────────────
        d1 = VGroup(
            Text("자격이 생기면 처치 확률이 실제로 ↑", font=FONT, font_size=22, color=WHITE),
            MathTex(r"\mathrm{Cov}(Z, D) \neq 0", font_size=34).set_color(TEAL_MAIN),
            Text("= Wald 분모 ≠ 0", font=FONT, font_size=20, color=GRAY_MID),
            Text("F통계량 > 10 → 강한 도구변수", font=FONT, font_size=20, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.4).move_to(detail_pos)
        self.play(t1.animate.set_color(TEAL_MAIN), FadeIn(d1, shift=UP * 0.1, run_time=0.6))
        self.wait(40.310 - 13.746 - 0.6)

        # ── Beat 3 (chunk4) 배제 제약 ──────────────────────────
        diagram = self._iv_diagram_icons()
        d2 = VGroup(
            Text("자격은 오직 처치를 통해서만 결과에 영향", font=FONT, font_size=22, color=WHITE),
            diagram,
            Text("Z → Y 직접 경로는 없어야 함", font=FONT, font_size=20, color=RED_MAIN),
        ).arrange(DOWN, buff=0.45).move_to(detail_pos)
        self.play(t1.animate.set_color(GRAY_MID), t2.animate.set_color(TEAL_MAIN),
                  FadeOut(d1), FadeIn(d2, shift=UP * 0.1), run_time=0.5)
        self.wait(59.629 - 40.310 - 0.5)

        # ── Beat 4 (chunk5) 단조성 ─────────────────────────────
        d3 = VGroup(
            Text("자격이 생기면 거부하는 사람(위반자) 없음", font=FONT, font_size=22, color=WHITE),
            MathTex(r"D_i(Z{=}1) \geq D_i(Z{=}0)", font_size=32).set_color(TEAL_MAIN),
            Text("늘어난 처치 = 전부 순응자", font=FONT, font_size=20, color=GRAY_MID),
        ).arrange(DOWN, buff=0.45).move_to(detail_pos)
        self.play(t2.animate.set_color(GRAY_MID), t3.animate.set_color(TEAL_MAIN),
                  FadeOut(d2), FadeIn(d3, shift=UP * 0.1), run_time=0.5)
        self.wait(72.678 - 59.629 - 0.5)

        # ── Beat 5 (chunk6) 결론 ───────────────────────────────
        concl = VGroup(
            Text("3가지 가정이 성립하면", font=FONT, font_size=24, color=WHITE),
            Text("Wald 추정량 = LATE", font=FONT, font_size=32, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(detail_pos)
        self.play(t3.animate.set_color(GRAY_MID),
                  t1.animate.set_color(TEAL_MAIN), t2.animate.set_color(TEAL_MAIN),
                  FadeOut(d3), FadeIn(concl, shift=UP * 0.1), run_time=0.6)
        self.play(t3.animate.set_color(TEAL_MAIN), run_time=0.3)
        # WAIT_TAIL = (79.821 + 0.5) - 72.678 - 0.6 - 0.3 = 6.743
        self.wait(6.743)

    def _iv_diagram(self) -> VGroup:
        """Z → D → Y 경로 다이어그램 (배제 제약 시각화)."""
        import numpy as np
        def node(lbl, color, x):
            c = Circle(radius=0.32, color=color, stroke_width=2.5, fill_opacity=0).move_to(np.array([x, 0, 0]))
            t = MathTex(lbl, font_size=28).set_color(color).move_to(c.get_center())
            return VGroup(c, t)
        z = node("Z", GOLD_MAIN, -1.7)
        d = node("D", TEAL_MAIN, 0.0)
        y = node("Y", WHITE, 1.7)
        a1 = Arrow(z.get_right(), d.get_left(), buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.25, color=GRAY_MID)
        a2 = Arrow(d.get_right(), y.get_left(), buff=0.1, stroke_width=3, max_tip_length_to_length_ratio=0.25, color=GRAY_MID)
        return VGroup(z, d, y, a1, a2)

    def _iv_diagram_icons(self) -> VGroup:
        """Z→D→Y 아이콘 다이어그램 (임상시험 예시, 배제 제약 시각화)."""
        from pathlib import Path
        import numpy as np

        ICONS = Path(__file__).parent.parent.parent / "assets" / "tabler-icons" / "icons" / "outline"
        xs     = [-2.2,  0.0,  2.2]
        svgs   = ["vaccine-bottle.svg", "pill.svg", "heartbeat.svg"]
        vars_  = ["Z", "D", "Y"]
        colors = [GOLD_MAIN, TEAL_MAIN, WHITE]
        subs   = ["임상 배정", "약 복용", "건강 회복"]

        nodes = []
        for x, svg, var, color, sub in zip(xs, svgs, vars_, colors, subs):
            ico = SVGMobject(str(ICONS / svg), height=0.75)
            ico.set_stroke(color=color, width=2.0, family=True).set_fill(opacity=0)
            ico.move_to(np.array([x, 0.1, 0]))
            v = MathTex(var, font_size=24).set_color(color).next_to(ico, UP, buff=0.12)
            s = Text(sub, font=FONT, font_size=14, color=GRAY_MID).next_to(ico, DOWN, buff=0.12)
            nodes.append(VGroup(ico, v, s))

        a1 = Arrow(np.array([xs[0]+0.52, 0.1, 0]), np.array([xs[1]-0.52, 0.1, 0]),
                   buff=0, stroke_width=2.5, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        a2 = Arrow(np.array([xs[1]+0.52, 0.1, 0]), np.array([xs[2]-0.52, 0.1, 0]),
                   buff=0, stroke_width=2.5, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)

        arc = CurvedArrow(np.array([xs[0]+0.1, 0.85, 0]), np.array([xs[2]-0.1, 0.85, 0]),
                          angle=-PI / 4, color=RED_MAIN, stroke_width=2.5)
        cross = Text("✕", font=FONT, font_size=22, color=RED_MAIN).move_to(np.array([0.0, 1.45, 0]))

        return VGroup(*nodes, a1, a2, arc, cross)
