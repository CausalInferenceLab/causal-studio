"""From a school budget to the two paths created by a common cause."""

from pathlib import Path
import sys

import numpy as np
from manim import (
    Arrow, Create, DashedLine, DOWN, FadeIn, FadeOut, LaggedStart, Line, Polygon,
    ReplacementTransform, RIGHT, UP, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
from visual import GHOST, GOLD, GRID, INK, MUTED, TREATED, LessonScene, ink, tabler_icon


def icon(name, color, size):
    return tabler_icon(name).set_stroke(color=color, width=3).scale_to_fit_height(size)


def resource_school(level, position, *, size=0.58, color=MUTED):
    school = icon("school", color, size)
    bars = VGroup(
        *(Line([-0.075, 0, 0], [0.075, 0, 0], color=GHOST if i < level else GRID,
               stroke_width=3.8) for i in range(3))
    ).arrange(RIGHT, buff=0.06).scale(size / 0.58)
    bars.next_to(school, DOWN, buff=size * 0.24)
    return VGroup(school, bars).move_to(position)


def intake_row():
    return VGroup(
        *(resource_school(3 if i < 4 else 1, [-4.55 + i * 1.30, 0.95, 0]) for i in range(8))
    )


def labeled_icon(symbol, label, position, color):
    glyph = icon(symbol, color, 0.76).move_to(position)
    return VGroup(glyph, ink(label, 31, color).next_to(glyph, DOWN, buff=0.17))


class Scene04(LessonScene):
    def construct(self):
        clock = self.clock("04_resources")

        small_school = resource_school(1, [-2.1, 0.85, 0], size=1.10)
        large_school = resource_school(3, [2.1, 0.85, 0], size=1.10, color=INK)
        small_label = ink("Smaller budget", 31, MUTED).next_to(small_school, DOWN, buff=0.23)
        large_label = ink("Larger budget", 31, INK).next_to(large_school, DOWN, buff=0.23)

        resources = resource_school(3, [0, 1.66, 0], size=0.92, color=GHOST)
        resources_label = ink("School resources", 31, GHOST).next_to(resources, UP, buff=0.14)
        tablets = labeled_icon("device-tablet", "Tablet adoption", [-3.54, -0.51, 0], TREATED)
        support = labeled_icon("users-group", "Teaching support", [3.54, -0.51, 0], MUTED)
        scores = labeled_icon("chart-bar", "Test scores", [3.54, -0.51, 0], INK)

        # Establish the resource difference before giving the same resource
        # glyph two consequences. This leaves the two paths to the next beat.
        with clock.beat() as duration:
            self.play(FadeIn(small_school), FadeIn(large_school), run_time=0.08 * duration)
            self.play(FadeIn(small_label), FadeIn(large_label), run_time=0.06 * duration)
            self.wait(0.17 * duration)
            self.play(
                FadeOut(VGroup(small_school, small_label, large_label)),
                ReplacementTransform(large_school, resources),
                FadeIn(resources_label, shift=0.10 * UP),
                run_time=0.11 * duration,
            )
            self.play(FadeIn(tablets, shift=0.12 * DOWN), run_time=0.08 * duration)
            self.wait(0.16 * duration)
            self.play(FadeIn(support, shift=0.12 * DOWN), run_time=0.08 * duration)
            self.wait(0.10 * duration)
            self.play(ReplacementTransform(support, scores), run_time=0.08 * duration)

        branch_left = Arrow([-0.68, 1.26, 0], [-2.96, -0.30, 0], buff=0,
                            color=GHOST, stroke_width=3.6, max_tip_length_to_length_ratio=0.10)
        branch_right = Arrow([0.68, 1.26, 0], [2.96, -0.30, 0], buff=0,
                             color=GHOST, stroke_width=3.6, max_tip_length_to_length_ratio=0.10)
        common_cause = ink("Common cause", 24, GHOST).move_to([0, 0.38, 0])
        with clock.beat() as duration:
            self.wait(0.07 * duration)
            self.play(Create(branch_left), run_time=0.10 * duration)
            self.wait(0.05 * duration)
            self.play(Create(branch_right), run_time=0.10 * duration)
            self.wait(0.20 * duration)
            self.play(
                resources.animate.scale(1.07),
                FadeIn(common_cause, shift=0.075 * UP),
                run_time=0.07 * duration,
            )
            self.wait(0.21 * duration)
            self.play(resources.animate.scale(1 / 1.07), run_time=0.06 * duration)

        effect_start = np.array([-2.75, -0.50, 0])
        effect_end = np.array([2.75, -0.50, 0])
        effect_line = DashedLine(effect_start, effect_end, dash_length=0.10,
                                 dashed_ratio=0.52, color=GOLD, stroke_width=3.2)
        effect_tip = Polygon(
            effect_end, effect_end - 0.18 * RIGHT + 0.065 * UP,
            effect_end - 0.18 * RIGHT - 0.065 * UP,
        ).set_fill(GOLD, opacity=1).set_stroke(width=0)
        effect_path = VGroup(effect_line, effect_tip)
        effect_label = ink("Effect of tablets?", 30, GOLD).move_to([0, -1.08, 0])
        next_schools = intake_row()
        with clock.beat() as duration:
            self.play(
                branch_left.animate.set_opacity(0.32),
                branch_right.animate.set_opacity(0.32),
                FadeOut(common_cause),
                Create(effect_path),
                FadeIn(effect_label, shift=0.08 * UP),
                run_time=0.10 * duration,
            )
            self.wait(0.48 * duration)
            self.play(
                FadeOut(VGroup(resources_label, tablets, scores, branch_left, branch_right,
                               effect_path, effect_label)),
                ReplacementTransform(resources, next_schools[3]),
                LaggedStart(*(FadeIn(school, shift=0.05 * UP) for i, school in enumerate(next_schools)
                              if i != 3), lag_ratio=0.07),
                run_time=0.15 * duration,
            )
        clock.finish()
