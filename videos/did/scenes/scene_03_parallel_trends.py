from manim import Create, FadeIn, FadeOut, RIGHT, Transform, TransformFromCopy, VGroup

from videos.did.did_chart import (
    CONTROL, CONTROL_CHANGE, DID, EFFECT, INK, TREAT_AFTER, TREAT_BEFORE, TREAT_CHANGE,
    DidScene, at, label, measure, numeral,
)


class ParallelTrends(DidScene):
    script = "03_parallel_trends"
    preview_durations = (7.1, 7.5, 7.1)
    tail = 1.0

    def animate_explanation(self):
        chart = self.chart
        path, estimated, effect = chart.estimate()
        common_change = chart.comparison_change_at_treated_start()
        self.add(chart.frame, chart.observed, common_change, path, estimated, effect)

        equation = VGroup(
            numeral(TREAT_CHANGE, size=68), numeral("−", size=53),
            numeral(CONTROL_CHANGE, size=68, color=CONTROL), numeral("=", size=53),
            numeral(DID, size=68, color=EFFECT),
        ).arrange(RIGHT, buff=0.24).move_to(at(-0.80, -3.18))
        name = label("차분의 차분", size=39).move_to(at(0.10, 2.76))
        other_path, other_point, other_effect = chart.estimate(TREAT_BEFORE + 40)
        parallel_path, parallel_point, parallel_effect = chart.estimate()
        same_slope = label("평행추세", size=39).move_to(at(0.10, 2.76))

        with self.clock.beat() as beat:
            full_change = measure(5.76, TREAT_BEFORE, TREAT_AFTER, INK, draw_guides=False)
            full_change[2].scale(0.70).next_to(full_change[1], RIGHT, buff=0.13)
            self.play(Create(full_change[1]), FadeIn(full_change[2]), run_time=0.52)
            self.wait(beat * 0.13)
            self.play(
                TransformFromCopy(full_change[2], equation[0]), FadeIn(equation[1]),
                run_time=0.85,
            )
            self.play(
                TransformFromCopy(common_change[2], equation[2]), FadeIn(equation[3]),
                run_time=0.80,
            )
            self.play(TransformFromCopy(effect[2], equation[4]), FadeOut(full_change), run_time=0.76)
            self.wait(beat * 0.17)
            self.play(FadeIn(name), run_time=0.5)
        with self.clock.beat() as beat:
            self.play(FadeOut(equation), FadeOut(name), FadeOut(common_change), run_time=0.60)
            self.wait(beat * 0.21)
            self.play(
                Transform(path, other_path),
                Transform(estimated, other_point),
                Transform(effect, other_effect), run_time=1.78,
            )
        with self.clock.beat() as beat:
            self.wait(beat * 0.24)
            self.play(
                Transform(path, parallel_path), Transform(estimated, parallel_point),
                Transform(effect, parallel_effect), run_time=1.72,
            )
            self.wait(beat * 0.15)
            self.play(FadeIn(same_slope), run_time=0.70)
