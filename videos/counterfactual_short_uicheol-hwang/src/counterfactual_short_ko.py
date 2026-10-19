"""같은 학생의 두 세계: 한국어 세로형 쇼츠.

이 파일에서만 9:16 화면을 설정한다. 다른 영상의 Manim 설정은 바꾸지 않는다.
"""

from pathlib import Path

from manim import (
    BLACK,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    RoundedRectangle,
    Scene,
    SVGMobject,
    Text,
    VGroup,
    config,
)


config.background_color = BLACK
config.frame_width = 4.5
config.frame_height = 8.0
config.pixel_width = 720
config.pixel_height = 1280
config.frame_rate = 30

FONT = "Apple SD Gothic Neo"
STUDENT_COLOR = "#F4F5F7"
TABLET_COLOR = "#68C9E8"
SCORE_COLOR = "#80D6A3"
QUESTION_COLOR = "#F4C86A"
CONTROL_COLOR = "#AEB4C0"
ICON_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"


def tabler_icon(name: str, color: str, height: float) -> SVGMobject:
    """Scene마다 같은 Tabler 아이콘과 색 규칙을 사용할 수 있게 한다."""
    icon = SVGMobject(str(ICON_DIR / name))
    icon.set_stroke(color=color, width=3.5)
    icon.set_fill(opacity=0)
    icon.set_height(height)
    return icon


class Scene01_TabletQuestion(Scene):
    """Scene 01 — 성적 상승만으로 태블릿 효과를 단정할 수 없다.

    오해: 태블릿을 받은 뒤 성적이 올랐으니 태블릿이 원인이라는 생각.
    시각적 전환: 관찰된 장면 전체가 사라지며 질문이 중앙에 들어온다.
    노트북: why_causal_inference_ko.ipynb, markdown 셀 3·5.
    영상 참고: videos/why_causal_inference/src/why_causal_inference.py의
    질문 제기와 태블릿 예시. 검정 배경에서 한 대상과 짧은 질문을 강조한다.
    스크립트: src/scripts/ko/01_tablet_question.txt
    청크 1 (0.000~6.504초): 태블릿 수령 후 성적 상승.
    청크 2 (6.504~13.704초): 태블릿 효과인지 질문하고 판단 보류.
    """

    def construct(self):
        # 첫 청크: 화면에는 학생 한 명만 둔다. 태블릿과 성적은 순서대로
        # 나타내되 둘 사이에 인과 화살표를 그리지 않는다.
        # 핵심 그룹: 학생(상), 태블릿 수령(중), 성적 상승(하).
        student = tabler_icon("user.svg", STUDENT_COLOR, 1.18)
        student.move_to(UP * 2.55)
        student_label = Text("한 학생", font=FONT, font_size=29, color=STUDENT_COLOR)
        student_label.next_to(student, DOWN, buff=0.15)
        student_group = VGroup(student, student_label)

        receive_arrow = Arrow(
            start=UP * 1.30,
            end=UP * 0.84,
            buff=0,
            stroke_width=3.5,
            color=TABLET_COLOR,
            max_tip_length_to_length_ratio=0.22,
        )
        tablet = tabler_icon("device-tablet.svg", TABLET_COLOR, 0.90)
        tablet.move_to(UP * 0.25)
        tablet_group = VGroup(receive_arrow, tablet)

        score_icon = tabler_icon("arrow-up.svg", SCORE_COLOR, 0.86)
        score_icon.move_to(DOWN * 1.43)
        score_label = Text("성적 상승", font=FONT, font_size=36, color=SCORE_COLOR)
        score_label.next_to(score_icon, DOWN, buff=0.17)
        score_group = VGroup(score_icon, score_label)

        self.play(FadeIn(student_group, shift=UP * 0.10), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(tablet_group, shift=UP * 0.10), run_time=0.6)
        self.wait(1.0)
        self.play(FadeIn(score_group, shift=UP * 0.10), run_time=0.7)
        self.wait(2.604)  # 청크 1의 끝인 6.504초에 맞춘다.

        # 둘째 청크: 첫 화면 전체를 빠르게 지운 뒤 질문을 중앙으로 들인다.
        # 남는 이전 요소는 없고, 새로 읽을 대상은 질문 하나뿐이다.
        first_beat = VGroup(student_group, tablet_group, score_group)
        question_icon = tabler_icon("question-mark.svg", QUESTION_COLOR, 1.20)
        question_label = Text("태블릿 덕분?", font=FONT, font_size=38, color=QUESTION_COLOR)
        question_group = VGroup(question_icon, question_label).arrange(DOWN, buff=0.30)
        question_group.move_to(ORIGIN)

        answer = Text("아직 모른다", font=FONT, font_size=42, color=STUDENT_COLOR)
        answer.move_to(ORIGIN)

        self.play(FadeOut(first_beat, shift=UP * 0.20), run_time=0.35)
        self.play(FadeIn(question_group, shift=DOWN * 0.25), run_time=0.45)
        self.wait(2.3)
        self.play(FadeOut(question_group), FadeIn(answer, shift=UP * 0.08), run_time=0.6)
        self.wait(4.0)  # 14.204초: mp3 종료 뒤 0.5초의 화면 여백.


