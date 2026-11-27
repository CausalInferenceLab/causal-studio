"""Return to the decision and close on the counterfactual comparison."""

from pathlib import Path
import sys

from manim import (
    Arrow, Circle, Create, DashedLine, Dot, DOWN, FadeIn, FadeOut, LaggedStart,
    LEFT, Line, RIGHT, Transform, UP, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
from visual import GOLD, GHOST, GRAY, GRID, INK, MUTED, TREATED, LessonScene, ScoreRuler, ink, tabler_icon


def icon(name, height, color):
    glyph = tabler_icon(name)
    return glyph.set_fill(opacity=0).set_stroke(color=color, width=3.3, opacity=1).set_height(height)


def option(name, label, x, color):
    glyph = icon(name, 1.66, color).move_to([x, 0.10, 0])
    return VGroup(glyph, ink(label, 36, color).next_to(glyph, DOWN, buff=0.24))


def symbol(name, text, x, y, color):
    glyph = icon(name, 0.47, color)
    item = VGroup(glyph, ink(text, 30, color)).arrange(RIGHT, buff=0.25)
    return item.move_to([x, y, 0])


def school(x, y, color):
    return icon("school", 0.55, color).move_to([x, y, 0])


def brace_path(x, axis_height, tail_height):
    return VGroup(
        Line([0, 1.72, 0], [0, axis_height, 0], color=GRID, stroke_width=2.1),
        Line([0, axis_height, 0], [x, axis_height, 0], color=GRID, stroke_width=2.1),
        Line([x, axis_height, 0], [x, tail_height, 0], color=GRID, stroke_width=2.1),
    )


class Scene07(LessonScene):
    def construct(self):
        clock = self.clock("07_the_question")
        budget = symbol("receipt", "School budget", 0, 2.28, MUTED)
        tablets = option("device-tablet", "Tablets", -2.45, TREATED)
        library = option("books", "Library", 2.45, GHOST)
        left_branch = brace_path(-2.45, 1.34, 1.02)
        right_branch = brace_path(2.45, 1.34, 1.02)
        either = ink("or", 28, MUTED).move_to([0, -0.26, 0])
        selection = VGroup(*(
            school((index - 2.5) * 0.66, 2.28, MUTED) for index in range(6)
        ))
        cohort_targets = [
            school(x + (index - 1) * 0.53, 1.53, color)
            for x, color in ((-2.45, TREATED), (2.45, GRAY)) for index in range(3)
        ]
        assessment = symbol("clipboard-text", "Same year-end assessment", 0, -2.03, INK)
        no_tablets = option("device-tablet", "No tablets", 2.45, GRAY)
        strike = Line([1.84, -0.41, 0], [3.02, 0.63, 0], color=GRAY, stroke_width=3.0)
        library_upgrade = option("books", "Library upgrade", 2.45, GHOST)

        with clock.beat() as duration:
            self.play(FadeIn(budget), FadeIn(tablets), FadeIn(library), FadeIn(either),
                      LaggedStart(FadeIn(left_branch), FadeIn(right_branch), lag_ratio=0.2),
                      run_time=0.90)
            self.wait(duration * 0.11)
            self.play(FadeOut(budget), FadeOut(either), FadeOut(left_branch), FadeOut(right_branch),
                      FadeIn(selection), run_time=0.80)
            self.wait(duration * 0.10)
            self.play(
                LaggedStart(*(Transform(mark, target) for mark, target in
                              zip(selection, cohort_targets, strict=True)), lag_ratio=0.10),
                FadeOut(library), FadeIn(no_tablets), Create(strike), run_time=1.55,
            )
            self.wait(duration * 0.13)
            self.play(FadeIn(assessment, shift=0.08 * UP), run_time=0.75)
            self.wait(duration * 0.21)
            self.play(FadeOut(no_tablets), FadeOut(strike), FadeIn(library_upgrade, shift=0.08 * UP),
                      *(dot.animate.set_color(GHOST).set_stroke(width=3.3) for dot in selection[3:]),
                      run_time=1.05)

        past_label = ink("Already purchased", 32, TREATED).move_to([-2.98, -0.91, 0])
        present_label = ink("Today", 32, MUTED).move_to([1.98, -0.91, 0])
        date_line = Arrow([-4.53, -0.25, 0], [4.40, -0.25, 0], color=GRID, buff=0,
                          stroke_width=2.5)
        start_tick = Line([-2.98, -0.42, 0], [-2.98, -0.08, 0], color=TREATED, stroke_width=2.4)
        end_tick = Line([1.98, -0.42, 0], [1.98, -0.08, 0], color=MUTED, stroke_width=2.4)
        purchase = icon("device-tablet", 0.89, TREATED).next_to(start_tick, UP, buff=0.21)
        cost = symbol("coins", "Cost", -1.68, 1.57, MUTED)
        ethics = symbol("scale", "Ethics", 1.41, 1.57, MUTED)

        with clock.beat() as duration:
            self.play(
                FadeOut(library_upgrade), FadeOut(tablets), FadeOut(assessment), FadeOut(selection),
                Create(date_line), run_time=0.90,
            )
            self.play(
                LaggedStart(Create(start_tick), FadeIn(purchase), FadeIn(past_label), lag_ratio=0.13),
                run_time=0.80,
            )
            self.play(Create(end_tick), FadeIn(present_label), run_time=0.65)
            self.wait(duration * 0.29)
            self.play(FadeIn(cost, shift=0.12 * UP), run_time=0.75)
            self.wait(duration * 0.18)
            self.play(FadeIn(ethics, shift=0.12 * UP), run_time=0.75)

        question = ink("Who would make a fair comparison?", 45).move_to([0, 2.25, 0])
        scale = Line([-3.97, -1.05, 0], [4.0, -1.05, 0], color=GRID, stroke_width=2.3)
        baseline = ink("Prospects before the purchase", 31, MUTED).next_to(scale, DOWN, buff=0.33)
        tablet_school = school(0.50, -0.50, TREATED)
        other_near = school(1.60, -0.50, GRAY)
        other_far = school(-2.56, -0.50, GRAY)
        comparison_box = Circle(color=GOLD, radius=0.63, stroke_width=2.2)
        comparison_box.stretch_to_fit_width(2.09).move_to([1.04, -0.48, 0])
        treated_tag = ink("Bought tablets", 27, TREATED).move_to([0.51, 0.34, 0])
        resources = symbol("coins", "School resources", -3.40, 1.04, GHOST)
        resources_link = DashedLine(resources.get_right() + RIGHT * 0.14, [-0.44, 0.23, 0],
                                    color=GHOST, stroke_width=1.6, dash_length=0.10)

        with clock.beat() as duration:
            self.play(
                FadeOut(cost), FadeOut(ethics), FadeOut(date_line), FadeOut(start_tick),
                FadeOut(end_tick), FadeOut(past_label), FadeOut(present_label), FadeOut(purchase),
                FadeIn(question), run_time=0.92,
            )
            self.wait(duration * 0.09)
            self.play(Create(scale), FadeIn(baseline), run_time=0.70)
            self.play(
                LaggedStart(FadeIn(tablet_school), FadeIn(other_far), FadeIn(other_near), lag_ratio=0.15),
                run_time=1.02,
            )
            self.wait(duration * 0.19)
            self.play(
                Create(comparison_box), FadeIn(treated_tag),
                other_far.animate.set_stroke(opacity=0.50), run_time=0.80,
            )
            self.wait(duration * 0.23)
            self.play(FadeIn(resources), Create(resources_link), run_time=0.92)
            self.wait(duration * 0.10)
            self.play(resources_link.animate.set_opacity(0.47), run_time=0.42)

        comparison_objects = VGroup(
            comparison_box, resources, resources_link, treated_tag, tablet_school,
            other_near, other_far, scale, baseline, question,
        )
        versus = ink("Change in school scores", 45).move_to([0, 2.35, 0])
        illustrative = ink("Hypothetical example", 25, MUTED).move_to([0, 1.76, 0])
        score_base = Line([-5.22, -1.49, 0], [3.40, -1.49, 0], color=GRID, stroke_width=2)
        x_year = (-4.62, -1.50, 2.52)
        years = VGroup(*(
            ink(year, 27, MUTED).move_to([x, -1.94, 0])
            for x, year in zip(x_year, ("Earlier", "Last year", "This year"), strict=True)
        ))
        t0, t1 = [-1.50, 0.16, 0], [2.52, 0.95, 0]
        n0, n1 = [-1.50, -1.00, 0], [2.52, -0.21, 0]
        tablet_trend = Line(t0, t1, color=TREATED, stroke_width=3.9)
        control_trend = Line(n0, n1, color=GRAY, stroke_width=3.6)
        tablet_ends = VGroup(*(Dot(p, radius=0.077, color=TREATED) for p in (t0, t1)))
        control_ends = VGroup(*(Dot(p, radius=0.077, color=GRAY) for p in (n0, n1)))
        changed = ink("+30", 40, TREATED).next_to(tablet_ends[1], RIGHT, buff=0.22)
        changed_no_tablets = ink("+30", 40, GRAY).next_to(control_ends[1], RIGHT, buff=0.22)
        has_tablets = ink("Bought tablets", 27, TREATED).move_to([-2.99, 0.16, 0])
        no_tablets_label = ink("No tablets", 27, GRAY).move_to([-2.99, -1.00, 0])
        easier = ink("Easier exam?", 27, MUTED).move_to([0.17, -0.97, 0])
        extra_help = ink("Extra tutoring?", 27, MUTED).move_to([0.17, -0.97, 0])

        with clock.beat() as duration:
            self.play(FadeOut(comparison_objects), FadeIn(versus), FadeIn(illustrative),
                      Create(score_base), FadeIn(years[1]), FadeIn(years[2]), run_time=0.95)
            self.wait(duration * 0.12)
            self.play(FadeIn(has_tablets), FadeIn(tablet_ends[0]),
                      Create(tablet_trend), FadeIn(tablet_ends[1]), run_time=1.50)
            self.play(FadeIn(changed), run_time=0.60)
            self.wait(duration * 0.15)
            self.play(FadeIn(easier), run_time=0.66)
            self.wait(duration * 0.13)
            self.play(FadeOut(easier), FadeIn(extra_help), run_time=0.63)
            self.wait(duration * 0.11)
            self.play(FadeOut(extra_help), FadeIn(no_tablets_label), FadeIn(control_ends[0]),
                      Create(control_trend), FadeIn(control_ends[1]), run_time=1.4)
            self.play(FadeIn(changed_no_tablets), run_time=0.55)

        assumption = ink("Would they have moved together?", 45).move_to(versus)
        hint_up = DashedLine([x_year[0], -0.39, 0], t0, color=TREATED, stroke_width=3,
                             dash_length=0.11)
        hint_down = DashedLine([x_year[0], -1.42, 0], n0, color=GRAY, stroke_width=2.9,
                               dash_length=0.11)
        alternative = DashedLine(t0, [2.52, 0.95, 0], color=GHOST, stroke_width=3.3,
                                 dash_length=0.13)
        missing = Circle(radius=0.074, color=GHOST, stroke_width=2.6).move_to(t1)
        alt_label = ink("Without tablets?", 27, GHOST).next_to(missing, RIGHT, buff=0.18)
        counterfactual_note = ink("The missing score", 32, GHOST).move_to([0.0, 1.57, 0])

        with clock.beat() as duration:
            self.play(FadeOut(versus), run_time=0.29)
            self.play(FadeIn(assumption), run_time=0.43)
            self.wait(duration * 0.17)
            self.play(
                FadeOut(changed), FadeOut(illustrative), FadeOut(tablet_trend),
                FadeOut(tablet_ends[1]), Create(alternative), run_time=0.87,
            )
            self.play(
                FadeIn(missing), FadeIn(alt_label), run_time=0.24,
            )
            self.wait(duration * 0.20)
            self.play(FadeOut(has_tablets), FadeOut(no_tablets_label), FadeIn(years[0]),
                      Create(hint_up), Create(hint_down), run_time=1.18)
            self.wait(duration * 0.16)
            self.play(FadeIn(counterfactual_note), run_time=0.79)

        trend_objects = VGroup(
            assumption, score_base, years, tablet_ends[0], control_trend, control_ends,
            changed_no_tablets, alternative, missing, alt_label, hint_up, hint_down, counterfactual_note,
        )

        ruler = ScoreRuler()
        score_line = ruler.axis()
        control_mean = ruler.mean(550, GRAY)
        treated_mean = ruler.mean(675, TREATED)
        alternate_mean = ruler.mean(750, GHOST, hollow=True)
        selection_gap = ruler.contrast(550, 750, label="+200", color=GOLD, y=0.54)
        causal_gap = ruler.contrast(750, 675, label="−75", color=GOLD, y=-0.71)
        selection_caption = ink("Different schools", 30, MUTED).next_to(selection_gap[1], UP, buff=0.23)
        causal_caption = ink("Same schools", 28, TREATED)
        causal_caption.move_to(ruler.at(550, -0.70) + 0.26 * LEFT, aligned_edge=RIGHT)
        guides = [
            DashedLine(ruler.at(value, ruler.AXIS_Y + 0.12), ruler.at(value, top), color=color,
                       stroke_width=1.6, dash_length=0.06)
            for value, color, top in ((550, GRAY, 0.51), (750, GHOST, 0.51), (675, TREATED, -0.74))
        ]
        closing_question = ink("What would these same people", 52)
        closing_tail = ink("have done under the other choice?", 52)
        final = VGroup(closing_question, closing_tail).arrange(DOWN, buff=0.19).move_to([0, 0.20, 0])
        closing_tail.set_color(TREATED)

        with clock.beat() as duration:
            self.play(
                FadeOut(trend_objects), FadeIn(score_line), FadeIn(treated_mean), run_time=1.02,
            )
            self.wait(duration * 0.065)
            self.play(
                FadeIn(control_mean), FadeIn(alternate_mean), Create(guides[0]),
                Create(guides[1]), Create(selection_gap[0]), FadeIn(selection_gap[1]),
                FadeIn(selection_caption), run_time=1.18,
            )
            self.wait(duration * 0.13)
            self.play(
                Create(guides[2]), Create(causal_gap[0]), FadeIn(causal_gap[1]),
                FadeIn(causal_caption), run_time=1.05,
            )
            self.wait(duration * 0.24)
            self.play(
                FadeOut(score_line), FadeOut(control_mean), FadeOut(treated_mean),
                FadeOut(alternate_mean), FadeOut(selection_gap), FadeOut(causal_gap),
                FadeOut(VGroup(*guides)), FadeOut(selection_caption), FadeOut(causal_caption),
                FadeIn(closing_question, shift=0.10 * UP), run_time=1.04,
            )
            self.play(FadeIn(closing_tail, shift=0.10 * UP), run_time=0.85)

        clock.finish()
