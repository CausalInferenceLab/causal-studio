from manim import *
import numpy as np

ICON = "/Users/jhkim/Desktop/personal_study/causal/causal-studio/videos/assets/tabler-icons/icons/outline"

SEVERE = "#b07cff"
MILD = "#39d98a"


class PropensityScore(Scene):
    """Scene 04 (EN). Same animations, English text, resynced.
    timings: build/audio/04_propensity_score_en.timings.json (total 88.18s, 19 chunks)
    """

    def construct(self):
        self.camera.background_color = "#0a0a0a"
        self.t = 0.0

        def go_to(target_time):
            dt = target_time - self.t
            if dt > 0:
                self.wait(dt)
                self.t += dt

        def play_at(target_time, *anims, run_time=0.5):
            go_to(target_time)
            self.play(*anims, run_time=run_time)
            self.t += run_time

        def icon(name, color, height=1.0):
            m = SVGMobject(f"{ICON}/{name}.svg")
            m.set_stroke(color, width=3)
            m.set_fill(color, opacity=0)
            m.scale_to_fit_height(height)
            return m

        # Beat 1 — limits of counting by hand → problem (chunk1~2)
        recap = VGroup(
            VGroup(Text("Severe", font_size=28, color=SEVERE, weight=BOLD),
                   MathTex(r"\tfrac{5}{6}", color=SEVERE).scale(0.95)).arrange(RIGHT, buff=0.25),
            VGroup(Text("Mild", font_size=28, color=MILD, weight=BOLD),
                   MathTex(r"\tfrac{2}{4}", color=MILD).scale(0.95)).arrange(RIGHT, buff=0.25),
        ).arrange(RIGHT, buff=1.2).move_to(UP * 0.3)
        recap_lbl = Text("Probabilities counted by hand", font_size=26, color=GRAY_B, weight=BOLD).next_to(recap, UP, buff=0.5)
        problem = Text("But there's a problem.", font_size=40, color=YELLOW, weight=BOLD).move_to(DOWN * 1.6)

        play_at(0.4, FadeIn(recap_lbl), FadeIn(recap), run_time=0.5)          # chunk1
        play_at(6.1, FadeIn(problem, shift=UP * 0.1), run_time=0.5)           # chunk2
        play_at(7.3, FadeOut(recap_lbl, recap, problem), run_time=0.3)

        # Beat 2 — many variables in reality (chunk3~5)
        def var_icon(name, label, color):
            ic = icon(name, color, height=0.95)
            lb = Text(label, font_size=24, color=color, weight=BOLD)
            return VGroup(ic, lb).arrange(DOWN, buff=0.25)

        v1 = var_icon("gender-bigender", "Sex", BLUE_B)
        v2 = var_icon("calendar", "Age", TEAL_B)
        v3 = var_icon("weight", "Weight", GOLD_B)
        v4 = var_icon("stethoscope", "Conditions", RED_B)
        vars_row = VGroup(v1, v2, v3, v4).arrange(RIGHT, buff=1.0).move_to(UP * 0.3)
        hard = Text("Too many confounders to count by hand", font_size=30, color=GRAY_A, weight=BOLD).move_to(DOWN * 2.2)

        play_at(7.9, LaggedStartMap(FadeIn, vars_row, lag_ratio=0.25), run_time=1.6)  # chunk3
        play_at(13.1, FadeIn(hard, shift=UP * 0.1), run_time=0.5)             # chunk4
        play_at(17.4, FadeOut(vars_row, hard), run_time=0.3)                  # chunk5

        # Beat 3 — propensity score: e(X) first, name after (chunk6~7)
        ps_title = Text("Propensity score", font_size=44, color=ORANGE, weight=BOLD).move_to(UP * 1.3)
        ps_eq = MathTex(r"e(X) = P(\,T=1 \mid X\,)", color=WHITE).scale(1.0).move_to(UP * 0.1)
        ps_gloss = Text("Probability of taking medicine, given patient info", font_size=28, color=GRAY_A, weight=BOLD).move_to(DOWN * 1.1)

        play_at(20.3, Write(ps_eq), run_time=0.7)                            # chunk6
        play_at(22, FadeIn(ps_gloss), run_time=0.5)
        play_at(24, FadeIn(ps_title, shift=DOWN * 0.1), run_time=0.5)
        play_at(26.5, Indicate(ps_eq, color=ORANGE, scale_factor=1.1), run_time=0.7)  # chunk7
        play_at(29.1, FadeOut(ps_title, ps_eq, ps_gloss), run_time=0.3)

        # Beat 4 — model flow + sigmoid (chunk8~13)
        in_node = Text("Patient info", font_size=26, color=GRAY_A, weight=BOLD).move_to(LEFT * 4.3)
        box_rect = RoundedRectangle(width=3.4, height=1.3, corner_radius=0.2, stroke_color=ORANGE, stroke_width=2.5)
        out_node = Text("Prob. of medicine", font_size=26, color=WHITE, weight=BOLD).move_to(RIGHT * 4.3)
        flow = VGroup(in_node, box_rect, out_node).arrange(RIGHT, buff=0.9).move_to(UP * 2.2)
        ar1 = Arrow(in_node.get_right(), box_rect.get_left(), color=GRAY_B, stroke_width=4, buff=0.2)
        ar2 = Arrow(box_rect.get_right(), out_node.get_left(), color=GRAY_B, stroke_width=4, buff=0.2)
        box_q = Text("?", font_size=40, color=GRAY_B, weight=BOLD).move_to(box_rect.get_center())
        box_lbl = Text("Logistic regression", font_size=24, color=ORANGE, weight=BOLD).move_to(box_rect.get_center())

        play_at(29.6, FadeIn(in_node, out_node), Create(box_rect), FadeIn(box_q),
                GrowArrow(ar1), GrowArrow(ar2), run_time=0.7)                  # chunk8
        play_at(34.9, ReplacementTransform(box_q, box_lbl), run_time=0.6)     # chunk9

        ax = Axes(x_range=[-6, 6, 3], y_range=[0, 1, 0.5], x_length=5.2, y_length=2.3,
                  axis_config={"include_tip": False, "stroke_color": GRAY_B},
                  y_axis_config={"include_numbers": True, "font_size": 20}).move_to(DOWN * 1.0)
        sig = ax.plot(lambda x: 1 / (1 + np.exp(-x)), x_range=[-6, 6], color=ORANGE, stroke_width=4)
        line0 = DashedLine(ax.c2p(-6, 0), ax.c2p(6, 0), color=GRAY_D, stroke_width=1.5)
        line1 = DashedLine(ax.c2p(-6, 1), ax.c2p(6, 1), color=GRAY_D, stroke_width=1.5)
        sig_name = Text("sigmoid", font_size=26, color=ORANGE, weight=BOLD, slant=ITALIC).next_to(ax, UP, buff=0.12)

        play_at(37.2, Create(ax), FadeIn(line0, line1, sig_name), run_time=0.8)  # chunk10
        play_at(38.4, Create(sig), run_time=2.0)

        lo_dot = Dot(ax.c2p(-5, 1 / (1 + np.exp(5))), color=BLUE_B, radius=0.09)
        hi_dot = Dot(ax.c2p(5, 1 / (1 + np.exp(-5))), color=GREEN_B, radius=0.09)
        lo_lbl = Text("small input → 0", font_size=16, color=BLUE_B, weight=BOLD).move_to(ax.c2p(-3.0, 0)).shift(DOWN * 0.50)
        hi_lbl = Text("large input → 1", font_size=16, color=GREEN_B, weight=BOLD).move_to(ax.c2p(3.0, 1)).shift(UP * 0.40)
        play_at(43.9, FadeIn(lo_dot), Flash(lo_dot, color=BLUE_B), FadeIn(lo_lbl, shift=UP * 0.08), run_time=0.7)  # chunk11
        play_at(45.9, FadeIn(hi_dot), Flash(hi_dot, color=GREEN_B), FadeIn(hi_lbl, shift=DOWN * 0.08), run_time=0.7)

        out_lbl = Text("Always between 0 and 1 → a probability", font_size=26, color=GREEN_B, weight=BOLD).to_edge(DOWN, buff=0.4)
        play_at(49.4, FadeIn(out_lbl, shift=UP * 0.1), run_time=0.5)          # chunk12
        ehat = MathTex(r"\hat{e}(X)", color=ORANGE).scale(1.0).next_to(out_node, DOWN, buff=0.25)
        ehat_lbl = Text("Estimated propensity score", font_size=22, color=GRAY_A, weight=BOLD).next_to(ehat, DOWN, buff=0.12)
        play_at(55.7, FadeIn(ehat), FadeIn(ehat_lbl), run_time=0.6)           # chunk13
        play_at(59.4, FadeOut(in_node, out_node, box_rect, box_lbl, ar1, ar2, ax, sig, line0, line1,
                               sig_name, lo_dot, hi_dot, lo_lbl, hi_lbl, out_lbl, ehat, ehat_lbl), run_time=0.4)

        # Beat 5 — IPW with estimated score (chunk14)
        big_box = RoundedRectangle(width=9.0, height=2.6, corner_radius=0.25,
                                   stroke_color=GRAY_B, stroke_width=2, fill_opacity=0).move_to(UP * 0.1)
        ipw_eq = MathTex(r"\hat{w} = \frac{T}{\hat{e}(X)} + \frac{1-T}{1-\hat{e}(X)}", color=WHITE).scale(1.15).move_to(UP * 0.1)
        same = Text("The rest is just like before", font_size=28, color=GRAY_A, weight=BOLD).next_to(big_box, UP, buff=0.4)

        play_at(60.5, FadeIn(same), Create(big_box), run_time=0.6)           # chunk14
        play_at(62.4, Write(ipw_eq), run_time=1.0)
        play_at(66.6, FadeOut(same, big_box, ipw_eq), run_time=0.35)

        # Beat 6 — when the model is wrong: missing age (chunk15~18)
        warn = Text("Only works if the score is estimated well", font_size=30, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.55)
        reg = MathTex(r"\text{logit}\,\hat{e}(X) = \beta_0 + \beta_1 x_1 + \beta_2 x_2", color=WHITE).scale(0.88).move_to(UP * 1.6)
        reg_legend = Text("x₁ : sex    x₂ : symptoms", font_size=22, color=GRAY_A, weight=BOLD).next_to(reg, DOWN, buff=0.25)
        miss_expr = VGroup(
            MathTex(r"x_3", color=RED_B).scale(0.76),
            Text("= age", font_size=22, color=RED_B, weight=BOLD),
        ).arrange(RIGHT, buff=0.08)
        miss = VGroup(
            Text("Missing variable", font_size=22, color=RED_B, weight=BOLD),
            miss_expr,
        ).arrange(RIGHT, buff=0.25).next_to(reg_legend, DOWN, buff=0.28)
        miss_cross = Cross(miss_expr, stroke_color=RED, stroke_width=4)

        ax2 = Axes(x_range=[0, 6, 2], y_range=[0, 6, 2], x_length=4.6, y_length=2.55,
                   axis_config={"include_tip": False, "stroke_color": GRAY_B, "include_numbers": False}).move_to(DOWN * 1.55)
        pts_x = [0.5, 1.3, 2.1, 3.0, 3.9, 4.7, 5.4]
        pts_y = [1.0, 3.0, 5.0, 5.3, 4.6, 2.4, 1.0]
        dots = VGroup(*[Dot(ax2.c2p(x, y), color=TEAL_B, radius=0.08) for x, y in zip(pts_x, pts_y)])
        bad_line = Line(ax2.c2p(0, 1.3), ax2.c2p(6, 4.6), color=RED_B, stroke_width=3)
        graph_lbl = Text("Misses the true pattern", font_size=24, color=RED_B, weight=BOLD).next_to(ax2, RIGHT, buff=0.3)

        play_at(67.8, FadeIn(warn), run_time=0.4)                            # chunk15~16
        play_at(74.1, FadeIn(reg), FadeIn(reg_legend), run_time=0.5)         # chunk17
        play_at(77.5, FadeIn(miss), Create(miss_cross), run_time=0.7)
        play_at(80.5, Create(ax2), LaggedStartMap(FadeIn, dots, lag_ratio=0.1), run_time=0.9)
        play_at(86.1, Create(bad_line), FadeIn(graph_lbl), run_time=0.7)     # chunk18

        # Beat 7 — closing: keep the screen, just emphasize (chunk19)
        play_at(91.8, Indicate(VGroup(ax2, dots, bad_line, graph_lbl), color=RED_B, scale_factor=1.05), run_time=1.0)
        play_at(93.8, Indicate(miss, color=RED_B, scale_factor=1.25), run_time=0.9)

        go_to(96.5)
