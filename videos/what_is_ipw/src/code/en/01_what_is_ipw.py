from manim import *
import numpy as np

ICON = "/Users/jhkim/Desktop/personal_study/causal/causal-studio/videos/assets/tabler-icons/icons/outline"


class MedicineQuestionSynced(Scene):
    """Scene 01 (EN) — Simpson's paradox intro. Same animations, English text.
    timings: build/audio/01_medicine_question_en.timings.json (total 70.25s, 17 chunks)
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

        def icon(name, color, height=1.1):
            m = SVGMobject(f"{ICON}/{name}.svg")
            m.set_stroke(color, width=3)
            m.set_fill(color, opacity=0)
            m.scale_to_fit_height(height)
            return m

        UNIT = 0.62

        def make_bar(days, color, y, x0, unit=UNIT):
            bar = RoundedRectangle(width=days * unit, height=0.42, corner_radius=0.07,
                                   stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=0.5)
            bar.move_to([x0 + days * unit / 2, y, 0])
            return bar

        def bar_row(label, days, color, y, x0, fs=24, unit=UNIT):
            lab = Text(label, font_size=fs, color=color, weight=BOLD)
            lab.move_to([x0 - 0.3 - lab.width / 2, y, 0])
            bar = make_bar(days, color, y, x0, unit)
            val = Text(f"{days:g}d", font_size=fs + 2, color=color, weight=BOLD).next_to(bar, RIGHT, buff=0.18)
            return VGroup(lab, bar, val)

        # Beat A — sick → medicine → recover, really the medicine? (chunk2~3)
        sick = icon("mood-sick", RED_B, height=1.5).move_to(LEFT * 3.4 + UP * 0.2)
        happy = icon("mood-happy", GREEN_B, height=1.5).move_to(RIGHT * 3.4 + UP * 0.2)
        rec_arrow = Arrow(sick.get_right(), happy.get_left(), color=WHITE, stroke_width=6, buff=0.5)
        pill = icon("pill", BLUE_B, height=0.95).move_to(UP * 1.45)
        pill_lbl = Text("Med", font_size=26, color=BLUE_B, weight=BOLD).next_to(pill, RIGHT, buff=0.15)
        qbig = Text("?", font_size=120, color=RED, weight=BOLD).move_to(DOWN * 1.7)

        play_at(2, FadeIn(sick, shift=UP * 0.15), run_time=0.4)            # chunk2
        play_at(3.5, GrowArrow(rec_arrow), FadeIn(happy, shift=UP * 0.15), run_time=0.5)
        play_at(4.9, FadeIn(pill, shift=DOWN * 0.15), FadeIn(pill_lbl), run_time=0.4)
        play_at(6.6, FadeIn(qbig, scale=1.2), run_time=0.4)                  # chunk3
        beatA = VGroup(sick, happy, rec_arrow, pill, pill_lbl, qbig)

        # Beat B — title (chunk4)
        title = Text("How to find the true cause?", font_size=40, color=YELLOW, weight=BOLD).move_to(UP * 0.3)
        play_at(9, FadeOut(beatA), FadeIn(title), run_time=0.5)            # chunk4

        # Beat C — what to compare? difference in recovery time (chunk5~6)
        hint = Text("Medicine should help you heal faster, right?", font_size=30, color=GRAY_A, weight=BOLD).move_to(DOWN * 0.4)
        play_at(14.1, title.animate.scale(0.85).to_edge(UP, buff=0.6), FadeIn(hint, shift=UP * 0.1), run_time=0.5)  # chunk5

        g_treat = icon("users", BLUE_B, height=1.2).move_to(LEFT * 3.4 + UP * 0.8)
        t_lbl = Text("Took medicine", font_size=26, color=BLUE_B, weight=BOLD).next_to(g_treat, DOWN, buff=0.25)
        g_ctrl = icon("users", RED_B, height=1.2).move_to(RIGHT * 3.4 + UP * 0.8)
        c_lbl = Text("No medicine", font_size=26, color=RED_B, weight=BOLD).next_to(g_ctrl, DOWN, buff=0.25)
        metric = Text("Difference in recovery time?", font_size=30, color=YELLOW, weight=BOLD).move_to(DOWN * 1.55)
        diff_arrow = DoubleArrow(LEFT * 1.7 + DOWN * 2.15, RIGHT * 1.7 + DOWN * 2.15, color=YELLOW,
                                 stroke_width=5, tip_length=0.22, buff=0.1)

        play_at(17.5, FadeOut(hint),
                FadeIn(g_treat, t_lbl), FadeIn(g_ctrl, c_lbl), run_time=0.5)  # chunk6
        play_at(19.8, FadeIn(metric, shift=UP * 0.08), GrowFromCenter(diff_arrow), run_time=0.5)
        beatC = VGroup(g_treat, t_lbl, g_ctrl, c_lbl, metric, diff_arrow)

        # Beat D — all patients bars: medicine 5.6 > none 4.7 (chunk7~9)
        c_title = Text("All patients", font_size=34, color=GRAY_A, weight=BOLD).to_edge(UP, buff=0.6)
        c_x0 = -1.6
        c_treat = bar_row("Took medicine", 5.6, BLUE, y=0.8, x0=c_x0, fs=26)
        c_ctrl = bar_row("No medicine", 4.7, RED, y=-0.5, x0=c_x0, fs=26)
        harm = Text("Medicine made it worse?", font_size=32, color=RED_B, weight=BOLD).move_to(DOWN * 2.0)
        harm_face = icon("mood-confuzed", RED_B, height=0.7).next_to(harm, LEFT, buff=0.25)

        play_at(23.6, FadeOut(beatC), ReplacementTransform(title, c_title), run_time=0.5)  # chunk7
        play_at(25.9, GrowFromEdge(c_treat[1], LEFT), FadeIn(c_treat[0], c_treat[2]), run_time=0.6)  # chunk8
        play_at(28.8, GrowFromEdge(c_ctrl[1], LEFT), FadeIn(c_ctrl[0], c_ctrl[2]), run_time=0.6)
        play_at(33.3, FadeIn(harm, shift=UP * 0.1), FadeIn(harm_face, shift=UP * 0.1), run_time=0.5)  # chunk9

        # Beat E — trap + split severe/mild (chunk10~11)
        trap = Text("But is that true?", font_size=28, color=YELLOW, weight=BOLD).move_to(DOWN * 2.0)
        play_at(40.3, FadeOut(harm, harm_face), FadeIn(trap, shift=UP * 0.08), run_time=0.45)  # chunk10

        split_title = Text("Now split by severity", font_size=34, color=YELLOW, weight=BOLD).to_edge(UP, buff=0.55)
        play_at(43.8, FadeOut(c_treat, c_ctrl, trap),
                ReplacementTransform(c_title, split_title), run_time=0.5)     # chunk11

        # Beat F — severe (7/8), mild (2/3): medicine shorter in each (chunk12~14)
        d_x0 = -1.9
        sev_head = Text("Severe", font_size=28, color=BLUE_D, weight=BOLD).move_to(LEFT * 5.1 + UP * 1.55)
        sev_t = bar_row("Med", 7, BLUE, y=1.95, x0=d_x0, fs=22)
        sev_c = bar_row("No med", 8, RED, y=1.15, x0=d_x0, fs=22)
        mild_head = Text("Mild", font_size=28, color=PINK, weight=BOLD).move_to(LEFT * 5.1 + DOWN * 1.15)
        mild_t = bar_row("Med", 2, BLUE, y=-0.75, x0=d_x0, fs=22)
        mild_c = bar_row("No med", 3, RED, y=-1.55, x0=d_x0, fs=22)
        sev_ok = Text("−1 day ✓", font_size=24, color=GREEN_B, weight=BOLD).next_to(sev_c, RIGHT, buff=0.5)
        mild_ok = Text("−1 day ✓", font_size=24, color=GREEN_B, weight=BOLD).next_to(mild_c, RIGHT, buff=0.5)

        play_at(47.5, FadeIn(sev_head), GrowFromEdge(sev_t[1], LEFT), FadeIn(sev_t[0], sev_t[2]), run_time=0.55)  # chunk12
        play_at(50.3, GrowFromEdge(sev_c[1], LEFT), FadeIn(sev_c[0], sev_c[2]), run_time=0.55)
        play_at(52.8, FadeIn(sev_ok, shift=LEFT * 0.1), run_time=0.4)
        play_at(56.1, FadeIn(mild_head), GrowFromEdge(mild_t[1], LEFT), FadeIn(mild_t[0], mild_t[2]), run_time=0.55)  # chunk13
        play_at(58.8, GrowFromEdge(mild_c[1], LEFT), FadeIn(mild_c[0], mild_c[2]), run_time=0.55)
        play_at(61.2, FadeIn(mild_ok, shift=LEFT * 0.1), run_time=0.4)
        both_ok = Text("Within each group, medicine clearly helps ✓", font_size=28, color=GREEN_B, weight=BOLD).to_edge(DOWN, buff=0.45)
        play_at(63.5, FadeIn(both_ok, shift=UP * 0.1), run_time=0.5)         # chunk14

        # Beat G — reversal: groups (medicine shorter) → overall (medicine longer) (chunk15)
        rev_title = Text("But combine them all…", font_size=34, color=ORANGE, weight=BOLD).to_edge(UP, buff=0.55)
        ov_x0 = -1.6
        ov_treat = make_bar(5.6, BLUE, y=0.7, x0=ov_x0)
        ov_ctrl = make_bar(4.7, RED, y=-0.6, x0=ov_x0)
        ov_t_lbl = Text("Took medicine", font_size=26, color=BLUE_B, weight=BOLD)
        ov_t_lbl.move_to([ov_x0 - 0.3 - ov_t_lbl.width / 2, 0.7, 0])
        ov_c_lbl = Text("No medicine", font_size=26, color=RED_B, weight=BOLD)
        ov_c_lbl.move_to([ov_x0 - 0.3 - ov_c_lbl.width / 2, -0.6, 0])
        ov_t_val = Text("5.6d", font_size=28, color=BLUE_B, weight=BOLD).next_to(ov_treat, RIGHT, buff=0.18)
        ov_c_val = Text("4.7d", font_size=28, color=RED_B, weight=BOLD).next_to(ov_ctrl, RIGHT, buff=0.18)
        flip = Text("Now medicine looks harmful ✗", font_size=30, color=RED_B, weight=BOLD).to_edge(DOWN, buff=0.5)

        play_at(68.7,
                FadeOut(sev_head, mild_head, sev_ok, mild_ok, both_ok,
                        sev_t[0], sev_t[2], sev_c[0], sev_c[2], mild_t[0], mild_t[2], mild_c[0], mild_c[2]),
                ReplacementTransform(split_title, rev_title), run_time=0.45)  # chunk15
        play_at(69.7,
                ReplacementTransform(VGroup(sev_t[1], mild_t[1]), ov_treat),
                ReplacementTransform(VGroup(sev_c[1], mild_c[1]), ov_ctrl),
                FadeIn(ov_t_lbl, ov_c_lbl, ov_t_val, ov_c_val), run_time=1.3)
        play_at(71.8, FadeIn(flip, shift=UP * 0.1), run_time=0.5)

        # Beat H — why? → IPW (chunk16~17)
        why = Text("Why does this happen?", font_size=36, color=YELLOW, weight=BOLD).move_to(DOWN * 2.6)
        play_at(74.9, FadeIn(why, scale=1.1), run_time=0.4)                  # chunk16

        ipw = Text("IPW", font_size=96, color=ORANGE, weight=BOLD)
        ipw_sub = Text("Inverse Probability Weighting", font_size=34, color=WHITE, weight=BOLD)
        ipw_group = VGroup(ipw, ipw_sub).arrange(DOWN, buff=0.35).move_to(ORIGIN)

        play_at(76.6,
                FadeOut(rev_title, ov_treat, ov_ctrl, ov_t_lbl, ov_c_lbl, ov_t_val, ov_c_val, flip, why),
                run_time=0.35)                                               # chunk17
        play_at(77.05, Write(ipw), run_time=0.6)
        play_at(78.3, FadeIn(ipw_sub, shift=UP * 0.1), run_time=0.4)

        go_to(80)
