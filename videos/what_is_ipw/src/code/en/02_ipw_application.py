from manim import *
import numpy as np

ICON = "/Users/jhkim/Desktop/personal_study/causal/causal-studio/videos/assets/tabler-icons/icons/outline"

SEVERE = "#b07cff"   # severe
MILD = "#39d98a"     # mild


class IPWApplication(Scene):
    """Scene 02 (EN). Same animations as KO, English text, resynced.
    timings: build/audio/02_ipw_application_en.timings.json (total 148.81s, 36 chunks)
    """

    def construct(self):
        self.camera.background_color = "#0a0a0a"
        self.t = 0.0

        def go_to(target_time):
            dt = target_time - self.t
            if dt > 0:
                self.wait(dt)
                self.t += dt

        def play_at(target_time, *anims, run_time=0.5):
            go_to(target_time)
            self.play(*anims, run_time=run_time)
            self.t += run_time

        def dot(color, r=0.16, fill=0.9):
            return Circle(radius=r, stroke_color=color, stroke_width=2).set_fill(color, opacity=fill)

        def ring(color, r=0.16):
            return Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(color, opacity=0.0)

        def people_block(n_sev, n_mild, cols=4, r=0.16, buff=0.16):
            g = VGroup(*[dot(SEVERE, r) for _ in range(n_sev)],
                       *[dot(MILD, r) for _ in range(n_mild)])
            rows = int(np.ceil(len(g) / cols))
            g.arrange_in_grid(rows=rows, cols=cols, buff=buff)
            return g

        def icon(name, color, height=1.0):
            m = SVGMobject(f"{ICON}/{name}.svg")
            m.set_stroke(color, width=3)
            m.set_fill(color, opacity=0)
            m.scale_to_fit_height(height)
            return m

        UNIT = 0.62

        def make_bar(days, color, y, x0, unit=UNIT):
            bar = RoundedRectangle(width=days * unit, height=0.46, corner_radius=0.07,
                                   stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.5)
            bar.move_to([x0 + days * unit / 2, y, 0])
            return bar

        # Beat 1 — recap of Simpson's paradox (chunk1~5)
        recap = Text("Let's recap", font_size=30, color=GRAY_A, weight=BOLD).to_edge(UP, buff=0.7)
        row_group = VGroup(
            Text("Within groups", font_size=30, color=GRAY_A, weight=BOLD),
            Text("medicine → faster", font_size=32, color=GREEN_B, weight=BOLD),
            Text("✓", font_size=40, color=GREEN_B, weight=BOLD),
        ).arrange(RIGHT, buff=0.5).move_to(UP * 1.55)
        row_total = VGroup(
            Text("Overall", font_size=30, color=GRAY_A, weight=BOLD),
            Text("medicine → slower", font_size=32, color=RED_B, weight=BOLD),
            Text("✗", font_size=40, color=RED_B, weight=BOLD),
        ).arrange(RIGHT, buff=0.5).move_to(UP * 0.45)
        paradox = Text("Simpson's Paradox", font_size=40, color=ORANGE, weight=BOLD).move_to(DOWN * 1.6)
        why = Text("Why does this happen?", font_size=34, color=YELLOW, weight=BOLD).move_to(DOWN * 2.9)

        play_at(0.3, FadeIn(recap), run_time=0.35)
        play_at(2.4, FadeIn(row_group, shift=UP * 0.1), run_time=0.45)        # chunk2
        play_at(7.5, FadeIn(row_total, shift=UP * 0.1), run_time=0.45)        # chunk3
        play_at(18.9, FadeIn(paradox, shift=UP * 0.1), run_time=0.5)          # chunk4
        play_at(21.5, FadeIn(why), run_time=0.4)                             # chunk5

        # Beat 2 — group makeup with dots + emphasis (chunk6~10)
        title2 = Text("Simpson's Paradox", font_size=34, color=ORANGE, weight=BOLD).to_edge(UP, buff=0.45)
        legend = VGroup(
            dot(SEVERE, 0.13), Text("Severe", font_size=22, color=SEVERE, weight=BOLD),
            dot(MILD, 0.13), Text("Mild", font_size=22, color=MILD, weight=BOLD),
        ).arrange(RIGHT, buff=0.22).next_to(title2, DOWN, buff=0.25)
        treat_block = people_block(5, 2, cols=4).scale(1.05).move_to(LEFT * 3.4 + DOWN * 0.3)
        treat_lbl = Text("Took medicine", font_size=27, color=BLUE_B, weight=BOLD).next_to(treat_block, UP, buff=0.4)
        ctrl_block = people_block(1, 2, cols=3).scale(1.05).move_to(RIGHT * 3.4 + DOWN * 0.3)
        ctrl_lbl = Text("No medicine", font_size=27, color=RED_B, weight=BOLD).next_to(ctrl_block, UP, buff=0.4)
        diff_note = Text("The two groups differed from the start", font_size=30, color=GRAY_A, weight=BOLD).move_to(DOWN * 2.9)
        treat_box = SurroundingRectangle(VGroup(treat_lbl, treat_block), color=BLUE_B, buff=0.25, corner_radius=0.15)
        ctrl_box = SurroundingRectangle(VGroup(ctrl_lbl, ctrl_block), color=RED_B, buff=0.25, corner_radius=0.15)

        play_at(23.1, FadeOut(recap, row_group, row_total, paradox, why),
                FadeIn(title2, legend), run_time=0.4)                          # chunk6
        play_at(25.3, FadeIn(treat_lbl), LaggedStartMap(FadeIn, treat_block, lag_ratio=0.12), run_time=1.0)  # chunk7
        play_at(26.7, Create(treat_box),
                *[Indicate(treat_block[i], color=SEVERE, scale_factor=1.4) for i in range(5)], run_time=1.3)
        play_at(28.4, FadeOut(treat_box), run_time=0.3)
        play_at(30.3, FadeIn(ctrl_lbl), LaggedStartMap(FadeIn, ctrl_block, lag_ratio=0.15), run_time=0.9)    # chunk8
        play_at(31.6, Create(ctrl_box),
                *[Indicate(ctrl_block[i], color=MILD, scale_factor=1.4) for i in range(1, 3)], run_time=1.3)
        play_at(33.4, FadeOut(ctrl_box), run_time=0.3)
        play_at(36, FadeIn(diff_note, shift=UP * 0.1), run_time=0.5)        # chunk9
        play_at(45.3, FadeOut(title2, legend, treat_block, treat_lbl, ctrl_block, ctrl_lbl, diff_note), run_time=0.3)

        # Beat 3 — confounder (+ treatment→outcome arrow) (chunk11~12)
        conf = VGroup(
            Text("Confounder", font_size=36, color=PURPLE_A, weight=BOLD),
            Text("Severe / Mild", font_size=26, color=GRAY_B, weight=BOLD),
        ).arrange(DOWN, buff=0.15).move_to(UP * 1.9)
        node_t = Text("Took medicine?", font_size=30, color=BLUE_B, weight=BOLD).move_to(LEFT * 3.3 + DOWN * 1.4)
        node_y = Text("Recovery time", font_size=30, color=GREEN_B, weight=BOLD).move_to(RIGHT * 3.3 + DOWN * 1.4)
        a1 = Arrow(conf.get_bottom(), node_t.get_top(), color=PURPLE_A, stroke_width=5, buff=0.25)
        a2 = Arrow(conf.get_bottom(), node_y.get_top(), color=PURPLE_A, stroke_width=5, buff=0.25)
        a3 = Arrow(node_t.get_right(), node_y.get_left(), color=BLUE_B, stroke_width=5, buff=0.3)

        play_at(46.5, FadeIn(conf, shift=DOWN * 0.1), run_time=0.5)           # chunk11
        play_at(48.3, GrowArrow(a1), GrowArrow(a2), FadeIn(node_t, node_y), run_time=0.7)
        play_at(49.8, GrowArrow(a3), run_time=0.6)
        play_at(51.9, Indicate(conf[1], color=PURPLE_A, scale_factor=1.2), run_time=0.8)  # chunk12

        # Beat 4 — idea + per-individual weight (chunk15~17)
        idea = Text("What if both groups had the same mix?", font_size=38, color=YELLOW, weight=BOLD).move_to(UP * 1.6)
        keep = Text("Keep the data as is", font_size=30, color=GRAY_A, weight=BOLD).move_to(UP * 0.4)
        ppl = VGroup(dot(SEVERE), dot(SEVERE), dot(MILD), dot(SEVERE), dot(MILD)).arrange(RIGHT, buff=0.9).move_to(DOWN * 0.9)
        badges = VGroup(*[Text("×?", font_size=22, color=ORANGE, weight=BOLD).next_to(d, UP, buff=0.12) for d in ppl])
        wgt_note = Text("Give each person a weight", font_size=34, color=ORANGE, weight=BOLD).move_to(DOWN * 2.1)

        play_at(58.3, FadeOut(conf, node_t, node_y, a1, a2, a3),
                FadeIn(idea, shift=UP * 0.1), run_time=0.5)                    # chunk15
        play_at(64.1, FadeIn(keep), run_time=0.4)                            # chunk16
        play_at(65.4, LaggedStartMap(FadeIn, ppl, lag_ratio=0.1),
                LaggedStartMap(FadeIn, badges, shift=DOWN * 0.1, lag_ratio=0.1),
                FadeIn(wgt_note), run_time=1.3)

        # Beat 5 — probability of taking medicine (chunk17~20)
        prob_box = RoundedRectangle(width=11.5, height=4.6, corner_radius=0.25,
                                    stroke_color=GRAY_B, stroke_width=2, fill_opacity=0).move_to(UP * 0.1)
        prob_title = Text("Probability of taking medicine", font_size=34, color=WHITE, weight=BOLD).move_to(prob_box.get_top() + DOWN * 0.5)
        sev_lbl = Text("Severe", font_size=26, color=SEVERE, weight=BOLD).move_to(LEFT * 4.85 + UP * 0.55)
        mild_lbl = Text("Mild", font_size=26, color=MILD, weight=BOLD).move_to(LEFT * 4.85 + DOWN * 1.2)
        LEFTX = -3.0
        sev_circ = VGroup(*[ring(SEVERE, 0.24) for _ in range(6)]).arrange(RIGHT, buff=0.26)
        sev_circ.move_to([0, 0.55, 0]).shift(RIGHT * (LEFTX - sev_circ.get_left()[0]))
        mild_circ = VGroup(*[ring(MILD, 0.24) for _ in range(4)]).arrange(RIGHT, buff=0.26)
        mild_circ.move_to([0, -1.2, 0]).shift(RIGHT * (LEFTX - mild_circ.get_left()[0]))
        sev_cnt = Text("5 of 6", font_size=22, color=SEVERE, weight=BOLD).move_to(RIGHT * 4.1 + UP * 0.9)
        sev_frac = MathTex(r"\tfrac{5}{6}\approx 83\%", color=SEVERE).scale(0.8).move_to(RIGHT * 4.1 + UP * 0.25)
        mild_cnt = Text("2 of 4", font_size=22, color=MILD, weight=BOLD).move_to(RIGHT * 4.1 + DOWN * 0.85)
        mild_frac = MathTex(r"\tfrac{2}{4}=50\%", color=MILD).scale(0.8).move_to(RIGHT * 4.1 + DOWN * 1.5)
        legend2 = Text("Colored = took medicine", font_size=22, color=GRAY_B, weight=BOLD).move_to(prob_box.get_bottom() + UP * 0.4)

        play_at(70.2, FadeOut(idea, keep, ppl, badges, wgt_note),
                Create(prob_box), FadeIn(prob_title), run_time=0.6)           # chunk17
        play_at(71.9, FadeIn(sev_lbl, mild_lbl),
                LaggedStartMap(FadeIn, VGroup(*sev_circ, *mild_circ), lag_ratio=0.1),
                FadeIn(legend2), run_time=1.4)                                # chunk18
        play_at(76.4, *[sev_circ[i].animate.set_fill(SEVERE, opacity=0.9) for i in range(5)],
                FadeIn(sev_cnt), run_time=1.3)                               # chunk19
        play_at(81.3, Write(sev_frac), run_time=0.7)
        play_at(84.7, *[mild_circ[i].animate.set_fill(MILD, opacity=0.9) for i in range(2)],
                FadeIn(mild_cnt), run_time=1.1)                              # chunk20
        play_at(87.5, Write(mild_frac), run_time=0.7)
        beat5 = VGroup(prob_box, prob_title, sev_lbl, sev_circ, sev_cnt, sev_frac,
                       mild_lbl, mild_circ, mild_cnt, mild_frac, legend2)

        # Beat 6 — weight = 1/prob, pull the people out of the probability box (chunk21~24)
        play_at(90.2, beat5.animate.scale(0.5).to_edge(LEFT, buff=0.3), run_time=0.7)  # chunk21
        whead = Text("Weight = 1 ÷ probability", font_size=32, color=ORANGE, weight=BOLD).move_to(RIGHT * 2.7 + UP * 2.55)
        link = Arrow(beat5.get_right() + UP * 0.5, whead.get_left() + DOWN * 0.2,
                     color=ORANGE, stroke_width=4, buff=0.2)

        def dd_cluster(flags, color, y):
            g = VGroup(*[(dot(color, 0.11) if f else ring(color, 0.11)) for f in flags]).arrange(RIGHT, buff=0.08)
            g.move_to([1.2, y, 0])
            return g

        dd1 = dd_cluster([True] * 5, SEVERE, 1.35)
        dd2 = dd_cluster([False], SEVERE, 0.25)
        dd3 = dd_cluster([True] * 2, MILD, -0.85)
        dd4 = dd_cluster([False] * 2, MILD, -1.95)

        def wbody(label, color, tex, anchor):
            lab = Text(label, font_size=19, color=color, weight=BOLD)
            m = MathTex(tex, color=color).scale(0.66)
            body = VGroup(lab, m).arrange(RIGHT, buff=0.26)
            body.next_to(anchor, RIGHT, buff=0.3)
            return body

        b1 = wbody("Severe · med", SEVERE, r"1 \div \tfrac{5}{6} = 1.2", dd1)
        b2 = wbody("Severe · no med", SEVERE, r"1 \div \tfrac{1}{6} = 6", dd2)
        b3 = wbody("Mild · med", MILD, r"1 \div \tfrac{2}{4} = 2", dd3)
        b4 = wbody("Mild · no med", MILD, r"1 \div \tfrac{2}{4} = 2", dd4)
        rare = Text("Rarer cases count more", font_size=23, color=YELLOW, weight=BOLD).move_to([2.6, -2.95, 0])

        play_at(91.2, GrowArrow(link), FadeIn(whead), run_time=0.5)          # chunk21
        play_at(93.6, FadeIn(rare, shift=UP * 0.08), run_time=0.4)          # chunk22
        play_at(97.4, TransformFromCopy(VGroup(*[sev_circ[i] for i in range(5)]), dd1),
                FadeIn(b1, shift=RIGHT * 0.1), run_time=0.9)                  # chunk23
        play_at(100.2, TransformFromCopy(VGroup(sev_circ[5]), dd2),
                FadeIn(b2, shift=RIGHT * 0.1), run_time=0.9)
        play_at(102.1, Indicate(b2[1], color=YELLOW, scale_factor=1.2), run_time=0.7)
        play_at(104.2, TransformFromCopy(VGroup(*[mild_circ[i] for i in range(2)]), dd3),
                FadeIn(b3, shift=RIGHT * 0.1), run_time=0.8)                  # chunk24
        play_at(106, TransformFromCopy(VGroup(*[mild_circ[i] for i in range(2, 4)]), dd4),
                FadeIn(b4, shift=RIGHT * 0.1), run_time=0.8)
        play_at(107.1, FadeOut(beat5, link, whead, dd1, dd2, dd3, dd4, b1, b2, b3, b4, rare), run_time=0.35)

        # Beat 7 — reweight to balance (chunk25~28)
        btitle = Text("After reweighting", font_size=34, color=ORANGE, weight=BOLD).to_edge(UP, buff=0.4)
        bt_t = people_block(5, 2, cols=4, r=0.14, buff=0.2).move_to(LEFT * 3.0 + UP * 1.15)
        bt_t_l = Text("Med", font_size=22, color=BLUE_B, weight=BOLD).next_to(bt_t, UP, buff=0.2)
        bt_c = people_block(1, 2, cols=3, r=0.14, buff=0.2).move_to(RIGHT * 3.0 + UP * 1.15)
        bt_c_l = Text("No med", font_size=22, color=RED_B, weight=BOLD).next_to(bt_c, UP, buff=0.2)
        orig_l = Text("Before", font_size=22, color=GRAY_B, weight=BOLD).move_to(LEFT * 5.4 + UP * 1.15)
        bt_t_badges = VGroup(
            *[Text("×1.2", font_size=14, color=ORANGE, weight=BOLD).next_to(bt_t[i], DOWN, buff=0.05) for i in range(5)],
            *[Text("×2", font_size=14, color=ORANGE, weight=BOLD).next_to(bt_t[i], DOWN, buff=0.05) for i in range(5, 7)],
        )
        bt_c_badges = VGroup(
            Text("×6", font_size=15, color=YELLOW, weight=BOLD).next_to(bt_c[0], DOWN, buff=0.05),
            *[Text("×2", font_size=14, color=ORANGE, weight=BOLD).next_to(bt_c[i], DOWN, buff=0.05) for i in range(1, 3)],
        )
        af_t = people_block(6, 4, cols=5, r=0.14, buff=0.2).move_to(LEFT * 3.0 + DOWN * 1.7)
        af_c = people_block(6, 4, cols=5, r=0.14, buff=0.2).move_to(RIGHT * 3.0 + DOWN * 1.7)
        after_l = Text("After", font_size=22, color=GRAY_B, weight=BOLD).move_to(LEFT * 5.4 + DOWN * 1.7)
        approx = MathTex(r"\approx", color=GREEN_B).scale(1.6).move_to(DOWN * 1.7)
        arr_t = Arrow(bt_t.get_bottom() + DOWN * 0.15, af_t.get_top(), color=ORANGE, stroke_width=4, buff=0.15)
        arr_c = Arrow(bt_c.get_bottom() + DOWN * 0.15, af_c.get_top(), color=ORANGE, stroke_width=4, buff=0.15)
        balance_note = Text("Same severe/mild mix in both groups now", font_size=26, color=GRAY_A, weight=BOLD).to_edge(DOWN, buff=0.35)
        ipw_name = Text("Inverse Probability Weighting (IPW)", font_size=30, color=ORANGE, weight=BOLD).next_to(btitle, DOWN, buff=0.12)

        play_at(108.4, FadeIn(btitle, bt_t, bt_t_l, orig_l, bt_c, bt_c_l), run_time=0.5)  # chunk25
        play_at(109.4, LaggedStartMap(FadeIn, bt_t_badges, shift=DOWN * 0.05, lag_ratio=0.05),
                LaggedStartMap(FadeIn, bt_c_badges, shift=DOWN * 0.05, lag_ratio=0.05), run_time=1.0)
        play_at(112.8, GrowArrow(arr_t), GrowArrow(arr_c), run_time=0.5)       # chunk26
        play_at(113.6, Indicate(bt_c_badges[0], color=YELLOW, scale_factor=1.6),
                LaggedStartMap(FadeIn, af_t, lag_ratio=0.06),
                LaggedStartMap(FadeIn, af_c, lag_ratio=0.06), FadeIn(after_l), run_time=2.0)
        play_at(119.7, FadeIn(approx, scale=1.2), FadeIn(balance_note), run_time=0.6)  # chunk27
        play_at(125.1, FadeIn(ipw_name, shift=DOWN * 0.1), run_time=0.5)     # chunk28
        play_at(127.6, FadeOut(btitle, ipw_name, bt_t, bt_t_l, bt_c, bt_c_l, orig_l, approx,
                                bt_t_badges, bt_c_badges, af_t, af_c, after_l, arr_t, arr_c, balance_note), run_time=0.4)

        # Beat 8 — weighted average: general formula first → groups (chunk29~34)
        dtitle = Text("Weighted average comparison", font_size=34, color=WHITE, weight=BOLD).to_edge(UP, buff=0.35)
        gnum = Text("Sum of (days × weight)", font_size=24, color=WHITE, weight=BOLD)
        gbar = Line(LEFT, RIGHT, color=GRAY_A, stroke_width=2.5).set_width(gnum.width + 0.5)
        gden = Text("Sum of weights", font_size=24, color=GRAY_A, weight=BOLD)
        gfrac = VGroup(gnum, gbar, gden).arrange(DOWN, buff=0.12)
        glbl = Text("Weighted avg =", font_size=26, color=ORANGE, weight=BOLD)
        general = VGroup(glbl, gfrac).arrange(RIGHT, buff=0.3).move_to(UP * 1.7)

        def calc_block(days_sev, days_mild, result, color_lbl, label, y):
            def term(grp_label, expr, color):
                lbl = Text(grp_label, font_size=18, color=color, weight=BOLD)
                m = MathTex(expr, color=color).scale(0.72)
                return VGroup(lbl, m).arrange(DOWN, buff=0.08)
            sev_chip = term("Sev", rf"{days_sev}\times 6", SEVERE)
            mild_chip = term("Mild", rf"{days_mild}\times 4", MILD)
            plus = MathTex("+", color=WHITE).scale(0.8)
            numer = VGroup(sev_chip, plus, mild_chip).arrange(RIGHT, buff=0.28)
            bar = Line(LEFT, RIGHT, color=GRAY_A, stroke_width=2.5)
            bar.set_width(numer.width + 0.4).next_to(numer, DOWN, buff=0.12)
            denom = MathTex("10", color=GRAY_A).scale(0.8).next_to(bar, DOWN, buff=0.08)
            frac = VGroup(numer, bar, denom)
            eq = MathTex(rf"= {result}", color=color_lbl).scale(1.0).next_to(frac, RIGHT, buff=0.35)
            lab = Text(label, font_size=24, color=color_lbl, weight=BOLD).next_to(frac, LEFT, buff=0.45)
            grp = VGroup(lab, frac, eq).scale(0.9)
            grp.move_to([0.5, y, 0])
            return grp

        treat_calc = calc_block(7, 2, "5", BLUE_B, "Took med", 0.1)
        ctrl_calc = calc_block(8, 3, "6", RED_B, "No med", -1.45)
        meaning = Text("6 = severe weight · 4 = mild weight · 10 = total",
                       font_size=20, color=GRAY_B, weight=BOLD).to_edge(DOWN, buff=0.4)

        play_at(129.4, FadeIn(dtitle), run_time=0.35)                        # chunk29
        play_at(132.6, FadeIn(general, shift=UP * 0.08), run_time=0.6)       # chunk30
        play_at(138.2, FadeIn(treat_calc, shift=UP * 0.08), run_time=0.6)    # chunk31
        play_at(142.9, FadeIn(ctrl_calc, shift=UP * 0.08), FadeIn(meaning), run_time=0.6)  # chunk32

        bx0 = -1.3
        b_treat = make_bar(5.6, BLUE, y=1.0, x0=bx0)
        b_ctrl = make_bar(4.7, RED, y=-0.3, x0=bx0)
        b_t_lbl = Text("Took medicine", font_size=24, color=BLUE_B, weight=BOLD)
        b_t_lbl.move_to([bx0 - 0.3 - b_t_lbl.width / 2, 1.0, 0])
        b_c_lbl = Text("No medicine", font_size=24, color=RED_B, weight=BOLD)
        b_c_lbl.move_to([bx0 - 0.3 - b_c_lbl.width / 2, -0.3, 0])
        b_t_val = Text("5.6d", font_size=24, color=BLUE_B, weight=BOLD).next_to(b_treat, RIGHT, buff=0.15)
        b_c_val = Text("4.7d", font_size=24, color=RED_B, weight=BOLD).next_to(b_ctrl, RIGHT, buff=0.15)
        state_lbl = Text("Before reweighting", font_size=26, color=GRAY_A, weight=BOLD).to_edge(UP, buff=1.15)

        play_at(146.8, FadeOut(dtitle, general, treat_calc, ctrl_calc, meaning),
                FadeIn(state_lbl, b_t_lbl, b_c_lbl),
                GrowFromEdge(b_treat, LEFT), GrowFromEdge(b_ctrl, LEFT),
                FadeIn(b_t_val, b_c_val), run_time=0.8)                       # chunk33
        nt_treat = make_bar(5.0, BLUE, y=1.0, x0=bx0)
        nt_ctrl = make_bar(6.0, RED, y=-0.3, x0=bx0)
        state2 = Text("After IPW", font_size=26, color=ORANGE, weight=BOLD).to_edge(UP, buff=1.15)
        eff = Text("Medicine: 1 day faster ✓", font_size=32, color=GREEN_B, weight=BOLD).to_edge(DOWN, buff=0.7)
        play_at(149.5,
                Transform(b_treat, nt_treat), Transform(b_ctrl, nt_ctrl),
                ReplacementTransform(state_lbl, state2),
                b_t_val.animate.become(Text("5d", font_size=24, color=BLUE_B, weight=BOLD).next_to(nt_treat, RIGHT, buff=0.15)),
                b_c_val.animate.become(Text("6d", font_size=24, color=RED_B, weight=BOLD).next_to(nt_ctrl, RIGHT, buff=0.15)),
                run_time=1.6)
        play_at(151.7, FadeIn(eff, shift=UP * 0.1), run_time=0.5)
        play_at(154, Indicate(eff, color=GREEN_B, scale_factor=1.1), run_time=0.8)  # chunk34
        play_at(158.2, FadeOut(state2, b_treat, b_ctrl, b_t_lbl, b_c_lbl, b_t_val, b_c_val, eff), run_time=0.4)

        # Beat 9 — conclusion: observational → IPW → like a randomized trial (chunk35~36)
        obs_t = people_block(4, 1, cols=3, r=0.17, buff=0.14)
        obs_c = people_block(1, 3, cols=2, r=0.17, buff=0.14)
        obs = VGroup(obs_t, obs_c).arrange(RIGHT, buff=0.7).move_to(LEFT * 4.2 + UP * 0.2)
        obs_lbl = Text("Observational data", font_size=28, color=GRAY_A, weight=BOLD).next_to(obs, DOWN, buff=0.5)
        shuffle = icon("arrows-shuffle", ORANGE, height=1.3).move_to(UP * 0.2)
        shuffle_lbl = Text("IPW", font_size=34, color=ORANGE, weight=BOLD).next_to(shuffle, DOWN, buff=0.25)
        arr = Arrow(LEFT * 1.7, RIGHT * 1.7, color=GRAY_B, stroke_width=5).move_to(UP * 0.2)
        bal_t = people_block(3, 2, cols=3, r=0.17, buff=0.14)
        bal_c = people_block(3, 2, cols=3, r=0.17, buff=0.14)
        bal = VGroup(bal_t, bal_c).arrange(RIGHT, buff=0.7).move_to(RIGHT * 4.2 + UP * 0.2)
        bal_lbl = Text("Like a randomized trial", font_size=28, color=GREEN_B, weight=BOLD).next_to(bal, DOWN, buff=0.5)
        concl = Text("Now we can compare it like a randomized trial", font_size=30, color=WHITE, weight=BOLD).to_edge(DOWN, buff=0.6)

        play_at(159.4, FadeIn(obs, shift=RIGHT * 0.1), FadeIn(obs_lbl), run_time=0.7)  # chunk35
        play_at(161.6, GrowArrow(arr), FadeIn(shuffle, shuffle_lbl), run_time=0.7)
        play_at(163.6, FadeIn(bal, shift=RIGHT * 0.1), FadeIn(bal_lbl), run_time=0.8)
        play_at(165.1, FadeIn(concl, shift=UP * 0.1), run_time=0.6)          # chunk36

        go_to(171.1)
