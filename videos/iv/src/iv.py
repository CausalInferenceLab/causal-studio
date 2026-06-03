"""IV (Instrumental Variables) 영상 Scene 모음.

7 Scenes, 총 ~7분 50초:
  Scene 01: 존 스노우 도입 (도구변수 = 자연이 던진 동전)
  Scene 02: 태블릿 RCT 복습 + 비순응으로 단순 비교가 깨짐
  Scene 03: 순응자/언제나-받는/절대-안받는 세 유형 + LATE
  Scene 04: 와알드 추정량 = ITT / 순응자 비율
  Scene 05: 도구변수 세 가정 (적합성/배제/독립성)
  Scene 06: 1969 베트남 징집 추첨 = 국가 규모 IV
  Scene 07: 아웃트로 (현실 속 우연 찾기)

작업 흐름: .claude/skills/manim-video-pipeline/SKILL.md 참조.
"""

import json
from pathlib import Path

from manim import *


TOPIC_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"

# 색상 의미 — 모든 Scene에서 일관되게 사용
ACCENT = YELLOW_E
COIN_COLOR = YELLOW_E
TREAT_COLOR = TEAL_C
CONTROL_COLOR = BLUE_C
FORBIDDEN = MAROON_C
CLEAN_WATER = BLUE_C
DIRTY_WATER = MAROON_C
INSTRUMENT = ORANGE
COMPLIER = GREEN
ALWAYS_TAKER = RED_C
NEVER_TAKER = BLUE_E
SOFT = GREY_B


