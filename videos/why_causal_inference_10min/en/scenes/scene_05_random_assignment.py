"""Visible chance imbalances, followed by the randomized mean comparison."""

from pathlib import Path
import sys

import numpy as np
from manim import (
    AnimationGroup, Arrow, Create, DashedLine, Dot, DOWN, FadeIn, FadeOut, GrowFromCenter, LaggedStart,
    LEFT, Line, MoveAlongPath, ReplacementTransform, RIGHT, Succession, UP, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from visual import GHOST, GOLD, GRAY, GRID, INK, MUTED, TREATED, LessonScene, ink
from scene_04_resources import intake_row


LEFT_GROUP = (-4.85, -3.78, -2.71, -1.64)
RIGHT_GROUP = (1.64, 2.71, 3.78, 4.85)
FIRST_DRAW = (0, 1, 2, 4)
SECOND_DRAW = (1, 4, 5, 7)


class Scene05(LessonScene):
    def construct(self):
        clock = self.clock("05_random_assignment")
        schools = intake_row()
        self.add(schools)

        group_headings = VGroup(
            ink("Tablets", 42, TREATED).move_to([-3.25, 2.22, 0]),
            ink("No tablets", 42, GRAY).move_to([3.25, 2.22, 0]),
        )
        divider = Line([0, -0.33, 0], [0, 1.53, 0], color=GRID, stroke_width=2)
        lottery_label = ink("Draw school names", 36, GOLD).move_to([0, -0.52, 0])
        chance_label = ink("Same chance for every school", 28, GOLD).move_to([0, -1.12, 0])

        def split(treated, *, marks=schools, height=0.87):
            control = tuple(i for i in range(len(marks)) if i not in treated)
            lift, slide, land = [], [], []
            for index, x in zip(treated + control, LEFT_GROUP + RIGHT_GROUP, strict=True):
                mark = marks[index]
                start = mark.get_center()
                end = np.array([x, height, 0])
                if start[0] * x < 0:
                    # Send opposite traffic down separate horizontal lanes.
                    offset = (0.94 if x > 0 else -0.97) * UP
                    start_lane = start + offset
                    end_lane = end + offset
                    lift.append(MoveAlongPath(mark, Line(start, start_lane)))
                    slide.append(MoveAlongPath(mark, Line(start_lane, end_lane)))
                    land.append(MoveAlongPath(mark, Line(end_lane, end)))
                else:
                    slide.append(mark.animate.move_to(end))
            return Succession(
                AnimationGroup(*lift, run_time=0.25),
                AnimationGroup(*slide, run_time=0.50),
                AnimationGroup(*land, run_time=0.25),
            )

        with clock.beat() as duration:
            self.wait(0.16 * duration)
            self.play(FadeIn(lottery_label, shift=0.08 * UP), run_time=0.07 * duration)
            self.wait(0.045 * duration)
            self.play(FadeOut(lottery_label), run_time=0.055 * duration)
            self.play(split(FIRST_DRAW), run_time=0.19 * duration)
            self.play(FadeIn(group_headings), Create(divider), run_time=0.07 * duration)
            self.play(FadeIn(chance_label, shift=0.08 * UP), run_time=0.08 * duration)
            self.wait(0.22 * duration)

        left_node = ink("Tablet assignment", 26, TREATED).move_to([-3.25, -1.77, 0])
        right_node = ink("Test scores", 26, INK).move_to([3.25, -1.77, 0])
        resource_node = ink("Resources", 30, GHOST).move_to([0, -0.56, 0])
        former_link = DashedLine([-0.93, -0.82, 0], [-2.92, -1.50, 0],
                                 color=GRID, stroke_width=2.5, dash_length=0.10)
        remaining_link = Arrow([0.93, -0.82, 0], [2.92, -1.50, 0], buff=0,
                               color=GHOST, stroke_width=3.4, tip_length=0.16)
        cancel = ink("×", 38, GOLD).move_to(former_link.get_center())
        with clock.beat() as duration:
            self.play(
                FadeOut(chance_label), FadeOut(divider), FadeIn(resource_node),
                FadeIn(left_node), FadeIn(right_node), run_time=0.10 * duration,
            )
            self.play(Create(former_link), run_time=0.09 * duration)
            self.play(FadeIn(cancel, scale=0.86), former_link.animate.set_opacity(0.30),
                      run_time=0.10 * duration)
            self.wait(0.12 * duration)
            self.play(Create(remaining_link), run_time=0.12 * duration)

        def resource_count(left, right, caption):
            texts = VGroup(
                ink(f"{left} with larger budgets", 29, GHOST).move_to([-3.25, -0.21, 0]),
                ink(f"{right} with larger budgets", 29, GHOST).move_to([3.25, -0.21, 0]),
            )
            tag = ink(caption, 25, MUTED).move_to([0, -1.38, 0])
            return VGroup(texts, tag)

        first_counts = resource_count(3, 1, "One possible draw")
        second_counts = resource_count(1, 3, "Another possible draw")
        long_run = ink("Balanced on average", 34, GHOST).move_to([0, -1.38, 0])
        with clock.beat() as duration:
            self.play(
                FadeOut(VGroup(left_node, right_node, resource_node, former_link,
                               remaining_link, cancel)),
                FadeIn(first_counts),
                run_time=0.10 * duration,
            )
            self.wait(0.27 * duration)
            self.play(FadeOut(first_counts), FadeOut(group_headings), run_time=0.06 * duration)
            self.play(split(SECOND_DRAW), run_time=0.19 * duration)
            self.play(FadeIn(second_counts), FadeIn(group_headings), run_time=0.08 * duration)
            self.wait(0.11 * duration)
            self.play(FadeOut(second_counts), FadeIn(long_run), run_time=0.11 * duration)

        # Geometry is illustrative. Remove budget markers and show one score
        # per assigned school before calculating either group's average.
        score_positions = {
            0: 1.95, 1: 2.45, 2: 0.40, 3: -0.65, 4: 1.40, 5: 0.20,
            6: -2.70, 7: -1.10,
        }
        dots = VGroup()
        for index in range(len(schools)):
            assigned = index in SECOND_DRAW
            color = TREATED if assigned else GRAY
            height = 0.92 if assigned else -0.05
            dots.add(Dot([score_positions[index], height, 0], radius=0.076, color=color))

        score_lanes = VGroup(
            Line([-3.75, 0.92, 0], [3.75, 0.92, 0], color=GRID, stroke_width=2),
            Line([-3.75, -0.05, 0], [3.75, -0.05, 0], color=GRID, stroke_width=2),
        )
        revised_headings = VGroup(
            ink("Tablets", 32, TREATED).move_to([-6.10, 0.92, 0], aligned_edge=LEFT),
            ink("No tablets", 32, GRAY).move_to([-6.10, -0.05, 0], aligned_edge=LEFT),
        )
        no_tablets_mean = np.mean([score_positions[i] for i in range(8) if i not in SECOND_DRAW])
        tablets_mean = np.mean([score_positions[i] for i in SECOND_DRAW])
        # Maintain direction as treated minus control. The magnitude and sign
        # are for a schematic example without measurement units on the axis.
        axis_y = -1.18
        mean_control = Dot([no_tablets_mean, axis_y, 0], radius=0.09, color=GRAY)
        mean_treated = Dot([tablets_mean, axis_y, 0], radius=0.09, color=TREATED)
        delta = Arrow(mean_control.get_center(), mean_treated.get_center(), buff=0.045,
                      stroke_width=3.4, color=GOLD, max_tip_length_to_length_ratio=0.26)
        mean_heading = ink("Average score", 27, MUTED).move_to([-6.10, axis_y, 0], aligned_edge=LEFT)
        gap_text = ink("Estimated average effect", 29, GOLD).move_to([0, -1.78, 0])
        trial = ink("Randomized controlled trial", 44, INK).move_to([0, 2.33, 0])
        schematic = ink("Illustrative test scores", 21, MUTED).move_to([0, 1.52, 0])
        with clock.beat() as duration:
            self.play(
                FadeOut(long_run),
                ReplacementTransform(group_headings, revised_headings),
                FadeIn(score_lanes),
                FadeIn(schematic),
                LaggedStart(*(ReplacementTransform(school, dot) for school, dot in zip(schools, dots)),
                            lag_ratio=0.045),
                run_time=0.14 * duration,
            )
            self.wait(0.22 * duration)

            def copies_to_mean(indices, destination):
                copies = VGroup(*(dots[index].copy() for index in indices))
                self.add(*copies)
                moving = [dot.animate.move_to(destination.get_center()) for dot in copies]
                return copies, moving

            controls = tuple(i for i in range(8) if i not in SECOND_DRAW)
            control_copies, control_moves = copies_to_mean(controls, mean_control)
            self.play(*control_moves, run_time=0.09 * duration)
            self.remove(*control_copies)
            self.add(mean_control)
            self.play(FadeIn(mean_heading), run_time=0.05 * duration)
            self.wait(0.11 * duration)

            treated_copies, treated_moves = copies_to_mean(SECOND_DRAW, mean_treated)
            self.play(*treated_moves, run_time=0.09 * duration)
            self.remove(*treated_copies)
            self.add(mean_treated)
            self.play(Create(delta), FadeIn(gap_text), run_time=0.07 * duration)
            self.wait(0.09 * duration)
            self.play(FadeIn(trial, shift=0.08 * UP), run_time=0.07 * duration)
        example_headings = VGroup(
            ink("Tablets", 38, TREATED).move_to([-3.25, 2.22, 0]),
            ink("No tablets", 38, GRAY).move_to([3.25, 2.22, 0]),
        )
        demonstration = ink("Toy example", 35, INK).move_to([0, 2.91, 0])
        no_effect = ink("True tablet effect  =  0", 28, GHOST).move_to([0, -2.34, 0])
        stocked_schools = intake_row()
        school_scores = VGroup(*(
            VGroup(school, ink("80" if index < 4 else "60", 27, GHOST if index < 4 else GRAY)
                   .next_to(school, DOWN, buff=0.17))
            for index, school in enumerate(stocked_schools)
        ))
        first_draw = ink("First draw", 25, MUTED).move_to([0, 1.60, 0])
        next_draw = ink("Second draw", 25, MUTED).move_to(first_draw)
        group_average_labels = (
            ink("75  average", 33, TREATED).move_to([-3.25, -0.72, 0]),
            ink("65  average", 33, GRAY).move_to([3.25, -0.72, 0]),
        )
        example_chart = VGroup(revised_headings, score_lanes, schematic, mean_control, mean_treated,
                               delta, mean_heading, gap_text, trial)
        with clock.beat() as duration:
            self.play(
                FadeOut(example_chart),
                FadeIn(demonstration, shift=0.06 * UP),
                LaggedStart(*(ReplacementTransform(dot, mark[0]) for dot, mark in
                              zip(dots, school_scores, strict=True)), lag_ratio=0.044),
                run_time=0.10 * duration,
            )
            self.wait(0.11 * duration)
            self.play(
                LaggedStart(*(FadeIn(mark[1], shift=0.06 * UP) for mark in school_scores[:4]),
                            lag_ratio=0.09),
                run_time=0.08 * duration,
            )
            self.wait(0.075 * duration)
            self.play(
                LaggedStart(*(FadeIn(mark[1], shift=0.06 * UP) for mark in school_scores[4:]),
                            lag_ratio=0.09),
                run_time=0.08 * duration,
            )
            self.wait(0.06 * duration)
            self.play(FadeIn(no_effect, shift=0.07 * UP), run_time=0.08 * duration)
            self.wait(0.075 * duration)
            self.play(
                split(FIRST_DRAW, marks=school_scores, height=0.62), run_time=0.14 * duration,
            )
            self.play(FadeIn(first_draw), FadeIn(example_headings), run_time=0.075 * duration)
            self.play(
                LaggedStart(*(FadeIn(label, shift=0.06 * UP) for label in group_average_labels),
                            lag_ratio=0.19),
                run_time=0.10 * duration,
            )

        def estimate(value):
            return VGroup(ink(value, 42, GOLD), ink("estimated gap", 24, MUTED)).arrange(
                DOWN, buff=0.085,
            ).move_to([0, -1.55, 0])

        plus_ten = estimate("+10")
        minus_ten = estimate("−10")
        updated_averages = (
            ink("65  average", 33, TREATED).move_to(group_average_labels[0]),
            ink("75  average", 33, GRAY).move_to(group_average_labels[1]),
        )
        with clock.beat() as duration:
            self.play(
                GrowFromCenter(plus_ten[0]),
                FadeIn(plus_ten[1], shift=0.06 * UP),
                run_time=0.11 * duration,
            )
            self.wait(0.17 * duration)
            self.play(
                FadeOut(VGroup(*group_average_labels, first_draw, plus_ten, example_headings)),
                run_time=0.07 * duration,
            )
            self.play(
                split(SECOND_DRAW, marks=school_scores, height=0.62),
                run_time=0.14 * duration,
            )
            self.play(
                *(FadeIn(label) for label in updated_averages), FadeIn(minus_ten), FadeIn(next_draw),
                FadeIn(example_headings), run_time=0.085 * duration,
            )
            self.wait(0.15 * duration)
            recap = VGroup(
                VGroup(ink("+10", 34, GOLD), ink("first draw", 22, MUTED)).arrange(DOWN, buff=0.085),
                VGroup(ink("−10", 34, GOLD), ink("second draw", 22, MUTED)).arrange(DOWN, buff=0.085),
            ).arrange(RIGHT, buff=1.10).move_to([0, -1.55, 0])
            self.play(
                ReplacementTransform(minus_ten, recap[1]),
                FadeIn(recap[0]),
                run_time=0.10 * duration,
            )
        clock.finish()
