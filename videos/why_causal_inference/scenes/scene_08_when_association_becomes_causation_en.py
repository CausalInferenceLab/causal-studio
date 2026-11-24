from manim import *

from why_causal_inference_common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_english_scene_timing_durations as load_scene_timing_durations,
)


class Scene08_WhenAssociationBecomesCausation(Scene):
    WAIT_TAIL = 0.3

    def construct(self):
        chunk_durations = load_scene_timing_durations("08_when_association_becomes_causation")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        # Beat 1:
        question = Text(
            "When does association become causation?",
            font_size=34,
            color=QUESTION_COLOR,
            weight=BOLD,
        )
        question.move_to(ORIGIN)

        # Beat 2:
        decomp_summary_recall = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
            r"+",
            r"Bias",
        ).scale(0.95)
        decomp_summary_recall[2].set_color(ACCENT_COLOR)
        decomp_summary_recall[4].set_color(QUESTION_COLOR)
        decomp_summary_recall.move_to(ORIGIN + UP * 0.7)

        att_recall_detail = MathTex(
            r"ATT = E[Y_1-Y_0\mid T=1]"
        ).scale(0.8).set_color(ACCENT_COLOR)
        bias_recall_detail = MathTex(
            r"Bias = E[Y_0\mid T=1]-E[Y_0\mid T=0]"
        ).scale(0.8).set_color(QUESTION_COLOR)
        att_recall_detail.next_to(decomp_summary_recall, DOWN, buff=0.42)
        bias_recall_detail.next_to(att_recall_detail, DOWN, buff=0.25)
        decomp_recall_group = VGroup(decomp_summary_recall, att_recall_detail, bias_recall_detail)

        # Beat 3:
        bias_zero = MathTex(r"\text{Bias} = 0", color=QUESTION_COLOR).scale(0.9)
        bias_zero.next_to(bias_recall_detail, DOWN, buff=0.45)

        # Beat 4:
        comparability_formula = MathTex(
            r"E[Y_0\mid T=1]",
            r"=",
            r"E[Y_0\mid T=0]",
        ).scale(1.1)
        comparability_formula[0].set_color(TABLET_COLOR)
        comparability_formula[1].set_color(WHITE)
        comparability_formula[2].set_color(LIBRARY_COLOR)
        comparability_formula.move_to(ORIGIN)

        # Beat 5:
        comparability_small = MathTex(
            r"E[Y_0\mid T=1] = E[Y_0\mid T=0]",
        ).scale(0.7).set_color(NEUTRAL_COLOR)
        comparability_small.to_edge(UP, buff=0.5)

        treated_card8 = RoundedRectangle(
            width=3.3, height=2.5, corner_radius=0.18,
            stroke_color=TABLET_COLOR, stroke_width=2.4,
        )
        control_card8 = RoundedRectangle(
            width=3.3, height=2.5, corner_radius=0.18,
            stroke_color=LIBRARY_COLOR, stroke_width=2.4,
        )
        treated_card8.move_to(LEFT * 2.5 + DOWN * 0.3)
        control_card8.move_to(RIGHT * 2.5 + DOWN * 0.3)

        treated_content8 = VGroup(
            MathTex(r"T=1").set_color(TABLET_COLOR).scale(0.78),
            Text("Tablet given", font_size=22, color=TABLET_COLOR, weight=BOLD),
            Text("Even without a tablet", font_size=19, color=WHITE),
            Text("similar scores", font_size=20, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.16).move_to(treated_card8)

        control_content8 = VGroup(
            MathTex(r"T=0").set_color(LIBRARY_COLOR).scale(0.78),
            Text("No tablet", font_size=22, color=LIBRARY_COLOR, weight=BOLD),
            Text("Control group", font_size=19, color=WHITE),
            Text("Average scores", font_size=20, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.16).move_to(control_card8)

        card_equal = MathTex(r"\approx").scale(1.3).set_color(ACCENT_COLOR)
        card_equal.move_to(ORIGIN + DOWN * 0.3)

        # Beat 6:
        comparable_badge = RoundedRectangle(
            width=5.0, height=0.9, corner_radius=0.22,
            stroke_color=ACCENT_COLOR, stroke_width=2.5,
            fill_color=ACCENT_COLOR, fill_opacity=0.1,
        )
        comparable_label = Text("Comparable", font_size=30, color=ACCENT_COLOR, weight=BOLD)
        comparable_badge.move_to(comparable_label)
        comparable_group = VGroup(comparable_badge, comparable_label)
        comparable_group.to_edge(DOWN, buff=0.65)

        # Beat 7:
        result_att = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
        ).scale(1.05)
        result_att[2].set_color(ACCENT_COLOR)
        result_att.move_to(ORIGIN + UP * 0.45)

        bias_zero_condition = MathTex(
            r"\because\;E[Y_0\mid T=1]=E[Y_0\mid T=0]"
        ).scale(0.75).set_color(NEUTRAL_COLOR)
        bias_zero_condition.next_to(result_att, DOWN, buff=0.5)

        # Beat 8:
        result_att_atc = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
            r"=",
            r"ATC",
        ).scale(1.0)
        result_att_atc[2].set_color(ACCENT_COLOR)
        result_att_atc[4].set_color(LIBRARY_COLOR)
        result_att_atc.move_to(ORIGIN + UP * 0.45)

        atc_condition = MathTex(
            r"\because\;E[Y_1-Y_0\mid T=1]=E[Y_1-Y_0\mid T=0]"
        ).scale(0.72).set_color(NEUTRAL_COLOR)
        atc_condition.next_to(result_att_atc, DOWN, buff=0.5)

        # Beat 9:
        result_full = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
            r"=",
            r"ATC",
            r"=",
            r"ATE",
        ).scale(0.95)
        result_full[2].set_color(ACCENT_COLOR)
        result_full[4].set_color(LIBRARY_COLOR)
        result_full[6].set_color(YELLOW_E)
        result_full.move_to(ORIGIN + UP * 0.45)

        # Beat 10:
        summary_text = Text(
            "Comparability",
            font_size=46,
            color=ACCENT_COLOR,
            weight=BOLD,
        )
        summary_text.move_to(ORIGIN + UP * 0.5)
        arrow_down = Arrow(
            summary_text.get_bottom() + DOWN * 0.1,
            summary_text.get_bottom() + DOWN * 0.85,
            color=WHITE,
            stroke_width=2.5,
        )
        causation_text = Text(
            "Association = Causation",
            font_size=28,
            color=WHITE,
        )
        causation_text.next_to(arrow_down, DOWN, buff=0.22)

        # Beat 11:
        next_question = Text(
            "How can we create\ncomparable groups in practice?",
            font_size=32,
            color=QUESTION_COLOR,
            weight=BOLD,
            line_spacing=1.2,
        )
        next_question.move_to(ORIGIN)

        # ── Beat 1 ──
        self.play(FadeIn(question, scale=0.9), run_time=0.85)
        wait_for_chunks([1], spent=0.85)

        # ── Beat 2 ──
        self.play(FadeOut(question, scale=0.95), run_time=0.4)
        self.play(FadeIn(decomp_summary_recall, shift=UP * 0.07), run_time=0.75)
        self.play(
            FadeIn(att_recall_detail, shift=UP * 0.06),
            FadeIn(bias_recall_detail, shift=UP * 0.06),
            run_time=0.6,
        )
        self.play(Indicate(decomp_summary_recall[2], color=ACCENT_COLOR, scale_factor=1.04), run_time=0.5)
        self.play(Indicate(decomp_summary_recall[4], color=QUESTION_COLOR, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([2], spent=2.25)

        # ── Beat 3 ──
        self.play(
            Indicate(decomp_summary_recall[4], color=QUESTION_COLOR, scale_factor=1.15),
            Indicate(bias_recall_detail, color=QUESTION_COLOR, scale_factor=1.08),
            run_time=0.65,
        )
        self.play(FadeIn(bias_zero, shift=UP * 0.07), run_time=0.55)
        wait_for_chunks([3], spent=1.2)

        # ── Beat 4 ──
        self.play(
            FadeOut(decomp_recall_group),
            FadeOut(bias_zero),
            run_time=0.55,
        )
        self.play(FadeIn(comparability_formula, shift=UP * 0.07), run_time=0.75)
        self.play(Indicate(comparability_formula[0], color=TABLET_COLOR, scale_factor=1.04), run_time=0.5)
        self.play(Indicate(comparability_formula[2], color=LIBRARY_COLOR, scale_factor=1.04), run_time=0.5)
        wait_for_chunks([4], spent=2.3)

        # ── Beat 5 ──
        self.play(Transform(comparability_formula, comparability_small), run_time=0.6)
        self.play(
            FadeIn(treated_card8, scale=0.95),
            FadeIn(control_card8, scale=0.95),
            FadeIn(treated_content8, shift=UP * 0.07),
            FadeIn(control_content8, shift=UP * 0.07),
            run_time=0.9,
        )
        self.play(FadeIn(card_equal, scale=0.9), run_time=0.5)
        wait_for_chunks([5], spent=2.0)

        # ── Beat 6 ──
        self.play(FadeIn(comparable_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(comparable_badge, color=ACCENT_COLOR, scale_factor=1.03), run_time=0.55)
        wait_for_chunks([6], spent=1.15)

        # ── Beat 7 ──
        self.play(
            FadeOut(treated_card8),
            FadeOut(control_card8),
            FadeOut(treated_content8),
            FadeOut(control_content8),
            FadeOut(card_equal),
            FadeOut(comparable_group),
            FadeOut(comparability_formula),
            run_time=0.65,
        )
        self.play(FadeIn(result_att, shift=UP * 0.07), run_time=0.75)
        self.play(FadeIn(bias_zero_condition, shift=UP * 0.06), run_time=0.55)
        wait_for_chunks([7], spent=1.3)

        # ── Beat 8 ──
        self.play(
            TransformMatchingTex(result_att, result_att_atc),
            FadeOut(bias_zero_condition),
            run_time=0.85,
        )
        self.play(FadeIn(atc_condition, shift=UP * 0.06), run_time=0.55)
        self.play(
            Indicate(result_att_atc[2], color=ACCENT_COLOR, scale_factor=1.04),
            Indicate(result_att_atc[4], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        wait_for_chunks([8], spent=2.0)

        # ── Beat 9 ──
        self.play(
            TransformMatchingTex(result_att_atc, result_full),
            FadeOut(atc_condition),
            run_time=0.85,
        )
        self.play(Indicate(result_full[6], color=YELLOW_E, scale_factor=1.06), run_time=0.55)
        wait_for_chunks([9], spent=1.4)

        # ── Beat 10 ──
        self.play(FadeOut(result_full), run_time=0.55)
        self.play(FadeIn(summary_text, scale=0.9), run_time=0.7)
        self.play(GrowArrow(arrow_down), run_time=0.5)
        self.play(FadeIn(causation_text, shift=UP * 0.06), run_time=0.5)
        wait_for_chunks([10], spent=2.25)

        # ── Beat 11 ──
        self.play(
            FadeOut(summary_text),
            FadeOut(arrow_down),
            FadeOut(causation_text),
            run_time=0.55,
        )
        self.play(FadeIn(next_question, scale=0.9), run_time=0.8)
        wait_for_chunks([11], spent=0.8)
        self.wait(self.WAIT_TAIL)
