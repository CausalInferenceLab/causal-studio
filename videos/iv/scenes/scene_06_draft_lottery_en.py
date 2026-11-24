from manim import *

from iv_common import (
    ACCENT,
    CONTROL_COLOR,
    FORBIDDEN,
    INSTRUMENT,
    SOFT,
    TREAT_COLOR,
    load_scene_timing_durations,
)


class Scene06_DraftLotteryEN(Scene):
    """English version of Scene 06. 5 chunks, ~71.26s."""

    WAIT_TAIL = 1.5

    def construct(self):
        d = load_scene_timing_durations("06_draft_lottery_en")

        # Beat 1: national scale intro
        title = Text("Same trick, national scale", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        scale_up = Text("Not just for small experiments", font_size=24, color=SOFT).move_to(ORIGIN + UP * 0.2)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(scale_up), run_time=1.2)
        self.wait(d[0] - 1.9)

        # Beat 2: 1969 USA draft
        self.play(FadeOut(scale_up), run_time=0.4)
        date_label = Text("USA · 1969", font_size=28, weight=BOLD, color=SOFT).to_edge(UP, buff=1.4)
        balls = VGroup()
        ball_nums = ["73", "144", "012"]
        for num in ball_nums:
            ball = Circle(radius=0.5, color=ACCENT, stroke_width=3, fill_color=YELLOW_A, fill_opacity=0.9)
            ball_num = Text(num, font_size=22, weight=BOLD, color=BLACK).move_to(ball)
            balls.add(VGroup(ball, ball_num))
        balls.arrange(RIGHT, buff=0.5).move_to(UP * 0.2)
        ball_caption = Text("365 birthday balls drawn at random", font_size=22, color=WHITE).next_to(balls, DOWN, buff=0.5)
        rule = Text("Low number → drafted", font_size=24, weight=BOLD, color=INSTRUMENT).move_to(DOWN * 1.5)
        independence_note = Text("Birthdate is unrelated to education or job", font_size=20, color=SOFT).next_to(rule, DOWN, buff=0.3)

        self.play(FadeIn(date_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2, scale=0.7) for b in balls], lag_ratio=0.2), run_time=1.4)
        self.play(Write(ball_caption), run_time=1.4)
        self.play(Write(rule), run_time=1.0)
        self.play(FadeIn(independence_note, shift=UP * 0.1), run_time=0.9)
        self.wait(d[1] - 5.4)

        # Beat 3: Angrist's question
        prior = VGroup(date_label, balls, ball_caption, rule, independence_note)
        self.play(FadeOut(prior), run_time=0.6)
        angrist = Text("Joshua Angrist's question", font_size=26, weight=BOLD, color=ACCENT).to_edge(UP, buff=1.2)
        question = Text('"What is the effect of military service on lifetime earnings?"', font_size=24, color=WHITE).move_to(ORIGIN + UP * 0.4)
        t_q = Text("Service", font_size=24, color=TREAT_COLOR)
        y_q = Text("Earnings", font_size=24, color=CONTROL_COLOR)
        arrow_q = Arrow(LEFT * 1.0, RIGHT * 1.0, buff=0.05, color=WHITE, stroke_width=4)
        chain = VGroup(t_q, arrow_q, y_q).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.0)

        self.play(FadeIn(angrist, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(question), run_time=1.4)
        self.play(FadeIn(chain, shift=UP * 0.1), run_time=1.0)
        self.wait(d[2] - 3.1)

        # Beat 4: naive bias
        bias_warn = Text("Veterans vs non-veterans simple comparison → bias", font_size=22, color=FORBIDDEN).to_edge(DOWN, buff=2.2)
        bias_reason = Text("Those who chose to serve differ from those who avoided", font_size=20, color=SOFT).next_to(bias_warn, DOWN, buff=0.25)
        self.play(FadeIn(bias_warn, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(bias_reason, shift=UP * 0.05), run_time=0.9)
        self.wait(d[3] - 1.9)

        # Beat 5: lottery as IV + Snow callback
        prior2 = VGroup(angrist, question, chain, bias_warn, bias_reason)
        self.play(FadeOut(prior2), run_time=0.6)
        title_fix = Text("Lottery number = instrument", font_size=30, weight=BOLD, color=INSTRUMENT).to_edge(UP, buff=1.2)
        z6 = Circle(radius=0.4, color=INSTRUMENT, stroke_width=3)
        z6t = Text("Lottery", font_size=18, color=INSTRUMENT, weight=BOLD).move_to(z6)
        z6g = VGroup(z6, z6t).move_to(LEFT * 3.5 + DOWN * 0.2)
        t6 = Circle(radius=0.4, color=TREAT_COLOR, stroke_width=3)
        t6t = Text("Service", font_size=18, color=TREAT_COLOR, weight=BOLD).move_to(t6)
        t6g = VGroup(t6, t6t).move_to(ORIGIN + DOWN * 0.2)
        y6 = Circle(radius=0.4, color=CONTROL_COLOR, stroke_width=3)
        y6t = Text("Earnings", font_size=18, color=CONTROL_COLOR, weight=BOLD).move_to(y6)
        y6g = VGroup(y6, y6t).move_to(RIGHT * 3.5 + DOWN * 0.2)
        zt6 = Arrow(z6g.get_right(), t6g.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        ty6 = Arrow(t6g.get_right(), y6g.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        callback = Text("Snow's water company trick from a century earlier\nworked in the US labor market too", font_size=22, color=SOFT, line_spacing=0.95).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(title_fix, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(z6g), FadeIn(t6g), FadeIn(y6g), run_time=0.9)
        self.play(GrowArrow(zt6), GrowArrow(ty6), run_time=0.9)
        self.play(Indicate(z6g, color=INSTRUMENT), run_time=0.8)
        self.play(Write(callback), run_time=1.6)
        self.wait(d[4] - 4.9)
        self.wait(self.WAIT_TAIL)
