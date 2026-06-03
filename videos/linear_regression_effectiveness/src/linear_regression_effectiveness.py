import json
from pathlib import Path

from manim import *


TOPIC_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"

ACCENT = YELLOW_E
RANDOM_COLOR = TEAL_C
OBS_COLOR = ORANGE
HIDDEN_COLOR = MAROON_C
SOFT = GREY_B


def load_icon(filename: str, color: str = WHITE, height: float = 1.1) -> SVGMobject:
    icon = SVGMobject(str(ASSET_DIR / filename))
    icon.set_stroke(color=color, width=2.6, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def load_scene_timing_durations(scene_basename: str) -> list[float]:
    payload = json.loads((TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json").read_text())
    return [float(chunk["duration"]) for chunk in payload["chunks"]]


def make_card(title: str, body: str, color: str, width: float = 4.0, height: float = 2.2) -> VGroup:
    frame = RoundedRectangle(
        width=width,
        height=height,
        corner_radius=0.18,
        stroke_color=color,
        stroke_width=2.8,
    )
    head = Text(title, font_size=28, weight=BOLD, color=color)
    head.next_to(frame.get_top(), DOWN, buff=0.28)
    body_text = Text(body, font_size=22, color=WHITE, line_spacing=0.9)
    body_text.move_to(frame.get_center() + DOWN * 0.15)
    return VGroup(frame, head, body_text)


class Scene01_RctVsObservationalIntro(Scene):
    """
    Scene 01: RCT vs Observational Intro

    Core Claim:
    무작위 배정에서는 회귀가 평균 차이를 압축해서 보여주지만,
    관찰자료에서는 먼저 변수 관계와 누락 가능성을 확인해야 한다.

    Expected Misconception:
    회귀식을 한 줄 쓰면 곧바로 인과효과를 읽을 수 있다고 느끼기 쉽다.

    Visual Pivot:
    왼쪽의 깔끔한 무작위 배정 카드에서,
    오른쪽의 관찰자료 카드와 숨은 변수 네트워크로 시선이 이동한 뒤,
    마지막에 체크리스트로 수렴한다.

    Notebook Reference:
    book/regression/05-The-Unreasonable-Effectiveness-of-Linear-Regression_minimal_ko.ipynb
    - Cell 0: 무작위 배정 vs 관찰자료 도입
    - Cell 2: wage.csv 사용
    - Cell 4: 변수 관계를 먼저 확인
    - Cell 6: 단순 회귀와 통제 회귀 비교 예고

    Script Reference:
    src/scripts/01_rct_vs_observational_intro.txt

    3Blue1Brown Reference:
    3b1b/_2020/covid.py - IntroQuestion
    Reason:
    하나의 질문에서 대비 구조를 만들고, 마지막에 체크리스트형 정리로 수렴하는 리듬이 유사해서.

    Script-to-Beat Mapping:
    1. chunk 1-3: 무작위 배정에서는 평균 차이와 같은 아이디어라는 도입
    2. chunk 4-5: 관찰자료에서는 계수를 바로 읽으면 안 된다는 경고
    3. chunk 6: wage.csv만 본다는 범위 고정
    4. chunk 7-8: 변수 관계와 누락변수편향 설명
    5. chunk 9: 분석 순서 체크리스트
    """

    WAIT_TAIL = 1.2

    def construct(self):
        durations = load_scene_timing_durations("01_rct_vs_observational_intro")

        title = Text("선형회귀는 언제 믿을 수 있을까?", font_size=34, weight=BOLD, color=ACCENT)
        title.to_edge(UP)

        random_card = make_card("무작위 배정", "평균 차이와\n같은 아이디어", RANDOM_COLOR)
        random_card.move_to(LEFT * 3.1 + UP * 0.2)
        random_icon = load_icon("arrows-shuffle.svg", RANDOM_COLOR, 0.9)
        random_icon.next_to(random_card[1], RIGHT, buff=0.2)

        obs_card = make_card("관찰자료", "계수를 바로\n인과효과로 읽지 않기", OBS_COLOR)
        obs_card.move_to(RIGHT * 3.0 + UP * 0.2)
        obs_icon = load_icon("alert-triangle.svg", OBS_COLOR, 0.9)
        obs_icon.next_to(obs_card[1], RIGHT, buff=0.2)

        bridge = Arrow(random_card.get_right(), obs_card.get_left(), buff=0.2, color=SOFT, stroke_width=3.5)
        bridge_label = Text("같은 회귀라도\n조건이 다르다", font_size=22, color=SOFT)
        bridge_label.next_to(bridge, UP, buff=0.22)

        # Beat 1
        # 남는 요소: 제목, 무작위 배정 카드
        # 새로 등장: 제목, 무작위 배정 카드, 화살표 라벨
        # 비워 두는 영역: 하단 절반
        # 핵심 시선 대상: 무작위 배정 카드
        self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.8)
        self.play(Create(random_card), FadeIn(random_icon, scale=0.85), run_time=1.2)
        self.wait(max(0.2, durations[0] - 2.0))
        self.play(GrowArrow(bridge), FadeIn(bridge_label, shift=UP * 0.1), run_time=0.9)
        self.wait(max(0.2, durations[1] - 0.9))
        same_idea = Text("회귀 = 평균 차이의 압축 표현", font_size=28, color=WHITE)
        same_idea.next_to(random_card, DOWN, buff=0.45)
        self.play(Write(same_idea), run_time=1.0)
        self.wait(max(0.2, durations[2] - 1.0))

        # Beat 2
        # 남는 요소: 제목, 두 카드, 연결 화살표
        # 새로 등장: 관찰자료 카드, 숨은 변수 원, 경고식
        # 비워 두는 영역: 좌하단
        # 핵심 시선 대상: 관찰자료 카드
        self.play(Create(obs_card), FadeIn(obs_icon, scale=0.85), run_time=1.0)
        self.wait(max(0.2, durations[3] - 1.0))

        wage_node = Circle(radius=0.42, color=WHITE, stroke_width=2.5)
        wage_label = Text("임금", font_size=20).move_to(wage_node)
        educ_node = Circle(radius=0.42, color=WHITE, stroke_width=2.5)
        educ_label = Text("교육", font_size=20).move_to(educ_node)
        hidden_node = Circle(radius=0.48, color=HIDDEN_COLOR, stroke_width=2.8)
        hidden_label = Text("숨은 변수", font_size=18, color=HIDDEN_COLOR).move_to(hidden_node)

        educ_group = VGroup(educ_node, educ_label).move_to(RIGHT * 1.8 + DOWN * 1.2)
        wage_group = VGroup(wage_node, wage_label).move_to(RIGHT * 3.5 + DOWN * 1.2)
        hidden_group = VGroup(hidden_node, hidden_label).move_to(RIGHT * 2.65 + DOWN * 2.35)
        arrow_ew = Arrow(educ_group.get_right(), wage_group.get_left(), buff=0.14, color=WHITE, stroke_width=3.2)
        arrow_he = Arrow(hidden_group.get_top(), educ_group.get_bottom(), buff=0.12, color=HIDDEN_COLOR, stroke_width=3.2)
        arrow_hw = Arrow(hidden_group.get_top(), wage_group.get_bottom(), buff=0.12, color=HIDDEN_COLOR, stroke_width=3.2)
        warn = Text("계수만 보면 위험", font_size=26, weight=BOLD, color=OBS_COLOR)
        warn.next_to(obs_card, DOWN, buff=0.42)

        self.play(FadeIn(warn, shift=UP * 0.1), Create(arrow_ew), FadeIn(educ_group), FadeIn(wage_group), run_time=1.2)
        self.play(GrowArrow(arrow_he), GrowArrow(arrow_hw), FadeIn(hidden_group, scale=0.9), run_time=1.0)
        self.wait(max(0.2, durations[4] - 2.2))

        # Beat 3
        # 남는 요소: 제목, 관찰자료 카드
        # 새로 등장: wage.csv 카드
        # 비워 두는 영역: 좌측 대부분
        # 핵심 시선 대상: wage.csv 카드
        file_icon = load_icon("file-spreadsheet.svg", ACCENT, 1.1)
        file_text = Text("wage.csv", font_size=28, weight=BOLD)
        file_sub = Text("이번 예제의 범위", font_size=22, color=SOFT)
        file_group = VGroup(file_icon, file_text, file_sub).arrange(DOWN, buff=0.18)
        file_group.move_to(LEFT * 3.0 + DOWN * 1.3)
        self.play(
            FadeOut(same_idea),
            FadeOut(bridge),
            FadeOut(bridge_label),
            FadeOut(educ_group),
            FadeOut(wage_group),
            FadeOut(hidden_group),
            FadeOut(arrow_ew),
            FadeOut(arrow_he),
            FadeOut(arrow_hw),
            FadeIn(file_group, shift=RIGHT * 0.2),
            run_time=1.0,
        )
        self.wait(max(0.2, durations[5] - 1.0))

        # Beat 4
        # 남는 요소: 제목, 관찰자료 카드, wage.csv 카드
        # 새로 등장: 변수 관계 네트워크, OVB 라벨
        # 비워 두는 영역: 상단 중앙
        # 핵심 시선 대상: 변수 관계 네트워크
        relation_title = Text("먼저 관계를 본다", font_size=28, weight=BOLD, color=ACCENT)
        relation_title.move_to(DOWN * 0.2)
        iq = Text("IQ", font_size=22)
        family = Text("가정 배경", font_size=22)
        educ = Text("교육", font_size=22)
        wage = Text("임금", font_size=22)
        iq.move_to(LEFT * 1.6 + DOWN * 1.4)
        family.move_to(LEFT * 0.2 + DOWN * 2.1)
        educ.move_to(RIGHT * 1.2 + DOWN * 1.4)
        wage.move_to(RIGHT * 2.8 + DOWN * 2.1)
        rel_arrows = VGroup(
            Arrow(iq.get_right(), educ.get_left(), buff=0.12, stroke_width=3),
            Arrow(family.get_right(), educ.get_bottom(), buff=0.12, stroke_width=3, color=HIDDEN_COLOR),
            Arrow(educ.get_right(), wage.get_left(), buff=0.12, stroke_width=3),
            Arrow(family.get_right(), wage.get_left(), buff=0.12, stroke_width=3, color=HIDDEN_COLOR),
        )
        ovb = Text("OVB", font_size=34, weight=BOLD, color=HIDDEN_COLOR)
        ovb.next_to(family, LEFT, buff=0.5)
        self.play(
            FadeIn(relation_title, shift=UP * 0.1),
            FadeIn(iq),
            FadeIn(family),
            FadeIn(educ),
            FadeIn(wage),
            *[GrowArrow(arr) for arr in rel_arrows],
            run_time=1.4,
        )
        self.wait(max(0.2, durations[6] - 1.4))
        self.play(Indicate(family, color=HIDDEN_COLOR), FadeIn(ovb, scale=0.85), run_time=1.0)
        self.wait(max(0.2, durations[7] - 1.0))

        # Beat 5
        # 남는 요소: 제목
        # 새로 등장: 분석 순서 체크리스트
        # 비워 두는 영역: 우하단 일부
        # 핵심 시선 대상: 체크리스트
        checklist = VGroup(
            Text("1. 관계 확인", font_size=28, color=WHITE),
            Text("2. 단순 회귀", font_size=28, color=WHITE),
            Text("3. 통제 회귀", font_size=28, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        checklist.move_to(DOWN * 1.0)
        accent_box = SurroundingRectangle(checklist[0], color=ACCENT, buff=0.15)
        self.play(
            FadeOut(obs_card),
            FadeOut(obs_icon),
            FadeOut(file_group),
            FadeOut(relation_title),
            FadeOut(iq),
            FadeOut(family),
            FadeOut(educ),
            FadeOut(wage),
            FadeOut(rel_arrows),
            FadeOut(ovb),
            FadeIn(checklist, shift=UP * 0.2),
            Create(accent_box),
            run_time=1.2,
        )
        self.play(accent_box.animate.surround(checklist[1], buff=0.15), run_time=0.8)
        self.play(accent_box.animate.surround(checklist[2], buff=0.15), run_time=0.8)
        self.wait(max(0.2, durations[8] - 2.8))
        self.wait(self.WAIT_TAIL)
