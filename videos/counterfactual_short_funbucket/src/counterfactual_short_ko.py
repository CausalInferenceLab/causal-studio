"""같은 학생의 두 세계: 한국어 세로형 쇼츠의 승인된 Scene만 구현한다."""

import json
import math
from pathlib import Path

from manim import (
    BLACK, WHITE, UP, Arrow, FadeIn, FadeOut, Indicate, Scene, SVGMobject, Text,
    Transform, VGroup,
    config, tempconfig,
)


TOPIC_DIR = Path(__file__).resolve().parents[1]
ICON_DIR = TOPIC_DIR.parent / "assets" / "tabler-icons" / "icons" / "outline"
FONT = "Apple SD Gothic Neo"
STUDENT_COLOR = WHITE
TABLET_COLOR = "#43C9C0"
QUESTION_COLOR = "#F8D66D"
OBSERVATION_COLOR = "#D6DBE2"

# 공용 manim.cfg를 수정하지 않고 이 영상의 Scene 생성·렌더 동안에만 적용한다.
SHORT_CONFIG = {
    "pixel_width": 360,
    "pixel_height": 640,
    "frame_width": 9.0,
    "frame_height": 16.0,
    "frame_rate": 15,
    "background_color": BLACK,
}


def load_icon(name: str, color: str, height: float) -> SVGMobject:
    """공용 Tabler 아이콘의 크기와 선 스타일을 통일한다."""
    icon = SVGMobject(str(ICON_DIR / f"{name}.svg"))
    icon.set_fill(opacity=0)
    icon.set_stroke(color=color, width=3.0, opacity=1)
    icon.height = height
    return icon


def make_student_and_tablet() -> VGroup:
    """독립 실행 시에도 같은 학생·색·위치를 재구성할 공통 시각 요소."""
    student = load_icon("user", STUDENT_COLOR, 2.3).move_to([-0.85, 1.8, 0])
    tablet = load_icon("device-tablet", TABLET_COLOR, 1.55).move_to([1.15, 1.65, 0])
    return VGroup(student, tablet)


def make_two_worlds() -> tuple[VGroup, dict, dict]:
    """학생을 복제하지 않고 한 명에서 두 조건으로 분기하는 공통 화면."""
    # 학생 아이콘은 언제나 하나만 둔다. 두 갈래는 서로 다른 학생이 아니라
    # 같은 학생에게 태블릿을 지급하거나 지급하지 않는 두 가능성이다.
    title = Text("같은 학생", font=FONT, font_size=38, color=WHITE)
    title.move_to([0, 5.15, 0])
    student = load_icon("user", STUDENT_COLOR, 1.65).move_to([0, 3.5, 0])
    header = VGroup(title, student)
    worlds = []
    for x, name, label, color in (
        (-2.0, "device-tablet", "받음", TABLET_COLOR),
        (2.0, "device-tablet-off", "안 받음", OBSERVATION_COLOR),
    ):
        branch = Arrow(
            [x * 0.12, 2.5, 0], [x, 1.25, 0], buff=0.08,
            color=color, stroke_width=3, max_tip_length_to_length_ratio=0.16,
        )
        tablet = load_icon(name, color, 1.25).move_to([x, 0.4, 0])
        condition = Text(label, font=FONT, font_size=31, color=color)
        condition.move_to([x, -0.85, 0])
        conditions = VGroup(branch, tablet, condition)
        result_arrow = Arrow(
            [x, -1.4, 0], [x, -2.0, 0], buff=0.06,
            color=OBSERVATION_COLOR, stroke_width=2.6,
        )
        school = load_icon("school", OBSERVATION_COLOR, 0.9).move_to([x, -2.75, 0])
        score = Text("성적", font=FONT, font_size=29, color=WHITE)
        score.move_to([x, -3.8, 0])
        result = VGroup(result_arrow, school, score)
        worlds.append({"condition": conditions, "result": result, "x": x})
    return header, worlds[0], worlds[1]


class CounterfactualShortScene(Scene):
    """설정을 임시 적용해 다른 토픽의 화면 비율에 영향을 주지 않는다."""

    def __init__(self, **kwargs):
        # -ql은 기존 확인본과 같은 360×640/15fps, -qh는 1080×1920/30fps.
        # 임시 설정을 인스턴스에 보관해 생성 시점과 렌더 시점의 해상도를 일치시킨다.
        self.short_config = dict(SHORT_CONFIG)
        if config.quality == "high_quality":
            self.short_config.update(pixel_width=1080, pixel_height=1920, frame_rate=30)
        with tempconfig(self.short_config):
            super().__init__(**kwargs)

    def render(self, preview=False):
        with tempconfig(self.short_config):
            return super().render(preview=preview)

    def wait_until(self, seconds: float):
        """청크의 절대 시각을 기준으로 대기해 전환 오차 누적을 줄인다."""
        remaining = seconds - float(self.time)
        if remaining > 1e-6:
            self.wait(remaining)

    def finish_after_audio(self, timing: dict):
        # 프레임 양자화의 오차를 고려해 MP3 끝 이후 최소 0.5초를 확보한다.
        target = math.ceil((float(timing["totalDuration"]) + 0.6) * config.frame_rate) / config.frame_rate
        self.wait_until(target)


