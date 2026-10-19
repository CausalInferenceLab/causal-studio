"""
같은 학생의 두 세계 — 태블릿의 효과는 어떻게 알까? (세로형 쇼츠, 한국어)

원본 노트북: book/why_causal_inference/why_causal_inference_ko.ipynb
- 셀 [5]: 태블릿과 성적의 연관관계 ≠ 인과관계
- 셀 [8]: 같은 학생의 두 세계는 동시에 관찰할 수 없다, 사실 / 반사실
참고 영상 코드: videos/why_causal_inference/src/why_causal_inference.py
- Scene03_CounterfactualWorlds (한 학생이 두 세계로 갈라지는 연출, 아이콘 로딩 방식)

Scene 간 공통 화면 문법 (모든 Scene에서 유지):
- 학생 = 흰색 user.svg 하나. 서로 다른 학생을 비교하는 그림은 쓰지 않는다.
- 색 의미: 태블릿(처치) = 청록, 성적(결과) = 노랑, 아직 모름(질문) = 주황, 보조 = 회색
- 세로 3구획: 상단(y≈+5) 짧은 핵심 문구 / 중단(y≈+1) 학생·태블릿 / 하단(y≈-4.4) 성적
"""

import json
from pathlib import Path

from manim import *

# ── 9:16 세로 화면: 이 영상 모듈에만 적용 ─────────────────────────────
# 렌더 화질 플래그(-ql, -qh 등)가 정한 긴 변을 세로 높이로 쓰고, 폭은 9/16로 계산한다.
_long_side = max(config.pixel_width, config.pixel_height)
config.pixel_height = _long_side
config.pixel_width = int(round(_long_side * 9 / 16 / 2) * 2)
config.frame_height = 16.0
config.frame_width = 9.0
config.background_color = BLACK

KOR_FONT = "Pretendard Variable"

STUDENT_COLOR = WHITE
TABLET_COLOR = TEAL_C
OUTCOME_COLOR = YELLOW_C
QUESTION_COLOR = "#F2994A"
MUTED_COLOR = GREY_B

TOPIC_DIR = Path(__file__).resolve().parents[1]
ICON_DIR = TOPIC_DIR.parent / "assets" / "tabler-icons" / "icons" / "outline"

# 마지막 청크가 끝난 뒤 화면을 더 유지하는 시간(초). 영상이 mp3보다 짧아지지 않게 하는 최소 여유.
# 합본 싱크 QA: Scene별 음성 트랙을 영상 길이에 정확히 맞추므로(apad) 여유가 길면 전체 길이만 늘어난다.
TAIL_PAD = 0.25

TOP_Y = 5.0
MID_Y = 1.0
LOW_Y = -4.4


