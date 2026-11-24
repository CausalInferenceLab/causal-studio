from manim import *

from videos.rdd.shared.common import (
    BLUE_MAIN,
    FONT,
    GRAY_DARK,
    GRAY_LIGHT,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


class Scene01RddIntro(Scene):
    """
    Scene 01: rdd_intro
    스크립트: videos/rdd/ko/narration/01_rdd_intro.txt
    build/audio/01_rdd_intro.timings.json 기준 타이밍 (총 97.19s)

    Beat1 chunk1  ( 0.00~ 4.69s)  알디디 소개 타이틀 (4.69s)
    Beat2 chunk2  ( 4.69~11.47s)  예시 설정: 수능 370점 기준 (6.78s)
    Beat3 chunk3  (11.47~32.37s)  369/371점 학생 카드 + 뱃지 + 2점 차이 (20.90s)
    Beat4 chunk4  (32.37~52.99s)  인과 질문 → 두 학생 비교 → 동등 조건 강조 (20.62s)
    Beat5 chunk5  (52.99~57.91s)  RDD 핵심 아이디어 타이틀 (4.92s)
    Beat6 chunk6  (57.91~66.22s)  정의: 기준점 근방 비교 → 인과 효과 추정 (8.31s)
    Beat7 chunk7  (66.22~78.62s)  ≈ 준무작위 배정 (12.40s)
    Beat8 chunk8  (78.62~90.09s)  적용 사례 테이블 (11.47s)
    Beat9 chunk9  (90.09~96.87s)  마무리 (6.78s)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~5.15s) ────────────────────────
        # 새로 등장: RDD 소개 타이틀 3줄
        # 핵심 시선: "RDD" + "Regression Discontinuity Design"
        # 지워질 요소: FadeOut → Beat2
        title = VGroup(
            Text("RDD", font=FONT, font_size=56, color=BLUE_MAIN),
            Text("Regression Discontinuity Design", font=FONT, font_size=26, color=BLUE_MAIN),
            Text("인과추론 방법론 중 하나", font=FONT, font_size=22, color=GRAY_MID),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(title[2], shift=UP * 0.15), run_time=0.4)
        self.wait(3.25)
        self.play(FadeOut(title), run_time=0.3)  # chunk1 end ~5.15s

        # ── Beat 2 (chunk2: 5.15~11.89s, 6.73s) ────────────
        # 새로 등장: 예시 설정 텍스트
        # 핵심 시선: "A대학교 장학금 기준: 수능 370점"
        # 지워질 요소: FadeOut → Beat3
        ex_intro = Text("먼저 예시로 감을 잡아보죠.", font=FONT, font_size=30, color=GRAY_MID).move_to(UP * 1.0)
        ex_setup = VGroup(
            Text("A대학교 장학금 기준:", font=FONT, font_size=32, color=WHITE),
            Text("수능 370점", font=FONT, font_size=44, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.35).next_to(ex_intro, DOWN, buff=0.55)

        self.play(FadeIn(ex_intro, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(ex_setup, shift=DOWN * 0.15), run_time=0.7)
        self.wait(5.03)
        self.play(FadeOut(VGroup(ex_intro, ex_setup)), run_time=0.5)  # chunk2 end ~11.89s

        # ── Beat 3 (chunk3: 11.89~32.60s, 20.71s) ───────────
        # 새로 등장: 학생 카드(좌·우) → 뱃지 → 2점 차이 강조 (하단)
        # 핵심 시선: 369점/371점 두 학생, 단 2점 차이
        # 지워질 요소: diff_note FadeOut → Beat4 (카드·뱃지는 Beat4에서도 유지)
        card_left  = self._student_card("369점", "학생 A", RED_MAIN).move_to(LEFT * 3)
        card_right = self._student_card("371점", "학생 B", BLUE_MAIN).move_to(RIGHT * 3)

        self.play(
            FadeIn(card_left,  shift=RIGHT * 0.3),
            FadeIn(card_right, shift=LEFT  * 0.3),
            run_time=1.0,
        )
        self.wait(3.0)

        badge_no  = self._badge("장학금 ✗", RED_MAIN).next_to(card_left,  DOWN, buff=0.4)
        badge_yes = self._badge("장학금 ✓", GREEN_MAIN).next_to(card_right, DOWN, buff=0.4)

        self.play(
            FadeIn(badge_no,  shift=DOWN * 0.2),
            FadeIn(badge_yes, shift=DOWN * 0.2),
            run_time=0.8,
        )
        self.wait(3.5)

        diff_note = Text(
            "2점 차이 = 컨디션·운의 차이",
            font=FONT, font_size=24, color=YELLOW_MAIN,
        ).move_to(DOWN * 2.8)

        self.play(FadeIn(diff_note, shift=UP * 0.15), run_time=0.7)
        self.wait(11.71)  # chunk3 end ~32.60s

        # ── Beat 4 (chunk4: 32.60~53.68s, 21.08s) ───────────
        # 남는 요소: 카드 + 뱃지
        # 새로 등장: 인과 질문 → 비교 답변 + 강조 → 동등 조건 설명
        # 핵심 시선: 두 학생이 가장 이상적인 비교대상
        # 지워질 요소: Beat5에서 전부 FadeOut
        self.play(FadeOut(diff_note), run_time=0.4)

        question = Text(
            "장학금의 대학교 성적에 대한 인과 효과를 알고 싶다면?",
            font=FONT, font_size=24, color=WHITE,
        ).move_to(UP * 2.6)

        self.play(FadeIn(question, shift=DOWN * 0.15), run_time=0.9)
        self.wait(4.0)

        answer = Text(
            "바로 이 두 학생을 비교해보면 어떨까요?",
            font=FONT, font_size=26, color=YELLOW_MAIN,
        ).next_to(question, DOWN, buff=0.45)

        circle_left  = SurroundingRectangle(card_left,  color=YELLOW_MAIN, buff=0.15, stroke_width=3)
        circle_right = SurroundingRectangle(card_right, color=YELLOW_MAIN, buff=0.15, stroke_width=3)

        self.play(
            FadeIn(answer, shift=DOWN * 0.15),
            Create(circle_left),
            Create(circle_right),
            run_time=0.9,
        )
        self.wait(5.0)

        equal_note = VGroup(
            Text("장학금 수혜 여부를 제외하면 사실상 동등한 조건", font=FONT, font_size=19, color=GREEN_MAIN),
            Text("→ 가장 이상적인 비교대상", font=FONT, font_size=20, color=GREEN_MAIN),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.8)

        self.play(FadeIn(equal_note, shift=UP * 0.15), run_time=0.7)
        self.wait(9.18)  # chunk4 end ~53.68s

        # ── Beat 5 (chunk5: 53.68~57.91s, 4.23s) ────────────
        # 제거: 카드·뱃지·강조·질문·답변·equal_note 전부
        # 새로 등장: RDD 핵심 아이디어 타이틀
        # 핵심 시선: "이것이 RDD의 핵심 아이디어"
        self.play(
            FadeOut(VGroup(
                card_left, card_right,
                badge_no, badge_yes,
                circle_left, circle_right,
                question, answer, equal_note,
            )),
            run_time=0.6,
        )

        rdd_title = VGroup(
            Text("이것이 RDD의 핵심 아이디어입니다", font=FONT, font_size=34, color=WHITE),
            Text("Regression Discontinuity Design", font=FONT, font_size=24, color=BLUE_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.8)

        self.play(FadeIn(rdd_title, shift=UP * 0.2), run_time=0.8)
        self.wait(2.83)  # chunk5 end ~57.91s

        # ── Beat 6 (chunk6: 57.91~66.64s, 8.73s) ────────────
        # 남는 요소: rdd_title
        # 새로 등장: 정의 텍스트 (WHITE로 통일)
        # 핵심 시선: 기준점 초과 여부 → 근방 비교 → 인과 효과 추정
        rdd_def = VGroup(
            Text("기준점을 넘는지 여부로 처치가 결정될 때,", font=FONT, font_size=22, color=WHITE),
            Text("기준점 바로 근방의 개체들을 비교해 인과 효과를 추정", font=FONT, font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.3).next_to(rdd_title, DOWN, buff=0.55)

        self.play(FadeIn(rdd_def, shift=DOWN * 0.15), run_time=0.8)
        self.wait(7.93)  # chunk6 end ~66.64s

        # ── Beat 7 (chunk7: 66.64~78.53s, 11.89s) ───────────
        # 제거: rdd_title + rdd_def (화면 전환)
        # 새로 등장: RCT vs RDD 비교 다이어그램
        # 핵심 시선: 기준점 근방 ≈ 준무작위 배정
        self.play(FadeOut(VGroup(rdd_title, rdd_def)), run_time=0.5)

        # ── RCT 패널 ──
        rct_box = RoundedRectangle(
            corner_radius=0.18, width=4.6, height=3.5,
            fill_color="#111827", fill_opacity=1,
            stroke_color=YELLOW_MAIN, stroke_width=1.5,
        )
        rct_hdr = Text("무작위 실험 (RCT)", font=FONT, font_size=20, color=YELLOW_MAIN)
        rct_hdr.move_to(rct_box.get_top() + DOWN * 0.45)
        coin_c = Circle(radius=0.38, stroke_color=YELLOW_MAIN, stroke_width=2.5).set_fill("#1F2937", opacity=1)
        coin_q = Text("?", font=FONT, font_size=26, color=YELLOW_MAIN).move_to(coin_c.get_center())
        coin = VGroup(coin_c, coin_q)
        rct_groups = VGroup(
            Text("처치군", font=FONT, font_size=18, color=GREEN_MAIN),
            Text("|", font=FONT, font_size=18, color=GRAY_MID),
            Text("통제군", font=FONT, font_size=18, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.35)
        rct_note = Text("직접 무작위 배정", font=FONT, font_size=15, color=GRAY_MID)
        rct_inner = VGroup(coin, rct_groups, rct_note).arrange(DOWN, buff=0.3)
        rct_inner.move_to(rct_box.get_center() + DOWN * 0.2)
        rct_panel = VGroup(rct_box, rct_hdr, rct_inner).move_to(LEFT * 3.2)

        # ── 가운데 ≈ ──
        approx_sign = Text("≈", font=FONT, font_size=52, color=WHITE)

        # ── RDD 패널 (미니 그래프 포함) ──
        rdd_box = RoundedRectangle(
            corner_radius=0.18, width=4.6, height=3.5,
            fill_color="#111827", fill_opacity=1,
            stroke_color=BLUE_MAIN, stroke_width=1.5,
        )
        rdd_hdr = Text("자연 실험 (RDD)", font=FONT, font_size=20, color=BLUE_MAIN)
        rdd_hdr.move_to(rdd_box.get_top() + DOWN * 0.45)
        mini_axis   = Line(LEFT * 1.35, RIGHT * 1.35, color=GRAY_MID, stroke_width=2)
        mini_cutoff = DashedLine(DOWN * 0.32, UP * 0.32, color=YELLOW_MAIN, stroke_width=2, dash_length=0.1)
        mini_near   = Rectangle(
            width=0.6, height=0.64,
            fill_color=GREEN_MAIN, fill_opacity=0.22,
            stroke_color=GREEN_MAIN, stroke_width=1.5,
        )
        mini_near_lbl   = Text("근방", font=FONT, font_size=12, color=GREEN_MAIN).next_to(mini_near, UP, buff=0.06)
        mini_cutoff_lbl = Text("70점", font=FONT, font_size=12, color=YELLOW_MAIN).next_to(mini_cutoff, DOWN, buff=0.27)
        mini_diagram = VGroup(mini_axis, mini_cutoff, mini_near, mini_near_lbl, mini_cutoff_lbl)
        rdd_groups = VGroup(
            Text("통제군 (<70)", font=FONT, font_size=15, color=RED_MAIN),
            Text("처치군 (≥70)", font=FONT, font_size=15, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.55)
        rdd_note = Text("기준점 근방 ≈ 무작위 배정", font=FONT, font_size=16, color=GREEN_MAIN)
        rdd_inner = VGroup(mini_diagram, rdd_groups, rdd_note).arrange(DOWN, buff=0.28)
        rdd_inner.move_to(rdd_box.get_center() + DOWN * 0.2)
        rdd_panel = VGroup(rdd_box, rdd_hdr, rdd_inner).move_to(RIGHT * 3.2)

        self.play(
            FadeIn(rct_panel, shift=LEFT * 0.3),
            FadeIn(approx_sign),
            FadeIn(rdd_panel, shift=RIGHT * 0.3),
            run_time=0.9,
        )
        self.wait(10.49)  # chunk7 end ~78.53s

        # ── Beat 8 (chunk8: 78.53~89.63s, 11.10s) ───────────
        # 제거: 비교 다이어그램
        # 새로 등장: 적용 사례 4행 테이블
        # 핵심 시선: 4가지 적용 맥락
        self.play(
            FadeOut(VGroup(rct_panel, approx_sign, rdd_panel)),
            run_time=0.6,
        )

        header = ["상황", "Running Variable", "Cutoff", "처치"]
        rows = [
            ["장학금 기준 점수", "수능 점수",  "370점",      "장학금 수혜"],
            ["복지 수급 자격",   "소득 수준",  "기준 중위소득 50%", "급여 지원"],
            ["음주 허용 나이",   "나이",       "만 19세",    "주류 구매 허용"],
            ["의약품 보험 적용", "약 값",      "특정 기준 가격", "보험 급여 적용"],
        ]

        table = self._make_table(header, rows)
        table_title = Text("RDD를 적용할 수 있는 상황들", font=FONT, font_size=28, color=BLUE_MAIN)
        table_group = VGroup(table_title, table).arrange(DOWN, buff=0.35).scale(0.78).move_to(ORIGIN)

        self.play(FadeIn(table_group, shift=UP * 0.3), run_time=1.0)
        self.wait(9.5)  # chunk8 end ~89.63s

        # ── Beat 9 (chunk9: 89.63~95.29s, 5.67s) ────────────
        # 남는 요소: table_group
        # 새로 등장: 마무리 결론 문구
        # 핵심 시선: "명확한 규칙 → 어디서든 적용 가능"
        conclusion = Text(
            "명확한 규칙으로 처치가 결정된다면 어디서든 적용을 고려해볼 수 있습니다",
            font=FONT, font_size=19, color=YELLOW_MAIN,
        ).next_to(table_group, DOWN, buff=0.4)

        self.play(FadeIn(conclusion, shift=UP * 0.15), run_time=0.6)
        self.wait(5.37)  # chunk9 + tail

    # ── 헬퍼 ─────────────────────────────────────────────────

    def _student_card(self, score: str, name: str, color: str) -> VGroup:
        box = RoundedRectangle(
            corner_radius=0.2, width=3.2, height=2.2,
            fill_color=GRAY_LIGHT, fill_opacity=1,
            stroke_color=color, stroke_width=3,
        )
        score_text = Text(score, font=FONT, font_size=48, color=color)
        name_text  = Text(name,  font=FONT, font_size=22, color=GRAY_DARK)
        content = VGroup(score_text, name_text).arrange(DOWN, buff=0.2)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def _badge(self, label: str, color: str) -> VGroup:
        bg = RoundedRectangle(
            corner_radius=0.15, width=2.4, height=0.6,
            fill_color=color, fill_opacity=0.15,
            stroke_color=color, stroke_width=2,
        )
        txt = Text(label, font=FONT, font_size=22, color=color)
        txt.move_to(bg.get_center())
        return VGroup(bg, txt)

    def _make_table(self, header: list, rows: list) -> VGroup:
        col_widths    = [3.2, 3.0, 3.2, 3.2]
        row_height    = 0.82
        header_height = 0.98
        all_rows      = [header] + rows
        n_cols        = len(header)
        n_rows        = len(all_rows)

        HEADER_BG = "#1A3A6E"
        ODD_BG    = "#EBF5FF"   # 연한 파란 줄무늬

        cells = VGroup()
        for r_idx, row in enumerate(all_rows):
            is_header = r_idx == 0
            h = header_height if is_header else row_height
            for c_idx, cell_text in enumerate(row):
                w = col_widths[c_idx]
                bg_color = HEADER_BG if is_header else (ODD_BG if r_idx % 2 == 1 else WHITE)
                # 세로 테두리 제거 — 가로선만 남겨 스프레드시트 느낌 탈피
                bg = Rectangle(
                    width=w, height=h,
                    fill_color=bg_color, fill_opacity=1,
                    stroke_width=0,
                )
                if is_header:
                    txt_color  = WHITE
                    txt_font   = "Apple SD Gothic Neo"
                    txt_weight = BOLD
                elif c_idx == 0:
                    txt_color  = BLUE_MAIN   # 상황 컬럼 강조
                    txt_font   = "Apple SD Gothic Neo"
                    txt_weight = BOLD
                else:
                    txt_color  = GRAY_DARK
                    txt_font   = FONT
                    txt_weight = NORMAL
                txt = Text(cell_text, font=txt_font, font_size=17,
                           color=txt_color, weight=txt_weight)
                txt.move_to(bg.get_center())
                if txt.width > w - 0.28:
                    txt.scale((w - 0.28) / txt.width)
                cells.add(VGroup(bg, txt))

        row_groups = VGroup()
        for r_idx in range(n_rows):
            row_vg = VGroup(*[cells[r_idx * n_cols + c] for c in range(n_cols)])
            row_vg.arrange(RIGHT, buff=0)
            row_groups.add(row_vg)
        row_groups.arrange(DOWN, buff=0)

        # 가로 구분선 — 헤더 아래는 BLUE_MAIN, 행 사이는 연한 회색
        dividers = VGroup()
        lx = row_groups.get_left()[0]
        rx = row_groups.get_right()[0]
        for r_idx in range(n_rows - 1):
            y = row_groups[r_idx].get_bottom()[1]
            is_header_sep = r_idx == 0
            dividers.add(Line(
                [lx, y, 0], [rx, y, 0],
                color=BLUE_MAIN if is_header_sep else "#CBD5E1",
                stroke_width=2.0 if is_header_sep else 0.8,
            ))

        # 외곽 테두리
        outer = RoundedRectangle(
            corner_radius=0.20,
            width=row_groups.width + 0.16,
            height=row_groups.height + 0.16,
            fill_opacity=0,
            stroke_color=BLUE_MAIN,
            stroke_width=2.2,
        ).move_to(row_groups.get_center())

        return VGroup(outer, row_groups, dividers)
