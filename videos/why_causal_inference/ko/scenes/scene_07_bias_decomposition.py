from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_icon,
    load_scene_timing_durations,
)


class Scene07_BiasDecomposition(Scene):
    """
    Scene 07: 편향 분해

    Core Claim:
    관찰 평균 차이는 처치 효과 하나만이 아니라, 원래 집단 차이에서 오는 편향까지 함께 섞인 값이다.

    Expected Misconception:
    단순 평균 차이가 틀리는 이유를 "표본이 작아서" 정도로만 이해하고,
    구조적으로 어떤 항이 섞였는지는 놓치기 쉽다.

    Visual Pivot:
    관찰 평균 차이 식이 `ATT + Bias` 분해식으로 다시 쓰이고,
    마지막에는 학교 여건이 처치와 결과 양쪽으로 향하는 교란 구조로 수렴한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "즉, 관찰된 연관성을 인과효과로 곧장 읽으면 틀릴 수 있습니다. 그렇다면 왜 이런 차이가 생기는 걸까요?"
    - 현재 Scene 첫 문장:
      "핵심은 단순 평균 차이에 편향(Bias) 이 섞여 있기 때문입니다."
    - Cell 14:
      태블릿 예시의 직관 설명, `E[Y|T=1]-E[Y|T=0]` 분해, 편향과 교란변수 설명

    Previous Scene Continuity:
    - 직전 Scene 코드:
      `Scene06_ObservedMeanDifferenceTrap`
    - 이어받는 시각 요소:
      태블릿 학교 vs 비교 학교 구도, 관찰 평균 차이 문제 제기
    - 바뀌는 점:
      숫자 계산 장면에서 벗어나, 왜 그런 차이가 생기는지 식과 구조로 해부한다.

    Script Reference:
    narration/07_bias_decomposition.txt

    Asset Reference:
    Tabler Icons (MIT)
    - device-tablet.svg
    - device-tablet-off.svg
    - coin.svg
    - map-pin.svg
    - users-group.svg
    - school.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py
    Reason:
    하나의 식을 점진적으로 재배열해 의미를 분리하고, 마지막에 원인 구조로 묶는 리듬을 참고했다.

    Script-to-Beat Mapping:
    1. 단순 평균 차이에 편향이 섞인다는 핵심 주장 제시
    2. 태블릿 학교가 원래 더 좋은 조건이었을 수 있다는 직관 예시
    3. `E[Y_0|T=1] > E[Y_0|T=0]`로 잠재적 결과 해석
    4. 관찰 연관성 식 제시
    5. `ATT + Bias` 분해식으로 재정리
    6. ATT와 Bias의 의미를 각각 읽게 함
    7. 교란변수 구조와 편향 제거 필요성으로 마무리

    Timing-to-Beat Mapping:
    - chunk 1 -> Beat 1
    - chunk 2 -> Beat 2
    - chunk 3 -> Beat 3
    - chunk 4-5 -> Beat 4-5
    - chunk 6-7 -> Beat 6
    - chunk 8-11 -> Beat 7
    """

    WAIT_TAIL = 1.5  # mp3(92.87s) > video(92.38s) → 0.49s 부족, 1.5s로 늘려 나레이션 끊김 해소

    def construct(self):
        chunk_durations = load_scene_timing_durations("07_bias_decomposition", language="ko")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        bias_word = Text("단순 평균 차이는 왜 인과효과가 아닐까?", font_size=34, color=QUESTION_COLOR, weight=BOLD)
        bias_word.move_to(ORIGIN + UP * 0.7)

        avg_diff_box = RoundedRectangle(
            width=4.3,
            height=0.8,
            corner_radius=0.2,
            stroke_color=WHITE,
            stroke_width=1.8,
        )
        avg_diff_label = Text("관찰된 평균 차이", font_size=26, color=WHITE, weight=BOLD).move_to(avg_diff_box)
        avg_diff_group = VGroup(avg_diff_box, avg_diff_label)
        avg_diff_group.move_to(ORIGIN + DOWN * 0.15)

        effect_box = RoundedRectangle(
            width=1.85,
            height=0.72,
            corner_radius=0.18,
            stroke_color=ACCENT_COLOR,
            stroke_width=1.8,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.12,
        )
        effect_label = Text("effect", font_size=22, color=ACCENT_COLOR, weight=BOLD).move_to(effect_box)
        effect_group = VGroup(effect_box, effect_label)

        plus = MathTex(r"+").scale(0.9).set_color(WHITE)

        bias_box = RoundedRectangle(
            width=1.55,
            height=0.72,
            corner_radius=0.18,
            stroke_color=QUESTION_COLOR,
            stroke_width=1.8,
            fill_color=QUESTION_COLOR,
            fill_opacity=0.12,
        )
        bias_label = Text("bias", font_size=22, color=QUESTION_COLOR, weight=BOLD).move_to(bias_box)
        bias_group = VGroup(bias_box, bias_label)

        split_group = VGroup(effect_group, plus, bias_group).arrange(RIGHT, buff=0.24)
        split_group.move_to(avg_diff_group)

        treated_card = RoundedRectangle(width=3.55, height=3.0, corner_radius=0.18, stroke_color=TABLET_COLOR, stroke_width=2.6)
        control_card = RoundedRectangle(width=3.55, height=3.0, corner_radius=0.18, stroke_color=LIBRARY_COLOR, stroke_width=2.6)
        treated_card.move_to(LEFT * 2.7 + DOWN * 0.05)
        control_card.move_to(RIGHT * 2.7 + DOWN * 0.05)

        treated_group = VGroup(
            MathTex(r"T=1").set_color(TABLET_COLOR).scale(0.82),
            Text("태블릿 지급", font_size=24, color=TABLET_COLOR, weight=BOLD),
            VGroup(
                load_icon("school.svg", WHITE, 0.64),
                load_icon("arrow-up.svg", TABLET_COLOR, 0.56),
            ).arrange(RIGHT, buff=0.18),
            Text("원래 성적이 높았을 수 있음", font_size=20, color=WHITE, weight=BOLD),
        ).arrange(DOWN, buff=0.18).move_to(treated_card)
        control_group = VGroup(
            MathTex(r"T=0").set_color(LIBRARY_COLOR).scale(0.82),
            Text("태블릿 미지급", font_size=24, color=LIBRARY_COLOR, weight=BOLD),
            VGroup(
                load_icon("school.svg", WHITE, 0.64),
                load_icon("arrow-down.svg", LIBRARY_COLOR, 0.56),
            ).arrange(RIGHT, buff=0.18),
            Text("원래 성적이 낮았을 수 있음", font_size=20, color=WHITE, weight=BOLD),
        ).arrange(DOWN, buff=0.18).move_to(control_card)

        inequality = MathTex(r"E[Y_0\mid T=1]", r">", r"E[Y_0\mid T=0]").scale(1.0)
        inequality[0].set_color(TABLET_COLOR)
        inequality[1].set_color(ACCENT_COLOR)
        inequality[2].set_color(LIBRARY_COLOR)
        inequality.to_edge(DOWN, buff=0.7)

        observed_formula = MathTex(
            r"E[Y\mid T=1] - E[Y\mid T=0]",
            r"=",
            r"E[Y_1\mid T=1] - E[Y_0\mid T=0]",
        ).scale(0.9)
        observed_formula.move_to(ORIGIN)

        decomp_summary = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
            r"+",
            r"Bias",
        ).scale(1.0)
        decomp_summary[2].set_color(ACCENT_COLOR)
        decomp_summary[4].set_color(QUESTION_COLOR)
        decomp_summary.move_to(ORIGIN + UP * 0.5)

        att_detail = MathTex(r"ATT = E[Y_1-Y_0\mid T=1]").scale(0.84).set_color(ACCENT_COLOR)
        bias_detail = MathTex(r"Bias = E[Y_0\mid T=1]-E[Y_0\mid T=0]").scale(0.84).set_color(QUESTION_COLOR)
        att_detail.next_to(decomp_summary, DOWN, buff=0.5)
        bias_detail.next_to(att_detail, DOWN, buff=0.28)

        att_focus = SurroundingRectangle(att_detail, color=ACCENT_COLOR, buff=0.16, corner_radius=0.1)
        bias_focus = SurroundingRectangle(bias_detail, color=QUESTION_COLOR, buff=0.16, corner_radius=0.1)
        att_note = Text("실제 인과효과", font_size=24, color=ACCENT_COLOR, weight=BOLD).next_to(att_focus, RIGHT, buff=0.28)
        bias_note = Text("원래 집단 차이", font_size=24, color=QUESTION_COLOR, weight=BOLD).next_to(bias_focus, RIGHT, buff=0.28)

        confounder_box = RoundedRectangle(width=4.4, height=1.7, corner_radius=0.18, stroke_color=NEUTRAL_COLOR, stroke_width=2.2).move_to(UP * 1.45)
        confounder_label = Text("학교 여건", font_size=28, color=WHITE, weight=BOLD)
        confounder_label.move_to(confounder_box.get_top() + DOWN * 0.36)
        budget_chip = VGroup(
            load_icon("coin.svg", GOLD_E, 0.3),
            Text("재정", font_size=20, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        location_chip = VGroup(
            load_icon("map-pin.svg", BLUE_E, 0.3),
            Text("위치", font_size=20, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        teacher_chip = VGroup(
            load_icon("user-star.svg", GREEN_E, 0.3),
            Text("교사의 질", font_size=20, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        confounder_factors = VGroup(budget_chip, location_chip, teacher_chip).arrange(RIGHT, buff=0.28)
        confounder_factors.move_to(confounder_box.get_center() + DOWN * 0.22)
        t_node = VGroup(Circle(radius=0.56, stroke_color=TABLET_COLOR, stroke_width=2.6), MathTex(r"T").set_color(TABLET_COLOR)).move_to(LEFT * 2.6 + DOWN * 0.35)
        y_node = VGroup(Circle(radius=0.56, stroke_color=ACCENT_COLOR, stroke_width=2.6), MathTex(r"Y").set_color(ACCENT_COLOR)).move_to(RIGHT * 2.6 + DOWN * 0.35)
        t_label = Text("처치", font_size=23, color=TABLET_COLOR, weight=BOLD).next_to(t_node, DOWN, buff=0.18)
        y_label = Text("결과", font_size=23, color=ACCENT_COLOR, weight=BOLD).next_to(y_node, DOWN, buff=0.18)
        c_to_t = Arrow(confounder_box.get_bottom() + LEFT * 0.42, t_node.get_top(), buff=0.12, color=NEUTRAL_COLOR, stroke_width=3.0)
        c_to_y = Arrow(confounder_box.get_bottom() + RIGHT * 0.42, y_node.get_top(), buff=0.12, color=NEUTRAL_COLOR, stroke_width=3.0)
        t_to_y = Arrow(t_node.get_right(), y_node.get_left(), buff=0.18, color=TABLET_COLOR, stroke_width=3.2)
        compare_axis = Line(LEFT * 1.7, RIGHT * 1.7, color=NEUTRAL_COLOR, stroke_width=2.2)
        compare_axis.to_edge(DOWN, buff=0.58)

        treated_bar = RoundedRectangle(
            width=0.56,
            height=1.18,
            corner_radius=0.1,
            stroke_color=TABLET_COLOR,
            stroke_width=2.4,
            fill_color=TABLET_COLOR,
            fill_opacity=0.15,
        )
        treated_bar.align_to(compare_axis, DOWN).shift(LEFT * 1.0)

        control_bar = RoundedRectangle(
            width=0.56,
            height=0.7,
            corner_radius=0.1,
            stroke_color=LIBRARY_COLOR,
            stroke_width=2.4,
            fill_color=LIBRARY_COLOR,
            fill_opacity=0.15,
        )
        control_bar.align_to(compare_axis, DOWN).shift(RIGHT * 1.0)

        treated_mark = MathTex(r"T=1").scale(0.68).set_color(TABLET_COLOR).next_to(treated_bar, DOWN, buff=0.12)
        control_mark = MathTex(r"T=0").scale(0.68).set_color(LIBRARY_COLOR).next_to(control_bar, DOWN, buff=0.12)
        compare_icon = load_icon("git-compare.svg", WHITE, 0.46).move_to(compare_axis.get_center() + UP * 0.48)
        compare_group = VGroup(compare_axis, treated_bar, control_bar, treated_mark, control_mark, compare_icon)

        balanced_axis = compare_axis.copy()
        balanced_treated_bar = RoundedRectangle(
            width=0.56,
            height=0.94,
            corner_radius=0.1,
            stroke_color=TABLET_COLOR,
            stroke_width=2.4,
            fill_color=TABLET_COLOR,
            fill_opacity=0.15,
        )
        balanced_treated_bar.align_to(balanced_axis, DOWN).shift(LEFT * 1.0)
        balanced_control_bar = RoundedRectangle(
            width=0.56,
            height=0.94,
            corner_radius=0.1,
            stroke_color=LIBRARY_COLOR,
            stroke_width=2.4,
            fill_color=LIBRARY_COLOR,
            fill_opacity=0.15,
        )
        balanced_control_bar.align_to(balanced_axis, DOWN).shift(RIGHT * 1.0)
        balanced_treated_mark = treated_mark.copy().next_to(balanced_treated_bar, DOWN, buff=0.12)
        balanced_control_mark = control_mark.copy().next_to(balanced_control_bar, DOWN, buff=0.12)
        equal_icon = load_icon("equal.svg", ACCENT_COLOR, 0.48).move_to(compare_icon)
        check_icon = load_icon("check.svg", ACCENT_COLOR, 0.38).next_to(equal_icon, UP, buff=0.08)
        balanced_icon = VGroup(equal_icon, check_icon)
        balanced_group = VGroup(
            balanced_axis,
            balanced_treated_bar,
            balanced_control_bar,
            balanced_treated_mark,
            balanced_control_mark,
            balanced_icon,
        )
        balanced_group.move_to(compare_group)

        confounder_cross = Cross(confounder_box, stroke_color=QUESTION_COLOR, stroke_width=5.5)
        confounder_cross.scale(1.05)

        # Beat 1:
        # 남는 요소: 없음.
        # 새로 등장하는 요소: bias_word, 평균 차이 배지.
        # 비워 두는 영역: 하단 카드 영역 전체.
        # 질문을 먼저 던지고, 바로 아래 배지가 effect + bias로 갈라지는 흐름으로 편향을 예고한다.
        self.play(FadeIn(bias_word, scale=0.9), run_time=0.8)
        self.play(FadeIn(avg_diff_group, shift=UP * 0.06), run_time=0.7)
        self.play(
            Transform(avg_diff_group, split_group),
            run_time=0.9,
        )
        wait_for_chunks([1], spent=2.4)

        # Beat 2:
        # 남는 요소: 없음.
        # 새로 등장하는 요소: 두 집단 카드.
        # 비워 두는 영역: 하단 수식 영역.
        # 직관 예시는 카드 2개만 남긴다. 긴 인용문 박스는 쓰지 않고 Y0 차이만 카드 내부에 둔다.
        self.play(FadeOut(bias_word, scale=0.95), FadeOut(avg_diff_group), run_time=0.3)
        self.play(
            FadeIn(treated_card, scale=0.96),
            FadeIn(control_card, scale=0.96),
            FadeIn(treated_group, shift=UP * 0.06),
            FadeIn(control_group, shift=UP * 0.06),
            run_time=0.95,
        )
        wait_for_chunks([2], spent=1.2)

        # Beat 3:
        # 남는 요소: title, 두 카드.
        # 새로 등장하는 요소: inequality.
        # 비워 두는 영역: 화면 상단 제목 외 대부분은 카드 2개와 하단 수식으로만 사용.
        # 카드의 Y0 차이를 잠재적 결과 부등식으로 압축한다.
        self.play(FadeIn(inequality, shift=UP * 0.08), run_time=0.65)
        self.play(
            Indicate(treated_group[-1], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(control_group[-1], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        wait_for_chunks([3], spent=1.25)

        # Beat 4:
        # 남는 요소: 없음.
        # 새로 등장하는 요소: observed_formula.
        # 비워 두는 영역: 좌우 카드 영역을 비워 수식 하나만 읽히게 한다.
        # 카드 장면을 완전히 정리한 뒤 관찰 데이터 식만 단독으로 올린다.
        self.play(
            FadeOut(treated_card),
            FadeOut(control_card),
            FadeOut(treated_group),
            FadeOut(control_group),
            FadeOut(inequality),
            FadeIn(observed_formula, shift=UP * 0.08),
            run_time=0.85,
        )
        self.play(Indicate(observed_formula[2], color=WHITE, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([4], spent=1.35)

        # Beat 5:
        # 남는 요소: decomp_summary, detail 식.
        # 새로 등장하는 요소: att/bias highlight와 짧은 note.
        # 비워 두는 영역: 좌우 측면.
        # 분해식만 화면 중앙에 두고 ATT와 Bias를 번갈아 읽게 한다.
        self.play(TransformMatchingTex(observed_formula, decomp_summary), run_time=0.95)
        self.play(FadeIn(att_detail, shift=UP * 0.06), FadeIn(bias_detail, shift=UP * 0.06), run_time=0.5)
        wait_for_chunks([5], spent=0.95)
        self.play(FadeIn(att_focus), FadeIn(att_note, shift=UP * 0.06), run_time=0.45)
        self.play(Indicate(att_focus, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.5)
        # chunk 6 앞부분의 "하나는 ... ATT" 설명이 먼저 충분히 지나가도록 잠시 유지한다.
        self.wait(3.4)
        self.play(
            FadeOut(att_focus),
            FadeOut(att_note),
            FadeIn(bias_focus),
            FadeIn(bias_note, shift=UP * 0.06),
            run_time=0.45,
        )
        self.play(Indicate(bias_focus, color=QUESTION_COLOR, scale_factor=1.02), run_time=0.5)
        wait_for_chunks([6, 7], spent=5.3)

        # Beat 6:
        # 남는 요소: confounder DAG, 하단 비교 패널.
        # 새로 등장하는 요소: 교란 세부 요인, 교란 경로 차단 표시, 정렬된 비교 패널.
        # 비워 두는 영역: 상단 수식 영역까지 모두 비워 DAG와 작은 하단 패널만 읽히게 한다.
        # 후반부는 "교란이 있으면 출발선이 다르고, 경로를 끊으면 비교 가능해진다"를 도형 변화로만 마무리한다.
        self.play(
            FadeOut(bias_focus),
            FadeOut(bias_note),
            FadeOut(decomp_summary),
            FadeOut(att_detail),
            FadeOut(bias_detail),
            run_time=0.75,
        )
        self.play(
            FadeIn(confounder_box, shift=DOWN * 0.08),
            FadeIn(confounder_label, shift=DOWN * 0.08),
            FadeIn(t_node, scale=0.92),
            FadeIn(y_node, scale=0.92),
            FadeIn(t_label, shift=UP * 0.06),
            FadeIn(y_label, shift=UP * 0.06),
            run_time=0.9,
        )
        self.play(Create(c_to_t), Create(c_to_y), GrowArrow(t_to_y), run_time=0.85)
        self.play(FadeIn(compare_group, shift=UP * 0.06), run_time=0.55)
        self.play(
            Indicate(confounder_box, color=QUESTION_COLOR, scale_factor=1.03),
            Indicate(compare_icon, color=WHITE, scale_factor=1.05),
            run_time=0.55,
        )
        self.wait(4.9)
        self.play(FadeIn(budget_chip, shift=UP * 0.05), run_time=0.35)
        self.play(FadeIn(location_chip, shift=UP * 0.05), run_time=0.35)
        self.play(FadeIn(teacher_chip, shift=UP * 0.05), run_time=0.45)
        wait_for_chunks([8, 9], spent=9.65)
        self.play(
            Create(confounder_cross),
            c_to_t.animate.set_stroke(opacity=0.22),
            c_to_y.animate.set_stroke(opacity=0.22),
            confounder_box.animate.set_stroke(opacity=0.32),
            confounder_label.animate.set_opacity(0.32),
            confounder_factors.animate.set_opacity(0.32),
            run_time=0.7,
        )
        self.wait(4.2)
        self.play(Transform(compare_group, balanced_group), run_time=0.8)
        self.play(Indicate(compare_group[5], color=ACCENT_COLOR, scale_factor=1.08), run_time=0.45)
        wait_for_chunks([10, 11], spent=6.95)
        self.wait(self.WAIT_TAIL)