def load_icon(filename: str, color: str, height: float) -> SVGMobject:
    """공용 Tabler Icons(outline) SVG를 선 아이콘으로 불러온다."""
    icon = SVGMobject(str(ICON_DIR / filename))
    icon.set_stroke(color=color, width=3, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def kor_text(text: str, size: float = 54, color: str = WHITE, weight: str = BOLD) -> Text:
    """짧은 화면 문구 전용. 긴 문장 자막은 쓰지 않는다."""
    return Text(text, font=KOR_FONT, font_size=size, color=color, weight=weight)


def make_student(height: float = 2.6) -> SVGMobject:
    """모든 Scene에서 같은 모양으로 쓰는 학생 아이콘."""
    return load_icon("user.svg", STUDENT_COLOR, height)


def make_tablet(height: float = 1.5) -> SVGMobject:
    return load_icon("device-tablet.svg", TABLET_COLOR, height)


def make_score_badge() -> VGroup:
    """성적(결과) 표시: '성적' 라벨 + 상승 아이콘. 숫자는 쓰지 않는다."""
    label = kor_text("성적", 52, OUTCOME_COLOR)
    trend = load_icon("trending-up.svg", OUTCOME_COLOR, 1.6)
    badge = VGroup(label, trend).arrange(RIGHT, buff=0.45)
    frame = SurroundingRectangle(
        badge, color=OUTCOME_COLOR, buff=0.45, corner_radius=0.25, stroke_width=3
    )
    return VGroup(frame, badge)


def load_chunk_ends(scene_basename: str) -> list[float]:
    """timings.json의 청크 끝 시각(초) 목록. 화면 전환 기준으로 쓴다."""
    path = TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json"
    chunks = json.loads(path.read_text())["chunks"]
    return [float(c["end"]) for c in chunks]


class TimedScene(Scene):
    """청크 시각에 맞춰 Beat를 넘기기 위한 경과 시간 추적용 베이스."""

    def setup(self):
        self.elapsed = 0.0

    def play_timed(self, *animations, run_time: float = 1.0, **kwargs):
        self.play(*animations, run_time=run_time, **kwargs)
        self.elapsed += run_time

    def wait_until(self, t: float):
        """해당 청크가 끝나는 시각까지 화면을 유지한다."""
        if t > self.elapsed + 1e-3:
            self.wait(t - self.elapsed)
            self.elapsed = t


class Scene01_Question(TimedScene):
    """
    Scene 01: 질문 — 태블릿을 받은 학생의 성적이 올랐다. 태블릿 덕분일까?

    핵심 주장:
    성적이 올랐다는 관찰만으로는 태블릿의 효과라고 단정할 수 없다.

    예상 오해:
    "태블릿을 받은 뒤 성적이 올랐으니 태블릿 덕분이다" (전후 비교 = 인과로 착각)

    Visual Pivot:
    학생 → 태블릿 → 성적 상승까지는 확실한 '관찰'로 실선 연결,
    태블릿 → 성적 사이의 '원인' 연결만 점선 + 물음표로 남겨 둔다.

    Scene 경계:
    - 첫 문장: "한 학생이 태블릿을 받았습니다."
    - 마지막 문장: "성적이 올랐다는 사실만으로는, 아직 알 수 없습니다."
    - 다음 Scene 02는 같은 학생이 두 세계로 갈라지는 장면으로 이어진다(학생 위치·크기 유지).
    - ipynb 셀 [5] 첫 문단(연관관계 ≠ 인과관계)에 해당.

    3b1b 참고: 3b1b/_2020/covid.py IntroQuestion
    선정 이유: 질문 하나를 화면 중앙에 던지고 단계적으로 의심을 키우는 인트로 리듬이 유사.

    Script-to-Beat (build/audio/01_question.timings.json 청크 기준):
    1. 청크1 "한 학생이 태블릿을 받았습니다." → 학생 등장, 태블릿이 학생 옆으로 들어옴
    2. 청크2 "그 뒤로 이 학생의 성적이 올랐어요." → 하단 성적 배지 + 학생→성적 실선 화살표
    3. 청크3 "…태블릿 덕분일까요?" → '태블릿' 라벨 퇴장 후 태블릿→성적 점선 화살표 + 큰 물음표, 상단 질문 문구
    4. 청크4 "…사실만으로는, 아직 알 수 없습니다." → 상단 문구 교체, 물음표 강조 유지
    """

    def construct(self):
        ends = load_chunk_ends("01_question")
        # 음성 마지막 이후 TAIL_PAD만큼 유지해 영상이 mp3보다 짧아지지 않게 한다.
        tail_end = ends[-1] + TAIL_PAD

        # ── Beat 1 (청크1: 학생이 태블릿을 받음) ─────────────────────────
        # 남는 요소: 없음(첫 Beat) / 새 요소: 학생(중단 왼쪽), 태블릿(중단 오른쪽)
        # 비워 두는 영역: 상단 문구, 하단 성적 / 단일 시선 대상: 학생이 태블릿을 받는 순간
        student = make_student().move_to([-1.4, MID_Y, 0])
        tablet = make_tablet().move_to([1.9, MID_Y, 0])
        tablet_label = kor_text("태블릿", 40, TABLET_COLOR).next_to(tablet, DOWN, buff=0.3)

        self.play_timed(FadeIn(student, shift=UP * 0.3), run_time=0.8)
        self.play_timed(
            FadeIn(tablet, shift=LEFT * 1.2),
            FadeIn(tablet_label),
            run_time=1.0,
        )
        self.wait_until(ends[0])

        # ── Beat 2 (청크2: 그 뒤로 성적이 오름) ─────────────────────────
        # 남는 요소: 학생·태블릿 / 새 요소: 하단 성적 배지, 학생→성적 실선 화살표
        # 비워 두는 영역: 상단 / 단일 시선 대상: 하단 '성적 ↑'
        score = make_score_badge().move_to([0, LOW_Y, 0])
        observed_arrow = Arrow(
            student.get_bottom() + DOWN * 0.1,
            score.get_top() + LEFT * 1.1,
            buff=0.25,
            stroke_width=6,
            color=MUTED_COLOR,
        )
        self.play_timed(GrowArrow(observed_arrow), run_time=0.8)
        self.play_timed(FadeIn(score, shift=UP * 0.4), run_time=0.9)
        self.wait_until(ends[1])

        # ── Beat 3 (청크3: 태블릿 덕분일까?) ─────────────────────────────
        # 남는 요소: 학생·태블릿·성적 / 새 요소: 태블릿→성적 점선 화살표 + 물음표, 상단 질문 문구
        # 관찰(실선)은 회색으로 물러나고, 원인 연결(점선)만 주황으로 강조한다.
        # 단일 시선 대상: 점선 위 물음표
        # 첫 렌더 QA: 라벨·점선·물음표가 좁은 틈에 몰려 과밀 → '태블릿' 라벨을 먼저 지워 공간을 비운 뒤
        # 점선을 태블릿 아이콘 바로 아래에서 길게 시작하고 물음표를 키운다.
        cause_arrow = DashedVMobject(
            Arrow(
                tablet.get_bottom() + DOWN * 0.15,
                score.get_top() + RIGHT * 1.1,
                buff=0.25,
                stroke_width=6,
                color=QUESTION_COLOR,
            ),
            num_dashes=14,
        )
        question = load_icon("question-mark.svg", QUESTION_COLOR, 1.6)
        question.move_to(cause_arrow.get_center() + RIGHT * 1.15)
        headline = kor_text("태블릿 덕분일까?", 64).move_to([0, TOP_Y, 0])

        self.play_timed(FadeOut(tablet_label), run_time=0.4)
        self.play_timed(
            observed_arrow.animate.set_opacity(0.45),
            Create(cause_arrow),
            run_time=1.0,
        )
        self.play_timed(FadeIn(question, scale=1.4), Write(headline), run_time=1.0)
        self.wait_until(ends[2])

        # ── Beat 4 (청크4: 이것만으로는 아직 알 수 없다) ──────────────────
        # 남는 요소: 학생·태블릿·성적·점선·물음표 / 교체: 상단 문구
        # 새 큰 요소는 추가하지 않고, 문구 교체 + 물음표 맥박으로 '단정 금지'만 전달한다.
        # 단일 시선 대상: 상단 새 문구
        verdict = kor_text("이것만으론 알 수 없다", 60, QUESTION_COLOR).move_to([0, TOP_Y, 0])
        self.play_timed(ReplacementTransform(headline, verdict), run_time=0.9)
        self.play_timed(Indicate(question, color=QUESTION_COLOR, scale_factor=1.25), run_time=1.0)

        self.wait_until(tail_end)


def make_scene01_final() -> tuple[SVGMobject, VGroup]:
    """Scene 01 마지막 화면을 그대로 다시 만든다. (학생, 나머지 요소 묶음)
    Scene 02가 이 화면에서 시작해 경계에서 화면이 끊기지 않게 하기 위한 용도.
    좌표·크기·색은 Scene01_Question.construct와 같아야 한다."""
    student = make_student().move_to([-1.4, MID_Y, 0])
    tablet = make_tablet().move_to([1.9, MID_Y, 0])
    score = make_score_badge().move_to([0, LOW_Y, 0])
    observed_arrow = Arrow(
        student.get_bottom() + DOWN * 0.1, score.get_top() + LEFT * 1.1,
        buff=0.25, stroke_width=6, color=MUTED_COLOR,
    ).set_opacity(0.45)
    cause_arrow = DashedVMobject(
        Arrow(
            tablet.get_bottom() + DOWN * 0.15, score.get_top() + RIGHT * 1.1,
            buff=0.25, stroke_width=6, color=QUESTION_COLOR,
        ),
        num_dashes=14,
    )
    question = load_icon("question-mark.svg", QUESTION_COLOR, 1.6)
    question.move_to(cause_arrow.get_center() + RIGHT * 1.15)
    verdict = kor_text("이것만으론 알 수 없다", 60, QUESTION_COLOR).move_to([0, TOP_Y, 0])
    return student, VGroup(tablet, score, observed_arrow, cause_arrow, question, verdict)


# ── Scene 02·03 공통: 같은 학생의 두 세계 패널 ─────────────────────────
# 세로 화면을 좌/우 두 칸으로 나눈다. 두 칸 모두 '같은 학생'의 복사본이며,
# 다른 학생이 아니라는 점은 Scene 02 Beat 1의 분기 화살표(한 명 → 두 세계)로 보여 준다.
PANEL_W = 3.9
PANEL_H = 6.9
PANEL_Y = -1.95  # 패널 중심. 위 끝 y=1.5, 아래 끝 y=-5.4
PANEL_X = 2.15
BAR_BASE_Y = -5.0
BAR_W = 1.2
BAR_H_TREATED = 2.2  # 가상 예시 막대 높이(숫자 없음)
BAR_H_CONTROL = 1.3


def make_world_panel(received: bool) -> dict:
    """한 세계의 패널: 테두리, 학생 복사본, 태블릿 받음/안 받음 표시, 성적 막대."""
    x = -PANEL_X if received else PANEL_X
    color = TABLET_COLOR if received else MUTED_COLOR
    frame = RoundedRectangle(
        width=PANEL_W, height=PANEL_H, corner_radius=0.25, stroke_color=color, stroke_width=3
    ).move_to([x, PANEL_Y, 0])
    student = make_student(1.1).move_to([x, 0.6, 0])
    tablet = load_icon("device-tablet.svg", color, 1.0).move_to([x, -0.75, 0])
    treatment = VGroup(tablet)
    if not received:
        # '안 받음'은 태블릿 위에 사선 하나로 표시한다(빨강 대신 회색 계열 유지, 색 의미 고정).
        slash = Line(
            tablet.get_corner(DL) + DL * 0.15, tablet.get_corner(UR) + UR * 0.15,
            color=MUTED_COLOR, stroke_width=5,
        )
        treatment.add(slash)
    label = kor_text("받음" if received else "안 받음", 36, color).move_to([x, -1.75, 0])
    bar_h = BAR_H_TREATED if received else BAR_H_CONTROL
    bar = Rectangle(
        width=BAR_W, height=bar_h, stroke_width=0, fill_color=OUTCOME_COLOR, fill_opacity=0.9
    ).move_to([x, BAR_BASE_Y + bar_h / 2, 0])
    return {
        "frame": frame, "student": student, "treatment": treatment,
        "label": label, "bar": bar,
        "body": VGroup(frame, student, treatment, label),
    }


def make_virtual_note() -> Text:
    """막대가 실제 데이터가 아님을 밝히는 하단 표기."""
    return kor_text("성적 막대 = 가상 예시", 28, MUTED_COLOR, weight=NORMAL).move_to([0, -6.1, 0])


class Scene02_TwoWorlds(TimedScene):
    """
    Scene 02: 비교 — 같은 학생이 태블릿을 받은 세계와 받지 않은 세계

    핵심 주장:
    태블릿의 효과는 '같은 학생'이 받은 세계와 받지 않은 세계의 성적 차이다.

    예상 오해:
    태블릿을 받은 학생과 안 받은 '다른 학생'을 비교하면 효과를 알 수 있다고 생각한다.
    → 화면에서 학생 한 명이 두 갈래로 나뉘는 연출로, 비교 대상이 같은 사람임을 고정한다.

    Visual Pivot:
    Scene 01의 학생(중단, 같은 크기)에서 출발해 위로 올라간 뒤 두 세계로 분기한다.

    Scene 경계:
    - 직전 Scene 01 마지막 문장: "성적이 올랐다는 사실만으로는, 아직 알 수 없습니다."
    - 현재 첫 문장: "같은 학생의 두 세계를 떠올려 봅시다."
    - 마지막 문장: "두 세계의 성적 차이가, 이 학생에게 태블릿이 준 효과예요."
    - ipynb 셀 [8] "같은 학생이 태블릿을 받은 세계와 받지 않은 세계" + ITE 정의(수식 없이 말로만).

    3b1b 참고: 3b1b/_2018/uncertainty.py (가능한 두 상태를 나란히 대비시키는 분위기)
    선정 이유: Scene03_CounterfactualWorlds(기존 영상)도 같은 파일을 참고해 화면 문법을 맞춘다.

    Script-to-Beat (build/audio/02_two_worlds.timings.json 청크 기준):
    1. 청크1 "같은 학생의 두 세계를…" → Scene 01 마지막 화면에서 시작, 학생만 남기고 퇴장 →
       학생이 상단 중앙으로 올라가고 두 갈래 화살표
    2. 청크2 "태블릿을 받은 세계와, 받지 않은 세계." → 좌(받음·청록) / 우(안 받음·회색) 패널 등장
    3. 청크3 "두 세계의 성적 차이가… 효과예요." → 두 막대 + 우측 양방향 화살표, 상단 문구 '차이 = 태블릿 효과'
    """

    def construct(self):
        ends = load_chunk_ends("02_two_worlds")
        tail_end = ends[-1] + TAIL_PAD

        # ── Beat 1 (청크1: 같은 학생의 두 세계) ────────────────────────────
        # 남는 요소: 없음 / 새 요소: 학생(Scene 01과 같은 위치·크기에서 시작) → 상단 중앙, 분기 화살표 2개
        # 비워 두는 영역: 하단 패널 자리 / 단일 시선 대상: 한 명의 학생이 둘로 갈라지는 지점
        # 경계 QA: 빈 화면에서 시작하면 Scene 01 → 02가 끊겨 보임
        # → Scene 01 마지막 화면을 그대로 세운 뒤, 학생만 남기고 나머지를 퇴장시킨다.
        student, s01_rest = make_scene01_final()
        self.add(student, s01_rest)
        headline = kor_text("같은 학생, 두 세계", 60).move_to([0, 5.6, 0])
        self.play_timed(FadeOut(s01_rest), run_time=0.5)
        self.play_timed(student.animate.scale(2.0 / 2.6).move_to([0, 3.4, 0]), Write(headline), run_time=1.0)
        split_left = Arrow([0, 2.35, 0], [-PANEL_X, 1.55, 0], buff=0.05, stroke_width=6, color=TABLET_COLOR)
        split_right = Arrow([0, 2.35, 0], [PANEL_X, 1.55, 0], buff=0.05, stroke_width=6, color=MUTED_COLOR)
        self.play_timed(GrowArrow(split_left), GrowArrow(split_right), run_time=0.8)
        self.wait_until(ends[0])

        # ── Beat 2 (청크2: 받은 세계와 받지 않은 세계) ─────────────────────
        # 남는 요소: 상단 학생·문구·분기 화살표 / 새 요소: 좌·우 패널(막대 제외)
        # 단일 시선 대상: 두 패널의 '받음 / 안 받음' 대비
        treated = make_world_panel(received=True)
        control = make_world_panel(received=False)
        self.play_timed(FadeIn(treated["body"], shift=DOWN * 0.3), run_time=0.9)
        self.play_timed(FadeIn(control["body"], shift=DOWN * 0.3), run_time=0.9)
        self.wait_until(ends[1])

        # ── Beat 3 (청크3: 두 세계의 성적 차이 = 이 학생에게 준 효과) ──────
        # 남는 요소: 패널 / 새 요소: 성적 막대 2개 → 기준 점선 + 양방향 화살표, 하단 '가상 예시'
        # 교체: 상단 문구 → '차이 = 태블릿 효과' / 단일 시선 대상: 오른쪽 막대 위 차이 화살표
        self.play_timed(
            GrowFromEdge(treated["bar"], DOWN), GrowFromEdge(control["bar"], DOWN),
            FadeIn(make_virtual_note()),
            run_time=1.0,
        )
        top_y = BAR_BASE_Y + BAR_H_TREATED
        low_y = BAR_BASE_Y + BAR_H_CONTROL
        guide = DashedLine(
            [-PANEL_X + BAR_W / 2, top_y, 0], [PANEL_X + BAR_W / 2 + 0.6, top_y, 0],
            color=OUTCOME_COLOR, stroke_width=3, dash_length=0.15,
        )
        gap = DoubleArrow(
            [PANEL_X + BAR_W / 2 + 0.45, low_y, 0], [PANEL_X + BAR_W / 2 + 0.45, top_y, 0],
            buff=0, stroke_width=5, tip_length=0.22, color=WHITE,
        )
        effect_title = kor_text("차이 = 태블릿 효과", 60).move_to([0, 5.6, 0])
        self.play_timed(Create(guide), GrowFromCenter(gap), run_time=0.9)
        self.play_timed(ReplacementTransform(headline, effect_title), run_time=0.8)
        self.wait_until(tail_end)


class Scene03_Counterfactual(TimedScene):
    """
    Scene 03: 핵심 — 실제로는 한쪽 결과만 관찰할 수 있다

    핵심 주장:
    현실에서는 한 세계만 관찰된다. 태블릿을 실제로 받았다면, 받지 않았을 때의 결과는 반사실이다.

    예상 오해:
    Scene 02의 두 막대를 실제 데이터처럼 둘 다 볼 수 있다고 생각한다.

    Visual Pivot:
    Scene 02 마지막 화면(두 패널 + 막대)을 그대로 이어받아, 오른쪽 세계만 흐려지고
    막대가 점선 '?'로 바뀐다. 차이 화살표는 사라진다 → 반사실을 모르면 효과도 바로 계산할 수 없다.

    Scene 경계:
    - 직전 Scene 02 마지막 문장: "두 세계의 성적 차이가, 이 학생에게 태블릿이 준 효과예요."
    - 현재 첫 문장: "하지만 현실에선 한 세계만 볼 수 있어요."
    - 마지막 문장: "이렇게 일어나지 않은 쪽의 결과를, 반사실이라고 합니다."
    - ipynb 셀 [8] "실제로 일어난 결과를 사실(Factual), 일어나지 않은 쪽의 결과를 반사실(Counterfactual)".

    3b1b 참고: 3b1b/_2018/uncertainty.py (Scene 02와 동일, 한쪽 상태를 지워 대비를 끝맺음)

    Script-to-Beat (build/audio/03_counterfactual.timings.json 청크 기준):
    1. 청크1 "하지만 현실에선 한 세계만…" → Scene 02 끝 화면(상단 학생·분기 화살표 포함) 재구성 후
       차이 화살표·상단 학생 퇴장, 상단 '한 세계만 보인다'
    2. 청크2 "태블릿을 실제로 받았다면… 볼 수 없죠." → 오른쪽 패널 흐림 + eye-off, 막대 → 점선 '?'
    3. 청크3 "…반사실이라고 합니다." → 좌 '실제' / 우 '반사실' 라벨, 상단 문구 교체
    """

    def construct(self):
        ends = load_chunk_ends("03_counterfactual")
        tail_end = ends[-1] + TAIL_PAD

        # ── Beat 1 (청크1: 현실에선 한 세계만) ──────────────────────────────
        # 개별 실행을 위해 Scene 02의 마지막 화면(패널·막대·차이 화살표·가상 예시)을 먼저 다시 세운다.
        # 남는 요소: 패널·막대·가상 예시 / 퇴장: 차이 화살표·점선 / 새 요소: 상단 '한 세계만 보인다'
        # 단일 시선 대상: 상단 문구
        treated = make_world_panel(received=True)
        control = make_world_panel(received=False)
        note = make_virtual_note()
        top_y = BAR_BASE_Y + BAR_H_TREATED
        low_y = BAR_BASE_Y + BAR_H_CONTROL
        gap = DoubleArrow(
            [PANEL_X + BAR_W / 2 + 0.45, low_y, 0], [PANEL_X + BAR_W / 2 + 0.45, top_y, 0],
            buff=0, stroke_width=5, tip_length=0.22, color=WHITE,
        )
        prev_title = kor_text("차이 = 태블릿 효과", 60).move_to([0, 5.6, 0])
        guide = DashedLine(
            [-PANEL_X + BAR_W / 2, top_y, 0], [PANEL_X + BAR_W / 2 + 0.6, top_y, 0],
            color=OUTCOME_COLOR, stroke_width=3, dash_length=0.15,
        )
        # Scene 02 끝 화면의 상단 학생·분기 화살표까지 똑같이 세워 경계에서 화면이 튀지 않게 한다.
        top_student = make_student(2.0).move_to([0, 3.4, 0])
        split_left = Arrow([0, 2.35, 0], [-PANEL_X, 1.55, 0], buff=0.05, stroke_width=6, color=TABLET_COLOR)
        split_right = Arrow([0, 2.35, 0], [PANEL_X, 1.55, 0], buff=0.05, stroke_width=6, color=MUTED_COLOR)
        self.add(
            treated["body"], control["body"], treated["bar"], control["bar"], note,
            gap, guide, prev_title, top_student, split_left, split_right,
        )

        one_world = kor_text("한 세계만 보인다", 60).move_to([0, 5.6, 0])
        # 차이 화살표는 '두 세계를 다 볼 수 있을 때만' 가능한 표시이므로 가장 먼저 퇴장시킨다.
        self.play_timed(
            FadeOut(gap), FadeOut(guide), FadeOut(top_student), FadeOut(split_left), FadeOut(split_right),
            ReplacementTransform(prev_title, one_world),
            run_time=1.0,
        )
        self.wait_until(ends[0])

        # ── Beat 2 (청크2: 실제로 받았다면, 안 받은 세계는 볼 수 없다) ──────
        # 남는 요소: 왼쪽 패널(선명) / 변형: 오른쪽 패널 흐림, 막대 → 점선 윤곽 + '?'
        # 새 요소: 오른쪽 패널 중앙 eye-off / 단일 시선 대상: 흐려지는 오른쪽 세계
        ghost_bar = DashedVMobject(
            Rectangle(width=BAR_W, height=BAR_H_CONTROL, color=QUESTION_COLOR, stroke_width=4)
            .move_to(control["bar"]),
            num_dashes=24,
        )
        unknown = load_icon("question-mark.svg", QUESTION_COLOR, 0.9).move_to(control["bar"])
        eye_off = load_icon("eye-off.svg", QUESTION_COLOR, 1.3).move_to([PANEL_X, 2.3, 0])
        # 첫 렌더 QA: set_opacity가 선 아이콘의 채우기까지 켜 패널이 회색 덩어리로 보임
        # → 선(stroke)과 글자(fill)를 따로 흐리게 한다.
        dim_lines = VGroup(control["frame"], control["student"], control["treatment"])
        self.play_timed(
            dim_lines.animate.set_stroke(opacity=0.25),
            control["label"].animate.set_fill(opacity=0.25),
            ReplacementTransform(control["bar"], ghost_bar),
            run_time=1.2,
        )
        self.play_timed(FadeIn(unknown, scale=1.3), FadeIn(eye_off, shift=DOWN * 0.2), run_time=0.8)
        self.wait_until(ends[1])

        # ── Beat 3 (청크3: 일어나지 않은 쪽의 결과 = 반사실) ────────────────
        # 남는 요소: 두 패널 / 새 요소: 좌 '실제'(흰색) · 우 '반사실'(주황) 라벨 — eye-off 자리를 라벨로 교체
        # 교체: 상단 문구 → '안 본 쪽 = 반사실' / 단일 시선 대상: 오른쪽 '반사실' 라벨
        factual_tag = kor_text("실제", 48).move_to([-PANEL_X, 2.3, 0])
        counter_tag = kor_text("반사실", 48, QUESTION_COLOR).move_to([PANEL_X, 2.3, 0])
        final_title = kor_text("못 본 쪽 = 반사실", 60, QUESTION_COLOR).move_to([0, 5.6, 0])
        self.play_timed(FadeIn(factual_tag, shift=DOWN * 0.2), ReplacementTransform(eye_off, counter_tag), run_time=0.9)
        self.play_timed(ReplacementTransform(one_world, final_title), run_time=0.8)
        self.play_timed(Indicate(counter_tag, color=QUESTION_COLOR, scale_factor=1.15), run_time=0.9)
        self.wait_until(tail_end)
