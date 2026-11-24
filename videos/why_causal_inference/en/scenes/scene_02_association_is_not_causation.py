from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_icon,
    load_scene_timing_durations,
    make_academic_outcome_icon,
    make_tablet_icon,
)


class Scene02_AssociationIsNotCausation(Scene):
    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("02_association_is_not_causation", language="en")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        left_icon = make_tablet_icon(TABLET_COLOR)
        left_icon.move_to(LEFT * 2.55 + DOWN * 0.1)
        right_icon = make_academic_outcome_icon(WHITE)
        right_icon.move_to(RIGHT * 2.55 + DOWN * 0.1)
        relation_arrow = Arrow(
            left_icon.get_right() + RIGHT * 0.1,
            right_icon.get_left() + LEFT * 0.1,
            buff=0.08,
            stroke_width=4,
            color=ACCENT_COLOR,
        )
        left_label = Text("Tablet given", font_size=24, color=TABLET_COLOR, weight=BOLD)
        left_label.next_to(left_icon, DOWN, buff=0.26)
        right_label = Text("High scores", font_size=24, color=ACCENT_COLOR, weight=BOLD)
        right_label.next_to(right_icon, DOWN, buff=0.26)

        confounder_chips = VGroup(
            VGroup(load_icon("coin.svg", GOLD_E, 0.55), Text("Funding", font_size=19, color=GOLD_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
            VGroup(load_icon("school-bell.svg", BLUE_E, 0.55), Text("Tutoring", font_size=19, color=BLUE_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
            VGroup(load_icon("users-group.svg", GREEN_E, 0.62), Text("Teachers", font_size=19, color=GREEN_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.38)
        confounder_title = Text("School conditions", font_size=24, color=WHITE, weight=BOLD)
        confounder_title.next_to(confounder_chips, UP, buff=0.22)
        confounder_box = RoundedRectangle(
            width=5.9,
            height=1.75,
            corner_radius=0.18,
            stroke_color=NEUTRAL_COLOR,
            stroke_width=2.2,
        )
        confounder_group = VGroup(confounder_box, confounder_title, confounder_chips)
        confounder_group.move_to(UP * 2.05)

        backdoor_left = CurvedArrow(
            confounder_group.get_bottom() + LEFT * 1.2,
            left_icon.get_top() + UP * 0.05,
            angle=0.32,
            color=NEUTRAL_COLOR,
            stroke_width=3.2,
        )
        backdoor_right = CurvedArrow(
            confounder_group.get_bottom() + RIGHT * 1.2,
            right_icon.get_top() + UP * 0.05,
            angle=-0.32,
            color=NEUTRAL_COLOR,
            stroke_width=3.2,
        )

        assoc = VGroup(
            Text("Correlation", font_size=34, color=WHITE, weight=BOLD),
            MathTex(r"\ne").scale(1.15).set_color(QUESTION_COLOR),
            Text("Causation", font_size=34, color=QUESTION_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.28)
        assoc.move_to(UP * 1.85)
        foot = Text("We can't attribute this to the tablet alone.", font_size=20, color=NEUTRAL_COLOR)
        foot.next_to(assoc, DOWN, buff=0.34)

        # Beat 1:
        self.play(FadeIn(left_icon, scale=0.9), FadeIn(right_icon, scale=0.9), run_time=0.9)
        self.play(
            GrowArrow(relation_arrow),
            FadeIn(left_label, shift=UP * 0.08),
            FadeIn(right_label, shift=UP * 0.08),
            run_time=0.9,
        )
        wait_for_chunks([1], spent=1.8)

        # Beat 2:
        self.play(FadeIn(confounder_group, shift=DOWN * 0.12), run_time=0.9)
        self.play(Create(backdoor_left), Create(backdoor_right), run_time=0.9)
        wait_for_chunks([2], spent=1.8)

        # Beat 3:
        self.play(
            FadeOut(relation_arrow),
            FadeOut(confounder_group),
            FadeOut(backdoor_left),
            FadeOut(backdoor_right),
            FadeOut(left_label),
            FadeOut(right_label),
            run_time=0.6,
        )
        self.play(FadeIn(assoc, shift=UP * 0.12), run_time=0.8)
        self.play(FadeIn(foot, shift=UP * 0.08), run_time=0.6)
        wait_for_chunks([3], spent=2.0)
        self.wait(self.WAIT_TAIL)
