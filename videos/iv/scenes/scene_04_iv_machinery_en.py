from manim import *

from iv_common import (
    ACCENT,
    COIN_COLOR,
    COMPLIER,
    CONTROL_COLOR,
    INSTRUMENT,
    SOFT,
    TREAT_COLOR,
    load_scene_timing_durations,
)


class Scene04_IvMachineryEN(Scene):
    """English version of Scene 04. 6 chunks, ~71.16s."""

    WAIT_TAIL = 1.5

    def construct(self):
        d = load_scene_timing_durations("04_iv_machinery_en")

        # Beat 1: intro
        title = Text("Computing LATE", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        intro = Text("The formula is surprisingly simple", font_size=26, color=SOFT).move_to(ORIGIN + UP * 0.3)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(intro), run_time=1.2)
        self.wait(d[0] - 1.9)

        # Beat 2: numerator (with fix: label just below title, bars lower, larger box buff)
        numerator_label = Text("Numerator: score difference from assignment", font_size=22, color=COIN_COLOR).next_to(title, DOWN, buff=0.4)
        score_z1 = Text("Treatment\nassigned avg", font_size=18, color=TREAT_COLOR, line_spacing=0.9)
        score_z0 = Text("Control\nassigned avg", font_size=18, color=CONTROL_COLOR, line_spacing=0.9)
        bar_z1 = Rectangle(width=0.8, height=1.7, color=TREAT_COLOR, fill_opacity=0.7, stroke_width=0)
        bar_z0 = Rectangle(width=0.8, height=1.3, color=CONTROL_COLOR, fill_opacity=0.7, stroke_width=0)
        bar_block_z1 = VGroup(bar_z1, score_z1).arrange(DOWN, buff=0.25)
        bar_block_z0 = VGroup(bar_z0, score_z0).arrange(DOWN, buff=0.25)
        bars = VGroup(bar_block_z1, bar_block_z0).arrange(RIGHT, buff=1.4, aligned_edge=DOWN).move_to(DOWN * 1.1)
        diff_brace = Brace(VGroup(bar_z1, bar_z0), direction=UP, buff=0.25, color=COIN_COLOR)
        diff_text = Text("This difference", font_size=22, color=COIN_COLOR).next_to(diff_brace, UP, buff=0.2)

        self.play(FadeOut(intro), run_time=0.4)
        self.play(FadeIn(numerator_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(bars, shift=UP * 0.15), run_time=1.2)
        self.play(GrowFromCenter(diff_brace), FadeIn(diff_text, shift=DOWN * 0.1), run_time=1.0)
        self.wait(d[1] - 3.3)

        # Beat 3: only compliers create the diff
        explain = Text("Only compliers create this difference", font_size=26, weight=BOLD, color=COMPLIER).move_to(DOWN * 2.7)
        complier_note = Text("(Always-takers / never-takers don't respond to the coin)", font_size=18, color=SOFT).next_to(explain, DOWN, buff=0.2)
        self.play(FadeIn(explain, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(complier_note, shift=UP * 0.05), run_time=0.7)
        numer_box = SurroundingRectangle(VGroup(bars, diff_brace, diff_text), color=COIN_COLOR, buff=0.4)
        self.play(Create(numer_box), run_time=1.0)
        self.wait(d[2] - 2.7)

        # Beat 4: divide by share
        divide_caption = Text("→ Divide by the share of compliers", font_size=26, color=ACCENT).move_to(DOWN * 3.4)
        self.play(FadeOut(complier_note), run_time=0.3)
        self.play(FadeIn(divide_caption, shift=UP * 0.1), run_time=1.0)
        self.wait(d[3] - 1.3)

        # Beat 5: denominator
        previous = VGroup(numerator_label, bars, diff_brace, diff_text,
                          explain, numer_box, divide_caption)
        self.play(FadeOut(previous), run_time=0.7)
        denom_label = Text("Denominator: share the coin moved", font_size=24, color=INSTRUMENT).move_to(UP * 1.6)
        ratio_block_left = self._make_ratio_block("Among treatment\nassigned, used", filled=6, total=8, color=TREAT_COLOR)
        ratio_block_right = self._make_ratio_block("Among control\nassigned, used", filled=2, total=8, color=CONTROL_COLOR)
        ratios = VGroup(ratio_block_left, ratio_block_right).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.2)
        complier_pct = Text("≈ Share of compliers  (6/8 − 2/8 = 50%)", font_size=22, color=COMPLIER).move_to(DOWN * 2.5)

        self.play(FadeIn(denom_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(ratios, shift=UP * 0.15), run_time=1.5)
        self.play(Write(complier_pct), run_time=1.4)
        self.wait(d[4] - 3.6)

        # Beat 6: Wald estimator
        self.play(FadeOut(VGroup(denom_label, ratios, complier_pct)), run_time=0.7)
        wald_title = Text("Wald Estimator", font_size=32, weight=BOLD, color=INSTRUMENT).to_edge(UP, buff=1.2)
        numer_line = Text("Score difference from assignment", font_size=26, color=COIN_COLOR)
        bar = Line(LEFT * 3.5, RIGHT * 3.5, color=WHITE, stroke_width=3)
        denom_line = Text("Share of compliers", font_size=26, color=INSTRUMENT)
        fraction = VGroup(numer_line, bar, denom_line).arrange(DOWN, buff=0.25).move_to(ORIGIN + UP * 0.1)
        equals = Text("=  LATE", font_size=30, weight=BOLD, color=COMPLIER).next_to(fraction, DOWN, buff=0.5)
        meaning = Text("Effect of treatment on a single complier", font_size=22, color=SOFT).next_to(equals, DOWN, buff=0.3)

        self.play(FadeIn(wald_title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(numer_line, shift=UP * 0.1), run_time=0.9)
        self.play(Create(bar), run_time=0.5)
        self.play(FadeIn(denom_line, shift=DOWN * 0.1), run_time=0.9)
        self.play(Write(equals), run_time=1.0)
        self.play(FadeIn(meaning, shift=UP * 0.05), run_time=0.9)
        self.wait(d[5] - 4.9)
        self.wait(self.WAIT_TAIL)

    @staticmethod
    def _make_ratio_block(title_text: str, filled: int, total: int, color: str) -> VGroup:
        title = Text(title_text, font_size=18, color=color, line_spacing=0.9)
        dots = VGroup()
        for i in range(total):
            d = Dot(radius=0.13, color=color if i < filled else GREY_D)
            if i >= filled:
                d.set_fill(opacity=0.3)
            dots.add(d)
        dots.arrange(RIGHT, buff=0.18)
        ratio_text = Text(f"{filled}/{total}", font_size=24, weight=BOLD, color=color)
        block = VGroup(title, dots, ratio_text).arrange(DOWN, buff=0.25)
        return block
