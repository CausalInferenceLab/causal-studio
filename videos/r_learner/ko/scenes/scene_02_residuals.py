from manim import Create, FadeIn, FadeOut, GrowArrow, ReplacementTransform, VGroup

from videos.r_learner.shared.common import (
    EXAMPLE, LearnerScene, OUTCOME, ResidualPlot, example_readout, outcome_ruler, store_title, treatment_ruler,
)


class Residuals(LearnerScene):
    script = "02_residuals"
    preview_durations = (8.2, 8.5, 8.5)

    def explain(self):
        outcome, treatment, title = outcome_ruler(), treatment_ruler(), store_title()
        plot = ResidualPlot()
        self.add(outcome.body, title)

        with self.clock.beat() as beat:
            self.wait(beat * 0.49)
            self.play(GrowArrow(outcome.span), FadeIn(outcome.amount), run_time=0.90)

        with self.clock.beat() as beat:
            self.play(Create(treatment.baseline), FadeIn(treatment.title), FadeIn(treatment.expected), run_time=0.78)
            self.wait(beat * 0.25)
            self.play(FadeIn(treatment.actual), run_time=0.56)
            self.wait(beat * 0.15)
            self.play(GrowArrow(treatment.span), FadeIn(treatment.amount), run_time=0.82)

        with self.clock.beat() as beat:
            self.wait(beat * 0.20)
            self.play(
                FadeOut(title),
                FadeOut(VGroup(outcome.body, outcome.span, treatment.body, treatment.span)),
                FadeIn(plot.frame),
                outcome.amount.animate.move_to(plot.point(-0.51, 6)),
                treatment.amount.animate.move_to(plot.point(0.60, -4)),
                run_time=1.00,
            )
            guides = plot.example_marks()
            self.play(
                Create(guides[0]), ReplacementTransform(treatment.amount, guides[2]), run_time=0.88,
            )
            self.play(
                Create(guides[1]), ReplacementTransform(outcome.amount, guides[3]), run_time=0.96,
            )
            self.play(FadeIn(plot.dots([EXAMPLE], OUTCOME)), run_time=0.40)
            self.play(FadeIn(example_readout()), run_time=0.57)
