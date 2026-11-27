"""Set up the tablet decision with the four-school example in notebook cell 10."""

from pathlib import Path
import sys

from manim import (
    DOWN, RIGHT, UP, Create, DashedLine, FadeIn, FadeOut, LaggedStart,
    Line, TransformFromCopy, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))

from visual import GRID, INK, MUTED, TREATED, LessonScene, ScoreRuler, ink, tabler_icon


def outline_icon(name, height, color, stroke_width=3):
    return (
        tabler_icon(name)
        .set_height(height)
        .set_fill(opacity=0)
        .set_stroke(color, width=stroke_width)
    )


class Scene01(LessonScene):
    def construct(self):
        clock = self.clock("01_the_purchase")
        with clock.beat() as duration:
            self.show_budget_decision(duration)
        with clock.beat() as duration:
            group_labels = self.show_observed_gap(duration)
        with clock.beat() as duration:
            self.revisit_group_labels(group_labels, duration)
        clock.finish()

    def show_budget_decision(self, duration):
        receipt = outline_icon("receipt", 0.44, MUTED, stroke_width=2.5)
        budget = VGroup(receipt, ink("School budget", 27, MUTED))
        budget.arrange(RIGHT, buff=0.18).move_to([0, 2.30, 0])

        def option(name, label, x, color):
            icon = outline_icon(name, 1.62, color).move_to([x, 0.10, 0])
            return VGroup(icon, ink(label, 36, color).next_to(icon, DOWN, buff=0.26))

        tablets = option("device-tablet", "Tablets", -2.45, TREATED)
        library = option("books", "Library", 2.45, INK)
        separator = ink("or", 27, MUTED).move_to([0, 0.10, 0])
        stem = Line([0, 1.94, 0], [0, 1.44, 0], color=GRID, stroke_width=1.6)
        arms = VGroup(
            Line([0, 1.44, 0], [-2.45, 1.44, 0], color=GRID, stroke_width=1.6),
            Line([0, 1.44, 0], [2.45, 1.44, 0], color=GRID, stroke_width=1.6),
        )
        legs = VGroup(
            Line([-2.45, 1.44, 0], [-2.45, 1.13, 0], color=GRID, stroke_width=1.6),
            Line([2.45, 1.44, 0], [2.45, 1.13, 0], color=GRID, stroke_width=1.6),
        )
        self.play(FadeIn(budget, shift=0.06 * UP), Create(stem), run_time=0.10 * duration)
        self.wait(0.06 * duration)
        self.play(Create(arms[0]), Create(legs[0]), FadeIn(tablets), run_time=0.11 * duration)
        self.wait(0.08 * duration)
        self.play(
            Create(arms[1]), Create(legs[1]), FadeIn(library), FadeIn(separator),
            run_time=0.11 * duration,
        )
        self.wait(0.11 * duration)
        self.play(
            library[0].animate.set_stroke(opacity=0.32),
            library[1].animate.set_opacity(0.38),
            separator.animate.set_opacity(0.32),
            run_time=0.14 * duration,
        )
        self.budget_art = VGroup(budget, stem, arms, legs, tablets, library, separator)

    def show_observed_gap(self, duration):
        ruler = ScoreRuler()
        upper, lower, axis_y = ruler.UPPER_ROW, ruler.LOWER_ROW, ruler.AXIS_Y
        treated_heading = ruler.lane("With tablets", upper, TREATED)
        other_heading = ruler.lane("Without tablets", lower, MUTED)
        average_heading = ruler.lane("Average score", axis_y, INK)
        treated_marks = VGroup(
            ruler.point(600, upper, TREATED),
            ruler.point(750, upper, TREATED),
        )
        other_marks = VGroup(
            ruler.point(500, lower, MUTED),
            ruler.point(600, lower, MUTED),
        )
        treated_mean = ruler.mean(675, TREATED)
        other_mean = ruler.mean(550, MUTED)
        arrow, delta = ruler.contrast(550, 675)

        def guide(score, color):
            return DashedLine(
                ruler.at(score, axis_y + 0.12), ruler.at(score, -0.85),
                color=color, stroke_width=1.6, dash_length=0.055,
            )

        self.play(FadeOut(self.budget_art), FadeIn(ruler.axis()), run_time=0.07 * duration)
        self.play(
            FadeIn(treated_heading), FadeIn(other_heading),
            LaggedStart(
                *(FadeIn(group, shift=0.06 * UP) for group in (*treated_marks, *other_marks)),
                lag_ratio=0.13,
            ),
            run_time=0.11 * duration,
        )
        self.wait(0.14 * duration)
        self.show_mean(treated_marks, treated_mean, 0.10 * duration, first_label=average_heading)
        self.wait(0.12 * duration)
        self.show_mean(other_marks, other_mean, 0.09 * duration)
        self.wait(0.08 * duration)
        self.play(
            Create(guide(550, MUTED)), Create(guide(675, TREATED)),
            Create(arrow), FadeIn(delta, shift=0.06 * UP),
            run_time=0.12 * duration,
        )
        return treated_heading, other_heading

    def show_mean(self, points, mean, duration, first_label=None):
        marker, number = mean
        duplicate = marker.copy()
        self.play(
            TransformFromCopy(points[0][0], marker),
            TransformFromCopy(points[1][0], duplicate),
            run_time=0.68 * duration,
        )
        self.remove(duplicate)
        labels = [FadeIn(number)]
        if first_label is not None:
            labels.append(FadeIn(first_label))
        self.play(*labels, run_time=0.32 * duration)

    def revisit_group_labels(self, headings, duration):
        treated_heading, other_heading = headings
        self.wait(0.44 * duration)
        self.play(
            treated_heading.animate.set_color(INK), other_heading.animate.set_color(INK),
            run_time=0.13 * duration,
        )
        self.wait(0.24 * duration)
        self.play(
            treated_heading.animate.set_color(TREATED), other_heading.animate.set_color(MUTED),
            run_time=0.12 * duration,
        )
