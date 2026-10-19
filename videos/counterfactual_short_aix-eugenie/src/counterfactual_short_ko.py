"""
같은 학생의 두 세계 — 태블릿의 효과는 어떻게 알까? (한국어 세로형 쇼츠)

9:16 세로 화면, 검정 배경, 35~45초 분량.
아래의 세로 화면 설정은 이 모듈을 렌더할 때만 적용되며 다른 영상에는 영향이 없다.

렌더 예:
    cd videos/counterfactual_short_aix-eugenie
    ../../.venv/bin/manim -ql --media_dir build/manim src/counterfactual_short_ko.py Scene01_TabletQuestion
"""

import json
import math
from pathlib import Path

from manim import *


# ─── 9:16 세로 화면 설정 (이 영상 전용) ───
# 품질 플래그(-ql/-qh)가 정한 해상도의 짧은 변을 가로, 긴 변을 세로로 돌린다.
# -ql → 480x854, -qh → 1080x1920. 좌표계는 폭 8, 높이 약 14.22 (x: ±4, y: ±7.11).
_short_side, _long_side = sorted((config.pixel_width, config.pixel_height))
config.pixel_width = _short_side
config.pixel_height = _long_side
config.frame_width = 8.0
config.frame_height = 8.0 * 16 / 9
config.background_color = BLACK


TOPIC_DIR = Path(__file__).resolve().parents[1]
ICON_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
FONT = "Apple SD Gothic Neo"

# ─── 색 의미 (모든 Scene 공통) ───
STUDENT_COLOR = WHITE        # 같은 학생 한 명 (항상 같은 아이콘·같은 색)
TABLET_COLOR = TEAL_C        # 태블릿(처치)과 태블릿에서 나온 관계
SCORE_COLOR = YELLOW_D       # 성적(결과)
QUESTION_COLOR = MAROON_B    # 아직 답할 수 없는 질문
OTHER_CAUSE_COLOR = GREY_C   # 태블릿 말고 성적을 바꿀 수 있는 다른 이유
GUIDE_COLOR = GREY_B         # 보조선, 보조 라벨

# ─── 화면 구획 (모든 Scene 공통, y 좌표) ───
HEADLINE_Y = 5.4             # 상단: 짧은 핵심 문구 한 줄
STUDENT_Y = 2.6              # 중상단: 학생과 태블릿
SCORE_BASE_Y = -4.3          # 하단: 성적 막대의 바닥선
SCORE_LOW = 1.2              # 오르기 전 성적 막대 높이 (숫자 없이 높이로만 표현)
SCORE_HIGH = 2.8             # 오른 뒤 성적 막대 높이
HEADLINE_MAX_WIDTH = 6.8     # 좌우 여백 0.6씩 확보


