from pathlib import Path

from manim import (
    DOWN, GREEN, UP, WHITE, YELLOW, Create, FadeIn, ReplacementTransform,
    Scene, Square, SurroundingRectangle, Text, VGroup,
)

from manim_timing import BeatClock


class BinarySearch(Scene):
    def construct(self):
        timing_file = Path(__file__).resolve().parents[1] / "build" / "audio" / "01_find_target.timings.json"
        clock = BeatClock(self, timing_file, (2.2, 2.0, 2.2))
        values = (3, 7, 11, 18, 23, 31, 42)
        title = Text("Find 31", font_size=48).move_to(UP * 2)
        cells = VGroup(
            *(VGroup(Square(side_length=0.95, color=WHITE), Text(str(value), font_size=32))
              for value in values)
        ).arrange(buff=0.16)
        midpoint = SurroundingRectangle(cells[3], color=YELLOW, buff=0.05)
        found = SurroundingRectangle(cells[5], color=GREEN, buff=0.05)
        captions = [
            Text(text, font_size=31, color=color).move_to(DOWN * 2.7)
            for text, color in (("Start at the middle", WHITE), ("31 > 18", YELLOW), ("31 found", GREEN))
        ]
        body = VGroup(cells, midpoint, found)
        for caption in captions:
            if body.get_bottom()[1] < caption.get_top()[1] + 0.25:
                raise ValueError("The caption must leave clear space below the visualization.")

        with clock.beat() as seconds:
            self.play(FadeIn(title), FadeIn(cells), run_time=seconds * 0.25)
            self.play(Create(midpoint), FadeIn(captions[0]), run_time=seconds * 0.30)
        with clock.beat() as seconds:
            self.play(ReplacementTransform(captions[0], captions[1]), run_time=seconds * 0.20)
            self.play(*(cell.animate.set_opacity(0.22) for cell in cells[:4]), run_time=seconds * 0.35)
        with clock.beat() as seconds:
            self.play(ReplacementTransform(midpoint, found),
                      ReplacementTransform(captions[1], captions[2]), run_time=seconds * 0.40)
        clock.finish()
