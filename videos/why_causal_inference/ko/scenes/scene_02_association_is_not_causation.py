from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_icon,
    make_academic_outcome_icon,
    make_tablet_icon,
)


class Scene02_AssociationIsNotCausation(Scene):
    """
    Scene 02: Association Is Not Causation

    Core Claim:
    태블릿이 있는 학교의 성적이 높아 보여도,
    그 차이를 태블릿 효과라고 바로 해석할 수는 없다.

    Expected Misconception:
    태블릿이 있는 학교의 평균 성적이 더 높으면,
    태블릿이 성취도를 높였다고 곧바로 결론 내리기 쉽다.

    Visual Pivot:
    태블릿 학교와 높은 성적의 연결선이 먼저 나타난 뒤,
    재정, 보충수업, 교사 확보 같은 다른 요인이 끼어들면서
    마지막에는 '연관관계'만 남는다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - Section 1 opening:
      태블릿 학교의 높은 성적은 인과가 아니라 연관일 수 있다는 직관 설명

    Script Reference:
    narration/02_association_is_not_causation.txt

    Asset Reference:
    Tabler Icons (MIT)
    - device-tablet.svg
    - school.svg
    - coin.svg
    - users-group.svg
    - school-bell.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py - IntroQuestion
    3b1b/videos/_2024/transformers/ml_basics.py
    Reason:
    앞쪽은 단순한 질문 구조를,
    뒤쪽은 짧은 라벨 여러 개를 깔끔하게 비교하는 배치를 참고했다.

    Script-to-Beat Mapping:
    1. 태블릿 학교와 높은 성적이 같이 보이는 장면
    2. 재정, 보충수업, 교사 확보가 이미 달랐을 수 있다는 점 제시
    3. 태블릿만으로 결론 내릴 수 없고, 남는 것은 연관관계라는 점 정리
    """

    WAIT_TAIL = 8.8

    def construct(self):
        # Beat 1 준비:
        # 태블릿과 높은 성적의 동시 관찰을 먼저 보여준다.
        left_icon = make_tablet_icon(TABLET_COLOR)
        left_icon.move_to(LEFT * 2.55 + DOWN * 0.1)
        right_icon = make_academic_outcome_icon(WHITE)
        right_icon.move_to(RIGHT * 2.55 + DOWN * 0.1)
        relation_arrow = Arrow(
            left_icon.get_right() + RIGHT * 0.1,
            right_icon.get_left() + LEFT * 0.1,
            buff=0.08,
            stroke_width=4,
            color=ACCENT_COLOR,
        )
        left_label = Text("태블릿 지급", font_size=24, color=TABLET_COLOR, weight=BOLD)
        left_label.next_to(left_icon, DOWN, buff=0.26)
        right_label = Text("높은 성적", font_size=24, color=ACCENT_COLOR, weight=BOLD)
        right_label.next_to(right_icon, DOWN, buff=0.26)

        # Beat 2 준비:
        # 태블릿 외에도 학교를 다르게 만드는 기존 여건이
        # 처치와 결과에 동시에 영향을 준다는 구조를 위쪽에서 내려오게 만든다.
        confounder_chips = VGroup(
            VGroup(load_icon("coin.svg", GOLD_E, 0.55), Text("재정", font_size=19, color=GOLD_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
            VGroup(load_icon("school-bell.svg", BLUE_E, 0.55), Text("보충수업", font_size=19, color=BLUE_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
            VGroup(load_icon("users-group.svg", GREEN_E, 0.62), Text("교사 확보", font_size=19, color=GREEN_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.38)
        confounder_title = Text("학교 여건", font_size=24, color=WHITE, weight=BOLD)
        confounder_title.next_to(confounder_chips, UP, buff=0.22)
        confounder_box = RoundedRectangle(
            width=5.9,
            height=1.75,
            corner_radius=0.18,
            stroke_color=NEUTRAL_COLOR,
            stroke_width=2.2,
        )
        confounder_group = VGroup(confounder_box, confounder_title, confounder_chips)
        confounder_group.move_to(UP * 2.05)

        backdoor_left = CurvedArrow(
            confounder_group.get_bottom() + LEFT * 1.2,
            left_icon.get_top() + UP * 0.05,
            angle=0.32,
            color=NEUTRAL_COLOR,
            stroke_width=3.2,
        )
        backdoor_right = CurvedArrow(
            confounder_group.get_bottom() + RIGHT * 1.2,
            right_icon.get_top() + UP * 0.05,
            angle=-0.32,
            color=NEUTRAL_COLOR,
            stroke_width=3.2,
        )

        # Beat 3 준비:
        # 마지막에는 인과 화살표를 지우고, 연관관계만 남긴다.
        assoc = VGroup(
            Text("상관관계", font_size=34, color=WHITE, weight=BOLD),
            MathTex(r"\ne").scale(1.15).set_color(QUESTION_COLOR),
            Text("인과관계", font_size=34, color=QUESTION_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.28)
        assoc.move_to(UP * 1.85)
        foot = Text("태블릿 효과라고 바로 말할 수는 없다", font_size=24, color=NEUTRAL_COLOR)
        foot.next_to(assoc, DOWN, buff=0.34)

        # Beat 1:
        # "태블릿이 있는 학교의 성적이 높다"는 관찰 자체를 보여준다.
        self.play(FadeIn(left_icon, scale=0.9), FadeIn(right_icon, scale=0.9), run_time=0.9)
        self.play(
            GrowArrow(relation_arrow),
            FadeIn(left_label, shift=UP * 0.08),
            FadeIn(right_label, shift=UP * 0.08),
            run_time=0.9,
        )
        self.wait(4.6)

        # Beat 2:
        # 태블릿 말고도 학교를 다르게 만드는 요인이 이미 있었고,
        # 그 요인들이 처치와 결과에 동시에 영향을 준다는 점을 보여준다.
        self.play(FadeIn(confounder_group, shift=DOWN * 0.12), run_time=0.9)
        self.play(Create(backdoor_left), Create(backdoor_right), run_time=0.9)
        self.wait(12.8)  # chunk2 종료(20.99s)까지 Beat2가 1.8s 부족 → 12.8s로 늘려 싱크+끊김 보정

        # Beat 3:
        # 태블릿만으로는 결론을 낼 수 없고, 남는 것은 연관관계뿐이라는 점으로 정리한다.
        self.play(
            FadeOut(relation_arrow),
            FadeOut(confounder_group),
            FadeOut(backdoor_left),
            FadeOut(backdoor_right),
            FadeOut(left_label),
            FadeOut(right_label),
            run_time=0.6,
        )
        self.play(FadeIn(assoc, shift=UP * 0.12), run_time=0.8)
        self.play(FadeIn(foot, shift=UP * 0.08), run_time=0.6)
        self.wait(self.WAIT_TAIL)
