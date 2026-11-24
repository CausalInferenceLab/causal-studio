from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    TABLET_COLOR,
    load_scene_timing_durations,
)


class Scene09_RandomizedExperiment(Scene):
    WAIT_TAIL = 0.3

    def construct(self):
        chunk_durations = load_scene_timing_durations("09_randomized_experiment", language="en")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        # Beat 1:
        random_label = Text("Randomization", font_size=52, color=ACCENT_COLOR, weight=BOLD)
        random_label.move_to(ORIGIN)

        # Beat 2-3: scatter plot — Conditions(x) × Score(y)
        scatter_axes = Axes(
            x_range=[0, 10, 10],
            y_range=[0, 10, 10],
            x_length=5.2,
            y_length=3.6,
            axis_config={
                "include_tip": True, "tip_length": 0.18,
                "stroke_width": 1.8, "color": NEUTRAL_COLOR, "include_ticks": False,
            },
        )
        scatter_axes.move_to(LEFT * 0.8 + DOWN * 0.1)
        scatter_x_label = Text("Conditions", font_size=19, color=NEUTRAL_COLOR)
        scatter_x_label.next_to(scatter_axes.x_axis, DOWN, buff=0.22)
        scatter_y_label = VGroup(*[
            Text(ch, font_size=19, color=NEUTRAL_COLOR) for ch in "Score"
        ]).arrange(DOWN, buff=0.05)
        scatter_y_label.next_to(scatter_axes.y_axis, LEFT, buff=0.22)
        scatter_axes_group = VGroup(scatter_axes, scatter_x_label, scatter_y_label)

        biased_t1_coords = [
            (5.5, 5.5), (6.5, 7.0), (7.0, 6.0), (8.0, 8.0), (9.0, 7.5),
            (7.5, 8.5), (8.5, 6.5), (6.0, 8.0), (9.0, 9.0), (7.0, 7.5),
        ]
        biased_t0_coords = [
            (1.0, 2.0), (2.0, 1.0), (2.5, 3.0), (3.5, 2.5), (4.0, 1.5),
            (1.5, 3.5), (3.0, 4.0), (4.5, 3.5), (2.0, 4.5), (4.0, 4.5),
        ]
        random_t1_coords = [
            (1.0, 4.5), (2.0, 7.0), (3.5, 5.0), (5.0, 8.0), (6.5, 6.5),
            (8.0, 4.0), (9.0, 7.5), (4.0, 3.5), (7.0, 6.0), (2.5, 8.0),
        ]
        random_t0_coords = [
            (1.5, 3.0), (3.0, 6.5), (4.5, 2.5), (6.0, 5.5), (7.5, 3.5),
            (9.0, 6.0), (2.0, 4.0), (5.5, 2.0), (8.5, 4.5), (3.5, 7.0),
        ]

        dot_r = 0.11
        biased_t1_dots = VGroup(*[
            Dot(scatter_axes.coords_to_point(x, y), radius=dot_r, color=TABLET_COLOR, fill_opacity=0.9)
            for x, y in biased_t1_coords
        ])
        biased_t0_dots = VGroup(*[
            Dot(scatter_axes.coords_to_point(x, y), radius=dot_r, color=LIBRARY_COLOR, fill_opacity=0.9)
            for x, y in biased_t0_coords
        ])

        _x0 = scatter_axes.coords_to_point(0, 0)[0]
        _x1 = scatter_axes.coords_to_point(10, 0)[0]
        _my1 = scatter_axes.coords_to_point(0, 6.0)[1]
        _my0 = scatter_axes.coords_to_point(0, 4.45)[1]
        mean_line_t1 = DashedLine(
            [_x0, _my1, 0], [_x1, _my1, 0],
            color=TABLET_COLOR, stroke_width=2.2, dash_length=0.12,
        )
        mean_line_t0 = DashedLine(
            [_x0, _my0, 0], [_x1, _my0, 0],
            color=LIBRARY_COLOR, stroke_width=2.2, dash_length=0.12,
        )
        mean_label_t1 = MathTex(r"E[Y\mid T=1]").scale(0.6).set_color(TABLET_COLOR)
        mean_label_t0 = MathTex(r"E[Y\mid T=0]").scale(0.6).set_color(LIBRARY_COLOR)
        mean_label_t1.next_to(mean_line_t1, RIGHT, buff=0.18)
        mean_label_t0.next_to(mean_line_t0, RIGHT, buff=0.18)

        # Beat 4:
        indep_formula = MathTex(
            r"(Y_0,\,Y_1)",
            r"\perp",
            r"T",
        ).scale(1.5)
        indep_formula[0].set_color(ACCENT_COLOR)
        indep_formula[1].set_color(WHITE)
        indep_formula[2].set_color(TABLET_COLOR)
        indep_formula.move_to(ORIGIN)

        # Beat 5:
        indep_small = MathTex(
            r"(Y_0,\,Y_1)\perp T"
        ).scale(0.75).set_color(NEUTRAL_COLOR)
        indep_small.to_edge(UP, buff=0.5)

        cond_preview = Text("Both conditions are automatically satisfied", font_size=28, color=WHITE)
        cond_preview.move_to(ORIGIN)

        # Beat 6:
        cond1_formula = MathTex(
            r"E[Y_0\mid T=1]",
            r"=",
            r"E[Y_0\mid T=0]",
        ).scale(1.05)
        cond1_formula[0].set_color(TABLET_COLOR)
        cond1_formula[1].set_color(WHITE)
        cond1_formula[2].set_color(LIBRARY_COLOR)
        cond1_formula.move_to(ORIGIN + UP * 0.55)

        cond1_num = Text("① Condition", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
        cond1_num.next_to(cond1_formula, LEFT, buff=0.3)

        bias_zero_badge = RoundedRectangle(
            width=3.2, height=0.78, corner_radius=0.2,
            stroke_color=ACCENT_COLOR, stroke_width=2.2,
            fill_color=ACCENT_COLOR, fill_opacity=0.1,
        )
        bias_zero_label = MathTex(r"\text{Bias} = 0").scale(0.88).set_color(ACCENT_COLOR)
        bias_zero_badge.move_to(bias_zero_label)
        bias_zero_group = VGroup(bias_zero_badge, bias_zero_label)
        bias_zero_group.next_to(cond1_formula, DOWN, buff=0.55)

        # Beat 7:
        cond1_small = MathTex(
            r"E[Y_0\mid T=1]=E[Y_0\mid T=0]"
        ).scale(0.68).set_color(NEUTRAL_COLOR)
        cond1_small.to_edge(UP, buff=0.5)

        cond2_formula = MathTex(
            r"E[Y_1\mid T=1]",
            r"=",
            r"E[Y_1\mid T=0]",
        ).scale(1.05)
        cond2_formula[0].set_color(TABLET_COLOR)
        cond2_formula[1].set_color(WHITE)
        cond2_formula[2].set_color(LIBRARY_COLOR)
        cond2_formula.move_to(ORIGIN + UP * 0.55)

        cond2_num = Text("② Condition", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
        cond2_num.next_to(cond2_formula, LEFT, buff=0.3)

        att_atc_badge = RoundedRectangle(
            width=3.8, height=0.78, corner_radius=0.2,
            stroke_color=ACCENT_COLOR, stroke_width=2.2,
            fill_color=ACCENT_COLOR, fill_opacity=0.1,
        )
        att_atc_label = MathTex(r"ATT = ATC").scale(0.88).set_color(ACCENT_COLOR)
        att_atc_badge.move_to(att_atc_label)
        att_atc_group = VGroup(att_atc_badge, att_atc_label)
        att_atc_group.next_to(cond2_formula, DOWN, buff=0.55)

        # Beat 8:
        conclusion_formula = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATE",
        ).scale(1.05)
        conclusion_formula[2].set_color(YELLOW_E)
        conclusion_formula.move_to(ORIGIN)

        # Beat 9:
        rct_label = Text("RCT", font_size=64, color=ACCENT_COLOR, weight=BOLD)
        rct_label.move_to(ORIGIN + UP * 0.5)
        gold_badge = RoundedRectangle(
            width=5.6, height=0.9, corner_radius=0.22,
            stroke_color=YELLOW_E, stroke_width=2.2,
            fill_color=YELLOW_E, fill_opacity=0.08,
        )
        gold_label = Text("Gold standard for causal inference", font_size=26, color=YELLOW_E, weight=BOLD)
        gold_badge.move_to(gold_label)
        gold_group = VGroup(gold_badge, gold_label)
        gold_group.next_to(rct_label, DOWN, buff=0.55)

        # ── Beat 1 ──
        self.play(FadeIn(random_label, scale=0.85), run_time=0.75)
        wait_for_chunks([1], spent=0.75)

        # ── Beat 2 ──
        self.play(FadeOut(random_label, scale=0.95), run_time=0.35)
        self.play(FadeIn(scatter_axes_group), run_time=0.7)
        self.play(
            FadeIn(biased_t1_dots, lag_ratio=0.12),
            FadeIn(biased_t0_dots, lag_ratio=0.12),
            run_time=0.9,
        )
        self.wait(2.4)
        self.play(
            *[biased_t1_dots[i].animate.move_to(
                scatter_axes.coords_to_point(*random_t1_coords[i])
              ) for i in range(len(random_t1_coords))],
            *[biased_t0_dots[i].animate.move_to(
                scatter_axes.coords_to_point(*random_t0_coords[i])
              ) for i in range(len(random_t0_coords))],
            run_time=1.2,
        )
        wait_for_chunks([2], spent=5.55)

        # ── Beat 3 ──
        self.play(
            Create(mean_line_t1),
            Create(mean_line_t0),
            run_time=0.7,
        )
        self.play(
            FadeIn(mean_label_t1, shift=LEFT * 0.05),
            FadeIn(mean_label_t0, shift=LEFT * 0.05),
            run_time=0.55,
        )
        wait_for_chunks([3], spent=1.25)

        # ── Beat 4 ──
        self.play(
            FadeOut(scatter_axes_group),
            FadeOut(biased_t1_dots),
            FadeOut(biased_t0_dots),
            FadeOut(mean_line_t1),
            FadeOut(mean_line_t0),
            FadeOut(mean_label_t1),
            FadeOut(mean_label_t0),
            run_time=0.5,
        )
        self.play(FadeIn(indep_formula, scale=0.9), run_time=0.8)
        self.play(Indicate(indep_formula[1], color=WHITE, scale_factor=1.1), run_time=0.55)
        wait_for_chunks([4], spent=1.85)

        # ── Beat 5 ──
        self.play(Transform(indep_formula, indep_small), run_time=0.6)
        self.play(FadeIn(cond_preview, shift=UP * 0.07), run_time=0.6)
        wait_for_chunks([5], spent=1.2)

        # ── Beat 6 ──
        self.play(
            FadeOut(cond_preview),
            FadeOut(indep_formula),
            run_time=0.5,
        )
        self.play(
            FadeIn(cond1_num, shift=RIGHT * 0.05),
            FadeIn(cond1_formula, shift=UP * 0.07),
            run_time=0.75,
        )
        self.play(
            Indicate(cond1_formula[0], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(cond1_formula[2], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        self.wait(3.5)
        self.play(FadeIn(bias_zero_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(bias_zero_badge, color=ACCENT_COLOR, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([6], spent=6.45)

        # ── Beat 7 ──
        self.play(
            Transform(cond1_formula, cond1_small),
            FadeOut(cond1_num),
            FadeOut(bias_zero_group),
            run_time=0.6,
        )
        self.play(
            FadeIn(cond2_num, shift=RIGHT * 0.05),
            FadeIn(cond2_formula, shift=UP * 0.07),
            run_time=0.75,
        )
        self.play(
            Indicate(cond2_formula[0], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(cond2_formula[2], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        self.wait(2.5)
        self.play(FadeIn(att_atc_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(att_atc_badge, color=ACCENT_COLOR, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([7], spent=5.55)

        # ── Beat 8 ──
        self.play(
            FadeOut(cond1_formula),
            FadeOut(cond2_num),
            FadeOut(cond2_formula),
            FadeOut(att_atc_group),
            run_time=0.55,
        )
        self.play(FadeIn(conclusion_formula, shift=UP * 0.07), run_time=0.75)
        self.play(Indicate(conclusion_formula[2], color=YELLOW_E, scale_factor=1.08), run_time=0.5)
        wait_for_chunks([8], spent=1.8)

        # ── Beat 9 ──
        self.play(FadeOut(conclusion_formula), run_time=0.5)
        self.play(FadeIn(rct_label, scale=0.85), run_time=0.75)
        self.play(FadeIn(gold_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(gold_badge, color=YELLOW_E, scale_factor=1.03), run_time=0.55)
        wait_for_chunks([9], spent=2.4)
        self.wait(self.WAIT_TAIL)
