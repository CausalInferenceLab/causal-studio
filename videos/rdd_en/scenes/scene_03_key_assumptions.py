from manim import *

from rdd_en_common import (
    BLUE_MAIN,
    FONT,
    GRAY_MID,
    GREEN_MAIN,
    RED_MAIN,
    WHITE,
    YELLOW_MAIN,
)


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
