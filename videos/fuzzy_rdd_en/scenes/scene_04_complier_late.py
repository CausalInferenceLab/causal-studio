from manim import *

from fuzzy_rdd_en_common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
)


class Scene04ComplierLate(Scene):
    """
    Scene 04: complier_late (English port of Scene04ComplierLate)
    스크립트: src/scripts/04_complier_late.txt
    타이밍: build/audio/04_complier_late.timings.json (총 67.59s, 8 chunks) — 전 체크포인트 청크 경계와 일치.

    한국어 원본의 "자격 X/자격 O", "처치 X/처치 O" 표기(한국어식 X=아니오/O=예)는
    영어에서 같은 의미로 안 읽히므로 "Ineligible/Eligible", "Not treated/Treated"로 바꿨다.

    Beat1 chunk1-2 ( 0.00~15.09)  context + "whose effect is this?" question
    Beat2 chunk3-4 (15.09~36.46)  only behavior-changers are captured
    Beat3 chunk5-7 (36.46~58.00)  four-type table (always/never excluded -> defiers excluded)
    Beat4 chunk8   (58.00~67.59)  compliers = target, LATE (WAIT_TAIL)
    """

    def construct(self):
        # ── Beat 1 (chunk1) context ───────────────────────────────
        ctx = VGroup(
            Text("We just calculated the treatment effect using the Wald estimator.", font=FONT, font_size=26, color=WHITE),
            VGroup(
                Text("But some can't get treated even when eligible,", font=FONT, font_size=22, color=GRAY_MID),
                Text("and some get treated even without eligibility.", font=FONT, font_size=22, color=GRAY_MID),
            ).arrange(DOWN, buff=0.2),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        self.play(FadeIn(ctx, shift=UP * 0.2), run_time=0.7)
        self.wait(9.2415 - 0.7)

        # ── Beat 1 (chunk2) question ───────────────────────────────
        q = VGroup(
            Text("So whose effect", font=FONT, font_size=30, color=WHITE),
            Text("did we just calculate?", font=FONT, font_size=38, color=TEAL_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.play(FadeOut(ctx, run_time=0.4), FadeIn(q, shift=UP * 0.15, run_time=0.6))
        self.wait(15.0930 - 9.2415 - 0.4 - 0.6)

        # ── Beat 2 (chunk3) two uncaptured cases ────────────────────
        b2 = VGroup(
            Text("Case 1.  Score below 370, but gets the scholarship", font=FONT, font_size=22, color=GRAY_MID),
            Text("Case 2.  Score at or above 370, but doesn't get it", font=FONT, font_size=22, color=GRAY_MID),
            Text("-> Not captured by the Wald estimator", font=FONT, font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.5)
        self.play(FadeOut(q, run_time=0.4), FadeIn(b2, shift=UP * 0.15, run_time=0.7))
        self.wait(23.3593 - 15.0930 - 0.4 - 0.7)

        # ── Beat 2 (chunk4) Wald formula + who it reflects ──────────
        formula_wald = MathTex(r"\hat{\tau}_{Fuzzy} = \frac{\Delta Y}{\Delta D}", font_size=52).move_to(UP * 0.5)
        b2c = Text("Only reflects people whose behavior changed because of eligibility", font=FONT, font_size=22, color=GOLD_MAIN)
        b2c.next_to(formula_wald, DOWN, buff=0.7)
        self.play(FadeOut(b2, run_time=0.4), FadeIn(VGroup(formula_wald, b2c), shift=UP * 0.1, run_time=0.6))
        self.wait(36.4553 - 23.3593 - 0.6)

        # ── Beat 3 (chunk5) four-type table ──────────────────────────
        self.play(FadeOut(VGroup(formula_wald, b2c)), run_time=0.5)
        header = self._type_row("Type", "Ineligible", "Eligible", 2.05, GRAY_MID, header=True)
        r_comp = self._type_row("Complier",     "Not treated", "Treated",     1.15, WHITE)
        r_at   = self._type_row("Always-taker", "Treated",     "Treated",     0.35, WHITE)
        r_nt   = self._type_row("Never-taker",  "Not treated", "Not treated", -0.45, WHITE)
        r_def  = self._type_row("Defier",       "Treated",     "Not treated", -1.25, WHITE)
        table = VGroup(header, r_comp, r_at, r_nt, r_def)
        hline = Line(LEFT * 4.3, RIGHT * 4.3, color=GRAY_MID, stroke_width=1).move_to(UP * 1.62)
        table_g = VGroup(table, hline).move_to(UP * 0.3)
        cap = Text("How treatment (D) varies with eligibility (Z)", font=FONT, font_size=24, color=WHITE).to_edge(UP, buff=0.7)
        self.play(FadeIn(VGroup(table_g, cap), run_time=0.7))
        self.wait(40.3098 - 36.4553 - 0.5 - 0.7)

        # chunk6: always/never-taker explanation (dim everything else)
        self.play(r_comp.animate.set_opacity(0.35), r_def.animate.set_opacity(0.35), run_time=0.5)
        self.wait(50.8517 - 40.3098 - 0.5)

        # chunk6 end: always/never dim + red strike, defier restored
        strike_at = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_at.get_center())
        strike_nt = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_nt.get_center())
        self.play(
            r_at.animate.set_opacity(0.35), r_nt.animate.set_opacity(0.35),
            Create(strike_at), Create(strike_nt),
            r_def.animate.set_opacity(1.0),
            run_time=0.5,
        )

        # chunk7: defier explanation (only defier white, no strike yet)
        self.wait(58.0034 - 50.8517 - 0.5)

        # chunk7 end: defier dim + red strike, complier restored
        strike_def = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_def.get_center())
        self.play(
            r_def.animate.set_opacity(0.35), Create(strike_def),
            r_comp.animate.set_opacity(1.0),
            run_time=0.5,
        )

        # ── Beat 4 (chunk8) compliers = LATE ─────────────────────────
        box = SurroundingRectangle(r_comp, color=TEAL_MAIN, buff=0.18, corner_radius=0.08, stroke_width=3)
        label_comp = Text("target ->", font=FONT, font_size=20, color=TEAL_MAIN)
        label_comp.next_to(box, LEFT, buff=0.2)
        cap4 = Text("Local average treatment effect on compliers (LATE)", font=FONT, font_size=22, color=WHITE).to_edge(DOWN, buff=1.5)
        self.play(Create(box), FadeOut(cap, run_time=0.3), FadeIn(cap4, shift=UP * 0.1, run_time=0.6), FadeIn(label_comp, run_time=0.6))
        # WAIT_TAIL = (67.587 + 1.0) - 58.003 - 0.5 - 0.6 = 9.484
        self.wait(9.484)

    def _type_row(self, name, v0, v1, y, name_color, header=False) -> VGroup:
        import numpy as np
        fs = 22 if header else 20
        n = Text(name, font=FONT, font_size=fs, color=name_color).move_to(np.array([-4.2, y, 0]), aligned_edge=LEFT)
        c0 = Text(v0, font=FONT, font_size=fs, color=name_color).move_to(np.array([1.4, y, 0]))
        c1 = Text(v1, font=FONT, font_size=fs, color=name_color).move_to(np.array([3.6, y, 0]))
        return VGroup(n, c0, c1)