class Scene01_TabletQuestion(CounterfactualShortScene):
    """
    핵심 주장: 성적 상승만으로 태블릿의 효과를 단정할 수 없다.
    예상 오해: 지급 이후 성적이 올랐으니 태블릿 덕분이라고 생각한다.
    시각적 전환: 학생·태블릿·상승 표시를 모두 지운 뒤 중앙의 질문만 강조한다.

    노트북: book/why_causal_inference/why_causal_inference_ko.ipynb
      전체 셀을 1부터 세어 셀 4의 태블릿 질문, 셀 6의 인과 해석 유보.
      학교 예시를 한 학생의 상황으로 각색하고 점수 데이터는 사용하지 않는다.
    직전 Scene: 없음. 독립 실행 시 필요한 요소를 이 Scene에서 모두 생성한다.
    첫 문장: 한 학생이 태블릿을 받은 뒤, 성적이 올랐어요.
    마지막 문장: 성적이 올랐다는 것만으로는 알 수 없어요.
    경계: 두 세계 비교와 반사실 설명 이전에 종료한다.

    스크립트: src/scripts/ko/01_tablet_question.txt (승인본 유지)
    타이밍: build/audio/01_tablet_question.timings.json
      청크 1, 0.00–4.80초: 학생·태블릿 다음에 성적 상승을 관찰로 제시.
      청크 2, 4.80–10.32초: 앞 화면 전체 제거 후 중앙 질문에 시선을 모음.
    참고: 기존 why_causal_inference.py의 Scene03_CounterfactualWorlds에서
      동일 학생과 공용 SVG를 사용하는 구조를 참고한다.
      3b1b/_2020/covid.py의 IntroQuestion은 질문을 순차 제시하고
      이전 요소를 지워 시선을 정리하는 리듬을 참고한다. 코드는 CE로 새로 작성.
    """

    WAIT_TAIL = 0.5

    def construct(self):
        timing = json.loads(
            (TOPIC_DIR / "build/audio/01_tablet_question.timings.json").read_text()
        )
        second_chunk_start = float(timing["chunks"][1]["start"])
        audio_end = float(timing["totalDuration"])

        # Beat 1a: 청크 1의 '한 학생이 태블릿을 받은 뒤'를 처리한다.
        # 제거할 이전 요소: 없음. 핵심 그룹 1개, 상중단의 학생·태블릿.
        # 하단은 비워 두고 단일 시선 대상은 학생, 다음에는 태블릿이다.
        context = make_student_and_tablet()
        self.play(FadeIn(context[0]), run_time=0.6)
        self.wait_until(0.8)
        self.play(FadeIn(context[1]), run_time=0.5)
        self.wait_until(2.6)

        # Beat 1b: 같은 청크의 '성적이 올랐어요'에 상승 표시를 붙인다.
        # 남는 요소: 상중단 맥락 1개. 새 그룹: 하중단의 성적 상승 표시.
        # 중앙 간격과 최하단은 비워 둔다. 주 시선 대상은 성적 상승 하나다.
        # 화살표는 성적의 변화만 뜻한다. 태블릿에서 성적으로 연결하지 않는다.
        school = load_icon("school", OBSERVATION_COLOR, 1.2).move_to([-0.7, -1.15, 0])
        upward = load_icon("arrow-up", OBSERVATION_COLOR, 1.0).move_to([0.85, -1.15, 0])
        rise_label = Text("성적 상승", font=FONT, font_size=36, color=WHITE)
        rise_label.move_to([0, -2.65, 0])
        observation = VGroup(school, upward, rise_label)
        self.play(
            context.animate.set_stroke(opacity=0.6), FadeIn(observation), run_time=0.6
        )
        self.wait_until(second_chunk_start)

        # Beat 2: 청크 2의 질문과 판단 유보를 같은 화면 메시지로 처리한다.
        # 먼저 학생·태블릿·성적 그룹 전체를 제거한다. 남는 이전 요소는 없다.
        # 다음 핵심 그룹은 중앙 질문 1개뿐이다. 위·아래 영역은 비워 둔다.
        # 단일 시선 대상: 아래에서 중앙으로 가볍게 들어오는 노란 질문.
        self.play(FadeOut(context), FadeOut(observation), run_time=0.3)
        question = Text(
            "태블릿 덕분일까?", font=FONT, font_size=42, color=QUESTION_COLOR
        ).move_to([0, 0, 0])
        self.play(FadeIn(question, shift=UP * 0.35), run_time=0.4)

        # 마지막 음성까지 질문을 유지한 뒤 최소 0.5초의 화면 여유를 둔다.
        # 프레임 단위로 올림하여 렌더 영상이 승인된 MP3보다 짧아지지 않게 한다.
        final_time = math.ceil((audio_end + self.WAIT_TAIL) * config.frame_rate) / config.frame_rate
        self.wait_until(final_time)


