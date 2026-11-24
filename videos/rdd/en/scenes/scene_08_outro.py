from manim import *

from videos.rdd.shared.common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    GREEN_MAIN,
    WHITE,
    YELLOW_MAIN,
)


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
