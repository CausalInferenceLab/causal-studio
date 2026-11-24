from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_icon,
    load_scene_timing_durations,
)


class Scene05_MultiverseTableAteAtt(Scene):
    WAIT_TAIL = 0.05

    def construct(self):
        chunk_durations = load_scene_timing_durations("05_multiverse_table_ate_att", language="en")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        def get_chunk_duration(index: int, fallback: float) -> float:
            if not chunk_durations or index - 1 >= len(chunk_durations):
                return fallback
            return chunk_durations[index - 1]

        def make_table_cell(content: Mobject, width: float, height: float, stroke_color=GREY_B) -> VGroup:
            box = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.08,
                stroke_color=stroke_color,
                stroke_width=1.8,
                fill_opacity=0.0,
            )
            content.move_to(box.get_center())
            return VGroup(box, content)

        headers = [
            (MathTex(r"i"), 0.58, 0.56, GREY_B),
            (MathTex(r"Y_0").set_color(LIBRARY_COLOR), 1.02, 0.56, LIBRARY_COLOR),
            (MathTex(r"Y_1").set_color(TABLET_COLOR), 1.02, 0.56, TABLET_COLOR),
            (MathTex(r"T").set_color(TABLET_COLOR), 0.64, 0.56, TABLET_COLOR),
            (MathTex(r"Y").set_color(WHITE), 0.92, 0.56, GREY_B),
            (MathTex(r"ITE").set_color(ACCENT_COLOR), 1.08, 0.56, ACCENT_COLOR),
        ]
        rows = [
            ["1", "500", "450", "0", "500", "-50"],
            ["2", "600", "600", "0", "600", "0"],
            ["3", "800", "600", "1", "600", "-200"],
            ["4", "700", "750", "1", "750", "50"],
        ]
        col_widths = [0.58, 1.02, 1.02, 0.64, 0.92, 1.08]

        header_cells = VGroup(
            *[
                make_table_cell(label.scale(0.74), width, height, color)
                for label, width, height, color in headers
            ]
        ).arrange(RIGHT, buff=0.08)

        body_rows = VGroup()
        for row in rows:
            row_cells = []
            for idx, value in enumerate(row):
                color = WHITE
                if idx == 1:
                    color = LIBRARY_COLOR
                elif idx == 2 or idx == 3:
                    color = TABLET_COLOR
                elif idx == 5:
                    color = ACCENT_COLOR
                cell = make_table_cell(
                    MathTex(value).scale(0.72).set_color(color),
                    col_widths[idx],
                    0.62,
                    GREY_B,
                )
                row_cells.append(cell)
            body_rows.add(VGroup(*row_cells).arrange(RIGHT, buff=0.08))
        body_rows.arrange(DOWN, buff=0.08)

        table_group = VGroup(header_cells, body_rows).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        table_group.move_to(UP * 0.2)

        treated_row_boxes = VGroup(*[cell[0] for row in (body_rows[2], body_rows[3]) for cell in row])
        treated_t_boxes = VGroup(body_rows[2][3][0], body_rows[3][3][0])
        treated_hint = VGroup(
            MathTex(r"T=1").scale(0.76).set_color(QUESTION_COLOR),
            Text("treated only", font_size=20, color=QUESTION_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        treated_hint.next_to(table_group, RIGHT, buff=0.42)
        treated_hint.align_to(VGroup(body_rows[2][3], body_rows[3][3]), UP)

        untreated_rows = VGroup(body_rows[0], body_rows[1])
        untreated_row_boxes = VGroup(*[cell[0] for row in untreated_rows for cell in row])
        untreated_y0_boxes = VGroup(body_rows[0][1][0], body_rows[1][1][0])
        untreated_y1_boxes = VGroup(body_rows[0][2][0], body_rows[1][2][0])
        untreated_y_boxes = VGroup(body_rows[0][4][0], body_rows[1][4][0])
        all_row_boxes = VGroup(*[cell[0] for row in body_rows for cell in row])
        y0_column_boxes = VGroup(*[row[1][0] for row in body_rows])
        y1_column_boxes = VGroup(*[row[2][0] for row in body_rows])
        t_column_boxes = VGroup(*[row[3][0] for row in body_rows])
        observed_y_boxes = VGroup(*[row[4][0] for row in body_rows])
        ite_column_boxes = VGroup(*[row[5][0] for row in body_rows])
        row_outcome_boxes = VGroup(*[box for row in body_rows for box in (row[1][0], row[2][0])])
        school1_boxes = VGroup(body_rows[0][1][0], body_rows[0][2][0], body_rows[0][5][0])
        school3_boxes = VGroup(body_rows[2][1][0], body_rows[2][2][0], body_rows[2][5][0])
        treated_y0_boxes = VGroup(body_rows[2][1][0], body_rows[3][1][0])
        treated_y1_boxes = VGroup(body_rows[2][2][0], body_rows[3][2][0])
        treated_y_boxes = VGroup(body_rows[2][4][0], body_rows[3][4][0])
        y0_boxes = VGroup(body_rows[2][1][0], body_rows[3][1][0])
        y1_boxes = VGroup(body_rows[2][2][0], body_rows[3][2][0])
        outcome_header_boxes = VGroup(header_cells[1][0], header_cells[2][0])

        portal = load_icon("world-question.svg", ACCENT_COLOR, 1.0)
        portal.move_to(UP * 2.0)
        portal_ring = Circle(radius=0.8, stroke_color=ACCENT_COLOR, stroke_width=2.8).move_to(portal)
        portal_label = Text("multiverse", font_size=22, color=ACCENT_COLOR, weight=BOLD)
        portal_label.next_to(portal_ring, DOWN, buff=0.16)

        school = load_icon("school.svg", WHITE, 0.95)
        school.move_to(DOWN * 0.15)
        school_tag = MathTex(r"i").scale(0.9).next_to(school, DOWN, buff=0.18)

        left_outcome = VGroup(
            MathTex(r"Y_0").set_color(LIBRARY_COLOR),
            MathTex(r"500").set_color(LIBRARY_COLOR),
        ).arrange(DOWN, buff=0.12)
        left_outcome.move_to(LEFT * 2.25 + DOWN * 0.2)
        right_outcome = VGroup(
            MathTex(r"Y_1").set_color(TABLET_COLOR),
            MathTex(r"450").set_color(TABLET_COLOR),
        ).arrange(DOWN, buff=0.12)
        right_outcome.move_to(RIGHT * 2.25 + DOWN * 0.2)

        left_arrow = CurvedArrow(
            school.get_left() + LEFT * 0.08 + UP * 0.2,
            left_outcome.get_right() + RIGHT * 0.1,
            angle=0.35,
            color=LIBRARY_COLOR,
            stroke_width=3.4,
        )
        right_arrow = CurvedArrow(
            school.get_right() + RIGHT * 0.08 + UP * 0.2,
            right_outcome.get_left() + LEFT * 0.1,
            angle=-0.35,
            color=TABLET_COLOR,
            stroke_width=3.4,
        )

        ate_formula = MathTex(r"ATE", r"=", r"\frac{-50 + 0 - 200 + 50}{4}", r"=", r"-50")
        ate_formula.scale(0.82)
        ate_formula[0].set_color(ACCENT_COLOR)
        ate_formula[-1].set_color(ACCENT_COLOR)
        ate_formula.next_to(table_group, DOWN, buff=0.52)

        att_formula = MathTex(r"ATT", r"=", r"\frac{-200 + 50}{2}", r"=", r"-75")
        att_formula.scale(0.82)
        att_formula[0].set_color(QUESTION_COLOR)
        att_formula[-1].set_color(QUESTION_COLOR)
        att_formula.move_to(ate_formula)

        untreated_fact_label = VGroup(
            MathTex(r"T=0").scale(0.68).set_color(WHITE),
            Text("Y0 factual", font_size=16, color=LIBRARY_COLOR, weight=BOLD),
            Text("Y1 counterfactual", font_size=16, color=TABLET_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        treated_fact_label = VGroup(
            MathTex(r"T=1").scale(0.68).set_color(WHITE),
            Text("Y1 factual", font_size=16, color=TABLET_COLOR, weight=BOLD),
            Text("Y0 counterfactual", font_size=16, color=LIBRARY_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        factual_legend = VGroup(untreated_fact_label, treated_fact_label).arrange(RIGHT, buff=0.42, aligned_edge=UP)
        factual_legend.next_to(table_group, DOWN, buff=0.3)

        # Beat 1:
        self.play(Create(portal_ring), FadeIn(portal, scale=0.9), FadeIn(portal_label, shift=UP * 0.08), run_time=0.9)
        self.play(FadeIn(school, scale=0.9), FadeIn(school_tag, shift=UP * 0.08), run_time=0.8)
        self.play(Create(left_arrow), Create(right_arrow), FadeIn(left_outcome), FadeIn(right_outcome), run_time=1.0)
        wait_for_chunks([1], spent=2.7)

        # Beat 2:
        self.play(
            FadeOut(VGroup(portal_ring, portal, portal_label, school, school_tag, left_arrow, right_arrow, left_outcome, right_outcome)),
            FadeIn(table_group, shift=UP * 0.12),
            run_time=1.0,
        )
        self.play(
            header_cells[1][0].animate.set_stroke(LIBRARY_COLOR, width=3.0),
            header_cells[2][0].animate.set_stroke(TABLET_COLOR, width=3.0),
            *[box.animate.set_stroke(LIBRARY_COLOR, width=2.8) for box in y0_column_boxes],
            *[box.animate.set_stroke(TABLET_COLOR, width=2.8) for box in y1_column_boxes],
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        row[1][0].animate.set_fill(LIBRARY_COLOR, opacity=0.12),
                        row[2][0].animate.set_fill(TABLET_COLOR, opacity=0.12),
                    )
                    for row in body_rows
                ],
                lag_ratio=0.16,
            ),
            run_time=1.1,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=ACCENT_COLOR, scale_factor=1.02) for box in row_outcome_boxes],
                lag_ratio=0.05,
            ),
            run_time=0.9,
        )
        wait_for_chunks([2], spent=4.0)
        self.play(
            *[box.animate.set_fill(opacity=0.0) for box in row_outcome_boxes],
            run_time=0.25,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=QUESTION_COLOR, scale_factor=1.02) for box in VGroup(header_cells[3][0], *t_column_boxes)],
                lag_ratio=0.1,
            ),
            run_time=0.75,
        )
        self.wait(1.35)
        self.play(
            LaggedStart(
                *[Indicate(box, color=WHITE, scale_factor=1.02) for box in VGroup(header_cells[4][0], *observed_y_boxes)],
                lag_ratio=0.1,
            ),
            run_time=0.75,
        )
        wait_for_chunks([3], spent=2.85)
        self.play(
            *[box.animate.set_fill(ACCENT_COLOR, opacity=0.12).set_stroke(ACCENT_COLOR, width=2.6) for box in row_outcome_boxes],
            run_time=0.55,
        )
        self.play(
            LaggedStart(
                *[
                    Indicate(VGroup(row[1][0], row[2][0]), color=ACCENT_COLOR, scale_factor=1.02)
                    for row in body_rows
                ],
                lag_ratio=0.12,
            ),
            run_time=0.7,
        )
        self.play(
            header_cells[5][0].animate.set_stroke(ACCENT_COLOR, width=3.0),
            *[box.animate.set_fill(ACCENT_COLOR, opacity=0.14).set_stroke(ACCENT_COLOR, width=2.8) for box in ite_column_boxes],
            run_time=0.55,
        )
        wait_for_chunks([4], spent=1.25)
        self.play(
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in row_outcome_boxes],
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in ite_column_boxes],
            header_cells[5][0].animate.set_stroke(ACCENT_COLOR, width=1.8),
            run_time=0.2,
        )
        self.play(
            school3_boxes[0].animate.set_fill(LIBRARY_COLOR, opacity=0.18).set_stroke(LIBRARY_COLOR, width=3.0),
            school3_boxes[1].animate.set_fill(TABLET_COLOR, opacity=0.18).set_stroke(TABLET_COLOR, width=3.0),
            school3_boxes[2].animate.set_fill(ACCENT_COLOR, opacity=0.18).set_stroke(ACCENT_COLOR, width=3.0),
            school1_boxes[0].animate.set_fill(LIBRARY_COLOR, opacity=0.18).set_stroke(LIBRARY_COLOR, width=3.0),
            school1_boxes[1].animate.set_fill(TABLET_COLOR, opacity=0.18).set_stroke(TABLET_COLOR, width=3.0),
            school1_boxes[2].animate.set_fill(ACCENT_COLOR, opacity=0.18).set_stroke(ACCENT_COLOR, width=3.0),
            run_time=0.6,
        )
        self.play(Indicate(school1_boxes, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.45)
        self.play(
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in school1_boxes],
            run_time=0.15,
        )
        self.play(Indicate(school3_boxes, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.45)
        self.play(
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in school3_boxes],
            run_time=0.15,
        )
        wait_for_chunks([5], spent=1.8)
        self.play(
            *[box.animate.set_fill(opacity=0.0) for box in row_outcome_boxes],
            header_cells[1][0].animate.set_stroke(LIBRARY_COLOR, width=1.8),
            header_cells[2][0].animate.set_stroke(TABLET_COLOR, width=1.8),
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in y0_column_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in y1_column_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in t_column_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in observed_y_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in ite_column_boxes],
            run_time=0.5,
        )

        # Beat 3:
        self.play(
            *[box.animate.set_fill(ACCENT_COLOR, opacity=0.08) for box in all_row_boxes],
            *[box.animate.set_stroke(ACCENT_COLOR, width=2.1) for box in all_row_boxes],
            FadeIn(ate_formula, shift=UP * 0.08),
            run_time=0.7,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=ACCENT_COLOR, scale_factor=1.015) for box in all_row_boxes],
                lag_ratio=0.04,
            ),
            run_time=0.7,
        )
        wait_for_chunks([6], spent=1.4)
        wait_for_chunks([7])

        # Beat 4:
        self.play(
            untreated_rows.animate.set_opacity(0.28),
            *[box.animate.set_fill(opacity=0.0) for box in all_row_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in all_row_boxes],
            *[box.animate.set_fill(QUESTION_COLOR, opacity=0.12) for box in treated_row_boxes],
            *[box.animate.set_stroke(QUESTION_COLOR, width=2.4) for box in treated_row_boxes],
            *[box.animate.set_fill(QUESTION_COLOR, opacity=0.22) for box in treated_t_boxes],
            *[box.animate.set_stroke(QUESTION_COLOR, width=3.0) for box in treated_t_boxes],
            FadeIn(treated_hint, shift=RIGHT * 0.08),
            TransformMatchingTex(ate_formula, att_formula),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=QUESTION_COLOR, scale_factor=1.03) for box in treated_t_boxes],
                lag_ratio=0.12,
            ),
            run_time=0.6,
        )
        wait_for_chunks([8], spent=1.5)
        self.play(Indicate(att_formula[-1], color=QUESTION_COLOR, scale_factor=1.08), run_time=0.55)
        wait_for_chunks([9], spent=0.55)
        self.play(
            LaggedStart(
                *[Indicate(box, color=QUESTION_COLOR, scale_factor=1.025) for box in treated_row_boxes],
                lag_ratio=0.08,
            ),
            run_time=0.8,
        )
        wait_for_chunks([10], spent=0.8)

        # Beat 5:
        self.play(
            FadeOut(att_formula),
            FadeOut(treated_hint),
            untreated_rows.animate.set_opacity(1.0),
            *[box.animate.set_fill(BLACK, opacity=0.0) for box in untreated_row_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in untreated_row_boxes],
            *[box.animate.set_fill(opacity=0.0) for box in treated_row_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in treated_row_boxes],
            *[box.animate.set_fill(opacity=0.0) for box in treated_t_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in treated_t_boxes],
            run_time=0.6,
        )
        self.play(
            *[box.animate.set_stroke(LIBRARY_COLOR, width=2.4) for box in untreated_y0_boxes],
            *[box.animate.set_stroke(TABLET_COLOR, width=2.4) for box in untreated_y1_boxes],
            *[box.animate.set_stroke(TABLET_COLOR, width=2.4) for box in treated_y1_boxes],
            *[box.animate.set_stroke(LIBRARY_COLOR, width=2.4) for box in treated_y0_boxes],
            *[box.animate.set_fill(LIBRARY_COLOR, opacity=0.1) for box in untreated_y0_boxes],
            *[box.animate.set_fill(TABLET_COLOR, opacity=0.1) for box in treated_y1_boxes],
            *[box.animate.set_fill(TABLET_COLOR, opacity=0.06) for box in untreated_y1_boxes],
            *[box.animate.set_fill(LIBRARY_COLOR, opacity=0.06) for box in treated_y0_boxes],
            *[box.animate.set_stroke(WHITE, width=2.8) for box in untreated_y_boxes],
            *[box.animate.set_stroke(WHITE, width=2.8) for box in treated_y_boxes],
            FadeIn(factual_legend, shift=UP * 0.08),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=WHITE, scale_factor=1.02) for box in untreated_y_boxes],
                *[Indicate(box, color=WHITE, scale_factor=1.02) for box in treated_y_boxes],
                lag_ratio=0.08,
            ),
            run_time=0.8,
        )
        wait_for_chunks([11], spent=1.7)
        self.wait(self.WAIT_TAIL)
