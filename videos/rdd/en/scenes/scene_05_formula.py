from manim import *

from videos.rdd.shared.common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


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
