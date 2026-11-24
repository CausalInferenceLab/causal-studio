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


class Scene02_RctRecapBreak(Scene):
    """
    Scene 02: 태블릿 RCT 복습 + 비순응으로 단순 비교가 깨짐.

    Core Claim:
    무작위 배정과 실제 처치를 구분해야 한다.
    배정은 무작위지만 실제 처치는 학교의 의지로 결정되므로,
    실제 처치 여부로 단순 평균을 비교하면 편향이 돌아온다.
    이 비뚤어진 상황이 바로 도구변수의 진짜 무대다.

    Visual Pivot:
    "배정 행"은 무작위 색칠이 유지되지만, "실제 처치 행"은 일부
    학교가 색을 바꾸는 순간 — 무작위성이 한 줄에만 남는다는 사실.

    Script: narration/02_rct_recap_break.txt — 5 chunks, 70.4s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("02_rct_recap_break", language="ko")
        # durations ≈ [15.91, 13.06, 7.25, 18.36, 15.86]

        # Beat 1 (0~15.91s): 태블릿 RCT 복습 — 8 학교, 동전으로 배정
        title = Text("태블릿 RCT 복습", font_size=30, weight=BOLD, color=SOFT).to_edge(UP, buff=0.4)
        coin = load_icon("coin.svg", COIN_COLOR, 1.0).move_to(UP * 1.0)

        # 8 학교: 4 처치 배정 + 4 통제 배정
        assigned_t = make_school_row(4, TREAT_COLOR).move_to(LEFT * 2.7 + DOWN * 0.6)
        assigned_t_label = Text("배정 = 처치", font_size=22, color=TREAT_COLOR).next_to(assigned_t, DOWN, buff=0.25)
        assigned_c = make_school_row(4, CONTROL_COLOR).move_to(RIGHT * 2.7 + DOWN * 0.6)
        assigned_c_label = Text("배정 = 통제", font_size=22, color=CONTROL_COLOR).next_to(assigned_c, DOWN, buff=0.25)

        # 단순 비교 → 인과효과
        naive_eq = Text("평균 차이  =  인과효과", font_size=26, color=GREEN).move_to(DOWN * 2.5)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(coin, scale=0.8), run_time=0.7)
        self.play(Rotate(coin, angle=2 * PI, axis=UP), run_time=1.0)
        self.play(FadeIn(assigned_t, shift=DOWN * 0.15), FadeIn(assigned_t_label),
                  FadeIn(assigned_c, shift=DOWN * 0.15), FadeIn(assigned_c_label), run_time=1.4)
        self.play(Write(naive_eq), run_time=1.2)
        self.wait(15.91 - 5.0)

        # Beat 2 (15.91~28.97s): 일부 처치 배정 학교가 거부 (실제 = 비처치)
        refuse_caption = Text("일부는 태블릿을 거부", font_size=22, color=FORBIDDEN).move_to(LEFT * 2.7 + DOWN * 1.9)
        # assigned_t 중 2개를 색 변경 (거부 = 통제 색)
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
        self.wait(13.06 - 3.2)

        # Beat 3 (28.97~36.22s): 일부 통제 배정 학교가 사비로 구매 (실제 = 처치)
        buy_caption = Text("일부는 사비로 구매", font_size=22, color=ACCENT).move_to(RIGHT * 2.7 + DOWN * 1.9)
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
        self.wait(7.25 - 2.6)

        # Beat 4 (36.22~54.58s): 실제 처치로 비교 → 편향 부활
        # 상단 작게 정리, 중앙에 "실제 처치" vs "실제 비처치" 묶음
        previous = VGroup(title, coin, assigned_t, assigned_c, assigned_t_label, assigned_c_label,
                          refuse_caption, buy_caption, x_marks, stars)
        warning = Text("실제 처치 여부로 비교하면…", font_size=26, color=FORBIDDEN).to_edge(UP, buff=0.6)
        # 실제 처치 그룹
        actual_t = VGroup(
            Dot(radius=0.20, color=TREAT_COLOR),
            Dot(radius=0.20, color=TREAT_COLOR),
            Dot(radius=0.20, color=TREAT_COLOR),
            Dot(radius=0.20, color=TREAT_COLOR),
        ).arrange(RIGHT, buff=0.4).move_to(LEFT * 2.8 + UP * 0.2)
        actual_t_label = Text("실제 처치", font_size=22, color=TREAT_COLOR).next_to(actual_t, DOWN, buff=0.25)
        actual_c = VGroup(
            Dot(radius=0.20, color=CONTROL_COLOR),
            Dot(radius=0.20, color=CONTROL_COLOR),
            Dot(radius=0.20, color=CONTROL_COLOR),
            Dot(radius=0.20, color=CONTROL_COLOR),
        ).arrange(RIGHT, buff=0.4).move_to(RIGHT * 2.8 + UP * 0.2)
        actual_c_label = Text("실제 비처치", font_size=22, color=CONTROL_COLOR).next_to(actual_c, DOWN, buff=0.25)
        bias_eq = Text("평균 차이  ≠  인과효과", font_size=28, weight=BOLD, color=FORBIDDEN).move_to(DOWN * 1.4)
        bias_note = Text("거부 학교 = 회의적,  자비 구매 학교 = 의지 강함", font_size=20, color=SOFT).next_to(bias_eq, DOWN, buff=0.4)

        self.play(FadeOut(previous), run_time=0.7)
        self.play(FadeIn(warning, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(actual_t), FadeIn(actual_t_label),
                  FadeIn(actual_c), FadeIn(actual_c_label), run_time=1.2)
        self.play(Write(bias_eq), run_time=1.0)
        self.play(FadeIn(bias_note, shift=UP * 0.1), run_time=0.9)
        self.wait(18.36 - 4.5)

        # Beat 5 (54.58~70.44s): 배정만 무작위 → IV의 무대
        bridge_title = Text("배정만 무작위", font_size=30, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        # 두 행: 배정 (랜덤 표시), 실제 처치 (랜덤 아님)
        row_label_assign = Text("배정", font_size=22, color=SOFT)
        row_label_actual = Text("실제 처치", font_size=22, color=SOFT)
        assign_row = make_school_row(8, COIN_COLOR, spacing=0.30)
        actual_row = VGroup(*[
            Dot(radius=0.18, color=c) for c in
            [TREAT_COLOR, CONTROL_COLOR, TREAT_COLOR, CONTROL_COLOR,
             TREAT_COLOR, TREAT_COLOR, CONTROL_COLOR, TREAT_COLOR]
        ])
        actual_row.arrange(RIGHT, buff=0.30)
        # 정렬: 두 행을 수평 정렬
        assign_block = VGroup(row_label_assign, assign_row).arrange(RIGHT, buff=0.6)
        actual_block = VGroup(row_label_actual, actual_row).arrange(RIGHT, buff=0.6)
        rows_block = VGroup(assign_block, actual_block).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(UP * 0.2)
        random_badge = Text("무작위 ✓", font_size=20, color=GREEN).next_to(assign_block, RIGHT, buff=0.5)
        not_random = Text("무작위 아님 ✗", font_size=20, color=FORBIDDEN).next_to(actual_block, RIGHT, buff=0.5)
        pivot = Text("무작위성을 잃지 않는 분석법이 필요하다 → IV", font_size=24, weight=BOLD, color=INSTRUMENT).move_to(DOWN * 2.2)

        self.play(FadeOut(warning), FadeOut(actual_t), FadeOut(actual_t_label),
                  FadeOut(actual_c), FadeOut(actual_c_label),
                  FadeOut(bias_eq), FadeOut(bias_note), run_time=0.7)
        self.play(FadeIn(bridge_title, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(rows_block, shift=UP * 0.15), run_time=1.4)
        self.play(FadeIn(random_badge), FadeIn(not_random), run_time=0.8)
        self.play(Write(pivot), run_time=1.4)
        self.wait(15.86 - 4.9)
        self.wait(self.WAIT_TAIL)
