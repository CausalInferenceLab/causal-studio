from manim import *

from videos.rdd.shared.common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


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
