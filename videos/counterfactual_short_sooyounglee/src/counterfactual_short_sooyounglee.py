import json
from pathlib import Path

from manim import *


# ─── 9:16 세로형 쇼츠 설정 ───
# 품질 플래그(-ql, -qh)가 정한 긴 변 길이를 세로로 쓰고, 가로는 9:16 비율로 맞춘다.
# 예: -ql → 480x854, -qh → 1080x1920
_long_side = max(config.pixel_width, config.pixel_height)
config.pixel_height = _long_side
config.pixel_width = int(round(_long_side * 9 / 16 / 2)) * 2
config.frame_width = 8.0
config.frame_height = 8.0 * 16 / 9
config.background_color = BLACK

TABLET_COLOR = TEAL_D
SCORE_COLOR = YELLOW_E
QUESTION_COLOR = YELLOW_E
OTHER_CAUSE_COLOR = GREY_B
ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
TOPIC_DIR = Path(__file__).resolve().parents[1]

# 쇼츠 하단 UI(제목, 채널명)가 덮는 영역을 피하기 위해 핵심 요소는 이 높이 위에만 둔다.
CAPTION_Y = 5.4


def load_icon(filename: str, color: str, height: float) -> SVGMobject:
    icon = SVGMobject(str(ASSET_DIR / filename))
    icon.set_stroke(color=color, width=3.2, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def load_audio_timings(scene_basename: str) -> tuple[list[float], float]:
    """chunk별 시작 시각과 mp3 전체 길이를 반환한다."""
    timings_path = TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json"
    payload = json.loads(timings_path.read_text())
    starts = [float(chunk["start"]) for chunk in payload["chunks"]]
    return starts, float(payload["totalDuration"])


def make_caption(text: str, color: str = WHITE) -> Text:
    caption = Text(text, font_size=60, weight=BOLD, color=color)
    caption.move_to(UP * CAPTION_Y)
    return caption


class TimedScene(Scene):
    """오디오 chunk 시작 시각에 Beat를 맞추기 위한 공통 기반 Scene."""

    def wait_until(self, t: float):
        remaining = t - self.renderer.time
        if remaining > 0.01:
            self.wait(remaining)


class Scene01_Question(TimedScene):
    """
    Scene 01: Question — 태블릿을 받은 학생의 성적이 올랐다. 태블릿 덕분일까?

    Core Claim:
    성적이 올랐다는 사실만으로는 태블릿 덕분이라고 말할 수 없다.

    Expected Misconception:
    "태블릿을 받은 뒤 성적이 올랐으니 태블릿 효과다"라고 전후 변화를 곧바로 효과로 읽는다.

    Visual Pivot:
    태블릿 → 80점을 잇는 점선 화살표(태블릿 덕분?)가 하나뿐이던 화면에,
    책·시계 같은 다른 원인 후보의 점선이 같은 80점으로 함께 들어오면서
    "이 상승만 보고는 원인을 고를 수 없다"로 바뀐다.

    Scene 경계:
    - 직전 Scene 마지막 문장: 없음 (첫 Scene)
    - 현재 Scene 첫 문장: "한 학생이 태블릿을 받았고, 몇 달 뒤 성적이 올랐습니다."
    - 현재 Scene 마지막 문장: "성적이 올랐다는 것만으로는 아직 알 수 없습니다."
    - 다음 Scene(two_worlds)의 '받지 않은 세계'는 여기서 꺼내지 않는다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 [3]: 태블릿 지급을 인과 질문으로 던지는 도입
    - 셀 [5]: 태블릿과 성적의 연관만으로 "태블릿이 학업 성취를 높인다"고 결론 낼 수 없다
      (원문은 학교 간 비교지만, 쇼츠에서는 한 학생의 전후 변화로 바꿔 서로 다른 학생 비교를 피한다)
    - 점수 70 → 80은 노트북 데이터가 아닌 가상 예시이며 화면에 '가상 예시'로 표시한다.

    Script Reference:
    src/scripts/ko/01_question.txt
    Audio: build/audio/01_question.mp3 (speed 1.1, 14.81s)

    Asset Reference:
    Tabler Icons (MIT) — user.svg, device-tablet.svg, book.svg, clock.svg

    3Blue1Brown Reference:
    3b1b/_2020/med_test.py - LearnAboutPositiveResult
    Reason:
    결과 하나(양성 판정)를 먼저 보여주고 그 결과를 곧바로 결론으로 읽고 싶게 만드는
    구조가 "성적 상승 → 태블릿 덕분?" 질문과 같아서, 결과를 먼저 보여준 뒤 질문을 얹는 리듬을 참고했다.

    Script-to-Beat Mapping (.timings.json chunk 기준):
      Beat 1 → chunk 1 "한 학생이 태블릿을 받았고, 몇 달 뒤 성적이 올랐습니다." (0.00~4.56s)
      Beat 2 → chunk 2 "그렇다면 태블릿 덕분일까요?"                       (4.56~7.34s)
      Beat 3 → chunk 3 앞 문장 "하지만 성적은 다른 이유로도 오를 수 있습니다." (7.34~약 10.9s)
      Beat 4 → chunk 3 뒤 문장 "성적이 올랐다는 것만으로는 아직 알 수 없습니다." (약 10.9~14.81s)

    화면 구획 (세로 8 x 14.2, 위에서부터):
      캡션 y≈5.4 / 학생+태블릿 y≈3.0 / 다른 원인 후보 y≈1.0 / 점수 줄 y≈-1.2 / 가상 예시 y≈-2.1
      y < -2.6 은 쇼츠 UI가 덮으므로 비워 둔다.
    """

    SCENE_BASENAME = "01_question"
    # chunk 3 안에서 두 번째 문장이 시작되는 대략적 시점 (chunk 3 길이의 약 47%)
    SECOND_SENTENCE_RATIO = 0.47
    WAIT_TAIL = 0.6

    def construct(self):
        starts, audio_end = load_audio_timings(self.SCENE_BASENAME)
        chunk3_len = audio_end - starts[2]
        beat4_start = starts[2] + chunk3_len * self.SECOND_SENTENCE_RATIO

        # ─── Beat 1: 한 학생이 태블릿을 받고, 몇 달 뒤 성적이 오른다 ───
        # 처리 문장: chunk 1 전체.
        # 남는 요소: 없음 (첫 화면)
        # 새로 등장: 학생+태블릿 그룹(상단), 점수 줄 70 → 80 + 가상 예시(중단)
        # 비워 두는 영역: 캡션 자리(최상단), 다른 원인 후보 자리(y≈1.0), 하단 UI 영역
        # 단일 핵심 시선: 앞부분은 학생에게 건네지는 태블릿, 뒷부분은 70 → 80 상승
        student = load_icon("user.svg", WHITE, 1.9)
        student.move_to(UP * 3.0)
        tablet = load_icon("device-tablet.svg", TABLET_COLOR, 1.05)
        tablet.next_to(student, RIGHT, buff=0.35).shift(DOWN * 0.35)

        score_before = Text("70", font_size=96, color=GREY_A)
        score_after = Text("80", font_size=96, weight=BOLD, color=SCORE_COLOR)
        score_row = VGroup(score_before, score_after).arrange(RIGHT, buff=2.0)
        score_row.move_to(DOWN * 1.2)
        rise_arrow = Arrow(
            score_before.get_right(),
            score_after.get_left(),
            buff=0.3,
            stroke_width=8,
            color=SCORE_COLOR,
        )
        hypothetical = Text("가상 예시", font_size=30, color=GREY_B)
        hypothetical.next_to(score_row, DOWN, buff=0.45)

        self.play(FadeIn(student, shift=UP * 0.2), run_time=0.6)
        self.play(FadeIn(tablet, shift=LEFT * 1.2), run_time=0.8)
        # "몇 달 뒤 성적이 올랐습니다"가 시작될 때까지 학생+태블릿만 보여 준다.
        self.wait_until(2.2)
        self.play(FadeIn(score_before), FadeIn(hypothetical), run_time=0.5)
        self.play(GrowArrow(rise_arrow), run_time=0.6)
        self.play(FadeIn(score_after, scale=1.3), run_time=0.5)

        # ─── Beat 2: "그렇다면 태블릿 덕분일까요?" ───
        # 처리 문장: chunk 2. 태블릿과 80점을 잇는 점선 하나로 "원인 추측"을 시각화한다.
        # 남는 요소: 학생+태블릿, 점수 줄, 가상 예시 (그대로 유지, 새 큰 요소 없음)
        # 새로 등장: 캡션 "태블릿 덕분?"(최상단), 태블릿 → 80 점선 화살표 + "?"
        # 비워 두는 영역: 다른 원인 후보 자리 왼쪽, 하단 UI 영역
        # 단일 핵심 시선: 태블릿에서 80으로 내려가는 점선
        self.wait_until(starts[1])
        tablet_link = DashedVMobject(
            Arrow(
                tablet.get_bottom(),
                score_after.get_corner(UR),
                buff=0.25,
                stroke_width=5,
                color=TABLET_COLOR,
            ),
            num_dashes=12,
        )
        link_question = Text("?", font_size=72, weight=BOLD, color=QUESTION_COLOR)
        link_question.next_to(tablet_link, RIGHT, buff=0.25)
        caption_q = make_caption("태블릿 덕분?")

        self.play(Create(tablet_link), FadeIn(caption_q, shift=DOWN * 0.2), run_time=0.9)
        self.play(FadeIn(link_question, scale=1.4), run_time=0.4)

        # ─── Beat 3: "하지만 성적은 다른 이유로도 오를 수 있습니다." ───
        # 처리 문장: chunk 3 앞 문장. 태블릿만이 아니라 다른 원인 후보도 같은 80점을 가리킨다.
        # 먼저 정리: 태블릿 전용 "?"를 지우고, 태블릿 점선을 회색으로 낮춰 특별 취급을 없앤다.
        # 남는 요소: 학생+태블릿, 점수 줄, 가상 예시, 캡션(곧 교체)
        # 새로 등장: 책·시계 아이콘(y≈1.0 왼쪽)과 각각의 회색 점선 → 80
        # 비워 두는 영역: 오른쪽 중단, 하단 UI 영역
        # 단일 핵심 시선: 80으로 모이는 여러 점선
        self.wait_until(starts[2])
        caption_other = make_caption("다른 이유일 수도", OTHER_CAUSE_COLOR)
        self.play(
            FadeOut(link_question),
            tablet_link.animate.set_color(OTHER_CAUSE_COLOR),
            FadeOut(caption_q),
            run_time=0.5,
        )

        book = load_icon("book.svg", OTHER_CAUSE_COLOR, 0.85)
        clock = load_icon("clock.svg", OTHER_CAUSE_COLOR, 0.85)
        other_causes = VGroup(book, clock).arrange(RIGHT, buff=1.1)
        other_causes.move_to(LEFT * 2.0 + UP * 1.0)
        # 점선 끝점을 80 윗변에 나눠 두어 화살촉끼리 겹치지 않게 한다 (태블릿 점선은 오른쪽 끝).
        landing_points = [
            score_after.get_corner(UL) + RIGHT * 0.05,
            score_after.get_top() + LEFT * 0.05,
        ]
        other_links = VGroup(*(
            DashedVMobject(
                Arrow(
                    cause.get_bottom(),
                    landing,
                    buff=0.2,
                    stroke_width=4,
                    color=OTHER_CAUSE_COLOR,
                ),
                num_dashes=10,
            )
            for cause, landing in zip(other_causes, landing_points)
        ))

        self.play(FadeIn(caption_other, shift=DOWN * 0.2), run_time=0.4)
        self.play(LaggedStartMap(FadeIn, other_causes, lag_ratio=0.4), run_time=0.8)
        self.play(LaggedStartMap(Create, other_links, lag_ratio=0.3), run_time=0.9)

        # ─── Beat 4: "성적이 올랐다는 것만으로는 아직 알 수 없습니다." ───
        # 처리 문장: chunk 3 뒤 문장. 결론 대신 열린 질문으로 Scene을 닫는다.
        # 먼저 정리: "다른 이유일 수도" 캡션을 결론 캡션으로 교체한다.
        # 남는 요소: 학생+태블릿, 다른 원인 후보, 점선들, 점수 줄, 가상 예시
        # 새로 등장: 캡션 "아직 알 수 없음", 80 주변 강조 원
        # 비워 두는 영역: 하단 UI 영역
        # 단일 핵심 시선: 최상단 캡션 "아직 알 수 없음"
        self.wait_until(beat4_start)
        caption_unknown = make_caption("아직 알 수 없음", QUESTION_COLOR)
        self.play(FadeOut(caption_other), FadeIn(caption_unknown, shift=DOWN * 0.2), run_time=0.6)
        self.play(Circumscribe(score_after, shape=Circle, color=QUESTION_COLOR), run_time=1.0)

        self.wait_until(audio_end)
        self.wait(self.WAIT_TAIL)
