from manim import Create, FadeIn, FadeOut, ReplacementTransform, VGroup

from videos.uplift_modeling.shared.common import (
    AUDIENCES, UpliftScene, at, label, opening_comparison, RatePanel, title,
)


class Lift(UpliftScene):
    script = "02_lift"
    preview_durations = (8.5, 7.0, 8.0)

    def explain(self):
        blocks, header, relation = opening_comparison()
        followup = label("쿠폰 없이도 살 사람은?", 33).move_to(at(0, -2.70))
        self.add(blocks, header, relation, followup)
        panels = [RatePanel(audience) for audience in AUDIENCES]
        header_target = title("같은 고객군에서 두 조건 비교")
        label_lift = title("업리프트", y=3.05)

        with self.clock.beat() as beat:
            moves = []
            for panel, block in zip(panels, blocks):
                moves.extend((
                    FadeOut(block[0]), ReplacementTransform(block[1], panel.treated[3]),
                    ReplacementTransform(block[2], panel.heading), FadeIn(panel.treated[:3]),
                ))
            self.play(
                ReplacementTransform(header, header_target), FadeOut(relation), FadeOut(followup),
                *moves, run_time=1.25,
            )
            self.wait(beat * 0.13)
            self.play(FadeIn(panels[0].control), run_time=0.77)
            self.wait(beat * 0.15)
            self.play(FadeIn(panels[1].control), run_time=0.77)

        with self.clock.beat() as beat:
            self.play(FadeOut(header_target), FadeIn(label_lift), run_time=0.66)
            self.wait(beat * 0.26)
            left = panels[0]
            self.play(Create(left.guides), Create(left.interval), FadeIn(left.delta), run_time=0.98)

        with self.clock.beat() as beat:
            self.wait(beat * 0.31)
            right = panels[1]
            self.play(Create(right.guides), Create(right.interval), FadeIn(right.delta), run_time=0.98)
