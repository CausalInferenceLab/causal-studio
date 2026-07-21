from manim import *

BLUE_MAIN   = "#3B82F6"
RED_MAIN    = "#EF4444"
GRAY_DARK   = "#374151"
GRAY_MID    = "#9CA3AF"
GRAY_LIGHT  = "#F3F4F6"
GREEN_MAIN  = "#22C55E"
YELLOW_MAIN = "#EAB308"
WHITE       = "#FFFFFF"

FONT = "AppleGothic"


class Scene01RddIntro(Scene):
    """
    Scene 01: rdd_intro
    스크립트: videos/rdd/src/scripts/01_rdd_intro.txt
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


class Scene02SharpVsFuzzy(Scene):
    """
    Scene 02: sharp_vs_fuzzy
    build/audio/02_sharp_vs_fuzzy.timings.json 기준 타이밍 (총 50.71s)

    Beat1 chunk1  ( 0.00~ 5.34s)  소개 타이틀 (5.34s)
    Beat2 chunk2  ( 5.34~20.39s)  Sharp RDD 그래프 — 0→1 완전 점프 (15.05s)
    Beat3 chunk3  (20.39~43.19s)  Fuzzy RDD 그래프 — 꺾임형 부분 점프 (22.80s)
    Beat4 chunk4  (43.19~50.71s)  요약: Sharp RDD 중심 + 별도 영상 예고 (7.52s)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~5.34s) ────────────────────────
        # 새로 등장: 소개 타이틀
        # 핵심 시선: "Sharp vs Fuzzy"
        # 지워질 요소: FadeOut → Beat2
        intro = VGroup(
            Text("RDD의 두 가지 형태", font=FONT, font_size=38, color=WHITE),
            VGroup(
                Text("Sharp", font=FONT, font_size=34, color=BLUE_MAIN),
                Text(" vs ", font=FONT, font_size=34, color=WHITE),
                Text("Fuzzy", font=FONT, font_size=34, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(intro[0], shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(intro[1], shift=UP * 0.2), run_time=0.8)
        self.wait(3.24)
        self.play(FadeOut(intro), run_time=0.5)  # chunk1 end ~5.34s

        # ── Beat 2 (chunk2: 5.34~20.39s, 15.05s) ────────────
        # 새로 등장: Sharp RDD 제목 + 처치확률 그래프 (완전 0→1 점프)
        # 핵심 시선: 기준점에서 처치 확률이 0→1로 완전 결정
        # 지워질 요소: FadeOut → Beat3
        sharp_title = Text("Sharp Design", font=FONT, font_size=36, color=BLUE_MAIN)
        sharp_desc  = Text(
            "기준점을 넘으면 처치 확률이 0 → 1로 완전히 결정",
            font=FONT, font_size=22, color=WHITE,
        )
        sharp_header = VGroup(sharp_title, sharp_desc).arrange(DOWN, buff=0.3).move_to(UP * 2.8)

        axes_s, step_s, cutoff_s = self._make_sharp_graph()
        graph_s = VGroup(axes_s, step_s, cutoff_s).scale(0.9).move_to(DOWN * 0.3)

        self.play(FadeIn(sharp_header, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(axes_s), run_time=0.8)
        self.play(Create(cutoff_s), run_time=0.5)
        self.play(Create(step_s), run_time=1.0)
        self.wait(11.95)  # chunk2 end ~20.39s

        # ── Beat 3 (chunk3: 20.39~43.19s, 22.80s) ───────────
        # 제거: Sharp 내용
        # 새로 등장: Fuzzy RDD 제목 + 꺾임형 처치확률 그래프 (부분 점프)
        # 핵심 시선: 기준점에서 뛰어오르지만 0→1이 아님, 좌우 기울기가 꺾임
        self.play(FadeOut(VGroup(sharp_header, graph_s)), run_time=0.6)

        fuzzy_title = Text("Fuzzy Design", font=FONT, font_size=36, color=RED_MAIN)
        fuzzy_desc  = Text(
            "기준점에서 처치 확률이 뛰어오르지만, 0 → 1이 아님",
            font=FONT, font_size=22, color=WHITE,
        )
        fuzzy_header = VGroup(fuzzy_title, fuzzy_desc).arrange(DOWN, buff=0.3).move_to(UP * 2.8)

        axes_f, step_f, cutoff_f = self._make_fuzzy_graph()
        graph_f = VGroup(axes_f, step_f, cutoff_f).scale(0.9).move_to(DOWN * 0.3)

        self.play(FadeIn(fuzzy_header, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(axes_f), run_time=0.8)
        self.play(Create(cutoff_f), run_time=0.5)
        self.play(Create(step_f), run_time=1.2)
        self.wait(18.90)  # chunk3 end ~43.19s

        # ── Beat 4 (chunk4: 43.19~50.71s, 7.52s) ───────────
        # 제거: Fuzzy 내용
        # 새로 등장: 요약 (Sharp RDD 중심)
        # 핵심 시선: "이 영상은 Sharp RDD 중심, Fuzzy는 별도 영상"
        self.play(FadeOut(VGroup(fuzzy_header, graph_f)), run_time=0.6)

        summary = VGroup(
            Text("이 영상의 초점", font=FONT, font_size=26, color=WHITE),
            Text("Sharp RDD", font=FONT, font_size=52, color=BLUE_MAIN),
            Text("Fuzzy RDD → 별도 영상에서", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)

        self.play(FadeIn(summary, shift=UP * 0.3), run_time=0.8)
        self.wait(6.12)  # chunk4 + tail

    # ── 헬퍼 ─────────────────────────────────────────────────

    def _make_axes(self):
        """Sharp/Fuzzy 공통 축 (x: 340~400, 기준점 370점)"""
        axes = Axes(
            x_range=[340, 401, 10],
            y_range=[-0.15, 1.35, 0.5],
            x_length=7.5,
            y_length=4.0,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_tip": False},
            x_axis_config={"numbers_to_include": [350, 360, 370, 380, 390]},
            y_axis_config={"numbers_to_include": [0, 0.5, 1]},
        )
        x_title = Text("수능 점수 (점)", font=FONT, font_size=18, color=WHITE).next_to(
            axes.x_axis.get_right(), RIGHT, buff=0.12
        )
        y_title = (
            Text("처치 확률", font=FONT, font_size=16, color=WHITE)
            .rotate(PI / 2)
            .next_to(axes.y_axis.get_top(), UP, buff=0.1)
        )
        cutoff_line = DashedLine(
            axes.c2p(370, -0.05), axes.c2p(370, 1.2),
            color=YELLOW_MAIN, dash_length=0.12, stroke_width=2.5,
        )
        cutoff_label = Text("Cutoff (370점)", font=FONT, font_size=16, color=YELLOW_MAIN).next_to(
            axes.c2p(370, 1.2), UP, buff=0.05
        )
        return VGroup(axes, x_title, y_title), VGroup(cutoff_line, cutoff_label), axes

    def _make_sharp_graph(self):
        """Sharp RDD: 처치 확률이 370점에서 0→1로 완전 점프 (수평선 + 수직 점프)"""
        axes_vg, cutoff_vg, axes = self._make_axes()
        left_line  = Line(axes.c2p(340, 0.0), axes.c2p(370, 0.0), color=RED_MAIN,  stroke_width=5)
        right_line = Line(axes.c2p(370, 1.0), axes.c2p(400, 1.0), color=BLUE_MAIN, stroke_width=5)
        jump_line  = Line(axes.c2p(370, 0.0), axes.c2p(370, 1.0), color=GRAY_MID,  stroke_width=2, stroke_opacity=0.7)
        dot_open   = Circle(radius=0.10, color=RED_MAIN,  fill_opacity=0, stroke_width=3).move_to(axes.c2p(370, 0.0))
        dot_closed = Dot(axes.c2p(370, 1.0), radius=0.10, color=BLUE_MAIN, fill_opacity=1)
        step_vg = VGroup(left_line, right_line, jump_line, dot_open, dot_closed)
        return axes_vg, step_vg, cutoff_vg

    def _make_fuzzy_graph(self):
        """Fuzzy RDD: 기준점에서 꺾이듯 부분 점프 (0.2→0.7), 좌우 기울기 다름"""
        axes_vg, cutoff_vg, axes = self._make_axes()
        # 왼쪽: 완만한 상승 추세 (340에서 0.1, 370에서 0.2)
        left_line  = axes.plot(
            lambda x: 0.1 + (0.2 - 0.1) / 30 * (x - 340),
            x_range=[340, 370], color=RED_MAIN, stroke_width=5,
        )
        # 오른쪽: 점프 후 더 가파른 상승 추세 (370에서 0.7, 400에서 0.85)
        right_line = axes.plot(
            lambda x: 0.7 + (0.85 - 0.7) / 30 * (x - 370),
            x_range=[370, 400], color=BLUE_MAIN, stroke_width=5,
        )
        jump_line  = DashedLine(
            axes.c2p(370, 0.2), axes.c2p(370, 0.7),
            color=GRAY_MID, stroke_width=2, dash_length=0.1, stroke_opacity=0.8,
        )
        dot_open   = Circle(radius=0.10, color=RED_MAIN,  fill_opacity=0, stroke_width=3).move_to(axes.c2p(370, 0.2))
        dot_closed = Dot(axes.c2p(370, 0.7), radius=0.10, color=BLUE_MAIN, fill_opacity=1)
        step_vg = VGroup(left_line, right_line, jump_line, dot_open, dot_closed)
        return axes_vg, step_vg, cutoff_vg


class Scene03KeyAssumptions(Scene):
    """
    Scene 03: key_assumptions
    build/audio/03_key_assumptions.timings.json 기준 타이밍 (총 90.00s)

    Beat1 chunk1   ( 0.00~18.62s)  소개 타이틀 + 신용점수 예시 설정 플로우
    Beat2 chunk2   (18.62~40.12s)  가정1: 연속성 — 신용점수 그래프 + jump arrow
    Beat3 chunk3   (40.12~64.78s)  연속성 위반 — 집/아파트 비교 패널
    Beat4 chunk4   (64.78~72.12s)  가정2: 국소 무작위성
    Beat5 chunk5   (72.12~90.00s)  조작(manipulation) 경고
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~18.62s, 18.62s) ───────────────
        title = Text("RDD의 핵심 가정", font=FONT, font_size=40, color=WHITE).move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.wait(3.0)
        self.play(FadeOut(title), run_time=0.6)

        # 예시 설정 플로우: 신용점수 → 대출 → 주택 구매율
        setup_lbl = Text("이번 예시", font=FONT, font_size=20, color=GRAY_MID).move_to(UP * 2.8)

        def _box(txt1, txt2, fill, stroke):
            bg = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.0,
                fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=1.5)
            body = VGroup(
                Text(txt1, font=FONT, font_size=18, color=WHITE),
                Text(txt2, font=FONT, font_size=13, color=GRAY_MID),
            ).arrange(DOWN, buff=0.06).move_to(bg.get_center())
            return VGroup(bg, body)

        rv_box    = _box("신용점수", "(Running Variable)", "#1e3a5f", BLUE_MAIN)
        treat_box = _box("주택담보대출 승인", "(Treatment)",       "#1a3a2a", GREEN_MAIN)
        out_box   = _box("주택 구매율", "(Outcome)",           "#3a1a1a", RED_MAIN)

        arr1 = Arrow(ORIGIN, RIGHT * 0.6, color=YELLOW_MAIN, stroke_width=2.5,
                     max_tip_length_to_length_ratio=0.35)
        arr2 = Arrow(ORIGIN, RIGHT * 0.6, color=WHITE, stroke_width=2.5,
                     max_tip_length_to_length_ratio=0.35)

        flow = VGroup(rv_box, arr1, treat_box, arr2, out_box).arrange(RIGHT, buff=0.25).move_to(ORIGIN)
        flow_all = VGroup(setup_lbl, flow)

        self.play(FadeIn(setup_lbl), FadeIn(rv_box), run_time=0.6)
        self.play(Create(arr1), run_time=0.4)
        self.play(FadeIn(treat_box), run_time=0.5)
        self.play(Create(arr2), run_time=0.4)
        self.play(FadeIn(out_box), run_time=0.5)
        # 0.8+3.0+0.6+0.6+0.4+0.5+0.4+0.5 = 6.8s
        self.wait(11.2)
        self.play(FadeOut(flow_all), run_time=0.6)  # ~18.62s

        # ── Beat 2 (chunk2: 22.06~42.77s, 20.71s) ────────────
        header1 = VGroup(
            Text("가정 1", font=FONT, font_size=22, color=WHITE),
            Text("연속성 (Continuity)", font=FONT, font_size=34, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.4).move_to(UP * 3.0)

        axes = Axes(
            x_range=[648, 752, 10],
            y_range=[0, 70, 10],
            x_length=8,
            y_length=4,
            axis_config={"color": WHITE, "include_tip": False},
            x_axis_config={"numbers_to_include": [660, 680, 700, 720, 740]},
            y_axis_config={"numbers_to_include": [10, 20, 30, 40, 50, 60]},
        )
        x_lbl = Text("신용점수 (점)", font=FONT, font_size=18, color=WHITE).next_to(
            axes.x_axis.get_right(), RIGHT, buff=0.12
        )
        y_lbl = (
            Text("주택 구매율 (%)", font=FONT, font_size=15, color=WHITE)
            .rotate(PI / 2)
            .next_to(axes.y_axis.get_top(), UP, buff=0.08)
        )

        y0_fn = lambda x: 10 + (x - 650) * 0.3   # 650→10%, 700→25%
        y1_fn = lambda x: y0_fn(x) + 20            # 700→45%, 750→60%

        y0_obs = axes.plot(y0_fn, x_range=[650, 700], color=RED_MAIN,  stroke_width=4.5)
        y1_obs = axes.plot(y1_fn, x_range=[700, 750], color=BLUE_MAIN, stroke_width=4.5)
        y0_cf  = axes.plot(y0_fn, x_range=[700, 750], color=RED_MAIN,  stroke_width=2.5, stroke_opacity=0.35)
        y1_cf  = axes.plot(y1_fn, x_range=[650, 700], color=BLUE_MAIN, stroke_width=2.5, stroke_opacity=0.35)
        y0_tag = Text("처치 X (대출 불가)", font=FONT, font_size=15, color=RED_MAIN).next_to(
            axes.c2p(665, y0_fn(665)), UP, buff=0.12
        )
        y1_tag = Text("처치 O (대출 승인)", font=FONT, font_size=15, color=BLUE_MAIN).next_to(
            axes.c2p(735, y1_fn(735)), UP, buff=0.12
        )
        cutoff_ln  = DashedLine(axes.c2p(700, 0), axes.c2p(700, 65), color=YELLOW_MAIN, stroke_width=2.5)
        cutoff_lbl = Text("Cutoff (700점)", font=FONT, font_size=14, color=YELLOW_MAIN).next_to(
            axes.c2p(700, 65), UP, buff=0.05
        )
        jump_arrow = DoubleArrow(
            axes.c2p(700, y0_fn(700) + 1), axes.c2p(700, y1_fn(700) - 1),
            color=GREEN_MAIN, buff=0, stroke_width=3, tip_length=0.15,
        )
        jump_tag = Text("처치 효과", font=FONT, font_size=18, color=GREEN_MAIN).next_to(
            jump_arrow, RIGHT, buff=0.12
        )

        graph_base = VGroup(axes, x_lbl, y_lbl, y0_obs, y1_obs, y0_cf, y1_cf,
                            y0_tag, y1_tag, cutoff_ln, cutoff_lbl)
        jump_vg    = VGroup(jump_arrow, jump_tag)
        VGroup(graph_base, jump_vg).scale(0.82).move_to(DOWN * 0.3)

        self.play(FadeIn(header1, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=0.8)
        self.play(Create(cutoff_ln), FadeIn(cutoff_lbl), run_time=0.5)
        self.play(Create(y0_obs), Create(y1_obs), run_time=0.8)
        self.play(FadeIn(y0_cf), FadeIn(y1_cf), FadeIn(y0_tag), FadeIn(y1_tag), run_time=0.6)
        self.wait(9.0)
        self.play(Create(jump_arrow), FadeIn(jump_tag), run_time=0.8)
        self.wait(8.2)  # chunk2 end ~40.12s

        # ── Beat 3 (chunk3: 42.77~67.85s, 25.08s) ────────────
        self.play(FadeOut(VGroup(graph_base, jump_vg)), run_time=0.7)

        viol_title = Text("만약 이 조건이 깨진다면?", font=FONT, font_size=24, color=RED_MAIN)
        viol_title.next_to(header1, DOWN, buff=0.25)

        # ─ 왼쪽 패널: 700점 미만 ─
        apt  = self._make_apartment_icon(color=GREEN_MAIN, size=1.1)
        l_body = VGroup(
            Text("신용점수 700점 미만", font=FONT, font_size=17, color=GREEN_MAIN),
            apt,
            Text("✓ 공공임대 신청 가능", font=FONT, font_size=17, color=GREEN_MAIN),
            Text("✗ 주택담보대출 불가", font=FONT, font_size=17, color=RED_MAIN),
        ).arrange(DOWN, buff=0.22)
        l_bg = RoundedRectangle(corner_radius=0.18, width=4.0, height=3.7,
            fill_color="#0d1f0f", fill_opacity=1, stroke_color=GREEN_MAIN, stroke_width=1.5)
        l_bg.move_to(l_body.get_center())
        left_panel = VGroup(l_bg, l_body).move_to(LEFT * 3.1 + DOWN * 0.4)

        # ─ 오른쪽 패널: 700점 이상 ─
        house = self._make_house_icon(color=BLUE_MAIN, size=1.1)
        r_body = VGroup(
            Text("신용점수 700점 이상", font=FONT, font_size=17, color=BLUE_MAIN),
            house,
            Text("✓ 주택담보대출 승인", font=FONT, font_size=17, color=GREEN_MAIN),
            Text("✗ 공공임대 자격 상실", font=FONT, font_size=17, color=RED_MAIN),
        ).arrange(DOWN, buff=0.22)
        r_bg = RoundedRectangle(corner_radius=0.18, width=4.0, height=3.7,
            fill_color="#0d0f1f", fill_opacity=1, stroke_color=BLUE_MAIN, stroke_width=1.5)
        r_bg.move_to(r_body.get_center())
        right_panel = VGroup(r_bg, r_body).move_to(RIGHT * 3.1 + DOWN * 0.4)

        # ─ 중앙 기준선 ─
        c_line = DashedLine(UP * 1.6, DOWN * 2.4, color=YELLOW_MAIN, stroke_width=2, dash_length=0.14)
        c_lbl  = Text("700점", font=FONT, font_size=20, color=YELLOW_MAIN).next_to(c_line, UP, buff=0.1)

        # ─ 하단 질문 ─
        question = Text(
            "주택 구매율 상승 = 대출 효과?  임대자격 소멸 효과?",
            font=FONT, font_size=19, color=WHITE,
        ).move_to(DOWN * 3.0)

        self.play(FadeIn(viol_title, shift=DOWN * 0.15), run_time=0.6)
        self.play(
            FadeIn(left_panel,  shift=RIGHT * 0.25),
            FadeIn(right_panel, shift=LEFT  * 0.25),
            run_time=0.8,
        )
        self.play(Create(c_line), FadeIn(c_lbl), run_time=0.5)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.5)
        self.wait(21.6)  # chunk3 end ~64.78s

        # ── Beat 4 (chunk4: 67.85~74.77s, 6.92s) ────────────
        self.play(
            FadeOut(VGroup(header1, viol_title, left_panel, right_panel, c_line, c_lbl, question)),
            run_time=0.7,
        )

        header2 = VGroup(
            Text("가정 2", font=FONT, font_size=22, color=WHITE),
            Text("국소 무작위성", font=FONT, font_size=34, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.4).move_to(UP * 1.5)

        local_body2 = VGroup(
            Text("개체가 기준점을 의도적으로 넘을 수 없어야 한다", font=FONT, font_size=22, color=WHITE),
            Text("→ 기준점 근방에서 준무작위 배정이 성립", font=FONT, font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.5)

        self.play(FadeIn(header2, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(local_body2[0], shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(local_body2[1], shift=UP * 0.2), run_time=0.6)
        self.wait(4.6)  # chunk4 end ~72.12s

        # ── Beat 5 (chunk5: 72.12~90.00s, 17.88s) ────────────
        self.play(FadeOut(VGroup(header2, local_body2)), run_time=0.7)

        warning = VGroup(
            Text("조작 (Manipulation)", font=FONT, font_size=36, color=RED_MAIN),
            Text("690점대 고객이 금융감독원 민원으로 점수를 강제로 올리거나", font=FONT, font_size=20, color=WHITE),
            Text("은행 담당자가 특정 고객 점수를 의도적으로 조정한다면", font=FONT, font_size=20, color=WHITE),
            Text("준무작위성이 위배됩니다", font=FONT, font_size=26, color=RED_MAIN),
            Text("→ 분석 전 반드시 확인", font=FONT, font_size=28, color=YELLOW_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        self.play(FadeIn(warning[0], shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(warning[1], shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(warning[2], shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(warning[3], shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(warning[4], shift=UP * 0.1), run_time=0.5)
        self.wait(14.4)  # chunk5 end ~90.00s + tail

    # ── 헬퍼 ──────────────────────────────────────────────────

    def _make_house_icon(self, color=BLUE_MAIN, size=1.0):
        """집 모양: 직사각형 몸체 + 삼각형 지붕 + 문"""
        body = Rectangle(
            width=size, height=size * 0.65,
            fill_color=color, fill_opacity=0.85, stroke_width=0,
        )
        roof = Polygon(
            np.array([-size / 2, 0, 0]),
            np.array([size / 2,  0, 0]),
            np.array([0, size * 0.5, 0]),
            fill_color=color, fill_opacity=0.95, stroke_width=0,
        ).next_to(body, UP, buff=0)
        door = Rectangle(
            width=size * 0.2, height=size * 0.28,
            fill_color=BLACK, fill_opacity=0.8,
            stroke_color=WHITE, stroke_width=0.5,
        ).move_to(body.get_bottom() + UP * size * 0.14)
        return VGroup(body, roof, door)

    def _make_apartment_icon(self, color=GREEN_MAIN, size=1.0):
        """아파트 모양: 직사각형 + 창문 격자"""
        body = Rectangle(
            width=size * 0.75, height=size * 1.0,
            fill_color=color, fill_opacity=0.85, stroke_width=0,
        )
        windows = VGroup(*[
            Rectangle(
                width=size * 0.15, height=size * 0.13,
                fill_color=YELLOW_MAIN, fill_opacity=0.9, stroke_width=0,
            ).move_to(body.get_center()
                      + RIGHT * (col - 0.5) * size * 0.28
                      + UP   * (1 - row)    * size * 0.27)
            for row in range(3) for col in range(2)
        ])
        return VGroup(body, windows)


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


class Scene05Formula(Scene):
    """
    Scene 05: formula (LATE와 회귀식)
    스크립트: videos/rdd/src/scripts/05_formula.txt
    참조 ipynb: book/rdd/01_rdd_basic_ko.ipynb §5 수식으로 이해하는 RDD (cell 10–11)
    총 길이: 79.05s (레이트 발음 반영 재생성)

    ipynb cell 12 핵심 파라미터:
        β₀=2.0, β₁=0.015, β₂=0.5, β₃=0.005, c=70

    직전 Scene04 마지막 화면: 새 화면 시작
    참조: 3b1b/_2019/clacks/simple_scenes.py — 수식 순서 설명·하이라이트 리듬

    .timings.json → Beat 대응:
      Beat1 chunk1 ( 0.00~ 6.92s) LATE 헤더 + 직관 그래프 (점프=LATE)
      Beat2 chunk2 ( 6.92~19.13s) 그래프(상)+산점도: E[Y|c+]·E[Y|c-] 점 / 수식(하): τ 한 줄
      Beat3 chunk3 (19.13~29.07s) 회귀선 다이어그램 (좌빨/우파/점프)
      Beat4 chunk4 (29.07~31.21s) 회귀식 전체 등장 (상단 고정)
      Beat5 chunk5 (31.21~37.57s) 회귀식 + 소형 그래프 + β₀ 주석
      Beat6 chunk6 (37.57~43.70s) 회귀식 + 소형 그래프 + β₂ 주석
      Beat7 chunk7 (43.70~51.08s) 회귀식 + 소형 그래프 + β₁·β₃ 주석
      Beat8 chunk8 (51.08~60.60s) 그래프+수식 유지 → 좌극한·우극한·τ=β̂₂ 오버레이
      Beat9 chunk9 (60.60~79.05s) 국소적 효과 한계 (수능 370점 예시)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~7.20s) ────────────────────────
        # 새로 등장: LATE 헤더(상) + 직관 그래프(중하, 점프=LATE)
        # 핵심 시선: 기준점에서의 점프 = LATE
        # 지워질 요소: FadeOut → Beat2
        late_header = VGroup(
            Text("LATE", font=FONT, font_size=30, color=BLUE_MAIN),
            Text("Local Average Treatment Effect", font=FONT, font_size=20, color=GRAY_MID),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 2.8)

        ax1, ll1, rl1, cl1 = self._make_rdd_graph(6.5, 3.0, DOWN * 0.2)
        jump1 = Arrow(ax1.c2p(70, 2.0), ax1.c2p(70, 2.5), buff=0,
                      color=YELLOW_MAIN, stroke_width=3, max_tip_length_to_length_ratio=0.22)
        late_lbl = MathTex(r"\text{LATE} = \hat{\tau}", font_size=26, color=YELLOW_MAIN).next_to(jump1, RIGHT, buff=0.12)

        self.play(FadeIn(late_header, shift=DOWN * 0.2), run_time=0.7)
        self.play(Create(ax1), Create(ll1), Create(rl1), run_time=1.0)
        self.play(Create(cl1), GrowArrow(jump1), FadeIn(late_lbl), run_time=0.6)
        self.wait(4.4)
        self.play(FadeOut(VGroup(late_header, ax1, ll1, rl1, cl1, jump1, late_lbl)), run_time=0.5)
        # chunk1 end ~7.20s

        # ── Beat 2 (chunk2: 7.20~20.39s) ────────────────────
        # 제거: Beat1 전부
        # 새로 등장: 그래프+산점도(상) + E[Y|c+]·E[Y|c-] 점 + τ수식(중하) + 연속성 줄글(최하)
        # 핵심 시선: 두 기대값의 차이 = 처치 효과
        ax2, ll2, rl2, cl2 = self._make_rdd_graph(6.0, 2.5, UP * 1.2)

        rng2 = np.random.default_rng(42)
        xs_l = rng2.uniform(42, 68, 14)
        ys_l = 2.0 + 0.015 * (xs_l - 70) + rng2.normal(0, 0.18, 14)
        xs_r = rng2.uniform(72, 98, 14)
        ys_r = 2.5 + 0.02 * (xs_r - 70) + rng2.normal(0, 0.18, 14)
        scatter2 = VGroup(
            *[Dot(ax2.c2p(x, y), color=RED_MAIN, radius=0.045, fill_opacity=0.5)
              for x, y in zip(xs_l, ys_l) if 1.5 <= y <= 4.5],
            *[Dot(ax2.c2p(x, y), color=BLUE_MAIN, radius=0.045, fill_opacity=0.5)
              for x, y in zip(xs_r, ys_r) if 1.5 <= y <= 4.5],
        )

        e_r_dot = Dot(ax2.c2p(70, 2.5), color=BLUE_MAIN, radius=0.09)
        e_r_lbl = MathTex(r"\mathbb{E}[Y \mid X\!=\!c^+]", font_size=20, color=BLUE_MAIN).next_to(e_r_dot, UP + RIGHT, buff=0.05)
        e_l_dot = Dot(ax2.c2p(70, 2.0), color=RED_MAIN, radius=0.09)
        e_l_lbl = MathTex(r"\mathbb{E}[Y \mid X\!=\!c^-]", font_size=20, color=RED_MAIN).next_to(e_l_dot, DOWN + RIGHT, buff=0.05)

        tau_eq = MathTex(
            r"\tau_{SRD} = ",
            r"\mathbb{E}[Y \mid X = c^+]",
            r"\;-\;",
            r"\mathbb{E}[Y \mid X = c^-]",
            font_size=28, color=WHITE,
        )
        tau_eq[1].set_color(BLUE_MAIN)
        tau_eq[3].set_color(RED_MAIN)
        tau_eq.move_to(DOWN * 1.5)

        # 요청 1: 연속성 assumption 줄글로
        assumption_note = Text(
            "앞서 말한 가정이 성립한다면, 이 차이는 순수한 처치 효과라고 볼 수 있다.",
            font=FONT, font_size=20, color=WHITE,
        ).move_to(DOWN * 2.6)

        self.play(Create(ax2), Create(ll2), Create(rl2), Create(cl2),
                  FadeIn(scatter2), run_time=0.8)
        self.play(FadeIn(e_r_dot), FadeIn(e_r_lbl), run_time=0.5)
        self.play(FadeIn(e_l_dot), FadeIn(e_l_lbl), run_time=0.5)
        self.wait(2.0)
        self.play(FadeIn(tau_eq, shift=UP * 0.1), run_time=0.6)
        self.wait(3.5)
        self.play(FadeIn(assumption_note, shift=UP * 0.1), run_time=0.6)
        self.wait(2.04)
        self.play(FadeOut(VGroup(ax2, ll2, rl2, cl2, scatter2,
                                 e_r_dot, e_r_lbl, e_l_dot, e_l_lbl,
                                 tau_eq, assumption_note)), run_time=0.6)
        # chunk2 end ~17.74s (new: 10.54s duration, was 13.19s)

        # ── Beat 3 (chunk3: 17.74~28.10s) ───────────────────
        # 새로 등장: 회귀선 다이어그램 (큰 화면, 절편 차이 = τ̂)
        # 핵심 시선: 기준점 c에서 두 회귀선의 점프
        # 끝: 그래프 FadeOut + 회귀식 가운데 FadeIn 동시 → Beat4로 자연 전환
        ax3, ll3, rl3, cl3 = self._make_rdd_graph(7.0, 4.2, ORIGIN + LEFT * 0.2)
        x_lbl = Text("점수 (X)", font=FONT, font_size=18, color=GRAY_MID).next_to(ax3.x_axis, DOWN, buff=0.2)
        y_lbl = Text("GPA", font=FONT, font_size=18, color=GRAY_MID).next_to(ax3.y_axis, LEFT, buff=0.1)
        jump3 = Arrow(ax3.c2p(70, 2.0), ax3.c2p(70, 2.5), buff=0,
                      color=YELLOW_MAIN, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        jump3_lbl = MathTex(r"\hat{\tau}", font_size=26, color=YELLOW_MAIN).next_to(jump3, RIGHT, buff=0.1)
        lbl_left = Text("미처치", font=FONT, font_size=17, color=RED_MAIN).move_to(ax3.c2p(52, 4.1))
        lbl_right = Text("처치", font=FONT, font_size=17, color=BLUE_MAIN).move_to(ax3.c2p(87, 4.1))

        # Beat4~9에서 사용할 회귀식: center 크기(36pt)로 생성, Beat5에서 위로 이동
        formula = MathTex(
            r"Y_i = ", r"\beta_0", r" + ", r"\beta_1",
            r"(X_i - c) + ", r"\beta_2", r"D_i + ", r"\beta_3",
            r"D_i(X_i - c) + \varepsilon_i",
            font_size=36, color=WHITE,
        ).move_to(ORIGIN)

        self.play(Create(ax3), FadeIn(x_lbl, y_lbl), run_time=1.0)
        self.play(Create(ll3), Create(rl3), run_time=1.0)
        self.play(Create(cl3), GrowArrow(jump3), FadeIn(jump3_lbl), run_time=0.6)
        self.play(FadeIn(lbl_left, lbl_right), run_time=0.4)
        self.wait(6.05)
        # "두 절편의 차이를 측정하면 되겠죠" 끝나자마자 그래프 out + 회귀식 in
        self.play(
            FadeOut(VGroup(ax3, x_lbl, y_lbl, ll3, rl3, cl3,
                           jump3, jump3_lbl, lbl_left, lbl_right)),
            FadeIn(formula, shift=UP * 0.15),
            run_time=0.7,
        )
        # chunk3 end ~30.74s

        # ── Beat 4 (chunk4: 30.74~42.63s) ───────────────────
        # 남는 요소: formula (ORIGIN, 큰 크기) — 시청자가 전체 회귀식을 읽을 수 있도록
        # 비워 두는 구역: 위·아래 (formula가 시선 독점)
        # 핵심 시선: 회귀식 전체 구조 — "이 식을 적합하면 두 직선을 알 수 있다"
        self.wait(11.89)
        # chunk4 end ~42.63s

        # ── Beat 5 (chunk5: 42.63~44.63s) ───────────────────
        # 남는 요소: formula
        # 새로 등장: formula → UP*2.8으로 자연스럽게 이동 + 소형 그래프 등장
        # 핵심 시선: "회귀식을 천천히 살펴봅시다" — 수식이 위로 고정됨
        self.play(
            formula.animate.move_to(UP * 2.8).scale(0.833),  # 36pt → 상단 30pt 상당
            run_time=1.0,
        )
        self.wait(1.0)
        # chunk5 end ~44.63s

        # ── Beats 6~8 공유: 소형 그래프 (formula 아래, 설명 위) ──
        sax, sll, srl, scl = self._make_rdd_graph(6.0, 2.5, DOWN * 0.7)

        # ── Beat 6 (chunk6: 44.63~51.08s) ───────────────────
        # 남는 요소: formula(상단) / 새로: 소형 그래프 + β₀ 주석
        # 핵심 시선: β₀ = 절편값
        b0_dot = Dot(sax.c2p(70, 2.0), color=RED_MAIN, radius=0.10)
        b0_h = DashedLine(sax.c2p(40, 2.0), sax.c2p(70, 2.0),
                          color=BLUE_MAIN, stroke_width=1.5, dash_length=0.08)
        b0_ann_lbl = MathTex(r"\beta_0", font_size=22, color=BLUE_MAIN).next_to(
            b0_h.get_center(), UP, buff=0.1)
        b0_ann = VGroup(b0_dot, b0_h, b0_ann_lbl)

        b0_desc = VGroup(
            MathTex(r"\beta_0", font_size=36, color=BLUE_MAIN),
            Text(": 기준점 바로 아래 기대 결과 (미처치 절편)", font=FONT, font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.6)

        self.play(Create(sax), Create(sll), Create(srl), Create(scl), run_time=0.8)
        self.play(FadeIn(b0_ann), run_time=0.5)
        self.play(formula[1].animate.set_color(BLUE_MAIN), FadeIn(b0_desc), run_time=0.5)
        self.wait(4.15)
        self.play(formula[1].animate.set_color(WHITE), FadeOut(VGroup(b0_ann, b0_desc)), run_time=0.5)
        # chunk6 end ~51.08s

        # ── Beat 7 (chunk7: 51.08~56.98s) ───────────────────
        # 남는 요소: formula + 소형 그래프 / 새로: β₂ 점프 화살표 주석
        # 핵심 시선: β₂ = 점프 = 처치 효과 (이 씬의 핵심)
        b2_arrow = Arrow(sax.c2p(70, 2.0), sax.c2p(70, 2.5), buff=0,
                         color=YELLOW_MAIN, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        b2_ann_lbl = MathTex(r"\beta_2", font_size=22, color=YELLOW_MAIN).next_to(b2_arrow, RIGHT, buff=0.1)
        b2_ann = VGroup(b2_arrow, b2_ann_lbl)

        b2_desc = VGroup(
            MathTex(r"\beta_2", font_size=36, color=YELLOW_MAIN),
            Text(": 기준점에서의 점프 = 처치 효과", font=FONT, font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.6)

        self.play(GrowArrow(b2_arrow), FadeIn(b2_ann_lbl), run_time=0.6)
        self.play(formula[5].animate.set_color(YELLOW_MAIN), FadeIn(b2_desc), run_time=0.5)
        self.wait(4.30)
        self.play(formula[5].animate.set_color(WHITE), FadeOut(VGroup(b2_ann, b2_desc)), run_time=0.5)
        # chunk7 end ~56.98s

        # ── Beat 8 (chunk8: 56.98~64.97s) ───────────────────
        # 남는 요소: formula + 소형 그래프 / 새로: β₁(좌선 점) + β₁+β₃(우선 점) 주석
        # 핵심 시선: 두 선의 기울기 차이 = β₃
        mid_l = Dot(sax.c2p(55, 2.0 + 0.015*(55-70)), color=RED_MAIN, radius=0.08)
        b1_ann_lbl = VGroup(
            MathTex(r"\beta_1", font_size=18, color=RED_MAIN),
            Text("(기울기)", font=FONT, font_size=14, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.05).next_to(mid_l, UP + LEFT, buff=0.05)
        b1_ann = VGroup(mid_l, b1_ann_lbl)

        mid_r = Dot(sax.c2p(85, 2.5 + 0.02*(85-70)), color=BLUE_MAIN, radius=0.08)
        b3_ann_lbl = VGroup(
            MathTex(r"\beta_1\!+\!\beta_3", font_size=18, color=BLUE_MAIN),
            Text("(기울기)", font=FONT, font_size=14, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.05).next_to(mid_r, UP + RIGHT, buff=0.05)
        b3_ann = VGroup(mid_r, b3_ann_lbl)

        b13_desc = VGroup(
            VGroup(
                MathTex(r"\beta_1", font_size=32, color=RED_MAIN),
                Text(": 미처치 기울기", font=FONT, font_size=18, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                MathTex(r"\beta_3", font_size=32, color=BLUE_MAIN),
                Text(": 처치 후 기울기 추가 변화", font=FONT, font_size=18, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.55)

        self.play(FadeIn(b1_ann), FadeIn(b3_ann), run_time=0.7)
        self.play(
            formula[3].animate.set_color(RED_MAIN),
            formula[7].animate.set_color(BLUE_MAIN),
            FadeIn(b13_desc),
            run_time=0.5,
        )
        self.wait(6.29)
        self.play(
            formula[3].animate.set_color(WHITE),
            formula[7].animate.set_color(WHITE),
            FadeOut(VGroup(b1_ann, b3_ann, b13_desc)),
            run_time=0.5,
        )
        # chunk8 end ~64.97s

        # ── Beat 9 (chunk9: 64.97~76.86s) ───────────────────
        # 남는 요소: formula(상단 UP*2.8) + sax 소형 그래프(하단 DOWN*0.7)
        # 새로 등장: limits_group(중상 UP*2.0) + tau_result(중 UP*1.05)
        # 핵심 시선: τ = β̂₂
        limits_group = VGroup(
            MathTex(r"\lim_{x \to c^-} = \beta_0", font_size=24, color=RED_MAIN),
            MathTex(r"\lim_{x \to c^+} = \beta_0 + \beta_2", font_size=24, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.6).move_to(UP * 2.0)

        tau_result = MathTex(
            r"\therefore \quad \hat{\tau}_{SRD} = \hat{\beta}_2",
            font_size=40, color=YELLOW_MAIN,
        ).move_to(UP * 1.5)

        self.play(FadeIn(limits_group, shift=UP * 0.12), run_time=0.7)
        self.play(Write(tau_result), run_time=0.7)
        self.wait(10.49)
        # chunk9 end ~76.86s

        # ── Beat 10 (chunk10: 76.86~92.65s) ─────────────────
        # 제거: sax + formula + limits + tau / 새로: 국소적 효과 경고 + 예시
        # 핵심 시선: RDD는 기준점 근방의 국소적 효과만 추정
        self.play(
            FadeOut(VGroup(sax, sll, srl, scl, formula, limits_group, tau_result)),
            run_time=0.7,
        )

        local_header = Text(
            "국소적 효과 (Local Effect)", font=FONT, font_size=30, color=YELLOW_MAIN,
        ).move_to(UP * 1.8)

        local_desc = Text(
            "RDD는 기준점 근방 개체들에 한정된 효과만 추정합니다.",
            font=FONT, font_size=22, color=WHITE,
        ).move_to(UP * 0.6)

        example_text = VGroup(
            Text("장학금 기준이 수능 370점이라고 했을 때,", font=FONT, font_size=19, color=GRAY_MID),
            Text("200점대 학생들에게 장학금이 어떤 효과를 낼지는 RDD로 알 수 없습니다.", font=FONT, font_size=19, color=GRAY_MID),
        ).arrange(DOWN, buff=0.15).move_to(DOWN * 0.6)

        self.play(FadeIn(local_header, shift=DOWN * 0.2), run_time=0.7)
        self.play(FadeIn(local_desc, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(example_text, shift=UP * 0.1), run_time=0.6)
        self.wait(13.19)  # chunk10 end ~92.65s + tail

    # ── 헬퍼 ─────────────────────────────────────────────────

    def _make_rdd_graph(self, x_length, y_length, position):
        """axes + 좌우 회귀선(β₀=2.0, β₁=0.015, β₂=0.5, β₃=0.005) + cutoff 점선 반환."""
        axes = Axes(
            x_range=[40, 100, 10], y_range=[1.5, 4.5, 1.0],
            x_length=x_length, y_length=y_length,
            axis_config={
                "color": GRAY_MID, "stroke_width": 1.2,
                "include_tip": True, "tip_width": 0.12, "tip_height": 0.12,
            },
        ).move_to(position)
        left_line = axes.plot(
            lambda x: 2.0 + 0.015*(x - 70), x_range=[40, 70],
            color=RED_MAIN, stroke_width=2.5,
        )
        right_line = axes.plot(
            lambda x: 2.5 + 0.02*(x - 70), x_range=[70, 100],
            color=BLUE_MAIN, stroke_width=2.5,
        )
        cutoff = DashedLine(
            axes.c2p(70, 1.5), axes.c2p(70, 4.5),
            color=GRAY_MID, stroke_width=1.2, dash_length=0.1,
        )
        return axes, left_line, right_line, cutoff


class Scene06Visualization(Scene):
    """
    Scene 06: visualization
    스크립트: videos/rdd/src/scripts/06_visualization.txt
    build/audio/06_visualization.timings.json 기준 타이밍 (총 76.72s)

    Beat1 chunk1  ( 0.00~ 4.23s)  타이틀: RDD 시각화
    Beat2 chunk2  ( 4.23~10.59s)  세 가지 정보 소개 (산점도·회귀선·불연속 점프구간)
    Beat3 chunk3  (10.59~19.13s)  산점도 등장 (처치/미처치 색 구분)
    Beat4 chunk4  (19.13~26.56s)  회귀선 등장 (좌·우 독립 추정)
    Beat5 chunk5  (26.56~35.06s)  점프 강조 → 처치 효과
    Beat6 chunk6  (35.06~45.37s)  핵심 확인 + 주의사항 예고 (10.31s)
    Beat7 chunk7  (45.37~61.16s)  기준점 근방만 인과 해석 가능 (15.79s)
    Beat8 chunk8  (61.16~76.44s)  좌우 기울기 달라도 무방 (15.28s)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~4.23s) ────────────────────────
        # 새로 등장: 타이틀 2줄
        # 핵심 시선: "RDD 시각화"
        # 지워질 요소: FadeOut → Beat2
        title = VGroup(
            Text("RDD 시각화", font=FONT, font_size=44, color=WHITE),
            Text("그래프로 직관적으로 이해하기", font=FONT, font_size=26, color=GRAY_MID),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.6)
        self.wait(2.33)
        self.play(FadeOut(title), run_time=0.5)  # chunk1 end ~4.23s

        # ── Beat 2 (chunk2: 4.23~10.59s) ────────────────────
        # 새로 등장: 세 가지 정보 헤더 + 칩 3개 순차 등장
        # 핵심 시선: 산점도·회귀선·불연속 점프구간 세 키워드
        # 지워질 요소: FadeOut → Beat3
        info_header = Text("세 가지 정보", font=FONT, font_size=34, color=WHITE).move_to(UP * 1.3)
        chips = VGroup(
            self._chip("① 산점도", GRAY_MID),
            self._chip("② 회귀선", BLUE_MAIN),
            self._chip("③ 불연속 점프구간", YELLOW_MAIN),
        ).arrange(DOWN, buff=0.35).next_to(info_header, DOWN, buff=0.5)

        self.play(FadeIn(info_header, shift=DOWN * 0.2), run_time=0.6)
        for chip in chips:
            self.play(FadeIn(chip, shift=RIGHT * 0.2), run_time=0.45)
        self.wait(4.0)
        self.play(FadeOut(VGroup(info_header, chips)), run_time=0.5)  # chunk2 end ~10.59s

        # ── 공통 그래프 구성 (Beat3~8 유지) ─────────────────
        # x축: 수능 점수 340~400점, cutoff=370점
        axes = Axes(
            x_range=[340, 401, 10], y_range=[1.5, 4.5, 0.5],
            x_length=8.0, y_length=4.5,
            axis_config={
                "color": GRAY_MID, "stroke_width": 1.2,
                "include_tip": True, "tip_width": 0.12, "tip_height": 0.12,
            },
            x_axis_config={"numbers_to_include": [340, 360, 380, 400]},
            y_axis_config={"numbers_to_include": [2.0, 2.5, 3.0, 3.5, 4.0]},
        ).move_to(RIGHT * 0.3 + UP * 0.4)

        # Y축 레이블: 회전 없이 숫자 왼쪽에 수평 배치
        y_lbl = Text("성적(GPA)", font=FONT, font_size=12, color=GRAY_MID)
        y_lbl.next_to(axes, LEFT, buff=0.1)

        # X축 레이블: 축 아래 중앙
        x_lbl = Text("수능 점수 (점)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_center(), DOWN, buff=0.55)

        cutoff_line = DashedLine(
            axes.c2p(370, 1.5), axes.c2p(370, 4.5),
            color=YELLOW_MAIN, stroke_width=2.5, dash_length=0.12,
        )
        cutoff_lbl = Text("Cutoff (370점)", font=FONT, font_size=14, color=YELLOW_MAIN).next_to(
            axes.c2p(370, 4.5), UR, buff=0.05
        )

        rng = np.random.default_rng(42)
        xs_l = rng.uniform(342, 368, 40)
        ys_l = 2.0 + 0.015 * (xs_l - 370) + rng.normal(0, 0.22, 40)
        xs_r = rng.uniform(372, 398, 40)
        ys_r = 2.5 + 0.02 * (xs_r - 370) + rng.normal(0, 0.22, 40)

        scatter_left = VGroup(*[
            Dot(axes.c2p(x, y), color=RED_MAIN, radius=0.055, fill_opacity=0.75)
            for x, y in zip(xs_l, ys_l) if 1.5 <= y <= 4.5
        ])
        scatter_right = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE_MAIN, radius=0.055, fill_opacity=0.75)
            for x, y in zip(xs_r, ys_r) if 1.5 <= y <= 4.5
        ])

        legend = VGroup(
            VGroup(
                Dot(color=RED_MAIN, radius=0.09),
                Text("미수혜 (<370점)", font=FONT, font_size=16, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                Dot(color=BLUE_MAIN, radius=0.09),
                Text("수혜 (≥370점)", font=FONT, font_size=16, color=BLUE_MAIN),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        legend.move_to(axes.get_corner(UR) + LEFT * 1.6 + DOWN * 0.4)

        # ── Beat 3 (chunk3: 10.59~19.13s) ───────────────────
        # 새로 등장: 축·컷오프·산점도·범례
        # 핵심 시선: 색으로 구분된 두 집단 점들
        # 지워질 요소: 없음 → Beat4에서 회귀선 추가
        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=0.8)
        self.play(Create(cutoff_line), FadeIn(cutoff_lbl), run_time=0.5)
        self.play(FadeIn(scatter_left), run_time=0.7)
        self.play(FadeIn(scatter_right), run_time=0.7)
        self.play(FadeIn(legend), run_time=0.6)
        self.wait(5.84)  # chunk3 end ~19.13s

        # ── Beat 4 (chunk4: 19.13~26.56s) ───────────────────
        # 남는 요소: 축·산점도·범례
        # 새로 등장: 좌우 회귀선 + 하단 설명
        # 핵심 시선: 기준점 좌·우 각각의 독립 회귀선
        # 지워질 요소: reg_desc FadeOut → Beat5
        left_line = axes.plot(
            lambda x: 2.0 + 0.015 * (x - 370), x_range=[340, 370],
            color=RED_MAIN, stroke_width=4.5,
        )
        right_line = axes.plot(
            lambda x: 2.5 + 0.02 * (x - 370), x_range=[370, 400],
            color=BLUE_MAIN, stroke_width=4.5,
        )
        reg_desc = Text(
            "기준점 좌·우에 각각 독립적으로 적합된 회귀선",
            font=FONT, font_size=19, color=WHITE,
        ).move_to(DOWN * 3.0)

        self.play(Create(left_line), run_time=0.8)
        self.play(Create(right_line), run_time=0.8)
        self.play(FadeIn(reg_desc), run_time=0.5)
        self.wait(4.53)  # chunk4 end ~26.56s
        self.play(FadeOut(reg_desc), run_time=0.4)

        # ── Beat 5 (chunk5: 26.56~35.06s) ───────────────────
        # 남는 요소: 축·산점도·범례·회귀선
        # 새로 등장: 점프 화살표 + 처치효과 레이블(MathTex τ̂) + 하단 설명
        # 핵심 시선: 기준점 370에서의 수직 점프 = τ̂
        # 지워질 요소: jump_desc FadeOut → Beat6
        jump_arrow = DoubleArrow(
            axes.c2p(370, 2.05), axes.c2p(370, 2.45),
            color=YELLOW_MAIN, buff=0, stroke_width=4, tip_length=0.18,
        )
        # τ̂ hat 렌더링: Text에서 MathTex 분리로 정확하게 표시
        jump_lbl = VGroup(
            Text("처치 효과 ", font=FONT, font_size=17, color=YELLOW_MAIN),
            MathTex(r"\hat{\tau}", font_size=22, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.08).next_to(jump_arrow, RIGHT, buff=0.15)

        jump_desc = Text(
            "두 회귀선의 절편 차이 = 처치 효과 추정량",
            font=FONT, font_size=19, color=YELLOW_MAIN,
        ).move_to(DOWN * 3.0)

        self.play(Create(jump_arrow), FadeIn(jump_lbl), run_time=0.8)
        self.play(FadeIn(jump_desc), run_time=0.5)
        self.wait(6.8)  # chunk5 end ~35.06s
        self.play(FadeOut(jump_desc), run_time=0.4)

        # ── Beat 6 (chunk6: 35.06~45.37s, 10.31s) ───────────
        # 남는 요소: 축·산점도·범례·회귀선·점프 화살표
        # 새로 등장: 주의 예고 문구 (하단)
        # 핵심 시선: "하지만 주의해야 할 것들이 있습니다"
        # 지워질 요소: caution_hint + jump 관련 → Beat7
        caution_hint = Text(
            "그래프를 볼 때 주의할 것들이 있습니다",
            font=FONT, font_size=20, color=YELLOW_MAIN,
        ).move_to(DOWN * 3.0)

        self.play(FadeIn(caution_hint, shift=UP * 0.15), run_time=0.6)
        self.wait(9.21)  # chunk6 end ~45.37s
        self.play(FadeOut(VGroup(caution_hint, jump_arrow, jump_lbl)), run_time=0.5)

        # ── Beat 7 (chunk7: 45.37~61.16s, 15.79s) ───────────
        # 남는 요소: 축·산점도·범례·회귀선
        # 새로 등장: 근방 강조 구간(초록, 365~375점) + 인과 해석 경고
        # 핵심 시선: 초록 구간 = 인과 해석 가능 / 원거리 점들 = 주의
        # 지워질 요소: near_region·near_lbl·caution_desc → Beat8
        r_l = axes.c2p(365, 1.5)
        r_r = axes.c2p(375, 4.5)
        near_w = r_r[0] - r_l[0]
        near_h = r_r[1] - r_l[1]
        near_cx = (r_l[0] + r_r[0]) / 2
        near_cy = (r_l[1] + r_r[1]) / 2

        near_region = Rectangle(
            width=near_w, height=near_h,
            fill_color=GREEN_MAIN, fill_opacity=0.14,
            stroke_color=GREEN_MAIN, stroke_width=1.8,
        ).move_to([near_cx, near_cy, 0])
        near_lbl = Text("인과 해석\n가능 구간", font=FONT, font_size=14, color=GREEN_MAIN).next_to(
            near_region, DOWN, buff=0.08
        )

        caution_desc = VGroup(
            Text("기준점 근방에서만 인과적 해석이 가능합니다", font=FONT, font_size=19, color=WHITE),
            Text("340점대·390점대 차이 → 장학금 효과가 아닌 능력 차이일 수 있음", font=FONT, font_size=17, color=RED_MAIN),
        ).arrange(DOWN, buff=0.22).move_to(DOWN * 3.0)

        self.play(FadeIn(near_region), FadeIn(near_lbl), run_time=0.7)
        self.play(FadeIn(caution_desc), run_time=0.6)
        self.wait(14.0)  # chunk7 end ~61.16s
        self.play(FadeOut(VGroup(near_region, near_lbl, caution_desc)), run_time=0.5)

        # ── Beat 8 (chunk8: 61.16~76.44s, 15.28s) ───────────
        # 남는 요소: 축·산점도·범례·회귀선
        # 새로 등장: 좌우 기울기 레이블 + 하단 설명
        # 핵심 시선: β₁ (미처치 기울기) vs β₁+β₃ (처치 기울기)
        slope_l_lbl = VGroup(
            Text("기울기: ", font=FONT, font_size=15, color=RED_MAIN),
            MathTex(r"\beta_1", font_size=20, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.08).move_to(axes.c2p(350, 2.0 + 0.015 * (350 - 370) + 0.45))

        slope_r_lbl = VGroup(
            Text("기울기: ", font=FONT, font_size=15, color=BLUE_MAIN),
            MathTex(r"\beta_1 + \beta_3", font_size=20, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.08).move_to(axes.c2p(390, 2.5 + 0.02 * (390 - 370) + 0.48))

        slope_note = VGroup(
            Text("좌우 회귀선의 기울기가 달라도 됩니다", font=FONT, font_size=20, color=BLUE_MAIN),
            Text("처치 여부에 따라 성적 향상 경향이 다를 수 있습니다", font=FONT, font_size=18, color=WHITE),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 3.0)

        self.play(FadeIn(slope_l_lbl), FadeIn(slope_r_lbl), run_time=0.7)
        self.play(FadeIn(slope_note), run_time=0.6)
        self.wait(13.98)  # chunk8 end ~76.44s + tail

    # ── 헬퍼 ─────────────────────────────────────────────────

    def _chip(self, label: str, color: str) -> VGroup:
        bg = RoundedRectangle(
            corner_radius=0.18, width=4.2, height=0.65,
            fill_color=color, fill_opacity=0.12,
            stroke_color=color, stroke_width=1.8,
        )
        txt = Text(label, font=FONT, font_size=22, color=color)
        txt.move_to(bg.get_center())
        return VGroup(bg, txt)


class Scene07Simulation(Scene):
    """
    Scene 07: simulation
    스크립트: videos/rdd/src/scripts/07_simulation.txt
    build/audio/07_simulation.timings.json 기준 타이밍 (총 61.18s)

    Beat1 chunk1  ( 0.00~ 2.09s)  타이틀 (2.09s)
    Beat2 chunk2  ( 2.09~16.49s)  설정 소개: cutoff=370, τ=0.5, N=500 (14.40s)
    Beat3 chunk3  (16.49~35.53s)  500명 산점도 + DGP 공식 (19.04s)
    Beat4 chunk4  (35.53~45.14s)  좌우 회귀선 적합 (9.61s)
    Beat5 chunk5  (45.14~58.28s)  결과: 절편 2.02·2.50, τ̂=0.48 (13.14s)
    Beat6 chunk6  (58.28~64.90s)  마무리: RDD 복원 성공 (6.61s)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~2.09s) ────────────────────────
        title = VGroup(
            Text("시뮬레이션", font=FONT, font_size=44, color=WHITE),
            Text("RDD가 처치 효과를 복원할 수 있을까?", font=FONT, font_size=26, color=GRAY_MID),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.5)
        self.wait(0.59)
        self.play(FadeOut(title), run_time=0.3)  # chunk1 end ~2.09s

        # ── Beat 2 (chunk2: 2.09~15.09s, 13.0s) ────────────
        # 새로 등장: 설정 소개 카드 4개
        # 핵심 시선: cutoff=70, 진짜 τ=0.5, N=500
        # 지워질 요소: FadeOut → Beat3
        setup_header = Text("시뮬레이션 설정", font=FONT, font_size=30, color=WHITE).move_to(UP * 1.7)
        setup_items = VGroup(
            self._setup_row("Cutoff", "370점  (이상 장학금 지급)", YELLOW_MAIN),
            self._setup_row("실제 처치 효과", "학점 0.5점 상승", GREEN_MAIN),
            self._setup_row("표본 크기 N", "500명", BLUE_MAIN),
            self._setup_row("Running Variable", "수능 점수", GRAY_MID),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(setup_header, DOWN, buff=0.45)

        self.play(FadeIn(setup_header, shift=DOWN * 0.15), run_time=0.5)
        for item in setup_items:
            self.play(FadeIn(item, shift=RIGHT * 0.15), run_time=0.4)
        self.wait(10.22)
        self.play(FadeOut(VGroup(setup_header, setup_items)), run_time=0.5)  # chunk2 end ~14.91s

        # ── 공통 그래프 구성 (Beat3~6 유지) ─────────────────
        axes = Axes(
            x_range=[340, 401, 10], y_range=[1.0, 4.0, 0.5],
            x_length=8.5, y_length=4.5,
            axis_config={
                "color": GRAY_MID, "stroke_width": 1.2,
                "include_tip": True, "tip_width": 0.12, "tip_height": 0.12,
            },
            x_axis_config={"numbers_to_include": [340, 350, 360, 370, 380, 390, 400]},
            y_axis_config={"numbers_to_include": [1.5, 2.0, 2.5, 3.0, 3.5]},
        ).move_to(RIGHT * 0.3 + UP * 0.4)

        y_lbl = Text("성적(GPA)", font=FONT, font_size=12, color=GRAY_MID)
        y_lbl.next_to(axes, LEFT, buff=0.1)
        x_lbl = Text("수능 점수 (점)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_center(), DOWN, buff=0.55)

        cutoff_line = DashedLine(
            axes.c2p(370, 1.0), axes.c2p(370, 4.0),
            color=YELLOW_MAIN, stroke_width=2.5, dash_length=0.12,
        )
        cutoff_lbl = Text("Cutoff (370점)", font=FONT, font_size=14, color=YELLOW_MAIN).next_to(
            axes.c2p(370, 4.0), UR, buff=0.05
        )

        rng = np.random.default_rng(42)
        n = 500
        xs = rng.uniform(340, 400, n)
        treated = (xs >= 370).astype(float)
        ys = 2.0 + 0.015 * (xs - 370) + 0.5 * treated + rng.normal(0, 0.3, n)

        scatter_left = VGroup(*[
            Dot(axes.c2p(x, y), color=RED_MAIN, radius=0.04, fill_opacity=0.55)
            for x, y in zip(xs, ys) if x < 370 and 1.0 <= y <= 4.0
        ])
        scatter_right = VGroup(*[
            Dot(axes.c2p(x, y), color=BLUE_MAIN, radius=0.04, fill_opacity=0.55)
            for x, y in zip(xs, ys) if x >= 370 and 1.0 <= y <= 4.0
        ])

        legend = VGroup(
            VGroup(
                Dot(color=RED_MAIN, radius=0.09),
                Text("미수혜 (<370점)", font=FONT, font_size=16, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                Dot(color=BLUE_MAIN, radius=0.09),
                Text("수혜 (≥370점)", font=FONT, font_size=16, color=BLUE_MAIN),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        legend.move_to(axes.get_corner(UR) + LEFT * 1.5 + DOWN * 0.4)

        # ── Beat 3 (chunk3: 15.09~32.09s, 17.0s) ───────────
        # 새로 등장: 축·cutoff·DGP 공식·산점도·범례 순차 등장
        # 핵심 시선: 데이터 생성 공식 → 산점도 등장
        # 지워질 요소: dgp_formula FadeOut → Beat4
        dgp_formula = VGroup(
            MathTex(
                r"y_i = 2.0 + 0.015(x_i - 370) + 0.5 \cdot T_i + \varepsilon_i",
                font_size=26, color=WHITE,
            ),
            MathTex(r"T_i = 1 \;(x_i \geq 370), \quad \varepsilon \sim \mathcal{N}(0,\,0.09)",
                    font_size=16, color=GRAY_MID),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 3.1)

        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=0.8)
        self.play(Create(cutoff_line), FadeIn(cutoff_lbl), run_time=0.5)
        self.play(FadeIn(dgp_formula), run_time=0.7)
        self.play(FadeIn(scatter_left), run_time=2.0)
        self.play(FadeIn(scatter_right), run_time=2.0)
        self.play(FadeIn(legend), run_time=0.5)
        self.wait(11.49)
        self.play(FadeOut(dgp_formula), run_time=0.4)  # chunk3 end ~33.30s

        # ── Beat 4 (chunk4: 32.09~41.70s, 9.61s) ───────────
        # 남는 요소: 축·cutoff·산점도·범례
        # 새로 등장: 좌우 회귀선 + 하단 설명
        # 핵심 시선: 기준점 70에서 좌·우 각각 독립 추정
        # 지워질 요소: reg_desc FadeOut → Beat5
        left_line = axes.plot(
            lambda x: 2.02 + 0.015 * (x - 370), x_range=[340, 370],
            color=RED_MAIN, stroke_width=4.5,
        )
        right_line = axes.plot(
            lambda x: 2.50 + 0.015 * (x - 370), x_range=[370, 400],
            color=BLUE_MAIN, stroke_width=4.5,
        )
        reg_desc = Text(
            "기준점 좌·우에 각각 독립적으로 회귀선 적합",
            font=FONT, font_size=19, color=WHITE,
        ).move_to(DOWN * 3.1)

        self.play(Create(left_line), run_time=0.9)
        self.play(Create(right_line), run_time=0.9)
        self.play(FadeIn(reg_desc), run_time=0.5)
        self.wait(6.91)
        self.play(FadeOut(reg_desc), run_time=0.4)  # chunk4 end ~41.70s

        # ── Beat 5 (chunk5: 41.70~54.57s, 12.87s) ───────────
        # 남는 요소: 축·cutoff·산점도·범례·회귀선
        # 새로 등장: 절편 점 + 레이블 + 점프 화살표 + 결과 박스
        # 핵심 시선: τ̂=0.47 ≈ 0.5 (진짜 처치 효과)
        left_dot = Dot(axes.c2p(370, 2.02), color=RED_MAIN, radius=0.12)
        right_dot = Dot(axes.c2p(370, 2.50), color=BLUE_MAIN, radius=0.12)
        left_dot_lbl = Text("2.02", font=FONT, font_size=18, color=WHITE).next_to(
            axes.c2p(370, 2.02), LEFT, buff=0.14
        )
        right_dot_lbl = Text("2.50", font=FONT, font_size=18, color=WHITE).next_to(
            axes.c2p(370, 2.50), LEFT, buff=0.14
        )

        jump_arrow = DoubleArrow(
            axes.c2p(370, 2.02), axes.c2p(370, 2.50),
            color=YELLOW_MAIN, buff=0, stroke_width=4, tip_length=0.15,
        )
        jump_lbl = VGroup(
            Text("처치 효과 추정 ", font=FONT, font_size=17, color=YELLOW_MAIN),
            MathTex(r"\hat{\tau}", font_size=22, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.08).next_to(jump_arrow, RIGHT, buff=0.15)

        result_desc = VGroup(
            Text("왼쪽 절편: 2.02   |   오른쪽 절편: 2.50", font=FONT, font_size=18, color=WHITE),
            VGroup(
                Text("추정 처치 효과 ", font=FONT, font_size=18, color=YELLOW_MAIN),
                MathTex(r"\hat{\tau} = 0.48", font_size=22, color=YELLOW_MAIN),
                Text("  (실제: τ = 0.5)", font=FONT, font_size=16, color=GREEN_MAIN),
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 3.1)

        self.play(
            FadeIn(left_dot), FadeIn(left_dot_lbl),
            FadeIn(right_dot), FadeIn(right_dot_lbl),
            run_time=0.7,
        )
        self.play(Create(jump_arrow), FadeIn(jump_lbl), run_time=0.7)
        self.play(FadeIn(result_desc), run_time=0.6)
        self.wait(9.84)   # chunk5 end ~54.75s

        # ── Beat 6 (chunk6: 54.57~61.02s, 6.45s) ───────────
        # 남는 요소: 축·산점도·회귀선·점프 화살표
        # 새로 등장: 결론 문구 (초록)
        # 핵심 시선: RDD가 처치 효과를 잘 복원한다
        conclusion = Text(
            "기준점 좌우 회귀식 적합 → RDD로 처치 효과 복원 가능",
            font=FONT, font_size=20, color=GREEN_MAIN,
        ).move_to(DOWN * 3.1)

        self.play(FadeOut(result_desc), FadeIn(conclusion), run_time=0.6)
        self.wait(13.66)  # chunk6 end ~68.93s (mp3 재생성 후 길이 반영)

    def _setup_row(self, key: str, val: str, color: str) -> VGroup:
        return VGroup(
            Text(f"{key}: ", font=FONT, font_size=19, color=GRAY_MID),
            Text(val, font=FONT, font_size=19, color=color),
        ).arrange(RIGHT, buff=0.12)


class Scene08Outro(Scene):
    """
    Scene 08: outro
    스크립트: videos/rdd/src/scripts/08_outro.txt
    build/audio/08_outro.timings.json 기준 타이밍 (총 30.78s)

    Beat1 chunk1  ( 0.00~ 2.51s)  타이틀 "Sharp RDD 핵심 정리" (2.51s)
    Beat2 chunk2  ( 2.51~16.95s)  요약 카드 3개 순차 등장 (14.44s)
                                  — Running Variable/Cutoff, 연속성 가정, β̂₂ = LATE
    Beat3 chunk3  (16.95~24.89s)  Sharp vs Fuzzy 비교 도식 (7.94s)
    Beat4 chunk4  (24.89~30.70s)  "Fuzzy RDD" 예고 타이틀 (5.80s)

    ipynb 범위: 해당 없음 (영상 마무리 + 다음 편 예고)
    참고 3b1b: 없음 — 카드 나열 + 예고 구조
    직전 Scene 마지막 문장: "기준점 좌우 회귀식 적합 → RDD로 처치 효과 복원 가능"
    현재 Scene 첫 문장: "Sharp RDD를 정리해봅시다."
    """

    def _summary_card(self, icon_tex: str, body: str, accent: str) -> VGroup:
        """
        왼쪽 컬러 세로선 + 아이콘 수식 + 본문 텍스트 한 줄짜리 카드.
        icon_tex: LaTeX 수식 문자열, body: 한국어 설명 문자열, accent: 강조색
        """
        bar = Rectangle(width=0.07, height=0.55, fill_opacity=1,
                         fill_color=accent, stroke_width=0).set_stroke(width=0)
        label = MathTex(icon_tex, font_size=22, color=accent)
        desc = Text(body, font=FONT, font_size=18, color=WHITE)
        row = VGroup(label, desc).arrange(RIGHT, buff=0.25)
        return VGroup(bar, row).arrange(RIGHT, buff=0.22)

    def construct(self):
        # ── Beat 1 (chunk1: 0~2.51s) ────────────────────────
        # 새로 등장: 섹션 타이틀
        # 핵심 시선: "Sharp RDD 핵심 정리"
        # 지워질 요소: FadeOut → Beat2
        title = VGroup(
            Text("Sharp RDD", font=FONT, font_size=46, color=WHITE),
            Text("핵심 정리", font=FONT, font_size=28, color=GRAY_MID),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.25), run_time=0.6)
        self.play(FadeIn(title[1], shift=UP * 0.15), run_time=0.5)
        self.wait(1.11)
        self.play(FadeOut(title), run_time=0.3)
        # chunk1 end ~2.51s

        # ── Beat 2 (chunk2: 2.51~16.95s, 14.44s) ────────────
        # 새로 등장: 요약 카드 3개 (상→중→하 순차)
        # 핵심 시선: ① 처치 확정 구조, ② 연속성 가정, ③ β̂₂ = LATE
        # 지워질 요소: FadeOut → Beat3
        card1 = self._summary_card(
            r"X_i \geq c \Rightarrow D_i = 1",
            "기준점 초과 시 처치 확정 (Sharp)",
            YELLOW_MAIN,
        )
        card2 = self._summary_card(
            r"\text{Continuity Assumption}",
            "기준점 근방 → 준무작위 배정",
            BLUE_MAIN,
        )
        card3 = self._summary_card(
            r"\hat{\beta}_2 = \text{LATE}",
            "기준점 점프 크기 = 국소 처치 효과",
            GREEN_MAIN,
        )
        cards = VGroup(card1, card2, card3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        cards.move_to(ORIGIN)

        self.play(FadeIn(card1, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(3.8)
        self.play(FadeIn(card2, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(3.8)
        self.play(FadeIn(card3, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(4.84)
        self.play(FadeOut(cards), run_time=0.5)
        # chunk2 end ~16.95s

        # ── Beat 3 (chunk3: 16.95~24.89s, 7.94s) ────────────
        # 새로 등장: Sharp vs Fuzzy 비교 패널 (좌/우)
        # 핵심 시선: "현실에서는 처치가 확정되지 않는다" → Fuzzy 개념 예고
        # 지워질 요소: FadeOut → Beat4

        # 좌: Sharp 박스
        sharp_box = VGroup(
            Text("Sharp RDD", font=FONT, font_size=20, color=YELLOW_MAIN),
            MathTex(r"D_i = \mathbf{1}(X_i \geq c)", font_size=22, color=WHITE),
            Text("기준점 초과 → 반드시 처치", font=FONT, font_size=16, color=GRAY_MID),
        ).arrange(DOWN, buff=0.22)
        sharp_frame = SurroundingRectangle(sharp_box, color=YELLOW_MAIN,
                                           buff=0.28, corner_radius=0.12, stroke_width=1.5)
        sharp_panel = VGroup(sharp_frame, sharp_box).move_to(LEFT * 3.1)

        # 우: Fuzzy 박스 (물음표 처리)
        fuzzy_box = VGroup(
            Text("Fuzzy RDD", font=FONT, font_size=20, color=BLUE_MAIN),
            MathTex(r"P(D_i{=}1 \mid X_i) \uparrow \text{ at } c",
                    font_size=22, color=WHITE),
            Text("기준점 초과 → 처치 확률 증가", font=FONT, font_size=16, color=GRAY_MID),
        ).arrange(DOWN, buff=0.22)
        fuzzy_frame = SurroundingRectangle(fuzzy_box, color=BLUE_MAIN,
                                           buff=0.28, corner_radius=0.12, stroke_width=1.5)
        fuzzy_panel = VGroup(fuzzy_frame, fuzzy_box).move_to(RIGHT * 3.1)

        vs_lbl = Text("vs", font=FONT, font_size=22, color=GRAY_MID).move_to(ORIGIN)

        self.play(
            FadeIn(sharp_panel, shift=RIGHT * 0.2),
            FadeIn(vs_lbl),
            FadeIn(fuzzy_panel, shift=LEFT * 0.2),
            run_time=0.7,
        )
        self.wait(6.74)
        self.play(FadeOut(VGroup(sharp_panel, vs_lbl, fuzzy_panel)), run_time=0.5)
        # chunk3 end ~24.89s

        # ── Beat 4 (chunk4: 24.89~30.70s, 5.80s) ────────────
        # 새로 등장: Fuzzy RDD 예고 타이틀
        # 핵심 시선: "다음 영상에서"
        next_label = Text("다음 영상에서", font=FONT, font_size=22, color=GRAY_MID)
        fuzzy_title = Text("Fuzzy RDD", font=FONT, font_size=52, color=BLUE_MAIN)
        arrow = Text("→", font=FONT, font_size=30, color=GRAY_MID)
        teaser = VGroup(next_label, fuzzy_title).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(next_label, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(fuzzy_title, shift=UP * 0.25), run_time=0.6)
        self.wait(7.26)
        # chunk4 end ~33.25s
