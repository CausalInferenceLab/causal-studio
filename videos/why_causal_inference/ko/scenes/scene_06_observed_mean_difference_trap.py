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


class Scene06_ObservedMeanDifferenceTrap(Scene):
    """
    Scene 06: 관찰된 평균 차이의 함정

    Core Claim:
    현실에서는 관찰된 집단 평균 차이를 곧바로 인과효과로 읽을 수 없고,
    같은 데이터에서도 관찰 차이와 진짜 ATE의 부호가 뒤집힐 수 있다.

    Expected Misconception:
    처치 집단 평균과 비교 집단 평균만 계산하면
    평균 효과를 충분히 근사할 수 있다고 오해하기 쉽다.

    Visual Pivot:
    Scene 05의 full table이 ipynb Cell 11의 observed table로 직접 바뀌고,
    그 표에서 계산한 `125`가 직전 Scene의 `ATE=-50`과 정면 충돌한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "ATE, ATT 모두 사실과 반사실이라는 두 세계를 모두 볼 수 있었기 때문에 계산할 수 있었던 것입니다."
    - 현재 Scene 첫 문장:
      "이제 현실로 돌아와 보겠습니다."
    - Cell 8:
      full table 데이터
    - Cell 11:
      observed table 데이터 (`y0`, `y1`, `te`에 `np.nan` 포함)
    - Cell 12:
      관찰 평균 차이 125와 진짜 `ATE=-50` 비교

    Notebook Code/Data Reference:
    - Cell 8 code:
      `pd.DataFrame(dict(i=[1,2,3,4], y0=[500,600,800,700], y1=[450,600,600,750], t=[0,0,1,1], y=[500,600,600,750], ite=[-50,0,-200,50]))`
    - Cell 11 code:
      `pd.DataFrame(dict(i=[1,2,3,4], y0=[500,600,np.nan,np.nan], y1=[np.nan,np.nan,600,750], t=[0,0,1,1], y=[500,600,600,750], te=[np.nan,np.nan,np.nan,np.nan]))`

    Previous Scene Continuity:
    - 직전 Scene 코드:
      `Scene05_MultiverseTableAteAtt`
    - 이어받는 시각 요소:
      같은 4개 학교 표, 같은 `Y_0 / Y_1 / T / Y` 열 의미, 같은 색 체계
    - 바뀌는 점:
      full-data table에서 관찰 가능한 셀만 남기고 counterfactual/ITE를 지운다.

    Script Reference:
    narration/06_observed_mean_difference_trap.txt

    Asset Reference:
    Tabler Icons (MIT)
    - school.svg
    - eye-off.svg
    - device-tablet.svg
    - device-tablet-off.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py
    Reason:
    같은 데이터 구조를 유지한 채 관찰 가능한 정보만 남겨 의미를 뒤집는 비교 연출이 필요해서 참고했다.

    Script-to-Beat Mapping:
    1. Scene 05의 table grammar를 이어받아, 현실에서는 counterfactual과 ITE가 비어 버린다고 정리
    2. 그래도 `E[Y|T=1]-E[Y|T=0]`를 써보고 싶어지는 유혹을 질문으로 제시
    3. observed table의 `Y` 열만 이용해 treated 평균 675, control 평균 550을 계산
    4. 관찰 차이 125가 양의 효과처럼 보인다고 강조
    5. 직전 Scene에서 계산한 진짜 `ATE=-50`과 비교해 부호가 뒤집힌다고 보여줌
    6. 관찰 연관성을 인과효과로 읽으면 틀릴 수 있다는 질문으로 다음 Scene에 넘김

    Timing-to-Beat Mapping:
    - chunk 1 -> Beat 1
    - chunk 2 -> Beat 2
    - chunk 3 -> Beat 3
    - chunk 4 -> Beat 4
    - chunk 5 -> Beat 5
    - chunk 6 -> Beat 6
    """

    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("06_observed_mean_difference_trap", language="ko")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        def make_table_cell(content: Mobject, width: float, height: float, stroke_color=GREY_B) -> VGroup:
            box = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.08,
                stroke_color=stroke_color,
                stroke_width=1.8,
                fill_opacity=0.0,
            )
            content.move_to(box.get_center())
            return VGroup(box, content)

        headers = [
            (MathTex(r"i"), 0.54, 0.56, GREY_B),
            (MathTex(r"Y_0").set_color(LIBRARY_COLOR), 1.0, 0.56, LIBRARY_COLOR),
            (MathTex(r"Y_1").set_color(TABLET_COLOR), 1.0, 0.56, TABLET_COLOR),
            (MathTex(r"T").set_color(TABLET_COLOR), 0.66, 0.56, TABLET_COLOR),
            (MathTex(r"Y").set_color(WHITE), 0.9, 0.56, GREY_B),
            (MathTex(r"ITE").set_color(ACCENT_COLOR), 0.96, 0.56, ACCENT_COLOR),
        ]
        full_rows = [
            ["1", "500", "450", "0", "500", "-50"],
            ["2", "600", "600", "0", "600", "0"],
            ["3", "800", "600", "1", "600", "-200"],
            ["4", "700", "750", "1", "750", "50"],
        ]
        observed_rows = [
            ["1", "500", None, "0", "500", None],
            ["2", "600", None, "0", "600", None],
            ["3", None, "600", "1", "600", None],
            ["4", None, "750", "1", "750", None],
        ]
        col_widths = [0.54, 1.0, 1.0, 0.66, 0.9, 0.96]

        header_cells = VGroup(
            *[make_table_cell(label.scale(0.72), width, height, color) for label, width, height, color in headers]
        ).arrange(RIGHT, buff=0.08)

        body_rows = VGroup()
        for row in full_rows:
            row_cells = []
            for idx, value in enumerate(row):
                color = WHITE
                if idx == 1:
                    color = LIBRARY_COLOR
                elif idx == 2 or idx == 3:
                    color = TABLET_COLOR
                elif idx == 5:
                    color = ACCENT_COLOR
                cell = make_table_cell(
                    MathTex(value).scale(0.72).set_color(color),
                    col_widths[idx],
                    0.62,
                    GREY_B,
                )
                row_cells.append(cell)
            body_rows.add(VGroup(*row_cells).arrange(RIGHT, buff=0.08))
        body_rows.arrange(DOWN, buff=0.08)

        table_group = VGroup(header_cells, body_rows).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        table_group.scale(0.92)
        table_group.move_to(UP * 0.18)

        y0_boxes = VGroup(*[row[1][0] for row in body_rows])
        y1_boxes = VGroup(*[row[2][0] for row in body_rows])
        t_boxes = VGroup(*[row[3][0] for row in body_rows])
        y_boxes = VGroup(*[row[4][0] for row in body_rows])
        te_boxes = VGroup(*[row[5][0] for row in body_rows])

        hidden_y1 = VGroup(body_rows[0][2], body_rows[1][2])
        hidden_y0 = VGroup(body_rows[2][1], body_rows[3][1])
        all_ite_cells = VGroup(*[row[5] for row in body_rows])

        for row_idx, row in enumerate(observed_rows):
            for col_idx, value in enumerate(row):
                if value is None:
                    box = body_rows[row_idx][col_idx][0]
                    if col_idx == 5:
                        eye = load_icon("eye-off.svg", ACCENT_COLOR, 0.48)
                    elif col_idx == 1:
                        eye = load_icon("eye-off.svg", LIBRARY_COLOR, 0.48)
                    else:
                        eye = load_icon("eye-off.svg", TABLET_COLOR, 0.48)
                    body_rows[row_idx][col_idx][1].become(eye.move_to(box.get_center()))

        control_rows = VGroup(body_rows[0], body_rows[1])
        treated_rows = VGroup(body_rows[2], body_rows[3])
        control_y_boxes = VGroup(body_rows[0][4][0], body_rows[1][4][0])
        treated_y_boxes = VGroup(body_rows[2][4][0], body_rows[3][4][0])

        reality_label = Text("현실에서는 관찰된 결과만 남습니다", font_size=25, color=ACCENT_COLOR, weight=BOLD)
        reality_label.next_to(table_group, UP, buff=0.34)
        table_block = VGroup(table_group, reality_label)

        direct_calc_formula = MathTex(r"ITE_i,\ ATE,\ ATT").scale(0.92).set_color(ACCENT_COLOR)
        direct_calc_cross = Cross(direct_calc_formula, stroke_color=MAROON_E, stroke_width=7)
        direct_calc_block = VGroup(direct_calc_formula, direct_calc_cross)
        direct_calc_block.next_to(table_group, DOWN, buff=0.34)

        temptation = VGroup(
            Text("그냥 두 집단 평균을", font_size=26, color=NEUTRAL_COLOR, weight=BOLD),
            Text("비교하면 안 될까?", font_size=30, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.18)
        temptation.scale(0.9)
        temptation.move_to(RIGHT * 3.95 + DOWN * 0.05)

        treated_mean_card = RoundedRectangle(width=3.45, height=1.6, corner_radius=0.16, stroke_color=TABLET_COLOR, stroke_width=2.4)
        control_mean_card = RoundedRectangle(width=3.45, height=1.6, corner_radius=0.16, stroke_color=LIBRARY_COLOR, stroke_width=2.4)
        treated_mean_card.move_to(RIGHT * 4.2 + UP * 0.95)
        control_mean_card.move_to(RIGHT * 4.2 + DOWN * 0.95)

        treated_mean = VGroup(
            Text("treated mean", font_size=20, color=TABLET_COLOR, weight=BOLD),
            MathTex(r"(600 + 750)/2 = 675").scale(0.68).set_color(WHITE),
        ).arrange(DOWN, buff=0.12).move_to(treated_mean_card)
        control_mean = VGroup(
            Text("control mean", font_size=20, color=LIBRARY_COLOR, weight=BOLD),
            MathTex(r"(500 + 600)/2 = 550").scale(0.68).set_color(WHITE),
        ).arrange(DOWN, buff=0.12).move_to(control_mean_card)

        observed_formula = MathTex(
            r"E[Y\mid T=1] - E[Y\mid T=0]",
            r"=",
            r"675 - 550",
            r"=",
            r"125",
        ).scale(0.84)
        observed_formula[0].set_color(WHITE)
        observed_formula[2].set_color(WHITE)
        observed_formula[4].set_color(TABLET_COLOR)
        observed_formula.move_to(ORIGIN + DOWN * 0.15)

        observed_positive = MathTex(r"+125").scale(1.5).set_color(TABLET_COLOR)
        observed_positive.move_to(ORIGIN + DOWN * 0.05)
        observed_positive_label = Text("관찰 평균 차이", font_size=22, color=TABLET_COLOR, weight=BOLD)
        observed_positive_label.next_to(observed_positive, UP, buff=0.28)

        true_ate = MathTex(r"-50").scale(1.5).set_color(MAROON_E)
        true_ate.move_to(ORIGIN + DOWN * 0.05)
        true_ate_label = Text("진짜 ATE", font_size=22, color=ACCENT_COLOR, weight=BOLD)
        true_ate_label.next_to(true_ate, UP, buff=0.28)

        sign_flip = MathTex(r"+125", r"\ne", r"-50").scale(1.05)
        sign_flip[0].set_color(TABLET_COLOR)
        sign_flip[1].set_color(MAROON_E)
        sign_flip[2].set_color(MAROON_E)
        sign_flip.next_to(true_ate, DOWN, buff=0.42)

        # Beat 6 준비:
        # 마지막 장면은 표의 기억을 남기기 위해 작은 표 실루엣은 지우고, 결론 문장과 다음 질문만 남긴다.
        closing = VGroup(
            Text("observed association", font_size=32, color=WHITE, weight=BOLD),
            MathTex(r"\ne").scale(1.2).set_color(ACCENT_COLOR),
            Text("causal effect", font_size=34, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.24)
        closing.move_to(UP * 0.55)
        why_next = Text("왜 이런 차이가 생길까?", font_size=28, color=QUESTION_COLOR, weight=BOLD)
        why_next.next_to(closing, DOWN, buff=0.34)

        # Beat 1:
        # Scene 05의 표 문법을 그대로 이어받아 full table을 먼저 보여준 뒤,
        # Cell 11 데이터대로 counterfactual과 ITE를 비워 현실 표로 바꾼다.
        self.play(FadeIn(reality_label, shift=UP * 0.08), FadeIn(table_group, shift=UP * 0.08), run_time=0.9)
        self.play(
            *[box.animate.set_fill(LIBRARY_COLOR, opacity=0.12).set_stroke(LIBRARY_COLOR, width=2.4) for box in VGroup(body_rows[0][1][0], body_rows[1][1][0])],
            *[box.animate.set_fill(TABLET_COLOR, opacity=0.12).set_stroke(TABLET_COLOR, width=2.4) for box in VGroup(body_rows[2][2][0], body_rows[3][2][0])],
            *[box.animate.set_fill(WHITE, opacity=0.08).set_stroke(WHITE, width=2.2) for box in y_boxes],
            run_time=0.7,
        )
        self.play(
            *[box.animate.set_fill(BLACK, opacity=0.38).set_stroke(TABLET_COLOR, width=2.2) for box in VGroup(hidden_y1[0][0], hidden_y1[1][0])],
            *[box.animate.set_fill(BLACK, opacity=0.38).set_stroke(LIBRARY_COLOR, width=2.2) for box in VGroup(hidden_y0[0][0], hidden_y0[1][0])],
            *[box.animate.set_fill(BLACK, opacity=0.42).set_stroke(ACCENT_COLOR, width=2.2) for box in VGroup(*[cell[0] for cell in all_ite_cells])],
            run_time=0.8,
        )
        # 앞 두 문장 동안은 표만 남겨 두고,
        # "그래서 개별 처치 효과인 ITE..."가 시작될 때 eye-off와 식을 함께 띄운다.
        self.wait(5.2)
        self.play(
            FadeIn(VGroup(*[cell[1] for cell in hidden_y1]), scale=0.9),
            FadeIn(VGroup(*[cell[1] for cell in hidden_y0]), scale=0.9),
            FadeIn(VGroup(*[cell[1] for cell in all_ite_cells]), scale=0.9),
            FadeIn(direct_calc_formula, shift=UP * 0.08),
            run_time=0.35,
        )
        # 식이 읽히기 시작한 직후, "직접 계산할 수 없고"에 맞춰 X를 올린다.
        self.wait(0.55)
        self.play(Create(direct_calc_cross), run_time=0.45)
        wait_for_chunks([1], spent=9.1)

        # Beat 2:
        # 직접 계산은 막혔지만, 평균 차이를 써보고 싶은 유혹이 자연스럽게 이어진다.
        # 초반 설명에만 필요했던 reality label은 여기서 바로 걷어내고,
        # 표만 좌측으로 밀어 다음 Beat 계산 공간을 연다.
        self.play(
            FadeOut(direct_calc_block, shift=DOWN * 0.08),
            FadeOut(reality_label, shift=UP * 0.08),
            table_group.animate.shift(LEFT * 1.45),
            FadeIn(temptation, shift=UP * 0.08),
            run_time=0.85,
        )
        wait_for_chunks([2], spent=0.85)

        # Beat 3:
        # Cell 12의 계산처럼 관찰 가능한 Y 열만 사용해 treated/control 평균을 계산한다.
        # 여기서는 표를 더 이상 이동시키지 않고, 열린 공간에서 바로 평균 계산으로 들어간다.
        self.play(
            FadeOut(temptation, shift=UP * 0.08),
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in y0_boxes],
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in y1_boxes],
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in te_boxes],
            *[box.animate.set_stroke(TABLET_COLOR, width=2.5) for box in t_boxes],
            *[box.animate.set_stroke(WHITE, width=2.5) for box in y_boxes],
            run_time=0.7,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=WHITE, scale_factor=1.025) for box in y_boxes],
                lag_ratio=0.08,
            ),
            run_time=0.7,
        )
        self.play(
            *[box.animate.set_fill(LIBRARY_COLOR, opacity=0.12).set_stroke(LIBRARY_COLOR, width=2.6) for box in control_y_boxes],
            FadeIn(control_mean_card),
            FadeIn(control_mean, shift=RIGHT * 0.08),
            run_time=0.75,
        )
        self.play(
            *[box.animate.set_fill(TABLET_COLOR, opacity=0.12).set_stroke(TABLET_COLOR, width=2.6) for box in treated_y_boxes],
            FadeIn(treated_mean_card),
            FadeIn(treated_mean, shift=RIGHT * 0.08),
            run_time=0.75,
        )
        wait_for_chunks([3], spent=3.6)

        # Beat 4:
        # 관찰 평균 차이만 먼저 읽히게 한다.
        # 여기서는 표를 배경으로 남기지 않고, Scene 5처럼 한 번 비워서 숫자만 보이게 만든다.
        self.play(
            FadeOut(treated_mean_card),
            FadeOut(treated_mean),
            FadeOut(control_mean_card),
            FadeOut(control_mean),
            FadeOut(table_group, shift=LEFT * 0.18),
            FadeIn(observed_positive_label, shift=UP * 0.08),
            FadeIn(observed_formula, shift=UP * 0.08),
            run_time=0.7,
        )
        self.play(Indicate(observed_formula[-1], color=TABLET_COLOR, scale_factor=1.08), run_time=0.5)
        self.play(TransformMatchingTex(observed_formula, observed_positive), run_time=0.6)
        wait_for_chunks([4], spent=1.45)

        # Beat 5:
        # 여기서 처음으로 진짜 ATE를 꺼내 관찰 차이 해석을 뒤집는다.
        self.play(
            FadeOut(observed_positive_label),
            FadeIn(true_ate_label, shift=UP * 0.08),
            TransformMatchingTex(observed_positive, true_ate),
            run_time=0.6,
        )
        self.play(
            FadeIn(sign_flip, shift=UP * 0.08),
            run_time=0.55,
        )
        wait_for_chunks([5], spent=1.15)

        # Beat 6:
        # 마지막에는 표와 계산 카드를 지우고, 관찰 연관성과 인과효과를 구분해야 한다는 문장으로 다음 질문을 남긴다.
        self.play(
            FadeOut(true_ate_label),
            FadeOut(true_ate),
            FadeOut(sign_flip),
            run_time=0.75,
        )
        self.play(FadeIn(closing, shift=UP * 0.08), run_time=0.6)
        self.play(FadeIn(why_next, shift=UP * 0.08), run_time=0.5)
        wait_for_chunks([6], spent=1.35)
        self.wait(self.WAIT_TAIL)
