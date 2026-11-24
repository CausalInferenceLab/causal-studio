from manim import Create, Dot, FadeIn, FadeOut, Line, ReplacementTransform, UP, VGroup

from videos.did.shared.common import (
    AFTER_X, BEFORE_X, DidScene, GUIDE, INK, MUTED, TREAT_AFTER, TREAT_BEFORE, at, label, numeral,
)


def stop(x, count):
    marker = Dot(at(x, -0.52), radius=0.083, color=INK)
    return VGroup(marker, numeral(count, size=100).next_to(marker, UP, buff=0.31))


class Observed(DidScene):
    script = "01_observed"
    preview_durations = (6.0, 3.2, 5.6)
    tail = 0.65

    def animate_explanation(self):
        chart = self.chart
        left_stop, right_stop = stop(BEFORE_X, TREAT_BEFORE), stop(AFTER_X, TREAT_AFTER)
        route = Line(at(BEFORE_X, -0.52), at(AFTER_X, -0.52), color=GUIDE, stroke_width=2.5)
        story = label("야간버스 증편", size=43).move_to(at(-0.8, 1.96))
        units = label("하루 평균 탑승객 · 명", size=28, color=MUTED).move_to(at(-0.8, 1.40))
        dates = chart.dates.copy().set_y(-1.04)
        dates.set_z_index(1)

        with self.clock.beat() as beat:
            self.play(FadeIn(story), run_time=0.65)
            self.wait(beat * 0.17)
            self.play(FadeIn(units), FadeIn(left_stop), FadeIn(dates[0]), run_time=0.65)
            self.wait(beat * 0.24)
            self.play(Create(route), run_time=0.95)
            self.play(FadeIn(right_stop, shift=UP * 0.12), FadeIn(dates[1]), run_time=0.55)
        with self.clock.beat():
            self.play(
                ReplacementTransform(left_stop, chart.treated_from),
                ReplacementTransform(right_stop, chart.treated_to),
                ReplacementTransform(route, chart.time_rule),
                ReplacementTransform(dates[0], chart.dates[0]),
                ReplacementTransform(dates[1], chart.dates[1]),
                FadeOut(story), ReplacementTransform(units, chart.unit),
                run_time=0.9,
            )
            self.play(Create(chart.treated_line), FadeIn(chart.guides), FadeIn(chart.treated_name), run_time=0.65)
            self.play(FadeIn(chart.treat_growth[0]), Create(chart.treat_growth[1]), FadeIn(chart.treat_growth[2]), run_time=0.75)
        with self.clock.beat() as beat:
            self.play(FadeIn(chart.control_from), FadeIn(chart.control_name), run_time=0.6)
            self.wait(beat * 0.19)
            self.play(Create(chart.control_line), run_time=1.2)
            self.play(FadeIn(chart.control_to), run_time=0.48)
            self.play(
                FadeIn(chart.control_growth[0]), Create(chart.control_growth[1]), FadeIn(chart.control_growth[2]),
                run_time=0.65,
            )
