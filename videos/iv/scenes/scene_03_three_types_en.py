from manim import *

from iv_common import (
    ACCENT,
    ALWAYS_TAKER,
    COIN_COLOR,
    COMPLIER,
    CONTROL_COLOR,
    INSTRUMENT,
    NEVER_TAKER,
    TREAT_COLOR,
    load_scene_timing_durations,
)


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
