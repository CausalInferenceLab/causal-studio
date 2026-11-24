from manim import *

from why_causal_inference_common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    load_icon,
)


class Scene04_MultiverseIteAteAtt(Scene):
    """
    Scene 04: ITE, ATE, ATT 정의

    Core Claim:
    반사실 개념 위에서 ITE를 정의할 수 있고,
    현실에서는 ITE를 직접 계산할 수 없기 때문에 ATE와 ATT 같은 평균 효과를 본다.

    Expected Misconception:
    ITE, ATE, ATT 표기가 한꺼번에 나오면
    모두 다른 개념처럼 보이지만, 사실은 같은 차이를 어디에 대해 평균내느냐의 차이다.

    Visual Pivot:
    먼저 같은 학교의 두 결과 차이로 ITE를 보여준 뒤,
    ITE는 직접 계산하기 어렵다는 제약을 강조하고,
    마지막에 ATE와 ATT를 평균 효과 두 줄로 정리한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "실제로 일어난 쪽은 factual이고, 일어나지 않은 다른 한쪽은 counterfactual로 남습니다."
    - 현재 Scene 첫 문장:
      "이 개념을 바탕으로 개별 처치 효과, 즉 ITE를 정의할 수 있습니다."
    - Cell 6 tail:
      ITE 정의 ~ ATE 정의 ~ ATT 정의

    Script Reference:
    src/scripts/04_multiverse_ite_ate_att.txt

    Asset Reference:
    none

    3Blue1Brown Reference:
    3b1b/videos/_2024/transformers/ml_basics.py
    Reason:
    짧은 수식 정의를 먼저 놓고, 그 다음 핵심 제약과 평균 효과를 단계적으로 정리하는 리듬이 유사하다.

    Script-to-Beat Mapping:
    1. ITE를 같은 학교의 두 잠재적 결과 차이로 정의
    2. 반사실을 관찰할 수 없어서 ITE를 직접 계산할 수 없다고 정리
    3. ATE와 ATT를 평균 효과로 정리
    """

    WAIT_TAIL = 8.2

    def construct(self):
        # Beat 1 준비:
        # 직전 Scene에서 factual / counterfactual 두 결과를 동시에 볼 수 없다는 점을 다뤘다.
        # 여기서는 바로 그 두 결과 차이가 ITE라는 것을 같은 학교 한 곳의 두 작은 상태 카드로 압축해 보여준다.
        ite_title = MathTex(r"ITE_i", r"=", r"Y_{1i}", r"-", r"Y_{0i}")
        ite_title.scale(1.08)
        ite_title[0].set_color(ACCENT_COLOR)
        ite_title[2].set_color(TABLET_COLOR)
        ite_title[4].set_color(LIBRARY_COLOR)
        ite_title.to_edge(UP, buff=0.65)

        left_frame = RoundedRectangle(
            width=2.55,
            height=2.6,
            corner_radius=0.18,
            stroke_color=TABLET_COLOR,
            stroke_width=2.6,
        )
        left_treat = MathTex(r"T_i = 1").scale(0.9).set_color(TABLET_COLOR)
        left_icon = load_icon("device-tablet.svg", TABLET_COLOR, 0.8)
        left_outcome = MathTex(r"Y_{1i}").scale(1.0).set_color(WHITE)
        left_group = VGroup(left_treat, left_icon, left_outcome).arrange(DOWN, buff=0.22)
        left_group.move_to(left_frame.get_center())
        left_world = VGroup(left_frame, left_group)
        left_world.move_to(LEFT * 2.2 + DOWN * 0.05)

        right_frame = RoundedRectangle(
            width=2.55,
            height=2.6,
            corner_radius=0.18,
            stroke_color=LIBRARY_COLOR,
            stroke_width=2.6,
        )
        right_treat = MathTex(r"T_i = 0").scale(0.9).set_color(LIBRARY_COLOR)
        right_icon = load_icon("device-tablet-off.svg", LIBRARY_COLOR, 0.8)
        right_outcome = MathTex(r"Y_{0i}").scale(1.0).set_color(WHITE)
        right_group = VGroup(right_treat, right_icon, right_outcome).arrange(DOWN, buff=0.22)
        right_group.move_to(right_frame.get_center())
        right_world = VGroup(right_frame, right_group)
        right_world.move_to(RIGHT * 2.2 + DOWN * 0.05)

        ite_arrow = DoubleArrow(
            left_world.get_right() + RIGHT * 0.08,
            right_world.get_left() + LEFT * 0.08,
            buff=0.1,
            stroke_width=4,
            color=ACCENT_COLOR,
        )
        # Beat 2 준비:
        # ITE는 직관적으로 명확하지만 반사실을 관찰할 수 없어서 직접 계산할 수 없다는 제약을 보여준다.
        # 새 박스를 더하지 않고 기존 두 카드만 남긴 채, 오른쪽 카드만 가려서 반사실의 비관측성을 표현한다.
        # Beat 3 준비:
        # ITE의 차이를 전체 평균과 처치집단 평균으로 확장해 ATE, ATT를 정의한다.
        ate_def = MathTex(r"ATE", r"=", r"E[Y_1 - Y_0]")
        ate_def.scale(0.98)
        ate_def[0].set_color(ACCENT_COLOR)
        ate_def.move_to(ORIGIN)
        ate_expand = VGroup(
            Text("Average", font_size=23, color=WHITE, weight=BOLD),
            Text("Treatment", font_size=23, color=ACCENT_COLOR, weight=BOLD),
            Text("Effect", font_size=23, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.16)
        ate_expand.next_to(ate_def, DOWN, buff=0.34)

        att_def = MathTex(r"ATT", r"=", r"E[Y_1 - Y_0 \mid T=1]")
        att_def.scale(0.94)
        att_def[0].set_color(QUESTION_COLOR)
        att_def.move_to(ORIGIN)
        att_expand = VGroup(
            Text("Average", font_size=22, color=WHITE, weight=BOLD),
            Text("Treatment", font_size=22, color=QUESTION_COLOR, weight=BOLD),
            Text("Effect", font_size=22, color=WHITE, weight=BOLD),
            Text("on the Treated", font_size=22, color=NEUTRAL_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.14)
        att_expand.next_to(att_def, DOWN, buff=0.34)

        avg_hint = Text("전체 집단", font_size=25, color=NEUTRAL_COLOR, weight=BOLD)
        avg_hint.next_to(ate_expand, DOWN, buff=0.28)
        att_hint = Text("처치받은 집단만", font_size=25, color=NEUTRAL_COLOR, weight=BOLD)
        att_hint.move_to(avg_hint)

        # Beat 1:
        # 스크립트의 "ITE를 정의할 수 있다"와 "Y_1 - Y_0" 설명을 처리한다.
        # 상단에는 정의 하나, 가운데에는 두 상태 카드만 둬 겹침 없이 '차이' 자체를 먼저 고정한다.
        self.play(FadeIn(ite_title, shift=UP * 0.08), run_time=0.8)
        self.play(
            FadeIn(left_world, shift=RIGHT * 0.18),
            FadeIn(right_world, shift=LEFT * 0.18),
            run_time=1.0,
        )
        self.play(GrowArrow(ite_arrow), run_time=0.7)
        self.wait(11.0)

        # Beat 2:
        # 스크립트의 "반사실을 관찰할 수 없으므로 ITE는 직접 계산할 수 없다"를 처리한다.
        # 두 카드 자체는 유지하고, 오른쪽 카드만 가려 새 요소 난립 없이 비관측성을 표현한다.
        self.play(
            FadeOut(ite_arrow),
            left_world.animate.move_to(LEFT * 2.2 + DOWN * 0.05),
            right_world.animate.move_to(RIGHT * 2.2 + DOWN * 0.05),
            run_time=0.9,
        )
        veil = Rectangle(
            width=right_world.width * 0.96,
            height=right_world.height * 0.96,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=0.62,
        ).move_to(right_world)
        eye_off = load_icon("eye-off.svg", WHITE, 0.72).move_to(right_world.get_center() + DOWN * 0.15)

        self.play(Indicate(left_world, color=TABLET_COLOR, scale_factor=1.02), run_time=0.7)
        self.play(FadeIn(veil), FadeIn(eye_off), run_time=0.6)
        self.wait(4.8)

        # Beat 3:
        # 스크립트의 "현실적인 대안으로 ATE", "처치받은 사람들에게 한정한 ATT"를 처리한다.
        # 직접 계산 불가라는 제약을 평균 효과로 넘기되, '누구에 대한 평균인가'가 바뀌는 점을 순차적으로 보여준다.
        self.play(
            FadeOut(VGroup(left_world, right_world, veil, eye_off), shift=DOWN * 0.1),
            FadeOut(ite_title, shift=UP * 0.08),
            run_time=0.9,
        )
        self.play(FadeIn(ate_def, shift=UP * 0.08), run_time=0.7)
        self.play(FadeIn(ate_expand, shift=UP * 0.08), run_time=0.6)
        self.play(FadeIn(avg_hint, shift=UP * 0.08), run_time=0.6)
        self.wait(8.4)
        self.play(
            TransformMatchingTex(ate_def, att_def),
            FadeTransform(ate_expand, att_expand),
            FadeTransform(avg_hint, att_hint),
            run_time=0.9,
        )
        self.wait(self.WAIT_TAIL)
