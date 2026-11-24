from manim import *

from why_causal_inference_common import (
    ACCENT_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    load_icon,
    load_english_scene_timing_durations as load_scene_timing_durations,
)


class Scene11_RctLimitsAndBeyond(Scene):
    WAIT_TAIL = 1.0

    def construct(self):
        chunk_durations = load_scene_timing_durations("11_rct_limits_and_beyond")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            total = sum(chunk_durations[i - 1] for i in indices) - spent + extra
            if total > 0:
                self.wait(total)

        COST_COLOR = GOLD_D
        ETHICS_COLOR = BLUE_D
        POLICY_COLOR = TEAL_D

        # ── Beat 1 ──
        divider = Line(
            UP * 3.8, DOWN * 3.8,
            stroke_width=1.5, color=NEUTRAL_COLOR, stroke_opacity=0.45,
        )

        rct_lbl = Text("RCT", font_size=60, color=GREEN_D, weight=BOLD)
        rct_check = Text("✓", font_size=52, color=GREEN_D)
        rct_sub = Text("Ideal design", font_size=20, color=GREEN_D)
        rct_left_grp = VGroup(rct_lbl, rct_check, rct_sub).arrange(DOWN, buff=0.22)
        rct_left_grp.move_to(LEFT * 3.2)

        real_lbl = Text("In practice", font_size=34, color=WHITE)
        real_cross = Text("✗", font_size=52, color=RED_D)
        real_sub = Text("not always possible", font_size=20, color=NEUTRAL_COLOR)
        rct_right_grp = VGroup(real_lbl, real_cross, real_sub).arrange(DOWN, buff=0.22)
        rct_right_grp.move_to(RIGHT * 3.2)

        self.play(Create(divider), run_time=0.5)
        self.play(
            FadeIn(rct_left_grp, shift=RIGHT * 0.12),
            FadeIn(rct_right_grp, shift=LEFT * 0.12),
            run_time=0.7,
        )
        wait_for_chunks([1], spent=1.2)

        # ── Beat 2 ──
        self.play(
            FadeOut(divider), FadeOut(rct_left_grp), FadeOut(rct_right_grp),
            run_time=0.5,
        )

        icons_meta = [
            ("coin.svg",          COST_COLOR,   "High cost",      "Billions for large-scale trials",   LEFT * 3.8),
            ("scale.svg",         ETHICS_COLOR, "Ethical limits", "Can't assign smoking or weapons",    ORIGIN),
            ("building-bank.svg", POLICY_COLOR, "Policy scale",   "National-level RCT infeasible",      RIGHT * 3.8),
        ]

        icon_cols_grp = VGroup()
        for icon_file, color, title, desc, pos in icons_meta:
            icon = load_icon(icon_file, color, 1.1)
            title_txt = Text(title, font_size=21, color=color, weight=BOLD)
            desc_txt = Text(desc, font_size=17, color=NEUTRAL_COLOR)
            col = VGroup(icon, VGroup(title_txt, desc_txt).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.28)
            col.move_to(pos + UP * 0.4)
            icon_cols_grp.add(col)

        for col in icon_cols_grp:
            self.play(FadeIn(col, scale=0.82), run_time=0.8)
            self.wait(0.3)

        no_smoking = load_icon("smoking-no.svg", RED_D, 0.65)
        smoke_txt = Text("Can't randomize smoking in pregnant women", font_size=19, color=NEUTRAL_COLOR)
        smoking_row = VGroup(no_smoking, smoke_txt).arrange(RIGHT, buff=0.3)
        smoking_box_rect = SurroundingRectangle(
            smoking_row, buff=0.24, color=NEUTRAL_COLOR,
            stroke_width=1.2, corner_radius=0.1, stroke_opacity=0.45,
        )
        smoking_panel = VGroup(smoking_box_rect, smoking_row)
        smoking_panel.move_to(DOWN * 2.3)

        self.wait(3.5)
        self.play(FadeIn(smoking_panel, shift=UP * 0.06), run_time=0.6)
        wait_for_chunks([2], spent=7.9)

        # ── Beat 3 ──
        self.play(FadeOut(icon_cols_grp), FadeOut(smoking_panel), run_time=0.5)

        question_txt = Text(
            '"If we could run the ideal experiment, how would we design it?"',
            font_size=20, color=ACCENT_COLOR,
        )
        question_box = SurroundingRectangle(
            question_txt, buff=0.3, color=ACCENT_COLOR,
            corner_radius=0.12, stroke_width=1.8,
        )
        question_grp = VGroup(question_box, question_txt)
        question_grp.move_to(UP * 0.6)

        anchor_txt = Text("Benchmark for observational research", font_size=22, color=WHITE)
        anchor_txt.next_to(question_grp, DOWN, buff=0.55)
        anchor_arr = Arrow(
            question_grp.get_bottom() + DOWN * 0.08,
            anchor_txt.get_top() + UP * 0.08,
            stroke_width=2.5, color=NEUTRAL_COLOR, buff=0,
            max_tip_length_to_length_ratio=0.3,
        )

        self.play(FadeIn(question_grp, shift=UP * 0.08), run_time=0.7)
        self.play(GrowArrow(anchor_arr), FadeIn(anchor_txt, shift=UP * 0.05), run_time=0.6)
        wait_for_chunks([3], spent=1.8)

        # ── Beat 4 ──
        self.play(
            FadeOut(question_grp), FadeOut(anchor_arr), FadeOut(anchor_txt),
            run_time=0.5,
        )

        quasi_title = Text("Quasi-experimental methods", font_size=28, color=WHITE, weight=BOLD)
        quasi_title.move_to(UP * 3.0)

        def q_node(label, color, fsize=20):
            txt = Text(label, font_size=fsize, color=color)
            box = SurroundingRectangle(
                txt, buff=0.22, color=color, corner_radius=0.1, stroke_width=1.8,
            )
            return VGroup(box, txt)

        def q_arrow(src, dst, color, stroke=2.2):
            dir_vec = dst.get_center() - src.get_center()
            return Arrow(
                src.get_boundary_point(dir_vec),
                dst.get_boundary_point(-dir_vec),
                buff=0.1, stroke_width=stroke, color=color,
                max_tip_length_to_length_ratio=0.25,
            )

        node_T = q_node("Treatment T", GOLD_D)
        node_Y = q_node("Outcome Y", TEAL_D)
        node_T.move_to(LEFT * 2.6 + UP * 0.2)
        node_Y.move_to(RIGHT * 2.6 + UP * 0.2)

        ty_y = node_T.get_center()[1]
        arr_T_Y = Arrow(
            [node_T.get_right()[0], ty_y, 0],
            [node_Y.get_left()[0], ty_y, 0],
            buff=0, stroke_width=3.0, color=ACCENT_COLOR,
            max_tip_length_to_length_ratio=0.25,
        )
        goal_lbl = Text("Causal effect of interest", font_size=17, color=NEUTRAL_COLOR)
        goal_lbl.next_to(arr_T_Y, DOWN, buff=0.2)

        self.play(FadeIn(quasi_title), run_time=0.4)
        self.play(FadeIn(node_T), FadeIn(node_Y), run_time=0.6)
        self.play(Create(arr_T_Y), FadeIn(goal_lbl), run_time=0.6)
        self.wait(3.0)

        node_X = q_node("Confounder X", QUESTION_COLOR, fsize=18)
        node_X.move_to(UP * 2.0)
        arr_X_T = q_arrow(node_X, node_T, QUESTION_COLOR)
        arr_X_Y = q_arrow(node_X, node_Y, QUESTION_COLOR)
        problem_lbl = Text("Confounder affects both treatment and outcome", font_size=18, color=QUESTION_COLOR)
        problem_lbl.move_to(DOWN * 1.5)

        self.play(FadeIn(node_X, shift=DOWN * 0.1), run_time=0.5)
        self.play(
            LaggedStart(Create(arr_X_T), Create(arr_X_Y), lag_ratio=0.4),
            run_time=0.7,
        )
        self.play(FadeIn(problem_lbl, shift=UP * 0.05), run_time=0.5)
        self.wait(3.5)

        midpt = (node_X.get_center() + node_T.get_center()) / 2
        ctrl_lbl = Text("Control", font_size=17, color=NEUTRAL_COLOR)
        ctrl_lbl.move_to(midpt + RIGHT * 0.5)
        solution_lbl = Text("Make treatment look as good as random", font_size=20, color=ACCENT_COLOR)
        solution_lbl.move_to(DOWN * 1.5)

        self.play(
            arr_X_T.animate.set_stroke(color=NEUTRAL_COLOR, opacity=0.25),
            arr_X_Y.animate.set_stroke(color=NEUTRAL_COLOR, opacity=0.25),
            FadeOut(problem_lbl),
            run_time=0.7,
        )
        self.play(FadeIn(ctrl_lbl), run_time=0.4)
        self.play(FadeIn(solution_lbl, shift=UP * 0.05), run_time=0.5)
        wait_for_chunks([4], spent=11.9)

        # ── Beat 5 ──
        beat4_all = VGroup(
            quasi_title, node_T, node_Y, arr_T_Y, goal_lbl,
            node_X, arr_X_T, arr_X_Y, ctrl_lbl, solution_lbl,
        )
        self.play(FadeOut(beat4_all), run_time=0.5)

        method_header = Text("Methods ahead", font_size=22, color=NEUTRAL_COLOR)
        method_header.move_to(UP * 2.2)

        method_names = ["Matching", "Diff-in-Diff", "Synthetic Control", "IV", "RDD"]
        method_colors = [BLUE_D, GREEN_D, GOLD_D, MAROON_D, TEAL_D]

        def make_method_card(name, color):
            txt = Text(name, font_size=14, color=color)
            box = RoundedRectangle(
                width=2.4, height=0.9, corner_radius=0.12,
                color=color, stroke_width=1.8,
            )
            box.set_fill(color=color, opacity=0.08)
            txt.move_to(box.get_center())
            return VGroup(box, txt)

        cards = VGroup(*[make_method_card(n, c) for n, c in zip(method_names, method_colors)])
        grid_pos = [(-3.3, 0.0), (0.0, 0.0), (3.3, 0.0), (-1.65, -1.1), (1.65, -1.1)]
        for card, (x, y) in zip(cards, grid_pos):
            card.move_to([x, y, 0])

        self.play(FadeIn(method_header), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(cards[i], shift=UP * 0.08) for i in range(3)], lag_ratio=0.25),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[FadeIn(cards[i], shift=UP * 0.08) for i in range(3, 5)], lag_ratio=0.3),
            run_time=0.7,
        )
        wait_for_chunks([5], spent=2.6)

        # ── Beat 6 ──
        self.play(
            cards.animate.set_opacity(0.2),
            method_header.animate.set_opacity(0.2),
            run_time=0.6,
        )

        goal_line1 = Text("Different tools, one goal.", font_size=28, color=WHITE, weight=BOLD)
        goal_line2 = Text(
            "Making groups comparable.",
            font_size=21, color=ACCENT_COLOR,
        )
        goal_grp = VGroup(goal_line1, goal_line2).arrange(DOWN, buff=0.3)
        goal_grp.move_to(UP * 1.4)

        self.play(FadeIn(goal_grp, shift=UP * 0.06), run_time=0.6)
        wait_for_chunks([6], spent=1.2)

        self.wait(1.5)
        self.play(
            FadeOut(VGroup(cards, method_header, goal_grp)),
            run_time=2.5,
        )
        self.wait(self.WAIT_TAIL)