def load_icon(filename: str, color, height: float, stroke_width: float = 2.6) -> SVGMobject:
    """공용 Tabler Icons(outline)의 SVG를 선 아이콘으로 불러온다."""
    icon = SVGMobject(str(ICON_DIR / filename))
    icon.set_stroke(color=color, width=stroke_width, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def make_student(height: float = 1.9) -> SVGMobject:
    return load_icon("user.svg", STUDENT_COLOR, height)


def make_tablet(height: float = 1.1) -> SVGMobject:
    return load_icon("device-tablet.svg", TABLET_COLOR, height)


def make_headline(text: str, color=WHITE) -> Text:
    headline = Text(text, font=FONT, font_size=46, color=color, weight=BOLD)
    if headline.width > HEADLINE_MAX_WIDTH:
        headline.scale_to_fit_width(HEADLINE_MAX_WIDTH)
    return headline.move_to(UP * HEADLINE_Y)


def make_score_bar(height: float, x: float = 0.0, width: float = 1.3) -> Rectangle:
    """바닥선에 붙은 성적 막대. 높이만 바꿔 Transform하면 위로 자라는 것처럼 보인다."""
    bar = Rectangle(
        width=width,
        height=height,
        stroke_width=0,
        fill_color=SCORE_COLOR,
        fill_opacity=0.9,
    )
    return bar.move_to([x, SCORE_BASE_Y + height / 2, 0])


# ─── 두 세계 화면 (Scene 02~03 공통) ───
# 세로 화면을 좌/우 두 칸으로 나눠, 같은 바닥선 위에서 두 세계의 성적 막대 높이를 바로 비교한다.
# 왼쪽 = 태블릿을 받은 세계, 오른쪽 = 받지 않은 세계. 두 칸의 학생은 같은 아이콘·같은 색이다.
WORLD_X = 1.85                # 각 세계 칸의 중심 x (±)
WORLD_STUDENT_Y = 2.4         # 각 세계의 학생 아이콘 y
WORLD_STUDENT_HEIGHT = 1.5
WORLD_TABLET_HEIGHT = 0.95
WORLD_STATUS_Y = 1.15         # "받음" / "안 받음" 라벨 y
WORLD_TAG_Y = -0.6            # Scene 03의 "관찰" / "반사실" 태그 y
WORLD_BAR_WIDTH = 1.1
WORLD_SCORE_WITH = SCORE_HIGH  # 받은 세계의 성적 (숫자 없이 높이만)
WORLD_SCORE_WITHOUT = 2.0      # 받지 않은 세계의 성적 (숫자 없이 높이만)
NO_TABLET_COLOR = GREY_B       # 태블릿을 받지 않은 상태


def build_two_worlds() -> dict:
    """Scene 02 마지막 화면(두 세계 + 효과 표시)을 구성하는 Mobject들을 만든다.

    Scene 02는 이 요소들을 순서대로 등장시키고,
    Scene 03은 같은 요소를 처음부터 화면에 올려 Scene 02의 끝 화면에서 이어 시작한다.
    """
    left_x, right_x = -WORLD_X, WORLD_X

    left_student = make_student(WORLD_STUDENT_HEIGHT).move_to([left_x - 0.5, WORLD_STUDENT_Y, 0])
    right_student = make_student(WORLD_STUDENT_HEIGHT).move_to([right_x - 0.5, WORLD_STUDENT_Y, 0])
    tablet = make_tablet(WORLD_TABLET_HEIGHT).move_to([left_x + 0.65, WORLD_STUDENT_Y - 0.15, 0])
    no_tablet = load_icon("device-tablet-off.svg", NO_TABLET_COLOR, WORLD_TABLET_HEIGHT)
    no_tablet.move_to([right_x + 0.65, WORLD_STUDENT_Y - 0.15, 0])

    status_on = Text("받음", font=FONT, font_size=32, color=TABLET_COLOR).move_to([left_x, WORLD_STATUS_Y, 0])
    status_off = Text("안 받음", font=FONT, font_size=32, color=NO_TABLET_COLOR).move_to([right_x, WORLD_STATUS_Y, 0])

    # 위쪽(학생 영역)만 나누는 세로 구분선. 아래쪽 막대 영역은 비교선이 지나가야 해서 비워 둔다.
    divider = DashedLine([0, 3.6, 0], [0, 0.5, 0], color=GREY_D, stroke_width=3, dash_length=0.15)

    def world_bar_parts(x: float, height: float) -> tuple:
        bar = make_score_bar(height, x=x, width=WORLD_BAR_WIDTH)
        base = Line([x - 0.85, SCORE_BASE_Y, 0], [x + 0.85, SCORE_BASE_Y, 0], color=GUIDE_COLOR, stroke_width=3)
        label = Text("성적", font=FONT, font_size=30, color=GUIDE_COLOR).move_to([x, SCORE_BASE_Y - 0.45, 0])
        return bar, base, label

    left_bar, left_base, left_label = world_bar_parts(left_x, WORLD_SCORE_WITH)
    right_bar, right_base, right_label = world_bar_parts(right_x, WORLD_SCORE_WITHOUT)

    # 효과 표시: 받지 않은 세계의 성적 높이를 받은 세계 막대까지 점선으로 끌고 와,
    # 두 높이의 차이를 양방향 화살표와 "효과" 라벨로 묶는다.
    without_top = SCORE_BASE_Y + WORLD_SCORE_WITHOUT
    with_top = SCORE_BASE_Y + WORLD_SCORE_WITH
    level_line = DashedLine(
        [right_x - WORLD_BAR_WIDTH / 2, without_top, 0],
        [left_x - WORLD_BAR_WIDTH / 2, without_top, 0],
        color=GUIDE_COLOR,
        stroke_width=3,
        dash_length=0.12,
    )
    gap_arrow = DoubleArrow(
        [left_x + 0.8, without_top, 0],
        [left_x + 0.8, with_top, 0],
        buff=0,
        color=TABLET_COLOR,
        stroke_width=5,
        tip_length=0.2,
        max_tip_length_to_length_ratio=0.3,
    )
    effect_label = Text("효과", font=FONT, font_size=36, color=TABLET_COLOR, weight=BOLD)
    effect_label.next_to(gap_arrow, RIGHT, buff=0.2)

    return {
        "left_student": left_student,
        "right_student": right_student,
        "tablet": tablet,
        "no_tablet": no_tablet,
        "status_on": status_on,
        "status_off": status_off,
        "divider": divider,
        "left_bar": left_bar,
        "left_base": left_base,
        "left_label": left_label,
        "right_bar": right_bar,
        "right_base": right_base,
        "right_label": right_label,
        "effect": VGroup(level_line, gap_arrow, effect_label),
    }


def load_chunk_durations(scene_basename: str, fallback: list[float]) -> list[float]:
    """build/audio/{scene}.timings.json의 청크 길이를 읽는다.

    오디오가 없는 환경에서도 Scene을 단독 렌더할 수 있도록,
    파일이 없거나 청크 수가 다르면 승인 당시 측정값(fallback)을 쓴다.
    """
    timings_path = TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json"
    if not timings_path.exists():
        return list(fallback)
    payload = json.loads(timings_path.read_text())
    durations = [float(chunk["duration"]) for chunk in payload.get("chunks", [])]
    return durations if len(durations) == len(fallback) else list(fallback)


class ShortScene(Scene):
    """청크 시작 시각에 맞춰 Beat를 시작하도록 돕는 공통 베이스."""

    def wait_until(self, timestamp: float) -> None:
        # wait 길이를 프레임 단위로 올림해 둔다. 소수 프레임은 렌더 시 버려져
        # 실제 영상이 self.time보다 조금씩 짧아지고, 오디오와 싱크가 밀리기 때문이다.
        frames = math.ceil((timestamp - self.time) * config.frame_rate - 1e-6)
        if frames > 0:
            self.wait(frames / config.frame_rate)


class Scene01_TabletQuestion(ShortScene):
    """
    Scene 01: 태블릿 덕분일까? (tablet_question)

    핵심 주장:
    성적이 올랐다는 사실만으로는 태블릿 덕분이라고 말할 수 없다.

    예상되는 오해:
    "태블릿을 받은 뒤 성적이 올랐으니 태블릿 효과다"라고 곧바로 결론 내린다.

    Visual Pivot:
    태블릿 → 성적 관계를 실선이 아닌 점선 + 물음표로 보여 주고,
    마지막에 출처 없는 회색 화살표(다른 이유)가 같은 성적 막대로 들어오면서
    "태블릿만이 원인"이라는 그림이 흔들린다.

    Scene 경계:
    - 직전 Scene 마지막 문장: 없음 (첫 Scene)
    - 현재 Scene 첫 문장: "태블릿을 받은 뒤, 한 학생의 성적이 올랐습니다."
    - 다음 Scene(두 세계 비교)의 "태블릿을 받지 않은 세계", "반사실"은 여기서 꺼내지 않는다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 3: 태블릿 지급을 인과 질문으로 던지는 도입
    - 셀 5: 성적이 높다는 것만으로 태블릿 효과라고 결론 내릴 수 없다는 논리
      (노트북은 학교 간 비교지만, 여기서는 학생 한 명의 성적 상승으로 바꿔 다른 학생과 비교하지 않는다)

    Script Reference:
    src/scripts/ko/01_tablet_question.txt
    build/audio/01_tablet_question.timings.json (청크 3개: 4.75s / 1.97s / 3.36s, 합 10.08s)

    Asset Reference:
    Tabler Icons (MIT) - user.svg, device-tablet.svg
    (물음표는 help-circle.svg 내부 점이 480p에서 사라져 굵은 글자로 대체)

    3Blue1Brown Reference:
    3b1b/_2020/covid.py - IntroQuestion
    Reason: 질문 하나를 옆에서 밀어 넣듯 등장시키고 잠시 머무르는 인트로 리듬이
    "태블릿 덕분일까?" 한 문장으로 여는 이 Scene과 같아서 참고했다. (코드는 CE로 새로 작성)

    Script-to-Beat Mapping:
    Beat 1 ← 청크 1 "태블릿을 받은 뒤, 한 학생의 성적이 올랐습니다." (0.00~4.75s)
             학생 등장 → 태블릿이 학생 옆으로 → 성적 막대가 이전 높이(점선)보다 위로 자람
    Beat 2 ← 청크 2 "태블릿 덕분일까요?" (4.75~6.72s)
             태블릿 → 성적 점선 화살표 + 물음표, 상단 문구 "태블릿 덕분일까?"
    Beat 3 ← 청크 3 "성적은 다른 이유로도 오를 수 있으니까요." (6.72~10.08s)
             상승 화살표 정리 → 회색 화살표 2개가 성적으로 들어옴, 상단 문구 "아직 알 수 없다"
    """

    SCENE_BASENAME = "01_tablet_question"
    FALLBACK_DURATIONS = [4.75, 1.97, 3.36]
    WAIT_TAIL = 1.0  # mp3(10.08s)보다 화면이 약 1초 늦게 끝나도록 남기는 여백

    def construct(self):
        durations = load_chunk_durations(self.SCENE_BASENAME, self.FALLBACK_DURATIONS)
        beat_starts = [sum(durations[:i]) for i in range(len(durations))]
        audio_end = sum(durations)

        # ─── Beat 1: 학생 한 명이 태블릿을 받고, 성적이 오른다 ───
        # 청크 1 "태블릿을 받은 뒤, 한 학생의 성적이 올랐습니다."
        # 남는 요소: 없음 (첫 화면)
        # 새로 등장: 학생+태블릿 그룹(중상단), 성적 막대+라벨(하단)
        # 비워 두는 영역: 상단 문구 줄, 학생과 막대 사이 (Beat 2의 화살표 자리)
        # 단일 시선 대상: 앞 절반은 학생+태블릿, 뒤 절반은 자라는 성적 막대
        student = make_student().move_to([-0.75, STUDENT_Y, 0])
        tablet = make_tablet().move_to([0.95, STUDENT_Y - 0.2, 0])

        score_bar = make_score_bar(SCORE_LOW)
        score_label = Text("성적", font=FONT, font_size=34, color=GUIDE_COLOR)
        score_label.move_to([0, SCORE_BASE_Y - 0.5, 0])
        baseline = Line([-1.2, SCORE_BASE_Y, 0], [1.2, SCORE_BASE_Y, 0], color=GUIDE_COLOR, stroke_width=3)
        # 오르기 전 높이를 점선으로 남겨, 숫자 없이도 "올랐다"가 읽히게 한다.
        before_level = DashedLine(
            [-0.95, SCORE_BASE_Y + SCORE_LOW, 0],
            [0.95, SCORE_BASE_Y + SCORE_LOW, 0],
            color=GUIDE_COLOR,
            stroke_width=3,
            dash_length=0.12,
        )
        rise_arrow = Arrow(
            [1.35, SCORE_BASE_Y + SCORE_LOW, 0],
            [1.35, SCORE_BASE_Y + SCORE_HIGH, 0],
            buff=0,
            color=SCORE_COLOR,
            stroke_width=7,
            max_tip_length_to_length_ratio=0.3,
        )

        # "태블릿을 받은 뒤": 학생이 먼저 서 있고, 태블릿이 오른쪽에서 들어와 학생 옆에 붙는다.
        self.play(FadeIn(student, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(tablet, shift=LEFT * 2.5), run_time=0.8)
        # "한 학생의 성적이": 하단에 성적 막대를 오르기 전 높이로 먼저 둔다.
        self.wait_until(beat_starts[0] + 1.9)
        self.play(
            Create(baseline),
            FadeIn(score_bar),
            FadeIn(score_label),
            run_time=0.6,
        )
        self.add(before_level)
        # "올랐습니다": 막대가 점선 위로 자라고, 오른쪽에 상승 화살표가 함께 뻗는다.
        self.wait_until(beat_starts[0] + 3.4)
        self.play(
            Transform(score_bar, make_score_bar(SCORE_HIGH)),
            GrowArrow(rise_arrow),
            run_time=0.9,
        )

        # ─── Beat 2: 그 상승이 태블릿 덕분인지 묻는다 ───
        # 청크 2 "태블릿 덕분일까요?"
        # 남는 요소: 학생+태블릿(중상단), 성적 막대·점선·상승 화살표(하단)
        # 새로 등장: 태블릿 → 성적 점선 화살표 + 물음표(중앙), 상단 문구
        # 비워 두는 영역: 화면 좌우 가장자리 (Beat 3의 회색 화살표 자리)
        # 단일 시선 대상: 태블릿과 성적을 잇는 점선 화살표 위의 물음표
        self.wait_until(beat_starts[1])
        link_start = tablet.get_bottom() + DOWN * 0.15
        link_end = score_bar.get_top() + UP * 0.2
        link = DashedLine(link_start, link_end, color=TABLET_COLOR, stroke_width=5, dash_length=0.18)
        link.add_tip(tip_length=0.3, tip_width=0.3)
        # 물음표는 아이콘(help-circle)의 내부 점이 저해상도에서 사라져 글자로 크게 쓴다.
        question_mark = Text("?", font=FONT, font_size=110, weight=BOLD, color=QUESTION_COLOR)
        question_mark.move_to(midpoint(link_start, link_end) + RIGHT * 1.0)
        headline = make_headline("태블릿 덕분일까?")

        self.play(
            Create(link),
            FadeIn(headline, shift=RIGHT * 0.4),
            run_time=0.8,
        )
        self.play(FadeIn(question_mark, scale=0.6), run_time=0.4)

        # ─── Beat 3: 성적은 다른 이유로도 오를 수 있다 ───
        # 청크 3 "성적은 다른 이유로도 오를 수 있으니까요."
        # 먼저 지울 요소: 상승 화살표 (오른쪽 회색 화살표와 자리가 겹치고, "올랐다"는 점선이 계속 보여 준다)
        # 남는 요소: 학생+태블릿, 점선 화살표+물음표, 성적 막대·점선
        # 새로 등장: 좌우 가장자리에서 성적 막대로 들어오는 회색 화살표 2개, 상단 문구 교체
        # 비워 두는 영역: 학생 주변 (다른 학생이나 다른 원인 라벨을 두지 않는다)
        # 단일 시선 대상: 성적 막대로 모이는 회색 화살표 (태블릿 말고도 들어오는 길)
        self.wait_until(beat_starts[2])
        other_causes = VGroup(
            Arrow(
                [-3.0, -0.9, 0],
                [-0.8, SCORE_BASE_Y + 2.0, 0],
                buff=0,
                color=OTHER_CAUSE_COLOR,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.12,
            ),
            Arrow(
                [3.0, -0.9, 0],
                [0.8, SCORE_BASE_Y + 2.0, 0],
                buff=0,
                color=OTHER_CAUSE_COLOR,
                stroke_width=6,
                max_tip_length_to_length_ratio=0.12,
            ),
        )
        other_causes.set_opacity(0.75)
        unknown_headline = make_headline("아직 알 수 없다", color=QUESTION_COLOR)

        self.play(FadeOut(rise_arrow), run_time=0.4)
        self.play(
            LaggedStart(*[GrowArrow(arrow) for arrow in other_causes], lag_ratio=0.35),
            run_time=1.2,
        )
        # 글자 모양이 다른 두 문구를 Transform으로 섞으면 중간 프레임이 뭉개져, 위로 밀어 교체한다.
        self.play(
            FadeOut(headline, shift=UP * 0.3),
            FadeIn(unknown_headline, shift=UP * 0.3),
            run_time=0.7,
        )

        # 마지막 문장이 끝난 뒤에도 화면이 잠시 머물도록 mp3 끝 + WAIT_TAIL까지 유지한다.
        self.wait_until(audio_end + self.WAIT_TAIL)


class Scene02_TwoWorlds(ShortScene):
    """
    Scene 02: 같은 학생, 두 세계 (two_worlds)

    핵심 주장:
    태블릿의 효과는 같은 학생이 태블릿을 받은 세계와 받지 않은 세계의 성적 차이다.

    예상되는 오해:
    태블릿을 받은 학생과 받지 않은 "다른" 학생을 비교하면 효과를 알 수 있다고 생각한다.
    → 이 Scene에는 다른 학생이 등장하지 않는다. 한 학생이 두 칸으로 복제될 뿐이다.

    Visual Pivot:
    Scene 01에서 혼자 서 있던 학생 한 명이 좌/우 두 세계로 갈라지고,
    같은 바닥선 위 두 막대의 높이 차이가 곧 "효과"로 묶인다.

    Scene 경계:
    - 직전 Scene 마지막 문장: "성적은 다른 이유로도 오를 수 있으니까요."
    - 현재 Scene 첫 문장: "같은 학생에게 두 세계가 있다고 상상해 봅시다."
    - 다음 Scene의 "현실에서는 한 세계만 볼 수 있다", "반사실"은 여기서 꺼내지 않는다.

    직전 Scene에서 이어받는 시각 요소:
    흰색 학생 아이콘, 청록 태블릿, 노란 성적 막대와 회색 바닥선, 상단 한 줄 문구 위치.
    첫 화면은 Scene 01과 같은 크기·위치의 학생 한 명에서 시작한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 8: "같은 학생이 태블릿을 받은 세계와 받지 않은 세계"와 두 잠재적 결과 (Y1, Y0)
    - 셀 9~10: 멀티버스로 두 결과를 모두 볼 수 있다는 가정과 개별 효과(Y1 - Y0)
      (수식과 표의 점수는 쓰지 않고, 막대 높이 차이로만 표현한다)

    Script Reference:
    src/scripts/ko/02_two_worlds.txt
    build/audio/02_two_worlds.timings.json (청크 3개: 4.85s / 6.31s / 4.25s, 합 15.41s)

    Asset Reference:
    Tabler Icons (MIT) - user.svg, device-tablet.svg, device-tablet-off.svg

    3Blue1Brown Reference:
    3b1b/_2018/uncertainty.py
    Reason: 동시에 볼 수 없는 두 가능 상태를 나란히 두고 대비시키는 구성이
    한 학생의 두 세계를 좌/우로 나누는 이 Scene과 같아서 참고했다. (코드는 CE로 새로 작성)

    Script-to-Beat Mapping:
    Beat 1 ← 청크 1 "같은 학생에게 두 세계가 있다고 상상해 봅시다." (0.00~4.85s)
             학생 한 명 → 같은 아이콘 두 개로 갈라짐, 상단 문구 "같은 학생, 두 세계"
    Beat 2 ← 청크 2 "한 세계에선 태블릿을 받고, 다른 세계에선 받지 않습니다." (4.85~11.16s)
             왼쪽에 태블릿 + "받음", 오른쪽에 태블릿 꺼짐 + "안 받음"
    Beat 3 ← 청크 3 "두 세계의 성적 차이가 태블릿의 효과입니다." (11.16~15.41s)
             두 막대가 같은 바닥선에서 자라고, 높이 차이에 "효과" 표시
    """

    SCENE_BASENAME = "02_two_worlds"
    FALLBACK_DURATIONS = [4.85, 6.31, 4.25]
    WAIT_TAIL = 0.8  # mp3(15.41s) 뒤 여백. 전체 영상 45초 예산 안에서 최소 0.5초 이상 확보

    def construct(self):
        durations = load_chunk_durations(self.SCENE_BASENAME, self.FALLBACK_DURATIONS)
        beat_starts = [sum(durations[:i]) for i in range(len(durations))]
        audio_end = sum(durations)
        w = build_two_worlds()

        # ─── Beat 1: 같은 학생 한 명이 두 세계로 갈라진다 ───
        # 청크 1 "같은 학생에게 두 세계가 있다고 상상해 봅시다."
        # 남는 요소: 없음 (Scene 01의 학생 크기·위치로 다시 시작)
        # 새로 등장: 상단 문구, 학생 1명 → 좌/우 학생 2개, 위쪽 구분선
        # 비워 두는 영역: 하단 성적 영역 전체 (Beat 3에서 사용)
        # 단일 시선 대상: 갈라지는 학생 아이콘
        student = make_student().move_to([0, STUDENT_Y, 0])
        headline = make_headline("같은 학생, 두 세계")

        # "같은 학생에게": Scene 01과 같은 학생이 가운데에 선다.
        self.play(FadeIn(student, shift=UP * 0.3), FadeIn(headline, shift=RIGHT * 0.4), run_time=0.7)
        # "두 세계가 있다고 상상해 봅시다": 같은 학생이 그대로 복제되어 좌/우로 나뉜다.
        self.wait_until(beat_starts[0] + 1.6)
        self.play(
            ReplacementTransform(student, w["left_student"]),
            TransformFromCopy(student, w["right_student"]),
            run_time=1.2,
        )
        self.play(Create(w["divider"]), run_time=0.6)

        # ─── Beat 2: 한 세계에서만 태블릿을 받는다 ───
        # 청크 2 "한 세계에선 태블릿을 받고, 다른 세계에선 받지 않습니다."
        # 남는 요소: 상단 문구, 좌/우 학생, 구분선
        # 새로 등장: 왼쪽 태블릿 + "받음" → 오른쪽 태블릿 꺼짐 + "안 받음" (한 번에 한 쪽씩)
        # 비워 두는 영역: 하단 성적 영역
        # 단일 시선 대상: 앞 절반은 왼쪽 태블릿, 뒤 절반은 오른쪽 태블릿 꺼짐
        self.wait_until(beat_starts[1] + 0.1)
        # "한 세계에선 태블릿을 받고"
        self.play(FadeIn(w["tablet"], shift=LEFT * 1.5), run_time=0.8)
        self.play(FadeIn(w["status_on"], shift=UP * 0.2), run_time=0.5)
        # "다른 세계에선 받지 않습니다"
        self.wait_until(beat_starts[1] + 3.4)
        self.play(FadeIn(w["no_tablet"], shift=LEFT * 1.5), run_time=0.8)
        self.play(FadeIn(w["status_off"], shift=UP * 0.2), run_time=0.5)

        # ─── Beat 3: 두 세계의 성적 차이 = 태블릿의 효과 ───
        # 청크 3 "두 세계의 성적 차이가 태블릿의 효과입니다."
        # 남는 요소: 상단 문구, 두 세계의 학생·태블릿·라벨 (중상단)
        # 새로 등장: 같은 바닥선 위 두 성적 막대(하단) → 높이 차이 표시 + "효과"
        # 비워 두는 영역: 막대 사이 가운데 (비교 점선과 "효과" 라벨 자리)
        # 단일 시선 대상: 앞 절반은 두 막대의 높이, 뒤 절반은 "효과" 화살표
        self.wait_until(beat_starts[2] + 0.1)
        # "두 세계의 성적 차이가": 두 막대가 동시에 같은 바닥선에서 자란다.
        self.play(
            Create(w["left_base"]),
            Create(w["right_base"]),
            FadeIn(w["left_label"]),
            FadeIn(w["right_label"]),
            run_time=0.4,
        )
        self.play(
            GrowFromEdge(w["left_bar"], DOWN),
            GrowFromEdge(w["right_bar"], DOWN),
            run_time=1.1,
        )
        # "태블릿의 효과입니다": 받지 않은 세계의 높이를 왼쪽으로 끌고 와 차이를 묶는다.
        self.wait_until(beat_starts[2] + 2.5)
        level_line, gap_arrow, effect_label = w["effect"]
        self.play(Create(level_line), run_time=0.5)
        self.play(GrowFromCenter(gap_arrow), FadeIn(effect_label, shift=LEFT * 0.2), run_time=0.6)

        self.wait_until(audio_end + self.WAIT_TAIL)


class Scene03_OneWorldObserved(ShortScene):
    """
    Scene 03: 현실은 한 세계뿐 (one_world_observed)

    핵심 주장:
    현실에서는 한 세계의 결과만 관찰된다. 실제로 태블릿을 받았다면,
    받지 않았을 때의 성적은 관찰할 수 없는 반사실이다.

    예상되는 오해:
    Scene 02의 두 막대를 현실에서도 모두 볼 수 있다고 생각한다.

    Visual Pivot:
    Scene 02 끝 화면(두 세계 + 효과)에서 효과 표시가 사라지고 두 세계가 함께 어두워진 뒤,
    실제로 일어난 왼쪽 세계만 다시 밝아진다. 오른쪽 막대는 점선 윤곽과 물음표로 바뀐다.

    Scene 경계:
    - 직전 Scene 마지막 문장: "두 세계의 성적 차이가 태블릿의 효과입니다."
    - 현재 Scene 첫 문장: "하지만 현실에서는 한 세계만 볼 수 있습니다."
    - 영상의 마지막 Scene이다. 추정 방법(무작위 실험 등)은 꺼내지 않는다.

    직전 Scene에서 이어받는 시각 요소:
    Scene 02의 마지막 화면 전체(build_two_worlds)를 그대로 올린 상태에서 시작한다.
    단독 렌더해도 같은 화면에서 시작하도록 첫 프레임에 직접 구성한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 8: "실제로 관찰할 수 있는 것은 둘 중 하나뿐", 사실(Factual) / 반사실(Counterfactual)
    - 셀 13: 받은 쪽의 Y0이 관찰되지 않는 표 (화면에서는 "관찰 불가" 의미를 점선 윤곽 + 물음표로 유지)

    Script Reference:
    src/scripts/ko/03_one_world_observed.txt
    build/audio/03_one_world_observed.timings.json (청크 3개: 4.80s / 4.42s / 5.57s, 합 14.78s)

    Asset Reference:
    Tabler Icons (MIT) - user.svg, device-tablet.svg, device-tablet-off.svg, eye.svg, eye-off.svg

    3Blue1Brown Reference:
    3b1b/_2018/uncertainty.py
    Reason: Scene 02와 같은 두 상태 대비 구성을 유지한 채, 한쪽만 남기는 전환으로 마무리하기 위해 참고했다.

    Script-to-Beat Mapping:
    Beat 1 ← 청크 1 "하지만 현실에서는 한 세계만 볼 수 있습니다." (0.00~4.80s)
             효과 표시 정리 → 두 세계가 함께 어두워짐, 상단 문구 "현실은 한 세계뿐"
    Beat 2 ← 청크 2 "이 학생은 실제로 태블릿을 받았습니다." (4.80~9.22s)
             왼쪽(받은 세계)만 다시 밝아지고 눈 아이콘 + "관찰"
    Beat 3 ← 청크 3 "그래서 받지 않았을 때의 성적은 볼 수 없는 반사실입니다." (9.22~14.78s)
             오른쪽 막대 → 점선 윤곽 + 물음표, 눈 가림 아이콘 + "반사실"
    """

    SCENE_BASENAME = "03_one_world_observed"
    FALLBACK_DURATIONS = [4.80, 4.42, 5.57]
    WAIT_TAIL = 0.8  # mp3(14.78s) 뒤 여백. 마지막 화면이 잠시 머물도록 최소 0.5초 이상 확보

    def construct(self):
        durations = load_chunk_durations(self.SCENE_BASENAME, self.FALLBACK_DURATIONS)
        beat_starts = [sum(durations[:i]) for i in range(len(durations))]
        audio_end = sum(durations)
        w = build_two_worlds()

        # ─── 시작 화면: Scene 02의 마지막 화면 ───
        headline = make_headline("같은 학생, 두 세계")
        left_world = VGroup(
            w["left_student"], w["tablet"], w["status_on"], w["left_bar"], w["left_base"], w["left_label"]
        )
        right_world = VGroup(
            w["right_student"], w["no_tablet"], w["status_off"], w["right_bar"], w["right_base"], w["right_label"]
        )
        self.add(headline, w["divider"], left_world, right_world, w["effect"])
        left_bright = left_world.copy()

        # ─── Beat 1: 현실에서는 한 세계만 볼 수 있다 ───
        # 청크 1 "하지만 현실에서는 한 세계만 볼 수 있습니다."
        # 먼저 지울 요소: 효과 표시(점선·화살표·"효과") — 두 막대를 모두 볼 수 있을 때만 그릴 수 있다
        # 남는 요소: 두 세계 (함께 어둡게), 구분선
        # 새로 등장: 상단 문구 교체 "현실은 한 세계뿐"
        # 비워 두는 영역: 막대 위 태그 줄 (Beat 2~3에서 사용)
        # 단일 시선 대상: 상단 문구
        self.wait_until(beat_starts[0] + 0.3)
        new_headline = make_headline("현실은 한 세계뿐")
        self.play(FadeOut(w["effect"]), run_time=0.5)
        self.play(
            FadeOut(headline, shift=UP * 0.3),
            FadeIn(new_headline, shift=UP * 0.3),
            left_world.animate.fade(0.7),
            right_world.animate.fade(0.7),
            run_time=0.9,
        )

        # ─── Beat 2: 실제로 태블릿을 받은 세계만 관찰된다 ───
        # 청크 2 "이 학생은 실제로 태블릿을 받았습니다."
        # 남는 요소: 상단 문구, 어두운 오른쪽 세계
        # 새로 등장: 왼쪽 세계 다시 밝게 + 눈 아이콘 "관찰" 태그 (왼쪽 막대 위)
        # 비워 두는 영역: 오른쪽 태그 자리 (Beat 3에서 사용)
        # 단일 시선 대상: 밝아진 왼쪽 세계
        self.wait_until(beat_starts[1] + 0.2)
        observed_tag = VGroup(
            load_icon("eye.svg", WHITE, 0.5),
            Text("관찰", font=FONT, font_size=34, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.15)
        observed_tag.move_to([-WORLD_X, WORLD_TAG_Y, 0])
        self.play(Transform(left_world, left_bright), run_time=0.8)
        self.play(FadeIn(observed_tag, shift=UP * 0.2), run_time=0.6)

        # ─── Beat 3: 받지 않았을 때의 성적은 볼 수 없는 반사실 ───
        # 청크 3 "그래서 받지 않았을 때의 성적은 볼 수 없는 반사실입니다."
        # 먼저 지울 요소: 오른쪽 노란 막대 (관찰되지 않으므로 채워진 막대로 남기지 않는다)
        # 남는 요소: 상단 문구, 밝은 왼쪽 세계 + "관찰", 어두운 오른쪽 학생·라벨
        # 새로 등장: 오른쪽 점선 윤곽 + 물음표 → 눈 가림 아이콘 "반사실" 태그
        # 비워 두는 영역: 막대 사이 가운데
        # 단일 시선 대상: 앞 절반은 오른쪽 점선 윤곽의 물음표, 뒤 절반은 "반사실" 태그
        self.wait_until(beat_starts[2] + 0.4)
        right_bar = w["right_bar"]
        unseen_outline = DashedVMobject(
            Rectangle(width=WORLD_BAR_WIDTH, height=WORLD_SCORE_WITHOUT, color=QUESTION_COLOR, stroke_width=4),
            num_dashes=28,
        ).move_to(right_bar.get_center())
        unseen_mark = Text("?", font=FONT, font_size=80, weight=BOLD, color=QUESTION_COLOR)
        unseen_mark.move_to(right_bar.get_center())
        # "받지 않았을 때의 성적은 볼 수 없는": 채워진 막대가 비고, 점선 윤곽과 물음표만 남는다.
        self.play(FadeOut(right_bar), Create(unseen_outline), run_time=0.9)
        self.play(FadeIn(unseen_mark, scale=0.6), run_time=0.4)
        # "반사실입니다": 오른쪽 막대 위에 반사실 태그.
        self.wait_until(beat_starts[2] + 2.8)
        counterfactual_tag = VGroup(
            load_icon("eye-off.svg", QUESTION_COLOR, 0.5),
            Text("반사실", font=FONT, font_size=34, color=QUESTION_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.15)
        counterfactual_tag.move_to([WORLD_X, WORLD_TAG_Y, 0])
        self.play(FadeIn(counterfactual_tag, shift=UP * 0.2), run_time=0.6)

        self.wait_until(audio_end + self.WAIT_TAIL)
