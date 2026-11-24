from manim import Create, DashedLine, FadeIn, FadeOut, Transform, TransformFromCopy, UP

from videos.did.shared.common import (
    BEFORE_X, CONTROL, CONTROL_BEFORE, DidScene, TREAT_BEFORE, at, label, rides,
)


class Counterfactual(DidScene):
    script = "02_counterfactual"
    preview_durations = (5.0, 7.4, 5.8)
    tail = 0.65

    def animate_explanation(self):
        chart = self.chart
        self.add(chart.frame, chart.observed, chart.treat_growth, chart.control_growth)
        path, estimated, effect = chart.estimate()
        offset = rides(BEFORE_X, TREAT_BEFORE) - rides(BEFORE_X, CONTROL_BEFORE)
        slope_copy = chart.control_line.copy().set_stroke(width=5.0).set_z_index(2)
        result_slope = slope_copy.copy().shift(offset)
        move_guide = DashedLine(
            rides(BEFORE_X, CONTROL_BEFORE), rides(BEFORE_X, TREAT_BEFORE),
            dash_length=0.12, color=CONTROL, stroke_width=1.7,
        )
        question = label("증편이 없었다면?", size=37).move_to(at(0.0, 2.76))

        with self.clock.beat() as beat:
            self.play(FadeOut(chart.treat_growth), run_time=0.55)
            self.wait(beat * 0.25)
            self.play(
                FadeIn(question), chart.treated_line.animate.set_stroke(opacity=0.33),
                chart.treated_to.animate.set_opacity(0.48), run_time=0.62,
            )
        with self.clock.beat() as beat:
            self.play(Create(move_guide), run_time=0.58)
            self.play(
                TransformFromCopy(slope_copy, result_slope),
                Transform(chart.control_growth, chart.comparison_change_at_treated_start()),
                run_time=1.65,
            )
            self.wait(beat * 0.14)
            self.play(FadeOut(result_slope), FadeIn(path), FadeOut(move_guide), run_time=0.56)
            self.play(FadeIn(estimated, shift=UP * 0.10), run_time=0.65)
        with self.clock.beat() as beat:
            self.play(
                chart.treated_line.animate.set_stroke(opacity=1.0),
                chart.treated_to.animate.set_opacity(1.0), FadeOut(question), run_time=0.67,
            )
            self.wait(beat * 0.19)
            self.play(FadeIn(effect[0]), Create(effect[1]), FadeIn(effect[2]), run_time=0.94)
