from manim import *

from rdd_en_common import (
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
