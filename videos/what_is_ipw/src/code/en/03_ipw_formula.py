from manim import *

ICON = "/Users/jhkim/Desktop/personal_study/causal/causal-studio/videos/assets/tabler-icons/icons/outline"

SEVERE = "#b07cff"
MILD = "#39d98a"


class IPWFormula(Scene):
    """Scene 03 (EN). Same animations, English text, resynced.
    timings: build/audio/03_ipw_formula_en.timings.json (total 53.28s, 13 chunks)
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

        # Beat 1~2 — symbols on one person (chunk1~5)
        person = icon("user", WHITE, height=1.5).move_to(LEFT * 1.6 + UP * 2.0)
        LEFT_ANCHOR = -4.9

        def define(sym, gloss, color, y):
            m = MathTex(sym, color=color).scale(1.05)
            colon = Text(":", font_size=30, color=GRAY_B)
            g = Text(gloss, font_size=24, color=GRAY_A, weight=BOLD)
            row = VGroup(m, colon, g).arrange(RIGHT, buff=0.28)
            row.move_to([0, y, 0])
            row.shift(RIGHT * (LEFT_ANCHOR - m.get_left()[0]))
            return row, m

        T_def, T_sym = define("T", "took medicine ( 1 / 0 )", BLUE_B, 0.55)
        X_def, X_sym = define("X", "patient state ( severe / mild )", SEVERE, -0.55)
        e_def, e_sym = define("e(X)=P(T=1|X)", "prob. of taking medicine", ORANGE, -1.65)

        play_at(0.5, FadeIn(person, shift=DOWN * 0.1), run_time=0.5)
        play_at(4.9, FadeIn(T_def, shift=RIGHT * 0.1), run_time=0.5)          # chunk3
        play_at(9.8, FadeIn(X_def, shift=RIGHT * 0.1), run_time=0.5)          # chunk4
        play_at(13.7, FadeIn(e_def, shift=RIGHT * 0.1), run_time=0.5)         # chunk5

        # Beat 3 — weight = reciprocal of probability, two cases (chunk6~9)
        play_at(17.3, FadeOut(person, T_def, X_def), run_time=0.4)            # chunk6
        play_at(18.3, e_def.animate.scale(0.85).to_edge(UP, buff=0.5), run_time=0.5)
        rule = Text("Rule: weight = 1 / probability", font_size=30, color=ORANGE, weight=BOLD).move_to(UP * 1.55)
        play_at(19.6, FadeIn(rule), run_time=0.5)

        case_t = VGroup(
            Text("Took medicine", font_size=28, color=BLUE_B, weight=BOLD),
            MathTex(r"(T=1)", color=BLUE_B).scale(0.65),
            MathTex(r"w = \frac{1}{e(X)}", color=BLUE_B).scale(1.2),
        ).arrange(RIGHT, buff=0.4).move_to(UP * 0.55)
        case_c = VGroup(
            Text("No medicine", font_size=28, color=RED_B, weight=BOLD),
            MathTex(r"(T=0)", color=RED_B).scale(0.65),
            MathTex(r"w = \frac{1}{1 - e(X)}", color=RED_B).scale(1.2),
        ).arrange(RIGHT, buff=0.4).move_to(DOWN * 1.1)
        rare = Text("The rarer the event, the larger the weight", font_size=26, color=YELLOW, weight=BOLD).to_edge(DOWN, buff=0.55)

        play_at(23.9, FadeIn(case_t, shift=UP * 0.08), run_time=0.6)          # chunk7
        play_at(28.9, FadeIn(case_c, shift=UP * 0.08), run_time=0.5)          # chunk8
        play_at(36.3, FadeIn(rare), run_time=0.45)                           # chunk9
        play_at(39.6, FadeOut(e_def, rule, case_t, case_c, rare), run_time=0.35)

        # Beat 4 — combine into one formula (chunk10~13)
        combined = MathTex("w", "=", r"\frac{T}{e(X)}", "+", r"\frac{1-T}{1-e(X)}").scale(1.25)
        combined.move_to(UP * 0.9)
        combined[2].set_color(BLUE_B)
        combined[4].set_color(RED_B)

        brace_t = Brace(combined[2], DOWN, color=BLUE_B)
        brace_c = Brace(combined[4], DOWN, color=RED_B)
        lbl_t = Text("Took medicine", font_size=24, color=BLUE_B, weight=BOLD).next_to(brace_t, DOWN, buff=0.15).shift(LEFT * 0.25)
        lbl_c = Text("No medicine", font_size=24, color=RED_B, weight=BOLD).next_to(brace_c, DOWN, buff=0.15).shift(RIGHT * 0.25)
        sub1 = MathTex(r"T=1:", r"\ w =", r"\frac{1}{e(X)}", r"+", r"\frac{0}{1-e(X)}").scale(0.82)
        sub1[0].set_color(BLUE_B)
        sub1[4].set_color(GRAY_D)
        sub0 = MathTex(r"T=0:", r"\ w =", r"\frac{0}{e(X)}", r"+", r"\frac{1}{1-e(X)}").scale(0.82)
        sub0[0].set_color(RED_B)
        sub0[2].set_color(GRAY_D)
        subs = VGroup(sub1, sub0).arrange(DOWN, buff=0.45).move_to(DOWN * 0.7)
        one = icon("user", WHITE, height=0.55)
        one_w = MathTex("w", color=ORANGE).scale(0.8)
        one_arrow = Arrow(LEFT * 0.4, RIGHT * 0.4, color=GRAY_B, stroke_width=4, buff=0.05)
        closing = VGroup(one, one_arrow, one_w,
                         Text(" Everyone gets their own weight", font_size=26, color=ORANGE, weight=BOLD)
                         ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.5)

        play_at(42.9, Write(combined), run_time=0.8)                         # chunk10
        play_at(46, GrowFromCenter(brace_t), FadeIn(lbl_t),
                GrowFromCenter(brace_c), FadeIn(lbl_c), run_time=0.6)          # chunk11
        play_at(50.7, FadeOut(brace_t, brace_c, lbl_t, lbl_c),
                combined.animate.to_edge(UP, buff=1.4).scale(0.9), run_time=0.5)  # chunk12
        play_at(51.4, FadeIn(sub1, shift=UP * 0.08), run_time=0.45)
        play_at(52.5, FadeIn(sub0, shift=UP * 0.08), run_time=0.45)
        play_at(56, FadeIn(closing, shift=UP * 0.1), run_time=0.5)         # chunk13

        go_to(61.1)