class Scene02_SameStudentWorlds(CounterfactualShortScene):
    """
    핵심 주장: 효과를 묻는 비교는 같은 학생이 같은 시험에서 겪는 두 경우다.
    예상 오해: 서로 다른 두 학생을 비교하거나 전후 성적만 비교하면 된다.
    시각적 전환: 학생 한 명에서 태블릿 받음/안 받음으로 화살표가 갈라진다.
    노트북: 전체 셀 9, '같은 학생이 태블릿을 받은 세계와 받지 않은 세계'부터
      두 잠재적 결과 정의까지. 수식과 숫자 데이터는 사용하지 않는다.
    직전 마지막 문장: 성적이 올랐다는 것만으로는 알 수 없어요.
    현재 첫 문장: 태블릿의 효과를 알려면, 같은 학생의 두 경우를 비교해야 해요.
    마지막 문장: 같은 시험에서, 태블릿을 받았을 때의 성적과 받지 않았을 때의 성적이에요.
    다음 경계: 관찰 가능성과 반사실 정의는 Scene 03에 남긴다.
    참고 코드: why_causal_inference.py의 Scene03_CounterfactualWorlds.
    참고 영상: 3b1b/_2020/covid.py의 IntroQuestion.
      이전 질문을 지우고 다음 설명에 시선을 모으는 전환 리듬을 참고한다.
    스크립트: src/scripts/ko/02_same_student_worlds.txt
    청크 대응: 1(0–5.448초)은 학생과 두 조건, 2(5.448–12.048초)는 두 결과.
    상단 학생 앵커와 두 갈래의 좌우 배치는 다음 Scene에서도 그대로 재구성한다.
    """

    def construct(self):
        timing = json.loads((TOPIC_DIR / "build/audio/02_same_student_worlds.timings.json").read_text())
        header, received, not_received = make_two_worlds()

        # Beat 1: 직전의 중앙 질문을 잠시 재현한 뒤 완전히 지운다.
        # 남는 이전 요소 없음. 단일 핵심 그룹은 상중단의 학생 한 명이다.
        # 하단은 비워 두며, 시선 대상은 '같은 학생'과 그 학생의 아이콘이다.
        previous_question = Text(
            "태블릿 덕분일까?", font=FONT, font_size=42, color=QUESTION_COLOR
        )
        self.add(previous_question)
        self.play(FadeOut(previous_question), run_time=0.35)
        self.play(FadeIn(header), run_time=0.55)
        self.wait_until(2.6)

        # Beat 2: 청크 1 후반의 '두 경우'에 맞춰 분기만 순서대로 제시한다.
        # 학생은 작은 공통 앵커로 남고 핵심 비교 그룹은 좌우 조건 2개다.
        # 결과 자리인 하단은 아직 비운다. 먼저 왼쪽, 다음 오른쪽만 읽게 한다.
        self.play(FadeIn(received["condition"]), run_time=0.5)
        self.wait_until(3.4)
        self.play(FadeIn(not_received["condition"]), run_time=0.5)
        self.wait_until(float(timing["chunks"][1]["start"]))

        # Beat 3: 청크 2의 '같은 시험' 도입을 받은 뒤 결과를 차례대로 붙인다.
        # 기존 조건 그룹에 결과를 통합하므로 핵심 비교 그룹은 여전히 좌우 2개.
        # 최하단 여백 유지. 한 번에 읽을 대상은 새로 등장하는 쪽의 성적 하나다.
        # 성적 수치나 상승·하락을 넣지 않아 태블릿의 효과 방향을 가정하지 않는다.
        self.wait_until(float(timing["chunks"][1]["start"]) + 1.0)
        self.play(FadeIn(received["result"]), run_time=0.55)
        self.wait_until(float(timing["chunks"][1]["start"]) + 3.3)
        self.play(FadeIn(not_received["result"]), run_time=0.55)
        self.finish_after_audio(timing)


