from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_icon,
    load_scene_timing_durations,
)


class Scene04_MultiverseIteAteAtt(Scene):
    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("04_multiverse_ite_ate_att", language="en")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        ite_title = MathTex(r"ITE_i", r"=", r"Y_{1i}", r"-", r"Y_{0i}")
        ite_title.scale(1.08)
        ite_title[0].set_color(ACCENT_COLOR)
        ite_title[2].set_color(TABLET_COLOR)
        ite_title[4].set_color(LIBRARY_COLOR)
        ite_title.to_edge(UP, buff=0.65)

        left_frame = RoundedRectangle(
            width=2.55,
            height=2.6,
            corner_radius=0.18,
            stroke_color=TABLET_COLOR,
            stroke_width=2.6,
        )
        left_treat = MathTex(r"T_i = 1").scale(0.9).set_color(TABLET_COLOR)
        left_icon = load_icon("device-tablet.svg", TABLET_COLOR, 0.8)
        left_outcome = MathTex(r"Y_{1i}").scale(1.0).set_color(WHITE)
        left_group = VGroup(left_treat, left_icon, left_outcome).arrange(DOWN, buff=0.22)
        left_group.move_to(left_frame.get_center())
        left_world = VGroup(left_frame, left_group)
        left_world.move_to(LEFT * 2.2 + DOWN * 0.05)

        right_frame = RoundedRectangle(
            width=2.55,
            height=2.6,
            corner_radius=0.18,
            stroke_color=LIBRARY_COLOR,
            stroke_width=2.6,
        )
        right_treat = MathTex(r"T_i = 0").scale(0.9).set_color(LIBRARY_COLOR)
        right_icon = load_icon("device-tablet-off.svg", LIBRARY_COLOR, 0.8)
        right_outcome = MathTex(r"Y_{0i}").scale(1.0).set_color(WHITE)
        right_group = VGroup(right_treat, right_icon, right_outcome).arrange(DOWN, buff=0.22)
        right_group.move_to(right_frame.get_center())
        right_world = VGroup(right_frame, right_group)
        right_world.move_to(RIGHT * 2.2 + DOWN * 0.05)

        ite_arrow = DoubleArrow(
            left_world.get_right() + RIGHT * 0.08,
            right_world.get_left() + LEFT * 0.08,
            buff=0.1,
            stroke_width=4,
            color=ACCENT_COLOR,
        )

        ate_def = MathTex(r"ATE", r"=", r"E[Y_1 - Y_0]")
        ate_def.scale(0.98)
        ate_def[0].set_color(ACCENT_COLOR)
        ate_def.move_to(ORIGIN)
        ate_expand = VGroup(
            Text("Average", font_size=23, color=WHITE, weight=BOLD),
            Text("Treatment", font_size=23, color=ACCENT_COLOR, weight=BOLD),
            Text("Effect", font_size=23, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.16)
        ate_expand.next_to(ate_def, DOWN, buff=0.34)

        att_def = MathTex(r"ATT", r"=", r"E[Y_1 - Y_0 \mid T=1]")
        att_def.scale(0.94)
        att_def[0].set_color(QUESTION_COLOR)
        att_def.move_to(ORIGIN)
        att_expand = VGroup(
            Text("Average", font_size=22, color=WHITE, weight=BOLD),
            Text("Treatment", font_size=22, color=QUESTION_COLOR, weight=BOLD),
            Text("Effect", font_size=22, color=WHITE, weight=BOLD),
            Text("on the Treated", font_size=22, color=NEUTRAL_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.14)
        att_expand.next_to(att_def, DOWN, buff=0.34)

        avg_hint = Text("All units", font_size=25, color=NEUTRAL_COLOR, weight=BOLD)
        avg_hint.next_to(ate_expand, DOWN, buff=0.28)
        att_hint = Text("Treated units only", font_size=25, color=NEUTRAL_COLOR, weight=BOLD)
        att_hint.move_to(avg_hint)

        # Beat 1:
        self.play(FadeIn(ite_title, shift=UP * 0.08), run_time=0.8)
        self.play(
            FadeIn(left_world, shift=RIGHT * 0.18),
            FadeIn(right_world, shift=LEFT * 0.18),
            run_time=1.0,
        )
        self.play(GrowArrow(ite_arrow), run_time=0.7)
        wait_for_chunks([1, 2], spent=2.5)

        # Beat 2:
        self.play(
            FadeOut(ite_arrow),
            left_world.animate.move_to(LEFT * 2.2 + DOWN * 0.05),
            right_world.animate.move_to(RIGHT * 2.2 + DOWN * 0.05),
            run_time=0.9,
        )
        veil = Rectangle(
            width=right_world.width * 0.96,
            height=right_world.height * 0.96,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=0.62,
        ).move_to(right_world)
        eye_off = load_icon("eye-off.svg", WHITE, 0.72).move_to(right_world.get_center() + DOWN * 0.15)

        self.play(Indicate(left_world, color=TABLET_COLOR, scale_factor=1.02), run_time=0.7)
        self.play(FadeIn(veil), FadeIn(eye_off), run_time=0.6)
        wait_for_chunks([3], spent=2.2)

        # Beat 3:
        self.play(
            FadeOut(VGroup(left_world, right_world, veil, eye_off), shift=DOWN * 0.1),
            FadeOut(ite_title, shift=UP * 0.08),
            run_time=0.9,
        )
        self.play(FadeIn(ate_def, shift=UP * 0.08), run_time=0.7)
        self.play(FadeIn(ate_expand, shift=UP * 0.08), run_time=0.6)
        self.play(FadeIn(avg_hint, shift=UP * 0.08), run_time=0.6)
        wait_for_chunks([4], spent=2.8)
        self.play(
            TransformMatchingTex(ate_def, att_def),
            FadeTransform(ate_expand, att_expand),
            FadeTransform(avg_hint, att_hint),
            run_time=0.9,
        )
        wait_for_chunks([5], spent=0.9)
        self.wait(self.WAIT_TAIL)