def student_marker() -> VGroup:
    """두 세계 Scene에서 같은 학생임을 고정하는 화면 상단 표식."""
    icon = tabler_icon("user.svg", STUDENT_COLOR, 1.18)
    icon.move_to(UP * 2.55)
    label = Text("같은 학생", font=FONT, font_size=29, color=STUDENT_COLOR)
    label.next_to(icon, DOWN, buff=0.15)
    return VGroup(icon, label)


def world_panel(received: bool) -> VGroup:
    """같은 학생에게 가능한 두 조건을 같은 크기와 위치 문법으로 표시한다."""
    x = -1.06 if received else 1.06
    color = TABLET_COLOR if received else CONTROL_COLOR
    icon_name = "device-tablet.svg" if received else "device-tablet-off.svg"
    label_text = "받음" if received else "안 받음"

    frame = RoundedRectangle(
        width=1.80,
        height=2.45,
        corner_radius=0.14,
        stroke_color=color,
        stroke_width=2.7,
        fill_color=BLACK,
        fill_opacity=0,
    )
    frame.move_to(RIGHT * x + DOWN * 0.85)
    icon = tabler_icon(icon_name, color, 0.70)
    icon.move_to(RIGHT * x + DOWN * 0.38)
    label = Text(label_text, font=FONT, font_size=26, color=color)
    label.move_to(RIGHT * x + DOWN * 1.43)
    return VGroup(frame, icon, label)


def world_branches() -> VGroup:
    """위의 학생 한 명에서 두 조건으로 갈라지는 화살표."""
    return VGroup(
        Arrow(
            start=UP * 1.37,
            end=LEFT * 1.06 + UP * 0.54,
            buff=0,
            stroke_width=2.8,
            color=TABLET_COLOR,
        ),
        Arrow(
            start=UP * 1.37,
            end=RIGHT * 1.06 + UP * 0.54,
            buff=0,
            stroke_width=2.8,
            color=CONTROL_COLOR,
        ),
    )


class Scene02_TwoWorlds(Scene):
    """Scene 02 — 태블릿 효과의 비교 대상은 같은 학생의 두 가능한 세계다.

    오해: 태블릿을 받은 학생과 다른 학생을 비교하는 장면으로 읽힐 수 있다.
    시각적 전환: 학생 아이콘 하나에서 두 조건으로 화살표가 갈라진다.
    노트북: why_causal_inference_ko.ipynb, markdown 셀 8의 두 잠재적 결과.
    영상 참고: videos/why_causal_inference/src/why_causal_inference.py의
    Scene03_CounterfactualWorlds. 표기법 없이 분기 구도만 사용한다.
    스크립트: src/scripts/ko/02_two_worlds.txt
    청크 1 (0.000~4.920초): 같은 학생의 두 세계로 비교 대상을 고정.
    청크 2 (4.920~11.328초): 태블릿 여부만 다른 두 조건을 제시.
    """

    def construct(self):
        student = student_marker()
        branches = world_branches()
        received = world_panel(True)
        not_received = world_panel(False)

        # 청크 1: 상단 학생 한 명에서 두 화살표를 뻗는다.
        # 화면 구획은 상단 학생, 중앙의 두 비어 있는 카드다.
        # 두 카드가 서로 다른 학생을 뜻하지 않도록 인물 아이콘을 복제하지 않는다.
        self.add(student)
        self.wait(0.6)
        self.play(Create(branches), run_time=0.8)
        self.play(FadeIn(received[0]), FadeIn(not_received[0]), run_time=0.7)
        self.wait(2.82)  # 첫 청크가 끝나는 4.920초까지 두 가능성을 유지한다.

        # 청크 2: 카드 안에 태블릿 지급 여부만 채운다.
        # 학생 한 명과 두 조건 외에 결과값이나 다른 학생은 추가하지 않는다.
        self.play(
            FadeIn(VGroup(received[1], received[2])),
            FadeIn(VGroup(not_received[1], not_received[2])),
            run_time=0.8,
        )
        self.wait(2.5)
        self.play(Indicate(student, color=STUDENT_COLOR, scale_factor=1.04), run_time=0.8)
        self.wait(2.608)  # 11.628초: 음성 종료 뒤 약 0.3초의 여백.


