from manim import *

TEAL_MAIN   = "#4DD0C4"
GOLD_MAIN   = "#C8A630"
GRAY_DARK   = "#374151"
GRAY_MID    = "#9CA3AF"
GRAY_LIGHT  = "#F3F4F6"
GREEN_MAIN  = "#22C55E"
RED_MAIN    = "#EF4444"
YELLOW_MAIN = "#EAB308"
WHITE       = "#FFFFFF"

FONT = "AppleGothic"


class Scene01RecapHook(Scene):
    """
    Scene 01: recap_hook (English port of videos/fuzzy_rdd/src/fuzzy_rdd.py Scene01RecapHook)
    스크립트: src/scripts/01_recap_hook.txt
    타이밍: build/audio/01_recap_hook.timings.json (총 51.51s, 9 chunks)

    한국어 버전과 문단 구조(9 chunks)가 1:1로 대응하고, 모든 wait() 체크포인트가
    청크 경계와 정확히 일치하므로, run_time들은 그대로 두고 wait() 인자만
    영어 오디오의 새 청크 경계 시간으로 교체했다. 시각 구조·색·레이아웃은 원본과 동일.

    Beat1 chunk1-2 ( 0.00~14.54s)  Sharp RDD recap: headline → example + step function graph
    Beat2 chunk3   (14.54~16.90s)  "reality isn't this clean" headline
    Beat3 chunk4-5 (16.90~29.40s)  contrasting real cases: 371(above cutoff, no scholarship) vs 369(below, got it)
    Beat4 chunk6-7 (29.40~40.36s)  generalize → Fuzzy RDD definition (2 lines + name)
    Beat5 chunk8-9 (40.36~51.51s)  Fuzzy RDD graph (partial jump) → closing question (WAIT_TAIL)
    """

    def construct(self):
        # ── Beat 1 (chunk1-2: 0~14.54) ──────────────────────────
        recap_title = VGroup(
            Text("Recap: Last Video", font=FONT, font_size=22, color=GRAY_MID),
            Text("Sharp RDD", font=FONT, font_size=46, color=TEAL_MAIN),
            Text("Cutoff crossed → 100% treatment", font=FONT, font_size=22, color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.6)

        self.play(FadeIn(recap_title, shift=UP * 0.2), run_time=0.7)
        self.wait(5.387 - 0.7)  # chunk1 end

        # chunk2: example (score >= / < 370) + Sharp RDD step function graph
        sharp_label = Text("Sharp RDD", font=FONT, font_size=30, color=TEAL_MAIN)
        example_label = Text("(Example)", font=FONT, font_size=20, color=GRAY_MID)
        example_lines = VGroup(
            Text("Score >= 370 -> gets scholarship", font=FONT, font_size=24, color=TEAL_MAIN),
            Text("Score < 370 -> gets nothing", font=FONT, font_size=24, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        example_group = VGroup(sharp_label, example_label, example_lines).arrange(DOWN, buff=0.25)

        step_graph = self._make_step_graph()
        content2 = VGroup(example_group, step_graph).arrange(DOWN, buff=0.9).move_to(ORIGIN)

        self.play(FadeOut(recap_title, run_time=0.5), FadeIn(content2, shift=UP * 0.15, run_time=0.8))
        self.wait(14.5357 - 5.387 - 0.8)  # chunk2 end

        self.play(FadeOut(content2), run_time=0.5)

        # ── Beat 2 (chunk3: 14.54~16.90) ────────────────────────
        headline2 = Text(
            "But reality isn't this clean", font=FONT, font_size=30, color=WHITE,
        ).move_to(ORIGIN)

        self.play(FadeIn(headline2, shift=UP * 0.2), run_time=0.6)
        self.wait(16.9041 - 14.5357 - 0.5 - 0.6)  # chunk3 end

        # ── Beat 3 (chunk4-5: 16.90~29.40) ──────────────────────
        top_label = Text("Real-World Cases", font=FONT, font_size=22, color=GRAY_MID).to_edge(UP, buff=1.3)

        left_card = self._make_case_card(
            score="371", status="Above cutoff", status_color=TEAL_MAIN,
            result="No scholarship", result_color=RED_MAIN, reason="Missed deadline",
        ).move_to(LEFT * 3.4 + DOWN * 0.25)
        right_card = self._make_case_card(
            score="369", status="Below cutoff", status_color=GOLD_MAIN,
            result="Got scholarship", result_color=GREEN_MAIN, reason="Secondary review",
        ).move_to(RIGHT * 3.4 + DOWN * 0.25)

        self.play(
            Transform(headline2, top_label),
            FadeIn(left_card, shift=RIGHT * 0.2),
            run_time=0.7,
        )
        self.wait(22.5698 - 16.9041 - 0.7)  # chunk4 end

        self.play(FadeIn(right_card, shift=LEFT * 0.2), run_time=0.6)
        self.wait(29.3965 - 22.5698 - 0.6)  # chunk5 end

        self.play(FadeOut(VGroup(headline2, left_card, right_card)), run_time=0.5)

        # ── Beat 4 (chunk6-7: 29.40~40.36) ──────────────────────
        headline3 = VGroup(
            Text("Crossing the cutoff doesn't mean everyone gets treated,", font=FONT, font_size=24, color=WHITE),
            Text("and falling short doesn't mean no one does", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        self.play(FadeIn(headline3, shift=UP * 0.2), run_time=0.7)
        self.wait(33.7154 - 29.3965 - 0.5 - 0.7)  # chunk6 end

        fuzzy_def = VGroup(
            Text("When the cutoff has a discontinuous effect on treatment", font=FONT, font_size=22, color=WHITE),
            Text("probability without fully determining it", font=FONT, font_size=22, color=WHITE),
            Text("Fuzzy RDD", font=FONT, font_size=30, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.25).move_to(ORIGIN)

        self.play(FadeOut(headline3, run_time=0.4), FadeIn(fuzzy_def, shift=UP * 0.2, run_time=0.7))
        self.wait(40.3563 - 33.7154 - 0.7)  # chunk7 end

        # ── Beat 5 (chunk8-9: 40.36~51.51) ──────────────────────
        graph_title = Text("Fuzzy RDD", font=FONT, font_size=32, color=GOLD_MAIN).to_edge(UP, buff=0.7)
        axes, cutoff_line = self._make_axes()
        fuzzy_curve = self._make_fuzzy_curve(axes)
        ax_x_lbl = Text("Score (X)", font=FONT, font_size=16, color=GRAY_MID)
        ax_x_lbl.next_to(axes.x_axis.get_right(), RIGHT, buff=0.12)
        ax_y_lbl = Text("P(Treatment) (D)", font=FONT, font_size=16, color=GRAY_MID)
        ax_y_lbl.next_to(axes.y_axis.get_top(), UP, buff=0.1)
        jump_label = Text("Partial jump: 15% -> 65%", font=FONT, font_size=22, color=WHITE)
        # AppleGothic 폰트에서 "Sharp RDD" 사이 공백이 거의 보이지 않아 별도 Text로 분리
        sharp_note = VGroup(
            Text("(Sharp", font=FONT, font_size=16, color=GRAY_MID),
            Text("RDD: 0% -> 100%)", font=FONT, font_size=16, color=GRAY_MID),
        ).arrange(RIGHT, buff=0.1)
        labels = VGroup(jump_label, sharp_note).arrange(DOWN, buff=0.15)

        graph_group = VGroup(axes, cutoff_line, fuzzy_curve, ax_x_lbl, ax_y_lbl).move_to(DOWN * 0.4)
        labels.next_to(graph_group, DOWN, buff=0.35)
        fuzzy_graph_group = VGroup(graph_title, graph_group, labels)

        self.play(FadeOut(fuzzy_def, run_time=0.5), FadeIn(fuzzy_graph_group, shift=UP * 0.15, run_time=0.8))
        self.wait(46.9972 - 40.3563 - 0.8)  # chunk8 end

        closing = Text(
            "How do we handle Fuzzy RDD?", font=FONT, font_size=34, color=WHITE,
        ).move_to(ORIGIN)

        self.play(FadeOut(fuzzy_graph_group), FadeIn(closing, shift=UP * 0.2), run_time=0.7)
        # WAIT_TAIL = (51.513 + 0.5) - (46.997 + 0.7) = 4.316
        self.wait(4.316)

    # ── 헬퍼 (원본과 동일 구조, 라벨만 영어) ─────────────────────

    def _make_case_card(self, score, status, status_color, result, result_color, reason) -> VGroup:
        score_t = Text(score, font=FONT, font_size=40, color=WHITE)

        status_t = Text(status, font=FONT, font_size=19, color=status_color)
        status_box = SurroundingRectangle(
            status_t, color=status_color, buff=0.12, corner_radius=0.08, stroke_width=1.5,
        )
        status_g = VGroup(status_box, status_t)

        result_t = Text(result, font=FONT, font_size=24, color=WHITE)
        result_box = SurroundingRectangle(
            result_t, color=result_color, fill_color=result_color, fill_opacity=0.9,
            buff=0.14, corner_radius=0.1, stroke_width=0,
        )
        result_g = VGroup(result_box, result_t)

        reason_t = Text(reason, font=FONT, font_size=16, color=GRAY_MID)

        inner = VGroup(score_t, status_g, result_g, reason_t).arrange(DOWN, buff=0.24)
        frame = RoundedRectangle(
            width=3.8, height=3.2, corner_radius=0.15, color=result_color, stroke_width=2.5,
        )
        inner.move_to(frame.get_center())
        return VGroup(frame, inner)

    def _make_step_graph(self) -> VGroup:
        axes = Axes(
            x_range=[0, 10, 10],
            y_range=[0, 1.2, 1],
            x_length=3.8,
            y_length=2.0,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_tip": False},
            x_axis_config={"numbers_to_include": []},
            y_axis_config={"numbers_to_include": [0, 1]},
            tips=False,
        )
        for label in axes.y_axis.numbers:
            label.set(font_size=14)

        c_x = 5
        cutoff_line = DashedLine(
            axes.c2p(c_x, 0), axes.c2p(c_x, 1.15),
            color=YELLOW_MAIN, dash_length=0.06, stroke_width=2,
        )
        left_line = axes.plot(lambda x: 0, x_range=[0, c_x], color=GOLD_MAIN, stroke_width=5)
        right_line = axes.plot(lambda x: 1, x_range=[c_x, 10], color=TEAL_MAIN, stroke_width=5)
        open_dot = Circle(radius=0.06, color=GOLD_MAIN, fill_opacity=0, stroke_width=2.5).move_to(axes.c2p(c_x, 0))
        closed_dot = Dot(axes.c2p(c_x, 1), radius=0.06, color=TEAL_MAIN)
        c_label = Text("c", font=FONT, font_size=18, color=YELLOW_MAIN).next_to(cutoff_line, DOWN, buff=0.1)

        x_lbl = Text("Score (X)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_right(), RIGHT, buff=0.12)
        y_lbl = Text("Treatment (D)", font=FONT, font_size=14, color=GRAY_MID)
        y_lbl.next_to(axes.y_axis.get_top(), UP, buff=0.1)

        return VGroup(axes, cutoff_line, left_line, right_line, open_dot, closed_dot, c_label, x_lbl, y_lbl)

    def _make_axes(self):
        axes = Axes(
            x_range=[340, 401, 30],
            y_range=[0, 1.01, 0.5],
            x_length=4.5,
            y_length=2.6,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_tip": False},
            x_axis_config={"numbers_to_include": [340, 370, 400]},
            y_axis_config={"numbers_to_include": [0, 1]},
            tips=False,
        )
        for label in axes.x_axis.numbers:
            label.set(font_size=16)
        for label in axes.y_axis.numbers:
            label.set(font_size=16)
        cutoff_line = DashedLine(
            axes.c2p(370, 0), axes.c2p(370, 1.05),
            color=YELLOW_MAIN, dash_length=0.08, stroke_width=2,
        )
        return axes, cutoff_line

    def _make_fuzzy_curve(self, axes: Axes) -> VGroup:
        left_line = axes.plot(
            lambda x: 0.05 + (0.15 - 0.05) / 30 * (x - 340),
            x_range=[340, 370], color=GOLD_MAIN, stroke_width=5,
        )
        right_line = axes.plot(
            lambda x: 0.65 + (0.85 - 0.65) / 30 * (x - 370),
            x_range=[370, 400], color=TEAL_MAIN, stroke_width=5,
        )
        jump_line = DashedLine(
            axes.c2p(370, 0.15), axes.c2p(370, 0.65),
            color=GRAY_MID, stroke_width=2, dash_length=0.08, stroke_opacity=0.8,
        )
        dot_open   = Circle(radius=0.07, color=GOLD_MAIN, fill_opacity=0, stroke_width=2.5).move_to(axes.c2p(370, 0.15))
        dot_closed = Dot(axes.c2p(370, 0.65), radius=0.07, color=TEAL_MAIN, fill_opacity=1)
        return VGroup(left_line, right_line, jump_line, dot_open, dot_closed)


class Scene02Variables(Scene):
    """
    Scene 02: variables (English port of Scene02Variables)
    스크립트: src/scripts/02_variables.txt
    타이밍: build/audio/02_variables.timings.json (총 52.45s, 7 chunks)

    Beat4/5의 Z/Y 등장 시점과 "메모 자라남" 시점은 한국어 버전에서도 문장
    글자 수 비율로 추정한 값이었으므로, 여기서도 같은 방식(구 청크 내 비율을
    새 청크 길이에 곱함)으로 다시 추정했다: Z ≈32.12s, Y ≈39.85s, note ≈47.46s.

    Beat1 chunk1   ( 0.00~ 4.55)  one-line definition headline
    Beat2 chunk2-3 ( 4.55~24.85)  scholarship rule + 4 real-world mismatch cases
    Beat3 chunk4   (24.85~27.72)  "let's distinguish four variables" bridge
    Beat4 chunk5-6 (27.72~42.54)  4-variable table: X->Z->D->Y rows appear in sequence
    Beat5 chunk7   (42.54~52.45)  Z=D (Sharp) vs Z != D (Fuzzy) contrast (WAIT_TAIL)
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~4.55) ──────────────────────────────
        title = VGroup(
            Text("What is Fuzzy RDD?", font=FONT, font_size=40, color=TEAL_MAIN),
            Text("RDD where the cutoff doesn't force treatment 100%", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP * 0.2), run_time=0.7)
        self.wait(4.5511 - 0.7)

        # ── Beat 2 (chunk2-3: 4.55~24.85) ────────────────────────
        rule = VGroup(
            Text("CSAT score >= 370", font=FONT, font_size=26, color=WHITE),
            Text("-> Eligible to apply", font=FONT, font_size=26, color=TEAL_MAIN),
        ).arrange(RIGHT, buff=0.3).to_edge(UP, buff=1.1)
        rule_note = Text("Under Sharp RDD, eligible = everyone treated", font=FONT, font_size=18, color=GRAY_MID).next_to(rule, DOWN, buff=0.3)

        self.play(FadeOut(title, run_time=0.5), FadeIn(VGroup(rule, rule_note), shift=UP * 0.15, run_time=0.7))
        self.wait(14.3499 - 4.5511 - 0.5 - 0.7)

        # chunk3: real-world cases (eligible but untreated / ineligible but treated)
        cases_pos = VGroup(
            Text("371 - missed the application deadline", font=FONT, font_size=20, color=RED_MAIN),
            Text("372 - rejected for incomplete paperwork", font=FONT, font_size=20, color=RED_MAIN),
            Text("375 - well-off, didn't bother applying", font=FONT, font_size=20, color=RED_MAIN),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        case_neg = Text("368 - received via secondary review", font=FONT, font_size=20, color=GREEN_MAIN)
        cases = VGroup(cases_pos, case_neg).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.6)

        self.play(FadeIn(cases, shift=UP * 0.15, lag_ratio=0.2, run_time=0.9))
        self.wait(24.8454 - 14.3499 - 0.9)

        # ── Beat 3 (chunk4: 24.85~27.72) ─────────────────────────
        bridge = Text("Let's distinguish four variables", font=FONT, font_size=32, color=WHITE).move_to(ORIGIN)
        self.play(FadeOut(VGroup(rule, rule_note, cases), run_time=0.4), FadeIn(bridge, shift=UP * 0.2, run_time=0.6))
        self.wait(27.7246 - 24.8454 - 0.4 - 0.6)

        # ── Beat 4 (chunk5-6: 27.72~42.54) 변수 4개 표 ───────────
        header = self._var_row_header()
        row_x = self._var_row("X", "Running var.", "CSAT score", TEAL_MAIN)
        row_z = self._var_row("Z", "Instrument", "Eligible (score >= 370)", GOLD_MAIN)
        row_d = self._var_row("D", "Treatment", "Actually received scholarship", TEAL_MAIN)
        row_y = self._var_row("Y", "Outcome", "GPA", GOLD_MAIN)

        header.shift(UP * 2.1)
        row_x.shift(UP * 1.1)
        row_z.shift(UP * 0.1)
        row_d.shift(DOWN * 1.0)
        row_y.shift(DOWN * 2.0)

        hline = Line(LEFT * 5.0, RIGHT * 4.5, color=GRAY_MID, stroke_width=0.8).set_y(1.6)

        full_table = VGroup(header, row_x, row_z, row_d, row_y)

        # chunk5 첫 문장 "First, X is the running variable..." → header+구분선+X 행
        self.play(FadeOut(bridge, run_time=0.4), FadeIn(VGroup(header, hline, row_x), shift=UP * 0.15, run_time=0.7))
        self.wait(32.123 - 27.7246 - 0.4 - 0.7)
        # chunk5 후반 "Z is the instrument..." → Z 행 (문장 길이 비율 추정)
        self.play(FadeIn(row_z, shift=UP * 0.15, run_time=0.5))
        self.wait(35.8052 - 32.123 - 0.5)
        # chunk6 전반 "D is the treatment variable..." → D 행
        self.play(FadeIn(row_d, shift=UP * 0.15, run_time=0.5))
        self.wait(39.845 - 35.8052 - 0.5)
        # chunk6 후반 "and Y is the outcome variable..." → Y 행
        self.play(FadeIn(row_y, shift=UP * 0.15, run_time=0.5))
        self.wait(42.5390 - 39.845 - 0.5)
        self.wait(0.8)  # 표 전환 전 brief pause

        # ── Beat 5 (chunk7: 42.54~52.45) Z=D vs Z != D ───────────
        self.play(FadeOut(VGroup(full_table, hline), run_time=0.5))

        sharp_top = VGroup(
            Text("Sharp RDD", font=FONT, font_size=24, color=GRAY_MID),
            MathTex(r"Z = D", font_size=44).set_color(GRAY_MID),
        ).arrange(DOWN, buff=0.35)
        CARD_H = 2.6
        sharp_frame = RoundedRectangle(width=3.6, height=CARD_H, corner_radius=0.15, color=GRAY_MID, stroke_width=2)
        sharp_top.move_to(sharp_frame.get_center())
        sharp_card = VGroup(sharp_frame, sharp_top)

        fuzzy_top = VGroup(
            Text("Fuzzy RDD", font=FONT, font_size=24, color=TEAL_MAIN),
            MathTex(r"Z \neq D", font_size=44).set_color(TEAL_MAIN),
        ).arrange(DOWN, buff=0.35)
        FUZZY_W = 5.6
        fuzzy_frame = RoundedRectangle(width=FUZZY_W, height=CARD_H, corner_radius=0.15, color=TEAL_MAIN, stroke_width=2)
        fuzzy_top.move_to(fuzzy_frame.get_center())
        fuzzy_card = VGroup(fuzzy_frame, fuzzy_top)

        cards = VGroup(sharp_card, fuzzy_card).arrange(RIGHT, buff=0.7, aligned_edge=UP).move_to(UP * 0.3)

        z_ref = VGroup(
            MathTex("Z", font_size=22).set_color(GOLD_MAIN),
            Text("= instrument (eligibility)", font=FONT, font_size=17, color=GRAY_MID),
        ).arrange(RIGHT, buff=0.15)
        d_ref = VGroup(
            MathTex("D", font_size=22).set_color(TEAL_MAIN),
            Text("= treatment (actual receipt)", font=FONT, font_size=17, color=GRAY_MID),
        ).arrange(RIGHT, buff=0.15)
        zd_recap = VGroup(z_ref, d_ref).arrange(RIGHT, buff=0.9).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(sharp_card, shift=UP * 0.15, run_time=0.7), FadeIn(fuzzy_card, shift=UP * 0.15, run_time=0.7), FadeIn(zd_recap, run_time=0.5))
        self.wait(47.457 - 42.5390 - 0.8 - 0.5 - 0.7)

        fuzzy_frame_grown = RoundedRectangle(
            width=FUZZY_W, height=3.6, corner_radius=0.15, color=TEAL_MAIN, stroke_width=2,
        )
        fuzzy_frame_grown.move_to(fuzzy_frame.get_center())
        fuzzy_frame_grown.align_to(fuzzy_frame, UP)

        fuzzy_note = VGroup(
            Text("Eligibility affects treatment,", font=FONT, font_size=17, color=WHITE),
            Text("but doesn't fully determine it", font=FONT, font_size=17, color=WHITE),
        ).arrange(DOWN, buff=0.12)
        note_zone_y = (fuzzy_top.get_bottom()[1] + fuzzy_frame_grown.get_bottom()[1]) / 2
        fuzzy_note.move_to([fuzzy_frame.get_center()[0], note_zone_y, 0])

        self.play(
            Transform(fuzzy_frame, fuzzy_frame_grown, run_time=0.6),
            FadeIn(fuzzy_note, shift=UP * 0.1, run_time=0.6),
        )
        # Earlier concurrent FadeOut/FadeIn self.play() calls in this scene only cost
        # max(run_times), not their sum, so the naive "target - sum(run_times)" formula
        # used above drifts ~1.3s early by this point. Recomputed from an actual timeline
        # simulation: cumulative time here is 46.757s, so WAIT_TAIL = (52.448+0.5) - 46.757 = 6.191
        self.wait(6.191)

    def _var_row_header(self) -> VGroup:
        s = Text("Symbol", font=FONT, font_size=18, color=GRAY_MID).move_to(LEFT * 4.3)
        n = Text("Meaning", font=FONT, font_size=18, color=GRAY_MID).move_to(LEFT * 2.4, aligned_edge=LEFT)
        d = Text("Example", font=FONT, font_size=18, color=GRAY_MID).move_to(RIGHT * 0.3, aligned_edge=LEFT)
        return VGroup(s, n, d)

    def _var_row(self, sym, name, desc, sym_color) -> VGroup:
        s = MathTex(sym + "_i", font_size=40).set_color(sym_color).move_to(LEFT * 4.3)
        n = Text(name, font=FONT, font_size=24, color=WHITE).move_to(LEFT * 2.4, aligned_edge=LEFT)
        d = Text(desc, font=FONT, font_size=22, color=GRAY_MID).move_to(RIGHT * 0.3, aligned_edge=LEFT)
        return VGroup(s, n, d)


class Scene03Wald(Scene):
    """
    Scene 03: wald (English port of Scene03Wald)
    스크립트: src/scripts/03_wald.txt
    타이밍: build/audio/03_wald.timings.json (총 39.90s, 5 chunks) — 전 체크포인트가 청크 경계와 정확히 일치.

    Beat1 chunk1   ( 0.00~ 2.74)  question headline
    Beat2 chunk2   ( 2.74~11.05)  partial jump: treatment rate bars 10%->65%
    Beat3 chunk3   (11.05~21.78)  Y +0.5 caption
    Beat4 chunk4-5 (21.78~39.90)  Wald estimator = dY/dD = 0.5/0.55 ~ 0.91 + numerator/denominator labels (WAIT_TAIL)
    """

    def construct(self):
        # ── Beat 1 (chunk1) ──────────────────────────────────────
        q = Text("How do we estimate the effect in Fuzzy RDD?", font=FONT, font_size=34, color=WHITE).move_to(ORIGIN)
        self.play(FadeIn(q, shift=UP * 0.2), run_time=0.6)
        self.wait(2.740 - 0.6)

        # ── Beat 2 (chunk2) partial jump bars ─────────────────────
        head = VGroup(
            Text("Fuzzy RDD: only some get treated past the cutoff", font=FONT, font_size=24, color=WHITE),
            Text("(bars = probability of getting the scholarship)", font=FONT, font_size=18, color=GRAY_MID),
        ).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.7)
        bar0 = self._prob_bar(0.10, "Ineligible", "10%", GOLD_MAIN, "(score < 370)").move_to(LEFT * 2.3 + DOWN * 0.1)
        bar1 = self._prob_bar(0.65, "Eligible", "65%", TEAL_MAIN, "(score >= 370)").move_to(RIGHT * 2.3 + DOWN * 0.1)
        delta = Text("+55%p", font=FONT, font_size=26, color=WHITE).move_to(UP * 0.9)
        bars = VGroup(bar0, bar1, delta)
        self.play(FadeOut(q, run_time=0.4), FadeIn(head, run_time=0.5), FadeIn(bars, shift=UP * 0.15, run_time=0.7))
        self.wait(11.0527 - 2.740 - 0.7)

        # ── Beat 3 (chunk3) Y increase caption ────────────────────
        y_caption = VGroup(
            Text("GPA (Y) rose by 0.5", font=FONT, font_size=24, color=WHITE),
            Text("= caused by the extra 55% recipients, not everyone", font=FONT, font_size=20, color=GRAY_MID),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(y_caption, shift=UP * 0.15, run_time=0.6))
        self.wait(21.7803 - 11.0527 - 0.6)

        # ── Beat 4 (chunk4-5) Wald estimator ──────────────────────
        self.play(FadeOut(VGroup(head, bars, y_caption)), run_time=0.5)
        formula = MathTex(
            r"\hat{\tau}_{Fuzzy}", r"=", r"\frac{\Delta Y}{\Delta D}", r"=",
            r"\frac{0.5}{0.55}", r"\approx", r"0.91", font_size=52,
        ).move_to(UP * 0.6)
        formula[2].set_color(WHITE)
        formula[6].set_color(GOLD_MAIN)
        self.play(FadeIn(formula, shift=UP * 0.15, run_time=0.7))
        self.wait(31.4863 - 21.7803 - 0.5 - 0.7)

        label_y = self._wald_label("Numerator (", r"ITT_Y", ") : change eligibility caused in outcome (Y)", GOLD_MAIN)
        label_d = self._wald_label("Denominator (", r"ITT_D", ") : change eligibility caused in treatment (D)", TEAL_MAIN)
        label_d.next_to(label_y, DOWN, buff=0.3)
        labels = VGroup(label_y, label_d)
        labels.next_to(formula, DOWN, buff=0.9)
        self.play(FadeIn(labels, shift=UP * 0.15, run_time=0.6))
        # WAIT_TAIL = (39.901 + 1.0) - 31.486 - 0.6 = 8.815
        self.wait(8.815)

    def _wald_label(self, prefix: str, sub: str, suffix: str, color) -> VGroup:
        t1 = Text(prefix, font=FONT, font_size=22, color=color)
        t2 = MathTex(sub, font_size=26).set_color(color)
        t3 = Text(suffix, font=FONT, font_size=22, color=color)
        row = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.05)
        t2.set_y(t1.get_center()[1])
        return row

    def _prob_bar(self, frac, label, pct, color, sublabel=None) -> VGroup:
        H = 2.6
        track = Rectangle(width=0.9, height=H, stroke_color=GRAY_MID, stroke_width=1.5, fill_opacity=0)
        fill = Rectangle(width=0.9, height=H * frac, stroke_width=0, fill_color=color, fill_opacity=0.9)
        fill.align_to(track, DOWN)
        pct_t = Text(pct, font=FONT, font_size=24, color=color).next_to(fill, UP, buff=0.15)
        lab = Text(label, font=FONT, font_size=20, color=WHITE).next_to(track, DOWN, buff=0.2)
        parts = VGroup(track, fill, pct_t, lab)
        if sublabel:
            sub = Text(sublabel, font=FONT, font_size=14, color=GRAY_MID).next_to(lab, DOWN, buff=0.1)
            parts.add(sub)
        return parts


class Scene04ComplierLate(Scene):
    """
    Scene 04: complier_late (English port of Scene04ComplierLate)
    스크립트: src/scripts/04_complier_late.txt
    타이밍: build/audio/04_complier_late.timings.json (총 67.59s, 8 chunks) — 전 체크포인트 청크 경계와 일치.

    한국어 원본의 "자격 X/자격 O", "처치 X/처치 O" 표기(한국어식 X=아니오/O=예)는
    영어에서 같은 의미로 안 읽히므로 "Ineligible/Eligible", "Not treated/Treated"로 바꿨다.

    Beat1 chunk1-2 ( 0.00~15.09)  context + "whose effect is this?" question
    Beat2 chunk3-4 (15.09~36.46)  only behavior-changers are captured
    Beat3 chunk5-7 (36.46~58.00)  four-type table (always/never excluded -> defiers excluded)
    Beat4 chunk8   (58.00~67.59)  compliers = target, LATE (WAIT_TAIL)
    """

    def construct(self):
        # ── Beat 1 (chunk1) context ───────────────────────────────
        ctx = VGroup(
            Text("We just calculated the treatment effect using the Wald estimator.", font=FONT, font_size=26, color=WHITE),
            VGroup(
                Text("But some can't get treated even when eligible,", font=FONT, font_size=22, color=GRAY_MID),
                Text("and some get treated even without eligibility.", font=FONT, font_size=22, color=GRAY_MID),
            ).arrange(DOWN, buff=0.2),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)
        self.play(FadeIn(ctx, shift=UP * 0.2), run_time=0.7)
        self.wait(9.2415 - 0.7)

        # ── Beat 1 (chunk2) question ───────────────────────────────
        q = VGroup(
            Text("So whose effect", font=FONT, font_size=30, color=WHITE),
            Text("did we just calculate?", font=FONT, font_size=38, color=TEAL_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.play(FadeOut(ctx, run_time=0.4), FadeIn(q, shift=UP * 0.15, run_time=0.6))
        self.wait(15.0930 - 9.2415 - 0.4 - 0.6)

        # ── Beat 2 (chunk3) two uncaptured cases ────────────────────
        b2 = VGroup(
            Text("Case 1.  Score below 370, but gets the scholarship", font=FONT, font_size=22, color=GRAY_MID),
            Text("Case 2.  Score at or above 370, but doesn't get it", font=FONT, font_size=22, color=GRAY_MID),
            Text("-> Not captured by the Wald estimator", font=FONT, font_size=26, color=WHITE),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.5)
        self.play(FadeOut(q, run_time=0.4), FadeIn(b2, shift=UP * 0.15, run_time=0.7))
        self.wait(23.3593 - 15.0930 - 0.4 - 0.7)

        # ── Beat 2 (chunk4) Wald formula + who it reflects ──────────
        formula_wald = MathTex(r"\hat{\tau}_{Fuzzy} = \frac{\Delta Y}{\Delta D}", font_size=52).move_to(UP * 0.5)
        b2c = Text("Only reflects people whose behavior changed because of eligibility", font=FONT, font_size=22, color=GOLD_MAIN)
        b2c.next_to(formula_wald, DOWN, buff=0.7)
        self.play(FadeOut(b2, run_time=0.4), FadeIn(VGroup(formula_wald, b2c), shift=UP * 0.1, run_time=0.6))
        self.wait(36.4553 - 23.3593 - 0.6)

        # ── Beat 3 (chunk5) four-type table ──────────────────────────
        self.play(FadeOut(VGroup(formula_wald, b2c)), run_time=0.5)
        header = self._type_row("Type", "Ineligible", "Eligible", 2.05, GRAY_MID, header=True)
        r_comp = self._type_row("Complier",     "Not treated", "Treated",     1.15, WHITE)
        r_at   = self._type_row("Always-taker", "Treated",     "Treated",     0.35, WHITE)
        r_nt   = self._type_row("Never-taker",  "Not treated", "Not treated", -0.45, WHITE)
        r_def  = self._type_row("Defier",       "Treated",     "Not treated", -1.25, WHITE)
        table = VGroup(header, r_comp, r_at, r_nt, r_def)
        hline = Line(LEFT * 4.3, RIGHT * 4.3, color=GRAY_MID, stroke_width=1).move_to(UP * 1.62)
        table_g = VGroup(table, hline).move_to(UP * 0.3)
        cap = Text("How treatment (D) varies with eligibility (Z)", font=FONT, font_size=24, color=WHITE).to_edge(UP, buff=0.7)
        self.play(FadeIn(VGroup(table_g, cap), run_time=0.7))
        self.wait(40.3098 - 36.4553 - 0.5 - 0.7)

        # chunk6: always/never-taker explanation (dim everything else)
        self.play(r_comp.animate.set_opacity(0.35), r_def.animate.set_opacity(0.35), run_time=0.5)
        self.wait(50.8517 - 40.3098 - 0.5)

        # chunk6 end: always/never dim + red strike, defier restored
        strike_at = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_at.get_center())
        strike_nt = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_nt.get_center())
        self.play(
            r_at.animate.set_opacity(0.35), r_nt.animate.set_opacity(0.35),
            Create(strike_at), Create(strike_nt),
            r_def.animate.set_opacity(1.0),
            run_time=0.5,
        )

        # chunk7: defier explanation (only defier white, no strike yet)
        self.wait(58.0034 - 50.8517 - 0.5)

        # chunk7 end: defier dim + red strike, complier restored
        strike_def = Line(LEFT * 4.3, RIGHT * 4.3, color=RED_MAIN, stroke_width=2.5).move_to(r_def.get_center())
        self.play(
            r_def.animate.set_opacity(0.35), Create(strike_def),
            r_comp.animate.set_opacity(1.0),
            run_time=0.5,
        )

        # ── Beat 4 (chunk8) compliers = LATE ─────────────────────────
        box = SurroundingRectangle(r_comp, color=TEAL_MAIN, buff=0.18, corner_radius=0.08, stroke_width=3)
        label_comp = Text("target ->", font=FONT, font_size=20, color=TEAL_MAIN)
        label_comp.next_to(box, LEFT, buff=0.2)
        cap4 = Text("Local average treatment effect on compliers (LATE)", font=FONT, font_size=22, color=WHITE).to_edge(DOWN, buff=1.5)
        self.play(Create(box), FadeOut(cap, run_time=0.3), FadeIn(cap4, shift=UP * 0.1, run_time=0.6), FadeIn(label_comp, run_time=0.6))
        # WAIT_TAIL = (67.587 + 1.0) - 58.003 - 0.5 - 0.6 = 9.484
        self.wait(9.484)

    def _type_row(self, name, v0, v1, y, name_color, header=False) -> VGroup:
        import numpy as np
        fs = 22 if header else 20
        n = Text(name, font=FONT, font_size=fs, color=name_color).move_to(np.array([-4.2, y, 0]), aligned_edge=LEFT)
        c0 = Text(v0, font=FONT, font_size=fs, color=name_color).move_to(np.array([1.4, y, 0]))
        c1 = Text(v1, font=FONT, font_size=fs, color=name_color).move_to(np.array([3.6, y, 0]))
        return VGroup(n, c0, c1)


class Scene05Assumptions(Scene):
    """
    Scene 05: assumptions (English port of Scene05Assumptions)
    스크립트: src/scripts/05_assumptions.txt
    타이밍: build/audio/05_assumptions.timings.json (총 62.26s, 6 chunks) — 전 체크포인트 청크 경계와 일치.

    Beat1 chunk1-2 ( 0.00~12.40)  Z = instrument (IV) -> 3 validity conditions (left list)
    Beat2 chunk3   (12.40~31.90)  relevance: Cov(Z,D)!=0, denominator!=0, F>10
    Beat3 chunk4   (31.90~43.98)  exclusion restriction: Z->D->Y, no direct path
    Beat4 chunk5   (43.98~56.29)  monotonicity: no defiers, D(Z=1)>=D(Z=0)
    Beat5 chunk6   (56.29~62.26)  3 conditions hold -> Wald = LATE (WAIT_TAIL)
    """

    def construct(self):
        import numpy as np
        # ── Beat 1 (chunk1-2) IV -> 3 conditions list ─────────────
        head = VGroup(
            Text("Eligibility Z = Instrumental Variable (IV)", font=FONT, font_size=34, color=TEAL_MAIN),
            Text("Fuzzy RDD is fundamentally an IV estimation problem", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        self.play(FadeIn(head, shift=UP * 0.2), run_time=0.6)
        self.wait(9.7524 - 0.6)

        top = Text("Three conditions for a valid instrument", font=FONT, font_size=24, color=GRAY_MID).to_edge(UP, buff=0.8)
        t1 = Text("1. Relevance", font=FONT, font_size=27, color=GRAY_MID)
        t2 = Text("2. Exclusion restriction", font=FONT, font_size=27, color=GRAY_MID)
        t3 = Text("3. Monotonicity", font=FONT, font_size=27, color=GRAY_MID)
        titles = VGroup(t1, t2, t3).arrange(DOWN, buff=0.9, aligned_edge=LEFT).move_to(LEFT * 4.0)
        sep = Line(UP * 1.9, DOWN * 1.9, color=GRAY_MID, stroke_width=1).move_to(LEFT * 1.6)

        self.play(FadeOut(head, run_time=0.4), FadeIn(top, run_time=0.5), FadeIn(titles, shift=RIGHT * 0.1, run_time=0.6), Create(sep, run_time=0.5))
        self.wait(12.3995 - 9.7524 - 0.4 - 0.6)

        detail_pos = RIGHT * 2.4

        # ── Beat 2 (chunk3) relevance ────────────────────────────
        d1 = VGroup(
            Text("Eligibility must actually raise treatment probability", font=FONT, font_size=22, color=WHITE),
            MathTex(r"\mathrm{Cov}(Z, D) \neq 0", font_size=34).set_color(TEAL_MAIN),
            Text("= Wald denominator != 0", font=FONT, font_size=20, color=GRAY_MID),
            Text("F-statistic > 10 -> strong instrument", font=FONT, font_size=20, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.4).move_to(detail_pos)
        self.play(t1.animate.set_color(TEAL_MAIN), FadeIn(d1, shift=UP * 0.1, run_time=0.6))
        self.wait(31.9042 - 12.3995 - 0.6)

        # ── Beat 3 (chunk4) exclusion restriction ────────────────
        diagram = self._iv_diagram_icons()
        d2 = VGroup(
            Text("Eligibility must affect the outcome only through treatment", font=FONT, font_size=22, color=WHITE),
            diagram,
            Text("No direct Z -> Y path allowed", font=FONT, font_size=20, color=RED_MAIN),
        ).arrange(DOWN, buff=0.45).move_to(detail_pos)
        self.play(t1.animate.set_color(GRAY_MID), t2.animate.set_color(TEAL_MAIN),
                  FadeOut(d1), FadeIn(d2, shift=UP * 0.1), run_time=0.5)
        self.wait(43.9786 - 31.9042 - 0.5)

        # ── Beat 4 (chunk5) monotonicity ──────────────────────────
        d3 = VGroup(
            Text("No one refuses treatment upon becoming eligible (no defiers)", font=FONT, font_size=22, color=WHITE),
            MathTex(r"D_i(Z{=}1) \geq D_i(Z{=}0)", font_size=32).set_color(TEAL_MAIN),
            Text("All the added treatment comes from compliers", font=FONT, font_size=20, color=GRAY_MID),
        ).arrange(DOWN, buff=0.45).move_to(detail_pos)
        self.play(t2.animate.set_color(GRAY_MID), t3.animate.set_color(TEAL_MAIN),
                  FadeOut(d2), FadeIn(d3, shift=UP * 0.1), run_time=0.5)
        self.wait(56.2852 - 43.9786 - 0.5)

        # ── Beat 5 (chunk6) conclusion ─────────────────────────────
        concl = VGroup(
            Text("If these three assumptions hold,", font=FONT, font_size=24, color=WHITE),
            Text("Wald estimator = LATE", font=FONT, font_size=32, color=GOLD_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(detail_pos)
        self.play(t3.animate.set_color(GRAY_MID),
                  t1.animate.set_color(TEAL_MAIN), t2.animate.set_color(TEAL_MAIN),
                  FadeOut(d3), FadeIn(concl, shift=UP * 0.1), run_time=0.6)
        self.play(t3.animate.set_color(TEAL_MAIN), run_time=0.3)
        # WAIT_TAIL = (62.261 + 0.5) - 56.285 - 0.6 - 0.3 = 5.576
        self.wait(5.576)

    def _iv_diagram_icons(self) -> VGroup:
        """Z->D->Y icon diagram (clinical trial example, exclusion restriction)."""
        from pathlib import Path
        import numpy as np

        ICONS = Path(__file__).parent.parent.parent / "assets" / "tabler-icons" / "icons" / "outline"
        xs     = [-2.2,  0.0,  2.2]
        svgs   = ["vaccine-bottle.svg", "pill.svg", "heartbeat.svg"]
        vars_  = ["Z", "D", "Y"]
        colors = [GOLD_MAIN, TEAL_MAIN, WHITE]
        subs   = ["Trial assignment", "Taking the drug", "Health improves"]

        nodes = []
        for x, svg, var, color, sub in zip(xs, svgs, vars_, colors, subs):
            ico = SVGMobject(str(ICONS / svg), height=0.75)
            ico.set_stroke(color=color, width=2.0, family=True).set_fill(opacity=0)
            ico.move_to(np.array([x, 0.1, 0]))
            v = MathTex(var, font_size=24).set_color(color).next_to(ico, UP, buff=0.12)
            s = Text(sub, font=FONT, font_size=13, color=GRAY_MID).next_to(ico, DOWN, buff=0.12)
            nodes.append(VGroup(ico, v, s))

        a1 = Arrow(np.array([xs[0]+0.52, 0.1, 0]), np.array([xs[1]-0.52, 0.1, 0]),
                   buff=0, stroke_width=2.5, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        a2 = Arrow(np.array([xs[1]+0.52, 0.1, 0]), np.array([xs[2]-0.52, 0.1, 0]),
                   buff=0, stroke_width=2.5, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)

        arc = CurvedArrow(np.array([xs[0]+0.1, 0.85, 0]), np.array([xs[2]-0.1, 0.85, 0]),
                          angle=-PI / 4, color=RED_MAIN, stroke_width=2.5)
        cross = Text("x", font=FONT, font_size=22, color=RED_MAIN, weight=BOLD).move_to(np.array([0.0, 1.45, 0]))

        return VGroup(*nodes, a1, a2, arc, cross)


class Scene06TwoSLS(Scene):
    """
    Scene 06: twosls (English port of Scene06TwoSLS)
    스크립트: src/scripts/06_twosls.txt
    타이밍: build/audio/06_twosls.timings.json (총 75.96s, 8 chunks)

    chunk3/4 내부의 NUMDEN/NOCL, LINE1/LINE2 체크포인트는 한국어 버전에서도
    "문장 길이 비율" 추정값이었으므로, 구 청크 내 비율을 새 청크 길이에 그대로
    곱해 재추정했다: NUMDEN≈13.74, NOCL≈19.98 (chunk3), LINE1≈30.43, LINE2≈34.47 (chunk4).
    나머지 체크포인트는 전부 청크 경계와 정확히 일치.

    chunk1:  0.00 ->  3.02  question: how do we compute the Wald Estimator with real data?
    chunk2:  3.02 -> 11.19  Wald formula (center) + numerator/denominator change labels
    chunk3: 11.19 -> 27.82  dashed divider + right "How to Compute It?": num/denom separately -> ratio -> point estimate, red "no CI"
    chunk4: 27.82 -> 37.52  "2SLS": 1) same point estimate (dot) 2) confidence interval (bar, dashed connector to dot)
    chunk5: 37.52 -> 45.42  note: 2SLS is a general IV method (general Z->D->Y chain)
    chunk6: 45.42 -> 52.24  our Fuzzy RDD: Z=eligibility(IV), D=treatment(endogenous) labels
    chunk7: 52.24 -> 65.20  stage 1: Z->D-hat (stage card)
    chunk8: 65.20 -> 75.96  stage 2: D-hat->Y, beta-hat-1=LATE (stage card, last, WAIT_TAIL)
    """

    def construct(self):
        import numpy as np

        # ── Beat 1 (chunk1, 0->3.02) question ─────────────────────
        question = Text("How do we compute the Wald Estimator with real data?",
                        font=FONT, font_size=26, color=GOLD_MAIN,
                        t2c={"Wald Estimator": TEAL_MAIN}).move_to(ORIGIN)
        self.play(FadeIn(question, shift=UP * 0.1, run_time=0.6))
        self.wait(3.0186 - 0.6)

        # ── Beat 2 (chunk2, 3.02->11.19) Wald formula + num/denom labels ──
        wald_title = Text("Wald Estimator", font=FONT, font_size=24, color=TEAL_MAIN).move_to(UP * 2.6)
        eq_main = MathTex(r"\hat{\tau}", r"=", r"\frac{\Delta Y}{\Delta D}", font_size=80)
        eq_main[0].set_color(TEAL_MAIN)
        eq_main[2].set_color(TEAL_MAIN)
        eq_main.move_to(UP * 0.2)
        num_lbl = Text("change in outcome", font=FONT, font_size=18, color=GRAY_MID).next_to(eq_main, RIGHT, buff=1.3).shift(UP * 0.65)
        den_lbl = Text("change in treatment prob.", font=FONT, font_size=18, color=GRAY_MID).next_to(eq_main, RIGHT, buff=1.3).shift(DOWN * 0.65)
        arr_num = Arrow(num_lbl.get_left(), eq_main[2].get_top() + RIGHT * 0.25, buff=0.12,
                        stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        arr_den = Arrow(den_lbl.get_left(), eq_main[2].get_bottom() + RIGHT * 0.25, buff=0.12,
                        stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        numden = VGroup(num_lbl, den_lbl, arr_num, arr_den)
        self.play(FadeOut(question, run_time=0.4),
                  FadeIn(wald_title, shift=UP * 0.1, run_time=0.5),
                  FadeIn(eq_main, shift=UP * 0.2, run_time=0.7))
        self.play(FadeIn(numden, run_time=0.5))
        self.wait(11.1920 - 3.0186 - 0.7 - 0.5)

        # ── Beat 3 (chunk3, 11.19->27.82) numerator/denominator -> point estimate / no CI ──
        vx = 3.2
        divider = DashedLine(np.array([-1.8, 2.25, 0]), np.array([-1.8, -2.25, 0]),
                             color=GRAY_MID, stroke_width=1.4, dash_length=0.12)
        rhead = Text("How to Compute It?", font=FONT, font_size=24, color=GOLD_MAIN).move_to(np.array([2.6, 1.95, 0]))
        num = VGroup(Text("numerator", font=FONT, font_size=15, color=GRAY_MID),
                     MathTex(r"\Delta Y", font_size=30).set_color(TEAL_MAIN)).arrange(RIGHT, buff=0.18).move_to(np.array([0.45, 0.95, 0]))
        den = VGroup(Text("denominator", font=FONT, font_size=15, color=GRAY_MID),
                     MathTex(r"\Delta D", font_size=30).set_color(GOLD_MAIN)).arrange(RIGHT, buff=0.18).move_to(np.array([0.45, -0.25, 0]))
        frac = MathTex(r"\frac{\Delta Y}{\Delta D}", font_size=46,
                       substrings_to_isolate=[r"\Delta Y", r"\Delta D"]).move_to(np.array([2.15, 0.35, 0]))
        frac.set_color_by_tex(r"\Delta Y", TEAL_MAIN)
        frac.set_color_by_tex(r"\Delta D", GOLD_MAIN)
        a_n = Arrow(num.get_right(), frac.get_left() + UP * 0.20, buff=0.16,
                    stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        a_d = Arrow(den.get_right(), frac.get_left() + DOWN * 0.20, buff=0.16,
                    stroke_width=1.8, color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        pt_dot = Dot(np.array([4.0, 0.35, 0]), radius=0.12, color=TEAL_MAIN)
        a_eq = Arrow(frac.get_right(), pt_dot.get_left(), buff=0.18,
                     stroke_width=2.0, color=GRAY_MID, max_tip_length_to_length_ratio=0.22)
        pt_label = Text("point estimate", font=FONT, font_size=16, color=TEAL_MAIN).next_to(pt_dot, UP, buff=0.22)
        compute_grp = VGroup(num, den, frac, a_n, a_d, a_eq, pt_label)
        nocl = Text("but we can't get a confidence interval", font=FONT, font_size=18, color=RED_MAIN).move_to(np.array([2.3, -1.55, 0]))
        self.play(
            FadeOut(numden, run_time=0.3),
            wald_title.animate.move_to(np.array([-4.1, 1.5, 0])),
            eq_main.animate.scale(0.72).move_to(np.array([-4.1, 0.1, 0])),
            Create(divider, run_time=0.6),
            FadeIn(rhead, run_time=0.5),
            run_time=0.7,
        )
        self.wait(13.744 - 11.1920 - 0.7)
        self.play(FadeIn(num, run_time=0.45), FadeIn(den, run_time=0.45))
        self.play(GrowArrow(a_n, run_time=0.4), GrowArrow(a_d, run_time=0.4), FadeIn(frac, run_time=0.45))
        self.play(GrowArrow(a_eq, run_time=0.4), FadeIn(pt_dot, run_time=0.4), FadeIn(pt_label, run_time=0.4))
        self.wait(19.976 - 13.744 - 0.45 - 0.45 - 0.4)
        self.play(FadeIn(nocl, run_time=0.5))
        self.wait(27.8175 - 19.976 - 0.5)

        # ── Beat 4 (chunk4, 27.82->37.52) 2SLS solves both ────────
        T4_END = 37.5234
        ans_2sls = Text('"2SLS"', font=FONT, font_size=36, weight=BOLD, color=GOLD_MAIN).move_to(np.array([2.55, 1.15, 0]))
        sub_2sls = Text("(Two-Stage Least Squares)", font=FONT, font_size=15, color=GRAY_MID).next_to(ans_2sls, DOWN, buff=0.14)
        line1 = Text("1)  Same as the numerator/denominator ratio", font=FONT, font_size=18, color=WHITE,
                     t2c={"numerator/denominator ratio": TEAL_MAIN}).move_to(np.array([-0.85, -0.55, 0]), aligned_edge=LEFT)
        line2 = Text("2)  Also gives a confidence interval", font=FONT, font_size=19, color=WHITE,
                     t2c={"confidence interval": GOLD_MAIN}).move_to(np.array([-0.85, -1.85, 0]), aligned_edge=LEFT)
        anchor_x = max(line1.get_right()[0], line2.get_right()[0]) + 1.0
        dotpos = np.array([anchor_x, line1.get_center()[1], 0])
        est_dot = Dot(dotpos, radius=0.11, color=TEAL_MAIN)
        dot_cap = Text("point estimate", font=FONT, font_size=14, color=TEAL_MAIN).move_to(dotpos + UP * 0.4)
        arr1 = Arrow(line1.get_right() + RIGHT * 0.1, dotpos + LEFT * 0.22, buff=0.08,
                     stroke_width=2.0, color=TEAL_MAIN, max_tip_length_to_length_ratio=0.28)
        ci_cy = line2.get_center()[1]
        ci_half = 0.72
        ci_bar = Line(np.array([anchor_x - ci_half, ci_cy, 0]), np.array([anchor_x + ci_half, ci_cy, 0]),
                      color=GOLD_MAIN, stroke_width=4)
        ci_capL = Line(np.array([anchor_x - ci_half, ci_cy - 0.14, 0]), np.array([anchor_x - ci_half, ci_cy + 0.14, 0]),
                       color=GOLD_MAIN, stroke_width=4)
        ci_capR = Line(np.array([anchor_x + ci_half, ci_cy - 0.14, 0]), np.array([anchor_x + ci_half, ci_cy + 0.14, 0]),
                       color=GOLD_MAIN, stroke_width=4)
        ci_center = Dot(np.array([anchor_x, ci_cy, 0]), radius=0.08, color=TEAL_MAIN)
        connector = DashedLine(est_dot.get_bottom() + DOWN * 0.02, np.array([anchor_x, ci_cy + 0.18, 0]),
                               color=TEAL_MAIN, stroke_width=1.6, dash_length=0.08)
        ci_fig = VGroup(ci_bar, ci_capL, ci_capR, ci_center)
        self.play(
            FadeOut(compute_grp, run_time=0.45), FadeOut(pt_dot, run_time=0.45), FadeOut(nocl, run_time=0.45),
            FadeIn(ans_2sls, scale=1.1, run_time=0.5), FadeIn(sub_2sls, run_time=0.5),
        )
        self.wait(30.427 - 27.8175 - 0.5)
        self.play(FadeIn(line1, run_time=0.5), FadeIn(est_dot, run_time=0.5), FadeIn(dot_cap, run_time=0.5))
        self.play(GrowArrow(arr1, run_time=0.4))
        self.wait(34.466 - 30.427 - 0.5 - 0.4)
        self.play(FadeIn(line2, run_time=0.5), Create(connector, run_time=0.5), Create(ci_fig, run_time=0.6))
        compare_grp = VGroup(wald_title, eq_main, divider, rhead, ans_2sls, sub_2sls,
                             est_dot, dot_cap, line1, arr1, line2, connector, ci_fig)
        self.wait(T4_END - 34.466 - 0.6)

        # ── Beat 5 (chunk5, 37.52->45.42) note: 2SLS is a general IV method ──
        nZ = MathTex(r"Z", font_size=48).set_color(GOLD_MAIN)
        nD = MathTex(r"D", font_size=48).set_color(TEAL_MAIN)
        nY = MathTex(r"Y", font_size=48).set_color(WHITE)
        chain = VGroup(nZ, nD, nY).arrange(RIGHT, buff=2.6).move_to(UP * 0.1)
        ar1 = Arrow(nZ.get_right(), nD.get_left(), buff=0.25, stroke_width=2.5,
                    color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        ar2 = Arrow(nD.get_right(), nY.get_left(), buff=0.25, stroke_width=2.5,
                    color=GRAY_MID, max_tip_length_to_length_ratio=0.25)
        roleZ = Text("instrument", font=FONT, font_size=16, color=GOLD_MAIN).next_to(nZ, DOWN, buff=0.3)
        roleD = Text("endogenous var.", font=FONT, font_size=16, color=TEAL_MAIN).next_to(nD, DOWN, buff=0.3)
        roleY = Text("outcome", font=FONT, font_size=16, color=WHITE).next_to(nY, DOWN, buff=0.3)
        chain_grp = VGroup(chain, ar1, ar2, roleZ, roleD, roleY)
        ref_title = Text("Note: 2SLS is a general IV estimation method", font=FONT, font_size=22, color=GRAY_MID).move_to(UP * 2.6)
        ref_cap = Text("Not specific to Fuzzy RDD", font=FONT, font_size=18, color=WHITE).move_to(DOWN * 2.0)
        self.play(FadeOut(compare_grp, run_time=0.4),
                  FadeIn(ref_title, run_time=0.5),
                  FadeIn(chain_grp, shift=UP * 0.1, run_time=0.6),
                  FadeIn(ref_cap, run_time=0.5))
        self.wait(45.4182 - 37.5234 - 0.6)

        # ── Beat 6 (chunk6, 45.42->52.24) our Fuzzy RDD: Z=eligibility, D=treatment ──
        nameZ = Text("Eligibility", font=FONT, font_size=16, color=GOLD_MAIN).next_to(nZ, UP, buff=0.3)
        nameD = Text("Treatment", font=FONT, font_size=16, color=TEAL_MAIN).next_to(nD, UP, buff=0.3)
        fuzzy_title = Text("In our Fuzzy RDD setting", font=FONT, font_size=24, color=TEAL_MAIN).move_to(UP * 2.6)
        fuzzy_cap = Text("Eligibility = instrument,   Treatment = endogenous variable", font=FONT, font_size=18, color=WHITE).move_to(DOWN * 2.0)
        self.play(FadeOut(ref_title, run_time=0.3), FadeIn(fuzzy_title, run_time=0.5),
                  FadeIn(nameZ, shift=DOWN * 0.05, run_time=0.5), FadeIn(nameD, shift=DOWN * 0.05, run_time=0.5),
                  FadeOut(ref_cap, run_time=0.3), FadeIn(fuzzy_cap, run_time=0.5))
        self.wait(52.2449 - 45.4182 - 0.5)

        # ── Beat 7 (chunk7, 52.24->65.20) stage 1 ─────────────────
        def _stage(label, eq_parts, accent, eq_color):
            box = RoundedRectangle(width=6.8, height=1.35, corner_radius=0.14,
                                   stroke_color=accent, stroke_width=2.6, fill_opacity=0)
            lab = Text(label, font=FONT, font_size=22, color=accent)
            eq = MathTex(*eq_parts, font_size=40).set_color(eq_color)
            VGroup(lab, eq).arrange(RIGHT, buff=0.5).move_to(box.get_center())
            return box, lab, eq

        s1_box, s1_lab, s1_eq = _stage(
            "Stage 1", [r"\hat{D}_i", r"=", r"\hat{\alpha}_0 +", r"\hat{\alpha}_1 Z_i"], TEAL_MAIN, WHITE)
        s1_eq[0].set_color(TEAL_MAIN)
        stage1 = VGroup(s1_box, s1_lab, s1_eq).move_to(UP * 2.0)
        s2d_box, s2d_lab, s2d_eq = _stage(
            "Stage 2", [r"Y_i =", r"\hat{\beta}_0 +", r"\hat{\beta}_1", r"\hat{D}_i"], GRAY_MID, GRAY_MID)
        stage2_dim = VGroup(s2d_box, s2d_lab, s2d_eq).move_to(DOWN * 0.1).set_opacity(0.4)
        flow_arrow = Arrow(stage1.get_bottom(), stage2_dim.get_top(), buff=0.12,
                           stroke_width=2.8, color=TEAL_MAIN, max_tip_length_to_length_ratio=0.28)
        flow_lbl = MathTex(r"\hat{D}", font_size=30).set_color(TEAL_MAIN).next_to(flow_arrow, RIGHT, buff=0.2)
        cap1 = VGroup(
            Text("Predict only the exogenous part of treatment using Z", font=FONT, font_size=18, color=TEAL_MAIN),
            MathTex(r"\rightarrow \hat{D}", font_size=26).set_color(TEAL_MAIN),
        ).arrange(RIGHT, buff=0.22).move_to(DOWN * 1.75)
        self.play(
            FadeOut(VGroup(chain_grp, nameZ, nameD, fuzzy_title, fuzzy_cap), run_time=0.4),
            FadeIn(stage1, shift=UP * 0.1, run_time=0.5),
            FadeIn(stage2_dim, run_time=0.5),
            GrowArrow(flow_arrow, run_time=0.5),
            FadeIn(flow_lbl, run_time=0.4),
        )
        self.play(FadeIn(cap1, run_time=0.4))
        self.wait(65.2016 - 52.2449 - 0.5 - 0.4)

        # ── Beat 8 (chunk8, 65.20->75.96) stage 2 (last, WAIT_TAIL) ──
        s2a_box, s2a_lab, s2a_eq = _stage(
            "Stage 2", [r"Y_i =", r"\hat{\beta}_0 +", r"\hat{\beta}_1", r"\hat{D}_i"], GOLD_MAIN, WHITE)
        stage2_act = VGroup(s2a_box, s2a_lab, s2a_eq).move_to(DOWN * 0.1)
        s2a_eq[2].set_color(GOLD_MAIN)
        s2a_eq[3].set_color(TEAL_MAIN)
        beta_box = SurroundingRectangle(s2a_eq[2], color=GOLD_MAIN, buff=0.06,
                                        stroke_width=2.2, corner_radius=0.04)
        cap2 = MathTex(r"\hat{\beta}_1 = \text{LATE}", font_size=34).set_color(GOLD_MAIN).move_to(DOWN * 1.75)
        self.play(
            stage1.animate.set_opacity(0.4),
            FadeOut(stage2_dim, run_time=0.3),
            FadeIn(stage2_act, run_time=0.5),
            FadeOut(cap1, run_time=0.3),
            FadeIn(cap2, run_time=0.5),
        )
        self.play(Create(beta_box, run_time=0.4))
        # WAIT_TAIL = (75.958 + 0.4) - 65.202 - 0.5 - 0.4 = 10.256
        self.wait(10.256)


class Scene07Recap(Scene):
    """
    Scene 07: recap (English port of Scene07Recap)
    스크립트: src/scripts/07_recap.txt
    타이밍: build/audio/07_recap.timings.json (총 25.15s, 3 chunks)

    한국어 최종본과 동일한 3비트 구조(정의 → 왈드 점추정 → 2SLS 신뢰구간 → 마무리)를
    그대로 포팅. Beat2/3의 왈드→2SLS 전환, 마무리 문장 등장 시점은 한국어 버전에서도
    문장 길이 비율로 추정한 값이었으므로, 같은 방식(구 청크 내 비율 → 새 청크 길이)으로
    재추정했다: 전환 ≈13.49s(청크2 내), 마무리 문장 ≈22.16s(청크3 내).

    Beat1 chunk1 ( 0.00~10.50)  Fuzzy RDD one-line definition (recap)
    Beat2 chunk2 (10.50~17.09)  Wald (point estimate, no CI) -> 2SLS (same point + CI)
        Scene06 Beat3/4 visual grammar reused: TEAL dot = point estimate, RED = no CI,
        GOLD bar+caps = CI, TEAL dashed connector = "interval centered on that point".
    Beat3 chunk3 (17.09~25.15)  closing: Sharp RDD checked, Fuzzy RDD checked -> next video (WAIT_TAIL)
    """

    def construct(self):
        import numpy as np

        # ── Beat 1 (chunk1, 0->10.50) Fuzzy RDD one-line definition (recap) ──
        defn = VGroup(
            Text("Fuzzy RDD", font=FONT, font_size=40, color=TEAL_MAIN),
            Text("When the cutoff doesn't fully determine treatment,", font=FONT, font_size=24, color=WHITE),
            Text("using eligibility as an instrument", font=FONT, font_size=24, color=GOLD_MAIN),
            Text("to estimate LATE on compliers", font=FONT, font_size=24, color=WHITE,
                 t2c={"LATE": GOLD_MAIN}),
        ).arrange(DOWN, buff=0.38).move_to(ORIGIN)
        self.play(FadeIn(defn[0], shift=UP * 0.2), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in defn[1:]], lag_ratio=0.4), run_time=1.4)
        self.wait(8.4954)

        # ── Beat 2 (chunk2, 10.50->17.09) Wald(point) -> 2SLS(point+CI) ──
        label = Text("Wald Estimator", font=FONT, font_size=32, color=TEAL_MAIN).move_to(UP * 1.7)
        underline = Line(label.get_corner(DL), label.get_corner(DR), color=TEAL_MAIN, stroke_width=2.5).shift(DOWN * 0.12)
        point = Dot(UP * 0.5, radius=0.13, color=TEAL_MAIN)
        value_lab = MathTex(r"\hat{\tau}", font_size=36).set_color(TEAL_MAIN).next_to(point, RIGHT, buff=0.35)
        dot_cap = Text("point estimate", font=FONT, font_size=16, color=TEAL_MAIN).next_to(point, LEFT, buff=0.35)
        blocked = Text("can't get a confidence interval", font=FONT, font_size=20, color=RED_MAIN).next_to(point, DOWN, buff=0.9)
        self.play(FadeOut(defn, run_time=0.4),
                  FadeIn(label, run_time=0.5), Create(underline, run_time=0.5), FadeIn(point, run_time=0.5),
                  FadeIn(value_lab, run_time=0.5), FadeIn(dot_cap, run_time=0.5),
                  FadeIn(blocked, run_time=0.5))
        self.wait(2.498)
        # Wald -> 2SLS: point/value/caption (TEAL) stay put; label is erased then rewritten
        # (fade out with underline, then Write back in) instead of an instant swap.
        label2 = Text("2SLS", font=FONT, font_size=32, color=GOLD_MAIN).move_to(label)
        underline2 = Line(label2.get_corner(DL), label2.get_corner(DR), color=GOLD_MAIN, stroke_width=2.5).shift(DOWN * 0.12)
        self.play(FadeOut(VGroup(label, underline), shift=UP * 0.15, run_time=0.4))
        self.play(Write(label2, run_time=0.5), Create(underline2, run_time=0.5))
        # red text is replaced by a GOLD CI bar + TEAL dashed connector; add a "confidence
        # interval" caption and a Flash on the point for a fuller closing-scene payoff.
        cx, py = point.get_center()[0], point.get_center()[1]
        ci_cy = py - 1.0
        ci_half = 0.85
        ci_bar = Line(np.array([cx - ci_half, ci_cy, 0]), np.array([cx + ci_half, ci_cy, 0]), color=GOLD_MAIN, stroke_width=5)
        ci_capL = Line(np.array([cx - ci_half, ci_cy - 0.16, 0]), np.array([cx - ci_half, ci_cy + 0.16, 0]), color=GOLD_MAIN, stroke_width=5)
        ci_capR = Line(np.array([cx + ci_half, ci_cy - 0.16, 0]), np.array([cx + ci_half, ci_cy + 0.16, 0]), color=GOLD_MAIN, stroke_width=5)
        ci_center = Dot(np.array([cx, ci_cy, 0]), radius=0.09, color=TEAL_MAIN)
        connector = DashedLine(point.get_bottom() + DOWN * 0.05, np.array([cx, ci_cy + 0.2, 0]),
                               color=TEAL_MAIN, stroke_width=1.6, dash_length=0.08)
        ci_fig = VGroup(ci_bar, ci_capL, ci_capR, ci_center)
        ci_cap = Text("confidence interval", font=FONT, font_size=18, color=GOLD_MAIN).next_to(ci_bar, DOWN, buff=0.28)
        self.play(FadeOut(blocked, run_time=0.3),
                  Create(connector, run_time=0.5), Create(ci_fig, run_time=0.6), FadeIn(ci_cap, run_time=0.6),
                  Flash(point, color=GOLD_MAIN, flash_radius=0.4, line_length=0.22, num_lines=10, run_time=0.6))
        self.wait(2.097)

        # ── Beat 3 (chunk3, 17.09->25.15) closing (WAIT_TAIL) ─────
        done = VGroup(
            Text("Sharp RDD  ✓", font=FONT, font_size=32, color=GREEN_MAIN),
            Text("Fuzzy RDD  ✓", font=FONT, font_size=32, color=GREEN_MAIN),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.4)
        nextv = Text("See you in the next video with another causal inference method", font=FONT, font_size=22, color=GRAY_MID).move_to(DOWN * 1.3)
        self.play(FadeOut(VGroup(label2, underline2, point, value_lab, dot_cap, connector, ci_fig, ci_cap), run_time=0.4),
                  FadeIn(done, shift=UP * 0.15, run_time=0.6))
        self.wait(4.467)
        self.play(FadeIn(nextv, shift=UP * 0.1, run_time=0.5))
        # WAIT_TAIL = (25.150 + 0.45) - 22.157 - 0.5 = 2.943
        self.wait(2.943)
