"""IV (Instrumental Variables) — English narration version.

Parallel to iv.py with the same 7-Scene structure and identical visual layout,
but with English on-screen text and English-audio timings.

Audio files: build/audio/{NN}_{scene}_en.{mp3,timings.json}
Class names: {SceneNN}_{Name}EN — suffix avoids render output collisions
with the Korean version under build/manim/videos/iv/1080p60/.

Helpers (load_icon, color palette, etc.) are imported from iv.py — single
source of truth for layout primitives. Only text strings and per-Beat wait
durations differ.
"""

from manim import *

from iv import (
    load_icon,
    load_scene_timing_durations,
    make_forbidden_card,
    make_school_row,
    ACCENT,
    COIN_COLOR,
    TREAT_COLOR,
    CONTROL_COLOR,
    FORBIDDEN,
    CLEAN_WATER,
    DIRTY_WATER,
    INSTRUMENT,
    COMPLIER,
    ALWAYS_TAKER,
    NEVER_TAKER,
    SOFT,
)


# ═══════════════════════════════════════════════════════════════════
# Scene 01 EN — Snow Pumps
# ═══════════════════════════════════════════════════════════════════


class Scene01_SnowPumpsEN(Scene):
    """English version of Scene 01 (Snow Pumps).
    7 chunks, ~80.11s. Mirrors Korean layout exactly.
    """

    WAIT_TAIL = 2.0

    def construct(self):
        d = load_scene_timing_durations("01_snow_pumps_en")

        # Beat 1: RCT recap
        coin = load_icon("coin.svg", COIN_COLOR, 1.4).move_to(ORIGIN + UP * 0.3)
        treat_dots = VGroup(*[Dot(radius=0.13, color=TREAT_COLOR) for _ in range(4)])
        treat_dots.arrange(RIGHT, buff=0.18)
        treat_label = Text("Treated", font_size=22, color=TREAT_COLOR)
        treat_group = VGroup(treat_dots, treat_label).arrange(DOWN, buff=0.18).move_to(LEFT * 3.2 + DOWN * 1.4)
        control_dots = VGroup(*[Dot(radius=0.13, color=CONTROL_COLOR) for _ in range(4)])
        control_dots.arrange(RIGHT, buff=0.18)
        control_label = Text("Control", font_size=22, color=CONTROL_COLOR)
        control_group = VGroup(control_dots, control_label).arrange(DOWN, buff=0.18).move_to(RIGHT * 3.2 + DOWN * 1.4)
        split_arrow_l = Arrow(coin.get_corner(DL), treat_group.get_top(), buff=0.2, color=SOFT, stroke_width=3)
        split_arrow_r = Arrow(coin.get_corner(DR), control_group.get_top(), buff=0.2, color=SOFT, stroke_width=3)
        bias_badge = Text("Bias = 0", font_size=26, weight=BOLD, color=GREEN).move_to(DOWN * 3.0)

        self.play(FadeIn(coin, scale=0.8), run_time=0.8)
        self.play(Rotate(coin, angle=2 * PI, axis=UP), run_time=1.2)
        self.play(GrowArrow(split_arrow_l), GrowArrow(split_arrow_r),
                  FadeIn(treat_group, shift=DOWN * 0.2), FadeIn(control_group, shift=DOWN * 0.2), run_time=1.5)
        self.play(FadeIn(bias_badge, shift=UP * 0.15), run_time=0.8)
        self.wait(d[0] - 4.3)

        # Beat 2: forbidden coins
        coin_small_target = coin.copy().scale(0.45).to_corner(UL, buff=0.5)
        smoking_card = make_forbidden_card("Smoking randomized\nfor pregnant women").move_to(LEFT * 2.8 + UP * 0.4)
        army_card = make_forbidden_card("Who gets drafted\ninto the army").move_to(RIGHT * 2.8 + UP * 0.4)
        forbidden_caption = Text("Coins the experimenter can't flip", font_size=24, color=FORBIDDEN).move_to(DOWN * 1.8)

        self.play(FadeOut(treat_group), FadeOut(control_group), FadeOut(split_arrow_l),
                  FadeOut(split_arrow_r), FadeOut(bias_badge), Transform(coin, coin_small_target), run_time=1.0)
        self.play(FadeIn(smoking_card, shift=UP * 0.15), FadeIn(army_card, shift=UP * 0.15), run_time=1.4)
        self.play(FadeIn(forbidden_caption, shift=UP * 0.1), run_time=0.8)
        self.wait(d[1] - 3.2)

        # Beat 3: the question
        big_question = Text("?", font_size=180, weight=BOLD, color=ACCENT).move_to(ORIGIN + UP * 0.2)
        question_caption = Text("Who can flip it for us?", font_size=30, color=WHITE).next_to(big_question, DOWN, buff=0.5)

        self.play(FadeOut(smoking_card), FadeOut(army_card), FadeOut(forbidden_caption), run_time=0.7)
        self.play(FadeIn(big_question, scale=0.6), run_time=1.0)
        self.play(Write(question_caption), run_time=1.0)
        self.wait(d[2] - 2.7)

        # Beat 4: 1854 London
        date_label = Text("London, 1854", font_size=30, weight=BOLD, color=SOFT).to_edge(UP, buff=0.5)
        streets = VGroup(*[
            Rectangle(width=5.0, height=0.35, stroke_color=GREY_C, stroke_width=2,
                       fill_color=GREY_E, fill_opacity=0.35) for _ in range(6)
        ])
        streets.arrange(DOWN, buff=0.18).move_to(ORIGIN + DOWN * 0.2)
        clean_drop = load_icon("droplet.svg", CLEAN_WATER, 0.7)
        clean_name = Text("Lambeth\n(clean upstream)", font_size=20, color=CLEAN_WATER, line_spacing=0.9)
        clean_group = VGroup(clean_drop, clean_name).arrange(DOWN, buff=0.18).next_to(streets, LEFT, buff=0.6)
        dirty_drop = load_icon("droplet.svg", DIRTY_WATER, 0.7)
        dirty_name = Text("S & V\n(sewage-mixed)", font_size=20, color=DIRTY_WATER, line_spacing=0.9)
        dirty_group = VGroup(dirty_drop, dirty_name).arrange(DOWN, buff=0.18).next_to(streets, RIGHT, buff=0.6)

        self.play(FadeOut(big_question), FadeOut(question_caption), FadeOut(coin), run_time=0.7)
        self.play(FadeIn(date_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[Create(s) for s in streets], lag_ratio=0.12), run_time=1.6)
        self.play(FadeIn(clean_group, shift=RIGHT * 0.2), FadeIn(dirty_group, shift=LEFT * 0.2), run_time=1.2)
        self.wait(d[3] - 4.2)

        # Beat 5: random street assignment
        assignment = [CLEAN_WATER, DIRTY_WATER, DIRTY_WATER, CLEAN_WATER, DIRTY_WATER, CLEAN_WATER]
        street_fills = [
            street.animate.set_fill(color, opacity=0.75).set_stroke(color=color)
            for street, color in zip(streets, assignment)
        ]
        self.play(LaggedStart(*street_fills, lag_ratio=0.18), run_time=2.4)
        chance_label = Text("Almost an accident", font_size=32, weight=BOLD, color=ACCENT).move_to(DOWN * 3.0)
        chance_box = SurroundingRectangle(chance_label, color=ACCENT, buff=0.15)
        self.play(FadeIn(chance_label, shift=UP * 0.1), Create(chance_box), run_time=1.0)
        self.wait(d[4] - 3.4)

        # Beat 6: nature's coin
        nature_coin = load_icon("coin.svg", COIN_COLOR, 1.6).move_to(ORIGIN + UP * 0.5)
        nature_caption = Text("A coin flipped by nature", font_size=28, color=COIN_COLOR).next_to(nature_coin, DOWN, buff=0.4)

        self.play(streets.animate.set_opacity(0.25),
                  clean_group.animate.set_opacity(0.4),
                  dirty_group.animate.set_opacity(0.4),
                  chance_label.animate.set_opacity(0.4),
                  chance_box.animate.set_opacity(0.4), run_time=0.7)
        self.play(FadeIn(nature_coin, scale=0.7), run_time=0.9)
        self.play(Rotate(nature_coin, angle=2 * PI, axis=UP), Write(nature_caption), run_time=1.4)
        self.wait(d[5] - 3.0)

        # Beat 7: title card
        title_group_old = VGroup(date_label, streets, clean_group, dirty_group,
                                  chance_label, chance_box, nature_coin, nature_caption)
        self.play(FadeOut(title_group_old), run_time=0.7)
        topic_title = Text("Instrumental Variable", font_size=64, weight=BOLD, color=INSTRUMENT)
        topic_sub = Text("IV", font_size=36, color=SOFT)
        title_stack = VGroup(topic_title, topic_sub).arrange(DOWN, buff=0.3).move_to(UP * 1.2)
        z_node = Circle(radius=0.42, color=INSTRUMENT, stroke_width=3)
        z_label = Text("Z", font_size=28, color=INSTRUMENT, weight=BOLD).move_to(z_node)
        z_group = VGroup(z_node, z_label).move_to(LEFT * 2.8 + DOWN * 1.6)
        t_node = Circle(radius=0.42, color=TREAT_COLOR, stroke_width=3)
        t_label = Text("T", font_size=28, color=TREAT_COLOR, weight=BOLD).move_to(t_node)
        t_group = VGroup(t_node, t_label).move_to(ORIGIN + DOWN * 1.6)
        y_node = Circle(radius=0.42, color=CONTROL_COLOR, stroke_width=3)
        y_label = Text("Y", font_size=28, color=CONTROL_COLOR, weight=BOLD).move_to(y_node)
        y_group = VGroup(y_node, y_label).move_to(RIGHT * 2.8 + DOWN * 1.6)
        zt_arrow = Arrow(z_group.get_right(), t_group.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        ty_arrow = Arrow(t_group.get_right(), y_group.get_left(), buff=0.12, color=WHITE, stroke_width=3)

        self.play(FadeIn(title_stack, shift=DOWN * 0.2), run_time=1.0)
        self.play(FadeIn(z_group), FadeIn(t_group), FadeIn(y_group), run_time=0.9)
        self.play(GrowArrow(zt_arrow), GrowArrow(ty_arrow), run_time=0.8)
        self.play(Indicate(z_group, color=INSTRUMENT), run_time=0.9)
        self.wait(d[6] - 3.6)
        self.wait(self.WAIT_TAIL)


# ═══════════════════════════════════════════════════════════════════
# Scene 02 EN — RCT Recap & Non-compliance Break
# ═══════════════════════════════════════════════════════════════════


class Scene02_RctRecapBreakEN(Scene):
    """English version of Scene 02. 5 chunks, ~68.98s."""

    WAIT_TAIL = 1.5

    def construct(self):
        d = load_scene_timing_durations("02_rct_recap_break_en")

        # Beat 1: tablet RCT recap
        title = Text("Tablet RCT recap", font_size=30, weight=BOLD, color=SOFT).to_edge(UP, buff=0.4)
        coin = load_icon("coin.svg", COIN_COLOR, 1.0).move_to(UP * 1.0)

        assigned_t = make_school_row(4, TREAT_COLOR).move_to(LEFT * 2.7 + DOWN * 0.6)
        assigned_t_label = Text("Assigned: Treatment", font_size=22, color=TREAT_COLOR).next_to(assigned_t, DOWN, buff=0.25)
        assigned_c = make_school_row(4, CONTROL_COLOR).move_to(RIGHT * 2.7 + DOWN * 0.6)
        assigned_c_label = Text("Assigned: Control", font_size=22, color=CONTROL_COLOR).next_to(assigned_c, DOWN, buff=0.25)
        naive_eq = Text("Mean difference  =  causal effect", font_size=24, color=GREEN).move_to(DOWN * 2.5)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(coin, scale=0.8), run_time=0.7)
        self.play(Rotate(coin, angle=2 * PI, axis=UP), run_time=1.0)
        self.play(FadeIn(assigned_t, shift=DOWN * 0.15), FadeIn(assigned_t_label),
                  FadeIn(assigned_c, shift=DOWN * 0.15), FadeIn(assigned_c_label), run_time=1.4)
        self.play(Write(naive_eq), run_time=1.2)
        self.wait(d[0] - 5.0)

        # Beat 2: some refuse
        refuse_caption = Text("Some refuse the tablet", font_size=22, color=FORBIDDEN).move_to(LEFT * 2.7 + DOWN * 1.9)
        self.play(FadeOut(naive_eq), run_time=0.4)
        self.play(FadeIn(refuse_caption, shift=UP * 0.1), run_time=0.7)
        refuse_animations = [
            assigned_t[i].animate.set_color(CONTROL_COLOR).set_stroke(color=FORBIDDEN, width=2)
            for i in (1, 3)
        ]
        self.play(LaggedStart(*refuse_animations, lag_ratio=0.3), run_time=1.6)
        x_marks = VGroup(*[
            Cross(assigned_t[i], stroke_color=FORBIDDEN, stroke_width=3).scale(0.5)
            for i in (1, 3)
        ])
        self.play(FadeIn(x_marks), run_time=0.5)
        self.wait(d[1] - 3.2)

        # Beat 3: some buy
        buy_caption = Text("Some buy with their own funds", font_size=22, color=ACCENT).move_to(RIGHT * 2.7 + DOWN * 1.9)
        self.play(FadeIn(buy_caption, shift=UP * 0.1), run_time=0.7)
        buy_animations = [
            assigned_c[i].animate.set_color(TREAT_COLOR).set_stroke(color=ACCENT, width=2)
            for i in (0, 2)
        ]
        self.play(LaggedStart(*buy_animations, lag_ratio=0.3), run_time=1.4)
        stars = VGroup(*[
            Star(n=5, outer_radius=0.18, color=ACCENT, fill_opacity=0.9).move_to(assigned_c[i])
            for i in (0, 2)
        ])
        self.play(FadeIn(stars, scale=0.6), run_time=0.5)
        self.wait(d[2] - 2.6)

        # Beat 4: comparing by actual treatment brings bias back
        previous = VGroup(title, coin, assigned_t, assigned_c, assigned_t_label, assigned_c_label,
                          refuse_caption, buy_caption, x_marks, stars)
        warning = Text("If we compare by actual treatment…", font_size=26, color=FORBIDDEN).to_edge(UP, buff=0.6)
        actual_t = VGroup(*[Dot(radius=0.20, color=TREAT_COLOR) for _ in range(4)]).arrange(RIGHT, buff=0.4).move_to(LEFT * 2.8 + UP * 0.2)
        actual_t_label = Text("Actually treated", font_size=22, color=TREAT_COLOR).next_to(actual_t, DOWN, buff=0.25)
        actual_c = VGroup(*[Dot(radius=0.20, color=CONTROL_COLOR) for _ in range(4)]).arrange(RIGHT, buff=0.4).move_to(RIGHT * 2.8 + UP * 0.2)
        actual_c_label = Text("Actually untreated", font_size=22, color=CONTROL_COLOR).next_to(actual_c, DOWN, buff=0.25)
        bias_eq = Text("Mean difference  ≠  causal effect", font_size=28, weight=BOLD, color=FORBIDDEN).move_to(DOWN * 1.4)
        bias_note = Text("Refusers = skeptical,  Self-buyers = motivated", font_size=20, color=SOFT).next_to(bias_eq, DOWN, buff=0.4)

        self.play(FadeOut(previous), run_time=0.7)
        self.play(FadeIn(warning, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(actual_t), FadeIn(actual_t_label),
                  FadeIn(actual_c), FadeIn(actual_c_label), run_time=1.2)
        self.play(Write(bias_eq), run_time=1.0)
        self.play(FadeIn(bias_note, shift=UP * 0.1), run_time=0.9)
        self.wait(d[3] - 4.5)

        # Beat 5: only assignment is random
        bridge_title = Text("Only the assignment is random", font_size=30, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        row_label_assign = Text("Assignment", font_size=22, color=SOFT)
        row_label_actual = Text("Actual", font_size=22, color=SOFT)
        assign_row = make_school_row(8, COIN_COLOR, spacing=0.30)
        actual_row = VGroup(*[
            Dot(radius=0.18, color=c) for c in
            [TREAT_COLOR, CONTROL_COLOR, TREAT_COLOR, CONTROL_COLOR,
             TREAT_COLOR, TREAT_COLOR, CONTROL_COLOR, TREAT_COLOR]
        ])
        actual_row.arrange(RIGHT, buff=0.30)
        assign_block = VGroup(row_label_assign, assign_row).arrange(RIGHT, buff=0.6)
        actual_block = VGroup(row_label_actual, actual_row).arrange(RIGHT, buff=0.6)
        rows_block = VGroup(assign_block, actual_block).arrange(DOWN, aligned_edge=LEFT, buff=0.7).move_to(UP * 0.2)
        random_badge = Text("Random ✓", font_size=20, color=GREEN).next_to(assign_block, RIGHT, buff=0.5)
        not_random = Text("Not random ✗", font_size=20, color=FORBIDDEN).next_to(actual_block, RIGHT, buff=0.5)
        pivot = Text("Use the randomness we still have → IV", font_size=24, weight=BOLD, color=INSTRUMENT).move_to(DOWN * 2.2)

        self.play(FadeOut(warning), FadeOut(actual_t), FadeOut(actual_t_label),
                  FadeOut(actual_c), FadeOut(actual_c_label),
                  FadeOut(bias_eq), FadeOut(bias_note), run_time=0.7)
        self.play(FadeIn(bridge_title, shift=DOWN * 0.1), run_time=0.6)
        self.play(FadeIn(rows_block, shift=UP * 0.15), run_time=1.4)
        self.play(FadeIn(random_badge), FadeIn(not_random), run_time=0.8)
        self.play(Write(pivot), run_time=1.4)
        self.wait(d[4] - 4.9)
        self.wait(self.WAIT_TAIL)


# ═══════════════════════════════════════════════════════════════════
# Scene 03 EN — Three Types
# ═══════════════════════════════════════════════════════════════════


class Scene03_ThreeTypesEN(Scene):
    """English version of Scene 03. 6 chunks, ~65.88s."""

    WAIT_TAIL = 1.5

    def construct(self):
        d = load_scene_timing_durations("03_three_types_en")

        # Beat 1: three types intro
        title = Text("Three types the coin moves", font_size=30, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.4)
        type_names = ["Complier", "Always-taker", "Never-taker"]
        type_colors = [COMPLIER, ALWAYS_TAKER, NEVER_TAKER]
        cards = VGroup()
        for name, color in zip(type_names, type_colors):
            frame = RoundedRectangle(width=3.4, height=1.1, corner_radius=0.16,
                                       stroke_color=color, stroke_width=2.5)
            label = Text(name, font_size=24, weight=BOLD, color=color).move_to(frame.get_center())
            cards.add(VGroup(frame, label))
        cards.arrange(RIGHT, buff=0.4).move_to(UP * 0.6)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cards], lag_ratio=0.25), run_time=1.6)
        self.wait(d[0] - 2.2)

        # Beat 2: complier
        track_label_z1 = Text("Assigned: Treatment", font_size=20, color=COIN_COLOR)
        track_label_z0 = Text("Assigned: Control", font_size=20, color=COIN_COLOR)
        track_z1 = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY_C, stroke_width=2)
        track_z0 = Line(LEFT * 2.5, RIGHT * 2.5, color=GREY_C, stroke_width=2)
        track1_block = VGroup(track_label_z1, track_z1).arrange(RIGHT, buff=0.4)
        track0_block = VGroup(track_label_z0, track_z0).arrange(RIGHT, buff=0.4)
        tracks = VGroup(track1_block, track0_block).arrange(DOWN, aligned_edge=LEFT, buff=1.0).move_to(DOWN * 0.3)

        complier_z1_dot = Dot(radius=0.20, color=TREAT_COLOR).move_to(track_z1.get_center())
        complier_z0_dot = Dot(radius=0.20, color=CONTROL_COLOR).move_to(track_z0.get_center())
        complier_caption = Text("Complier: follows the coin", font_size=24, color=COMPLIER).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(cards), run_time=0.5)
        self.play(FadeIn(tracks, shift=DOWN * 0.1), run_time=0.8)
        self.play(FadeIn(complier_z1_dot, scale=0.7), FadeIn(complier_z0_dot, scale=0.7), run_time=0.8)
        self.play(Write(complier_caption), run_time=1.2)
        self.wait(d[1] - 3.3)

        # Beat 3: always-taker
        always_z1 = Dot(radius=0.20, color=ALWAYS_TAKER).move_to(track_z1.get_center() + RIGHT * 0.9)
        always_z0 = Dot(radius=0.20, color=ALWAYS_TAKER).move_to(track_z0.get_center() + RIGHT * 0.9)
        always_caption = Text("Always-taker: treated regardless", font_size=24, color=ALWAYS_TAKER).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(complier_caption), run_time=0.4)
        self.play(FadeIn(always_z1, scale=0.7), FadeIn(always_z0, scale=0.7), run_time=0.8)
        self.play(Write(always_caption), run_time=1.2)
        self.wait(d[2] - 2.4)

        # Beat 4: never-taker
        never_z1 = Dot(radius=0.20, color=NEVER_TAKER).move_to(track_z1.get_center() - RIGHT * 0.9)
        never_z0 = Dot(radius=0.20, color=NEVER_TAKER).move_to(track_z0.get_center() - RIGHT * 0.9)
        never_caption = Text("Never-taker: untreated regardless", font_size=24, color=NEVER_TAKER).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(always_caption), run_time=0.4)
        self.play(FadeIn(never_z1, scale=0.7), FadeIn(never_z0, scale=0.7), run_time=0.8)
        self.play(Write(never_caption), run_time=1.2)
        self.wait(d[3] - 2.4)

        # Beat 5: only complier moves
        self.play(FadeOut(never_caption), run_time=0.4)
        reveal = Text("Only compliers move with the coin", font_size=26, weight=BOLD, color=COMPLIER).to_edge(DOWN, buff=0.5)
        complier_box_top = SurroundingRectangle(complier_z1_dot, color=COMPLIER, buff=0.15, stroke_width=3)
        complier_box_bot = SurroundingRectangle(complier_z0_dot, color=COMPLIER, buff=0.15, stroke_width=3)
        self.play(
            always_z1.animate.set_opacity(0.45), always_z0.animate.set_opacity(0.45),
            never_z1.animate.set_opacity(0.45), never_z0.animate.set_opacity(0.45),
            run_time=0.7,
        )
        self.play(Create(complier_box_top), Create(complier_box_bot), run_time=0.9)
        self.play(Write(reveal), run_time=1.4)
        self.wait(d[4] - 3.4)

        # Beat 6: LATE card
        late_box = RoundedRectangle(width=8.0, height=2.0, corner_radius=0.2,
                                      stroke_color=INSTRUMENT, stroke_width=3)
        late_title = Text("LATE", font_size=42, weight=BOLD, color=INSTRUMENT)
        late_sub = Text("Local Average Treatment Effect\nThe effect limited to compliers", font_size=22,
                         color=WHITE, line_spacing=0.95)
        late_stack = VGroup(late_title, late_sub).arrange(DOWN, buff=0.25).move_to(late_box.get_center())

        prior = VGroup(tracks, complier_z1_dot, complier_z0_dot,
                        complier_box_top, complier_box_bot,
                        always_z1, always_z0, never_z1, never_z0, reveal, title)
        self.play(FadeOut(prior), run_time=0.7)
        self.play(Create(late_box), run_time=0.9)
        self.play(FadeIn(late_stack, shift=UP * 0.2), run_time=1.4)
        self.wait(d[5] - 3.0)
        self.wait(self.WAIT_TAIL)


