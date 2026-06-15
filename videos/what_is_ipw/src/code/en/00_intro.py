from manim import *

# Scene 00 (EN) — intro title card (~7s).
# timings: build/audio/00_intro_en.timings.json (total 6.92s)
#   chunk1 0.0~3.1, chunk2 3.1~6.92


class Intro(Scene):
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

        topic = Text("Today's topic", font_size=36, color=GRAY_A, weight=BOLD)
        ipw = Text("IPW", font_size=150, color=ORANGE, weight=BOLD)
        full = Text("Inverse Probability Weighting", font_size=40, color=WHITE, weight=BOLD)
        title = VGroup(topic, ipw, full).arrange(DOWN, buff=0.4).move_to(UP * 0.2)
        rule = Line(LEFT * 2.9, RIGHT * 2.9, color=ORANGE, stroke_width=3).next_to(ipw, DOWN, buff=0.18)
        sub = Text("Finding the true cause from observational data",
                   font_size=30, color=GRAY_B, weight=BOLD).next_to(title, DOWN, buff=0.7)

        play_at(0.3, FadeIn(topic, shift=DOWN * 0.1), run_time=0.4)
        play_at(0.85, Write(ipw), run_time=0.7)
        play_at(1.75, GrowFromCenter(rule), FadeIn(full, shift=UP * 0.1), run_time=0.5)
        play_at(3.7, FadeIn(sub, shift=UP * 0.1), run_time=0.5)   # chunk2

        go_to(7.6)