def load_icon(filename: str, color: str = WHITE, height: float = 1.0) -> SVGMobject:
    icon = SVGMobject(str(ASSET_DIR / filename))
    icon.set_stroke(color=color, width=2.6, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def load_scene_timing_durations(scene_basename: str) -> list[float]:
    payload = json.loads(
        (TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json").read_text()
    )
    return [float(chunk["duration"]) for chunk in payload["chunks"]]


def make_forbidden_card(label: str, width: float = 2.6, height: float = 1.6) -> VGroup:
    """금지된 시나리오 카드: 라벨 + 빨간 X 오버레이."""
    frame = RoundedRectangle(
        width=width, height=height,
        corner_radius=0.14,
        stroke_color=FORBIDDEN, stroke_width=2.4,
    )
    text = Text(label, font_size=22, color=WHITE, line_spacing=0.9)
    text.move_to(frame.get_center())
    x1 = Line(frame.get_corner(UL), frame.get_corner(DR), color=FORBIDDEN, stroke_width=4)
    x2 = Line(frame.get_corner(UR), frame.get_corner(DL), color=FORBIDDEN, stroke_width=4)
    return VGroup(frame, text, x1, x2)


def make_school_dot(color: str, radius: float = 0.20) -> Dot:
    return Dot(radius=radius, color=color)


def make_school_row(count: int, color: str, spacing: float = 0.45) -> VGroup:
    dots = VGroup(*[make_school_dot(color) for _ in range(count)])
    dots.arrange(RIGHT, buff=spacing)
    return dots


def make_lock(color: str = WHITE, height: float = 0.9) -> SVGMobject:
    icon = load_icon("lock.svg", color, height)
    return icon


def make_unlock(color: str = WHITE, height: float = 0.9) -> SVGMobject:
    icon = load_icon("lock-open.svg", color, height)
    return icon


# ═══════════════════════════════════════════════════════════════════
# Scene 01 — Snow Pumps
# ═══════════════════════════════════════════════════════════════════


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
    Script: src/scripts/01_snow_pumps.txt — 7 chunks, 79.97s
    """

    WAIT_TAIL = 2.0

    def construct(self):
        durations = load_scene_timing_durations("01_snow_pumps")

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


# ═══════════════════════════════════════════════════════════════════
# Scene 02 — RCT Recap & Non-compliance Break
# ═══════════════════════════════════════════════════════════════════


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

    Script: src/scripts/02_rct_recap_break.txt — 5 chunks, 70.4s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("02_rct_recap_break")
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


# ═══════════════════════════════════════════════════════════════════
# Scene 03 — Three Types (Compliers / Always / Never)
# ═══════════════════════════════════════════════════════════════════


class Scene03_ThreeTypes(Scene):
    """
    Scene 03: 비순응의 세 유형 + LATE.

    Core Claim:
    동전이 움직이는 사람은 순응자뿐이다.
    따라서 도구변수가 짚어 내는 효과는 전체 평균 처치 효과(ATE)가 아니라,
    순응자에 한정된 국소 평균 처치 효과(LATE)이다.

    Visual Pivot:
    동전이 처치/통제로 떨어지는 두 세계를 평행 트랙으로 보여줘서,
    같은 사람이 두 세계에서 어떻게 행동하는지를 한 번에 비교.

    Script: src/scripts/03_three_types.txt — 6 chunks, 70.3s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("03_three_types")
        # durations ≈ [8.02, 11.86, 13.01, 10.20, 16.06, 11.16]

        # Beat 1 (0~8.02s): 세 유형 소개
        title = Text("동전이 움직이는 세 유형", font_size=30, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.4)
        type_names = ["순응자", "언제나 받음", "절대 안 받음"]
        type_colors = [COMPLIER, ALWAYS_TAKER, NEVER_TAKER]
        cards = VGroup()
        for name, color in zip(type_names, type_colors):
            frame = RoundedRectangle(width=3.4, height=1.1, corner_radius=0.16,
                                       stroke_color=color, stroke_width=2.5)
            label = Text(name, font_size=24, weight=BOLD, color=color).move_to(frame.get_center())
            cards.add(VGroup(frame, label))
        cards.arrange(RIGHT, buff=0.4).move_to(UP * 0.6)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.25), run_time=1.6)
        self.wait(8.02 - 2.2)

        # Beat 2 (8.02~19.88s): 순응자 — 동전 따라감
        # 두 평행 트랙: 배정 처치 / 배정 통제, 각 트랙 위에 순응자가 어떻게 행동하는지
        # 작은 카드 상단 유지는 480p에서 가독성이 떨어지므로 FadeOut으로 정리한다.
        # 타입 식별은 dot 색 + 캡션이 담당한다.

        track_label_z1 = Text("배정 = 처치", font_size=20, color=COIN_COLOR)
        track_label_z0 = Text("배정 = 통제", font_size=20, color=COIN_COLOR)
        track_z1 = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY_C, stroke_width=2)
        track_z0 = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY_C, stroke_width=2)
        track1_block = VGroup(track_label_z1, track_z1).arrange(RIGHT, buff=0.4)
        track0_block = VGroup(track_label_z0, track_z0).arrange(RIGHT, buff=0.4)
        tracks = VGroup(track1_block, track0_block).arrange(DOWN, aligned_edge=LEFT, buff=1.0).move_to(DOWN * 0.6)

        complier_z1_dot = Dot(radius=0.18, color=TREAT_COLOR).move_to(track_z1.get_center())
        complier_z0_dot = Dot(radius=0.18, color=CONTROL_COLOR).move_to(track_z0.get_center())
        complier_caption = Text("순응자: 동전이 가리키는 대로 행동", font_size=24, color=COMPLIER).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(cards), run_time=0.5)
        self.play(FadeIn(tracks, shift=DOWN * 0.1), run_time=0.8)
        self.play(FadeIn(complier_z1_dot, scale=0.7), FadeIn(complier_z0_dot, scale=0.7), run_time=0.8)
        self.play(Write(complier_caption), run_time=1.2)
        self.wait(11.86 - 3.3)

        # Beat 3 (19.88~32.89s): 언제나 받음 — 두 트랙 모두 처치색
        always_z1 = Dot(radius=0.18, color=ALWAYS_TAKER).move_to(track_z1.get_center() + RIGHT * 0.8)
        always_z0 = Dot(radius=0.18, color=ALWAYS_TAKER).move_to(track_z0.get_center() + RIGHT * 0.8)
        always_caption = Text("언제나 받음: 동전과 무관하게 처치", font_size=24, color=ALWAYS_TAKER).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(complier_caption), run_time=0.4)
        self.play(FadeIn(always_z1, scale=0.7), FadeIn(always_z0, scale=0.7), run_time=0.8)
        self.play(Write(always_caption), run_time=1.2)
        self.wait(13.01 - 2.4)

        # Beat 4 (32.89~43.09s): 절대 안 받음 — 두 트랙 모두 통제색
        never_z1 = Dot(radius=0.18, color=NEVER_TAKER).move_to(track_z1.get_center() - RIGHT * 0.8)
        never_z0 = Dot(radius=0.18, color=NEVER_TAKER).move_to(track_z0.get_center() - RIGHT * 0.8)
        never_caption = Text("절대 안 받음: 동전과 무관하게 비처치", font_size=24, color=NEVER_TAKER).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(always_caption), run_time=0.4)
        self.play(FadeIn(never_z1, scale=0.7), FadeIn(never_z0, scale=0.7), run_time=0.8)
        self.play(Write(never_caption), run_time=1.2)
        self.wait(10.20 - 2.4)

        # Beat 5 (43.09~59.15s): 핵심 — 순응자만 동전에 반응
        # 다른 dot들은 적당히 약화(0.45), complier만 박스로 강조.
        self.play(FadeOut(never_caption), run_time=0.4)
        reveal = Text("동전 결과에 따라 움직이는 건 순응자뿐", font_size=26, weight=BOLD, color=COMPLIER).to_edge(DOWN, buff=0.5)
        complier_box_top = SurroundingRectangle(complier_z1_dot, color=COMPLIER, buff=0.15, stroke_width=3)
        complier_box_bot = SurroundingRectangle(complier_z0_dot, color=COMPLIER, buff=0.15, stroke_width=3)
        self.play(
            always_z1.animate.set_opacity(0.45), always_z0.animate.set_opacity(0.45),
            never_z1.animate.set_opacity(0.45), never_z0.animate.set_opacity(0.45),
            run_time=0.7,
        )
        self.play(Create(complier_box_top), Create(complier_box_bot), run_time=0.9)
        self.play(Write(reveal), run_time=1.4)
        self.wait(16.06 - 3.4)

        # Beat 6 (59.15~70.31s): LATE 정의 카드
        late_box = RoundedRectangle(width=8.0, height=2.0, corner_radius=0.2,
                                      stroke_color=INSTRUMENT, stroke_width=3)
        late_title = Text("LATE", font_size=42, weight=BOLD, color=INSTRUMENT)
        late_sub = Text("Local Average Treatment Effect\n순응자에 한정된 평균 처치 효과", font_size=22,
                         color=WHITE, line_spacing=0.95)
        late_stack = VGroup(late_title, late_sub).arrange(DOWN, buff=0.25).move_to(late_box.get_center())
        late_group = VGroup(late_box, late_stack).move_to(ORIGIN)

        prior = VGroup(tracks, complier_z1_dot, complier_z0_dot,
                        complier_box_top, complier_box_bot,
                        always_z1, always_z0, never_z1, never_z0, reveal, title)
        self.play(FadeOut(prior), run_time=0.7)
        self.play(Create(late_box), run_time=0.9)
        self.play(FadeIn(late_stack, shift=UP * 0.2), run_time=1.4)
        self.wait(11.16 - 3.0)
        self.wait(self.WAIT_TAIL)