class Scene03_OnlyOneOutcome(CounterfactualShortScene):
    """
    핵심 주장: 태블릿을 실제로 받았다면 받지 않았을 때의 결과가 반사실이다.
    예상 오해: 두 가능성을 그릴 수 있으니 두 성적도 실제로 관찰할 수 있다.
    시각적 전환: 오른쪽 결과를 지우고 물음표로 바꾼 뒤 '반사실'이라 이름 붙인다.
    노트북: 전체 셀 9, '두 값 모두 있을 수 있는 결과'부터
      실제 받은 쪽은 관찰하고 다른 쪽은 관찰할 수 없다는 예시 및 반사실 정의까지.
      개별 효과 수식과 평균 효과 설명에 들어가기 전에 종료한다. 숫자는 사용하지 않는다.
    직전 마지막 문장: 같은 시험에서, 태블릿을 받았을 때의 성적과 받지 않았을 때의 성적이에요.
    현재 첫 문장: 하지만 실제로는 한쪽 결과만 관찰할 수 있어요.
    마지막 문장: 이 관찰할 수 없는 결과를 반사실이라고 해요.
    스크립트: src/scripts/ko/03_only_one_outcome.txt
    타이밍: 1(0–4.608초) 한쪽 결과 관찰, 2(4.608–7.728초) 실제 지급,
      3(7.728–15.240초) 받지 않았을 결과를 반사실로 명명한다.
    이어받는 요소: Scene 02의 학생 한 명, 두 분기, 조건 및 결과의 좌표·색.
      이전 Scene 실행 여부와 무관하게 공통 함수로 같은 화면을 재구성한다.
    참고 코드: why_causal_inference.py의 Scene03_CounterfactualWorlds.
    참고 영상: 3b1b/_2020/covid.py의 IntroQuestion.
      이전 설명 요소를 지운 다음 핵심 하나를 강조하는 리듬을 차용한다.
    """

    def construct(self):
        timing = json.loads((TOPIC_DIR / "build/audio/03_only_one_outcome.timings.json").read_text())
        header, received, not_received = make_two_worlds()
        self.add(
            header, received["condition"], received["result"],
            not_received["condition"], not_received["result"],
        )

        # Beat 1: Scene 02의 마지막 구도를 이어받아 오른쪽 성적부터 제거한다.
        # 남는 요소: 작은 공통 학생 앵커와 좌우 두 비교 그룹. 새 큰 박스는 없다.
        # 하단 여백을 비워 두고, 단일 시선 대상은 사라지는 오른쪽 결과다.
        # 물음표는 성적 0이나 숨겨진 측정값이 아니라 관찰할 수 없는 결과다.
        self.wait_until(0.6)
        observed_label = Text("관찰", font=FONT, font_size=29, color=TABLET_COLOR)
        observed_label.move_to(received["result"][2])
        self.play(
            FadeOut(not_received["result"][1:]),
            Transform(received["result"][2], observed_label), run_time=0.45,
        )
        unknown = load_icon("question-mark", OBSERVATION_COLOR, 0.9)
        unknown.move_to([2.0, -2.75, 0])
        unknown_label = Text("관찰 불가", font=FONT, font_size=27, color=OBSERVATION_COLOR)
        unknown_label.move_to([2.0, -3.8, 0])
        self.play(FadeIn(VGroup(unknown, unknown_label)), run_time=0.45)
        self.wait_until(float(timing["chunks"][1]["start"]))

        # Beat 2: 청크 2의 '실제로 받았죠'는 왼쪽 지급 조건만 강조한다.
        # 오른쪽 비교 구조는 맥락으로 남긴다. 상단 문구는 지워 읽을 대상을 줄인다.
        # 학생 아이콘은 계속 하나만 남기므로 동일 대상의 두 갈래라는 구조는 유지된다.
        # 두 비교 그룹의 공간을 유지하고 주 시선은 왼쪽 태블릿 한 곳에 둔다.
        actual_label = Text("실제 받음", font=FONT, font_size=29, color=TABLET_COLOR)
        actual_label.move_to(received["condition"][2])
        self.play(
            FadeOut(header[0]),
            Transform(received["condition"][2], actual_label),
            Indicate(received["condition"][1], color=TABLET_COLOR, scale_factor=1.12),
            received["result"][1].animate.set_stroke(color=TABLET_COLOR),
            run_time=0.65,
        )
        self.wait_until(float(timing["chunks"][2]["start"]))

        # Beat 3: 청크 3은 오른쪽의 받지 않았을 결과에만 시선을 옮긴다.
        # 왼쪽은 관찰 결과의 맥락으로 남긴다. 단일 주 시선은 오른쪽 물음표다.
        # 새 큰 요소 없이 기존 물음표 색만 바꾸고, 아래 라벨을 교체한다.
        self.play(unknown.animate.set_stroke(color=QUESTION_COLOR), run_time=0.5)
        self.wait_until(float(timing["chunks"][2]["end"]) - 2.4)
        counterfactual = Text("반사실", font=FONT, font_size=34, color=QUESTION_COLOR)
        counterfactual.move_to(unknown_label)
        self.play(Transform(unknown_label, counterfactual), run_time=0.55)
        self.finish_after_audio(timing)
