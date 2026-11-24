from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_icon,
    load_scene_timing_durations,
    make_tablet_icon,
    make_world_panel,
)


class Scene03_CounterfactualWorlds(Scene):
    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("03_counterfactual_worlds", language="en")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        treatment_seed = MathTex(r"T_i").scale(1.45).set_color(TABLET_COLOR)
        treatment_seed.move_to(LEFT * 2.35 + UP * 0.45)
        treatment_word = Text("Treatment", font_size=24, color=WHITE, weight=BOLD)
        treatment_word.next_to(treatment_seed, DOWN, buff=0.2)

        treatment_yes = VGroup(
            MathTex(r"T_i = 1").set_color(TABLET_COLOR),
            make_tablet_icon(TABLET_COLOR),
        ).arrange(RIGHT, buff=0.2)
        treatment_yes.move_to(RIGHT * 1.45 + UP * 1.45)

        treatment_no = VGroup(
            MathTex(r"T_i = 0").set_color(LIBRARY_COLOR),
            load_icon("device-tablet-off.svg", LIBRARY_COLOR, 1.45),
        ).arrange(RIGHT, buff=0.2)
        treatment_no.move_to(RIGHT * 1.45 + DOWN * 0.6)

        up_arrow = CurvedArrow(
            treatment_seed.get_right() + RIGHT * 0.05 + UP * 0.12,
            treatment_yes.get_left() + LEFT * 0.12 + DOWN * 0.04,
            angle=-0.52,
            stroke_width=3.6,
            color=TABLET_COLOR,
        )
        down_arrow = CurvedArrow(
            treatment_seed.get_right() + RIGHT * 0.05 + DOWN * 0.12,
            treatment_no.get_left() + LEFT * 0.12 + UP * 0.04,
            angle=0.52,
            stroke_width=3.6,
            color=LIBRARY_COLOR,
        )

        outcome_def = VGroup(
            MathTex(r"Y_i").scale(1.2).set_color(ACCENT_COLOR),
            Text("Academic achievement", font_size=22, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.22)
        outcome_def.move_to(UP * 0.45)
        outcome_icon = load_icon("school.svg", ACCENT_COLOR, 1.05)
        outcome_icon.next_to(outcome_def, DOWN, buff=0.34)

        treatment_group = VGroup(
            treatment_seed,
            treatment_word,
            up_arrow,
            down_arrow,
            treatment_yes,
            treatment_no,
        )

        left_world = make_world_panel("device-tablet.svg", r"T_i = 1", r"Y_{1i}", TABLET_COLOR)
        right_world = make_world_panel("device-tablet-off.svg", r"T_i = 0", r"Y_{0i}", LIBRARY_COLOR)
        worlds = VGroup(left_world, right_world).arrange(RIGHT, buff=1.1)
        worlds.move_to(DOWN * 0.15)

        left_label = Text("factual", font_size=22, color=TABLET_COLOR, weight=BOLD)
        left_label.next_to(left_world, UP, buff=0.22)
        right_label = Text("counterfactual", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
        right_label.next_to(right_world, UP, buff=0.22)

        unseen = load_icon("eye-off.svg", NEUTRAL_COLOR, 0.78)
        unseen.next_to(right_world[0], DOWN, buff=0.18)

        impossible = Text("Both cannot be observed at once", font_size=25, color=QUESTION_COLOR, weight=BOLD)
        impossible.to_edge(DOWN, buff=0.78)
        impossible_line = Underline(impossible, color=QUESTION_COLOR, buff=0.12, stroke_width=2.4)
        counter_shade = SurroundingRectangle(
            right_world,
            buff=0.08,
            corner_radius=0.18,
            stroke_opacity=0,
            fill_color=BLACK,
            fill_opacity=0.0,
        )

        factual_world_pos = LEFT * 3.0 + DOWN * 0.08
        counter_world_pos = RIGHT * 3.0 + DOWN * 0.08

        # Intro:
        wait_for_chunks([1])

        # Beat 1:
        self.play(FadeIn(treatment_seed, scale=0.9), FadeIn(treatment_word, shift=UP * 0.08), run_time=1.0)
        self.wait(2.6)
        self.play(Create(up_arrow), Create(down_arrow), run_time=1.1)
        self.play(FadeIn(treatment_yes, shift=LEFT * 0.08), FadeIn(treatment_no, shift=LEFT * 0.08), run_time=1.0)
        self.play(
            FadeOut(treatment_group, shift=LEFT * 0.08),
            FadeIn(outcome_def, shift=UP * 0.12),
            FadeIn(outcome_icon, scale=0.9),
            run_time=1.0,
        )
        wait_for_chunks([2, 3], spent=6.7)

        # Beat 2:
        self.play(
            FadeOut(VGroup(outcome_def, outcome_icon), shift=UP * 0.1),
            FadeIn(worlds, shift=UP * 0.12),
            run_time=1.1,
        )
        wait_for_chunks([4, 5], spent=1.1)

        # Beat 3:
        self.play(
            left_world.animate.move_to(factual_world_pos),
            right_world.animate.move_to(counter_world_pos),
            FadeIn(left_label, shift=UP * 0.1),
            FadeIn(right_label, shift=UP * 0.1),
            run_time=1.1,
        )
        counter_shade.move_to(right_world)
        self.play(
            counter_shade.animate.set_fill(opacity=0.5),
            FadeIn(unseen, scale=0.9),
            FadeIn(impossible, shift=UP * 0.08),
            Create(impossible_line),
            run_time=1.0,
        )
        wait_for_chunks([6], spent=2.1)
        self.wait(self.WAIT_TAIL)
