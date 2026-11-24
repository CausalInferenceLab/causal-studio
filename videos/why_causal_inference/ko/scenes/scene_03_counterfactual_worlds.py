from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_icon,
    make_tablet_icon,
    make_world_panel,
)


class Scene03_CounterfactualWorlds(Scene):
    """
    Scene 03: Counterfactual Worlds

    Core Claim:
    인과추론은 먼저 T_i와 Y_i를 정의하고,
    같은 대상의 잠재적 결과 Y_{1i}, Y_{0i}를 상정한 뒤,
    현실에서는 둘을 동시에 관찰할 수 없다는 문제를 마주한다.

    Expected Misconception:
    처치 여부와 결과 변수를 정의하면 인과효과도 곧바로 관찰할 수 있을 것처럼 보인다.

    Visual Pivot:
    T_i와 Y_i 표기에서 시작해 한 학생이 두 세계로 갈라지고,
    마지막에는 한쪽만 남아 사실 / 반사실 구조로 수렴한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - Section 1: 반사실과 잠재적 결과
    - T_i, Y_i 정의
    - Y_1, Y_0 도입과 반사실 관찰 불가능성

    Script Reference:
    narration/03_counterfactual_worlds.txt

    Asset Reference:
    Tabler Icons (MIT)
    - user.svg
    - device-tablet.svg
    - book-off.svg
    - school.svg
    - eye-off.svg
    - arrows-split-2.svg
    - circle-x.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py - IntroQuestion
    3b1b/videos/_2018/uncertainty.py
    Reason:
    전자는 질문을 단계적으로 분해하는 인트로 리듬을,
    후자는 동시에 볼 수 없는 두 가능 상태를 대비시키는 분위기를 참고했다.

    Script-to-Beat Mapping:
    1. T_i와 Y_i를 먼저 정의
    2. 두 가능한 세계 Y_{1i}, Y_{0i}를 바로 제시
    3. 둘 중 하나만 현실에 존재한다는 근본 문제 제시
    4. 사실 / 반사실 대비로 마무리
    """

    WAIT_TAIL = 10.0

    def construct(self):
        # Beat 1 준비:
        # 첫 화면은 표기법만 좁게 보여준다.
        # 먼저 T_i를 소개하고, 그 다음에 T_i = 1 / 0 두 갈래로 분기시킨다.
        treatment_seed = MathTex(r"T_i").scale(1.45).set_color(TABLET_COLOR)
        treatment_seed.move_to(LEFT * 2.35 + UP * 0.45)
        treatment_word = Text("처치", font_size=24, color=WHITE, weight=BOLD)
        treatment_word.next_to(treatment_seed, DOWN, buff=0.2)

        treatment_yes = VGroup(
            MathTex(r"T_i = 1").set_color(TABLET_COLOR),
            make_tablet_icon(TABLET_COLOR),
        ).arrange(RIGHT, buff=0.2)
        treatment_yes.move_to(RIGHT * 1.45 + UP * 1.45)

        treatment_no = VGroup(
            MathTex(r"T_i = 0").set_color(LIBRARY_COLOR),
            load_icon("device-tablet-off.svg", LIBRARY_COLOR, 1.45),
        ).arrange(RIGHT, buff=0.2)
        treatment_no.move_to(RIGHT * 1.45 + DOWN * 0.6)

        up_arrow = CurvedArrow(
            treatment_seed.get_right() + RIGHT * 0.05 + UP * 0.12,
            treatment_yes.get_left() + LEFT * 0.12 + DOWN * 0.04,
            angle=-0.52,
            stroke_width=3.6,
            color=TABLET_COLOR,
        )
        down_arrow = CurvedArrow(
            treatment_seed.get_right() + RIGHT * 0.05 + DOWN * 0.12,
            treatment_no.get_left() + LEFT * 0.12 + UP * 0.04,
            angle=0.52,
            stroke_width=3.6,
            color=LIBRARY_COLOR,
        )

        # Beat 1 -> Beat 2 연결:
        # 처치 표기법이 정리된 뒤에만 Y_i를 보여준다.
        # 처치와 결과 변수를 같은 화면에서 한꺼번에 설명하지 않기 위한 분리다.
        outcome_def = VGroup(
            MathTex(r"Y_i").scale(1.2).set_color(ACCENT_COLOR),
            Text("학업 성취도", font_size=26, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.22)
        outcome_def.move_to(UP * 0.45)
        outcome_icon = load_icon("school.svg", ACCENT_COLOR, 1.05)
        outcome_icon.next_to(outcome_def, DOWN, buff=0.34)

        treatment_group = VGroup(
            treatment_seed,
            treatment_word,
            up_arrow,
            down_arrow,
            treatment_yes,
            treatment_no,
        )

        left_world = make_world_panel("device-tablet.svg", r"T_i = 1", r"Y_{1i}", TABLET_COLOR)
        right_world = make_world_panel("device-tablet-off.svg", r"T_i = 0", r"Y_{0i}", LIBRARY_COLOR)
        worlds = VGroup(left_world, right_world).arrange(RIGHT, buff=1.1)
        worlds.move_to(DOWN * 0.15)

        left_label = Text("factual", font_size=22, color=TABLET_COLOR, weight=BOLD)
        left_label.next_to(left_world, UP, buff=0.22)
        right_label = Text("counterfactual", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
        right_label.next_to(right_world, UP, buff=0.22)

        unseen = load_icon("eye-off.svg", NEUTRAL_COLOR, 0.78)
        unseen.next_to(right_world[0], DOWN, buff=0.18)

        impossible = Text("둘 다 관찰할 수는 없다", font_size=25, color=QUESTION_COLOR, weight=BOLD)
        impossible.to_edge(DOWN, buff=0.78)
        impossible_line = Underline(impossible, color=QUESTION_COLOR, buff=0.12, stroke_width=2.4)
        counter_shade = SurroundingRectangle(
            right_world,
            buff=0.08,
            corner_radius=0.18,
            stroke_opacity=0,
            fill_color=BLACK,
            fill_opacity=0.0,
        )

        # Beat 3 목표 상태:
        # 먼저 두 세계를 좌우에 정리한 뒤, 반사실 세계 위에 반투명 가림막을 올린다.
        # 원래 색을 유지하면서 "관찰 불가"만 읽히게 하기 위한 처리다.
        factual_world_pos = LEFT * 3.0 + DOWN * 0.08
        counter_world_pos = RIGHT * 3.0 + DOWN * 0.08

        # Intro:
        # 첫 문장 "이제 직관을 넘어서..."는 빈 화면으로 받는다.
        # 표기법을 정리하겠다는 선언이므로, 시각 정보 없이 호흡만 확보한다.
        self.wait(6.2)

        # Beat 1:
        # 스크립트의 "먼저 T_i는 처치 여부를 뜻한다"를 처리한다.
        # 이어서 T_i = 1, T_i = 0 두 상태를 분기시켜 처치 개념을 시각적으로 고정한다.
        self.play(FadeIn(treatment_seed, scale=0.9), FadeIn(treatment_word, shift=UP * 0.08), run_time=1.0)
        self.wait(2.6)
        self.play(Create(up_arrow), Create(down_arrow), run_time=1.1)
        self.play(FadeIn(treatment_yes, shift=LEFT * 0.08), FadeIn(treatment_no, shift=LEFT * 0.08), run_time=1.0)
        self.wait(7.6)
        # 같은 화면에 정보를 더 쌓지 않고, 이제 결과 변수 Y_i로 전환한다.
        self.play(
            FadeOut(treatment_group, shift=LEFT * 0.08),
            FadeIn(outcome_def, shift=UP * 0.12),
            FadeIn(outcome_icon, scale=0.9),
            run_time=1.0,
        )
        self.wait(9.2)

        # Beat 2:
        # 스크립트의 "근본적인 문제"와 "잠재적 결과 도입"을 한 흐름으로 처리한다.
        # 두 세계를 충분히 오래 유지해, 문제 제기와 Y_{1i}/Y_{0i} 설명을 모두 받는다.
        self.play(
            FadeOut(VGroup(outcome_def, outcome_icon), shift=UP * 0.1),
            FadeIn(worlds, shift=UP * 0.12),
            run_time=1.1,
        )
        self.wait(24.8)

        # Beat 3:
        # 스크립트의 "실제로 관찰할 수 있는 것은 둘 중 하나뿐"을 처리한다.
        # factual / counterfactual 대비와 더 정리된 하단 문구로 관찰 불가능성을 정리한다.
        self.play(
            left_world.animate.move_to(factual_world_pos),
            right_world.animate.move_to(counter_world_pos),
            FadeIn(left_label, shift=UP * 0.1),
            FadeIn(right_label, shift=UP * 0.1),
            run_time=1.1,
        )
        counter_shade.move_to(right_world)
        self.play(
            counter_shade.animate.set_fill(opacity=0.5),
            FadeIn(unseen, scale=0.9),
            FadeIn(impossible, shift=UP * 0.08),
            Create(impossible_line),
            run_time=1.0,
        )
        self.wait(self.WAIT_TAIL)
