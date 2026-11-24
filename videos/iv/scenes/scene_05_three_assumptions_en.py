from manim import *

from iv_common import (
    ACCENT,
    COIN_COLOR,
    CONTROL_COLOR,
    FORBIDDEN,
    INSTRUMENT,
    SOFT,
    TREAT_COLOR,
    load_icon,
    load_scene_timing_durations,
)


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
