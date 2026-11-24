from manim import *

from videos.iv.shared.common import (
    ACCENT,
    CLEAN_WATER,
    COIN_COLOR,
    CONTROL_COLOR,
    DIRTY_WATER,
    FORBIDDEN,
    INSTRUMENT,
    SOFT,
    TREAT_COLOR,
    load_icon,
    load_scene_timing_durations,
    make_forbidden_card,
)


class Scene01_SnowPumps(Scene):
    """
    Scene 01: Snow Pumps (도구변수 시리즈의 도입)

    Core Claim:
    실험자가 동전을 던질 수 없는 현실에서, 자연이 우연히 던진 동전을
    찾아내는 것이 도구변수(IV)다. 1854년 런던의 수도 회사 배관망이
    그런 자연의 동전 역할을 했다.

    Visual Pivot:
    "실험자가 못 던지는 동전" → "런던 배관망이 대신 던져 준 동전"

    3Blue1Brown Reference: 3b1b/_2020/covid.py — 큰 사건을 핵심 질문으로 압축
    Script: narration/01_snow_pumps.txt — 7 chunks, 79.97s
    """

    WAIT_TAIL = 2.0

    def construct(self):
        durations = load_scene_timing_durations("01_snow_pumps", language="ko")

        # Beat 1 (0~11.16s): RCT 복습
        coin = load_icon("coin.svg", COIN_COLOR, 1.4)
        coin.move_to(ORIGIN + UP * 0.3)
        treat_dots = VGroup(*[Dot(radius=0.13, color=TREAT_COLOR) for _ in range(4)])
        treat_dots.arrange(RIGHT, buff=0.18)
        treat_label = Text("처치", font_size=22, color=TREAT_COLOR)
        treat_group = VGroup(treat_dots, treat_label).arrange(DOWN, buff=0.18)
        treat_group.move_to(LEFT * 3.2 + DOWN * 1.4)
        control_dots = VGroup(*[Dot(radius=0.13, color=CONTROL_COLOR) for _ in range(4)])
        control_dots.arrange(RIGHT, buff=0.18)
        control_label = Text("비교", font_size=22, color=CONTROL_COLOR)
        control_group = VGroup(control_dots, control_label).arrange(DOWN, buff=0.18)
        control_group.move_to(RIGHT * 3.2 + DOWN * 1.4)
        split_arrow_l = Arrow(coin.get_corner(DL), treat_group.get_top(), buff=0.2, color=SOFT, stroke_width=3)
        split_arrow_r = Arrow(coin.get_corner(DR), control_group.get_top(), buff=0.2, color=SOFT, stroke_width=3)
        bias_badge = Text("편향 = 0", font_size=26, weight=BOLD, color=GREEN).move_to(DOWN * 3.0)

        self.play(FadeIn(coin, scale=0.8), run_time=0.8)
        self.play(Rotate(coin, angle=2 * PI, axis=UP), run_time=1.2)
        self.play(GrowArrow(split_arrow_l), GrowArrow(split_arrow_r),
                  FadeIn(treat_group, shift=DOWN * 0.2), FadeIn(control_group, shift=DOWN * 0.2), run_time=1.5)
        self.play(FadeIn(bias_badge, shift=UP * 0.15), run_time=0.8)
        self.wait(11.16 - 4.3)

        # Beat 2 (11.16~23.71s): 금지된 동전
        coin_small_target = coin.copy().scale(0.45).to_corner(UL, buff=0.5)
        smoking_card = make_forbidden_card("임산부에게\n흡연 배정").move_to(LEFT * 2.6 + UP * 0.4)
        army_card = make_forbidden_card("누구를\n군대로 보낼지").move_to(RIGHT * 2.6 + UP * 0.4)
        forbidden_caption = Text("실험자가 던질 수 없는 동전들", font_size=24, color=FORBIDDEN).move_to(DOWN * 1.8)

        self.play(FadeOut(treat_group), FadeOut(control_group), FadeOut(split_arrow_l),
                  FadeOut(split_arrow_r), FadeOut(bias_badge), Transform(coin, coin_small_target), run_time=1.0)
        self.play(FadeIn(smoking_card, shift=UP * 0.15), FadeIn(army_card, shift=UP * 0.15), run_time=1.4)
        self.play(FadeIn(forbidden_caption, shift=UP * 0.1), run_time=0.8)
        self.wait(12.55 - 3.2)

        # Beat 3 (23.71~32.47s): 누가 대신 던져 줄까?
        big_question = Text("?", font_size=180, weight=BOLD, color=ACCENT).move_to(ORIGIN + UP * 0.2)
        question_caption = Text("누가 대신 던져 줄까?", font_size=30, color=WHITE).next_to(big_question, DOWN, buff=0.5)

        self.play(FadeOut(smoking_card), FadeOut(army_card), FadeOut(forbidden_caption), run_time=0.7)
        self.play(FadeIn(big_question, scale=0.6), run_time=1.0)
        self.play(Write(question_caption), run_time=1.0)
        self.wait(8.76 - 2.7)

        # Beat 4 (32.47~50.88s): 1854 런던
        date_label = Text("1854년 런던", font_size=30, weight=BOLD, color=SOFT).to_edge(UP, buff=0.5)
        streets = VGroup(*[
            Rectangle(width=5.0, height=0.35, stroke_color=GREY_C, stroke_width=2,
                       fill_color=GREY_E, fill_opacity=0.35) for _ in range(6)
        ])
        streets.arrange(DOWN, buff=0.18)
        streets.move_to(ORIGIN + DOWN * 0.2)
        clean_drop = load_icon("droplet.svg", CLEAN_WATER, 0.7)
        clean_name = Text("Lambeth\n(상류 물)", font_size=20, color=CLEAN_WATER, line_spacing=0.9)
        clean_group = VGroup(clean_drop, clean_name).arrange(DOWN, buff=0.18)
        clean_group.next_to(streets, LEFT, buff=0.6)
        dirty_drop = load_icon("droplet.svg", DIRTY_WATER, 0.7)
        dirty_name = Text("S & V\n(하수 섞인 강물)", font_size=20, color=DIRTY_WATER, line_spacing=0.9)
        dirty_group = VGroup(dirty_drop, dirty_name).arrange(DOWN, buff=0.18)
        dirty_group.next_to(streets, RIGHT, buff=0.6)

        self.play(FadeOut(big_question), FadeOut(question_caption), FadeOut(coin), run_time=0.7)
        self.play(FadeIn(date_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[Create(s) for s in streets], lag_ratio=0.12), run_time=1.6)
        self.play(FadeIn(clean_group, shift=RIGHT * 0.2), FadeIn(dirty_group, shift=LEFT * 0.2), run_time=1.2)
        self.wait(18.41 - 4.2)

        # Beat 5 (50.88~63.24s): 거리별 회사 배정 = 우연
        assignment = [CLEAN_WATER, DIRTY_WATER, DIRTY_WATER, CLEAN_WATER, DIRTY_WATER, CLEAN_WATER]
        street_fills = [
            street.animate.set_fill(color, opacity=0.75).set_stroke(color=color)
            for street, color in zip(streets, assignment)
        ]
        self.play(LaggedStart(*street_fills, lag_ratio=0.18), run_time=2.4)
        chance_label = Text("거의 우연", font_size=32, weight=BOLD, color=ACCENT).move_to(DOWN * 3.0)
        chance_box = SurroundingRectangle(chance_label, color=ACCENT, buff=0.15)
        self.play(FadeIn(chance_label, shift=UP * 0.1), Create(chance_box), run_time=1.0)
        self.wait(12.36 - 3.4)

        # Beat 6 (63.24~69.65s): 자연이 던진 동전
        nature_coin = load_icon("coin.svg", COIN_COLOR, 1.6).move_to(ORIGIN + UP * 0.5)
        nature_caption = Text("자연이 던진 동전", font_size=28, color=COIN_COLOR).next_to(nature_coin, DOWN, buff=0.4)

        self.play(streets.animate.set_opacity(0.25),
                  clean_group.animate.set_opacity(0.4),
                  dirty_group.animate.set_opacity(0.4),
                  chance_label.animate.set_opacity(0.4),
                  chance_box.animate.set_opacity(0.4), run_time=0.7)
        self.play(FadeIn(nature_coin, scale=0.7), run_time=0.9)
        self.play(Rotate(nature_coin, angle=2 * PI, axis=UP), Write(nature_caption), run_time=1.4)
        self.wait(6.41 - 3.0)

        # Beat 7 (69.65~79.97s): 도구변수 타이틀
        title_group_old = VGroup(date_label, streets, clean_group, dirty_group,
                                  chance_label, chance_box, nature_coin, nature_caption)
        self.play(FadeOut(title_group_old), run_time=0.7)
        topic_title = Text("도구변수", font_size=72, weight=BOLD, color=INSTRUMENT)
        topic_sub = Text("Instrumental Variable · IV", font_size=28, color=SOFT)
        title_stack = VGroup(topic_title, topic_sub).arrange(DOWN, buff=0.3).move_to(UP * 1.2)
        z_node = Circle(radius=0.42, color=INSTRUMENT, stroke_width=3)
        z_label = Text("Z", font_size=28, color=INSTRUMENT, weight=BOLD).move_to(z_node)
        z_group = VGroup(z_node, z_label).move_to(LEFT * 2.8 + DOWN * 1.6)
        t_node = Circle(radius=0.42, color=TREAT_COLOR, stroke_width=3)
        t_label = Text("T", font_size=28, color=TREAT_COLOR, weight=BOLD).move_to(t_node)
        t_group = VGroup(t_node, t_label).move_to(ORIGIN + DOWN * 1.6)
        y_node = Circle(radius=0.42, color=CONTROL_COLOR, stroke_width=3)
        y_label = Text("Y", font_size=28, color=CONTROL_COLOR, weight=BOLD).move_to(y_node)
        y_group = VGroup(y_node, y_label).move_to(RIGHT * 2.8 + DOWN * 1.6)
        zt_arrow = Arrow(z_group.get_right(), t_group.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        ty_arrow = Arrow(t_group.get_right(), y_group.get_left(), buff=0.12, color=WHITE, stroke_width=3)

        self.play(FadeIn(title_stack, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(z_group), FadeIn(t_group), FadeIn(y_group), run_time=0.9)
        self.play(GrowArrow(zt_arrow), GrowArrow(ty_arrow), run_time=0.8)
        self.play(Indicate(z_group, color=INSTRUMENT), run_time=0.9)
        self.wait(10.32 - 3.6)
        self.wait(self.WAIT_TAIL)
