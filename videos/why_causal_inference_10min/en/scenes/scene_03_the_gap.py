"""Separate the two distances in the observed gap using notebook cells 10 and 17."""

from pathlib import Path
import sys

from manim import (
    DOWN, UP, Create, DashedLine, FadeIn, FadeOut, Indicate, VGroup,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "shared"))

from visual import GHOST, GOLD, INK, MUTED, TREATED, LessonScene, ScoreRuler, ink


class Scene03(LessonScene):
    def construct(self):
        ruler = ScoreRuler()
        clock = self.clock("03_the_gap")
        axis_y = ruler.AXIS_Y
        treated = ruler.mean(675, TREATED)
        alternate = ruler.mean(750, GHOST, hollow=True)
        comparison = ruler.mean(550, MUTED)
        average_heading = ruler.lane("Average score", axis_y)
        effect_y = -0.02
        selection_y = 1.10
        net_y = -1.03

        def guide(score, end_y, color, opacity=0.42):
            return DashedLine(
                ruler.at(score, axis_y + 0.12), ruler.at(score, end_y + 0.055),
                color=color, stroke_width=1.6, stroke_opacity=opacity, dash_length=0.055,
            ).set_z_index(-1)

        old_contrast = ruler.contrast(750, 675)
        old_comparison_label = ink("with − without", 20, GOLD).next_to(
            old_contrast[0], DOWN, buff=0.16,
        )
        old_guides = VGroup(guide(675, -0.93, TREATED), guide(750, -0.93, GHOST))
        past_gap = ruler.contrast(550, 675, color=GOLD, y=0.95)
        past_heading = ruler.lane("Different schools", 0.95, MUTED)
        past_guide = guide(550, 0.95, MUTED, opacity=0.26)
        current_heading = ruler.lane("Same schools", -0.93, MUTED)

        selection = ruler.contrast(550, 750, color=GHOST, y=selection_y)
        effect = ruler.contrast(750, 675, color=TREATED, y=effect_y)
        net = ruler.contrast(550, 675, y=net_y)
        comparison_guide = guide(550, selection_y, MUTED)
        hypothetical_guide = guide(750, selection_y, GHOST)
        observed_guide = guide(675, effect_y, TREATED)
        selection_prompt = ruler.lane("Switch schools", selection_y, GHOST)
        effect_prompt = ruler.lane("Give tablets", effect_y, TREATED)
        selection_label = ruler.lane("Selection bias", selection_y, GHOST)
        effect_label = ruler.lane("Tablet effect", effect_y, TREATED)
        total_label = ruler.lane("Observed gap", net_y, GOLD)

        self.add(
            ruler.axis(), average_heading, treated, alternate,
            old_contrast, old_comparison_label, old_guides,
        )

        with clock.beat() as duration:
            self.wait(0.10 * duration)
            self.play(
                FadeIn(comparison), FadeIn(current_heading),
                Create(past_guide), Create(past_gap[0]),
                FadeIn(past_gap[1]), FadeIn(past_heading),
                run_time=0.12 * duration,
            )
            self.wait(0.10 * duration)
            self.play(
                Indicate(treated, scale_factor=1.17, color=TREATED),
                run_time=0.16 * duration,
            )
            self.wait(0.17 * duration)
            self.play(
                Indicate(comparison, scale_factor=1.14, color=MUTED),
                Indicate(alternate, scale_factor=1.14, color=GHOST),
                run_time=0.14 * duration,
            )

        with clock.beat() as duration:
            self.play(
                FadeOut(old_contrast), FadeOut(old_guides), FadeOut(old_comparison_label),
                FadeOut(past_gap), FadeOut(past_guide), FadeOut(past_heading),
                FadeOut(current_heading),
                run_time=0.06 * duration,
            )
            self.wait(0.13 * duration)
            self.play(
                Create(comparison_guide),
                Indicate(comparison, scale_factor=1.12, color=MUTED),
                run_time=0.08 * duration,
            )
            self.wait(0.17 * duration)
            self.play(
                Create(hypothetical_guide),
                Indicate(alternate, scale_factor=1.12, color=GHOST),
                run_time=0.08 * duration,
            )
            self.wait(0.10 * duration)
            self.play(
                Create(selection[0]), FadeIn(selection_prompt),
                run_time=0.09 * duration,
            )
            self.play(FadeIn(selection[1], shift=0.05 * UP), run_time=0.04 * duration)

        with clock.beat() as duration:
            self.wait(0.34 * duration)
            self.play(FadeIn(effect_prompt), run_time=0.09 * duration)
            self.wait(0.12 * duration)
            self.play(
                Create(effect[0]), Create(observed_guide),
                FadeIn(effect[1], shift=0.05 * UP),
                run_time=0.19 * duration,
            )

        with clock.beat() as duration:
            self.wait(0.28 * duration)
            self.play(
                Create(net[0]), FadeIn(net[1], shift=0.05 * UP), FadeIn(total_label),
                run_time=0.12 * duration,
            )
            self.wait(0.08 * duration)
            self.play(FadeOut(selection_prompt), run_time=0.043 * duration)
            self.play(FadeIn(selection_label), run_time=0.043 * duration)
            self.wait(0.08 * duration)
            self.play(FadeOut(effect_prompt), run_time=0.043 * duration)
            self.play(FadeIn(effect_label), run_time=0.043 * duration)
            self.wait(0.07 * duration)
            self.play(
                Indicate(net[1], scale_factor=1.08, color=GOLD),
                run_time=0.10 * duration,
            )
        clock.finish()
