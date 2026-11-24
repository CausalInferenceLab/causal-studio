from manim import *

from why_causal_inference_common import (
    ACCENT_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    load_icon,
    load_scene_timing_durations,
)


class Scene10_OnlineClassroomRCT(Scene):
    """
    Scene 10: 온라인 수업 RCT 사례

    Core Claim:
    실제 RCT 데이터(온라인 수업 실험)를 통해 단순 평균 차이 = ATE 직접 확인.
    대면 78.55 vs 온라인 73.64 → ATE ≈ -4.91점.
    무작위 배정이 선택 편향을 설계 단계에서 제거하기 때문에 인과 해석 가능.

    Expected Misconception:
    "온라인 학생이 원래 더 우수/열등할 수 있다"는 선택 편향 우려.
    RCT는 설계 단계에서 이를 제거하므로 단순 평균 차이 = ATE.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "무작위 배정 하나로, 비교 가능성의 두 조건을 동시에 확보할 수 있습니다."
    - 현재 Scene 첫 문장:
      "실제 데이터로 확인해 볼게요."
    - Cell 22: 온라인 수업 실험 소개 (대면/온라인/혼합 무작위 배정)
    - Cell 23-24: face_to_face=78.55, blended=77.09, online=73.64
    - Cell 25: ATE≈-4.91, 균형 검증 (gender/asian/black/hispanic/white)

    Script-to-Beat Mapping:
    - Beat 1: chunk 1 (0-1.8s) + chunk 2 (1.8-11.2s) → 실험 소개 타이틀
    - Beat 2: chunk 3 (11.2-26.1s) → 세 수업 방식 카드 + 무작위 배정
    - Beat 3: chunk 4 (26.1-50.7s) → 선택 편향 문제 + RCT 해결
    - Beat 4: chunk 5 (50.7-56.6s) + chunk 6 (56.6-72.4s) + chunk 7 (72.4-83.9s) → 결과 표 + ATE
    - Beat 5: chunk 8 (83.9-110.9s) → 균형 검증 표
    """

    WAIT_TAIL = 0.3

    def construct(self):
        chunk_durations = load_scene_timing_durations("10_online_classroom_rct")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            total = sum(chunk_durations[i - 1] for i in indices) - spent + extra
            if total > 0:
                self.wait(total)

        FACE_COLOR = BLUE_D
        ONLINE_COLOR = MAROON_D
        BLEND_COLOR = GREEN_D

        icon_face = load_icon("school.svg", FACE_COLOR, 0.72)
        icon_online = load_icon("device-desktop.svg", ONLINE_COLOR, 0.72)
        icon_blend = load_icon("devices.svg", BLEND_COLOR, 0.72)

        # ── Beat 1: 실험 소개 — 아이콘으로 T/Y 시각화 (chunk 1-2, 11.05s) ──────
        # 남는: 없음 / 새로: title, T 아이콘 3개+레이블, 화살표, Y 아이콘+레이블
        # 핵심: "처치 T = 수업 방식 → 결과 Y = 기말 점수" 관계
        title = Text("온라인 수업 실험", font_size=40, color=WHITE)
        title.move_to(UP * 2.0)

        # T 섹션: 처치 T 헤더 + 수업방식 아이콘 3개
        t_header = Text("처치  T", font_size=22, color=NEUTRAL_COLOR)
        icon_f1 = load_icon("school.svg", FACE_COLOR, 0.5)
        icon_b1 = load_icon("devices.svg", BLEND_COLOR, 0.5)
        icon_o1 = load_icon("device-desktop.svg", ONLINE_COLOR, 0.5)
        lbl_f1 = Text("대면", font_size=16, color=FACE_COLOR)
        lbl_b1 = Text("혼합", font_size=16, color=BLEND_COLOR)
        lbl_o1 = Text("온라인", font_size=16, color=ONLINE_COLOR)
        col_f1 = VGroup(icon_f1, lbl_f1).arrange(DOWN, buff=0.1)
        col_b1 = VGroup(icon_b1, lbl_b1).arrange(DOWN, buff=0.1)
        col_o1 = VGroup(icon_o1, lbl_o1).arrange(DOWN, buff=0.1)
        t_icons = VGroup(col_f1, col_b1, col_o1).arrange(RIGHT, buff=0.35)
        t_section = VGroup(t_header, t_icons).arrange(DOWN, buff=0.28)
        t_section.move_to(LEFT * 2.8 + DOWN * 0.3)

        # Y 섹션: 결과 Y 헤더 + 체크리스트 아이콘 + 레이블
        y_header = Text("결과  Y", font_size=22, color=NEUTRAL_COLOR)
        icon_y = load_icon("checklist.svg", ACCENT_COLOR, 0.55)
        lbl_y = Text("기말 시험 점수", font_size=16, color=ACCENT_COLOR)
        y_col = VGroup(icon_y, lbl_y).arrange(DOWN, buff=0.1)
        y_section = VGroup(y_header, y_col).arrange(DOWN, buff=0.28)
        y_section.move_to(RIGHT * 2.5 + DOWN * 0.3)

        # T → Y 화살표
        ty_arrow = Arrow(
            t_section.get_right() + RIGHT * 0.1,
            y_section.get_left() + LEFT * 0.1,
            buff=0.05, stroke_width=2.5, color=NEUTRAL_COLOR,
            max_tip_length_to_length_ratio=0.1,
        )

        ty_visual = VGroup(t_section, ty_arrow, y_section)

        self.play(FadeIn(title, shift=UP * 0.06), run_time=0.6)
        self.play(
            LaggedStart(
                FadeIn(t_section, shift=RIGHT * 0.05),
                GrowArrow(ty_arrow),
                FadeIn(y_section, shift=LEFT * 0.05),
                lag_ratio=0.3,
            ),
            run_time=1.1,
        )
        wait_for_chunks([1, 2], spent=1.7)

        # ── Beat 2: 세 수업 방식 카드 (chunk 3, 14.9s) ───────────────────────
        # 남는: title(상단 축소) / 제거: ty_labels / 새로: 카드 3개 + RCT 배지→화살표
        # 핵심: 대면/혼합/온라인 카드

        def make_format_card(icon, label, color):
            lbl = Text(label, font_size=24, color=color)
            grp = VGroup(icon, lbl).arrange(DOWN, buff=0.2)
            rect = SurroundingRectangle(
                grp, buff=0.25, color=color,
                stroke_opacity=0.7, fill_opacity=0.06, fill_color=color,
            )
            return VGroup(rect, grp)

        card_f = make_format_card(icon_face, "대면", FACE_COLOR)
        card_b = make_format_card(icon_blend, "혼합", BLEND_COLOR)
        card_o = make_format_card(icon_online, "온라인", ONLINE_COLOR)
        cards = VGroup(card_f, card_b, card_o).arrange(RIGHT, buff=0.55)
        cards.move_to(ORIGIN)

        rct_badge = Text("무작위 배정", font_size=22, color=ACCENT_COLOR)
        rct_badge.move_to(UP * 2.4)
        rct_arr = Arrow(
            rct_badge.get_bottom() + DOWN * 0.05,
            cards.get_top() + UP * 0.05,
            buff=0.1, stroke_width=2.0, color=ACCENT_COLOR,
            max_tip_length_to_length_ratio=0.12,
        )

        self.play(
            title.animate.scale(0.65).to_edge(UP, buff=0.25),
            FadeOut(ty_visual),
            run_time=0.55,
        )
        self.play(
            LaggedStart(
                FadeIn(card_f, shift=UP * 0.05),
                FadeIn(card_b, shift=UP * 0.05),
                FadeIn(card_o, shift=UP * 0.05),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )
        self.play(FadeIn(rct_badge), Create(rct_arr), run_time=0.8)

        # ── Beat 2 Phase 2: "처치는 수업 방식, 결과는 기말 점수" (chunk 3 후반) ──
        # 카드 좌측 축소 이동 + 우측에 T→Y 다이어그램 등장
        # chunk 3 = 16.02s, phase1 spent ≈ 1.8s → 나머지 ~9s 대기 후 전환
        self.wait(8.5)

        # rct_badge/arr FadeOut 후 카드 축소+이동, Y 섹션 등장
        t_lbl = Text("처치  T", font_size=21, color=NEUTRAL_COLOR)
        icon_y2 = load_icon("checklist.svg", ACCENT_COLOR, 0.6)
        y_lbl2 = Text("기말 시험 점수", font_size=18, color=ACCENT_COLOR)
        y_hdr2 = Text("결과  Y", font_size=21, color=NEUTRAL_COLOR)
        y_col2 = VGroup(icon_y2, y_lbl2).arrange(DOWN, buff=0.12)
        y_sec2 = VGroup(y_hdr2, y_col2).arrange(DOWN, buff=0.28)
        y_sec2.move_to(RIGHT * 3.0)

        ty_mid_arr = Arrow(
            LEFT * 0.6, RIGHT * 1.8,
            buff=0.0, stroke_width=2.5, color=NEUTRAL_COLOR,
            max_tip_length_to_length_ratio=0.1,
        )

        self.play(
            FadeOut(rct_badge), FadeOut(rct_arr),
            cards.animate.scale(0.72).move_to(LEFT * 3.0),
            run_time=0.65,
        )
        t_lbl.next_to(cards, UP, buff=0.18)
        self.play(FadeIn(t_lbl), run_time=0.4)
        self.play(GrowArrow(ty_mid_arr), FadeIn(y_sec2, shift=LEFT * 0.05), run_time=0.7)
        # spent(chunk3): 0.55+1.0+0.8+8.5+0.65+0.4+0.7 = 12.6s → wait 16.02-12.6 = 3.42s
        wait_for_chunks([3], spent=12.6)

        # ── Beat 3: 선택 편향 문제 → RCT 해결 (chunk 4, 23.87s) ──────────────
        # 남는: 없음 (모두 FadeOut) / 핵심: 선택 편향 DAG → 무작위 배정이 차단
        # 이 Beat 시작은 chunk 4 시작 시점 (0.5s FadeOut 포함)
        self.play(
            FadeOut(cards), FadeOut(t_lbl), FadeOut(ty_mid_arr), FadeOut(y_sec2), FadeOut(title),
            run_time=0.5,
        )

        # DAG 노드 헬퍼: SurroundingRectangle + 텍스트
        def dag_node(label, color, fsize=22):
            txt = Text(label, font_size=fsize, color=color)
            box = SurroundingRectangle(txt, buff=0.22, color=color, stroke_opacity=0.8,
                                       fill_color=color, fill_opacity=0.08)
            return VGroup(box, txt)

        node_bg = dag_node("학생 배경", QUESTION_COLOR)       # 교란변수 (상단 중앙)
        node_T  = dag_node("수업 방식 T", ONLINE_COLOR)       # 처치 (좌하단)
        node_Y  = dag_node("성적 Y", ACCENT_COLOR)            # 결과 (우하단)

        node_bg.move_to(UP * 1.5)
        node_T.move_to(LEFT * 3.0 + DOWN * 0.8)
        node_Y.move_to(RIGHT * 3.0 + DOWN * 0.8)

        # 화살표 3개: 배경→T (교란 경로), 배경→Y, T→Y (인과)
        def dag_arrow(src, dst, color, stroke=2.2):
            return Arrow(
                src.get_boundary_point(dst.get_center() - src.get_center()),
                dst.get_boundary_point(src.get_center() - dst.get_center()),
                buff=0.08, stroke_width=stroke, color=color,
                max_tip_length_to_length_ratio=0.12,
            )

        arr_bg_T = dag_arrow(node_bg, node_T, QUESTION_COLOR)   # 교란 경로 (나중에 X)
        arr_bg_Y = dag_arrow(node_bg, node_Y, QUESTION_COLOR)
        arr_T_Y  = dag_arrow(node_T,  node_Y, NEUTRAL_COLOR)

        # 교란 경로 라벨: "배경 → 수업 선택"
        conf_label = Text("자기주도? 저소득?", font_size=18, color=QUESTION_COLOR)
        conf_label.next_to(arr_bg_T, LEFT, buff=0.08)

        # X 마크 (교란 경로 차단) + RCT 설명
        cross = Text("✕", font_size=38, color=ACCENT_COLOR)
        cross.move_to(arr_bg_T.get_center())
        rct_cut = Text("무작위 배정이 이 경로를 차단합니다", font_size=21, color=ACCENT_COLOR)
        rct_cut.move_to(DOWN * 2.5)

        bq = Text("무작위 배정 없었다면?", font_size=28, color=ACCENT_COLOR)
        bq.move_to(UP * 3.0)

        # Beat 3 애니메이션: DAG 구축 → 교란 경로 강조 → 차단
        self.play(FadeIn(bq), run_time=0.6)
        self.wait(2.0)
        self.play(
            LaggedStart(FadeIn(node_bg), FadeIn(node_T), FadeIn(node_Y), lag_ratio=0.25),
            run_time=0.9,
        )
        self.play(
            Create(arr_bg_T), Create(arr_bg_Y), Create(arr_T_Y),
            run_time=0.8,
        )
        self.play(FadeIn(conf_label, shift=RIGHT * 0.04), run_time=0.5)
        self.wait(4.0)
        # 교란 경로 강조 (빨갛게 Indicate)
        self.play(Indicate(arr_bg_T, color=RED_D, scale_factor=1.1), run_time=0.7)
        self.wait(5.0)
        # RCT가 교란 경로 차단
        self.play(
            arr_bg_T.animate.set_opacity(0.25),
            conf_label.animate.set_opacity(0.25),
            run_time=0.5,
        )
        self.play(FadeIn(cross, scale=0.5), run_time=0.5)
        self.play(FadeIn(rct_cut, shift=UP * 0.05), run_time=0.6)
        # spent(chunk4): 0.5+0.6+2.0+0.9+0.8+0.5+4.0+0.7+5.0+0.5+0.5+0.6 = 16.6s
        wait_for_chunks([4], spent=16.6)

        # ── Beat 4: 결과 표 + ATE (chunk 5-7, 33.2s) ─────────────────────────
        # 남는: 없음 / 새로: 결과 표(3행×2열) + ATE 수식
        # 핵심: 78.55 vs 73.64, ATE≈−4.91
        self.play(
            FadeOut(bq), FadeOut(node_bg), FadeOut(node_T), FadeOut(node_Y),
            FadeOut(arr_bg_T), FadeOut(arr_bg_Y), FadeOut(arr_T_Y),
            FadeOut(conf_label), FadeOut(cross), FadeOut(rct_cut),
            run_time=0.5,
        )

        # 고정 열 x 좌표 (2열: 수업방식 | 평균점수)
        col_xs = [-1.8, 1.4]
        row_ys = [1.6, 0.7, -0.1, -0.9]
        res_data = [
            ("수업 방식", "평균 점수"),
            ("대면",     "78.55"),
            ("혼합",     "77.09"),
            ("온라인",   "73.64"),
        ]
        res_colors = [
            [NEUTRAL_COLOR, NEUTRAL_COLOR],
            [FACE_COLOR,    FACE_COLOR],
            [BLEND_COLOR,   BLEND_COLOR],
            [ONLINE_COLOR,  ONLINE_COLOR],
        ]
        res_fsizes = [22, 26, 26, 26]

        res_cells = []
        for r, (row_data, cols_color, fsize) in enumerate(zip(res_data, res_colors, res_fsizes)):
            for c, (val, color) in enumerate(zip(row_data, cols_color)):
                cell = Text(val, font_size=fsize, color=color)
                cell.move_to([col_xs[c], row_ys[r], 0])
                res_cells.append(cell)
        res_table = VGroup(*res_cells)

        divider = Line(
            [col_xs[0] - 0.6, row_ys[0] - 0.42, 0],
            [col_xs[1] + 0.8, row_ys[0] - 0.42, 0],
            stroke_width=1.5, color=NEUTRAL_COLOR, stroke_opacity=0.5,
        )

        ate_eq = VGroup(
            MathTex(r"\widehat{ATE} = 78.55 - 73.64 \approx -4.91", font_size=30).set_color(WHITE),
            Text("점", font_size=28, color=WHITE),
        ).arrange(RIGHT, buff=0.05)
        ate_eq.move_to(DOWN * 2.0)

        self.play(FadeIn(VGroup(*res_cells[:2])), Create(divider), run_time=0.7)
        self.play(
            LaggedStart(
                FadeIn(VGroup(*res_cells[2:4])),
                FadeIn(VGroup(*res_cells[4:6])),
                FadeIn(VGroup(*res_cells[6:8])),
                lag_ratio=0.35,
            ),
            run_time=0.9,
        )
        # chunk 5: 에이티이 추정 방법 간단 (5.9s)
        wait_for_chunks([5], spent=0.5 + 0.7 + 0.9)  # FadeOut + 표 표시

        self.play(FadeIn(ate_eq, shift=UP * 0.05), run_time=0.7)
        self.play(Indicate(ate_eq, color=ACCENT_COLOR, scale_factor=1.06), run_time=0.6)
        # chunk 6: 수치 결과 (15.7s)
        wait_for_chunks([6], spent=1.3)

        # chunk 7: 걱정 불필요 — 결과 표에서 두 값 Indicate
        self.play(Indicate(VGroup(*res_cells[2:4]), color=FACE_COLOR, scale_factor=1.06), run_time=0.5)
        self.play(Indicate(VGroup(*res_cells[6:8]), color=ONLINE_COLOR, scale_factor=1.06), run_time=0.5)
        # chunk 7: 11.5s
        wait_for_chunks([7], spent=1.0)

        # ── Beat 5: 균형 검증 표 (chunk 8, 27.1s) ────────────────────────────
        # 남는: 없음 / 새로: 균형 검증 표(6행×5열)
        # 핵심: 흑인계(△) — 소규모 표본의 한계
        self.play(
            FadeOut(res_table), FadeOut(divider), FadeOut(ate_eq),
            run_time=0.5,
        )

        bal_title = Text("무작위화 균형 검증", font_size=24, color=NEUTRAL_COLOR)
        bal_title.move_to(UP * 2.8)

        # 5열: 변수 | 대면 | 혼합 | 온라인 | 균형
        col_xs_b = [-3.1, -1.5, -0.6, 0.3, 1.2]
        row_ys_b = [2.0, 1.3, 0.6, -0.1, -0.8, -1.5]
        bal_data = [
            ("변수",    "대면",  "혼합",  "온라인", ""),
            ("성별",    "0.63", "0.55", "0.54",  "✓"),
            ("아시아계", "0.20", "0.22", "0.23",  "✓"),
            ("흑인계",  "0.07", "0.10", "0.03",  "△"),
            ("히스패닉", "0.01", "0.01", "0.03",  "✓"),
            ("백인",    "0.72", "0.63", "0.70",  "✓"),
        ]

        bal_row_groups = []
        for r, row_data in enumerate(bal_data):
            row_cells = []
            for c, val in enumerate(row_data):
                if r == 0:
                    color, fsize = NEUTRAL_COLOR, 18
                elif c == 0:
                    color, fsize = NEUTRAL_COLOR, 19
                elif c == 4:
                    color, fsize = (YELLOW_E if val == "△" else TEAL_D), 19
                elif r == 3:   # 흑인계 행 경고색
                    color, fsize = YELLOW_E, 19
                else:
                    color, fsize = WHITE, 19
                cell = Text(val, font_size=fsize, color=color)
                cell.move_to([col_xs_b[c], row_ys_b[r], 0])
                row_cells.append(cell)
            bal_row_groups.append(VGroup(*row_cells))

        bal_divider = Line(
            [col_xs_b[0] - 0.4, row_ys_b[0] - 0.42, 0],
            [col_xs_b[4] + 0.35, row_ys_b[0] - 0.42, 0],
            stroke_width=1.5, color=NEUTRAL_COLOR, stroke_opacity=0.5,
        )

        bal_note = Text(
            "소규모 표본에서는 우연한 불균형이 생길 수 있다",
            font_size=19, color=NEUTRAL_COLOR,
        )
        bal_note.move_to(DOWN * 2.1)

        self.play(FadeIn(bal_title), run_time=0.5)
        self.play(FadeIn(bal_row_groups[0]), Create(bal_divider), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(bal_row_groups[i]) for i in range(1, 6)], lag_ratio=0.25),
            run_time=1.2,
        )
        self.play(Indicate(bal_row_groups[3], color=YELLOW_E, scale_factor=1.08), run_time=0.6)
        self.play(FadeIn(bal_note, shift=UP * 0.05), run_time=0.6)
        # chunk 8: 27.1s, spent = 0.5(FadeOut)+0.5+0.6+1.2+0.6+0.6 = 4.0s
        wait_for_chunks([8], spent=4.0)
        self.wait(self.WAIT_TAIL)
