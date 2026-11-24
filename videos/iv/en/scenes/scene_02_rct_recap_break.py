from manim import *

from videos.iv.shared.common import (
    ACCENT,
    COIN_COLOR,
    CONTROL_COLOR,
    FORBIDDEN,
    INSTRUMENT,
    SOFT,
    TREAT_COLOR,
    load_icon,
    load_scene_timing_durations,
    make_school_row,
)


class Scene02_RctRecapBreakEN(Scene):
    """English version of Scene 02. 5 chunks, ~68.98s."""

    WAIT_TAIL = 1.5

    def construct(self):
        d = load_scene_timing_durations("02_rct_recap_break", language="en")

        # Beat 1: tablet RCT recap
        title = Text("Tablet RCT recap", font_size=30, weight=BOLD, color=SOFT).to_edge(UP, buff=0.4)
        coin = load_icon("coin.svg", COIN_COLOR, 1.0).move_to(UP * 1.0)

        assigned_t = make_school_row(4, TREAT_COLOR).move_to(LEFT * 2.7 + DOWN * 0.6)
        assigned_t_label = Text("Assigned: Treatment", font_size=22, color=TREAT_COLOR).next_to(assigned_t, DOWN, buff=0.25)
        assigned_c = make_school_row(4, CONTROL_COLOR).move_to(RIGHT * 2.7 + DOWN * 0.6)
        assigned_c_label = Text("Assigned: Control", font_size=22, color=CONTROL_COLOR).next_to(assigned_c, DOWN, buff=0.25)
        naive_eq = Text("Mean difference  =  causal effect", font_size=24, color=GREEN).move_to(DOWN * 2.5)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(coin, scale=0.8), run_time=0.7)
        self.play(Rotate(coin, angle=2 * PI, axis=UP), run_time=1.0)
        self.play(FadeIn(assigned_t, shift=DOWN * 0.15), FadeIn(assigned_t_label),
                  FadeIn(assigned_c, shift=DOWN * 0.15), FadeIn(assigned_c_label), run_time=1.4)
        self.play(Write(naive_eq), run_time=1.2)
        self.wait(d[0] - 5.0)

        # Beat 2: some refuse
        refuse_caption = Text("Some refuse the tablet", font_size=22, color=FORBIDDEN).move_to(LEFT * 2.7 + DOWN * 1.9)
        self.play(FadeOut(naive_eq), run_time=0.4)
        self.play(FadeIn(refuse_caption, shift=UP * 0.1), run_time=0.7)
        refuse_animations = [
            assigned_t[i].animate.set_color(CONTROL_COLOR).set_stroke(color=FORBIDDEN, width=2)
            for i in (1, 3)
        ]
        self.play(LaggedStart(*refuse_animations, lag_ratio=0.3), run_time=1.6)
        x_marks = VGroup(*[
            Cross(assigned_t[i], stroke_color=FORBIDDEN, stroke_width=3).scale(0.5)
            for i in (1, 3)
        ])
        self.play(FadeIn(x_marks), run_time=0.5)
        self.wait(d[1] - 3.2)

        # Beat 3: some buy
        buy_caption = Text("Some buy with their own funds", font_size=22, color=ACCENT).move_to(RIGHT * 2.7 + DOWN * 1.9)
        self.play(FadeIn(buy_caption, shift=UP * 0.1), run_time=0.7)
        buy_animations = [
            assigned_c[i].animate.set_color(TREAT_COLOR).set_stroke(color=ACCENT, width=2)
            for i in (0, 2)
        ]
        self.play(LaggedStart(*buy_animations, lag_ratio=0.3), run_time=1.4)
        stars = VGroup(*[
            Star(n=5, outer_radius=0.18, color=ACCENT, fill_opacity=0.9).move_to(assigned_c[i])
            for i in (0, 2)
        ])
        self.play(FadeIn(stars, scale=0.6), run_time=0.5)
        self.wait(d[2] - 2.6)

        # Beat 4: comparing by actual treatment brings bias back
        previous = VGroup(title, coin, assigned_t, assigned_c, assigned_t_label, assigned_c_label,
                          refuse_caption, buy_caption, x_marks, stars)
        warning = Text("If we compare by actual treatment…", font_size=26, color=FORBIDDEN).to_edge(UP, buff=0.6)
        actual_t = VGroup(*[Dot(radius=0.20, color=TREAT_COLOR) for _ in range(4)]).arrange(RIGHT, buff=0.4).move_to(LEFT * 2.8 + UP * 0.2)
        actual_t_label = Text("Actually treated", font_size=22, color=TREAT_COLOR).next_to(actual_t, DOWN, buff=0.25)
        actual_c = VGroup(*[Dot(radius=0.20, color=CONTROL_COLOR) for _ in range(4)]).arrange(RIGHT, buff=0.4).move_to(RIGHT * 2.8 + UP * 0.2)
        actual_c_label = Text("Actually untreated", font_size=22, color=CONTROL_COLOR).next_to(actual_c, DOWN, buff=0.25)
        bias_eq = Text("Mean difference  ≠  causal effect", font_size=28, weight=BOLD, color=FORBIDDEN).move_to(DOWN * 1.4)
        bias_note = Text("Refusers = skeptical,  Self-buyers = motivated", font_size=20, color=SOFT).next_to(bias_eq, DOWN, buff=0.4)

        self.play(FadeOut(previous), run_time=0.7)
        self.play(FadeIn(warning, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(actual_t), FadeIn(actual_t_label),
                  FadeIn(actual_c), FadeIn(actual_c_label), run_time=1.2)
        self.play(Write(bias_eq), run_time=1.0)
        self.play(FadeIn(bias_note, shift=UP * 0.1), run_time=0.9)
        self.wait(d[3] - 4.5)

        # Beat 5: only assignment is random
        bridge_title = Text("Only the assignment is random", font_size=30, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        row_label_assign = Text("Assignment", font_size=22, color=SOFT)
        row_label_actual = Text("Actual", font_size=22, color=SOFT)
        assign_row = make_school_row(8, COIN_COLOR, spacing=0.30)
        actual_row = VGroup(*[
            Dot(radius=0.18, color=c) for c in
            [TREAT_COLOR, CONTROL_COLOR, TREAT_COLOR, CONTROL_COLOR,
             TREAT_COLOR, TREAT_COLOR, CONTROL_COLOR, TREAT_COLOR]
        ])
        actual_row.arrange(RIGHT, buff=0.30)
        assign_block = VGroup(row_label_assign, assign_row).arrange(RIGHT, buff=0.6)
        actual_block = VGroup(row_label_actual, actual_row).arrange(RIGHT, buff=0.6)
        rows_block = VGroup(assign_block, actual_block).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(UP * 0.2)
        random_badge = Text("Random ✓", font_size=20, color=GREEN).next_to(assign_block, RIGHT, buff=0.5)
        not_random = Text("Not random ✗", font_size=20, color=FORBIDDEN).next_to(actual_block, RIGHT, buff=0.5)
        pivot = Text("Use the randomness we still have → IV", font_size=24, weight=BOLD, color=INSTRUMENT).move_to(DOWN * 2.2)

        self.play(FadeOut(warning), FadeOut(actual_t), FadeOut(actual_t_label),
                  FadeOut(actual_c), FadeOut(actual_c_label),
                  FadeOut(bias_eq), FadeOut(bias_note), run_time=0.7)
        self.play(FadeIn(bridge_title, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(rows_block, shift=UP * 0.15), run_time=1.4)
        self.play(FadeIn(random_badge), FadeIn(not_random), run_time=0.8)
        self.play(Write(pivot), run_time=1.4)
        self.wait(d[4] - 4.9)
        self.wait(self.WAIT_TAIL)
