from manim import *

from videos.rdd.shared.common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


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
