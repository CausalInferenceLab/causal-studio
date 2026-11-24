from manim import (
    Create, DecimalNumber, DOWN, FadeIn, FadeOut, ValueTracker, VGroup, always_redraw,
)

from videos.r_learner.visuals import (
    EXAMPLE, LARGE, LearnerScene, MUTED, OUTCOME, ResidualPlot, at, example_readout, label, large_summary,
    math, squared_loss,
)


class Fit(LearnerScene):
    script = "03_fit"
    preview_durations = (8.6, 7.6, 8.6)

    def explain(self):
        plot = ResidualPlot()
        demo = plot.example_marks()
        example = plot.dots([EXAMPLE], OUTCOME)
        other_dots = plot.dots([point for point in LARGE if point != EXAMPLE])
        readout = example_readout()
        self.add(plot.frame, demo, example, readout)
        group = label("큰 매장", 34).move_to(at(4.8, 2.10))
        slope = ValueTracker(6.0)
        fit = always_redraw(lambda: plot.fit(slope.get_value()))
        errors = always_redraw(lambda: plot.errors(LARGE, slope.get_value()))
        loss_caption = label("세로 오차 제곱합", 29, MUTED).move_to(at(4.8, -0.38))
        loss_number = DecimalNumber(squared_loss(LARGE, 6), num_decimal_places=1, font_size=55, color=OUTCOME)
        loss_number.move_to(at(4.8, -1.00))
        loss_number.add_updater(lambda number: number.set_value(squared_loss(LARGE, slope.get_value())).move_to(at(4.8, -1.00)))
        r_loss = math(r"\sum_i(\widetilde Y_i-\tau\,\widetilde W_i)^2", size=34).move_to(at(4.5, -1.77))

        with self.clock.beat() as beat:
            self.play(FadeOut(demo), FadeOut(readout), FadeIn(group), FadeIn(other_dots, lag_ratio=0.18), run_time=1.16)
            self.wait(beat * 0.28)

        with self.clock.beat() as beat:
            first_line = plot.fit(slope.get_value())
            self.play(Create(first_line), run_time=0.80)
            self.remove(first_line)
            self.add(fit)
            self.play(FadeIn(errors), run_time=0.70)
            self.wait(beat * 0.18)
            self.play(slope.animate.set_value(10), run_time=1.42)

        with self.clock.beat() as beat:
            self.play(FadeIn(loss_caption), FadeIn(loss_number), FadeIn(r_loss), run_time=0.72)
            self.wait(beat * 0.15)
            self.play(slope.animate.set_value(16), run_time=1.95)
            self.wait(beat * 0.12)
            loss_number.clear_updaters()
            errors.clear_updaters()
            self.play(
                FadeOut(VGroup(group, loss_caption, loss_number, r_loss, errors)),
                FadeIn(large_summary(), shift=DOWN * 0.10), run_time=0.74,
            )
