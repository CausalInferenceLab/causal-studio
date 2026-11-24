from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    TABLET_COLOR,
    load_scene_timing_durations,
)


class Scene09_RandomizedExperiment(Scene):
    """
    Scene 09: 무작위 실험 (RCT)

    Core Claim:
    무작위 배정은 (Y_0,Y_1)⊥T 조건을 만들어,
    편향 제거(조건 1)와 동질 반응(조건 2)을 동시에 확보한다.
    그 결과 단순 평균 차이가 ATE와 같아진다.

    Expected Misconception:
    "무작위이면 두 집단이 완벽하게 같아진다"고 오해하기 쉽다.
    실제로는 평균적으로 비슷해지는 것이며,
    두 가지 조건이 별도로 충족되어야 ATE까지 연결된다는 점을 놓치기 쉽다.

    Visual Pivot:
    Scene07에서 교란 → T 화살표가 있던 DAG와 달리,
    이번엔 교란 → T 경로가 없는 DAG로 무작위 배정의 구조적 차이를 보여준다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "현실에서 어떻게 이런 비교 가능한 집단을 만들 수 있을까요?"
    - 현재 Scene 첫 문장:
      "바로 무작위 배정입니다."
    - Cell 19-20: 무작위 배정 개념, (Y_0,Y_1)⊥T, 두 조건, ATT=ATC=ATE

    Previous Scene Continuity:
    - 직전 Scene: Scene08_WhenAssociationBecomesCausation
    - 이어받는 시각 요소: ATT=ATC=ATE 등식 구조, 비교 가능성 개념
    - 바뀌는 점: "조건이 필요하다"에서 "무작위 배정으로 조건을 확보한다"로 전환

    Script Reference:
    narration/09_randomized_experiment.txt

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py
    Reason:
    단일 독립 조건에서 두 결론이 자동으로 도출되는 점진적 수식 전개 리듬 참고.

    Script-to-Beat Mapping:
    1. "무작위 배정" 핵심 키워드 제시 (chunk 1)
    2. 교란 → T 없는 DAG: 배정이 교란과 무관함 (chunk 2)
    3. 두 집단 막대 동등화: 처치 여부 외 모든 면 비슷 (chunk 3)
    4. (Y_0,Y_1)⊥T 독립 수식 (chunk 4)
    5. "두 조건 자동 충족" 예고 (chunk 5)
    6. 조건 1: E[Y_0|T=1]=E[Y_0|T=0] → 편향=0 (chunk 6)
    7. 조건 2: E[Y_1|T=1]=E[Y_1|T=0] → ATT=ATC (chunk 7)
    8. 결론: 평균차이=ATE (chunk 8)
    9. RCT = gold standard 마무리 (chunk 9)

    Timing-to-Beat Mapping:
    - chunk 1 -> Beat 1  (0 – 1.67s)
    - chunk 2 -> Beat 2  (1.67 – 11.19s)
    - chunk 3 -> Beat 3  (11.19 – 17.69s)
    - chunk 4 -> Beat 4  (17.69 – 23.41s)
    - chunk 5 -> Beat 5  (23.41 – 27.82s)
    - chunk 6 -> Beat 6  (27.82 – 42.77s)
    - chunk 7 -> Beat 7  (42.77 – 53.50s)
    - chunk 8 -> Beat 8  (53.50 – 56.98s)
    - chunk 9 -> Beat 9  (56.98 – 69.15s)
    """

    WAIT_TAIL = 0.3

    def construct(self):
        chunk_durations = load_scene_timing_durations("09_randomized_experiment", language="ko")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        # ── 사전 Mobject 정의 ──────────────────────────────────────────────────

        # Beat 1: "무작위 배정" 핵심 키워드
        random_label = Text("무작위 배정", font_size=52, color=ACCENT_COLOR, weight=BOLD)
        random_label.move_to(ORIGIN)

        # Beat 2-3: 산점도 — 학교 여건(x) × 시험 점수(y)
        # Beat 2: 편향 있는 분포 → 무작위 배정 후 섞인 분포 (점 이동 애니메이션)
        # Beat 3: 무작위화 후 평균선 + 레이블 (처치 효과 = 두 그룹 평균 차이)
        scatter_axes = Axes(
            x_range=[0, 10, 10],
            y_range=[0, 10, 10],
            x_length=5.2,
            y_length=3.6,
            axis_config={
                "include_tip": True, "tip_length": 0.18,
                "stroke_width": 1.8, "color": NEUTRAL_COLOR, "include_ticks": False,
            },
        )
        scatter_axes.move_to(LEFT * 0.8 + DOWN * 0.1)
        scatter_x_label = Text("학교 여건", font_size=19, color=NEUTRAL_COLOR)
        scatter_x_label.next_to(scatter_axes.x_axis, DOWN, buff=0.22)
        scatter_y_label = VGroup(*[
            Text(ch, font_size=19, color=NEUTRAL_COLOR) for ch in "시험점수"
        ]).arrange(DOWN, buff=0.05)
        scatter_y_label.next_to(scatter_axes.y_axis, LEFT, buff=0.22)
        scatter_axes_group = VGroup(scatter_axes, scatter_x_label, scatter_y_label)

        # 편향 있는 배정: T=1 우상단, T=0 좌하단 (교란요인과 처치가 상관됨)
        biased_t1_coords = [
            (5.5, 5.5), (6.5, 7.0), (7.0, 6.0), (8.0, 8.0), (9.0, 7.5),
            (7.5, 8.5), (8.5, 6.5), (6.0, 8.0), (9.0, 9.0), (7.0, 7.5),
        ]
        biased_t0_coords = [
            (1.0, 2.0), (2.0, 1.0), (2.5, 3.0), (3.5, 2.5), (4.0, 1.5),
            (1.5, 3.5), (3.0, 4.0), (4.5, 3.5), (2.0, 4.5), (4.0, 4.5),
        ]
        # 무작위화 후: x 전역 분포, 두 그룹이 y 방향으로 교차(interleaved)
        # T=1 평균 y ≈ 6.0, T=0 평균 y ≈ 4.45 — 개별 점은 겹침
        random_t1_coords = [
            (1.0, 4.5), (2.0, 7.0), (3.5, 5.0), (5.0, 8.0), (6.5, 6.5),
            (8.0, 4.0), (9.0, 7.5), (4.0, 3.5), (7.0, 6.0), (2.5, 8.0),
        ]
        random_t0_coords = [
            (1.5, 3.0), (3.0, 6.5), (4.5, 2.5), (6.0, 5.5), (7.5, 3.5),
            (9.0, 6.0), (2.0, 4.0), (5.5, 2.0), (8.5, 4.5), (3.5, 7.0),
        ]

        dot_r = 0.11
        biased_t1_dots = VGroup(*[
            Dot(scatter_axes.coords_to_point(x, y), radius=dot_r, color=TABLET_COLOR, fill_opacity=0.9)
            for x, y in biased_t1_coords
        ])
        biased_t0_dots = VGroup(*[
            Dot(scatter_axes.coords_to_point(x, y), radius=dot_r, color=LIBRARY_COLOR, fill_opacity=0.9)
            for x, y in biased_t0_coords
        ])

        # Beat 3: 평균선 — T=1 평균 y≈6.8, T=0 평균 y≈3.5
        _x0 = scatter_axes.coords_to_point(0, 0)[0]
        _x1 = scatter_axes.coords_to_point(10, 0)[0]
        _my1 = scatter_axes.coords_to_point(0, 6.0)[1]  # T=1 무작위화 후 평균
        _my0 = scatter_axes.coords_to_point(0, 4.45)[1]  # T=0 무작위화 후 평균
        mean_line_t1 = DashedLine(
            [_x0, _my1, 0], [_x1, _my1, 0],
            color=TABLET_COLOR, stroke_width=2.2, dash_length=0.12,
        )
        mean_line_t0 = DashedLine(
            [_x0, _my0, 0], [_x1, _my0, 0],
            color=LIBRARY_COLOR, stroke_width=2.2, dash_length=0.12,
        )
        mean_label_t1 = MathTex(r"E[Y\mid T=1]").scale(0.6).set_color(TABLET_COLOR)
        mean_label_t0 = MathTex(r"E[Y\mid T=0]").scale(0.6).set_color(LIBRARY_COLOR)
        mean_label_t1.next_to(mean_line_t1, RIGHT, buff=0.18)
        mean_label_t0.next_to(mean_line_t0, RIGHT, buff=0.18)

        # Beat 4: (Y_0, Y_1) ⊥ T 독립 수식
        indep_formula = MathTex(
            r"(Y_0,\,Y_1)",
            r"\perp",
            r"T",
        ).scale(1.5)
        indep_formula[0].set_color(ACCENT_COLOR)
        indep_formula[1].set_color(WHITE)
        indep_formula[2].set_color(TABLET_COLOR)
        indep_formula.move_to(ORIGIN)

        # Beat 5: "두 조건 자동 충족" 예고 (수식 작게 상단)
        indep_small = MathTex(
            r"(Y_0,\,Y_1)\perp T"
        ).scale(0.75).set_color(NEUTRAL_COLOR)
        indep_small.to_edge(UP, buff=0.5)

        cond_preview = Text("두 조건이 자동으로 충족됩니다", font_size=30, color=WHITE)
        cond_preview.move_to(ORIGIN)

        # Beat 6: 조건 1 수식 + 편향=0 결과
        # 구획: 상단(조건 수식), 하단(편향=0 배지)
        cond1_formula = MathTex(
            r"E[Y_0\mid T=1]",
            r"=",
            r"E[Y_0\mid T=0]",
        ).scale(1.05)
        cond1_formula[0].set_color(TABLET_COLOR)
        cond1_formula[1].set_color(WHITE)
        cond1_formula[2].set_color(LIBRARY_COLOR)
        cond1_formula.move_to(ORIGIN + UP * 0.55)

        cond1_num = Text("① 조건", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
        cond1_num.next_to(cond1_formula, LEFT, buff=0.3)

        bias_zero_badge = RoundedRectangle(
            width=3.2, height=0.78, corner_radius=0.2,
            stroke_color=ACCENT_COLOR, stroke_width=2.2,
            fill_color=ACCENT_COLOR, fill_opacity=0.1,
        )
        bias_zero_label = MathTex(r"\text{Bias} = 0").scale(0.88).set_color(ACCENT_COLOR)
        bias_zero_badge.move_to(bias_zero_label)
        bias_zero_group = VGroup(bias_zero_badge, bias_zero_label)
        bias_zero_group.next_to(cond1_formula, DOWN, buff=0.55)

        # Beat 7: 조건 1 작게 + 조건 2 수식 + ATT=ATC
        cond1_small = MathTex(
            r"E[Y_0\mid T=1]=E[Y_0\mid T=0]"
        ).scale(0.68).set_color(NEUTRAL_COLOR)
        cond1_small.to_edge(UP, buff=0.5)

        cond2_formula = MathTex(
            r"E[Y_1\mid T=1]",
            r"=",
            r"E[Y_1\mid T=0]",
        ).scale(1.05)
        cond2_formula[0].set_color(TABLET_COLOR)
        cond2_formula[1].set_color(WHITE)
        cond2_formula[2].set_color(LIBRARY_COLOR)
        cond2_formula.move_to(ORIGIN + UP * 0.55)

        cond2_num = Text("② 조건", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
        cond2_num.next_to(cond2_formula, LEFT, buff=0.3)

        att_atc_badge = RoundedRectangle(
            width=3.8, height=0.78, corner_radius=0.2,
            stroke_color=ACCENT_COLOR, stroke_width=2.2,
            fill_color=ACCENT_COLOR, fill_opacity=0.1,
        )
        att_atc_label = MathTex(r"ATT = ATC").scale(0.88).set_color(ACCENT_COLOR)
        att_atc_badge.move_to(att_atc_label)
        att_atc_group = VGroup(att_atc_badge, att_atc_label)
        att_atc_group.next_to(cond2_formula, DOWN, buff=0.55)

        # Beat 8: 결론 수식 (평균차이 = ATE)
        conclusion_formula = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATE",
        ).scale(1.05)
        conclusion_formula[2].set_color(YELLOW_E)
        conclusion_formula.move_to(ORIGIN)

        # Beat 9: RCT gold standard 배지
        rct_label = Text("RCT", font_size=64, color=ACCENT_COLOR, weight=BOLD)
        rct_label.move_to(ORIGIN + UP * 0.5)
        gold_badge = RoundedRectangle(
            width=5.6, height=0.9, corner_radius=0.22,
            stroke_color=YELLOW_E, stroke_width=2.2,
            fill_color=YELLOW_E, fill_opacity=0.08,
        )
        gold_label = Text("인과효과 추정의 gold standard", font_size=26, color=YELLOW_E, weight=BOLD)
        gold_badge.move_to(gold_label)
        gold_group = VGroup(gold_badge, gold_label)
        gold_group.next_to(rct_label, DOWN, buff=0.55)

        # ── Beat 1: "무작위 배정" 키워드 ────────────────────────────────────
        # 남는 요소: 없음
        # 새로 등장: random_label (중앙)
        # 비워두는 영역: 전체
        # 핵심 시선: "무작위 배정" 텍스트
        self.play(FadeIn(random_label, scale=0.85), run_time=0.75)
        wait_for_chunks([1], spent=0.75)

        # ── Beat 2: 산점도 — 편향 분포 → 무작위 섞임 ────────────────────────
        # 남는 요소: 없음 (random_label FadeOut)
        # 새로 등장: scatter_axes_group → biased dots → 점 이동 애니메이션
        # 비워두는 영역: 우측 (Beat3 레이블 공간 확보)
        # 핵심 시선: 점들이 섞이는 순간 (무작위 배정의 시각적 의미)
        self.play(FadeOut(random_label, scale=0.95), run_time=0.35)
        self.play(FadeIn(scatter_axes_group), run_time=0.7)
        self.play(
            FadeIn(biased_t1_dots, lag_ratio=0.12),
            FadeIn(biased_t0_dots, lag_ratio=0.12),
            run_time=0.9,
        )
        # 편향 상태를 잠깐 보여준 뒤 무작위 배정으로 점들이 섞임
        self.wait(2.4)
        self.play(
            *[biased_t1_dots[i].animate.move_to(
                scatter_axes.coords_to_point(*random_t1_coords[i])
              ) for i in range(len(random_t1_coords))],
            *[biased_t0_dots[i].animate.move_to(
                scatter_axes.coords_to_point(*random_t0_coords[i])
              ) for i in range(len(random_t0_coords))],
            run_time=1.2,
        )
        wait_for_chunks([2], spent=5.55)

        # ── Beat 3: 평균선 + 레이블 — 두 그룹 평균 비교 ─────────────────────
        # 남는 요소: scatter_axes_group + biased_t1/t0_dots (무작위화 후 위치)
        # 새로 등장: mean_line_t1, mean_line_t0, mean_label_t1, mean_label_t0
        # 비워두는 영역: 우측 레이블 공간
        # 핵심 시선: 두 평균선의 간격 = 순수한 처치 효과
        self.play(
            Create(mean_line_t1),
            Create(mean_line_t0),
            run_time=0.7,
        )
        self.play(
            FadeIn(mean_label_t1, shift=LEFT * 0.05),
            FadeIn(mean_label_t0, shift=LEFT * 0.05),
            run_time=0.55,
        )
        wait_for_chunks([3], spent=1.25)

        # ── Beat 4: (Y_0, Y_1) ⊥ T 독립 수식 ──────────────────────────────
        # 남는 요소: 없음 (scatter 일체 FadeOut)
        # 새로 등장: indep_formula (중앙, 크게)
        # 비워두는 영역: 상단/하단
        # 핵심 시선: ⊥ 기호 (독립 조건)
        self.play(
            FadeOut(scatter_axes_group),
            FadeOut(biased_t1_dots),
            FadeOut(biased_t0_dots),
            FadeOut(mean_line_t1),
            FadeOut(mean_line_t0),
            FadeOut(mean_label_t1),
            FadeOut(mean_label_t0),
            run_time=0.5,
        )
        self.play(FadeIn(indep_formula, scale=0.9), run_time=0.8)
        self.play(Indicate(indep_formula[1], color=WHITE, scale_factor=1.1), run_time=0.55)
        wait_for_chunks([4], spent=1.85)

        # ── Beat 5: "두 조건 자동 충족" 예고 ────────────────────────────────
        # 남는 요소: indep_small (수식 축소 → 상단)
        # 새로 등장: cond_preview (중앙)
        # 비워두는 영역: 하단
        # 핵심 시선: "두 조건" 텍스트
        self.play(Transform(indep_formula, indep_small), run_time=0.6)
        self.play(FadeIn(cond_preview, shift=UP * 0.07), run_time=0.6)
        wait_for_chunks([5], spent=1.2)

        # ── Beat 6: 조건 1 — E[Y_0|T=1] = E[Y_0|T=0] + 편향=0 ─────────────
        # 남는 요소: 없음 (cond_preview FadeOut, indep_formula 제거)
        # 새로 등장: cond1_num, cond1_formula (상단), bias_zero_group (하단)
        # 비워두는 영역: 좌/우 여백
        # 핵심 시선: cond1_formula
        self.play(
            FadeOut(cond_preview),
            FadeOut(indep_formula),
            run_time=0.5,
        )
        self.play(
            FadeIn(cond1_num, shift=RIGHT * 0.05),
            FadeIn(cond1_formula, shift=UP * 0.07),
            run_time=0.75,
        )
        self.play(
            Indicate(cond1_formula[0], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(cond1_formula[2], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        self.wait(3.5)
        self.play(FadeIn(bias_zero_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(bias_zero_badge, color=ACCENT_COLOR, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([6], spent=6.45)

        # ── Beat 7: 조건 2 — E[Y_1|T=1] = E[Y_1|T=0] + ATT=ATC ────────────
        # 남는 요소: cond1_small (조건1 축소 → 상단)
        # 새로 등장: cond2_num, cond2_formula, att_atc_group
        # 비워두는 영역: 좌/우 여백, 상단은 조건1 small
        # 핵심 시선: cond2_formula + ATT=ATC
        self.play(
            Transform(cond1_formula, cond1_small),
            FadeOut(cond1_num),
            FadeOut(bias_zero_group),
            run_time=0.6,
        )
        self.play(
            FadeIn(cond2_num, shift=RIGHT * 0.05),
            FadeIn(cond2_formula, shift=UP * 0.07),
            run_time=0.75,
        )
        self.play(
            Indicate(cond2_formula[0], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(cond2_formula[2], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        self.wait(2.5)
        self.play(FadeIn(att_atc_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(att_atc_badge, color=ACCENT_COLOR, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([7], spent=5.55)

        # ── Beat 8: 결론 — 평균차이 = ATE ──────────────────────────────────
        # 남는 요소: 없음 (조건들 FadeOut)
        # 새로 등장: conclusion_formula (중앙)
        # 비워두는 영역: 상단/하단
        # 핵심 시선: ATE 항
        self.play(
            FadeOut(cond1_formula),
            FadeOut(cond2_num),
            FadeOut(cond2_formula),
            FadeOut(att_atc_group),
            run_time=0.55,
        )
        self.play(FadeIn(conclusion_formula, shift=UP * 0.07), run_time=0.75)
        self.play(Indicate(conclusion_formula[2], color=YELLOW_E, scale_factor=1.08), run_time=0.5)
        wait_for_chunks([8], spent=1.8)

        # ── Beat 9: RCT = gold standard ──────────────────────────────────
        # 남는 요소: 없음 (conclusion_formula FadeOut)
        # 새로 등장: rct_label (상단), gold_group (하단)
        # 비워두는 영역: 좌/우 여백
        # 핵심 시선: "RCT" 텍스트 + gold_group 배지
        self.play(FadeOut(conclusion_formula), run_time=0.5)
        self.play(FadeIn(rct_label, scale=0.85), run_time=0.75)
        self.play(FadeIn(gold_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(gold_badge, color=YELLOW_E, scale_factor=1.03), run_time=0.55)
        wait_for_chunks([9], spent=2.4)
        self.wait(self.WAIT_TAIL)
