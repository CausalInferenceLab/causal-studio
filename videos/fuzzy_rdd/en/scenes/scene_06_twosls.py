from manim import *

from videos.fuzzy_rdd.shared.common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
)


class Scene06TwoSLS(Scene):
    """
    Scene 06: twosls (English port of Scene06TwoSLS)
    스크립트: narration/06_twosls.txt
    타이밍: build/audio/06_twosls.timings.json (총 75.96s, 8 chunks)

    chunk3/4 내부의 NUMDEN/NOCL, LINE1/LINE2 체크포인트는 한국어 버전에서도
    "문장 길이 비율" 추정값이었으므로, 구 청크 내 비율을 새 청크 길이에 그대로
    곱해 재추정했다: NUMDEN≈13.74, NOCL≈19.98 (chunk3), LINE1≈30.43, LINE2≈34.47 (chunk4).
    나머지 체크포인트는 전부 청크 경계와 정확히 일치.

    chunk1:  0.00 ->  3.02  question: how do we compute the Wald Estimator with real data?
    chunk2:  3.02 -> 11.19  Wald formula (center) + numerator/denominator change labels
    chunk3: 11.19 -> 27.82  dashed divider + right "How to Compute It?": num/denom separately -> ratio -> point estimate, red "no CI"
    chunk4: 27.82 -> 37.52  "2SLS": 1) same point estimate (dot) 2) confidence interval (bar, dashed connector to dot)
    chunk5: 37.52 -> 45.42  note: 2SLS is a general IV method (general Z->D->Y chain)
    chunk6: 45.42 -> 52.24  our Fuzzy RDD: Z=eligibility(IV), D=treatment(endogenous) labels
    chunk7: 52.24 -> 65.20  stage 1: Z->D-hat (stage card)
    chunk8: 65.20 -> 75.96  stage 2: D-hat->Y, beta-hat-1=LATE (stage card, last, WAIT_TAIL)
    """

    def construct(self):
        import numpy as np

        # ── Beat 1 (chunk1, 0->3.02) question ─────────────────────
        question = Text("How do we compute the Wald Estimator with real data?",
                        font=FONT, font_size=26, color=GOLD_MAIN,
                        t2c={"Wald Estimator": TEAL_MAIN}).move_to(ORIGIN)
        self.play(FadeIn(question, shift=UP * 0.1, run_time=0.6))
        self.wait(3.0186 - 0.6)

        # ── Beat 2 (chunk2, 3.02->11.19) Wald formula + num/denom labels ──
        wald_title = Text("Wald Estimator", font=FONT, font_size=24, color=TEAL_MAIN).move_to(UP * 2.6)
        eq_main = MathTex(r"\hat{\tau}", r"=", r"\frac{\Delta Y}{\Delta D}", font_size=80)
        eq_main[0].set_color(TEAL_MAIN)
        eq_main[2].set_color(TEAL_MAIN)
        eq_main.move_to(UP * 0.2)
        num_lbl = Text("change in outcome", font=FONT, font_size=18, color=GRAY_MID).next_to(eq_main, RIGHT, buff=1.3).shift(UP * 0.65)
        den_lbl = Text("change in treatment prob.", font=FONT, font_size=18, color=GRAY_MID).next_to(eq_main, RIGHT, buff=1.3).shift(DOWN * 0.65)
        arr_num = Arrow(num_lbl.get_left(), eq_main[2].get_top() + RIGHT * 0.25, buff=0.12,
                        stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        arr_den = Arrow(den_lbl.get_left(), eq_main[2].get_bottom() + RIGHT * 0.25, buff=0.12,
                        stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        numden = VGroup(num_lbl, den_lbl, arr_num, arr_den)
        self.play(FadeOut(question, run_time=0.4),
                  FadeIn(wald_title, shift=UP * 0.1, run_time=0.5),
                  FadeIn(eq_main, shift=UP * 0.2, run_time=0.7))
        self.play(FadeIn(numden, run_time=0.5))
        self.wait(11.1920 - 3.0186 - 0.7 - 0.5)

        # ── Beat 3 (chunk3, 11.19->27.82) numerator/denominator -> point estimate / no CI ──
        vx = 3.2
        divider = DashedLine(np.array([-1.8, 2.25, 0]), np.array([-1.8, -2.25, 0]),
                             color=GRAY_MID, stroke_width=1.4, dash_length=0.12)
        rhead = Text("How to Compute It?", font=FONT, font_size=24, color=GOLD_MAIN).move_to(np.array([2.6, 1.95, 0]))
        num = VGroup(Text("numerator", font=FONT, font_size=15, color=GRAY_MID),
                     MathTex(r"\Delta Y", font_size=30).set_color(TEAL_MAIN)).arrange(RIGHT, buff=0.18).move_to(np.array([0.45, 0.95, 0]))
        den = VGroup(Text("denominator", font=FONT, font_size=15, color=GRAY_MID),
                     MathTex(r"\Delta D", font_size=30).set_color(GOLD_MAIN)).arrange(RIGHT, buff=0.18).move_to(np.array([0.45, -0.25, 0]))
        fraction_template = TexTemplate()
        fraction_template.add_to_preamble(r"\usepackage{xcolor}")
        numerator = rf"\textcolor[HTML]{{{TEAL_MAIN[1:]}}}{{\Delta Y}}"
        denominator = rf"\textcolor[HTML]{{{GOLD_MAIN[1:]}}}{{\Delta D}}"
        frac = MathTex(rf"\frac{{{numerator}}}{{{denominator}}}", font_size=46,
                       tex_template=fraction_template).move_to(np.array([2.15, 0.35, 0]))
        a_n = Arrow(num.get_right(), frac.get_left() + UP * 0.20, buff=0.16,
                    stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        a_d = Arrow(den.get_right(), frac.get_left() + DOWN * 0.20, buff=0.16,
                    stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        pt_dot = Dot(np.array([4.0, 0.35, 0]), radius=0.12, color=TEAL_MAIN)
        a_eq = Arrow(frac.get_right(), pt_dot.get_left(), buff=0.18,
                     stroke_width=2.0, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        pt_label = Text("point estimate", font=FONT, font_size=16, color=TEAL_MAIN).next_to(pt_dot, UP, buff=0.22)
        compute_grp = VGroup(num, den, frac, a_n, a_d, a_eq, pt_label)
        nocl = Text("but we can't get a confidence interval", font=FONT, font_size=18, color=RED_MAIN).move_to(np.array([2.3, -1.55, 0]))
        self.play(
            FadeOut(numden, run_time=0.3),
            wald_title.animate.move_to(np.array([-4.1, 1.5, 0])),
            eq_main.animate.scale(0.72).move_to(np.array([-4.1, 0.1, 0])),
            Create(divider, run_time=0.6),
            FadeIn(rhead, run_time=0.5),
            run_time=0.7,
        )
        self.wait(13.744 - 11.1920 - 0.7)
        self.play(FadeIn(num, run_time=0.45), FadeIn(den, run_time=0.45))
        self.play(GrowArrow(a_n, run_time=0.4), GrowArrow(a_d, run_time=0.4), FadeIn(frac, run_time=0.45))
        self.play(GrowArrow(a_eq, run_time=0.4), FadeIn(pt_dot, run_time=0.4), FadeIn(pt_label, run_time=0.4))
        self.wait(19.976 - 13.744 - 0.45 - 0.45 - 0.4)
        self.play(FadeIn(nocl, run_time=0.5))
        self.wait(27.8175 - 19.976 - 0.5)

        # ── Beat 4 (chunk4, 27.82->37.52) 2SLS solves both ────────
        T4_END = 37.5234
        ans_2sls = Text('"2SLS"', font=FONT, font_size=36, weight=BOLD, color=GOLD_MAIN).move_to(np.array([2.55, 1.15, 0]))
        sub_2sls = Text("(Two-Stage Least Squares)", font=FONT, font_size=15, color=GRAY_MID).next_to(ans_2sls, DOWN, buff=0.14)
        line1 = Text("1)  Same as the numerator/denominator ratio", font=FONT, font_size=18, color=WHITE,
                     t2c={"numerator/denominator ratio": TEAL_MAIN}).move_to(np.array([-0.85, -0.55, 0]), aligned_edge=LEFT)
        line2 = Text("2)  Also gives a confidence interval", font=FONT, font_size=19, color=WHITE,
                     t2c={"confidence interval": GOLD_MAIN}).move_to(np.array([-0.85, -1.85, 0]), aligned_edge=LEFT)
        anchor_x = max(line1.get_right()[0], line2.get_right()[0]) + 1.0
        dotpos = np.array([anchor_x, line1.get_center()[1], 0])
        est_dot = Dot(dotpos, radius=0.11, color=TEAL_MAIN)
        dot_cap = Text("point estimate", font=FONT, font_size=14, color=TEAL_MAIN).move_to(dotpos + UP * 0.4)
        arr1 = Arrow(line1.get_right() + RIGHT * 0.1, dotpos + LEFT * 0.22, buff=0.08,
                     stroke_width=2.0, color=TEAL_MAIN, max_tip_length_to_length_ratio=0.28)
        ci_cy = line2.get_center()[1]
        ci_half = 0.72
        ci_bar = Line(np.array([anchor_x - ci_half, ci_cy, 0]), np.array([anchor_x + ci_half, ci_cy, 0]),
                      color=GOLD_MAIN, stroke_width=4)
        ci_capL = Line(np.array([anchor_x - ci_half, ci_cy - 0.14, 0]), np.array([anchor_x - ci_half, ci_cy + 0.14, 0]),
                       color=GOLD_MAIN, stroke_width=4)
        ci_capR = Line(np.array([anchor_x + ci_half, ci_cy - 0.14, 0]), np.array([anchor_x + ci_half, ci_cy + 0.14, 0]),
                       color=GOLD_MAIN, stroke_width=4)
        ci_center = Dot(np.array([anchor_x, ci_cy, 0]), radius=0.08, color=TEAL_MAIN)
        connector = DashedLine(est_dot.get_bottom() + DOWN * 0.02, np.array([anchor_x, ci_cy + 0.18, 0]),
                               color=TEAL_MAIN, stroke_width=1.6, dash_length=0.08)
        ci_fig = VGroup(ci_bar, ci_capL, ci_capR, ci_center)
        self.play(
            FadeOut(compute_grp, run_time=0.45), FadeOut(pt_dot, run_time=0.45), FadeOut(nocl, run_time=0.45),
            FadeIn(ans_2sls, scale=1.1, run_time=0.5), FadeIn(sub_2sls, run_time=0.5),
        )
        self.wait(30.427 - 27.8175 - 0.5)
        self.play(FadeIn(line1, run_time=0.5), FadeIn(est_dot, run_time=0.5), FadeIn(dot_cap, run_time=0.5))
        self.play(GrowArrow(arr1, run_time=0.4))
        self.wait(34.466 - 30.427 - 0.5 - 0.4)
        self.play(FadeIn(line2, run_time=0.5), Create(connector, run_time=0.5), Create(ci_fig, run_time=0.6))
        compare_grp = VGroup(wald_title, eq_main, divider, rhead, ans_2sls, sub_2sls,
                             est_dot, dot_cap, line1, arr1, line2, connector, ci_fig)
        self.wait(T4_END - 34.466 - 0.6)

        # ── Beat 5 (chunk5, 37.52->45.42) note: 2SLS is a general IV method ──
        nZ = MathTex(r"Z", font_size=48).set_color(GOLD_MAIN)
        nD = MathTex(r"D", font_size=48).set_color(TEAL_MAIN)
        nY = MathTex(r"Y", font_size=48).set_color(WHITE)
        chain = VGroup(nZ, nD, nY).arrange(RIGHT, buff=2.6).move_to(UP * 0.1)
        ar1 = Arrow(nZ.get_right(), nD.get_left(), buff=0.25, stroke_width=2.5,
                    color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        ar2 = Arrow(nD.get_right(), nY.get_left(), buff=0.25, stroke_width=2.5,
                    color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        roleZ = Text("instrument", font=FONT, font_size=16, color=GOLD_MAIN).next_to(nZ, DOWN, buff=0.3)
        roleD = Text("endogenous var.", font=FONT, font_size=16, color=TEAL_MAIN).next_to(nD, DOWN, buff=0.3)
        roleY = Text("outcome", font=FONT, font_size=16, color=WHITE).next_to(nY, DOWN, buff=0.3)
        chain_grp = VGroup(chain, ar1, ar2, roleZ, roleD, roleY)
        ref_title = Text("Note: 2SLS is a general IV estimation method", font=FONT, font_size=22, color=GRAY_MID).move_to(UP * 2.6)
        ref_cap = Text("Not specific to Fuzzy RDD", font=FONT, font_size=18, color=WHITE).move_to(DOWN * 2.0)
        self.play(FadeOut(compare_grp, run_time=0.4),
                  FadeIn(ref_title, run_time=0.5),
                  FadeIn(chain_grp, shift=UP * 0.1, run_time=0.6),
                  FadeIn(ref_cap, run_time=0.5))
        self.wait(45.4182 - 37.5234 - 0.6)

        # ── Beat 6 (chunk6, 45.42->52.24) our Fuzzy RDD: Z=eligibility, D=treatment ──
        nameZ = Text("Eligibility", font=FONT, font_size=16, color=GOLD_MAIN).next_to(nZ, UP, buff=0.3)
        nameD = Text("Treatment", font=FONT, font_size=16, color=TEAL_MAIN).next_to(nD, UP, buff=0.3)
        fuzzy_title = Text("In our Fuzzy RDD setting", font=FONT, font_size=24, color=TEAL_MAIN).move_to(UP * 2.6)
        fuzzy_cap = Text("Eligibility = instrument,   Treatment = endogenous variable", font=FONT, font_size=18, color=WHITE).move_to(DOWN * 2.0)
        self.play(FadeOut(ref_title, run_time=0.3), FadeIn(fuzzy_title, run_time=0.5),
                  FadeIn(nameZ, shift=DOWN * 0.05, run_time=0.5), FadeIn(nameD, shift=DOWN * 0.05, run_time=0.5),
                  FadeOut(ref_cap, run_time=0.3), FadeIn(fuzzy_cap, run_time=0.5))
        self.wait(52.2449 - 45.4182 - 0.5)

        # ── Beat 7 (chunk7, 52.24->65.20) stage 1 ─────────────────
        def _stage(label, eq_parts, accent, eq_color):
            box = RoundedRectangle(width=6.8, height=1.35, corner_radius=0.14,
                                   stroke_color=accent, stroke_width=2.6, fill_opacity=0)
            lab = Text(label, font=FONT, font_size=22, color=accent)
            eq = MathTex(*eq_parts, font_size=40).set_color(eq_color)
            VGroup(lab, eq).arrange(RIGHT, buff=0.5).move_to(box.get_center())
            return box, lab, eq

        s1_box, s1_lab, s1_eq = _stage(
            "Stage 1", [r"\hat{D}_i", r"=", r"\hat{\alpha}_0 +", r"\hat{\alpha}_1 Z_i"], TEAL_MAIN, WHITE)
        s1_eq[0].set_color(TEAL_MAIN)
        stage1 = VGroup(s1_box, s1_lab, s1_eq).move_to(UP * 2.0)
        s2d_box, s2d_lab, s2d_eq = _stage(
            "Stage 2", [r"Y_i =", r"\hat{\beta}_0 +", r"\hat{\beta}_1", r"\hat{D}_i"], GRAY_MID, GRAY_MID)
        stage2_dim = VGroup(s2d_box, s2d_lab, s2d_eq).move_to(DOWN * 0.1).set_opacity(0.4)
        flow_arrow = Arrow(stage1.get_bottom(), stage2_dim.get_top(), buff=0.12,
                           stroke_width=2.8, color=TEAL_MAIN, max_tip_length_to_length_ratio=0.28)
        flow_lbl = MathTex(r"\hat{D}", font_size=30).set_color(TEAL_MAIN).next_to(flow_arrow, RIGHT, buff=0.2)
        cap1 = VGroup(
            Text("Predict only the exogenous part of treatment using Z", font=FONT, font_size=18, color=TEAL_MAIN),
            MathTex(r"\rightarrow \hat{D}", font_size=26).set_color(TEAL_MAIN),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 1.75)
        self.play(
            FadeOut(VGroup(chain_grp, nameZ, nameD, fuzzy_title, fuzzy_cap), run_time=0.4),
            FadeIn(stage1, shift=UP * 0.1, run_time=0.5),
            FadeIn(stage2_dim, run_time=0.5),
            GrowArrow(flow_arrow, run_time=0.5),
            FadeIn(flow_lbl, run_time=0.4),
        )
        self.play(FadeIn(cap1, run_time=0.4))
        self.wait(65.2016 - 52.2449 - 0.5 - 0.4)

        # ── Beat 8 (chunk8, 65.20->75.96) stage 2 (last, WAIT_TAIL) ──
        s2a_box, s2a_lab, s2a_eq = _stage(
            "Stage 2", [r"Y_i =", r"\hat{\beta}_0 +", r"\hat{\beta}_1", r"\hat{D}_i"], GOLD_MAIN, WHITE)
        stage2_act = VGroup(s2a_box, s2a_lab, s2a_eq).move_to(DOWN * 0.1)
        s2a_eq[2].set_color(GOLD_MAIN)
        s2a_eq[3].set_color(TEAL_MAIN)
        beta_box = SurroundingRectangle(s2a_eq[2], color=GOLD_MAIN, buff=0.06,
                                        stroke_width=2.2, corner_radius=0.04)
        cap2 = MathTex(r"\hat{\beta}_1 = \text{LATE}", font_size=34).set_color(GOLD_MAIN).move_to(DOWN * 1.75)
        self.play(
            stage1.animate.set_opacity(0.4),
            FadeOut(stage2_dim, run_time=0.3),
            FadeIn(stage2_act, run_time=0.5),
            FadeOut(cap1, run_time=0.3),
            FadeIn(cap2, run_time=0.5),
        )
        self.play(Create(beta_box, run_time=0.4))
        # WAIT_TAIL = (75.958 + 0.4) - 65.202 - 0.5 - 0.4 = 10.256
        self.wait(10.256)
