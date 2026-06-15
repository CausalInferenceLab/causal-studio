from manim import *
import numpy as np

SEVERE = "#b07cff"
MILD = "#39d98a"


class IPWSummary(Scene):
    """Scene 05 (EN). Same animations, English text, resynced.
    timings: build/audio/05_summary_en.timings.json (total 67.25s, 16 chunks)
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

        def dot(color, r=0.13):
            return Circle(radius=r, stroke_color=color, stroke_width=2).set_fill(color, opacity=0.9)

        def people_block(n_sev, n_mild, cols=5, r=0.13, buff=0.12):
            g = VGroup(*[dot(SEVERE, r) for _ in range(n_sev)], *[dot(MILD, r) for _ in range(n_mild)])
            rows = int(np.ceil(len(g) / cols))
            g.arrange_in_grid(rows=rows, cols=cols, buff=buff)
            return g

        def badge(m, txt, color=ORANGE, fs=14):
            return Text(txt, font_size=fs, color=color, weight=BOLD).next_to(m, DOWN, buff=0.04)

        # Beat 1 — problem recap: confounding (chunk1~5)
        head = Text("To recap", font_size=32, color=GRAY_A, weight=BOLD).to_edge(UP, buff=0.55)
        legend = VGroup(
            dot(SEVERE), Text("Severe", font_size=24, color=SEVERE, weight=BOLD),
            dot(MILD), Text("Mild", font_size=24, color=MILD, weight=BOLD),
        ).arrange(RIGHT, buff=0.25).next_to(head, DOWN, buff=0.3)
        ques = Text("Does medicine really speed up recovery?", font_size=32, color=YELLOW, weight=BOLD).move_to(UP * 0.9)
        treat = people_block(5, 2, cols=4).move_to(LEFT * 3.3 + DOWN * 0.3)
        treat_l = Text("Took medicine", font_size=26, color=BLUE_B, weight=BOLD).next_to(treat, UP, buff=0.3)
        ctrl = people_block(1, 2, cols=3).move_to(RIGHT * 3.3 + DOWN * 0.3)
        ctrl_l = Text("No medicine", font_size=26, color=RED_B, weight=BOLD).next_to(ctrl, UP, buff=0.3)
        confound = Text("The confounder (severe/mild) hides the true effect", font_size=28, color=PURPLE_A, weight=BOLD).move_to(DOWN * 2.5)

        play_at(0.4, FadeIn(head), run_time=0.4)
        play_at(2, FadeIn(legend, shift=DOWN * 0.05), FadeIn(ques), run_time=0.5)  # chunk2
        play_at(5.5, FadeOut(ques), FadeIn(treat_l, treat), FadeIn(ctrl_l, ctrl), run_time=0.6)  # chunk3
        treat_box = SurroundingRectangle(VGroup(treat_l, treat), color=BLUE_B, buff=0.2, corner_radius=0.12)
        ctrl_box = SurroundingRectangle(VGroup(ctrl_l, ctrl), color=RED_B, buff=0.2, corner_radius=0.12)
        play_at(10.2, Create(treat_box),
                *[Indicate(treat[i], color=SEVERE, scale_factor=1.4) for i in range(5)], run_time=1.2)  # chunk4
        play_at(12.5, ReplacementTransform(treat_box, ctrl_box),
                *[Indicate(ctrl[i], color=MILD, scale_factor=1.4) for i in range(1, 3)], run_time=1.2)
        play_at(14.3, FadeOut(ctrl_box), run_time=0.3)
        play_at(14.7, FadeIn(confound, shift=UP * 0.1), run_time=0.5)               # chunk5
        play_at(19, FadeOut(head, legend, treat, treat_l, ctrl, ctrl_l, confound), run_time=0.35)

        # Beat 2 — IPW: weights make the two groups equal + true effect (chunk6~8)
        ipw_head = Text("IPW: weights make the two groups equal", font_size=32, color=ORANGE, weight=BOLD).to_edge(UP, buff=0.5)
        bt0 = people_block(5, 2, cols=4, buff=0.32).move_to(LEFT * 3.7 + UP * 0.75)
        bc0 = people_block(1, 2, cols=3, buff=0.32).move_to(RIGHT * 3.7 + UP * 0.75)
        bt_l = Text("Med", font_size=24, color=BLUE_B, weight=BOLD).next_to(bt0, UP, buff=0.25)
        bc_l = Text("No med", font_size=24, color=RED_B, weight=BOLD).next_to(bc0, UP, buff=0.25)
        bc_l.match_y(bt_l)
        bt_badges = VGroup(*[badge(bt0[i], "×1.2") for i in range(5)], *[badge(bt0[i], "×2") for i in range(5, 7)])
        bc_badges = VGroup(badge(bc0[0], "×6", YELLOW, 15), *[badge(bc0[i], "×2") for i in range(1, 3)])
        mul_note = Text("× weight", font_size=26, color=ORANGE, weight=BOLD).move_to(UP * 0.75)
        bt1 = people_block(6, 4, cols=5).move_to(LEFT * 3.7 + UP * 0.75)
        bc1 = people_block(6, 4, cols=5).move_to(RIGHT * 3.7 + UP * 0.75)
        approx = MathTex(r"\approx", color=GREEN_B).scale(1.6).move_to(UP * 0.75)
        UNIT = 0.5
        eff_t = VGroup(Text("Med", font_size=22, color=BLUE_B, weight=BOLD),
                       RoundedRectangle(width=5 * UNIT, height=0.36, corner_radius=0.06, stroke_color=BLUE,
                                        stroke_width=2, fill_color=BLUE, fill_opacity=0.5),
                       Text("5d", font_size=22, color=BLUE_B, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to(DOWN * 1.5 + LEFT * 0.4)
        eff_c = VGroup(Text("No med", font_size=22, color=RED_B, weight=BOLD),
                       RoundedRectangle(width=6 * UNIT, height=0.36, corner_radius=0.06, stroke_color=RED,
                                        stroke_width=2, fill_color=RED, fill_opacity=0.5),
                       Text("6d", font_size=22, color=RED_B, weight=BOLD)).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.3 + LEFT * 0.4)
        eff_lbl = Text("True effect: 1 day faster ✓", font_size=26, color=GREEN_B, weight=BOLD).to_edge(DOWN, buff=0.4)

        play_at(19.3, FadeIn(ipw_head), FadeIn(bt_l, bt0, bc_l, bc0), run_time=0.5)  # chunk6
        play_at(21.7, LaggedStartMap(FadeIn, bt_badges, shift=DOWN * 0.05, lag_ratio=0.05),
                LaggedStartMap(FadeIn, bc_badges, shift=DOWN * 0.05, lag_ratio=0.05), FadeIn(mul_note), run_time=1.0)  # chunk7
        play_at(23.5, FadeOut(bt_badges, bc_badges, mul_note),
                ReplacementTransform(bt0, bt1), ReplacementTransform(bc0, bc1), FadeIn(approx), run_time=1.0)
        play_at(28.2, FadeIn(eff_t, eff_c), run_time=0.5)                            # chunk8
        play_at(30, FadeIn(eff_lbl, shift=UP * 0.1), run_time=0.5)
        play_at(32.55, FadeOut(ipw_head, bt1, bt_l, bc1, bc_l, approx, eff_t, eff_c, eff_lbl), run_time=0.35)

        # Beat 3 — real data: sigmoid figure + per-individual weight (chunk9~13)
        real_head = Text("In real data", font_size=30, color=GRAY_A, weight=BOLD).to_edge(UP, buff=0.5)
        ax = Axes(x_range=[-6, 6, 3], y_range=[0, 1, 1], x_length=4.4, y_length=2.1,
                  axis_config={"include_tip": False, "stroke_color": GRAY_B, "include_numbers": False}).move_to(LEFT * 3.7 + UP * 0.25)
        sig = ax.plot(lambda x: 1 / (1 + np.exp(-x)), x_range=[-6, 6], color=ORANGE, stroke_width=4)
        sig_name = Text("Logistic regression", font_size=24, color=ORANGE, weight=BOLD).next_to(ax, UP, buff=0.15)
        ehat = MathTex(r"\hat{e}(X)", color=ORANGE).scale(0.95).next_to(ax, DOWN, buff=0.3)
        ehat_lbl = Text("Estimated propensity score", font_size=20, color=GRAY_A, weight=BOLD).next_to(ehat, DOWN, buff=0.12)

        play_at(33.45, FadeIn(real_head), Create(ax), Create(sig), FadeIn(sig_name), run_time=0.9)  # chunk9
        play_at(39.1, Write(ehat), FadeIn(ehat_lbl), run_time=0.6)                 # chunk10
        ppl = VGroup(dot(SEVERE), dot(SEVERE), dot(MILD), dot(SEVERE), dot(MILD)).arrange(RIGHT, buff=0.45).move_to(RIGHT * 3.3 + UP * 0.6)
        ppl_badges = VGroup(*[badge(ppl[i], "×w", ORANGE, 16) for i in range(len(ppl))])
        indiv_lbl = Text("A weight for each person", font_size=24, color=ORANGE, weight=BOLD).next_to(ppl, DOWN, buff=0.45)
        play_at(42.9, FadeIn(ppl), LaggedStartMap(FadeIn, ppl_badges, shift=DOWN * 0.05, lag_ratio=0.08),
                FadeIn(indiv_lbl), run_time=1.0)                                     # chunk11
        balanced = Text("Now the groups match ✓", font_size=24, color=GREEN_B, weight=BOLD).next_to(indiv_lbl, DOWN, buff=0.3)
        play_at(47.2, FadeIn(balanced, shift=UP * 0.08), run_time=0.5)             # chunk12
        caution = Text("If the model is wrong, so is IPW → choose inputs carefully", font_size=26, color=YELLOW, weight=BOLD).to_edge(DOWN, buff=0.5)
        play_at(50.3, FadeIn(caution, shift=UP * 0.1), run_time=0.5)               # chunk13
        play_at(55.3, FadeOut(real_head, ax, sig, sig_name, ehat, ehat_lbl, ppl, ppl_badges, indiv_lbl, balanced, caution), run_time=0.4)

        # Beat 4 — why IPW matters: merit / limit (chunk14~16)
        sig_title = Text("Why IPW matters", font_size=44, color=ORANGE, weight=BOLD).to_edge(UP, buff=0.8)
        merit = VGroup(
            Text("✓", font_size=34, color=GREEN_B, weight=BOLD),
            Text("Causal effects from observational data alone", font_size=30, color=GREEN_B, weight=BOLD),
        ).arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        limit = VGroup(
            Text("△", font_size=32, color=GRAY_B, weight=BOLD),
            Text("Limited by unmeasured confounders", font_size=30, color=GRAY_A, weight=BOLD),
        ).arrange(RIGHT, buff=0.35).move_to(DOWN * 0.8)

        play_at(56.8, FadeIn(sig_title, shift=DOWN * 0.1), FadeIn(merit, shift=UP * 0.1), run_time=0.6)  # chunk14
        play_at(64.6, FadeIn(limit, shift=UP * 0.1), run_time=0.5)               # chunk15
        play_at(67.9, Indicate(sig_title, color=ORANGE, scale_factor=1.12), run_time=1.0)  # chunk16

        go_to(74.6)
