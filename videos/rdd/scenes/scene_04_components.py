from manim import *

from rdd_common import (
    BLUE_MAIN,
    FONT,
    GRAY_LIGHT,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


class Scene04Components(Scene):
    """
    Scene 04: components (세 가지 핵심 개념)
    스크립트: videos/rdd/src/scripts/04_components.txt
    참조 ipynb: book/rdd/01_rdd_basic_ko.ipynb §4 구성 요소 (cell 7–9)
    총 길이: 81.50s

    ipynb cell 8 핵심 데이터:
        A: 69점, D=0, Y₁=?,   Y₀=3.1
        B: 70점, D=1, Y₁=3.6, Y₀=?
        C: 71점, D=1, Y₁=3.7, Y₀=?
        D: 75점, D=1, Y₁=3.9, Y₀=?

    직전 Scene03 이어받는 요소: 없음 (새 화면 시작)

    .timings.json → Beat 대응:
      Beat1 chunk1 ( 0.0~ 4.37s) 제목: 세 가지 핵심 개념
      Beat2 chunk2 ( 4.37~29.63s) ① Running Variable — X_i 레이블·예시·조작불가
      Beat3 chunk3 (29.63~42.17s) ② 컷-오프 — D_i 공식·두 경우 (MathTex 표기)
      Beat4 chunk4 (42.17~59.12s) ③ 잠재적 결과 — Y₁/Y₀ 표 등장
      Beat5 chunk5 (59.12~70.03s) ? = 반사실 강조 (SurroundingRect + 레이블)
      Beat6 chunk6 (70.03~81.32s) 90점 학생 → RDD 추정 범위 밖 텍스트
    """

    def construct(self):
        # ── Beat 1 ──────────────────────────────────────────
        # 새로 등장: 제목 2줄 (상/하)
        # 남는 요소: 없음 / 비워 두는 구역: 전체
        # 핵심 시선: "세 가지 핵심 개념"
        # 지워질 요소: 없음 → FadeOut 후 Beat2로
        title = VGroup(
            Text("세 가지 핵심 개념", font=FONT, font_size=44, color=WHITE),
            Text("Running Variable · Cutoff · 잠재적 결과",
                 font=FONT, font_size=24, color=GRAY_MID),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.6)
        self.wait(4.2)  # chunk1 끝(5.619s) 이후에 전환
        self.play(FadeOut(title), run_time=0.5)  # chunk1 end ~5.62s

        # ── Beat 2 ──────────────────────────────────────────
        # 제거: 제목
        # 새로 등장: ① 헤더(상단) + X_i(중상) + 설명(중) + 예시 pills(중하) + 조작불가(하단)
        # 비워 두는 구역: 하단(조작불가 등장 전)
        # 핵심 시선: Running Variable = X_i
        # 지워질 요소: 전부 FadeOut → Beat3
        header1 = VGroup(
            Text("①", font=FONT, font_size=28, color=BLUE_MAIN),
            Text("Running Variable", font=FONT, font_size=36, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 2.9)

        xi_label = MathTex(r"X_i", font_size=72, color=BLUE_MAIN).move_to(UP * 1.5)
        xi_desc = Text(
            "처치 여부를 결정하는 연속형 변수",
            font=FONT, font_size=22, color=WHITE,  # 검정 배경 위 → WHITE
        ).next_to(xi_label, DOWN, buff=0.4)
        examples = VGroup(
            self._pill("수능 점수", BLUE_MAIN),
            self._pill("나이", BLUE_MAIN),
            self._pill("소득 수준", BLUE_MAIN),
        ).arrange(RIGHT, buff=0.4).next_to(xi_desc, DOWN, buff=0.4)
        no_manip = Text(
            "※ 개체가 이 값을 조작할 수 없어야 함",
            font=FONT, font_size=20, color=YELLOW_MAIN,
        ).move_to(DOWN * 2.6)

        self.play(FadeIn(header1, shift=DOWN * 0.2), run_time=0.7)
        self.play(Write(xi_label), run_time=0.6)
        self.play(FadeIn(xi_desc, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(examples, shift=UP * 0.15), run_time=0.8)
        self.wait(14.7)  # 수능/나이/소득 예시 설명 구간
        self.play(FadeIn(no_manip, shift=UP * 0.15), run_time=0.7)
        self.wait(4.8)   # "조작 불가" 설명 구간 → chunk2 end ~29.02s
        self.play(
            FadeOut(VGroup(header1, xi_label, xi_desc, examples, no_manip)),
            run_time=0.6,
        )

        # ── Beat 3 ──────────────────────────────────────────
        # 제거: Beat2 전부
        # 새로 등장: ② 헤더(상단) + D_i 공식(중) + 두 경우 MathTex(중하)
        # 비워 두는 구역: 최하단 / c=70 레이블 없음
        # 핵심 시선: D_i = 1[X_i ≥ c] 공식
        # 지워질 요소: 전부 FadeOut → Beat4
        header2 = VGroup(
            Text("②", font=FONT, font_size=28, color=YELLOW_MAIN),
            Text("Cutoff (임계값)", font=FONT, font_size=36, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 2.9)

        formula = MathTex(
            r"D_i = \mathbf{1}[X_i \geq c]",
            font_size=54, color=WHITE,  # 검정 배경 위 → WHITE
        ).move_to(UP * 1.2)

        # X_i 표기: Text 대신 MathTex으로 수식 렌더링
        case1 = VGroup(
            MathTex(r"X_i \geq c", font_size=30, color=BLUE_MAIN),
            Text("→  처치 O", font=FONT, font_size=22, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.3)
        case2 = VGroup(
            MathTex(r"X_i < c", font_size=30, color=RED_MAIN),
            Text("→  처치 X", font=FONT, font_size=22, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.3)
        cases = VGroup(case1, case2).arrange(DOWN, buff=0.35).next_to(formula, DOWN, buff=0.5)

        self.play(FadeIn(header2, shift=DOWN * 0.2), run_time=0.7)
        self.play(Write(formula), run_time=1.0)
        self.play(FadeIn(cases, shift=UP * 0.15), run_time=0.8)
        self.wait(9.4)   # chunk3 end ~42.17s
        self.play(
            FadeOut(VGroup(header2, formula, cases)),
            run_time=0.6,
        )

        # ── Beat 4 ──────────────────────────────────────────
        # 제거: Beat3 전부
        # 새로 등장: ③ 헤더(상단) + Y₁/Y₀ 표(중단, ? 포함)
        # 비워 두는 구역: 하단 여백 (Beat5에서 cf_label 등장)
        # 핵심 시선: ? 칸 — 관측 불가 = 반사실
        # 지워질 요소: 없음 (table은 Beat5에서 유지)
        header3 = VGroup(
            Text("③", font=FONT, font_size=28, color=GREEN_MAIN),
            Text("잠재적 결과 (Potential Outcomes)",
                 font=FONT, font_size=32, color=GREEN_MAIN),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 3.0)

        table, q_cells, _ = self._make_po_table()
        table.next_to(header3, DOWN, buff=0.5)

        self.play(FadeIn(header3, shift=DOWN * 0.2), run_time=0.7)
        self.play(FadeIn(table, shift=UP * 0.2), run_time=0.9)
        self.wait(15.4)  # chunk4 end ~59.12s

        # ── Beat 5 ──────────────────────────────────────────
        # 남는 요소: header3 + table
        # 새로 등장: ? 칸 강조 박스(중) + "반사실" 레이블(하단)
        # 제거될 요소: q_highlights + cf_label → Beat6에서 FadeOut
        # 핵심 시선: ? = 반사실 (Counterfactual)
        q_highlights = VGroup(*[
            SurroundingRectangle(q, color=YELLOW_MAIN, buff=0.06, stroke_width=2.5)
            for q in q_cells
        ])
        cf_label = Text(
            "? = 반사실 (Counterfactual)",
            font=FONT, font_size=22, color=YELLOW_MAIN,
        ).move_to(DOWN * 2.8)

        self.play(Create(q_highlights), run_time=0.8)
        self.play(FadeIn(cf_label, shift=UP * 0.2), run_time=0.7)
        self.wait(8.9)   # chunk5 end ~70.03s

        # ── Beat 6 ──────────────────────────────────────────
        # 제거: q_highlights + cf_label
        # 새로 등장: "90점 학생 → RDD 추정 범위 밖" 텍스트(하단)
        # 남는 요소: header3 + table
        # 핵심 시선: 90점 학생의 반사실은 RDD가 다루지 않는 범위임을 명시
        self.play(FadeOut(VGroup(q_highlights, cf_label)), run_time=0.5)

        out_label = VGroup(
            Text("90점 학생의 반사실", font=FONT, font_size=22, color=RED_MAIN),
            Text("→  RDD 추정 범위 밖", font=FONT, font_size=22, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.3).move_to(DOWN * 2.8)

        self.play(FadeIn(out_label, shift=UP * 0.15), run_time=0.7)
        self.wait(11.3)  # chunk6 end ~81.32s + tail

    # ── 헬퍼 ─────────────────────────────────────────────────

    def _pill(self, label: str, color: str) -> VGroup:
        bg = RoundedRectangle(
            corner_radius=0.2, width=2.4, height=0.55,
            fill_color=color, fill_opacity=0.12,
            stroke_color=color, stroke_width=1.8,
        )
        txt = Text(label, font=FONT, font_size=20, color=color)
        txt.move_to(bg.get_center())
        return VGroup(bg, txt)

    def _make_po_table(self):
        """ipynb cell 8 기준 잠재적 결과 표. 반환: (table, q_cells, data_rows)"""
        col_labels = ["학생", "점수", "Y₁ (수혜)", "Y₀ (미수혜)"]
        data = [
            ("A", "69", "?",   "3.1"),
            ("B", "70", "3.6", "?"),
            ("C", "71", "3.7", "?"),
            ("D", "75", "3.9", "?"),
        ]
        col_w = [1.2, 1.2, 2.0, 2.0]
        row_h = 0.7
        all_rows = [col_labels] + [list(r) for r in data]

        cells = VGroup()
        q_cells = []

        for r_idx, row in enumerate(all_rows):
            is_header = r_idx == 0
            for c_idx, txt_val in enumerate(row):
                w = col_w[c_idx]
                is_q = (txt_val == "?")
                bg_color = "#1E3A5F" if is_header else (GRAY_LIGHT if r_idx % 2 == 1 else WHITE)
                # 밝은 셀 배경 위는 BLACK, 어두운 헤더는 WHITE
                txt_color = WHITE if is_header else (YELLOW_MAIN if is_q else BLACK)
                bg = Rectangle(
                    width=w, height=row_h,
                    fill_color=bg_color, fill_opacity=1,
                    stroke_color=GRAY_MID, stroke_width=0.8,
                )
                t = Text(txt_val, font=FONT, font_size=20, color=txt_color)
                t.move_to(bg.get_center())
                if t.width > w - 0.15:
                    t.scale((w - 0.15) / t.width)
                cells.add(VGroup(bg, t))
                if is_q:
                    q_cells.append(bg)

        n_cols = len(col_labels)
        n_rows = len(all_rows)
        row_groups = VGroup()
        data_rows = []
        for r in range(n_rows):
            rg = VGroup(*[cells[r * n_cols + c] for c in range(n_cols)])
            rg.arrange(RIGHT, buff=0)
            row_groups.add(rg)
            if r > 0:
                data_rows.append(rg)
        row_groups.arrange(DOWN, buff=0)
        return row_groups, q_cells, data_rows