class Scene03_Counterfactual(Scene):
    """Scene 03 — 실제로 받은 학생의 미지급 결과는 관찰할 수 없는 반사실이다.

    오해: 두 카드의 결과를 실제로 모두 볼 수 있다는 생각.
    시각적 전환: 직전 Scene의 두 카드를 그대로 이어받고 한쪽을 가린다.
    노트북: why_causal_inference_ko.ipynb, markdown 셀 8의 관찰 결과·반사실.
    영상 참고: videos/why_causal_inference/src/why_causal_inference.py의
    Scene03_CounterfactualWorlds. 같은 두 세계에서 한쪽만 남기는 구조를 사용한다.
    스크립트: src/scripts/ko/03_counterfactual.txt
    청크 1 (0.000~4.464초): 두 결과를 함께 관찰할 수 없다는 문제.
    청크 2 (4.464~13.464초): 받은 쪽만 관찰, 받지 않은 쪽은 반사실.
    """

    def construct(self):
        student = student_marker()
        branches = world_branches()
        received = world_panel(True)
        not_received = world_panel(False)

        observed_icon = tabler_icon("eye.svg", SCORE_COLOR, 0.54)
        observed_label = Text("관찰", font=FONT, font_size=28, color=SCORE_COLOR)
        observed_group = VGroup(observed_icon, observed_label).arrange(DOWN, buff=0.10)
        observed_group.move_to(LEFT * 1.06 + DOWN * 2.76)

        unseen_icon = tabler_icon("eye-off.svg", QUESTION_COLOR, 0.54)
        unseen_label = Text("반사실", font=FONT, font_size=28, color=QUESTION_COLOR)
        unseen_group = VGroup(unseen_icon, unseen_label).arrange(DOWN, buff=0.10)
        unseen_group.move_to(RIGHT * 1.06 + DOWN * 2.76)

        # 청크 1: 독립 실행 시에도 모든 요소를 만들되, 첫 프레임을
        # 직전 Scene의 마지막 화면과 같게 두어 합본 경계에서 끊기지 않게 한다.
        # 결과 점수는 표시하지 않아 두 결과를 관찰한 듯 보이지 않게 한다.
        impossible = Text("둘 다 볼 수 없다", font=FONT, font_size=28,
                          color=QUESTION_COLOR)
        impossible.move_to(DOWN * 2.78)
        self.add(student, branches, received, not_received)
        self.play(FadeIn(impossible, shift=UP * 0.08), run_time=0.6)
        self.play(Indicate(VGroup(received, not_received), color=QUESTION_COLOR,
                           scale_factor=1.02), run_time=0.8)
        self.wait(3.064)  # 첫 청크가 끝나는 4.464초까지 두 조건을 제시한다.

        # 청크 2: 실제로 태블릿을 받았다는 가정 아래 왼쪽만 관찰한다.
        # 오른쪽 카드는 흐리게 하고, 마지막에 반사실 이름을 부여한다.
        self.play(FadeOut(impossible), FadeIn(observed_group, shift=UP * 0.08),
                  run_time=0.7)
        self.play(not_received.animate.set_opacity(0.30),
                  branches[1].animate.set_opacity(0.30), run_time=0.7)
        self.wait(2.9)
        self.play(FadeIn(unseen_group, shift=UP * 0.08), run_time=0.7)
        self.wait(4.3)  # 13.764초: 음성 종료 뒤 약 0.3초의 여백.
