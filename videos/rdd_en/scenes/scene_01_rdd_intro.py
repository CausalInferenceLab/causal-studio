from manim import *

from rdd_en_common import (
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
    Scene 01: rdd_intro (English)
    Script: videos/rdd_en/src/scripts/01_rdd_intro.txt
    Audio: 80.74s (9 chunks)

    Beat1 chunk1  ( 0.00~ 5.76s)  RDD title
    Beat2 chunk2  ( 5.76~15.05s)  University A example setup
    Beat3 chunk3  (15.05~31.76s)  Student cards 369/371 + badges + 2-pt gap
    Beat4 chunk4  (31.76~48.67s)  Causal question + ideal comparison
    Beat5 chunk5  (48.67~52.20s)  Core idea of RDD title
    Beat6 chunk6  (52.20~60.84s)  RDD definition
    Beat7 chunk7  (60.84~67.38s)  RCT ≈ RDD diagram
    Beat8 chunk8  (67.38~76.81s)  Application examples table
    Beat9 chunk9  (76.81~80.74s)  Conclusion
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~5.76s) ─────────────────────────
        # New: RDD intro title 3 lines
        # Focus: "RDD" + "Regression Discontinuity Design"
        # Remove: FadeOut → Beat2
        title = VGroup(
            Text("RDD", font=FONT, font_size=56, color=BLUE_MAIN),
            Text("Regression Discontinuity Design", font=FONT, font_size=26, color=BLUE_MAIN),
            Text("A Method in Causal Inference", font=FONT, font_size=22, color=GRAY_MID),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(title[2], shift=UP * 0.15), run_time=0.4)
        self.wait(3.86)
        self.play(FadeOut(title), run_time=0.3)  # chunk1 end ~5.76s

        # ── Beat 2 (chunk2: 5.76~15.05s, 9.29s) ─────────────
        # New: Example setup text
        # Focus: "University A scholarship: Korean CSAT ≥ 370"
        # Remove: FadeOut → Beat3
        ex_intro = Text("Let's build intuition with an example.", font=FONT, font_size=30, color=GRAY_MID).move_to(UP * 1.0)
        ex_setup = VGroup(
            Text("University A Scholarship Rule:", font=FONT, font_size=28, color=WHITE),
            Text("Korean CSAT ≥ 370 pts", font=FONT, font_size=40, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.35).next_to(ex_intro, DOWN, buff=0.55)

        self.play(FadeIn(ex_intro, shift=DOWN * 0.15), run_time=0.5)
        self.play(FadeIn(ex_setup, shift=DOWN * 0.15), run_time=0.7)
        self.wait(7.58)
        self.play(FadeOut(VGroup(ex_intro, ex_setup)), run_time=0.5)  # chunk2 end ~15.05s

        # ── Beat 3 (chunk3: 15.05~31.76s, 16.72s) ────────────
        # New: Student cards (left/right) → badges → 2-pt gap note (bottom)
        # Focus: 369 pts / 371 pts, only 2 pts apart
        # Remove: diff_note FadeOut → Beat4 (cards/badges stay)
        card_left  = self._student_card("369 pts", "Student A", RED_MAIN).move_to(LEFT * 3)
        card_right = self._student_card("371 pts", "Student B", BLUE_MAIN).move_to(RIGHT * 3)

        self.play(
            FadeIn(card_left,  shift=RIGHT * 0.3),
            FadeIn(card_right, shift=LEFT  * 0.3),
            run_time=1.0,
        )
        self.wait(3.0)

        badge_no  = self._badge("No Scholarship ✗", RED_MAIN).next_to(card_left,  DOWN, buff=0.4)
        badge_yes = self._badge("Scholarship ✓",    GREEN_MAIN).next_to(card_right, DOWN, buff=0.4)

        self.play(
            FadeIn(badge_no,  shift=DOWN * 0.2),
            FadeIn(badge_yes, shift=DOWN * 0.2),
            run_time=0.8,
        )
        self.wait(3.5)

        diff_note = Text(
            "2-pt gap = luck, not ability",
            font=FONT, font_size=24, color=YELLOW_MAIN,
        ).move_to(DOWN * 2.8)

        self.play(FadeIn(diff_note, shift=UP * 0.15), run_time=0.7)
        self.wait(7.72)  # chunk3 end ~31.76s

        # ── Beat 4 (chunk4: 31.76~48.67s, 16.90s) ────────────
        # Keep: cards + badges
        # New: causal question → comparison answer + highlight → equal condition
        # Focus: these two students are the ideal comparison pair
        # Remove: all FadeOut → Beat5
        self.play(FadeOut(diff_note), run_time=0.4)

        question = Text(
            "How to estimate the causal effect of the scholarship on GPA?",
            font=FONT, font_size=22, color=WHITE,
        ).move_to(UP * 2.6)

        self.play(FadeIn(question, shift=DOWN * 0.15), run_time=0.9)
        self.wait(3.0)

        answer = Text(
            "Why not compare exactly these two students?",
            font=FONT, font_size=24, color=YELLOW_MAIN,
        ).next_to(question, DOWN, buff=0.45)

        circle_left  = SurroundingRectangle(card_left,  color=YELLOW_MAIN, buff=0.15, stroke_width=3)
        circle_right = SurroundingRectangle(card_right, color=YELLOW_MAIN, buff=0.15, stroke_width=3)

        self.play(
            FadeIn(answer, shift=DOWN * 0.15),
            Create(circle_left),
            Create(circle_right),
            run_time=0.9,
        )
        self.wait(4.0)

        equal_note = VGroup(
            Text("Essentially identical — except for scholarship status", font=FONT, font_size=19, color=GREEN_MAIN),
            Text("→ The ideal comparison pair", font=FONT, font_size=20, color=GREEN_MAIN),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.8)

        self.play(FadeIn(equal_note, shift=UP * 0.15), run_time=0.7)
        self.wait(7.0)  # chunk4 end ~48.67s

        # ── Beat 5 (chunk5: 48.67~52.20s, 3.53s) ─────────────
        # Remove: all previous elements
        # New: RDD core idea title
        # Focus: "This is the core idea of RDD"
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
            Text("This is the core idea of RDD", font=FONT, font_size=34, color=WHITE),
            Text("Regression Discontinuity Design", font=FONT, font_size=24, color=BLUE_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.8)

        self.play(FadeIn(rdd_title, shift=UP * 0.2), run_time=0.8)
        self.wait(2.13)  # chunk5 end ~52.20s

        # ── Beat 6 (chunk6: 52.20~60.84s, 8.64s) ─────────────
        # Keep: rdd_title
        # New: definition text
        # Focus: crossing a cutoff → compare near cutoff → causal effect
        rdd_def = VGroup(
            Text("When treatment is assigned based on crossing a cutoff,", font=FONT, font_size=21, color=WHITE),
            Text("compare units near the cutoff to estimate the causal effect.", font=FONT, font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.3).next_to(rdd_title, DOWN, buff=0.55)

        self.play(FadeIn(rdd_def, shift=DOWN * 0.15), run_time=0.8)
        self.wait(7.84)  # chunk6 end ~60.84s

        # ── Beat 7 (chunk7: 60.84~67.38s, 6.54s) ─────────────
        # Remove: rdd_title + rdd_def
        # New: RCT ≈ RDD comparison diagram
        # Focus: near cutoff ≈ quasi-random assignment
        self.play(FadeOut(VGroup(rdd_title, rdd_def)), run_time=0.5)

        # ── RCT panel ──
        rct_box = RoundedRectangle(
            corner_radius=0.18, width=4.6, height=3.5,
            fill_color="#111827", fill_opacity=1,
            stroke_color=YELLOW_MAIN, stroke_width=1.5,
        )
        rct_hdr = Text("Randomized Experiment (RCT)", font=FONT, font_size=18, color=YELLOW_MAIN)
        rct_hdr.move_to(rct_box.get_top() + DOWN * 0.45)
        coin_c = Circle(radius=0.38, stroke_color=YELLOW_MAIN, stroke_width=2.5).set_fill("#1F2937", opacity=1)
        coin_q = Text("?", font=FONT, font_size=26, color=YELLOW_MAIN).move_to(coin_c.get_center())
        coin = VGroup(coin_c, coin_q)
        rct_groups = VGroup(
            Text("Treatment", font=FONT, font_size=18, color=GREEN_MAIN),
            Text("|", font=FONT, font_size=18, color=GRAY_MID),
            Text("Control", font=FONT, font_size=18, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.35)
        rct_note = Text("Direct random assignment", font=FONT, font_size=15, color=GRAY_MID)
        rct_inner = VGroup(coin, rct_groups, rct_note).arrange(DOWN, buff=0.3)
        rct_inner.move_to(rct_box.get_center() + DOWN * 0.2)
        rct_panel = VGroup(rct_box, rct_hdr, rct_inner).move_to(LEFT * 3.2)

        # ── center ≈ ──
        approx_sign = Text("≈", font=FONT, font_size=52, color=WHITE)

        # ── RDD panel (mini graph) ──
        rdd_box = RoundedRectangle(
            corner_radius=0.18, width=4.6, height=3.5,
            fill_color="#111827", fill_opacity=1,
            stroke_color=BLUE_MAIN, stroke_width=1.5,
        )
        rdd_hdr = Text("Natural Experiment (RDD)", font=FONT, font_size=18, color=BLUE_MAIN)
        rdd_hdr.move_to(rdd_box.get_top() + DOWN * 0.45)
        mini_axis   = Line(LEFT * 1.35, RIGHT * 1.35, color=GRAY_MID, stroke_width=2)
        mini_cutoff = DashedLine(DOWN * 0.32, UP * 0.32, color=YELLOW_MAIN, stroke_width=2, dash_length=0.1)
        mini_near   = Rectangle(
            width=0.6, height=0.64,
            fill_color=GREEN_MAIN, fill_opacity=0.22,
            stroke_color=GREEN_MAIN, stroke_width=1.5,
        )
        mini_near_lbl   = Text("Near", font=FONT, font_size=12, color=GREEN_MAIN).next_to(mini_near, UP, buff=0.06)
        mini_cutoff_lbl = Text("370", font=FONT, font_size=12, color=YELLOW_MAIN).next_to(mini_cutoff, DOWN, buff=0.27)
        mini_diagram = VGroup(mini_axis, mini_cutoff, mini_near, mini_near_lbl, mini_cutoff_lbl)
        rdd_groups = VGroup(
            Text("Control (<370)", font=FONT, font_size=14, color=RED_MAIN),
            Text("Treatment (≥370)", font=FONT, font_size=14, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.45)
        rdd_note = Text("Near cutoff ≈ random", font=FONT, font_size=16, color=GREEN_MAIN)
        rdd_inner = VGroup(mini_diagram, rdd_groups, rdd_note).arrange(DOWN, buff=0.28)
        rdd_inner.move_to(rdd_box.get_center() + DOWN * 0.2)
        rdd_panel = VGroup(rdd_box, rdd_hdr, rdd_inner).move_to(RIGHT * 3.2)

        self.play(
            FadeIn(rct_panel, shift=LEFT * 0.3),
            FadeIn(approx_sign),
            FadeIn(rdd_panel, shift=RIGHT * 0.3),
            run_time=0.9,
        )
        self.wait(5.14)  # chunk7 end ~67.38s

        # ── Beat 8 (chunk8: 67.38~76.81s, 9.43s) ─────────────
        # Remove: comparison diagram
        # New: application examples table
        # Focus: 4 real-world contexts for RDD
        self.play(
            FadeOut(VGroup(rct_panel, approx_sign, rdd_panel)),
            run_time=0.6,
        )

        header = ["Setting", "Running Variable", "Cutoff", "Treatment"]
        rows = [
            ["Scholarship",     "CSAT score",   "370 pts",          "Scholarship"],
            ["Welfare benefits","Income level",  "50% median income","Financial aid"],
            ["Legal drinking",  "Age",           "Age 19",           "Alcohol purchase"],
            ["Drug insurance",  "Drug price",    "Price threshold",  "Insurance coverage"],
        ]

        table = self._make_table(header, rows)
        table_title = Text("When RDD Can Be Applied", font=FONT, font_size=28, color=BLUE_MAIN)
        table_group = VGroup(table_title, table).arrange(DOWN, buff=0.35).scale(0.78).move_to(ORIGIN)

        self.play(FadeIn(table_group, shift=UP * 0.3), run_time=1.0)
        self.wait(7.83)  # chunk8 end ~76.81s

        # ── Beat 9 (chunk9: 76.81~80.74s, 3.93s) ─────────────
        # Keep: table_group
        # New: closing conclusion
        # Focus: "Wherever there's a rule, RDD can apply"
        conclusion = Text(
            "Wherever a clear rule determines treatment, RDD is worth considering.",
            font=FONT, font_size=18, color=YELLOW_MAIN,
        ).next_to(table_group, DOWN, buff=0.4)

        self.play(FadeIn(conclusion, shift=UP * 0.15), run_time=0.6)
        self.wait(3.83)  # chunk9 + WAIT_TAIL

    # ── helpers ──────────────────────────────────────────────

    def _student_card(self, score: str, name: str, color: str) -> VGroup:
        box = RoundedRectangle(
            corner_radius=0.2, width=3.2, height=2.2,
            fill_color=GRAY_LIGHT, fill_opacity=1,
            stroke_color=color, stroke_width=3,
        )
        score_text = Text(score, font=FONT, font_size=44, color=color)
        name_text  = Text(name,  font=FONT, font_size=22, color=GRAY_DARK)
        content = VGroup(score_text, name_text).arrange(DOWN, buff=0.2)
        content.move_to(box.get_center())
        return VGroup(box, content)

    def _badge(self, label: str, color: str) -> VGroup:
        bg = RoundedRectangle(
            corner_radius=0.15, width=2.8, height=0.6,
            fill_color=color, fill_opacity=0.15,
            stroke_color=color, stroke_width=2,
        )
        txt = Text(label, font=FONT, font_size=20, color=color)
        txt.move_to(bg.get_center())
        if txt.width > bg.width - 0.2:
            txt.scale((bg.width - 0.2) / txt.width)
        return VGroup(bg, txt)

    def _make_table(self, header: list, rows: list) -> VGroup:
        col_widths    = [3.2, 3.0, 3.2, 3.2]
        row_height    = 0.82
        header_height = 0.98
        all_rows      = [header] + rows
        n_cols        = len(header)
        n_rows        = len(all_rows)

        HEADER_BG = "#1A3A6E"
        ODD_BG    = "#EBF5FF"

        cells = VGroup()
        for r_idx, row in enumerate(all_rows):
            is_header = r_idx == 0
            h = header_height if is_header else row_height
            for c_idx, cell_text in enumerate(row):
                w = col_widths[c_idx]
                bg_color = HEADER_BG if is_header else (ODD_BG if r_idx % 2 == 1 else WHITE)
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
                    txt_color  = BLUE_MAIN
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

        outer = RoundedRectangle(
            corner_radius=0.20,
            width=row_groups.width + 0.16,
            height=row_groups.height + 0.16,
            fill_opacity=0,
            stroke_color=BLUE_MAIN,
            stroke_width=2.2,
        ).move_to(row_groups.get_center())

        return VGroup(outer, row_groups, dividers)
