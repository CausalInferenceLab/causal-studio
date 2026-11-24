from manim import *

from rdd_en_common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


class Scene07Simulation(Scene):
    """
    Scene 07: simulation (English)
    Audio: 46.58s (6 chunks)

    Beat1 chunk1  ( 0.00~ 1.86s)  title
    Beat2 chunk2  ( 1.86~10.31s)  simulation setup: cutoff=370, τ=0.5, N=500
    Beat3 chunk3  (10.31~21.55s)  500 students scatter + DGP formula
    Beat4 chunk4  (21.55~28.00s)  fit regression lines left/right
    Beat5 chunk5  (28.00~39.24s)  results: intercepts 2.02/2.50, τ̂=0.48
    Beat6 chunk6  (39.24~46.58s)  conclusion: RDD recovers treatment effect
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~1.86s) ─────────────────────────
        title = VGroup(
            Text("Simulation", font=FONT, font_size=44, color=WHITE),
            Text("Can RDD Recover the Treatment Effect?", font=FONT, font_size=26, color=GRAY_MID),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.5)
        self.wait(0.36)
        self.play(FadeOut(title), run_time=0.3)

        # ── Beat 2 (chunk2: 1.86~10.31s, 8.45s) ─────────────
        setup_header = Text("Simulation Setup", font=FONT, font_size=30, color=WHITE).move_to(UP * 1.7)
        setup_items = VGroup(
            self._setup_row("Cutoff", "370 pts  (scholarship threshold)", YELLOW_MAIN),
            self._setup_row("True Treatment Effect", "0.5 GPA points", GREEN_MAIN),
            self._setup_row("Sample Size N", "500 students", BLUE_MAIN),
            self._setup_row("Running Variable", "Korean CSAT Score", GRAY_MID),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(setup_header, DOWN, buff=0.45)

        self.play(FadeIn(setup_header, shift=DOWN * 0.15), run_time=0.5)
        for item in setup_items:
            self.play(FadeIn(item, shift=RIGHT * 0.15), run_time=0.4)
        self.wait(5.85)
        self.play(FadeOut(VGroup(setup_header, setup_items)), run_time=0.5)

        # ── shared graph structure (Beats 3~6) ───────────────
        axes = Axes(
            x_range=[340, 401, 10], y_range=[1.0, 4.0, 0.5],
            x_length=8.5, y_length=4.5,
            axis_config={
                "color": GRAY_MID, "stroke_width": 1.2,
                "include_tip": True, "tip_width": 0.12, "tip_height": 0.12,
            },
            x_axis_config={"numbers_to_include": [340, 350, 360, 370, 380, 390, 400]},
            y_axis_config={"numbers_to_include": [1.5, 2.0, 2.5, 3.0, 3.5]},
        ).move_to(RIGHT * 0.3 + UP * 0.4)

        y_lbl = Text("GPA", font=FONT, font_size=12, color=GRAY_MID)
        y_lbl.next_to(axes, LEFT, buff=0.1)
        x_lbl = Text("CSAT Score (pts)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_center(), DOWN, buff=0.55)

        cutoff_line = DashedLine(
            axes.c2p(370, 1.0), axes.c2p(370, 4.0),
            color=YELLOW_MAIN, stroke_width=2.5, dash_length=0.12,
        )
        cutoff_lbl = Text("Cutoff (370 pts)", font=FONT, font_size=14, color=YELLOW_MAIN).next_to(
            axes.c2p(370, 4.0), UR, buff=0.05
        )

        rng = np.random.default_rng(42)
        n = 500
        xs = rng.uniform(340, 400, n)
        treated = (xs >= 370).astype(float)
        ys = 2.0 + 0.015 * (xs - 370) + 0.5 * treated + rng.normal(0, 0.3, n)

        scatter_left = VGroup(*[
            Dot(axes.c2p(x, y), color=RED_MAIN, radius=0.04, fill_opacity=0.55)
            for x, y in zip(xs, ys) if x < 370 and 1.0 <= y <= 4.0
        ])
        scatter_right = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE_MAIN, radius=0.04, fill_opacity=0.55)
            for x, y in zip(xs, ys) if x >= 370 and 1.0 <= y <= 4.0
        ])

        legend = VGroup(
            VGroup(
                Dot(color=RED_MAIN, radius=0.09),
                Text("No Scholarship (<370)", font=FONT, font_size=16, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                Dot(color=BLUE_MAIN, radius=0.09),
                Text("Scholarship (≥370)", font=FONT, font_size=16, color=BLUE_MAIN),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        legend.move_to(axes.get_corner(UR) + LEFT * 1.5 + DOWN * 0.4)

        # ── Beat 3 (chunk3: 10.31~21.55s, 11.24s) ────────────
        dgp_formula = VGroup(
            MathTex(
                r"y_i = 2.0 + 0.015(x_i - 370) + 0.5 \cdot T_i + \varepsilon_i",
                font_size=26, color=WHITE,
            ),
            MathTex(r"T_i = 1 \;(x_i \geq 370), \quad \varepsilon \sim \mathcal{N}(0,\,0.09)",
                    font_size=16, color=GRAY_MID),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 3.1)

        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=0.8)
        self.play(Create(cutoff_line), FadeIn(cutoff_lbl), run_time=0.5)
        self.play(FadeIn(dgp_formula), run_time=0.7)
        self.play(FadeIn(scatter_left), run_time=2.0)
        self.play(FadeIn(scatter_right), run_time=2.0)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(4.34)
        self.play(FadeOut(dgp_formula), run_time=0.4)

        # ── Beat 4 (chunk4: 21.55~28.00s, 6.45s) ─────────────
        left_line = axes.plot(
            lambda x: 2.02 + 0.015 * (x - 370), x_range=[340, 370],
            color=RED_MAIN, stroke_width=4.5,
        )
        right_line = axes.plot(
            lambda x: 2.50 + 0.015 * (x - 370), x_range=[370, 400],
            color=BLUE_MAIN, stroke_width=4.5,
        )
        reg_desc = Text(
            "Fitting regression lines independently on each side",
            font=FONT, font_size=19, color=WHITE,
        ).move_to(DOWN * 3.1)

        self.play(Create(left_line), run_time=0.9)
        self.play(Create(right_line), run_time=0.9)
        self.play(FadeIn(reg_desc), run_time=0.5)
        self.wait(3.76)
        self.play(FadeOut(reg_desc), run_time=0.4)

        # ── Beat 5 (chunk5: 28.00~39.24s, 11.24s) ────────────
        left_dot = Dot(axes.c2p(370, 2.02), color=RED_MAIN, radius=0.12)
        right_dot = Dot(axes.c2p(370, 2.50), color=BLUE_MAIN, radius=0.12)
        left_dot_lbl = Text("2.02", font=FONT, font_size=18, color=WHITE).next_to(
            axes.c2p(370, 2.02), LEFT, buff=0.14
        )
        right_dot_lbl = Text("2.50", font=FONT, font_size=18, color=WHITE).next_to(
            axes.c2p(370, 2.50), LEFT, buff=0.14
        )

        jump_arrow = DoubleArrow(
            axes.c2p(370, 2.02), axes.c2p(370, 2.50),
            color=YELLOW_MAIN, buff=0, stroke_width=4, tip_length=0.15,
        )
        jump_lbl = VGroup(
            Text("Estimated Effect ", font=FONT, font_size=17, color=YELLOW_MAIN),
            MathTex(r"\hat{\tau}", font_size=22, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.08).next_to(jump_arrow, RIGHT, buff=0.15)

        result_desc = VGroup(
            Text("Left Intercept: 2.02   |   Right Intercept: 2.50", font=FONT, font_size=18, color=WHITE),
            VGroup(
                Text("Estimated Treatment Effect ", font=FONT, font_size=18, color=YELLOW_MAIN),
                MathTex(r"\hat{\tau} = 0.48", font_size=22, color=YELLOW_MAIN),
                Text("  (True: τ = 0.5)", font=FONT, font_size=16, color=GREEN_MAIN),
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 3.1)

        self.play(
            FadeIn(left_dot), FadeIn(left_dot_lbl),
            FadeIn(right_dot), FadeIn(right_dot_lbl),
            run_time=0.7,
        )
        self.play(Create(jump_arrow), FadeIn(jump_lbl), run_time=0.7)
        self.play(FadeIn(result_desc), run_time=0.6)
        self.wait(9.24)

        # ── Beat 6 (chunk6: 39.24~46.58s, 7.34s) ─────────────
        conclusion = Text(
            "Fitting separate regression lines → RDD recovers the treatment effect",
            font=FONT, font_size=19, color=GREEN_MAIN,
        ).move_to(DOWN * 3.1)

        self.play(FadeOut(result_desc), FadeIn(conclusion), run_time=0.6)
        self.wait(6.73)  # chunk6 + WAIT_TAIL

    def _setup_row(self, key: str, val: str, color: str) -> VGroup:
        return VGroup(
            Text(f"{key}: ", font=FONT, font_size=19, color=GRAY_MID),
            Text(val, font=FONT, font_size=19, color=color),
        ).arrange(RIGHT, buff=0.12)
