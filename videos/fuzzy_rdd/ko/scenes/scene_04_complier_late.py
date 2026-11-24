from manim import *

from videos.fuzzy_rdd.shared.common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
)


class Scene04ComplierLate(Scene):
    """
    Scene 04: complier_late  (ipynb §3 "추정된 효과는 무엇을 의미하는가")
    스크립트: narration/04_complier_late.txt
    타이밍: build/audio/04_complier_late.timings.json (총 55.58s, 7 chunks)

    직전 Scene(03_wald) 마지막 문장: "...왈드 추정량이라고 합니다."
    현재 Scene 첫 문장: "방금 우리는 왈드 추정량으로 처치 효과를 계산했습니다..."

    Beat1 chunk1-2 ( 0.00~20.81)  맥락 설명 + "누구에 대한 효과?" 질문
    Beat2 chunk3-4 (20.81~36.78)  행동이 바뀐 사람만 잡힌다
    Beat3 chunk5-7 (36.78~63.53)  네 유형 표 (항상/절대 제외 → 위반자 배제)
    Beat4 chunk8   (63.53~75.10)  순응자 = 추정 대상, LATE (WAIT_TAIL)
    """

    def construct(self):
        # ── Beat 1 (chunk1) 맥락 설명 ─────────────────────────
        ctx = VGroup(
            Text("Wald 추정량으로 처치 효과를 계산했습니다.", font=FONT, font_size=26, color=WHITE),
            VGroup(
                Text("자격이 생겨도 일부는 처치를 받을 수 없고,", font=FONT, font_size=22, color=GRAY_MID),
                Text("자격이 없더라도 일부는 처치를 받을 수 있습니다.", font=FONT, font_size=22, color=GRAY_MID),
            ).arrange(DOWN, buff=0.2),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        self.play(FadeIn(ctx, shift=UP * 0.2), run_time=0.7)
        self.wait(12.121 - 0.7)

        # ── Beat 1 (chunk2) 질문 ───────────────────────────────
        q = VGroup(
            Text("그 효과는", font=FONT, font_size=30, color=WHITE),
            Text("'누구'에 대한 효과일까?", font=FONT, font_size=38, color=TEAL_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.play(FadeOut(ctx, run_time=0.4), FadeIn(q, shift=UP * 0.15, run_time=0.6))
        self.wait(20.944 - 12.121 - 0.4 - 0.6)

        # ── Beat 2 (chunk3) 잡히지 않는 두 케이스 ───────────────
        b2 = VGroup(
            Text("Case 1.  수능 370점 미만이어도 장학금 받는 학생", font=FONT, font_size=22, color=GRAY_MID),
            Text("Case 2.  수능 370점 이상이어도 장학금 못 받는 학생", font=FONT, font_size=22, color=GRAY_MID),
            Text("→ Wald 추정량에 잡히지 않음", font=FONT, font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.5)
        self.play(FadeOut(q, run_time=0.4), FadeIn(b2, shift=UP * 0.15, run_time=0.7))
        self.wait(30.824 - 20.944 - 0.4 - 0.7)

        # ── Beat 2 (chunk4) Wald 식 + 반영 대상 ─────────────────
        formula_wald = MathTex(r"\hat{\tau}_{Fuzzy} = \frac{\Delta Y}{\Delta D}", font_size=52).move_to(UP * 0.5)
        b2c = Text("오직 '자격 때문에 행동이 바뀐 사람'만 반영", font=FONT, font_size=24, color=GOLD_MAIN)
        b2c.next_to(formula_wald, DOWN, buff=0.7)
        self.play(FadeOut(b2, run_time=0.4), FadeIn(VGroup(formula_wald, b2c), shift=UP * 0.1, run_time=0.6))
        self.wait(45.592 - 30.824 - 0.6)

        # ── Beat 3 (chunk5) 네 유형 표 ─────────────────────────
        self.play(FadeOut(VGroup(formula_wald, b2c)), run_time=0.5)
        header = self._type_row("유형", "자격 X", "자격 O", 2.05, GRAY_MID, header=True)
        r_comp = self._type_row("순응자 (Complier)",          "처치 X", "처치 O",  1.15, WHITE)
        r_at   = self._type_row("항상 수혜자 (Always-taker)",  "처치 O", "처치 O",  0.35, WHITE)
        r_nt   = self._type_row("절대 비수혜자 (Never-taker)", "처치 X", "처치 X", -0.45, WHITE)
        r_def  = self._type_row("위반자 (Defier)",             "처치 O", "처치 X", -1.25, WHITE)
        table = VGroup(header, r_comp, r_at, r_nt, r_def)
        hline = Line(LEFT * 4.3, RIGHT * 4.3, color=GRAY_MID, stroke_width=1).move_to(UP * 1.62)
        table_g = VGroup(table, hline).move_to(UP * 0.3)
        cap = Text("자격(Z)에 따라 처치(D)가 어떻게 달라지나", font=FONT, font_size=24, color=WHITE).to_edge(UP, buff=0.7)
        self.play(FadeIn(VGroup(table_g, cap), run_time=0.7))
        self.wait(51.815 - 45.592 - 0.5 - 0.7)

        # chunk6: 항상/절대 수혜자 설명 (하얗게 강조, 나머지 흐리게)
        self.play(r_comp.animate.set_opacity(0.35), r_def.animate.set_opacity(0.35), run_time=0.5)
        self.wait(65.376 - 51.815 - 0.5)

        # chunk6 끝: 항상/절대 dim + 빨간줄, 위반자 복원
        strike_at = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_at.get_center())
        strike_nt = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_nt.get_center())
        self.play(
            r_at.animate.set_opacity(0.35), r_nt.animate.set_opacity(0.35),
            Create(strike_at), Create(strike_nt),
            r_def.animate.set_opacity(1.0),
            run_time=0.5,
        )

        # chunk7: 위반자 설명 (위반자만 하얀글씨, 빨간줄 없음)
        self.wait(72.342 - 65.376 - 0.5)

        # chunk7 끝: 위반자 dim + 빨간줄, 순응자 복원
        strike_def = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_def.get_center())
        self.play(
            r_def.animate.set_opacity(0.35), Create(strike_def),
            r_comp.animate.set_opacity(1.0),
            run_time=0.5,
        )

        # ── Beat 4 (chunk8) 순응자 = LATE ──────────────────────
        box = SurroundingRectangle(r_comp, color=TEAL_MAIN, buff=0.18, corner_radius=0.08, stroke_width=3)
        label_comp = Text("추정 대상 →", font=FONT, font_size=20, color=TEAL_MAIN)
        label_comp.next_to(box, LEFT, buff=0.2)
        cap4 = Text("순응자들에 대한 국소 평균 처치 효과 (LATE)", font=FONT, font_size=22, color=WHITE).to_edge(DOWN, buff=1.5)
        self.play(Create(box), FadeOut(cap, run_time=0.3), FadeIn(cap4, shift=UP * 0.1, run_time=0.6), FadeIn(label_comp, run_time=0.6))
        # WAIT_TAIL = (84.950 + 1.0) - 72.342 - 0.5 - 0.6 = 12.508
        self.wait(12.508)

    def _type_row(self, name, v0, v1, y, name_color, header=False) -> VGroup:
        """네 유형 표 한 행: 이름(좌) + Z=0열 + Z=1열, 고정 x로 정렬."""
        import numpy as np
        fs = 22 if header else 20
        n = Text(name, font=FONT, font_size=fs, color=name_color).move_to(np.array([-4.2, y, 0]), aligned_edge=LEFT)
        c0 = Text(v0, font=FONT, font_size=fs, color=name_color).move_to(np.array([1.4, y, 0]))
        c1 = Text(v1, font=FONT, font_size=fs, color=name_color).move_to(np.array([3.6, y, 0]))
        return VGroup(n, c0, c1)
