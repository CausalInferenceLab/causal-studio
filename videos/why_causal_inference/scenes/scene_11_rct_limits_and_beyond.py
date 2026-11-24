from manim import *

from why_causal_inference_common import (
    ACCENT_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    load_icon,
    load_scene_timing_durations,
)


class Scene11_RctLimitsAndBeyond(Scene):
    """
    RCT의 한계와 준실험 방법론 소개

    직전 Scene (Scene10) 마지막: 무작위화 균형 검증 표
    현재 Scene 첫 문장: "알씨티는 간단하면서도 강력한 방법입니다."

    ipynb 범위: RCT 한계 섹션 ~ 준실험 방법론 목록

    핵심 주장: RCT는 강력하지만 현실적 제약이 있다.
               준실험 방법론들이 그 대안이다.
    오해 교정: 관찰 연구도 조건을 충족하면 인과 추론이 가능하다.
    visual pivot:
    - Beat 1: 좌우 분할 프레임(RCT ✓ vs 현실 ✗) — mlp.py MLPStepsPreview 패턴
    - Beat 2: 아이콘 팝업(비용/윤리/정책) + 흡연 예시 — med_test.py 순차 등장
    - Beat 3: 이상적 실험 질문 박스 → 관찰 연구 기준점
    - Beat 4: DAG 단계 빌드업 (①T→Y ②X 등장·문제 ③X 제어·해결)
    - Beat 5: 방법론 5개 계단 배치 (좌상→우하)
    - Beat 6: 카드 opacity 0.2 + 목표 텍스트 강조 — embedding.py 패턴

    Beat별 script-to-beat mapping:
    - Beat 1 (chunk 1, 6.3s): "알씨티는 강력하지만 항상 가능하지는 않습니다"
    - Beat 2 (chunk 2, 15.3s): 세 가지 한계 아이콘 + 흡연 예시 패널
    - Beat 3 (chunk 3, 11.8s): 이상적 실험 질문 박스 → 관찰 연구 기준점
    - Beat 4 (chunk 4, 18.3s): DAG 3단계 빌드업
    - Beat 5 (chunk 5, 11.1s): 방법론 5개 계단 배치
    - Beat 6 (chunk 6, 6.9s): 카드 dim + 비교 가능성 목표 강조
    """

    WAIT_TAIL = 1.0

    def construct(self):
        chunk_durations = load_scene_timing_durations("11_rct_limits_and_beyond")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            total = sum(chunk_durations[i - 1] for i in indices) - spent + extra
            if total > 0:
                self.wait(total)

        COST_COLOR = GOLD_D
        ETHICS_COLOR = BLUE_D
        POLICY_COLOR = TEAL_D

        # ── Beat 1: 좌우 분할 프레임 — RCT ✓ vs 현실 ✗ (chunk 1, 6.3s) ───────
        # mlp.py MLPStepsPreview: 수직선으로 두 패널 나눠 대비
        # 남는: 없음 / 새로: 분할선 + 좌(RCT✓) + 우(현실✗) / 핵심: 좌우 대비
        divider = Line(
            UP * 3.8, DOWN * 3.8,
            stroke_width=1.5, color=NEUTRAL_COLOR, stroke_opacity=0.45,
        )

        rct_lbl = Text("RCT", font_size=60, color=GREEN_D, weight=BOLD)
        rct_check = Text("✓", font_size=52, color=GREEN_D)
        rct_sub = Text("이상적 설계", font_size=20, color=GREEN_D)
        rct_left_grp = VGroup(rct_lbl, rct_check, rct_sub).arrange(DOWN, buff=0.22)
        rct_left_grp.move_to(LEFT * 3.2)

        real_lbl = Text("현실에서는", font_size=34, color=WHITE)
        real_cross = Text("✗", font_size=52, color=RED_D)
        real_sub = Text("항상 가능하지 않다", font_size=20, color=NEUTRAL_COLOR)
        rct_right_grp = VGroup(real_lbl, real_cross, real_sub).arrange(DOWN, buff=0.22)
        rct_right_grp.move_to(RIGHT * 3.2)

        self.play(Create(divider), run_time=0.5)
        self.play(
            FadeIn(rct_left_grp, shift=RIGHT * 0.12),
            FadeIn(rct_right_grp, shift=LEFT * 0.12),
            run_time=0.7,
        )
        # chunk 1: 6.3s, spent = 0.5 + 0.7 = 1.2s
        wait_for_chunks([1], spent=1.2)

        # ── Beat 2: 한계 아이콘 팝업 + 흡연 예시 (chunk 2, 15.3s) ─────────────
        # med_test.py NewContrastThreeContexts: 3개 항목 순차 등장 패턴
        # 제거: divider + 좌우 / 새로: 아이콘 3개(팝업) + 흡연 패널 / 핵심: 아이콘 순차
        self.play(
            FadeOut(divider), FadeOut(rct_left_grp), FadeOut(rct_right_grp),
            run_time=0.5,
        )

        icons_meta = [
            ("coin.svg",          COST_COLOR,   "비용 과다",    "대규모 임상 수십억 원",    LEFT * 3.8),
            ("scale.svg",         ETHICS_COLOR, "윤리 제약",    "흡연·무기 노출 배정 불가",  ORIGIN),
            ("building-bank.svg", POLICY_COLOR, "정책 통제",    "국가 단위 무작위 배정 불가", RIGHT * 3.8),
        ]

        icon_cols_grp = VGroup()
        for icon_file, color, title, desc, pos in icons_meta:
            icon = load_icon(icon_file, color, 1.1)
            title_txt = Text(title, font_size=21, color=color, weight=BOLD)
            desc_txt = Text(desc, font_size=17, color=NEUTRAL_COLOR)
            col = VGroup(icon, VGroup(title_txt, desc_txt).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.28)
            col.move_to(pos + UP * 0.4)
            icon_cols_grp.add(col)

        # 아이콘 순차 팝업 (scale=0.82: 약간 작게서 커지는 느낌)
        for col in icon_cols_grp:
            self.play(FadeIn(col, scale=0.82), run_time=0.8)
            self.wait(0.3)

        # "가령 임산부에게" 직전 (~chunk 2의 7.5s 지점) — 흡연 예시 패널
        no_smoking = load_icon("smoking-no.svg", RED_D, 0.65)
        smoke_txt = Text("임산부에게 흡연 무작위 배정 불가", font_size=19, color=NEUTRAL_COLOR)
        smoking_row = VGroup(no_smoking, smoke_txt).arrange(RIGHT, buff=0.3)
        smoking_box_rect = SurroundingRectangle(
            smoking_row, buff=0.24, color=NEUTRAL_COLOR,
            stroke_width=1.2, corner_radius=0.1, stroke_opacity=0.45,
        )
        smoking_panel = VGroup(smoking_box_rect, smoking_row)
        smoking_panel.move_to(DOWN * 2.3)

        self.wait(3.5)
        self.play(FadeIn(smoking_panel, shift=UP * 0.06), run_time=0.6)
        # chunk 2: 15.3s, spent = 0.5 + 3*(0.8+0.3) + 3.5 + 0.6 = 7.9s
        wait_for_chunks([2], spent=7.9)

        # ── Beat 3: 이상적 실험 사고 실험 (chunk 3, 11.8s) ──────────────────
        # 제거: 아이콘 그룹 + 흡연 패널 / 새로: 질문 박스 + 기준점 / 핵심: 질문 박스
        self.play(FadeOut(icon_cols_grp), FadeOut(smoking_panel), run_time=0.5)

        question_txt = Text(
            '"이상적인 실험이라면 어떻게 설계할까?"',
            font_size=26, color=ACCENT_COLOR,
        )
        question_box = SurroundingRectangle(
            question_txt, buff=0.3, color=ACCENT_COLOR,
            corner_radius=0.12, stroke_width=1.8,
        )
        question_grp = VGroup(question_box, question_txt)
        question_grp.move_to(UP * 0.6)

        anchor_txt = Text("관찰 연구 설계의 기준점", font_size=22, color=WHITE)
        anchor_txt.next_to(question_grp, DOWN, buff=0.55)
        anchor_arr = Arrow(
            question_grp.get_bottom() + DOWN * 0.08,
            anchor_txt.get_top() + UP * 0.08,
            stroke_width=2.5, color=NEUTRAL_COLOR, buff=0,
            max_tip_length_to_length_ratio=0.3,
        )

        self.play(FadeIn(question_grp, shift=UP * 0.08), run_time=0.7)
        self.play(GrowArrow(anchor_arr), FadeIn(anchor_txt, shift=UP * 0.05), run_time=0.6)
        # chunk 3: 11.8s, spent = 0.5 + 0.7 + 0.6 = 1.8s
        wait_for_chunks([3], spent=1.8)

        # ── Beat 4: 준실험 개념 DAG 3단계 빌드업 (chunk 4, 18.3s) ────────────
        # mlp.py LaggedStartMap(GrowArrow): 화살표 단계별 등장으로 인과 이야기 구축
        # 제거: 질문 박스 → 새로: ①T→Y ②X 등장(문제) ③X 제어(해결)
        # 핵심: 각 단계에서 바뀌는 화살표 색/opacity
        self.play(
            FadeOut(question_grp), FadeOut(anchor_arr), FadeOut(anchor_txt),
            run_time=0.5,
        )

        quasi_title = Text("준실험 방법론", font_size=28, color=WHITE, weight=BOLD)
        quasi_title.move_to(UP * 3.0)

        def q_node(label, color, fsize=20):
            txt = Text(label, font_size=fsize, color=color)
            box = SurroundingRectangle(
                txt, buff=0.22, color=color, corner_radius=0.1, stroke_width=1.8,
            )
            return VGroup(box, txt)

        def q_arrow(src, dst, color, stroke=2.2):
            dir_vec = dst.get_center() - src.get_center()
            return Arrow(
                src.get_boundary_point(dir_vec),
                dst.get_boundary_point(-dir_vec),
                buff=0.1, stroke_width=stroke, color=color,
                max_tip_length_to_length_ratio=0.25,
            )

        node_T = q_node("처치 T", GOLD_D)
        node_Y = q_node("결과 Y", TEAL_D)
        node_T.move_to(LEFT * 2.6 + UP * 0.2)
        node_Y.move_to(RIGHT * 2.6 + UP * 0.2)

        # get_right/get_left + 동일 y 좌표 고정 → 완전 수평 화살표
        ty_y = node_T.get_center()[1]  # 두 노드 동일 y (UP * 0.2)
        arr_T_Y = Arrow(
            [node_T.get_right()[0], ty_y, 0],
            [node_Y.get_left()[0], ty_y, 0],
            buff=0, stroke_width=3.0, color=ACCENT_COLOR,
            max_tip_length_to_length_ratio=0.25,
        )
        goal_lbl = Text("알고 싶은 인과 효과", font_size=17, color=NEUTRAL_COLOR)
        goal_lbl.next_to(arr_T_Y, DOWN, buff=0.2)

        # ① T→Y: "이게 알고 싶은 인과 관계"
        self.play(FadeIn(quasi_title), run_time=0.4)
        self.play(FadeIn(node_T), FadeIn(node_Y), run_time=0.6)
        self.play(Create(arr_T_Y), FadeIn(goal_lbl), run_time=0.6)
        self.wait(3.0)  # 오디오: "알씨티처럼 처치가 잠재적 결과와 독립이라는..."

        # ② 교란변수 X 등장 — 관찰 연구의 문제
        node_X = q_node("교란 변수 X", QUESTION_COLOR, fsize=18)
        node_X.move_to(UP * 2.0)
        arr_X_T = q_arrow(node_X, node_T, QUESTION_COLOR)
        arr_X_Y = q_arrow(node_X, node_Y, QUESTION_COLOR)
        problem_lbl = Text("교란 변수가 처치와 결과 모두에 영향", font_size=18, color=QUESTION_COLOR)
        problem_lbl.move_to(DOWN * 1.5)

        self.play(FadeIn(node_X, shift=DOWN * 0.1), run_time=0.5)
        self.play(
            LaggedStart(Create(arr_X_T), Create(arr_X_Y), lag_ratio=0.4),
            run_time=0.7,
        )
        self.play(FadeIn(problem_lbl, shift=UP * 0.05), run_time=0.5)
        self.wait(3.5)  # 오디오: "어떤 공변량을 통제하면 처치가 사실상..."

        # ③ 교란 경로 제어 — 준실험의 해결
        midpt = (node_X.get_center() + node_T.get_center()) / 2
        ctrl_lbl = Text("통 제", font_size=17, color=NEUTRAL_COLOR)
        ctrl_lbl.move_to(midpt + RIGHT * 0.5)
        solution_lbl = Text("처치가 사실상 무작위처럼 보이도록", font_size=20, color=ACCENT_COLOR)
        solution_lbl.move_to(DOWN * 1.5)

        self.play(
            arr_X_T.animate.set_stroke(color=NEUTRAL_COLOR, opacity=0.25),
            arr_X_Y.animate.set_stroke(color=NEUTRAL_COLOR, opacity=0.25),
            FadeOut(problem_lbl),
            run_time=0.7,
        )
        self.play(FadeIn(ctrl_lbl), run_time=0.4)
        self.play(FadeIn(solution_lbl, shift=UP * 0.05), run_time=0.5)
        # chunk 4: 18.3s, spent = 0.5+0.4+0.6+0.6+3.0+0.5+0.7+0.5+3.5+0.7+0.4+0.5 = 11.9s
        wait_for_chunks([4], spent=11.9)

        # ── Beat 5: 방법론 5개 — 2행 그리드 3+2 (chunk 5, 11.1s) ──────────────
        # 제거: 준실험 DAG 전체 / 새로: 상단 3개 + 하단 2개 그리드 / 핵심: 카드 배치
        beat4_all = VGroup(
            quasi_title, node_T, node_Y, arr_T_Y, goal_lbl,
            node_X, arr_X_T, arr_X_Y, ctrl_lbl, solution_lbl,
        )
        self.play(FadeOut(beat4_all), run_time=0.5)

        method_header = Text("앞으로 다룰 방법론들", font_size=22, color=NEUTRAL_COLOR)
        method_header.move_to(UP * 2.2)

        method_names = ["매칭", "이중차분법", "합성통제법", "도구변수", "회귀불연속"]
        method_colors = [BLUE_D, GREEN_D, GOLD_D, MAROON_D, TEAL_D]

        def make_method_card(name, color):
            txt = Text(name, font_size=18, color=color)
            box = RoundedRectangle(
                width=2.1, height=0.9, corner_radius=0.12,
                color=color, stroke_width=1.8,
            )
            box.set_fill(color=color, opacity=0.08)
            txt.move_to(box.get_center())
            return VGroup(box, txt)

        cards = VGroup(*[make_method_card(n, c) for n, c in zip(method_names, method_colors)])
        # 2행 그리드: 상단 3개(x=-3,0,3 / y=0.0), 하단 2개(x=-1.5,1.5 / y=-1.1)
        grid_pos = [(-3.0, 0.0), (0.0, 0.0), (3.0, 0.0), (-1.5, -1.1), (1.5, -1.1)]
        for card, (x, y) in zip(cards, grid_pos):
            card.move_to([x, y, 0])

        self.play(FadeIn(method_header), run_time=0.4)
        # 상단 3개 먼저, 하단 2개 이어서
        self.play(
            LaggedStart(*[FadeIn(cards[i], shift=UP * 0.08) for i in range(3)], lag_ratio=0.25),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[FadeIn(cards[i], shift=UP * 0.08) for i in range(3, 5)], lag_ratio=0.3),
            run_time=0.7,
        )
        # chunk 5: 11.1s, spent = 0.5+0.4+1.0+0.7 = 2.6s
        wait_for_chunks([5], spent=2.6)

        # ── Beat 6: 카드 opacity 0.2 + 목표 텍스트 강조 (chunk 6, 6.9s) ───────
        # embedding.py: 비포커스 항목 opacity 0.2, 핵심 목표만 선명하게
        # 카드·헤더: opacity 0.2(유지) / 새로: 목표 텍스트(카드 위 여백) / 핵심: 목표
        self.play(
            cards.animate.set_opacity(0.2),
            method_header.animate.set_opacity(0.2),
            run_time=0.6,
        )

        # 새 스크립트: "방법은 달라도 목표는 하나입니다. 두 집단을 비교 가능하게 만드는 것."
        goal_line1 = Text("방법은 달라도 목표는 하나입니다.", font_size=28, color=WHITE, weight=BOLD)
        goal_line2 = Text(
            "두 집단을 비교 가능하게 만드는 것.",
            font_size=21, color=ACCENT_COLOR,
        )
        goal_grp = VGroup(goal_line1, goal_line2).arrange(DOWN, buff=0.3)
        goal_grp.move_to(UP * 1.4)  # 상단 카드(y=0.0, top≈0.45) 위 여백

        self.play(FadeIn(goal_grp, shift=UP * 0.06), run_time=0.6)
        # chunk 6: 9.94s, spent = 0.6 + 0.6 = 1.2s
        wait_for_chunks([6], spent=1.2)

        # ── Beat 7: 에필로그 — 자연스러운 페이드아웃 ──
        # dim 상태 그대로 머물렀다가 부드럽게 페이드아웃 — 갑작스러운 밝아짐 없이
        self.wait(1.5)
        self.play(
            FadeOut(VGroup(cards, method_header, goal_grp)),
            run_time=2.5,
        )
        self.wait(self.WAIT_TAIL)