# ═══════════════════════════════════════════════════════════════════
# Scene 04 EN — Wald Machinery
# ═══════════════════════════════════════════════════════════════════


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


# ═══════════════════════════════════════════════════════════════════
# Scene 05 EN — Three Assumptions
# ═══════════════════════════════════════════════════════════════════


class Scene05_ThreeAssumptionsEN(Scene):
    """English version of Scene 05. 5 chunks, ~69.91s."""

    WAIT_TAIL = 1.5

    def construct(self):
        d = load_scene_timing_durations("05_three_assumptions_en")

        # Beat 1: three locks
        title = Text("IV's three locks", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        lock_names = ["Relevance", "Exclusion", "Independence"]
        locks = VGroup()
        for name in lock_names:
            lk = load_icon("lock.svg", FORBIDDEN, 1.1)
            nm = Text(name, font_size=22, weight=BOLD, color=WHITE).next_to(lk, DOWN, buff=0.25)
            locks.add(VGroup(lk, nm))
        locks.arrange(RIGHT, buff=1.5).move_to(DOWN * 0.4)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(lk, shift=UP * 0.15) for lk in locks], lag_ratio=0.25), run_time=1.6)
        warning = Text("If even one fails, you can't trust the result", font_size=22, color=SOFT).to_edge(DOWN, buff=0.6)
        self.play(Write(warning), run_time=1.4)
        self.wait(d[0] - 3.7)

        # Beat 2: relevance (fix: locks fully fade, not shrunk)
        self.play(FadeOut(warning), FadeOut(locks), run_time=0.8)

        z_node = Circle(radius=0.45, color=INSTRUMENT, stroke_width=3)
        z_text = Text("Z", font_size=26, weight=BOLD, color=INSTRUMENT).move_to(z_node)
        z_grp = VGroup(z_node, z_text).move_to(LEFT * 2.8 + DOWN * 0.5)
        t_node = Circle(radius=0.45, color=TREAT_COLOR, stroke_width=3)
        t_text = Text("T", font_size=26, weight=BOLD, color=TREAT_COLOR).move_to(t_node)
        t_grp = VGroup(t_node, t_text).move_to(RIGHT * 2.8 + DOWN * 0.5)
        strong_arrow = Arrow(z_grp.get_right(), t_grp.get_left(), buff=0.12, color=GREEN, stroke_width=8)
        strong_label = Text("Z strongly moves T ✓", font_size=22, color=GREEN).next_to(strong_arrow, UP, buff=0.3)
        weak_arrow = Arrow(z_grp.get_right(), t_grp.get_left(), buff=0.12, color=FORBIDDEN, stroke_width=2)
        weak_label = Text("Weak → denominator ≈ 0 → estimate explodes ✗", font_size=22, color=FORBIDDEN).next_to(weak_arrow, DOWN, buff=0.3)

        self.play(FadeIn(z_grp), FadeIn(t_grp), run_time=0.8)
        self.play(GrowArrow(strong_arrow), FadeIn(strong_label, shift=DOWN * 0.1), run_time=1.0)
        self.play(Transform(strong_arrow, weak_arrow), FadeIn(weak_label, shift=UP * 0.1), run_time=1.4)
        self.wait(d[1] - 3.2)

        # Beat 3: exclusion
        previous = VGroup(z_grp, t_grp, strong_arrow, strong_label, weak_label)
        self.play(FadeOut(previous), run_time=0.6)

        z_node2 = Circle(radius=0.4, color=INSTRUMENT, stroke_width=3)
        z_text2 = Text("Z", font_size=24, weight=BOLD, color=INSTRUMENT).move_to(z_node2)
        z_grp2 = VGroup(z_node2, z_text2).move_to(LEFT * 3.5 + DOWN * 0.3)
        t_node2 = Circle(radius=0.4, color=TREAT_COLOR, stroke_width=3)
        t_text2 = Text("T", font_size=24, weight=BOLD, color=TREAT_COLOR).move_to(t_node2)
        t_grp2 = VGroup(t_node2, t_text2).move_to(ORIGIN + DOWN * 0.3)
        y_node2 = Circle(radius=0.4, color=CONTROL_COLOR, stroke_width=3)
        y_text2 = Text("Y", font_size=24, weight=BOLD, color=CONTROL_COLOR).move_to(y_node2)
        y_grp2 = VGroup(y_node2, y_text2).move_to(RIGHT * 3.5 + DOWN * 0.3)
        zt_arrow2 = Arrow(z_grp2.get_right(), t_grp2.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        ty_arrow2 = Arrow(t_grp2.get_right(), y_grp2.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        zy_arc = CurvedArrow(z_grp2.get_top(), y_grp2.get_top(), color=FORBIDDEN, stroke_width=3, angle=-1.4)
        zy_cross = Cross(zy_arc, stroke_color=FORBIDDEN, stroke_width=4).scale(1.0)
        excl_label = Text("Z → Y must only pass through T", font_size=22, color=WHITE).to_edge(DOWN, buff=0.8)

        self.play(FadeIn(z_grp2), FadeIn(t_grp2), FadeIn(y_grp2), run_time=0.9)
        self.play(GrowArrow(zt_arrow2), GrowArrow(ty_arrow2), run_time=0.9)
        self.play(Create(zy_arc), run_time=0.8)
        self.play(FadeIn(zy_cross, scale=0.7), run_time=0.6)
        self.play(Write(excl_label), run_time=1.4)
        self.wait(d[2] - 4.6)

        # Beat 4: independence
        previous2 = VGroup(z_grp2, t_grp2, y_grp2, zt_arrow2, ty_arrow2, zy_arc, zy_cross, excl_label)
        self.play(FadeOut(previous2), run_time=0.6)
        indep_title = Text("Z must be independent of potential outcomes", font_size=24, weight=BOLD, color=ACCENT).to_edge(UP, buff=1.4)
        coin_small = load_icon("coin.svg", COIN_COLOR, 1.0).move_to(LEFT * 3.0)
        latent_box = RoundedRectangle(width=3.8, height=1.4, corner_radius=0.15,
                                       stroke_color=SOFT, stroke_width=2)
        latent_text = Text("Potential outcomes\n( Y₀, Y₁ )", font_size=22, color=WHITE, line_spacing=0.95).move_to(latent_box.get_center())
        latent_grp = VGroup(latent_box, latent_text).move_to(RIGHT * 2.5)
        indep_sym = Text("⊥", font_size=46, weight=BOLD, color=GREEN).move_to(ORIGIN)
        check_note = Text("Randomized assignment: satisfied by design\nNature's coin: argue case by case", font_size=20, color=SOFT, line_spacing=0.95).to_edge(DOWN, buff=0.6)

        self.play(FadeIn(indep_title, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(coin_small), FadeIn(latent_grp), run_time=1.0)
        self.play(Write(indep_sym), run_time=0.8)
        self.play(FadeIn(check_note, shift=UP * 0.1), run_time=1.4)
        self.wait(d[3] - 3.9)

        # Beat 5: all three unlock
        previous3 = VGroup(indep_title, coin_small, latent_grp, indep_sym, check_note)
        self.play(FadeOut(previous3), run_time=0.6)
        unlocks = VGroup()
        for name in lock_names:
            uk = load_icon("lock-open.svg", GREEN, 1.1)
            nm = Text(name, font_size=22, weight=BOLD, color=GREEN).next_to(uk, DOWN, buff=0.25)
            unlocks.add(VGroup(uk, nm))
        unlocks.arrange(RIGHT, buff=1.5).move_to(DOWN * 0.4)
        door_caption = Text("Only when all three open does the IV door open", font_size=24, weight=BOLD, color=INSTRUMENT).to_edge(DOWN, buff=0.6)

        self.play(LaggedStart(*[FadeIn(uk, shift=UP * 0.15) for uk in unlocks], lag_ratio=0.2), run_time=1.4)
        self.play(Write(door_caption), run_time=1.6)
        self.wait(d[4] - 3.0)
        self.wait(self.WAIT_TAIL)


# ═══════════════════════════════════════════════════════════════════
# Scene 06 EN — Draft Lottery
# ═══════════════════════════════════════════════════════════════════


class Scene06_DraftLotteryEN(Scene):
    """English version of Scene 06. 5 chunks, ~71.26s."""

    WAIT_TAIL = 1.5

    def construct(self):
        d = load_scene_timing_durations("06_draft_lottery_en")

        # Beat 1: national scale intro
        title = Text("Same trick, national scale", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        scale_up = Text("Not just for small experiments", font_size=24, color=SOFT).move_to(ORIGIN + UP * 0.2)
        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(scale_up), run_time=1.2)
        self.wait(d[0] - 1.9)

        # Beat 2: 1969 USA draft
        self.play(FadeOut(scale_up), run_time=0.4)
        date_label = Text("USA · 1969", font_size=28, weight=BOLD, color=SOFT).to_edge(UP, buff=1.4)
        balls = VGroup()
        ball_nums = ["73", "144", "012"]
        for num in ball_nums:
            ball = Circle(radius=0.5, color=ACCENT, stroke_width=3, fill_color=YELLOW_A, fill_opacity=0.9)
            ball_num = Text(num, font_size=22, weight=BOLD, color=BLACK).move_to(ball)
            balls.add(VGroup(ball, ball_num))
        balls.arrange(RIGHT, buff=0.5).move_to(UP * 0.2)
        ball_caption = Text("365 birthday balls drawn at random", font_size=22, color=WHITE).next_to(balls, DOWN, buff=0.5)
        rule = Text("Low number → drafted", font_size=24, weight=BOLD, color=INSTRUMENT).move_to(DOWN * 1.5)
        independence_note = Text("Birthdate is unrelated to education or job", font_size=20, color=SOFT).next_to(rule, DOWN, buff=0.3)

        self.play(FadeIn(date_label, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.2, scale=0.7) for b in balls], lag_ratio=0.2), run_time=1.4)
        self.play(Write(ball_caption), run_time=1.4)
        self.play(Write(rule), run_time=1.0)
        self.play(FadeIn(independence_note, shift=UP * 0.1), run_time=0.9)
        self.wait(d[1] - 5.4)

        # Beat 3: Angrist's question
        prior = VGroup(date_label, balls, ball_caption, rule, independence_note)
        self.play(FadeOut(prior), run_time=0.6)
        angrist = Text("Joshua Angrist's question", font_size=26, weight=BOLD, color=ACCENT).to_edge(UP, buff=1.2)
        question = Text('"What is the effect of military service on lifetime earnings?"', font_size=24, color=WHITE).move_to(ORIGIN + UP * 0.4)
        t_q = Text("Service", font_size=24, color=TREAT_COLOR)
        y_q = Text("Earnings", font_size=24, color=CONTROL_COLOR)
        arrow_q = Arrow(LEFT * 1.0, RIGHT * 1.0, buff=0.05, color=WHITE, stroke_width=4)
        chain = VGroup(t_q, arrow_q, y_q).arrange(RIGHT, buff=0.3).move_to(DOWN * 1.0)

        self.play(FadeIn(angrist, shift=DOWN * 0.1), run_time=0.7)
        self.play(Write(question), run_time=1.4)
        self.play(FadeIn(chain, shift=UP * 0.1), run_time=1.0)
        self.wait(d[2] - 3.1)

        # Beat 4: naive bias
        bias_warn = Text("Veterans vs non-veterans simple comparison → bias", font_size=22, color=FORBIDDEN).to_edge(DOWN, buff=2.2)
        bias_reason = Text("Those who chose to serve differ from those who avoided", font_size=20, color=SOFT).next_to(bias_warn, DOWN, buff=0.25)
        self.play(FadeIn(bias_warn, shift=UP * 0.1), run_time=1.0)
        self.play(FadeIn(bias_reason, shift=UP * 0.05), run_time=0.9)
        self.wait(d[3] - 1.9)

        # Beat 5: lottery as IV + Snow callback
        prior2 = VGroup(angrist, question, chain, bias_warn, bias_reason)
        self.play(FadeOut(prior2), run_time=0.6)
        title_fix = Text("Lottery number = instrument", font_size=30, weight=BOLD, color=INSTRUMENT).to_edge(UP, buff=1.2)
        z6 = Circle(radius=0.4, color=INSTRUMENT, stroke_width=3)
        z6t = Text("Lottery", font_size=18, color=INSTRUMENT, weight=BOLD).move_to(z6)
        z6g = VGroup(z6, z6t).move_to(LEFT * 3.5 + DOWN * 0.2)
        t6 = Circle(radius=0.4, color=TREAT_COLOR, stroke_width=3)
        t6t = Text("Service", font_size=18, color=TREAT_COLOR, weight=BOLD).move_to(t6)
        t6g = VGroup(t6, t6t).move_to(ORIGIN + DOWN * 0.2)
        y6 = Circle(radius=0.4, color=CONTROL_COLOR, stroke_width=3)
        y6t = Text("Earnings", font_size=18, color=CONTROL_COLOR, weight=BOLD).move_to(y6)
        y6g = VGroup(y6, y6t).move_to(RIGHT * 3.5 + DOWN * 0.2)
        zt6 = Arrow(z6g.get_right(), t6g.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        ty6 = Arrow(t6g.get_right(), y6g.get_left(), buff=0.12, color=WHITE, stroke_width=3)
        callback = Text("Snow's water company trick from a century earlier\nworked in the US labor market too", font_size=22, color=SOFT, line_spacing=0.95).to_edge(DOWN, buff=0.7)

        self.play(FadeIn(title_fix, shift=DOWN * 0.1), run_time=0.7)
        self.play(FadeIn(z6g), FadeIn(t6g), FadeIn(y6g), run_time=0.9)
        self.play(GrowArrow(zt6), GrowArrow(ty6), run_time=0.9)
        self.play(Indicate(z6g, color=INSTRUMENT), run_time=0.8)
        self.play(Write(callback), run_time=1.6)
        self.wait(d[4] - 4.9)
        self.wait(self.WAIT_TAIL)


# ═══════════════════════════════════════════════════════════════════
# Scene 07 EN — Outro
# ═══════════════════════════════════════════════════════════════════


class Scene07_OutroEN(Scene):
    """English version of Scene 07. 3 chunks, ~31.49s."""

    WAIT_TAIL = 1.5

    def construct(self):
        d = load_scene_timing_durations("07_outro_en")

        # Beat 1: three vignettes
        title = Text("Accidents are already around us", font_size=30, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        snow = self._make_vignette("droplet.svg", CLEAN_WATER, "1854 London", "Water company")
        draft = self._make_vignette("dice.svg", ACCENT, "1969 USA", "Draft lottery")
        birth = self._make_vignette("cake.svg", PINK, "Maybe", "Your birthday")
        vignettes = VGroup(snow, draft, birth).arrange(RIGHT, buff=0.9).move_to(ORIGIN + UP * 0.2)
        common = Text("All accidents already in the real world", font_size=22, color=SOFT).to_edge(DOWN, buff=1.2)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in vignettes], lag_ratio=0.25), run_time=1.8)
        self.play(Write(common), run_time=1.2)
        self.wait(d[0] - 3.7)

        # Beat 2: hardest part isn't the formula
        self.play(FadeOut(common), run_time=0.4)
        hard_line = Text("The hardest part isn't the formula", font_size=26, color=WHITE).move_to(DOWN * 1.4)
        hard_line2 = Text("It's finding the accident", font_size=30, weight=BOLD, color=INSTRUMENT).next_to(hard_line, DOWN, buff=0.3)
        self.play(Write(hard_line), run_time=1.2)
        self.play(Write(hard_line2), run_time=1.4)
        self.wait(d[1] - 3.0)

        # Beat 3: closing card
        self.play(FadeOut(VGroup(title, vignettes, hard_line, hard_line2)), run_time=0.7)
        close_line1 = Text("When you can't randomize,", font_size=28, color=WHITE).move_to(UP * 0.6)
        close_line2 = Text("find the coin nature has already flipped.", font_size=28, weight=BOLD, color=INSTRUMENT).next_to(close_line1, DOWN, buff=0.4)
        end_tag = Text("That's the next step in causal inference.", font_size=22, color=SOFT).next_to(close_line2, DOWN, buff=0.6)

        self.play(Write(close_line1), run_time=1.2)
        self.play(Write(close_line2), run_time=1.4)
        self.play(FadeIn(end_tag, shift=UP * 0.1), run_time=1.0)
        self.wait(d[2] - 3.6)
        self.wait(self.WAIT_TAIL)

    @staticmethod
    def _make_vignette(icon_name: str, color: str, year: str, name: str) -> VGroup:
        try:
            icon = load_icon(icon_name, color, 0.9)
        except Exception:
            icon = Circle(radius=0.4, color=color, stroke_width=3)
        year_text = Text(year, font_size=20, color=color, weight=BOLD)
        name_text = Text(name, font_size=18, color=WHITE)
        block = VGroup(icon, year_text, name_text).arrange(DOWN, buff=0.25)
        return block
