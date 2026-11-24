from manim import *

from videos.iv.shared.common import (
    ACCENT,
    CLEAN_WATER,
    INSTRUMENT,
    SOFT,
    load_icon,
    load_scene_timing_durations,
)


class Scene07_OutroEN(Scene):
    """English version of Scene 07. 3 chunks, ~31.49s."""

    WAIT_TAIL = 1.5

    def construct(self):
        d = load_scene_timing_durations("07_outro", language="en")

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
