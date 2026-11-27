"""Follow the same schools from their observed to their hypothetical scores."""

import sys
from pathlib import Path

from manim import (
    Create, DashedLine, DOWN, FadeIn, FadeOut, Indicate, Line, RIGHT, UP,
    VGroup, ValueTracker, always_redraw, smooth,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
from visual import GOLD, GRAY, GHOST, GRID, INK, TREATED, LessonScene, ScoreRuler, ink


class Scene02(LessonScene):
    def construct(self):
        clock = self.clock("02_same_schools")
        ruler = ScoreRuler()
        upper, lower, axis = ruler.UPPER_ROW, ruler.LOWER_ROW, ruler.AXIS_Y

        def guide(score, shade):
            return DashedLine(
                ruler.at(score, axis + 0.12), ruler.at(score, -0.85),
                color=shade, stroke_width=1.6, dash_length=0.055,
            )

        observed_3 = ruler.point(600, upper, TREATED)
        grouped_4 = ruler.point(750, upper, TREATED)
        alternate_3 = ruler.point(800, upper, GHOST, hollow=True)
        alternate_4 = ruler.point(700, lower, GHOST, hollow=True)
        tablet_label = ruler.lane("With tablets", upper, TREATED)
        observed_mean = ruler.mean(675, TREATED)
        observed_guide = guide(675, TREATED)
        prior_comparison = VGroup(
            ruler.lane("Without tablets", lower, GRAY),
            ruler.point(500, lower, GRAY), ruler.point(600, lower, GRAY),
            ruler.mean(550, GRAY), guide(550, GRAY), ruler.contrast(550, 675),
        )
        school_3 = ruler.lane("School 3", upper, INK)
        school_4 = ruler.lane("School 4", lower, INK)
        mean_label = ruler.lane("Average score", axis)
        question = ink("What if the same schools had no tablets?", 43).move_to([0, 2.85, 0])
        legend = VGroup(
            VGroup(ruler.mark(500, 0, TREATED), ink("With tablets", 24, TREATED)),
            VGroup(ruler.mark(500, 0, GHOST, True), ink("Without tablets (hypothetical)", 24, GHOST)),
        )
        for item in legend:
            item.arrange(RIGHT, buff=0.13)
        legend.arrange(RIGHT, buff=0.57).move_to([0, 2.14, 0])
        frame = self.camera.frame
        frame.save_state()
        axis_marks = ruler.axis()
        self.add(axis_marks, tablet_label, observed_3, grouped_4,
                 observed_mean, observed_guide, mean_label, prior_comparison)

        with clock.beat() as seconds:
            self.wait(0.11 * seconds)
            self.play(FadeOut(prior_comparison), FadeOut(tablet_label),
                      observed_guide.animate.set_opacity(0.24), run_time=0.06 * seconds)
            self.play(
                FadeIn(school_3), FadeIn(school_4),
                grouped_4.animate.shift(ruler.at(0, lower) - ruler.at(0, upper)),
                run_time=0.08 * seconds,
            )
            self.wait(0.05 * seconds)
            self.play(Indicate(observed_3[0], color=TREATED, scale_factor=1.55),
                      run_time=0.08 * seconds)
            self.wait(0.16 * seconds)
            self.play(Indicate(grouped_4[0], color=TREATED, scale_factor=1.55),
                      run_time=0.08 * seconds)
            self.wait(0.10 * seconds)
            self.play(
                FadeIn(question, shift=0.08 * UP),
                frame.animate.scale(0.965, about_point=observed_mean[0].get_center()),
                run_time=0.09 * seconds,
            )
            self.wait(0.14 * seconds)

        with clock.beat() as seconds:
            self.play(FadeIn(legend), run_time=0.07 * seconds)
            self.wait(0.10 * seconds)
            line_3 = self.reveal_alternative(observed_3, alternate_3, 0.14 * seconds)
            self.wait(0.12 * seconds)
            line_4 = self.reveal_alternative(grouped_4, alternate_4, 0.14 * seconds)
            self.wait(0.14 * seconds)
            self.play(
                alternate_3[0].animate.set_stroke(width=4.4),
                alternate_4[0].animate.set_stroke(width=4.4),
                run_time=0.10 * seconds,
            )

        with clock.beat() as seconds:
            local_3 = ruler.contrast(800, 600, "−200", GHOST, 0.83)
            local_4 = ruler.contrast(700, 750, "+50", TREATED, -0.12)
            local_3[1].scale(0.72).next_to(local_3[0], UP, buff=0.10)
            local_4[1].scale(0.72).next_to(local_4[0], DOWN, buff=0.10)
            alternate_mean = ruler.mean(750, GHOST, True)
            alternate_guide = guide(750, GHOST)
            effect = ruler.contrast(750, 675)
            detail = ink("with − without", 20, GOLD).next_to(effect[0], -UP, buff=0.16)

            self.wait(0.14 * seconds)
            self.play(FadeOut(line_3), Create(local_3[0]), FadeIn(local_3[1]), run_time=0.10 * seconds)
            self.wait(0.18 * seconds)
            self.play(FadeOut(line_4), Create(local_4[0]), FadeIn(local_4[1]), run_time=0.09 * seconds)
            self.wait(0.12 * seconds)
            self.play(FadeOut(local_3), FadeOut(local_4), run_time=0.06 * seconds)
            self.gather_mean(alternate_3[0], alternate_4[0], alternate_mean[0], 0.08 * seconds)
            self.play(
                FadeIn(alternate_mean[1]), Create(alternate_guide),
                observed_guide.animate.set_opacity(1), run_time=0.07 * seconds,
            )
            self.play(Create(effect[0]), FadeIn(effect[1]), FadeIn(detail), run_time=0.09 * seconds)

        with clock.beat() as seconds:
            unobserved = VGroup(alternate_3, alternate_4)
            label = ink("Counterfactual", 43).move_to(question)
            self.wait(0.20 * seconds)
            self.play(
                FadeOut(question), FadeOut(detail),
                unobserved.animate.set_opacity(0.35),
                run_time=0.08 * seconds,
            )
            self.wait(0.20 * seconds)
            self.play(FadeIn(label, shift=0.08 * UP), run_time=0.08 * seconds)
            self.wait(0.19 * seconds)
            self.play(
                FadeOut(unobserved), FadeOut(label), FadeOut(school_3), FadeOut(school_4),
                FadeOut(legend), FadeOut(observed_3), FadeOut(grouped_4),
                FadeOut(alternate_guide), FadeOut(observed_guide),
                frame.animate.restore(), run_time=0.11 * seconds,
            )
        last_comparison = VGroup(axis_marks, mean_label, observed_mean, alternate_mean, effect)
        last_comparison_frame = last_comparison.copy().add(detail.copy())
        scope_question = ink("Whose average effect?", 49).move_to([0, 2.60, 0])
        group_labels, values = VGroup(), VGroup()
        for index, value in enumerate(("−50", "0", "−200", "+50"), 1):
            x = (index - 2.5) * 2.32
            color = GRAY if index <= 2 else TREATED
            group_labels.add(ink(f"School {index}", 30, color).move_to([x, 0.94, 0]))
            values.add(ink(value, 53, color).move_to([x, 0.07, 0]))
        rule = Line([-4.70, -0.51, 0], [4.70, -0.51, 0], color=GRID, stroke_width=2)

        with clock.beat() as seconds:
            self.wait(0.07 * seconds)
            self.play(FadeOut(last_comparison), FadeIn(scope_question), run_time=0.08 * seconds)
            self.play(FadeIn(group_labels[2:]), FadeIn(values[2:]), run_time=0.08 * seconds)
            self.wait(0.16 * seconds)
            self.play(FadeIn(group_labels[:2]), Create(rule), run_time=0.08 * seconds)
            self.wait(0.21 * seconds)
            self.play(FadeIn(values[0], shift=0.07 * UP), run_time=0.06 * seconds)
            self.wait(0.06 * seconds)
            self.play(FadeIn(values[1], shift=0.07 * UP), run_time=0.06 * seconds)
            self.play(Indicate(values[2:], color=TREATED, scale_factor=1.12),
                      run_time=0.08 * seconds)

        with clock.beat() as seconds:
            def result(label, value):
                return VGroup(ink(label, 30), ink(value, 53, GOLD)).arrange(RIGHT, buff=0.24).move_to([0, -1.37, 0])

            all_schools = result("All four schools", "−50")
            tablets_only = result("Tablet schools", "−75")
            self.wait(0.12 * seconds)
            self.play(FadeIn(all_schools, shift=0.08 * UP), run_time=0.09 * seconds)
            self.wait(0.12 * seconds)
            self.play(FadeOut(all_schools), group_labels[:2].animate.set_opacity(0.25),
                      values[:2].animate.set_opacity(0.25), run_time=0.06 * seconds)
            self.play(FadeIn(tablets_only, shift=0.08 * UP), run_time=0.08 * seconds)
            self.wait(0.27 * seconds)
            self.play(
                FadeOut(scope_question), FadeOut(group_labels), FadeOut(values), FadeOut(rule),
                FadeOut(tablets_only), run_time=0.08 * seconds,
            )
            self.play(FadeIn(last_comparison_frame), run_time=0.09 * seconds)
        clock.finish()

    def reveal_alternative(self, observed, alternate, seconds):
        mark, value = alternate
        start = observed[0].get_center()
        destination = mark.get_center()
        displacement = destination - start
        mark.move_to(start)
        progress = ValueTracker(0)

        def connector():
            return DashedLine(
                start, start + max(0.0001, progress.get_value()) * displacement,
                color=GHOST, stroke_width=1.75, stroke_opacity=0.50, dash_length=0.09,
            ).set_z_index(-1)

        connection = always_redraw(connector)
        self.play(FadeIn(mark), run_time=0.15 * seconds)
        self.add(connection)
        mark.add_updater(lambda item: item.move_to(start + progress.get_value() * displacement))
        self.play(progress.animate.set_value(1), run_time=0.69 * seconds, rate_func=smooth)
        connection.clear_updaters()
        mark.clear_updaters()
        self.play(FadeIn(value, shift=0.07 * UP), run_time=0.16 * seconds)
        return connection

    def gather_mean(self, first, second, destination, seconds):
        copies = VGroup(first.copy(), second.copy())
        self.add(copies)
        position = destination.get_center()
        self.play(*(mark.animate.move_to(position) for mark in copies), run_time=seconds)
        self.remove(copies)
        self.add(destination)
