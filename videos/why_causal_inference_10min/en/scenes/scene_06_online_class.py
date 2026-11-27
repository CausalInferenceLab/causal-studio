"""A randomized classroom experiment from the notebook's saved group means."""

from pathlib import Path
import sys

import numpy as np
from manim import (
    Arrow, Create, DashedLine, Dot, DOWN, FadeIn, FadeOut, Indicate,
    LaggedStart, LEFT, Line, RIGHT, UP, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))
from visual import GOLD, GHOST, GRAY, GRID, INK, MUTED, TREATED, LessonScene, ink, tabler_icon


def icon(name, height, color):
    glyph = tabler_icon(name)
    return glyph.set_fill(opacity=0).set_stroke(color=color, width=3.3, opacity=1).set_height(height)


def format_icon(name, label, x, y, color):
    glyph = icon(name, 1.02, color).move_to([x, y, 0])
    return VGroup(glyph, ink(label, 31, color).next_to(glyph, DOWN, buff=0.21))


def token_row(count, center, color, step=0.34):
    return VGroup(*(
        Dot(center + (i - (count - 1) / 2) * step * RIGHT, radius=0.067, color=color)
        for i in range(count)
    ))


def x_at(score):
    return -4.15 + (score - 70) * 0.70


def tick_position(score):
    return np.array([x_at(score), -1.46, 0])


def exam_axis():
    start, end = tick_position(70), tick_position(82)
    axis = VGroup(Line(start, end, stroke_width=2.0, color=GRID))
    for value in (70, 72, 74, 76, 78, 80, 82):
        p = tick_position(value)
        tick = Line(p + 0.1 * UP, p + 0.1 * DOWN, color=GRAY, stroke_width=1.4)
        axis.add(tick, ink(str(value), 23, MUTED).next_to(tick, DOWN, buff=0.15))
    return axis


def group_mean(score, name, color):
    anchor = tick_position(score)
    marker = Dot(anchor, radius=0.12, color=color).set_z_index(2)
    cap = marker.get_center() + 1.55 * UP
    line = DashedLine(anchor + 0.16 * UP, cap, color=color, stroke_width=1.6,
                      stroke_opacity=0.72, dash_length=0.085)
    number = ink(f"{score:.1f}", 63, color).next_to(line, UP, buff=0.16)
    label = ink(name, 30, color).next_to(number, UP, buff=0.14)
    return VGroup(marker, line, number, label)