# ═══════════════════════════════════════════════════════════════════
# Scene 04 — Wald Machinery (Numerator / Denominator)
# ═══════════════════════════════════════════════════════════════════


class Scene04_IvMachinery(Scene):
    """
    Scene 04: 와알드 추정량 = ITT / 순응자 비율.

    Core Claim:
    LATE를 숫자로 구하는 식은 ITT(배정 결과 차이)를 순응자 비율로
    나눈 비율이다. 분자는 동전이 만든 총 효과, 분모는 동전이 실제로
    움직인 비율, 둘을 나누면 "한 명의 순응자에게 처치가 만든 효과"가 된다.

    Visual Pivot:
    분자와 분모가 처음에는 따로 등장해 의미가 명확히 분리된 뒤,
    마지막에 분수선 위/아래로 합쳐지며 한 식으로 수렴.

    Script: src/scripts/04_iv_machinery.txt — 6 chunks, 79.51s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("04_iv_machinery")
        # durations ≈ [7.42, 16.85, 18.12, 5.95, 14.57, 16.61]

        # Beat 1 (0~7.42s): "식은 간단하다" 인트로
        title = Text("LATE를 숫자로 구하기", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        intro = Text("식은 의외로 간단합니다", font_size=26, color=SOFT).move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(intro), run_time=1.2)
        self.wait(7.42 - 1.9)

        # Beat 2 (7.42~24.27s): 분자 — 배정별 평균 점수 차이
        # 라벨은 title 바로 아래에 두어 "이 차이" 위쪽 텍스트와 충돌 방지.
        numerator_label = Text("분자: 배정으로 만든 점수 차이", font_size=24, color=COIN_COLOR).next_to(title, DOWN, buff=0.4)
        score_z1 = Text("처치 배정\n평균 점수", font_size=20, color=TREAT_COLOR, line_spacing=0.9)
        score_z0 = Text("통제 배정\n평균 점수", font_size=20, color=CONTROL_COLOR, line_spacing=0.9)
        # 바 높이를 축소해 위쪽 라벨과 간격 확보.
        bar_z1 = Rectangle(width=0.8, height=1.7, color=TREAT_COLOR, fill_opacity=0.7, stroke_width=0)
        bar_z0 = Rectangle(width=0.8, height=1.3, color=CONTROL_COLOR, fill_opacity=0.7, stroke_width=0)
        bar_block_z1 = VGroup(bar_z1, score_z1).arrange(DOWN, buff=0.25)
        bar_block_z0 = VGroup(bar_z0, score_z0).arrange(DOWN, buff=0.25)
        # 바닥선 정렬로 바 차트 느낌, 위치는 좀 더 아래로 내려 vertical 여백 확보.
        bars = VGroup(bar_block_z1, bar_block_z0).arrange(RIGHT, buff=1.4, aligned_edge=DOWN).move_to(DOWN * 1.1)
        diff_brace = Brace(VGroup(bar_z1, bar_z0), direction=UP, buff=0.25, color=COIN_COLOR)
        diff_text = Text("이 차이", font_size=22, color=COIN_COLOR).next_to(diff_brace, UP, buff=0.2)

        self.play(FadeOut(intro), run_time=0.4)
        self.play(FadeIn(numerator_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(bars, shift=UP * 0.15), run_time=1.2)
        self.play(GrowFromCenter(diff_brace), FadeIn(diff_text, shift=DOWN * 0.1), run_time=1.0)
        self.wait(16.85 - 3.3)

        # Beat 3 (24.27~42.39s): 작게 나오는 이유 — 순응자만 움직임
        explain = Text("이 차이는 순응자만이 만든다", font_size=26, weight=BOLD, color=COMPLIER).move_to(DOWN * 2.5)
        complier_note = Text("(언제나 받음 / 절대 안 받음 학교는 동전에 무반응)", font_size=18, color=SOFT).next_to(explain, DOWN, buff=0.2)
        # 분자 차이를 살짝 줄여서 시각적으로 강조
        self.play(FadeIn(explain, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(complier_note, shift=UP * 0.05), run_time=0.7)
        # 박스로 분자 묶기 (buff 키워 내용 튀어나옴 방지)
        numer_box = SurroundingRectangle(VGroup(bars, diff_brace, diff_text), color=COIN_COLOR, buff=0.4)
        self.play(Create(numer_box), run_time=1.0)
        self.wait(18.12 - 2.7)

        # Beat 4 (42.39~48.34s): "그래서 비율로 나눠야 한다"
        divide_caption = Text("→ 순응자 비율로 나눠 환산한다", font_size=26, color=ACCENT).move_to(DOWN * 3.3)
        self.play(FadeOut(complier_note), run_time=0.3)
        self.play(FadeIn(divide_caption, shift=UP * 0.1), run_time=1.0)
        self.wait(5.95 - 1.3)

        # Beat 5 (48.34~62.91s): 분모 — 실제 사용 비율 차이 = 순응자 비율
        # 화면 정리 후 새 분모 시각화
        previous = VGroup(numerator_label, bars, diff_brace, diff_text,
                          explain, numer_box, divide_caption)
        self.play(FadeOut(previous), run_time=0.7)
        denom_label = Text("분모: 동전이 움직인 비율", font_size=24, color=INSTRUMENT).move_to(UP * 1.6)
        # 두 그룹: 처치 배정 중 실제 사용 비율 / 통제 배정 중 실제 사용 비율
        ratio_block_left = self._make_ratio_block("처치 배정 중\n실제 사용", filled=6, total=8, color=TREAT_COLOR)
        ratio_block_right = self._make_ratio_block("통제 배정 중\n실제 사용", filled=2, total=8, color=CONTROL_COLOR)
        ratios = VGroup(ratio_block_left, ratio_block_right).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.2)
        complier_pct = Text("≈ 순응자 비율 (6/8 − 2/8 = 50%)", font_size=22, color=COMPLIER).move_to(DOWN * 2.5)

        self.play(FadeIn(denom_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(ratios, shift=UP * 0.15), run_time=1.5)
        self.play(Write(complier_pct), run_time=1.4)
        self.wait(14.57 - 3.6)

        # Beat 6 (62.91~79.52s): 와알드 추정량 = 분자 / 분모
        self.play(FadeOut(VGroup(denom_label, ratios, complier_pct)), run_time=0.7)
        wald_title = Text("와알드 추정량 (Wald Estimator)", font_size=28, weight=BOLD, color=INSTRUMENT).to_edge(UP, buff=1.2)
        numer_line = Text("배정으로 만든 점수 차이", font_size=26, color=COIN_COLOR)
        bar = Line(LEFT * 3.2, RIGHT * 3.2, color=WHITE, stroke_width=3)
        denom_line = Text("순응자 비율", font_size=26, color=INSTRUMENT)
        fraction = VGroup(numer_line, bar, denom_line).arrange(DOWN, buff=0.25).move_to(ORIGIN + UP * 0.1)
        equals = Text("=  LATE", font_size=30, weight=BOLD, color=COMPLIER).next_to(fraction, DOWN, buff=0.5)
        meaning = Text("한 순응자에게 처치가 만든 효과", font_size=22, color=SOFT).next_to(equals, DOWN, buff=0.3)

        self.play(FadeIn(wald_title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(numer_line, shift=UP * 0.1), run_time=0.9)
        self.play(Create(bar), run_time=0.5)
        self.play(FadeIn(denom_line, shift=DOWN * 0.1), run_time=0.9)
        self.play(Write(equals), run_time=1.0)
        self.play(FadeIn(meaning, shift=UP * 0.05), run_time=0.9)
        self.wait(16.61 - 4.9)
        self.wait(self.WAIT_TAIL)

    @staticmethod
    def _make_ratio_block(title_text: str, filled: int, total: int, color: str) -> VGroup:
        title = Text(title_text, font_size=20, color=color, line_spacing=0.9)
        dots = VGroup()
        for i in range(total):
            d = Dot(radius=0.13, color=color if i < filled else GREY_D)
            if i >= filled:
                d.set_fill(opacity=0.3)
            dots.add(d)
        dots.arrange(RIGHT, buff=0.18)
        ratio_text = Text(f"{filled}/{total}", font_size=24, weight=BOLD, color=color)
        block = VGroup(title, dots, ratio_text).arrange(DOWN, buff=0.25)
        return block


# ═══════════════════════════════════════════════════════════════════
# Scene 05 — Three Assumptions (Locks)
# ═══════════════════════════════════════════════════════════════════


class Scene05_ThreeAssumptions(Scene):
    """
    Scene 05: 도구변수 세 가정 — 적합성, 배제, 독립성.

    Core Claim:
    와알드 식의 정당성은 세 가정 모두에 동시에 매달려 있다.
    적합성이 약하면 분모가 0에 가까워져 추정값이 폭주하고,
    배제 조건이 깨지면 분자가 처치 외 경로로 오염되며,
    독립성이 깨지면 처음부터 무작위성이 없는 셈이다.

    Visual Pivot:
    세 자물쇠가 차례로 등장해 마지막에 동시에 풀리는 순간 —
    어느 하나라도 잠겨 있으면 IV의 문은 열리지 않는다.

    Script: src/scripts/05_three_assumptions.txt — 5 chunks, 71.06s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("05_three_assumptions")
        # durations ≈ [11.90, 17.66, 17.76, 14.57, 9.17]

        # Beat 1 (0~11.90s): 세 자물쇠 등장
        title = Text("도구변수의 세 자물쇠", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        lock_names = ["적합성", "배제 조건", "독립성"]
        locks = VGroup()
        for name in lock_names:
            lk = load_icon("lock.svg", FORBIDDEN, 1.1)
            nm = Text(name, font_size=22, weight=BOLD, color=WHITE).next_to(lk, DOWN, buff=0.25)
            locks.add(VGroup(lk, nm))
        locks.arrange(RIGHT, buff=1.5).move_to(DOWN * 0.4)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(lk, shift=UP * 0.15) for lk in locks], lag_ratio=0.25), run_time=1.6)
        warning = Text("하나라도 어긋나면 결과를 믿을 수 없다", font_size=22, color=SOFT).to_edge(DOWN, buff=0.6)
        self.play(Write(warning), run_time=1.4)
        self.wait(11.90 - 3.7)

        # Beat 2 (11.90~29.56s): 적합성 — Z가 T를 실제로 움직여야 함
        # locks을 상단에 작게 남기지 않는다 (Beat 4의 indep_title과 충돌).
        # Beat 2~4 동안 무대를 비우고, Beat 5에서 unlock 상태로 다시 등장시킨다.
        self.play(FadeOut(warning), FadeOut(locks), run_time=0.8)

        # DAG: Z → T 화살표 두께가 핵심
        z_node = Circle(radius=0.45, color=INSTRUMENT, stroke_width=3)
        z_text = Text("Z", font_size=26, weight=BOLD, color=INSTRUMENT).move_to(z_node)
        z_grp = VGroup(z_node, z_text).move_to(LEFT * 2.8 + DOWN * 0.5)
        t_node = Circle(radius=0.45, color=TREAT_COLOR, stroke_width=3)
        t_text = Text("T", font_size=26, weight=BOLD, color=TREAT_COLOR).move_to(t_node)
        t_grp = VGroup(t_node, t_text).move_to(RIGHT * 2.8 + DOWN * 0.5)
        strong_arrow = Arrow(z_grp.get_right(), t_grp.get_left(), buff=0.12, color=GREEN, stroke_width=8)
        strong_label = Text("Z가 T를 강하게 움직임 ✓", font_size=22, color=GREEN).next_to(strong_arrow, UP, buff=0.3)
        weak_arrow = Arrow(z_grp.get_right(), t_grp.get_left(), buff=0.12, color=FORBIDDEN, stroke_width=2)
        weak_label = Text("약하면 분모 ≈ 0 → 추정값 폭주 ✗", font_size=22, color=FORBIDDEN).next_to(weak_arrow, DOWN, buff=0.3)

        self.play(FadeIn(z_grp), FadeIn(t_grp), run_time=0.8)
        self.play(GrowArrow(strong_arrow), FadeIn(strong_label, shift=DOWN * 0.1), run_time=1.0)
        self.play(Transform(strong_arrow, weak_arrow), FadeIn(weak_label, shift=UP * 0.1), run_time=1.4)
        self.wait(17.66 - 3.2)

        # Beat 3 (29.56~47.32s): 배제 조건 — Z → Y는 오직 T를 통해서만
        previous = VGroup(z_grp, t_grp, strong_arrow, strong_label, weak_label)
        self.play(FadeOut(previous), run_time=0.6)

        # DAG: Z → T → Y, 그리고 Z → Y 직접 경로가 금지
        z_node2 = Circle(radius=0.4, color=INSTRUMENT, stroke_width=3)
        z_text2 = Text("Z", font_size=24, weight=BOLD, color=INSTRUMENT).move_to(z_node2)
        z_grp2 = VGroup(z_node2, z_text2).move_to(LEFT * 3.5 + DOWN * 0.3)
        t_node2 = Circle(radius=0.4, color=TREAT_COLOR, stroke_width=3)
        t_text2 = Text("T", font_size=24, weight=BOLD, color=TREAT_COLOR).move_to(t_node2)
        t_grp2 = VGroup(t_node2, t_text2).move_to(ORIGIN + DOWN * 0.3)
        y_node2 = Circle(radius=0.4, color=CONTROL_COLOR, stroke_width=3)
        y_text2 = Text("Y", font_size=24, weight=BOLD, color=CONTROL_COLOR).move_to(y_node2)
        y_grp2 = VGroup(y_node2, y_text2).move_to(RIGHT * 3.5 + DOWN * 0.3)
        zt_arrow2 = Arrow(z_grp2.get_right(), t_grp2.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        ty_arrow2 = Arrow(t_grp2.get_right(), y_grp2.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        # 금지된 직접 경로 (Z → Y arc) 빨간 X로
        zy_arc = CurvedArrow(z_grp2.get_top(), y_grp2.get_top(), color=FORBIDDEN, stroke_width=3, angle=-1.4)
        zy_cross = Cross(zy_arc, stroke_color=FORBIDDEN, stroke_width=4).scale(1.0)
        excl_label = Text("Z → Y의 영향은 오직 T를 거쳐야 한다", font_size=22, color=WHITE).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(z_grp2), FadeIn(t_grp2), FadeIn(y_grp2), run_time=0.9)
        self.play(GrowArrow(zt_arrow2), GrowArrow(ty_arrow2), run_time=0.9)
        self.play(Create(zy_arc), run_time=0.8)
        self.play(FadeIn(zy_cross, scale=0.7), run_time=0.6)
        self.play(Write(excl_label), run_time=1.4)
        self.wait(17.76 - 4.6)

        # Beat 4 (47.32~61.89s): 독립성 — Z ⊥ (Y_0, Y_1)
        previous2 = VGroup(z_grp2, t_grp2, y_grp2, zt_arrow2, ty_arrow2, zy_arc, zy_cross, excl_label)
        self.play(FadeOut(previous2), run_time=0.6)
        indep_title = Text("Z는 잠재적 결과와 독립이어야 한다", font_size=26, weight=BOLD, color=ACCENT).to_edge(UP, buff=1.4)
        coin_small = load_icon("coin.svg", COIN_COLOR, 1.0).move_to(LEFT * 3.0)
        latent_box = RoundedRectangle(width=3.8, height=1.4, corner_radius=0.15,
                                       stroke_color=SOFT, stroke_width=2)
        latent_text = Text("잠재적 결과\n( 와이 0, 와이 1 )", font_size=22, color=WHITE, line_spacing=0.95).move_to(latent_box.get_center())
        latent_grp = VGroup(latent_box, latent_text).move_to(RIGHT * 2.5)
        indep_sym = Text("⊥", font_size=46, weight=BOLD, color=GREEN).move_to(ORIGIN)
        check_note = Text("RCT 배정이라면 설계상 만족\n자연의 동전이라면 따져 봐야 한다", font_size=20, color=SOFT, line_spacing=0.95).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(indep_title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(coin_small), FadeIn(latent_grp), run_time=1.0)
        self.play(Write(indep_sym), run_time=0.8)
        self.play(FadeIn(check_note, shift=UP * 0.1), run_time=1.4)
        self.wait(14.57 - 3.9)

        # Beat 5 (61.89~71.06s): 세 자물쇠 모두 풀림
        previous3 = VGroup(indep_title, coin_small, latent_grp, indep_sym, check_note)
        self.play(FadeOut(previous3), run_time=0.6)
        # unlock 자물쇠를 새로 등장시킨다 (Beat 2에서 원래 locks을 FadeOut했음).
        unlocks = VGroup()
        for name in lock_names:
            uk = load_icon("lock-open.svg", GREEN, 1.1)
            nm = Text(name, font_size=22, weight=BOLD, color=GREEN).next_to(uk, DOWN, buff=0.25)
            unlocks.add(VGroup(uk, nm))
        unlocks.arrange(RIGHT, buff=1.5).move_to(DOWN * 0.4)
        door_caption = Text("세 자물쇠가 모두 풀려야 도구변수의 문이 열린다", font_size=24, weight=BOLD, color=INSTRUMENT).to_edge(DOWN, buff=0.6)

        self.play(LaggedStart(*[FadeIn(uk, shift=UP * 0.15) for uk in unlocks], lag_ratio=0.2), run_time=1.4)
        self.play(Write(door_caption), run_time=1.6)
        self.wait(9.17 - 3.0)
        self.wait(self.WAIT_TAIL)


# ═══════════════════════════════════════════════════════════════════
# Scene 06 — Draft Lottery (Vietnam, 1969)
# ═══════════════════════════════════════════════════════════════════


class Scene06_DraftLottery(Scene):
    """
    Scene 06: 1969 베트남 징집 추첨 = 국가 규모 IV.

    Core Claim:
    스노우의 수도 회사 트릭은 한 도시 위생 연구에 머무르지 않았다.
    한 세기 뒤 미국에서, 빙고 추첨이라는 자연의 동전이 군 복무가
    평생 소득에 미친 효과를 추정하는 도구변수로 쓰였다.

    Visual Pivot:
    빙고볼이 떨어지며 생일 번호가 결정되는 순간 — 우연이 사람을
    움직였다. 스노우의 수도 배관과 같은 구조다.

    Script: src/scripts/06_draft_lottery.txt — 5 chunks, 66.10s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("06_draft_lottery")
        # durations ≈ [6.72, 22.97, 10.56, 11.40, 14.45]

        # Beat 1 (0~6.72s): 국가 규모로 작동
        title = Text("같은 트릭, 국가 규모", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        scale_up = Text("작은 실험만이 아니다", font_size=24, color=SOFT).move_to(ORIGIN + UP * 0.2)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(scale_up), run_time=1.2)
        self.wait(6.72 - 1.9)

        # Beat 2 (6.72~29.69s): 1969 베트남 징집 추첨
        self.play(FadeOut(scale_up), run_time=0.4)
        date_label = Text("1969년 · 미국", font_size=28, weight=BOLD, color=SOFT).to_edge(UP, buff=1.4)
        # 빙고볼 시뮬레이션: 3개 공
        balls = VGroup()
        ball_nums = ["73", "144", "012"]
        for i, num in enumerate(ball_nums):
            ball = Circle(radius=0.5, color=ACCENT, stroke_width=3, fill_color=YELLOW_A, fill_opacity=0.9)
            ball_num = Text(num, font_size=22, weight=BOLD, color=BLACK).move_to(ball)
            balls.add(VGroup(ball, ball_num))
        balls.arrange(RIGHT, buff=0.5).move_to(UP * 0.2)
        ball_caption = Text("생일 365일이 적힌 공을 무작위로 추첨", font_size=22, color=WHITE).next_to(balls, DOWN, buff=0.5)
        rule = Text("낮은 번호 → 입대", font_size=24, weight=BOLD, color=INSTRUMENT).move_to(DOWN * 1.5)
        independence_note = Text("태어난 날짜는 학력, 직업과 무관", font_size=20, color=SOFT).next_to(rule, DOWN, buff=0.3)

        self.play(FadeIn(date_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2, scale=0.7) for b in balls], lag_ratio=0.2), run_time=1.4)
        self.play(Write(ball_caption), run_time=1.4)
        self.play(Write(rule), run_time=1.0)
        self.play(FadeIn(independence_note, shift=UP * 0.1), run_time=0.9)
        self.wait(22.97 - 5.4)

        # Beat 3 (29.69~40.25s): 앵그리스트의 질문
        prior = VGroup(date_label, balls, ball_caption, rule, independence_note)
        self.play(FadeOut(prior), run_time=0.6)
        angrist = Text("조슈아 앵그리스트의 질문", font_size=26, weight=BOLD, color=ACCENT).to_edge(UP, buff=1.2)
        question = Text("\"군 복무가 평생 소득에 어떤 영향을 줄까?\"", font_size=26, color=WHITE).move_to(ORIGIN + UP * 0.4)
        # T → Y
        t_q = Text("군 복무", font_size=24, color=TREAT_COLOR)
        y_q = Text("평생 소득", font_size=24, color=CONTROL_COLOR)
        arrow_q = Arrow(LEFT * 1.0, RIGHT * 1.0, buff=0.05, color=WHITE, stroke_width=4)
        chain = VGroup(t_q, arrow_q, y_q).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.0)

        self.play(FadeIn(angrist, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(question), run_time=1.4)
        self.play(FadeIn(chain, shift=UP * 0.1), run_time=1.0)
        self.wait(10.56 - 3.1)

        # Beat 4 (40.25~51.65s): 단순 비교는 편향 — 참전 선택의 차이
        # chain을 작게 위로 정리, 편향 경고
        bias_warn = Text("참전 군인 vs 비참전 군인 단순 비교 → 편향", font_size=24, color=FORBIDDEN).to_edge(DOWN, buff=2.2)
        bias_reason = Text("참전을 선택한 사람과 회피한 사람은 애초에 다르다", font_size=20, color=SOFT).next_to(bias_warn, DOWN, buff=0.25)
        self.play(FadeIn(bias_warn, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(bias_reason, shift=UP * 0.05), run_time=0.9)
        self.wait(11.40 - 1.9)

        # Beat 5 (51.65~66.10s): 추첨을 도구변수로 → 스노우 회귀
        prior2 = VGroup(angrist, question, chain, bias_warn, bias_reason)
        self.play(FadeOut(prior2), run_time=0.6)
        title_fix = Text("추첨 번호 = 도구변수", font_size=30, weight=BOLD, color=INSTRUMENT).to_edge(UP, buff=1.2)
        # DAG: Z(추첨) → T(복무) → Y(소득)
        z6 = Circle(radius=0.4, color=INSTRUMENT, stroke_width=3)
        z6t = Text("추첨", font_size=20, color=INSTRUMENT, weight=BOLD).move_to(z6)
        z6g = VGroup(z6, z6t).move_to(LEFT * 3.5 + DOWN * 0.2)
        t6 = Circle(radius=0.4, color=TREAT_COLOR, stroke_width=3)
        t6t = Text("복무", font_size=20, color=TREAT_COLOR, weight=BOLD).move_to(t6)
        t6g = VGroup(t6, t6t).move_to(ORIGIN + DOWN * 0.2)
        y6 = Circle(radius=0.4, color=CONTROL_COLOR, stroke_width=3)
        y6t = Text("소득", font_size=20, color=CONTROL_COLOR, weight=BOLD).move_to(y6)
        y6g = VGroup(y6, y6t).move_to(RIGHT * 3.5 + DOWN * 0.2)
        zt6 = Arrow(z6g.get_right(), t6g.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        ty6 = Arrow(t6g.get_right(), y6g.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        callback = Text("한 세기 전 런던의 수도 회사 트릭이\n미국 노동시장에서도 통했다", font_size=22, color=SOFT, line_spacing=0.95).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(title_fix, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(z6g), FadeIn(t6g), FadeIn(y6g), run_time=0.9)
        self.play(GrowArrow(zt6), GrowArrow(ty6), run_time=0.9)
        self.play(Indicate(z6g, color=INSTRUMENT), run_time=0.8)
        self.play(Write(callback), run_time=1.6)
        self.wait(14.45 - 4.9)
        self.wait(self.WAIT_TAIL)


# ═══════════════════════════════════════════════════════════════════
# Scene 07 — Outro
# ═══════════════════════════════════════════════════════════════════


class Scene07_Outro(Scene):
    """
    Scene 07: 아웃트로 — 현실 속 우연 찾기.

    Core Claim:
    도구변수 분석에서 가장 어려운 일은 수식이 아니라, 현실 속에
    이미 존재하는 우연을 찾아내는 일이다. 무작위 배정이 불가능한
    질문 앞에서, 자연이 던진 동전을 찾는 안목이 다음 단계다.

    Visual Pivot:
    세 역사적 장면(수도 회사, 빙고볼, 생일)이 한 줄로 등장한 뒤,
    공통점인 "우연"이 한 단어로 응축되는 순간.

    Script: src/scripts/07_outro.txt — 3 chunks, 33.86s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("07_outro")
        # durations ≈ [16.56, 8.35, 8.95]

        # Beat 1 (0~16.56s): 세 장면 회상
        title = Text("우연은 이미 우리 곁에 있다", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        # 세 미니 카드
        snow = self._make_vignette("droplet.svg", CLEAN_WATER, "1854 런던", "수도 회사")
        draft = self._make_vignette("dice.svg", ACCENT, "1969 미국", "징집 추첨")
        birth = self._make_vignette("cake.svg", PINK, "어쩌면", "여러분의 생일")
        vignettes = VGroup(snow, draft, birth).arrange(RIGHT, buff=0.9).move_to(ORIGIN + UP * 0.2)
        common = Text("모두 현실 속 우연", font_size=24, color=SOFT).to_edge(DOWN, buff=1.2)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in vignettes], lag_ratio=0.25), run_time=1.8)
        self.play(Write(common), run_time=1.2)
        self.wait(16.56 - 3.7)

        # Beat 2 (16.56~24.91s): 가장 어려운 일은 우연 찾기
        self.play(FadeOut(common), run_time=0.4)
        hard_line = Text("가장 어려운 일은 수식이 아니라", font_size=26, color=WHITE).move_to(DOWN * 1.4)
        hard_line2 = Text("우연을 찾아내는 일이다", font_size=30, weight=BOLD, color=INSTRUMENT).next_to(hard_line, DOWN, buff=0.3)
        self.play(Write(hard_line), run_time=1.2)
        self.play(Write(hard_line2), run_time=1.4)
        self.wait(8.35 - 3.0)

        # Beat 3 (24.91~33.86s): 닫기 카드
        self.play(FadeOut(VGroup(title, vignettes, hard_line, hard_line2)), run_time=0.7)
        close_line1 = Text("무작위 배정을 할 수 없다면,", font_size=30, color=WHITE).move_to(UP * 0.6)
        close_line2 = Text("자연이 이미 던진 동전을 찾아내세요.", font_size=30, weight=BOLD, color=INSTRUMENT).next_to(close_line1, DOWN, buff=0.4)
        end_tag = Text("그게 인과추론의 다음 단계입니다.", font_size=22, color=SOFT).next_to(close_line2, DOWN, buff=0.6)

        self.play(Write(close_line1), run_time=1.2)
        self.play(Write(close_line2), run_time=1.4)
        self.play(FadeIn(end_tag, shift=UP * 0.1), run_time=1.0)
        self.wait(8.95 - 3.6)
        self.wait(self.WAIT_TAIL)

    @staticmethod
    def _make_vignette(icon_name: str, color: str, year: str, name: str) -> VGroup:
        try:
            icon = load_icon(icon_name, color, 0.9)
        except Exception:
            # 폴백: 색 원
            icon = Circle(radius=0.4, color=color, stroke_width=3)
        year_text = Text(year, font_size=20, color=color, weight=BOLD)
        name_text = Text(name, font_size=18, color=WHITE)
        block = VGroup(icon, year_text, name_text).arrange(DOWN, buff=0.25)
        return block
