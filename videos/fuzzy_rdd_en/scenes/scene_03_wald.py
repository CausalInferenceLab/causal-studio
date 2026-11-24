from manim import *

from fuzzy_rdd_en_common import (
    FONT,
    GOLD_MAIN,
    GRAY_MID,
    TEAL_MAIN,
    WHITE,
)


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
