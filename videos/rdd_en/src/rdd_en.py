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


class Scene02SharpVsFuzzy(Scene):
    """
    Scene 02: sharp_vs_fuzzy (English)
    Audio: 41.45s (4 chunks)

    Beat1 chunk1  ( 0.00~ 3.67s)  intro title
    Beat2 chunk2  ( 3.67~16.67s)  Sharp RDD graph — 0→1 complete jump
    Beat3 chunk3  (16.67~36.92s)  Fuzzy RDD graph — partial jump
    Beat4 chunk4  (36.92~41.45s)  Summary: Sharp focus + separate video for Fuzzy
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~3.67s) ─────────────────────────
        intro = VGroup(
            Text("Two Forms of RDD", font=FONT, font_size=38, color=WHITE),
            VGroup(
                Text("Sharp", font=FONT, font_size=34, color=BLUE_MAIN),
                Text(" vs ", font=FONT, font_size=34, color=WHITE),
                Text("Fuzzy", font=FONT, font_size=34, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.15),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(intro[0], shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(intro[1], shift=UP * 0.2), run_time=0.8)
        self.wait(1.57)
        self.play(FadeOut(intro), run_time=0.5)  # chunk1 end ~3.67s

        # ── Beat 2 (chunk2: 3.67~16.67s, 13.0s) ─────────────
        # New: Sharp RDD title + treatment probability graph (0→1 complete jump)
        # Focus: treatment probability jumps from 0 to 1 at cutoff
        # Remove: FadeOut → Beat3
        sharp_title = Text("Sharp Design", font=FONT, font_size=36, color=BLUE_MAIN)
        sharp_desc  = Text(
            "Crossing the cutoff fully determines treatment — probability goes 0 → 1",
            font=FONT, font_size=20, color=WHITE,
        )
        sharp_header = VGroup(sharp_title, sharp_desc).arrange(DOWN, buff=0.3).move_to(UP * 2.8)

        axes_s, step_s, cutoff_s = self._make_sharp_graph()
        graph_s = VGroup(axes_s, step_s, cutoff_s).scale(0.9).move_to(DOWN * 0.3)

        self.play(FadeIn(sharp_header, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(axes_s), run_time=0.8)
        self.play(Create(cutoff_s), run_time=0.5)
        self.play(Create(step_s), run_time=1.0)
        self.wait(9.90)  # chunk2 end ~16.67s

        # ── Beat 3 (chunk3: 16.67~36.92s, 20.25s) ────────────
        # Remove: Sharp content
        # New: Fuzzy RDD title + partial jump graph
        # Focus: probability jumps at cutoff but not 0→1
        self.play(FadeOut(VGroup(sharp_header, graph_s)), run_time=0.6)

        fuzzy_title = Text("Fuzzy Design", font=FONT, font_size=36, color=RED_MAIN)
        fuzzy_desc  = Text(
            "Treatment probability jumps at the cutoff — but not all the way from 0 to 1",
            font=FONT, font_size=20, color=WHITE,
        )
        fuzzy_header = VGroup(fuzzy_title, fuzzy_desc).arrange(DOWN, buff=0.3).move_to(UP * 2.8)

        axes_f, step_f, cutoff_f = self._make_fuzzy_graph()
        graph_f = VGroup(axes_f, step_f, cutoff_f).scale(0.9).move_to(DOWN * 0.3)

        self.play(FadeIn(fuzzy_header, shift=DOWN * 0.2), run_time=0.8)
        self.play(Create(axes_f), run_time=0.8)
        self.play(Create(cutoff_f), run_time=0.5)
        self.play(Create(step_f), run_time=1.2)
        self.wait(16.35)  # chunk3 end ~36.92s

        # ── Beat 4 (chunk4: 36.92~41.45s, 4.53s) ─────────────
        # Remove: Fuzzy content
        # New: summary — Sharp RDD focus
        self.play(FadeOut(VGroup(fuzzy_header, graph_f)), run_time=0.6)

        summary = VGroup(
            Text("This video focuses on", font=FONT, font_size=26, color=WHITE),
            Text("Sharp RDD", font=FONT, font_size=52, color=BLUE_MAIN),
            Text("Fuzzy RDD → covered in a separate video", font=FONT, font_size=24, color=WHITE),
        ).arrange(DOWN, buff=0.45).move_to(ORIGIN)

        self.play(FadeIn(summary, shift=UP * 0.3), run_time=0.8)
        self.wait(3.51)  # chunk4 + WAIT_TAIL

    # ── helpers ──────────────────────────────────────────────

    def _make_axes(self):
        axes = Axes(
            x_range=[340, 401, 10],
            y_range=[-0.15, 1.35, 0.5],
            x_length=7.5,
            y_length=4.0,
            axis_config={"color": WHITE, "stroke_width": 1.2, "include_tip": False},
            x_axis_config={"numbers_to_include": [350, 360, 370, 380, 390]},
            y_axis_config={"numbers_to_include": [0, 0.5, 1]},
        )
        x_title = Text("CSAT Score (pts)", font=FONT, font_size=18, color=WHITE).next_to(
            axes.x_axis.get_right(), RIGHT, buff=0.12
        )
        y_title = (
            Text("Treatment Prob.", font=FONT, font_size=16, color=WHITE)
            .rotate(PI / 2)
            .next_to(axes.y_axis.get_top(), UP, buff=0.1)
        )
        cutoff_line = DashedLine(
            axes.c2p(370, -0.05), axes.c2p(370, 1.2),
            color=YELLOW_MAIN, dash_length=0.12, stroke_width=2.5,
        )
        cutoff_label = Text("Cutoff (370 pts)", font=FONT, font_size=16, color=YELLOW_MAIN).next_to(
            axes.c2p(370, 1.2), UP, buff=0.05
        )
        return VGroup(axes, x_title, y_title), VGroup(cutoff_line, cutoff_label), axes

    def _make_sharp_graph(self):
        axes_vg, cutoff_vg, axes = self._make_axes()
        left_line  = Line(axes.c2p(340, 0.0), axes.c2p(370, 0.0), color=RED_MAIN,  stroke_width=5)
        right_line = Line(axes.c2p(370, 1.0), axes.c2p(400, 1.0), color=BLUE_MAIN, stroke_width=5)
        jump_line  = Line(axes.c2p(370, 0.0), axes.c2p(370, 1.0), color=GRAY_MID,  stroke_width=2, stroke_opacity=0.7)
        dot_open   = Circle(radius=0.10, color=RED_MAIN,  fill_opacity=0, stroke_width=3).move_to(axes.c2p(370, 0.0))
        dot_closed = Dot(axes.c2p(370, 1.0), radius=0.10, color=BLUE_MAIN, fill_opacity=1)
        step_vg = VGroup(left_line, right_line, jump_line, dot_open, dot_closed)
        return axes_vg, step_vg, cutoff_vg

    def _make_fuzzy_graph(self):
        axes_vg, cutoff_vg, axes = self._make_axes()
        left_line  = axes.plot(
            lambda x: 0.1 + (0.2 - 0.1) / 30 * (x - 340),
            x_range=[340, 370], color=RED_MAIN, stroke_width=5,
        )
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
    Scene 03: key_assumptions (English)
    Audio: 71.41s (5 chunks)

    Beat1 chunk1  ( 0.00~13.42s)  intro title + credit score example setup flow
    Beat2 chunk2  (13.42~27.44s)  Assumption 1: Continuity — credit score graph + jump arrow
    Beat3 chunk3  (27.44~48.62s)  Continuity violation — house/apartment comparison panels
    Beat4 chunk4  (48.62~55.31s)  Assumption 2: Local Randomization
    Beat5 chunk5  (55.31~71.41s)  Manipulation warning
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~13.42s, 13.42s) ────────────────
        title = Text("Key Assumptions of RDD", font=FONT, font_size=40, color=WHITE).move_to(ORIGIN)
        self.play(FadeIn(title, shift=UP * 0.3), run_time=0.8)
        self.wait(2.0)
        self.play(FadeOut(title), run_time=0.6)

        setup_lbl = Text("This example", font=FONT, font_size=20, color=GRAY_MID).move_to(UP * 2.8)

        def _box(txt1, txt2, fill, stroke):
            bg = RoundedRectangle(corner_radius=0.15, width=2.8, height=1.0,
                fill_color=fill, fill_opacity=1, stroke_color=stroke, stroke_width=1.5)
            body = VGroup(
                Text(txt1, font=FONT, font_size=18, color=WHITE),
                Text(txt2, font=FONT, font_size=13, color=GRAY_MID),
            ).arrange(DOWN, buff=0.06).move_to(bg.get_center())
            return VGroup(bg, body)

        rv_box    = _box("Credit Score", "(Running Variable)", "#1e3a5f", BLUE_MAIN)
        treat_box = _box("Mortgage Loan Approval", "(Treatment)",       "#1a3a2a", GREEN_MAIN)
        out_box   = _box("Home Purchase Rate", "(Outcome)",           "#3a1a1a", RED_MAIN)

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
        self.wait(7.02)
        self.play(FadeOut(flow_all), run_time=0.6)  # ~13.42s

        # ── Beat 2 (chunk2: 13.42~27.44s, 14.02s) ────────────
        header1 = VGroup(
            Text("Assumption 1", font=FONT, font_size=22, color=WHITE),
            Text("Continuity", font=FONT, font_size=34, color=BLUE_MAIN),
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
        x_lbl = Text("Credit Score (pts)", font=FONT, font_size=18, color=WHITE).next_to(
            axes.x_axis.get_right(), RIGHT, buff=0.12
        )
        y_lbl = (
            Text("Home Purchase Rate (%)", font=FONT, font_size=15, color=WHITE)
            .rotate(PI / 2)
            .next_to(axes.y_axis.get_top(), UP, buff=0.08)
        )

        y0_fn = lambda x: 10 + (x - 650) * 0.3
        y1_fn = lambda x: y0_fn(x) + 20

        y0_obs = axes.plot(y0_fn, x_range=[650, 700], color=RED_MAIN,  stroke_width=4.5)
        y1_obs = axes.plot(y1_fn, x_range=[700, 750], color=BLUE_MAIN, stroke_width=4.5)
        y0_cf  = axes.plot(y0_fn, x_range=[700, 750], color=RED_MAIN,  stroke_width=2.5, stroke_opacity=0.35)
        y1_cf  = axes.plot(y1_fn, x_range=[650, 700], color=BLUE_MAIN, stroke_width=2.5, stroke_opacity=0.35)
        y0_tag = Text("No Loan", font=FONT, font_size=15, color=RED_MAIN).next_to(
            axes.c2p(665, y0_fn(665)), UP, buff=0.12
        )
        y1_tag = Text("Loan Approved", font=FONT, font_size=15, color=BLUE_MAIN).next_to(
            axes.c2p(735, y1_fn(735)), UP, buff=0.12
        )
        cutoff_ln  = DashedLine(axes.c2p(700, 0), axes.c2p(700, 65), color=YELLOW_MAIN, stroke_width=2.5)
        cutoff_lbl = Text("Cutoff (700 pts)", font=FONT, font_size=14, color=YELLOW_MAIN).next_to(
            axes.c2p(700, 65), UP, buff=0.05
        )
        jump_arrow = DoubleArrow(
            axes.c2p(700, y0_fn(700) + 1), axes.c2p(700, y1_fn(700) - 1),
            color=GREEN_MAIN, buff=0, stroke_width=3, tip_length=0.15,
        )
        jump_tag = Text("Treatment Effect", font=FONT, font_size=18, color=GREEN_MAIN).next_to(
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
        self.wait(5.0)
        self.play(Create(jump_arrow), FadeIn(jump_tag), run_time=0.8)
        self.wait(4.72)  # chunk2 end ~27.44s

        # ── Beat 3 (chunk3: 27.44~48.62s, 21.18s) ────────────
        self.play(FadeOut(VGroup(graph_base, jump_vg)), run_time=0.7)

        viol_title = Text("What if this assumption breaks down?", font=FONT, font_size=22, color=RED_MAIN)
        viol_title.next_to(header1, DOWN, buff=0.25)

        # left panel: credit score < 700
        apt  = self._make_apartment_icon(color=GREEN_MAIN, size=1.1)
        l_body = VGroup(
            Text("Credit Score < 700", font=FONT, font_size=17, color=GREEN_MAIN),
            apt,
            Text("✓ Eligible for public rental", font=FONT, font_size=17, color=GREEN_MAIN),
            Text("✗ No mortgage approval", font=FONT, font_size=17, color=RED_MAIN),
        ).arrange(DOWN, buff=0.22)
        l_bg = RoundedRectangle(corner_radius=0.18, width=4.0, height=3.7,
            fill_color="#0d1f0f", fill_opacity=1, stroke_color=GREEN_MAIN, stroke_width=1.5)
        l_bg.move_to(l_body.get_center())
        left_panel = VGroup(l_bg, l_body).move_to(LEFT * 3.1 + DOWN * 0.4)

        # right panel: credit score ≥ 700
        house = self._make_house_icon(color=BLUE_MAIN, size=1.1)
        r_body = VGroup(
            Text("Credit Score ≥ 700", font=FONT, font_size=17, color=BLUE_MAIN),
            house,
            Text("✓ Mortgage approved", font=FONT, font_size=17, color=GREEN_MAIN),
            Text("✗ Loses rental eligibility", font=FONT, font_size=17, color=RED_MAIN),
        ).arrange(DOWN, buff=0.22)
        r_bg = RoundedRectangle(corner_radius=0.18, width=4.0, height=3.7,
            fill_color="#0d0f1f", fill_opacity=1, stroke_color=BLUE_MAIN, stroke_width=1.5)
        r_bg.move_to(r_body.get_center())
        right_panel = VGroup(r_bg, r_body).move_to(RIGHT * 3.1 + DOWN * 0.4)

        c_line = DashedLine(UP * 1.6, DOWN * 2.4, color=YELLOW_MAIN, stroke_width=2, dash_length=0.14)
        c_lbl  = Text("700 pts", font=FONT, font_size=20, color=YELLOW_MAIN).next_to(c_line, UP, buff=0.1)

        question = Text(
            "Higher home purchase rate = loan effect?  Or loss of rental eligibility?",
            font=FONT, font_size=17, color=WHITE,
        ).move_to(DOWN * 3.0)

        self.play(FadeIn(viol_title, shift=DOWN * 0.15), run_time=0.6)
        self.play(
            FadeIn(left_panel,  shift=RIGHT * 0.25),
            FadeIn(right_panel, shift=LEFT  * 0.25),
            run_time=0.8,
        )
        self.play(Create(c_line), FadeIn(c_lbl), run_time=0.5)
        self.play(FadeIn(question, shift=UP * 0.15), run_time=0.5)
        self.wait(18.08)  # chunk3 end ~48.62s

        # ── Beat 4 (chunk4: 48.62~55.31s, 6.69s) ─────────────
        self.play(
            FadeOut(VGroup(header1, viol_title, left_panel, right_panel, c_line, c_lbl, question)),
            run_time=0.7,
        )

        header2 = VGroup(
            Text("Assumption 2", font=FONT, font_size=22, color=WHITE),
            Text("Local Randomization", font=FONT, font_size=34, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.4).move_to(UP * 1.5)

        local_body2 = VGroup(
            Text("Units must be unable to precisely manipulate their running variable", font=FONT, font_size=21, color=WHITE),
            Text("→ Near the cutoff, quasi-random assignment holds", font=FONT, font_size=21, color=WHITE),
        ).arrange(DOWN, buff=0.35).move_to(DOWN * 0.5)

        self.play(FadeIn(header2, shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(local_body2[0], shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(local_body2[1], shift=UP * 0.2), run_time=0.6)
        self.wait(3.99)  # chunk4 end ~55.31s

        # ── Beat 5 (chunk5: 55.31~71.41s, 16.10s) ────────────
        self.play(FadeOut(VGroup(header2, local_body2)), run_time=0.7)

        warning = VGroup(
            Text("Manipulation", font=FONT, font_size=36, color=RED_MAIN),
            Text("If a customer in the 690s files a complaint to inflate their score,", font=FONT, font_size=19, color=WHITE),
            Text("or a bank officer intentionally adjusts a client's score —", font=FONT, font_size=19, color=WHITE),
            Text("local randomization is violated.", font=FONT, font_size=24, color=RED_MAIN),
            Text("→ Must be tested before analysis", font=FONT, font_size=26, color=YELLOW_MAIN),
        ).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        self.play(FadeIn(warning[0], shift=DOWN * 0.2), run_time=0.8)
        self.play(FadeIn(warning[1], shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(warning[2], shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(warning[3], shift=UP * 0.1), run_time=0.5)
        self.play(FadeIn(warning[4], shift=UP * 0.1), run_time=0.5)
        self.wait(12.58)  # chunk5 + WAIT_TAIL

    # ── helpers ──────────────────────────────────────────────

    def _make_house_icon(self, color=BLUE_MAIN, size=1.0):
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
    Scene 04: components (English)
    Audio: 58.21s (6 chunks)

    Beat1 chunk1  ( 0.00~ 3.67s)  title: three core concepts
    Beat2 chunk2  ( 3.67~21.04s)  ① Running Variable
    Beat3 chunk3  (21.04~28.56s)  ② Cutoff
    Beat4 chunk4  (28.56~42.63s)  ③ Potential Outcomes — table
    Beat5 chunk5  (42.63~50.20s)  ? = Counterfactual highlight
    Beat6 chunk6  (50.20~58.21s)  90-pt student outside RDD range
    """

    def construct(self):
        # ── Beat 1 ───────────────────────────────────────────
        title = VGroup(
            Text("Three Core Concepts", font=FONT, font_size=44, color=WHITE),
            Text("Running Variable · Cutoff · Potential Outcomes",
                 font=FONT, font_size=24, color=GRAY_MID),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.6)
        self.wait(1.77)
        self.play(FadeOut(title), run_time=0.5)

        # ── Beat 2 ───────────────────────────────────────────
        header1 = VGroup(
            Text("①", font=FONT, font_size=28, color=BLUE_MAIN),
            Text("Running Variable", font=FONT, font_size=36, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 2.9)

        xi_label = MathTex(r"X_i", font_size=72, color=BLUE_MAIN).move_to(UP * 1.5)
        xi_desc = Text(
            "A continuous variable that determines treatment",
            font=FONT, font_size=22, color=WHITE,
        ).next_to(xi_label, DOWN, buff=0.4)
        examples = VGroup(
            self._pill("CSAT Score", BLUE_MAIN),
            self._pill("Age", BLUE_MAIN),
            self._pill("Income Level", BLUE_MAIN),
        ).arrange(RIGHT, buff=0.4).next_to(xi_desc, DOWN, buff=0.4)
        no_manip = Text(
            "※ Units must not be able to manipulate this value",
            font=FONT, font_size=20, color=YELLOW_MAIN,
        ).move_to(DOWN * 2.6)

        self.play(FadeIn(header1, shift=DOWN * 0.2), run_time=0.7)
        self.play(Write(xi_label), run_time=0.6)
        self.play(FadeIn(xi_desc, shift=UP * 0.15), run_time=0.6)
        self.play(FadeIn(examples, shift=UP * 0.15), run_time=0.8)
        self.wait(8.7)
        self.play(FadeIn(no_manip, shift=UP * 0.15), run_time=0.7)
        self.wait(4.07)
        self.play(
            FadeOut(VGroup(header1, xi_label, xi_desc, examples, no_manip)),
            run_time=0.6,
        )

        # ── Beat 3 ───────────────────────────────────────────
        header2 = VGroup(
            Text("②", font=FONT, font_size=28, color=YELLOW_MAIN),
            Text("Cutoff (Threshold)", font=FONT, font_size=36, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 2.9)

        formula = MathTex(
            r"D_i = \mathbf{1}[X_i \geq c]",
            font_size=54, color=WHITE,
        ).move_to(UP * 1.2)

        case1 = VGroup(
            MathTex(r"X_i \geq c", font_size=30, color=BLUE_MAIN),
            Text("→  Treatment ✓", font=FONT, font_size=22, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.3)
        case2 = VGroup(
            MathTex(r"X_i < c", font_size=30, color=RED_MAIN),
            Text("→  Treatment ✗", font=FONT, font_size=22, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.3)
        cases = VGroup(case1, case2).arrange(DOWN, buff=0.35).next_to(formula, DOWN, buff=0.5)

        self.play(FadeIn(header2, shift=DOWN * 0.2), run_time=0.7)
        self.play(Write(formula), run_time=1.0)
        self.play(FadeIn(cases, shift=UP * 0.15), run_time=0.8)
        self.wait(4.42)
        self.play(FadeOut(VGroup(header2, formula, cases)), run_time=0.6)

        # ── Beat 4 ───────────────────────────────────────────
        header3 = VGroup(
            Text("③", font=FONT, font_size=28, color=GREEN_MAIN),
            Text("Potential Outcomes",
                 font=FONT, font_size=32, color=GREEN_MAIN),
        ).arrange(RIGHT, buff=0.3).move_to(UP * 3.0)

        table, q_cells, _ = self._make_po_table()
        table.next_to(header3, DOWN, buff=0.5)

        self.play(FadeIn(header3, shift=DOWN * 0.2), run_time=0.7)
        self.play(FadeIn(table, shift=UP * 0.2), run_time=0.9)
        self.wait(12.47)

        # ── Beat 5 ───────────────────────────────────────────
        q_highlights = VGroup(*[
            SurroundingRectangle(q, color=YELLOW_MAIN, buff=0.06, stroke_width=2.5)
            for q in q_cells
        ])
        cf_label = Text(
            "? = Counterfactual",
            font=FONT, font_size=22, color=YELLOW_MAIN,
        ).move_to(DOWN * 2.8)

        self.play(Create(q_highlights), run_time=0.8)
        self.play(FadeIn(cf_label, shift=UP * 0.2), run_time=0.7)
        self.wait(6.07)

        # ── Beat 6 ───────────────────────────────────────────
        self.play(FadeOut(VGroup(q_highlights, cf_label)), run_time=0.5)

        out_label = VGroup(
            Text("Counterfactual for 90-pt student", font=FONT, font_size=22, color=RED_MAIN),
            Text("→  Outside RDD estimation range", font=FONT, font_size=22, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.3).move_to(DOWN * 2.8)

        self.play(FadeIn(out_label, shift=UP * 0.15), run_time=0.7)
        self.wait(7.35)  # chunk6 + WAIT_TAIL

    # ── helpers ──────────────────────────────────────────────

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
        col_labels = ["Student", "Score", "Y₁ (treated)", "Y₀ (untreated)"]
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
    Scene 05: formula (English)
    Audio: 69.89s (10 chunks)

    Beat1  chunk1  ( 0.00~ 5.25s)  LATE header + intuition graph
    Beat2  chunk2  ( 5.25~14.21s)  graph + E[Y|c+]/E[Y|c-] + τ equation
    Beat3  chunk3  (14.21~22.10s)  regression diagram
    Beat4  chunk4  (22.10~31.39s)  full regression equation (center)
    Beat5  chunk5  (31.39~33.16s)  equation moves to top
    Beat6  chunk6  (33.16~38.03s)  β₀ annotation
    Beat7  chunk7  (38.03~43.98s)  β₂ annotation
    Beat8  chunk8  (43.98~50.02s)  β₁·β₃ annotation
    Beat9  chunk9  (50.02~57.68s)  limits + τ̂ = β̂₂ result
    Beat10 chunk10 (57.68~69.89s)  local effect warning
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~5.25s) ─────────────────────────
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
        self.wait(2.45)
        self.play(FadeOut(VGroup(late_header, ax1, ll1, rl1, cl1, jump1, late_lbl)), run_time=0.5)

        # ── Beat 2 (chunk2: 5.25~14.21s, 8.96s) ─────────────
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

        assumption_note = Text(
            "If the assumptions hold, this difference is a pure causal effect.",
            font=FONT, font_size=20, color=WHITE,
        ).move_to(DOWN * 2.6)

        self.play(Create(ax2), Create(ll2), Create(rl2), Create(cl2),
                  FadeIn(scatter2), run_time=0.8)
        self.play(FadeIn(e_r_dot), FadeIn(e_r_lbl), run_time=0.5)
        self.play(FadeIn(e_l_dot), FadeIn(e_l_lbl), run_time=0.5)
        self.wait(1.0)
        self.play(FadeIn(tau_eq, shift=UP * 0.1), run_time=0.6)
        self.wait(2.0)
        self.play(FadeIn(assumption_note, shift=UP * 0.1), run_time=0.6)
        self.wait(2.96)
        self.play(FadeOut(VGroup(ax2, ll2, rl2, cl2, scatter2,
                                 e_r_dot, e_r_lbl, e_l_dot, e_l_lbl,
                                 tau_eq, assumption_note)), run_time=0.6)

        # ── Beat 3 (chunk3: 14.21~22.10s, 7.89s) ─────────────
        ax3, ll3, rl3, cl3 = self._make_rdd_graph(7.0, 4.2, ORIGIN + LEFT * 0.2)
        x_lbl = Text("Score (X)", font=FONT, font_size=18, color=GRAY_MID).next_to(ax3.x_axis, DOWN, buff=0.2)
        y_lbl = Text("GPA", font=FONT, font_size=18, color=GRAY_MID).next_to(ax3.y_axis, LEFT, buff=0.1)
        jump3 = Arrow(ax3.c2p(70, 2.0), ax3.c2p(70, 2.5), buff=0,
                      color=YELLOW_MAIN, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        jump3_lbl = MathTex(r"\hat{\tau}", font_size=26, color=YELLOW_MAIN).next_to(jump3, RIGHT, buff=0.1)
        lbl_left = Text("Untreated", font=FONT, font_size=17, color=RED_MAIN).move_to(ax3.c2p(52, 4.1))
        lbl_right = Text("Treated", font=FONT, font_size=17, color=BLUE_MAIN).move_to(ax3.c2p(87, 4.1))

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
        self.wait(4.19)
        self.play(
            FadeOut(VGroup(ax3, x_lbl, y_lbl, ll3, rl3, cl3,
                           jump3, jump3_lbl, lbl_left, lbl_right)),
            FadeIn(formula, shift=UP * 0.15),
            run_time=0.7,
        )

        # ── Beat 4 (chunk4: 22.10~31.39s, 9.29s) ─────────────
        self.wait(9.29)

        # ── Beat 5 (chunk5: 31.39~33.16s, 1.77s) ─────────────
        self.play(
            formula.animate.move_to(UP * 2.8).scale(0.833),
            run_time=1.0,
        )
        self.wait(0.77)

        # ── Beats 6~8 shared: small graph below formula ──────
        sax, sll, srl, scl = self._make_rdd_graph(6.0, 2.5, DOWN * 0.7)

        # ── Beat 6 (chunk6: 33.16~38.03s, 4.88s) ─────────────
        b0_dot = Dot(sax.c2p(70, 2.0), color=RED_MAIN, radius=0.10)
        b0_h = DashedLine(sax.c2p(40, 2.0), sax.c2p(70, 2.0),
                          color=BLUE_MAIN, stroke_width=1.5, dash_length=0.08)
        b0_ann_lbl = MathTex(r"\beta_0", font_size=22, color=BLUE_MAIN).next_to(
            b0_h.get_center(), UP, buff=0.1)
        b0_ann = VGroup(b0_dot, b0_h, b0_ann_lbl)

        b0_desc = VGroup(
            MathTex(r"\beta_0", font_size=36, color=BLUE_MAIN),
            Text(": Expected outcome just below cutoff (untreated intercept)", font=FONT, font_size=18, color=WHITE),
        ).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.6)

        self.play(Create(sax), Create(sll), Create(srl), Create(scl), run_time=0.8)
        self.play(FadeIn(b0_ann), run_time=0.5)
        self.play(formula[1].animate.set_color(BLUE_MAIN), FadeIn(b0_desc), run_time=0.5)
        self.wait(2.58)
        self.play(formula[1].animate.set_color(WHITE), FadeOut(VGroup(b0_ann, b0_desc)), run_time=0.5)

        # ── Beat 7 (chunk7: 38.03~43.98s, 5.94s) ─────────────
        b2_arrow = Arrow(sax.c2p(70, 2.0), sax.c2p(70, 2.5), buff=0,
                         color=YELLOW_MAIN, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        b2_ann_lbl = MathTex(r"\beta_2", font_size=22, color=YELLOW_MAIN).next_to(b2_arrow, RIGHT, buff=0.1)
        b2_ann = VGroup(b2_arrow, b2_ann_lbl)

        b2_desc = VGroup(
            MathTex(r"\beta_2", font_size=36, color=YELLOW_MAIN),
            Text(": Jump at cutoff = treatment effect", font=FONT, font_size=19, color=WHITE),
        ).arrange(RIGHT, buff=0.2).move_to(DOWN * 2.6)

        self.play(GrowArrow(b2_arrow), FadeIn(b2_ann_lbl), run_time=0.6)
        self.play(formula[5].animate.set_color(YELLOW_MAIN), FadeIn(b2_desc), run_time=0.5)
        self.wait(4.34)
        self.play(formula[5].animate.set_color(WHITE), FadeOut(VGroup(b2_ann, b2_desc)), run_time=0.5)

        # ── Beat 8 (chunk8: 43.98~50.02s, 6.04s) ─────────────
        mid_l = Dot(sax.c2p(55, 2.0 + 0.015*(55-70)), color=RED_MAIN, radius=0.08)
        b1_ann_lbl = VGroup(
            MathTex(r"\beta_1", font_size=18, color=RED_MAIN),
            Text("(Slope)", font=FONT, font_size=14, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.05).next_to(mid_l, UP + LEFT, buff=0.05)
        b1_ann = VGroup(mid_l, b1_ann_lbl)

        mid_r = Dot(sax.c2p(85, 2.5 + 0.02*(85-70)), color=BLUE_MAIN, radius=0.08)
        b3_ann_lbl = VGroup(
            MathTex(r"\beta_1\!+\!\beta_3", font_size=18, color=BLUE_MAIN),
            Text("(Slope)", font=FONT, font_size=14, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.05).next_to(mid_r, UP + RIGHT, buff=0.05)
        b3_ann = VGroup(mid_r, b3_ann_lbl)

        b13_desc = VGroup(
            VGroup(
                MathTex(r"\beta_1", font_size=32, color=RED_MAIN),
                Text(": Untreated slope", font=FONT, font_size=18, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                MathTex(r"\beta_3", font_size=32, color=BLUE_MAIN),
                Text(": Change in slope on treated side", font=FONT, font_size=18, color=WHITE),
            ).arrange(RIGHT, buff=0.2),
        ).arrange(DOWN, buff=0.2).move_to(DOWN * 2.55)

        self.play(FadeIn(b1_ann), FadeIn(b3_ann), run_time=0.7)
        self.play(
            formula[3].animate.set_color(RED_MAIN),
            formula[7].animate.set_color(BLUE_MAIN),
            FadeIn(b13_desc),
            run_time=0.5,
        )
        self.wait(4.34)
        self.play(
            formula[3].animate.set_color(WHITE),
            formula[7].animate.set_color(WHITE),
            FadeOut(VGroup(b1_ann, b3_ann, b13_desc)),
            run_time=0.5,
        )

        # ── Beat 9 (chunk9: 50.02~57.68s, 7.66s) ─────────────
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
        self.wait(6.26)

        # ── Beat 10 (chunk10: 57.68~69.89s, 12.21s) ──────────
        self.play(
            FadeOut(VGroup(sax, sll, srl, scl, formula, limits_group, tau_result)),
            run_time=0.7,
        )

        local_header = Text(
            "Local Effect", font=FONT, font_size=30, color=YELLOW_MAIN,
        ).move_to(UP * 1.8)

        local_desc = Text(
            "RDD estimates the treatment effect only for units near the cutoff.",
            font=FONT, font_size=22, color=WHITE,
        ).move_to(UP * 0.6)

        example_text = VGroup(
            Text("If the scholarship cutoff is 370 on the Korean CSAT,", font=FONT, font_size=19, color=GRAY_MID),
            Text("we cannot use RDD to learn how a scholarship would affect a student who scored 200.", font=FONT, font_size=19, color=GRAY_MID),
        ).arrange(DOWN, buff=0.15).move_to(DOWN * 0.6)

        self.play(FadeIn(local_header, shift=DOWN * 0.2), run_time=0.7)
        self.play(FadeIn(local_desc, shift=UP * 0.1), run_time=0.6)
        self.play(FadeIn(example_text, shift=UP * 0.1), run_time=0.6)
        self.wait(9.64)  # chunk10 + WAIT_TAIL

    # ── helpers ──────────────────────────────────────────────

    def _make_rdd_graph(self, x_length, y_length, position):
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
    Scene 06: visualization (English)
    Audio: 56.14s (8 chunks)

    Beat1 chunk1  ( 0.00~ 2.46s)  title: RDD Visualization
    Beat2 chunk2  ( 2.46~ 7.71s)  three layers of information intro
    Beat3 chunk3  ( 7.71~13.93s)  scatter plot (color-coded by group)
    Beat4 chunk4  (13.93~19.09s)  regression lines (fitted independently)
    Beat5 chunk5  (19.09~25.59s)  discontinuous jump = treatment effect
    Beat6 chunk6  (25.59~33.76s)  core of RDD + caution preview
    Beat7 chunk7  (33.76~45.42s)  causal interpretation only near cutoff
    Beat8 chunk8  (45.42~56.14s)  slopes allowed to differ
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~2.46s) ─────────────────────────
        title = VGroup(
            Text("RDD Visualization", font=FONT, font_size=44, color=WHITE),
            Text("Building intuition through graphs", font=FONT, font_size=26, color=GRAY_MID),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.8)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.6)
        self.wait(0.56)
        self.play(FadeOut(title), run_time=0.5)

        # ── Beat 2 (chunk2: 2.46~7.71s, 5.25s) ──────────────
        info_header = Text("Three layers of information", font=FONT, font_size=34, color=WHITE).move_to(UP * 1.3)
        chips = VGroup(
            self._chip("① Scatter Plot", GRAY_MID),
            self._chip("② Regression Lines", BLUE_MAIN),
            self._chip("③ Discontinuous Jump", YELLOW_MAIN),
        ).arrange(DOWN, buff=0.35).next_to(info_header, DOWN, buff=0.5)

        self.play(FadeIn(info_header, shift=DOWN * 0.2), run_time=0.6)
        for chip in chips:
            self.play(FadeIn(chip, shift=RIGHT * 0.2), run_time=0.45)
        self.wait(2.80)
        self.play(FadeOut(VGroup(info_header, chips)), run_time=0.5)

        # ── shared graph structure (Beats 3~8) ───────────────
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

        y_lbl = Text("GPA", font=FONT, font_size=12, color=GRAY_MID)
        y_lbl.next_to(axes, LEFT, buff=0.1)
        x_lbl = Text("CSAT Score (pts)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_center(), DOWN, buff=0.55)

        cutoff_line = DashedLine(
            axes.c2p(370, 1.5), axes.c2p(370, 4.5),
            color=YELLOW_MAIN, stroke_width=2.5, dash_length=0.12,
        )
        cutoff_lbl = Text("Cutoff (370 pts)", font=FONT, font_size=14, color=YELLOW_MAIN).next_to(
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
                Text("No Scholarship (<370)", font=FONT, font_size=16, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                Dot(color=BLUE_MAIN, radius=0.09),
                Text("Scholarship (≥370)", font=FONT, font_size=16, color=BLUE_MAIN),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        legend.move_to(axes.get_corner(UR) + LEFT * 1.6 + DOWN * 0.4)

        # ── Beat 3 (chunk3: 7.71~13.93s, 6.22s) ─────────────
        self.play(Create(axes), Write(x_lbl), Write(y_lbl), run_time=0.8)
        self.play(Create(cutoff_line), FadeIn(cutoff_lbl), run_time=0.5)
        self.play(FadeIn(scatter_left), run_time=0.7)
        self.play(FadeIn(scatter_right), run_time=0.7)
        self.play(FadeIn(legend), run_time=0.6)
        self.wait(2.92)

        # ── Beat 4 (chunk4: 13.93~19.09s, 5.15s) ─────────────
        left_line = axes.plot(
            lambda x: 2.0 + 0.015 * (x - 370), x_range=[340, 370],
            color=RED_MAIN, stroke_width=4.5,
        )
        right_line = axes.plot(
            lambda x: 2.5 + 0.02 * (x - 370), x_range=[370, 400],
            color=BLUE_MAIN, stroke_width=4.5,
        )
        reg_desc = Text(
            "Regression lines fitted independently on each side",
            font=FONT, font_size=19, color=WHITE,
        ).move_to(DOWN * 3.0)

        self.play(Create(left_line), run_time=0.8)
        self.play(Create(right_line), run_time=0.8)
        self.play(FadeIn(reg_desc), run_time=0.5)
        self.wait(2.65)
        self.play(FadeOut(reg_desc), run_time=0.4)

        # ── Beat 5 (chunk5: 19.09~25.59s, 6.50s) ─────────────
        jump_arrow = DoubleArrow(
            axes.c2p(370, 2.05), axes.c2p(370, 2.45),
            color=YELLOW_MAIN, buff=0, stroke_width=4, tip_length=0.18,
        )
        jump_lbl = VGroup(
            Text("Treatment Effect ", font=FONT, font_size=17, color=YELLOW_MAIN),
            MathTex(r"\hat{\tau}", font_size=22, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.08).next_to(jump_arrow, RIGHT, buff=0.15)

        jump_desc = Text(
            "Intercept difference = estimated treatment effect",
            font=FONT, font_size=19, color=YELLOW_MAIN,
        ).move_to(DOWN * 3.0)

        self.play(Create(jump_arrow), FadeIn(jump_lbl), run_time=0.8)
        self.play(FadeIn(jump_desc), run_time=0.5)
        self.wait(4.80)
        self.play(FadeOut(jump_desc), run_time=0.4)

        # ── Beat 6 (chunk6: 25.59~33.76s, 8.17s) ─────────────
        caution_hint = Text(
            "A few things to keep in mind when reading this graph",
            font=FONT, font_size=19, color=YELLOW_MAIN,
        ).move_to(DOWN * 3.0)

        self.play(FadeIn(caution_hint, shift=UP * 0.15), run_time=0.6)
        self.wait(7.07)
        self.play(FadeOut(VGroup(caution_hint, jump_arrow, jump_lbl)), run_time=0.5)

        # ── Beat 7 (chunk7: 33.76~45.42s, 11.66s) ────────────
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
        near_lbl = Text("Causal\ninterp. zone", font=FONT, font_size=13, color=GREEN_MAIN).next_to(
            near_region, DOWN, buff=0.08
        )

        caution_desc = VGroup(
            Text("Causal interpretation holds only near the cutoff", font=FONT, font_size=19, color=WHITE),
            Text("Scores ~340 vs ~390: GPA gap may reflect ability — not the scholarship", font=FONT, font_size=17, color=RED_MAIN),
        ).arrange(DOWN, buff=0.22).move_to(DOWN * 3.0)

        self.play(FadeIn(near_region), FadeIn(near_lbl), run_time=0.7)
        self.play(FadeIn(caution_desc), run_time=0.6)
        self.wait(9.86)
        self.play(FadeOut(VGroup(near_region, near_lbl, caution_desc)), run_time=0.5)

        # ── Beat 8 (chunk8: 45.42~56.14s, 10.72s) ────────────
        slope_l_lbl = VGroup(
            Text("Slope: ", font=FONT, font_size=15, color=RED_MAIN),
            MathTex(r"\beta_1", font_size=20, color=RED_MAIN),
        ).arrange(RIGHT, buff=0.08).move_to(axes.c2p(350, 2.0 + 0.015 * (350 - 370) + 0.45))

        slope_r_lbl = VGroup(
            Text("Slope: ", font=FONT, font_size=15, color=BLUE_MAIN),
            MathTex(r"\beta_1 + \beta_3", font_size=20, color=BLUE_MAIN),
        ).arrange(RIGHT, buff=0.08).move_to(axes.c2p(390, 2.5 + 0.02 * (390 - 370) + 0.48))

        slope_note = VGroup(
            Text("The slopes on the two sides are allowed to differ", font=FONT, font_size=20, color=BLUE_MAIN),
            Text("GPA growth trends may differ between treated and untreated groups", font=FONT, font_size=17, color=WHITE),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 3.0)

        self.play(FadeIn(slope_l_lbl), FadeIn(slope_r_lbl), run_time=0.7)
        self.play(FadeIn(slope_note), run_time=0.6)
        self.wait(9.43)  # chunk8 + WAIT_TAIL

    # ── helpers ──────────────────────────────────────────────

    def _chip(self, label: str, color: str) -> VGroup:
        bg = RoundedRectangle(
            corner_radius=0.18, width=4.5, height=0.65,
            fill_color=color, fill_opacity=0.12,
            stroke_color=color, stroke_width=1.8,
        )
        txt = Text(label, font=FONT, font_size=22, color=color)
        txt.move_to(bg.get_center())
        if txt.width > bg.width - 0.2:
            txt.scale((bg.width - 0.2) / txt.width)
        return VGroup(bg, txt)


class Scene07Simulation(Scene):
    """
    Scene 07: simulation (English)
    Audio: 46.58s (6 chunks)

    Beat1 chunk1  ( 0.00~ 1.86s)  title
    Beat2 chunk2  ( 1.86~10.31s)  simulation setup: cutoff=370, τ=0.5, N=500
    Beat3 chunk3  (10.31~21.55s)  500 students scatter + DGP formula
    Beat4 chunk4  (21.55~28.00s)  fit regression lines left/right
    Beat5 chunk5  (28.00~39.24s)  results: intercepts 2.02/2.50, τ̂=0.48
    Beat6 chunk6  (39.24~46.58s)  conclusion: RDD recovers treatment effect
    """

    def construct(self):
        # ── Beat 1 (chunk1: 0~1.86s) ─────────────────────────
        title = VGroup(
            Text("Simulation", font=FONT, font_size=44, color=WHITE),
            Text("Can RDD Recover the Treatment Effect?", font=FONT, font_size=26, color=GRAY_MID),
        ).arrange(DOWN, buff=0.4).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.3), run_time=0.7)
        self.play(FadeIn(title[1], shift=UP * 0.2), run_time=0.5)
        self.wait(0.36)
        self.play(FadeOut(title), run_time=0.3)

        # ── Beat 2 (chunk2: 1.86~10.31s, 8.45s) ─────────────
        setup_header = Text("Simulation Setup", font=FONT, font_size=30, color=WHITE).move_to(UP * 1.7)
        setup_items = VGroup(
            self._setup_row("Cutoff", "370 pts  (scholarship threshold)", YELLOW_MAIN),
            self._setup_row("True Treatment Effect", "0.5 GPA points", GREEN_MAIN),
            self._setup_row("Sample Size N", "500 students", BLUE_MAIN),
            self._setup_row("Running Variable", "Korean CSAT Score", GRAY_MID),
        ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).next_to(setup_header, DOWN, buff=0.45)

        self.play(FadeIn(setup_header, shift=DOWN * 0.15), run_time=0.5)
        for item in setup_items:
            self.play(FadeIn(item, shift=RIGHT * 0.15), run_time=0.4)
        self.wait(5.85)
        self.play(FadeOut(VGroup(setup_header, setup_items)), run_time=0.5)

        # ── shared graph structure (Beats 3~6) ───────────────
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

        y_lbl = Text("GPA", font=FONT, font_size=12, color=GRAY_MID)
        y_lbl.next_to(axes, LEFT, buff=0.1)
        x_lbl = Text("CSAT Score (pts)", font=FONT, font_size=14, color=GRAY_MID)
        x_lbl.next_to(axes.x_axis.get_center(), DOWN, buff=0.55)

        cutoff_line = DashedLine(
            axes.c2p(370, 1.0), axes.c2p(370, 4.0),
            color=YELLOW_MAIN, stroke_width=2.5, dash_length=0.12,
        )
        cutoff_lbl = Text("Cutoff (370 pts)", font=FONT, font_size=14, color=YELLOW_MAIN).next_to(
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
                Text("No Scholarship (<370)", font=FONT, font_size=16, color=RED_MAIN),
            ).arrange(RIGHT, buff=0.18),
            VGroup(
                Dot(color=BLUE_MAIN, radius=0.09),
                Text("Scholarship (≥370)", font=FONT, font_size=16, color=BLUE_MAIN),
            ).arrange(RIGHT, buff=0.18),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        legend.move_to(axes.get_corner(UR) + LEFT * 1.5 + DOWN * 0.4)

        # ── Beat 3 (chunk3: 10.31~21.55s, 11.24s) ────────────
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
        self.wait(4.34)
        self.play(FadeOut(dgp_formula), run_time=0.4)

        # ── Beat 4 (chunk4: 21.55~28.00s, 6.45s) ─────────────
        left_line = axes.plot(
            lambda x: 2.02 + 0.015 * (x - 370), x_range=[340, 370],
            color=RED_MAIN, stroke_width=4.5,
        )
        right_line = axes.plot(
            lambda x: 2.50 + 0.015 * (x - 370), x_range=[370, 400],
            color=BLUE_MAIN, stroke_width=4.5,
        )
        reg_desc = Text(
            "Fitting regression lines independently on each side",
            font=FONT, font_size=19, color=WHITE,
        ).move_to(DOWN * 3.1)

        self.play(Create(left_line), run_time=0.9)
        self.play(Create(right_line), run_time=0.9)
        self.play(FadeIn(reg_desc), run_time=0.5)
        self.wait(3.76)
        self.play(FadeOut(reg_desc), run_time=0.4)

        # ── Beat 5 (chunk5: 28.00~39.24s, 11.24s) ────────────
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
            Text("Estimated Effect ", font=FONT, font_size=17, color=YELLOW_MAIN),
            MathTex(r"\hat{\tau}", font_size=22, color=YELLOW_MAIN),
        ).arrange(RIGHT, buff=0.08).next_to(jump_arrow, RIGHT, buff=0.15)

        result_desc = VGroup(
            Text("Left Intercept: 2.02   |   Right Intercept: 2.50", font=FONT, font_size=18, color=WHITE),
            VGroup(
                Text("Estimated Treatment Effect ", font=FONT, font_size=18, color=YELLOW_MAIN),
                MathTex(r"\hat{\tau} = 0.48", font_size=22, color=YELLOW_MAIN),
                Text("  (True: τ = 0.5)", font=FONT, font_size=16, color=GREEN_MAIN),
            ).arrange(RIGHT, buff=0.12),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 3.1)

        self.play(
            FadeIn(left_dot), FadeIn(left_dot_lbl),
            FadeIn(right_dot), FadeIn(right_dot_lbl),
            run_time=0.7,
        )
        self.play(Create(jump_arrow), FadeIn(jump_lbl), run_time=0.7)
        self.play(FadeIn(result_desc), run_time=0.6)
        self.wait(9.24)

        # ── Beat 6 (chunk6: 39.24~46.58s, 7.34s) ─────────────
        conclusion = Text(
            "Fitting separate regression lines → RDD recovers the treatment effect",
            font=FONT, font_size=19, color=GREEN_MAIN,
        ).move_to(DOWN * 3.1)

        self.play(FadeOut(result_desc), FadeIn(conclusion), run_time=0.6)
        self.wait(6.73)  # chunk6 + WAIT_TAIL

    def _setup_row(self, key: str, val: str, color: str) -> VGroup:
        return VGroup(
            Text(f"{key}: ", font=FONT, font_size=19, color=GRAY_MID),
            Text(val, font=FONT, font_size=19, color=color),
        ).arrange(RIGHT, buff=0.12)


class Scene08Outro(Scene):
    """
    Scene 08: outro (English)
    Audio: 24.77s (4 chunks)

    Beat1 chunk1  ( 0.00~ 1.58s)  title: Sharp RDD Key Takeaways
    Beat2 chunk2  ( 1.58~14.12s)  3 summary cards
    Beat3 chunk3  (14.12~19.04s)  Sharp vs Fuzzy comparison panels
    Beat4 chunk4  (19.04~24.77s)  Fuzzy RDD teaser
    """

    def _summary_card(self, icon_tex: str, body: str, accent: str) -> VGroup:
        bar = Rectangle(width=0.07, height=0.55, fill_opacity=1,
                         fill_color=accent, stroke_width=0).set_stroke(width=0)
        label = MathTex(icon_tex, font_size=22, color=accent)
        desc = Text(body, font=FONT, font_size=18, color=WHITE)
        row = VGroup(label, desc).arrange(RIGHT, buff=0.25)
        return VGroup(bar, row).arrange(RIGHT, buff=0.22)

    def construct(self):
        # ── Beat 1 (chunk1: 0~1.58s) ─────────────────────────
        title = VGroup(
            Text("Sharp RDD", font=FONT, font_size=46, color=WHITE),
            Text("Key Takeaways", font=FONT, font_size=28, color=GRAY_MID),
        ).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(title[0], shift=UP * 0.25), run_time=0.6)
        self.play(FadeIn(title[1], shift=UP * 0.15), run_time=0.5)
        self.wait(0.18)
        self.play(FadeOut(title), run_time=0.3)

        # ── Beat 2 (chunk2: 1.58~14.12s, 12.54s) ─────────────
        card1 = self._summary_card(
            r"X_i \geq c \Rightarrow D_i = 1",
            "Crossing cutoff fully determines treatment (Sharp)",
            YELLOW_MAIN,
        )
        card2 = self._summary_card(
            r"\text{Continuity Assumption}",
            "Near the cutoff → quasi-random assignment",
            BLUE_MAIN,
        )
        card3 = self._summary_card(
            r"\hat{\beta}_2 = \text{LATE}",
            "Jump at cutoff = local treatment effect",
            GREEN_MAIN,
        )
        cards = VGroup(card1, card2, card3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        cards.move_to(ORIGIN)

        self.play(FadeIn(card1, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(3.5)
        self.play(FadeIn(card2, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(3.5)
        self.play(FadeIn(card3, shift=RIGHT * 0.15), run_time=0.5)
        self.wait(3.54)
        self.play(FadeOut(cards), run_time=0.5)

        # ── Beat 3 (chunk3: 14.12~19.04s, 4.92s) ─────────────
        sharp_box = VGroup(
            Text("Sharp RDD", font=FONT, font_size=20, color=YELLOW_MAIN),
            MathTex(r"D_i = \mathbf{1}(X_i \geq c)", font_size=22, color=WHITE),
            Text("Crossing cutoff → treatment guaranteed", font=FONT, font_size=15, color=GRAY_MID),
        ).arrange(DOWN, buff=0.22)
        sharp_frame = SurroundingRectangle(sharp_box, color=YELLOW_MAIN,
                                           buff=0.28, corner_radius=0.12, stroke_width=1.5)
        sharp_panel = VGroup(sharp_frame, sharp_box).move_to(LEFT * 3.1)

        fuzzy_box = VGroup(
            Text("Fuzzy RDD", font=FONT, font_size=20, color=BLUE_MAIN),
            MathTex(r"P(D_i{=}1 \mid X_i) \uparrow \text{ at } c",
                    font_size=22, color=WHITE),
            Text("Crossing cutoff → treatment probability increases", font=FONT, font_size=15, color=GRAY_MID),
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
        self.wait(3.72)
        self.play(FadeOut(VGroup(sharp_panel, vs_lbl, fuzzy_panel)), run_time=0.5)

        # ── Beat 4 (chunk4: 19.04~24.77s, 5.73s) ─────────────
        next_label = Text("In the next video", font=FONT, font_size=22, color=GRAY_MID)
        fuzzy_title = Text("Fuzzy RDD", font=FONT, font_size=52, color=BLUE_MAIN)
        teaser = VGroup(next_label, fuzzy_title).arrange(DOWN, buff=0.3).move_to(ORIGIN)

        self.play(FadeIn(next_label, shift=UP * 0.2), run_time=0.5)
        self.play(FadeIn(fuzzy_title, shift=UP * 0.25), run_time=0.6)
        self.wait(4.62)  # chunk4 + WAIT_TAIL
