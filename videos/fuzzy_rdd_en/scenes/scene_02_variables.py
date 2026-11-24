from manim import *

from fuzzy_rdd_en_common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    TEAL_MAIN,
    WHITE,
)


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
