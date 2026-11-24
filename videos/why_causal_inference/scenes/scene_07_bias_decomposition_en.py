from manim import *

from why_causal_inference_common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_icon,
    load_english_scene_timing_durations as load_scene_timing_durations,
)


class Scene07_BiasDecomposition(Scene):
    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("07_bias_decomposition")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        bias_word = Text("Why isn't the simple mean difference a causal effect?", font_size=28, color=QUESTION_COLOR, weight=BOLD)
        bias_word.move_to(ORIGIN + UP * 0.7)

        avg_diff_box = RoundedRectangle(
            width=4.3,
            height=0.8,
            corner_radius=0.2,
            stroke_color=WHITE,
            stroke_width=1.8,
        )
        avg_diff_label = Text("Observed mean difference", font_size=26, color=WHITE, weight=BOLD).move_to(avg_diff_box)
        avg_diff_group = VGroup(avg_diff_box, avg_diff_label)
        avg_diff_group.move_to(ORIGIN + DOWN * 0.15)

        effect_box = RoundedRectangle(
            width=1.85,
            height=0.72,
            corner_radius=0.18,
            stroke_color=ACCENT_COLOR,
            stroke_width=1.8,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.12,
        )
        effect_label = Text("effect", font_size=22, color=ACCENT_COLOR, weight=BOLD).move_to(effect_box)
        effect_group = VGroup(effect_box, effect_label)

        plus = MathTex(r"+").scale(0.9).set_color(WHITE)

        bias_box = RoundedRectangle(
            width=1.55,
            height=0.72,
            corner_radius=0.18,
            stroke_color=QUESTION_COLOR,
            stroke_width=1.8,
            fill_color=QUESTION_COLOR,
            fill_opacity=0.12,
        )
        bias_label = Text("bias", font_size=22, color=QUESTION_COLOR, weight=BOLD).move_to(bias_box)
        bias_group = VGroup(bias_box, bias_label)

        split_group = VGroup(effect_group, plus, bias_group).arrange(RIGHT, buff=0.24)
        split_group.move_to(avg_diff_group)

        treated_card = RoundedRectangle(width=3.55, height=3.0, corner_radius=0.18, stroke_color=TABLET_COLOR, stroke_width=2.6)
        control_card = RoundedRectangle(width=3.55, height=3.0, corner_radius=0.18, stroke_color=LIBRARY_COLOR, stroke_width=2.6)
        treated_card.move_to(LEFT * 2.7 + DOWN * 0.05)
        control_card.move_to(RIGHT * 2.7 + DOWN * 0.05)

        treated_group = VGroup(
            MathTex(r"T=1").set_color(TABLET_COLOR).scale(0.82),
            Text("Tablet given", font_size=24, color=TABLET_COLOR, weight=BOLD),
            VGroup(
                load_icon("school.svg", WHITE, 0.64),
                load_icon("arrow-up.svg", TABLET_COLOR, 0.56),
            ).arrange(RIGHT, buff=0.18),
            Text("May have scored\nhigher to begin with", font_size=18, color=WHITE, weight=BOLD),
        ).arrange(DOWN, buff=0.18).move_to(treated_card)
        control_group = VGroup(
            MathTex(r"T=0").set_color(LIBRARY_COLOR).scale(0.82),
            Text("No tablet", font_size=24, color=LIBRARY_COLOR, weight=BOLD),
            VGroup(
                load_icon("school.svg", WHITE, 0.64),
                load_icon("arrow-down.svg", LIBRARY_COLOR, 0.56),
            ).arrange(RIGHT, buff=0.18),
            Text("May have scored\nlower to begin with", font_size=18, color=WHITE, weight=BOLD),
        ).arrange(DOWN, buff=0.18).move_to(control_card)

        inequality = MathTex(r"E[Y_0\mid T=1]", r">", r"E[Y_0\mid T=0]").scale(1.0)
        inequality[0].set_color(TABLET_COLOR)
        inequality[1].set_color(ACCENT_COLOR)
        inequality[2].set_color(LIBRARY_COLOR)
        inequality.to_edge(DOWN, buff=0.7)

        observed_formula = MathTex(
            r"E[Y\mid T=1] - E[Y\mid T=0]",
            r"=",
            r"E[Y_1\mid T=1] - E[Y_0\mid T=0]",
        ).scale(0.9)
        observed_formula.move_to(ORIGIN)

        decomp_summary = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
            r"+",
            r"Bias",
        ).scale(1.0)
        decomp_summary[2].set_color(ACCENT_COLOR)
        decomp_summary[4].set_color(QUESTION_COLOR)
        decomp_summary.move_to(ORIGIN + UP * 0.5)

        att_detail = MathTex(r"ATT = E[Y_1-Y_0\mid T=1]").scale(0.84).set_color(ACCENT_COLOR)
        bias_detail = MathTex(r"Bias = E[Y_0\mid T=1]-E[Y_0\mid T=0]").scale(0.84).set_color(QUESTION_COLOR)
        att_detail.next_to(decomp_summary, DOWN, buff=0.5)
        bias_detail.next_to(att_detail, DOWN, buff=0.28)

        att_focus = SurroundingRectangle(att_detail, color=ACCENT_COLOR, buff=0.16, corner_radius=0.1)
        bias_focus = SurroundingRectangle(bias_detail, color=QUESTION_COLOR, buff=0.16, corner_radius=0.1)
        att_note = Text("True causal effect", font_size=20, color=ACCENT_COLOR, weight=BOLD).next_to(att_focus, RIGHT, buff=0.22)
        bias_note = Text("Pre-existing\ngroup difference", font_size=18, color=QUESTION_COLOR, weight=BOLD).next_to(bias_focus, RIGHT, buff=0.22)

        confounder_box = RoundedRectangle(width=4.4, height=2.1, corner_radius=0.18, stroke_color=NEUTRAL_COLOR, stroke_width=2.2).move_to(UP * 1.45)
        confounder_label = Text("School conditions", font_size=24, color=WHITE, weight=BOLD)
        confounder_label.move_to(confounder_box.get_top() + DOWN * 0.38)
        budget_chip = VGroup(
            load_icon("coin.svg", GOLD_E, 0.26),
            Text("Funding", font_size=17, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        location_chip = VGroup(
            load_icon("map-pin.svg", BLUE_E, 0.26),
            Text("Location", font_size=17, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        teacher_chip = VGroup(
            load_icon("user-star.svg", GREEN_E, 0.26),
            Text("Teacher quality", font_size=17, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        _row1_chips = VGroup(budget_chip, location_chip).arrange(RIGHT, buff=0.22)
        confounder_factors = VGroup(_row1_chips, teacher_chip).arrange(DOWN, buff=0.12)
        confounder_factors.move_to(confounder_box.get_center() + DOWN * 0.28)
        t_node = VGroup(Circle(radius=0.56, stroke_color=TABLET_COLOR, stroke_width=2.6), MathTex(r"T").set_color(TABLET_COLOR)).move_to(LEFT * 2.6 + DOWN * 0.35)
        y_node = VGroup(Circle(radius=0.56, stroke_color=ACCENT_COLOR, stroke_width=2.6), MathTex(r"Y").set_color(ACCENT_COLOR)).move_to(RIGHT * 2.6 + DOWN * 0.35)
        t_label = Text("Treatment", font_size=23, color=TABLET_COLOR, weight=BOLD).next_to(t_node, DOWN, buff=0.18)
        y_label = Text("Outcome", font_size=23, color=ACCENT_COLOR, weight=BOLD).next_to(y_node, DOWN, buff=0.18)
        c_to_t = Arrow(confounder_box.get_bottom() + LEFT * 0.42, t_node.get_top(), buff=0.12, color=NEUTRAL_COLOR, stroke_width=3.0)
        c_to_y = Arrow(confounder_box.get_bottom() + RIGHT * 0.42, y_node.get_top(), buff=0.12, color=NEUTRAL_COLOR, stroke_width=3.0)
        t_to_y = Arrow(t_node.get_right(), y_node.get_left(), buff=0.18, color=TABLET_COLOR, stroke_width=3.2)
        compare_axis = Line(LEFT * 1.7, RIGHT * 1.7, color=NEUTRAL_COLOR, stroke_width=2.2)
        compare_axis.to_edge(DOWN, buff=0.58)

        treated_bar = RoundedRectangle(
            width=0.56,
            height=1.18,
            corner_radius=0.1,
            stroke_color=TABLET_COLOR,
            stroke_width=2.4,
            fill_color=TABLET_COLOR,
            fill_opacity=0.15,
        )
        treated_bar.align_to(compare_axis, DOWN).shift(LEFT * 1.0)

        control_bar = RoundedRectangle(
            width=0.56,
            height=0.7,
            corner_radius=0.1,
            stroke_color=LIBRARY_COLOR,
            stroke_width=2.4,
            fill_color=LIBRARY_COLOR,
            fill_opacity=0.15,
        )
        control_bar.align_to(compare_axis, DOWN).shift(RIGHT * 1.0)

        treated_mark = MathTex(r"T=1").scale(0.68).set_color(TABLET_COLOR).next_to(treated_bar, DOWN, buff=0.12)
        control_mark = MathTex(r"T=0").scale(0.68).set_color(LIBRARY_COLOR).next_to(control_bar, DOWN, buff=0.12)
        compare_icon = load_icon("git-compare.svg", WHITE, 0.46).move_to(compare_axis.get_center() + UP * 0.48)
        compare_group = VGroup(compare_axis, treated_bar, control_bar, treated_mark, control_mark, compare_icon)

        balanced_axis = compare_axis.copy()
        balanced_treated_bar = RoundedRectangle(
            width=0.56,
            height=0.94,
            corner_radius=0.1,
            stroke_color=TABLET_COLOR,
            stroke_width=2.4,
            fill_color=TABLET_COLOR,
            fill_opacity=0.15,
        )
        balanced_treated_bar.align_to(balanced_axis, DOWN).shift(LEFT * 1.0)
        balanced_control_bar = RoundedRectangle(
            width=0.56,
            height=0.94,
            corner_radius=0.1,
            stroke_color=LIBRARY_COLOR,
            stroke_width=2.4,
            fill_color=LIBRARY_COLOR,
            fill_opacity=0.15,
        )
        balanced_control_bar.align_to(balanced_axis, DOWN).shift(RIGHT * 1.0)
        balanced_treated_mark = treated_mark.copy().next_to(balanced_treated_bar, DOWN, buff=0.12)
        balanced_control_mark = control_mark.copy().next_to(balanced_control_bar, DOWN, buff=0.12)
        equal_icon = load_icon("equal.svg", ACCENT_COLOR, 0.48).move_to(compare_icon)
        check_icon = load_icon("check.svg", ACCENT_COLOR, 0.38).next_to(equal_icon, UP, buff=0.08)
        balanced_icon = VGroup(equal_icon, check_icon)
        balanced_group = VGroup(
            balanced_axis,
            balanced_treated_bar,
            balanced_control_bar,
            balanced_treated_mark,
            balanced_control_mark,
            balanced_icon,
        )
        balanced_group.move_to(compare_group)

        confounder_cross = Cross(confounder_box, stroke_color=QUESTION_COLOR, stroke_width=5.5)
        confounder_cross.scale(1.05)

        # Beat 1:
        self.play(FadeIn(bias_word, scale=0.9), run_time=0.8)
        self.play(FadeIn(avg_diff_group, shift=UP * 0.06), run_time=0.7)
        self.play(
            Transform(avg_diff_group, split_group),
            run_time=0.9,
        )
        wait_for_chunks([1, 2], spent=2.4)

        # Beat 2:
        self.play(FadeOut(bias_word, scale=0.95), FadeOut(avg_diff_group), run_time=0.3)
        self.play(
            FadeIn(treated_card, scale=0.96),
            FadeIn(control_card, scale=0.96),
            FadeIn(treated_group, shift=UP * 0.06),
            FadeIn(control_group, shift=UP * 0.06),
            run_time=0.95,
        )
        wait_for_chunks([3], spent=1.2)

        # Beat 3:
        self.play(FadeIn(inequality, shift=UP * 0.08), run_time=0.65)
        self.play(
            Indicate(treated_group[-1], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(control_group[-1], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        wait_for_chunks([4], spent=1.25)

        # Beat 4:
        self.play(
            FadeOut(treated_card),
            FadeOut(control_card),
            FadeOut(treated_group),
            FadeOut(control_group),
            FadeOut(inequality),
            FadeIn(observed_formula, shift=UP * 0.08),
            run_time=0.85,
        )
        self.play(Indicate(observed_formula[2], color=WHITE, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([5], spent=1.35)

        # Beat 5:
        self.play(TransformMatchingTex(observed_formula, decomp_summary), run_time=0.95)
        self.play(FadeIn(att_detail, shift=UP * 0.06), FadeIn(bias_detail, shift=UP * 0.06), run_time=0.5)
        wait_for_chunks([6], spent=0.95)
        self.play(FadeIn(att_focus), FadeIn(att_note, shift=UP * 0.06), run_time=0.45)
        self.play(Indicate(att_focus, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.5)
        self.wait(3.4)
        self.play(
            FadeOut(att_focus),
            FadeOut(att_note),
            FadeIn(bias_focus),
            FadeIn(bias_note, shift=UP * 0.06),
            run_time=0.45,
        )
        self.play(Indicate(bias_focus, color=QUESTION_COLOR, scale_factor=1.02), run_time=0.5)
        wait_for_chunks([7, 8], spent=5.3)

        # Beat 6:
        self.play(
            FadeOut(bias_focus),
            FadeOut(bias_note),
            FadeOut(decomp_summary),
            FadeOut(att_detail),
            FadeOut(bias_detail),
            run_time=0.75,
        )
        self.play(
            FadeIn(confounder_box, shift=DOWN * 0.08),
            FadeIn(confounder_label, shift=DOWN * 0.08),
            FadeIn(t_node, scale=0.92),
            FadeIn(y_node, scale=0.92),
            FadeIn(t_label, shift=UP * 0.06),
            FadeIn(y_label, shift=UP * 0.06),
            run_time=0.9,
        )
        self.play(Create(c_to_t), Create(c_to_y), GrowArrow(t_to_y), run_time=0.85)
        self.play(FadeIn(compare_group, shift=UP * 0.06), run_time=0.55)
        self.play(
            Indicate(confounder_box, color=QUESTION_COLOR, scale_factor=1.03),
            Indicate(compare_icon, color=WHITE, scale_factor=1.05),
            run_time=0.55,
        )
        self.wait(4.9)
        self.play(FadeIn(budget_chip, shift=UP * 0.05), run_time=0.35)
        self.play(FadeIn(location_chip, shift=UP * 0.05), run_time=0.35)
        self.play(FadeIn(teacher_chip, shift=UP * 0.05), run_time=0.45)
        wait_for_chunks([9, 10], spent=9.65)
        self.play(
            Create(confounder_cross),
            c_to_t.animate.set_stroke(opacity=0.22),
            c_to_y.animate.set_stroke(opacity=0.22),
            confounder_box.animate.set_stroke(opacity=0.32),
            confounder_label.animate.set_opacity(0.32),
            confounder_factors.animate.set_opacity(0.32),
            run_time=0.7,
        )
        self.wait(4.2)
        self.play(Transform(compare_group, balanced_group), run_time=0.8)
        self.play(Indicate(compare_group[5], color=ACCENT_COLOR, scale_factor=1.08), run_time=0.45)
        wait_for_chunks([11, 12], spent=6.95)
        self.wait(self.WAIT_TAIL)
