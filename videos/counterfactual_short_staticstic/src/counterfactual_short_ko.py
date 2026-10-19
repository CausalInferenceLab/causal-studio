import json
from pathlib import Path

from manim import *

# 이 영상 전용 9:16 세로 설정. 다른 영상의 config에는 영향을 주지 않는다.
# 프레임 9 x 16 단위, 540 x 960 px => 1단위 = 60px (기본 480p 가로 영상과 같은 밀도).
config.frame_width = 9.0
config.frame_height = 16.0
config.pixel_width = 540
config.pixel_height = 960
config.background_color = BLACK

FONT = "Noto Sans KR"

# 색상 의미 (Scene 간 공통)
STUDENT_COLOR = WHITE      # 같은 학생: 항상 흰색 user 아이콘
TABLET_COLOR = TEAL_D      # 태블릿(처치): 청록
GRADE_COLOR = GREEN_C      # 성적 변화: 초록
QUESTION_COLOR = YELLOW_E  # 질문·강조: 노랑
NEUTRAL_COLOR = GREY_B     # 보조 화살표·라벨

ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
TOPIC_DIR = Path(__file__).resolve().parents[1]


def load_icon(filename: str, color: str, height: float) -> SVGMobject:
    icon = SVGMobject(str(ASSET_DIR / filename))
    icon.set_stroke(color=color, width=6, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def make_student(height: float = 2.6) -> SVGMobject:
    return load_icon("user.svg", STUDENT_COLOR, height)


def make_tablet(height: float = 2.2) -> SVGMobject:
    return load_icon("device-tablet.svg", TABLET_COLOR, height)


def make_grade_up(height: float = 2.2) -> SVGMobject:
    return load_icon("trending-up.svg", GRADE_COLOR, height)


def make_label(text: str, color: str, font_size: float = 48) -> Text:
    return Text(text, font=FONT, font_size=font_size, color=color, weight=BOLD)


def load_chunk_durations(scene_basename: str, fallback: list[float]) -> list[float]:
    timings_path = TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json"
    if not timings_path.exists():
        return fallback
    payload = json.loads(timings_path.read_text(encoding="utf-8"))
    return [float(chunk["duration"]) for chunk in payload.get("chunks", [])]


class TimedScene(Scene):
    """누적 시간을 추적해 timings.json의 청크 경계에 화면 전환을 맞추는 공통 베이스."""

    def setup(self):
        self.t = 0.0

    def play_t(self, *animations, run_time: float = 1.0, **kwargs):
        self.play(*animations, run_time=run_time, **kwargs)
        self.t += run_time

    def wait_until(self, target: float):
        gap = target - self.t
        if gap > 0.04:
            self.wait(gap)
            self.t = target


class Scene01_TabletQuestion(TimedScene):
    """
    Scene 01: 질문 — 성적이 올랐다는 사실만으로는 태블릿 덕분인지 알 수 없다.

    Core Claim:
    성적 상승 + 태블릿 지급이 함께 관찰되어도 그것만으로 태블릿의 효과라고 단정할 수 없다.

    Expected Misconception:
    "태블릿을 받았고 성적이 올랐으니 태블릿 덕분이다."

    Visual Pivot:
    학생 -> 태블릿 -> 성적 상승의 직선 흐름 사이에 큰 물음표를 끼워 넣어
    "연결을 아직 확인하지 못했다"는 점을 보여준다. 마지막은 학생 한 명만 남겨
    Scene 02에서 같은 학생이 두 세계로 갈라질 자리를 만든다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 3: 태블릿 지급을 인과 질문으로 여는 도입
    - 셀 5: 성적이 높아도 태블릿 효과라고 단정할 수 없다는 설명
    - 셀 8: 태블릿 지급 = 처치 (용어는 쓰지 않고 개념만 사용)

    Script Reference:
    src/scripts/ko/01_tablet_question.txt
    직전 Scene 마지막 문장: 없음 (첫 Scene)
    현재 Scene 첫 문장: "한 학생이 이번 학기에 태블릿을 받았어요."

    Script-to-Beat Mapping (timings.json 기준):
    청크 1 (0.00~6.96s)
      "한 학생이 이번 학기에 태블릿을 받았어요." -> 학생 등장, 태블릿이 학생에게 향하는 화살표, `태블릿 지급`
      "그리고 학기 말, 성적이 올랐습니다."       -> 아래쪽에 상승 아이콘, `성적 ↑`
    청크 2 (6.96~16.37s)
      "그럼 성적이 오른 건 정말 태블릿 덕분일까요?" -> 학생을 지우고 태블릿과 성적 사이에 큰 물음표, `태블릿 덕분?`
      "성적이 올랐다는 사실만으로는, 아직 알 수 없어요." -> 물음표 강조 후 학생 한 명만 중앙에 남김

    3Blue1Brown Reference:
    3b1b/_2020/covid.py - IntroQuestion 의 "질문을 한 가지씩 제시" 리듬만 참고.
    (이 Scene은 코드를 가져오지 않고 구성만 참고했다.)
    """

    # 승인된 음성(16.37s)보다 화면이 약간 늦게 끝나도록 여백을 둔다.
    WAIT_TAIL = 0.7

    def construct(self):
        d1, d2 = load_chunk_durations("01_tablet_question", [6.96, 9.408])
        t_chunk2 = d1            # 청크 2 시작 (질문 문장)
        t_end = d1 + d2          # 음성 끝
        # 청크 2 안에서 두 번째 문장("...아직 알 수 없어요")이 시작되는 시점. 글자 수 비율로 추정.
        t_second_sentence = t_chunk2 + d2 * 0.38

        # ─── Beat 1: 청크 1 — 학생이 태블릿을 받고, 성적이 오른다 ───
        # 남는 요소: 없음(첫 화면)
        # 새로 등장: 학생(상단), 태블릿+화살표(중단), 성적 상승(하단)
        # 비워 두는 영역: 좌우 여백, 최하단 자막 안전 영역
        # 단일 핵심 시선 대상: 지금 말하는 문장에 해당하는 새 요소 (순서대로 하나씩 등장)
        student = make_student(2.6).move_to(UP * 4.3)
        tablet = make_tablet(2.2).move_to(UP * 0.9)
        tablet_label = make_label("태블릿 지급", TABLET_COLOR).next_to(tablet, DOWN, buff=0.35)
        give_arrow = Arrow(
            tablet.get_top(), student.get_bottom(),
            buff=0.15, stroke_width=10, color=TABLET_COLOR,
        )
        grade = make_grade_up(2.2).move_to(DOWN * 3.9)
        grade_label = make_label("성적 ↑", GRADE_COLOR).next_to(grade, DOWN, buff=0.35)

        # "한 학생이" — 학생 먼저
        self.play_t(FadeIn(student, shift=DOWN * 0.2), run_time=0.8)
        self.wait_until(1.2)
        # "태블릿을 받았어요" — 태블릿이 학생을 향한다
        self.play_t(FadeIn(tablet, shift=UP * 0.2), GrowArrow(give_arrow), run_time=1.0)
        self.play_t(FadeIn(tablet_label), run_time=0.5)
        # "그리고 학기 말, 성적이 올랐습니다" — 하단에 성적 상승
        self.wait_until(4.0)
        self.play_t(FadeIn(grade, shift=UP * 0.3), run_time=0.8)
        self.play_t(FadeIn(grade_label), run_time=0.5)
        self.wait_until(t_chunk2)

        # ─── Beat 2: 청크 2 앞 문장 — "정말 태블릿 덕분일까요?" ───
        # 먼저 지울 것: 학생과 지급 화살표 (시선 경쟁 제거)
        # 남는 요소: 태블릿(상단으로 이동), 성적 상승(하단 유지)
        # 새로 등장: 큰 물음표(중앙) + `태블릿 덕분?`, 위아래 연결 화살표
        # 비워 두는 영역: 좌우 여백
        # 단일 핵심 시선 대상: 중앙의 큰 물음표
        tablet_group = VGroup(tablet, tablet_label)
        question = Text("?", font=FONT, font_size=220, color=QUESTION_COLOR, weight=BOLD)
        question.move_to(UP * 0.1)
        question_label = make_label("태블릿 덕분?", QUESTION_COLOR, 52).next_to(question, DOWN, buff=0.2)

        self.play_t(
            FadeOut(student), FadeOut(give_arrow),
            tablet_group.animate.shift(UP * 3.5),
            run_time=0.8,
        )
        link_top = Arrow(
            tablet_group.get_bottom(), question.get_top(),
            buff=0.15, stroke_width=8, color=NEUTRAL_COLOR,
        )
        link_bottom = Arrow(
            question_label.get_bottom(), grade.get_top(),
            buff=0.15, stroke_width=8, color=NEUTRAL_COLOR,
        )
        self.play_t(
            FadeIn(question, scale=0.6), GrowArrow(link_top), GrowArrow(link_bottom),
            run_time=0.8,
        )
        self.play_t(FadeIn(question_label), run_time=0.5)

        # ─── Beat 3: 청크 2 뒤 문장 — "성적이 올랐다는 사실만으로는, 아직 알 수 없어요" ───
        # 남는 요소: 물음표를 포함한 세로 흐름 전체
        # 새로 등장: 없음 (물음표만 한 번 강조)
        # 단일 핵심 시선 대상: 물음표
        self.wait_until(t_second_sentence)
        self.play_t(Indicate(question, color=QUESTION_COLOR, scale_factor=1.2), run_time=1.2)

        # ─── Beat 4: 마무리 — 학생 한 명만 중앙에 남긴다 (Scene 02 시작 화면과 동일) ───
        # 먼저 지울 것: 태블릿·성적·물음표·화살표·라벨 전부
        # 새로 등장: 중앙의 학생 (Scene 02에서 두 갈래로 나뉠 자리)
        # 비워 두는 영역: 학생 외 전체
        self.wait_until(t_end - 2.2)
        final_student = make_student(3.8).move_to(UP * 0.5)
        self.play_t(
            FadeOut(tablet_group), FadeOut(question), FadeOut(question_label),
            FadeOut(link_top), FadeOut(link_bottom), FadeOut(grade), FadeOut(grade_label),
            run_time=0.7,
        )
        self.play_t(FadeIn(final_student, scale=0.9), run_time=0.8)
        self.wait_until(t_end + self.WAIT_TAIL)