class Scene06(LessonScene):
    def construct(self):
        clock = self.clock("06_online_class")
        source = token_row(12, np.array([0.0, 1.52, 0]), MUTED)
        student_caption = ink("University students", 27, MUTED).move_to([0, 2.22, 0])
        person = format_icon("chalkboard", "In person", -3.34, -0.06, GRAY)
        online = format_icon("device-laptop", "Online", 3.34, -0.06, TREATED)
        question = ink("Does class format affect exam scores?", 45).move_to([0, -2.04, 0])

        with clock.beat() as duration:
            self.play(LaggedStart(*(FadeIn(m, shift=0.16 * UP) for m in source), lag_ratio=0.06),
                      FadeIn(student_caption), run_time=1.5)
            self.wait(duration * 0.22)
            self.play(FadeIn(person, shift=0.10 * UP), FadeIn(online, shift=0.10 * UP),
                      run_time=1.1)
            self.wait(duration * 0.14)
            self.play(FadeIn(question, shift=0.11 * UP), run_time=0.75)

        study = VGroup(icon("clock", 0.45, MUTED), ink("Prefers to study alone", 27, MUTED))
        study.arrange(RIGHT, buff=0.21).move_to([-2.60, 2.29, 0])
        work = VGroup(icon("briefcase", 0.45, MUTED), ink("Work schedule", 27, MUTED))
        work.arrange(RIGHT, buff=0.19).move_to([2.64, 2.29, 0])
        left_choice = Arrow([-1.50, 1.36, 0], [-3.34, 0.72, 0], buff=0.07,
                            stroke_width=2.7, color=GRAY)
        right_choice = Arrow([1.50, 1.36, 0], [3.34, 0.72, 0], buff=0.07,
                             stroke_width=2.7, color=TREATED)
        selection_question = ink("Who picks each format?", 41).move_to(question)
        exam_question = VGroup(icon("clipboard-text", 0.65, MUTED), ink("Exam scores?", 33, MUTED))
        exam_question.arrange(RIGHT, buff=0.26).move_to(question)

        with clock.beat() as duration:
            self.play(FadeOut(question), FadeIn(selection_question, shift=UP * 0.06), run_time=0.75)
            self.wait(duration * 0.08)
            self.play(Create(left_choice), Create(right_choice), run_time=0.95)
            self.wait(duration * 0.14)
            self.play(FadeOut(student_caption), FadeIn(study, shift=UP * 0.08),
                      run_time=0.65)
            self.wait(duration * 0.12)
            self.play(FadeIn(work, shift=UP * 0.08), run_time=0.70)
            self.wait(duration * 0.16)
            self.play(FadeOut(selection_question), FadeIn(exam_question), run_time=0.65)
            self.play(person[0].animate.set_stroke(opacity=0.55), person[1].animate.set_opacity(0.55),
                      online[0].animate.set_stroke(opacity=0.55), online[1].animate.set_opacity(0.55),
                      Indicate(exam_question, color=INK, scale_factor=1.055), run_time=0.9)

        stations = (-3.75, 0.0, 3.75)
        blended = format_icon("devices", "Blended", 0.0, -0.06, GHOST)
        random = VGroup(icon("arrows-shuffle", 0.52, INK), ink("Random assignment", 30))
        random.arrange(RIGHT, buff=0.21).move_to([0, 2.20, 0])
        mixed_order = (0, 2, 1, 2, 0, 1, 1, 0, 2, 1, 2, 0)
        target_rows = [
            token_row(4, np.array([x, 0.90, 0]), color, step=0.26)
            for x, color in zip(stations, (GRAY, GHOST, TREATED), strict=True)
        ]
        routes = []
        for x, color in zip(stations, (GRAY, GHOST, TREATED), strict=True):
            routes.append(DashedLine(np.array([0, 1.72, 0]), np.array([x, 1.10, 0]),
                                     color=color, stroke_width=1.65, dash_length=0.08))
        used = [0, 0, 0]
        deal = []
        for marker, index in zip(source, mixed_order, strict=True):
            goal = target_rows[index][used[index]]
            deal.append(marker.animate.move_to(goal).set_color(goal.get_color()))
            used[index] += 1
        exam_label = ink("Final exam score", 36).move_to([0, -1.93, 0])

        with clock.beat() as duration:
            self.play(
                FadeOut(study), FadeOut(work), FadeOut(left_choice),
                FadeOut(right_choice), FadeOut(exam_question),
                FadeIn(random),
                person[0].animate.set_stroke(opacity=1).shift(0.41 * LEFT),
                person[1].animate.set_opacity(1).shift(0.41 * LEFT),
                online[0].animate.set_stroke(opacity=1).shift(0.41 * RIGHT),
                online[1].animate.set_opacity(1).shift(0.41 * RIGHT), run_time=1.00,
            )
            self.wait(duration * 0.17)
            self.play(FadeIn(blended), LaggedStart(*(Create(p) for p in routes), lag_ratio=0.18),
                      run_time=1.25)
            self.play(LaggedStart(*deal, lag_ratio=0.095), run_time=2.6)
            self.wait(duration * 0.20)
            self.play(blended[0].animate.set_stroke(opacity=0.46), blended[1].animate.set_opacity(0.55),
                      *(m.animate.set_opacity(0.42) for m, i in zip(source, mixed_order, strict=True) if i == 1),
                      run_time=0.79)
            self.wait(duration * 0.10)
            self.play(FadeIn(exam_label), run_time=0.60)

        axis = exam_axis()
        average_label = ink("Average final exam score", 39).move_to([0, 2.55, 0])
        in_person_mean = group_mean(78.547485, "In person", GRAY)
        online_mean = group_mean(73.635263, "Online", TREATED)
        start = np.array([x_at(78.547485), -0.84, 0])
        end = np.array([x_at(73.635263), -0.84, 0])
        effect_arrow = Arrow(start, end, color=GOLD, buff=0.05, stroke_width=4.0)
        estimate = ink("−4.91 points", 40, GOLD).next_to(effect_arrow, UP, buff=0.15)

        with clock.beat() as duration:
            self.play(
                FadeOut(random), FadeOut(source), FadeOut(VGroup(*routes)),
                FadeOut(blended), FadeOut(online), FadeOut(person), FadeOut(exam_label),
                Create(axis[0]), run_time=0.48,
            )
            self.play(FadeIn(average_label), FadeIn(VGroup(*axis[1:])), run_time=0.55)
            self.play(FadeIn(in_person_mean, shift=0.11 * UP), run_time=0.75)
            self.wait(duration * 0.155)
            self.play(FadeIn(online_mean, shift=0.11 * UP), run_time=0.75)
            self.wait(duration * 0.36)
            self.play(Create(effect_arrow), FadeIn(estimate, shift=UP * 0.09), run_time=1.0)
            self.wait(duration * 0.04)
            self.play(Indicate(estimate, color=GOLD, scale_factor=1.045), run_time=0.85)

        qualification = ink("Estimate from this experiment", 29, MUTED).move_to([0, -2.40, 0])
        student_set = token_row(10, np.array([0.0, 1.35, 0]), MUTED)
        groups = (-3.6, 0.0, 3.6)
        trial_positions = [
            token_row(count, np.array([x, -0.66, 0]), color, step=0.29)
            for count, x, color in zip((3, 4, 3), groups, (GRAY, GHOST, TREATED), strict=True)
        ]
        assignment = (0, 1, 2, 1, 2, 0, 2, 1, 1, 0)
        used = [0, 0, 0]
        shuffle = []
        for student, group in zip(student_set, assignment, strict=True):
            target = trial_positions[group][used[group]]
            shuffle.append(student.animate.move_to(target).set_color(target.get_color()))
            used[group] += 1
        trial_names = VGroup(*(
            ink(name, 31, color).move_to([x, -1.31, 0])
            for name, x, color in zip(("In person", "Blended", "Online"), groups,
                                      (GRAY, GHOST, TREATED), strict=True)
        ))
        experiment = VGroup(icon("arrows-shuffle", 0.67, INK), ink("Assign format first", 36))
        experiment.arrange(RIGHT, buff=0.28).move_to([0, 2.14, 0])
        choice = ink("Student preference", 31, MUTED).move_to([0, 0.03, 0])
        no_choice_line = Line(choice.get_left() + LEFT * 0.11, choice.get_right() + RIGHT * 0.11,
                              color=GOLD, stroke_width=2.2)

        with clock.beat() as duration:
            self.play(FadeIn(qualification), run_time=0.66)
            self.wait(duration * 0.30)
            self.play(
                FadeOut(average_label), FadeOut(axis), FadeOut(online_mean),
                FadeOut(in_person_mean), FadeOut(estimate), FadeOut(effect_arrow),
                FadeOut(qualification), FadeIn(experiment), FadeIn(student_set), run_time=1.0,
            )
            self.wait(duration * 0.10)
            self.play(LaggedStart(*shuffle, lag_ratio=0.08), FadeIn(trial_names), run_time=2.55)
            self.wait(duration * 0.115)
            self.play(FadeIn(choice), run_time=0.63)
            self.play(Create(no_choice_line), run_time=0.60)
            self.play(choice.animate.set_opacity(0.48), no_choice_line.animate.set_opacity(0.48),
                      run_time=0.72)

        clock.finish()
