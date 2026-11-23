"""
같은 학생의 두 세계 — 태블릿의 효과는 어떻게 알까? (한국어 세로 쇼츠, 약 45초)

- Scene 01 질문: 성적이 올랐다는 사실만으로는 태블릿 덕분이라고 말할 수 없다.
- Scene 02 비교: 같은 학생의 '받은 세계'와 '받지 않은 세계'를 비교해야 효과를 안다.
- Scene 03 핵심: 현실에선 한쪽만 관찰된다. 실제로 받았다면, 받지 않았을 때의 결과는 반사실이다.

각 Scene은 따로 렌더해도 되도록, 직전 Scene의 마지막 화면을 공용 함수로 다시 만들어 시작한다.
그래서 직전 Scene의 마지막 프레임과 다음 Scene의 첫 프레임이 같아 합본 경계가 끊기지 않는다.

렌더 예 (videos/counterfactual_short_jhkimon 에서):
  ../../.venv/bin/manim -ql --media_dir build/manim src/counterfactual_short_ko.py Scene01_TabletQuestion
"""

import json
from pathlib import Path
from types import SimpleNamespace

from manim import *


# ── 9:16 세로 화면: 이 파일에만 적용 ─────────────────────────────────
# -ql(854x480), -qh(1920x1080) 같은 화질 플래그가 정한 가로형 해상도를 세로로 뒤집고,
# 화면 높이 8을 기준으로 폭을 같은 비율(약 4.5)로 맞춘다.
if config.pixel_width > config.pixel_height:
    config.pixel_width, config.pixel_height = config.pixel_height, config.pixel_width
config.frame_height = 8.0
config.frame_width = config.frame_height * config.pixel_width / config.pixel_height
config.background_color = BLACK

TOPIC_DIR = Path(__file__).resolve().parents[1]
AUDIO_DIR = TOPIC_DIR / "build" / "audio"
ICON_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
FONT = "NanumSquare Neo"

# 색의 의미는 세 Scene에서 똑같이 쓴다.
STUDENT_COLOR = WHITE      # 학생 (두 세계 모두 같은 사람)
TABLET_COLOR = TEAL_C      # 태블릿을 받은 세계
NO_TABLET_COLOR = GOLD_C   # 태블릿을 받지 않은 세계
QUESTION_COLOR = YELLOW_C  # 질문, 핵심 강조
UNSEEN_COLOR = GREY_B      # 관찰할 수 없는 것, 보조 정보
DIM_COLOR = GREY_D         # 일어나지 않은 세계

# 화면 구획 (세로 8 x 가로 약 4.5).
# 상단 제목 한 줄, 가운데 아이콘·세계 칸, 그 아래 점수 줄. y < -2.6은 쇼츠 UI에 가려질 수 있어 비워 둔다.
HEADLINE_Y = 3.15
PANEL_X, PANEL_Y = 1.05, 0.6
PANEL_W, PANEL_H = 1.9, 2.9
SCORE_Y = -1.35
NOTE_Y = -1.95
EXAMPLE_TAG_Y = -2.5

# 노트북 셀 10 표의 i=4 학생 (t=1, y1=750, y0=700)을 가상 예시 점수로 쓴다.
SCORE_WITH_TABLET = "750점"
SCORE_WITHOUT_TABLET = "700점"


def ko(text: str, size: float = 34, color=WHITE) -> Text:
    return Text(text, font=FONT, font_size=size, color=color, weight=BOLD)


def icon(name: str, color, height: float, stroke: float = 3.2) -> SVGMobject:
    mob = SVGMobject(str(ICON_DIR / name))
    mob.set_fill(opacity=0)
    mob.set_stroke(color=color, width=stroke, opacity=1)
    mob.height = height
    return mob


def make_student(height: float = 1.1) -> SVGMobject:
    # 학생 모양은 세 Scene 모두 이 아이콘 하나로 통일한다.
    return icon("user.svg", STUDENT_COLOR, height)


def headline(text: str, color=WHITE) -> Text:
    title = ko(text, 34, color)
    # 세로 화면 폭을 넘지 않도록 좌우 0.35씩 여백을 남긴다.
    if title.width > config.frame_width - 0.7:
        title.scale_to_fit_width(config.frame_width - 0.7)
    return title.move_to(UP * HEADLINE_Y)


def link(start, end, color) -> Arrow:
    return Arrow(
        start,
        end,
        buff=0.15,
        color=color,
        stroke_width=4,
        tip_length=0.18,
        max_tip_length_to_length_ratio=0.4,
        max_stroke_width_to_length_ratio=8,
    )


def build_chain() -> SimpleNamespace:
    """Scene 01 화면: 태블릿 → 학생 → 성적↑ 을 세로 한 줄로 놓는다."""
    tablet = icon("device-tablet.svg", TABLET_COLOR, 0.8).move_to(UP * 1.65)
    student = make_student(1.1)
    score = VGroup(ko("성적", 36), icon("trending-up.svg", WHITE, 0.42)).arrange(RIGHT, buff=0.16)
    score.move_to(DOWN * 1.65)
    give = link(tablet.get_bottom(), student.get_top(), TABLET_COLOR)
    lead = link(student.get_bottom(), score.get_top(), WHITE)
    return SimpleNamespace(
        tablet=tablet,
        student=student,
        score=score,
        give=give,
        lead=lead,
        group=VGroup(tablet, give, student, lead, score),
    )


def build_world(side: int, color, badge_icon: str, label: str) -> SimpleNamespace:
    """세계 한 칸: 위에서부터 태블릿 아이콘, 짧은 라벨, 학생."""
    center = side * PANEL_X * RIGHT + PANEL_Y * UP
    frame = RoundedRectangle(
        width=PANEL_W,
        height=PANEL_H,
        corner_radius=0.18,
        stroke_color=color,
        stroke_width=3,
    ).move_to(center)
    badge = icon(badge_icon, color, 0.6).move_to(center + UP * 0.95)
    tag = ko(label, 26, color).move_to(center + UP * 0.35)
    student = make_student(0.95).move_to(center + DOWN * 0.6)
    return SimpleNamespace(
        frame=frame,
        badge=badge,
        tag=tag,
        student=student,
        group=VGroup(frame, badge, tag, student),
    )


def build_worlds() -> SimpleNamespace:
    """Scene 02 마지막 화면: 같은 학생의 두 세계 + 두 점수 + 차이(효과)."""
    left = build_world(-1, TABLET_COLOR, "device-tablet.svg", "받음")
    right = build_world(1, NO_TABLET_COLOR, "device-tablet-off.svg", "안 받음")
    score_l = ko(SCORE_WITH_TABLET, 32).move_to([-PANEL_X, SCORE_Y, 0])
    score_r = ko(SCORE_WITHOUT_TABLET, 32).move_to([PANEL_X, SCORE_Y, 0])
    effect = DoubleArrow(
        LEFT * 0.26,
        RIGHT * 0.26,
        buff=0,
        color=QUESTION_COLOR,
        stroke_width=4,
        tip_length=0.13,
        max_tip_length_to_length_ratio=0.4,
    ).move_to(UP * SCORE_Y)
    effect_label = ko("효과", 28, QUESTION_COLOR).move_to(UP * NOTE_Y)
    example_tag = ko("가상 예시", 22, UNSEEN_COLOR).move_to(UP * EXAMPLE_TAG_Y)
    return SimpleNamespace(
        left=left,
        right=right,
        score_l=score_l,
        score_r=score_r,
        effect=effect,
        effect_label=effect_label,
        example_tag=example_tag,
        group=VGroup(
            left.group, right.group, score_l, score_r, effect, effect_label, example_tag
        ),
    )


class ShortScene(Scene):
    """세 Scene 공통: build/audio/{AUDIO}.timings.json의 청크 시작 시각에 맞춰 Beat를 놓는다.

    timings.json이 없으면(새로 clone한 경우 등) 아래 FALLBACK 값(2026-10-19 생성본 실측)을 쓴다.
    청크 안의 문장·구 경계는 같은 mp3의 silencedetect(-40dB) 결과를 청크 시작 기준 오프셋으로 적었다.
    """

    AUDIO = ""
    FALLBACK_STARTS: tuple = ()
    FALLBACK_TOTAL = 0.0
    # 마지막 음성 뒤 화면 여유. 합본 때 붙이는 무음 쉼보다 0.2초 길게 잡아 영상이 오디오보다 먼저 끝나지 않게 한다.
    END_PAD = 0.5

    def setup(self):
        path = AUDIO_DIR / f"{self.AUDIO}.timings.json"
        if path.exists():
            payload = json.loads(path.read_text())
            self.starts = [float(chunk["start"]) for chunk in payload["chunks"]]
            self.total = float(payload["totalDuration"])
        else:
            self.starts = list(self.FALLBACK_STARTS)
            self.total = self.FALLBACK_TOTAL

    def cue(self, chunk: int, offset: float = 0.0) -> float:
        return self.starts[chunk - 1] + offset

    def wait_until(self, t: float):
        remaining = t - self.renderer.time
        if remaining > 1e-3:
            self.wait(remaining)

    def finish(self):
        self.wait_until(self.total + self.END_PAD)


class Scene01_TabletQuestion(ShortScene):
    """
    Scene 01: 질문 — 태블릿을 받은 학생의 성적이 올랐다. 태블릿 덕분일까?

    Core Claim:
    성적이 올랐다는 사실만으로는 그것이 태블릿 덕분이라고 말할 수 없다.

    Expected Misconception:
    "받고 나서 올랐으니 태블릿 효과다." 성적은 다른 이유로도 오를 수 있다.

    Visual Pivot:
    태블릿 → 학생 → 성적↑ 세로 사슬 옆에 '태블릿 → 성적' 지름길 화살표와 "?"가 붙었다가 흐려지고,
    이름 없는 회색 원인들이 성적으로 들어온다. 마지막엔 사슬만 남기고 "무엇과 비교할까?"로 끝낸다.

    Scene Boundary:
    - 직전 Scene 마지막 문장: 없음 (첫 Scene)
    - 현재 Scene 첫 문장: "한 학생이 태블릿을 받았습니다."
    - 다음 Scene 첫 문장: "같은 학생의 두 세계를 비교해야 해요." (여기서는 답을 말하지 않고 질문으로만 끝낸다)

    Notebook Reference: book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 3: 교육 정책에서 태블릿 지급 여부를 묻는 인과 질문 도입
    - 셀 5: "태블릿과 높은 성적이 함께 있어도 태블릿 덕분이라고 결론 낼 수 없다"
      (원문은 학교 간 비교라서, 다른 학생과 비교하지 않고 한 학생 기준 '다른 이유' 가능성만 가져왔다)

    Script Reference: src/scripts/ko/01_tablet_question.txt

    Asset Reference: Tabler Icons (MIT) — user, device-tablet, trending-up, help

    3Blue1Brown Reference: 3b1b/_2020/covid.py - IntroQuestion
    Reason: 질문 하나를 짧게 띄우고 다음 질문으로 넘기는 인트로 리듬이 쇼츠 첫 장면과 맞아서.

    Script-to-Beat Mapping (01_tablet_question.timings.json, 19.34s):
    1. 청크1 0.00~5.90  "한 학생이 태블릿을 받았습니다. / 그리고 성적이 올랐어요."
       → 학생 등장, 태블릿이 화살표로 전달(1.6s), 성적↑ 등장(3.91s)
    2. 청크2 5.90~8.62  "이건 태블릿 덕분일까요?" → 제목 "태블릿 덕분?" + 태블릿→성적 지름길 화살표와 "?"
    3. 청크3 8.62~14.38 "아직은 알 수 없습니다. / 성적은 다른 이유로도 오를 수 있으니까요."
       → 제목 "아직 모른다" + 지름길 흐려짐, 회색 원인 두 개가 성적으로 들어옴(11.05s)
    4. 청크4 14.38~19.34 "그럼 태블릿의 효과는 / 무엇과 비교해야 알 수 있을까요?"
       → 정리 후 태블릿 강조(15.23s), 제목 "무엇과 비교할까?"(16.81s)
    """

    AUDIO = "01_tablet_question"
    FALLBACK_STARTS = (0.0, 5.90, 8.62, 14.38)
    FALLBACK_TOTAL = 19.34
    END_PAD = 0.55  # 합본 쉼 0.35s + 여유 0.2s

    def construct(self):
        chain = build_chain()

        # ─── Beat 1-a: "한 학생이 태블릿을 받았습니다" (청크1, 발화 1.06~3.21s) ───
        # 남는 요소: 없음 / 새 요소: 학생(가운데), 태블릿(위)과 전달 화살표
        # 비워 두는 영역: 상단 제목 줄, 하단 성적 자리 / 핵심 시선: 태블릿이 학생에게 가는 화살표
        # 첫 1초는 무음이라 학생을 먼저 놓고, "태블릿을"에 맞춰 태블릿을 건넨다.
        self.play(FadeIn(chain.student, scale=0.9), run_time=0.6)
        self.wait_until(self.cue(1, 1.6))
        self.play(FadeIn(chain.tablet, shift=DOWN * 0.2), run_time=0.5)
        self.play(GrowArrow(chain.give), run_time=0.5)

        # ─── Beat 1-b: "그리고 성적이 올랐어요" (발화 3.91~5.72s) ───
        # 남는 요소: 태블릿→학생 / 새 요소: 학생→성적↑ (하단)
        # 비워 두는 영역: 상단 제목 줄 / 핵심 시선: 성적↑
        # 수치 없이 상승 아이콘만 쓴다. 점수는 Scene 02에서 가상 예시로만 등장한다.
        self.wait_until(self.cue(1, 3.91))
        self.play(GrowArrow(chain.lead), run_time=0.4)
        self.play(FadeIn(chain.score, shift=UP * 0.25), run_time=0.6)

        # ─── Beat 2: "이건 태블릿 덕분일까요?" (청크2, 발화 5.96~7.83s) ───
        # 남는 요소: 세로 사슬 / 새 요소: 제목 "태블릿 덕분?"(상단), 태블릿→성적 지름길 화살표와 "?"(오른쪽)
        # 비워 두는 영역: 왼쪽 / 핵심 시선: 오른쪽 지름길 화살표의 "?"
        # 사람들이 흔히 긋는 '태블릿 → 성적' 직결 주장을 화살표 하나로 보여주고, 아직 물음표로 둔다.
        claim = CurvedArrow(
            chain.tablet.get_right() + RIGHT * 0.12,
            chain.score.get_right() + RIGHT * 0.12,
            angle=-TAU / 5,
            color=QUESTION_COLOR,
            stroke_width=4,
            tip_length=0.18,
        )
        mark = ko("?", 54, QUESTION_COLOR).move_to(claim.point_from_proportion(0.5) + RIGHT * 0.3)
        doubt_title = headline("태블릿 덕분?")
        self.wait_until(self.cue(2, 0.06))
        self.play(FadeIn(doubt_title, shift=DOWN * 0.15), Create(claim), run_time=0.8)
        self.play(FadeIn(mark, scale=1.3), run_time=0.4)

        # ─── Beat 3-a: "아직은 알 수 없습니다" (청크3, 발화 8.65~10.35s) ───
        # 남는 요소: 세로 사슬 / 바뀌는 요소: 제목 → "아직 모른다", 지름길 화살표·"?" 흐리게
        # 비워 두는 영역: 왼쪽 / 핵심 시선: 바뀐 제목
        # 성적 상승만으로 효과를 단정하지 않는다는 점을, 지름길 주장을 지우지 않고 흐리게 남겨 보여준다.
        unknown_title = headline("아직 모른다")
        self.wait_until(self.cue(3, 0.03))
        self.play(
            FadeTransform(doubt_title, unknown_title),
            claim.animate.set_color(DIM_COLOR),
            mark.animate.set_color(DIM_COLOR),
            run_time=0.7,
        )

        # ─── Beat 3-b: "성적은 다른 이유로도 오를 수 있으니까요" (발화 11.05~13.86s) ───
        # 남는 요소: 세로 사슬, 흐린 지름길 / 새 요소: 이름 없는 회색 원인 두 개 → 성적 (왼쪽)
        # 비워 두는 영역: 상단 오른쪽 / 핵심 시선: 성적으로 들어오는 회색 점선 화살표
        # 다른 학생이나 구체적 원인을 그리지 않고, "?" 아이콘으로 '다른 이유'의 가능성만 표시한다.
        others = VGroup()
        for spot, aim in ((LEFT * 1.6 + DOWN * 0.55, UP * 0.1), (LEFT * 1.6 + DOWN * 2.4, DOWN * 0.1)):
            cause = icon("help.svg", UNSEEN_COLOR, 0.5).move_to(spot)
            target = chain.score.get_left() + LEFT * 0.2 + aim
            path = DashedLine(
                cause.get_right() + RIGHT * 0.08,
                target,
                dash_length=0.08,
                color=UNSEEN_COLOR,
                stroke_width=3,
            )
            path.add_tip(tip_length=0.14)
            others.add(VGroup(cause, path))
        self.wait_until(self.cue(3, 2.43))
        self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * 0.15) for o in others], lag_ratio=0.35), run_time=0.9)

        # ─── Beat 4: "그럼 태블릿의 효과는 / 무엇과 비교해야 알 수 있을까요?" (청크4, 발화 14.41~19.30s) ───
        # 지워지는 요소: 회색 원인, 흐린 지름길, "아직 모른다" / 남는 요소: 세로 사슬
        # 새 요소: 제목 "무엇과 비교할까?" / 핵심 시선: 제목 질문
        # 답(같은 학생의 두 세계)은 Scene 02의 몫이라, 여기서는 사슬만 남기고 질문으로 끝낸다.
        self.wait_until(self.cue(4, 0.03))
        self.play(FadeOut(others), FadeOut(claim), FadeOut(mark), FadeOut(unknown_title), run_time=0.6)
        self.wait_until(self.cue(4, 0.85))  # "태블릿의 효과는"
        self.play(Wiggle(chain.tablet, scale_value=1.15), run_time=0.9)
        compare_title = headline("무엇과 비교할까?", QUESTION_COLOR)
        self.wait_until(self.cue(4, 2.43))  # "무엇과 비교해야"
        self.play(FadeIn(compare_title, shift=DOWN * 0.15), run_time=0.6)

        self.finish()


class Scene02_TwoWorlds(ShortScene):
    """
    Scene 02: 비교 — 같은 학생이 태블릿을 받은 세계와 받지 않은 세계

    Core Claim:
    태블릿의 효과는 같은 학생의 '받은 세계'와 '받지 않은 세계'의 성적 차이다.

    Expected Misconception:
    받은 학생과 안 받은 다른 학생을 비교하면 된다고 생각하기 쉽다.
    그래서 화면에서는 한 학생 아이콘이 그대로 둘로 갈라져, 두 칸이 같은 사람임을 보여준다.

    Visual Pivot:
    Scene 01의 세로 사슬에서 학생만 남고, 그 학생이 좌우 두 세계 칸으로 갈라진다.
    두 칸 아래 점수 사이에 양방향 화살표가 생기며 "효과"로 이름 붙는다.

    Scene Boundary:
    - 직전 Scene 마지막 문장: "그럼 태블릿의 효과는 무엇과 비교해야 알 수 있을까요?"
    - 현재 Scene 첫 문장: "같은 학생의 두 세계를 비교해야 해요."
    - 다음 Scene 첫 문장: "하지만 현실에선 한쪽 세계만 일어나요." (관찰 불가 이야기는 여기서 하지 않는다)

    Notebook Reference: book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 8: "같은 학생이 태블릿을 받은 세계와 받지 않은 세계", 개별 효과 = 두 결과의 차이 (수식 없이 말로만)
    - 셀 9~10: 멀티버스 가정에서 두 결과를 모두 보는 표. i=4 학생(t=1, y1=750, y0=700)을 점수로 사용

    Script Reference: src/scripts/ko/02_two_worlds.txt

    Asset Reference: Tabler Icons (MIT) — user, device-tablet, device-tablet-off

    3Blue1Brown Reference: 3b1b/_2018/uncertainty.py - TwoCarsAtRedLight
    Reason: 같은 모양의 대상 두 개를 좌우로 나란히 두고 조건 하나만 다르게 비교하는 구성이 두 세계 칸과 같아서.
    Project Reference: videos/why_causal_inference/src/why_causal_inference.py - Scene03_CounterfactualWorlds (세계 칸 구성)

    Script-to-Beat Mapping (02_two_worlds.timings.json, 11.42s):
    1. 청크1 0.00~3.50  "같은 학생의 / 두 세계를 비교해야 해요." → 사슬 정리·제목 교체, 학생이 두 칸으로 갈라짐(1.29s)
    2. 청크2 3.50~7.37  "태블릿을 받은 세계와 / 받지 않은 세계." → 왼쪽 칸 받음(3.53s), 오른쪽 칸 안 받음(5.71s)
    3. 청크3 7.37~11.42 "두 성적의 차이가 / 바로 태블릿의 효과예요." → 두 점수+가상 예시(7.45s), 차이 화살표(8.32s), "효과"(9.73s)
    """

    AUDIO = "02_two_worlds"
    FALLBACK_STARTS = (0.0, 3.50, 7.37)
    FALLBACK_TOTAL = 11.42
    END_PAD = 0.5  # 합본 쉼 0.3s + 여유 0.2s

    def construct(self):
        # 시작 화면 = Scene 01 마지막 화면 (세로 사슬 + "무엇과 비교할까?")
        chain = build_chain()
        old_title = headline("무엇과 비교할까?", QUESTION_COLOR)
        self.add(chain.group, old_title)

        worlds = build_worlds()
        left, right = worlds.left, worlds.right

        # ─── Beat 1-a: "같은 학생의" (청크1, 발화 0.00~1.01s) ───
        # 지워지는 요소: 태블릿, 화살표, 성적↑ / 남는 요소: 학생(가운데)
        # 새 요소: 제목 "같은 학생, 두 세계" / 핵심 시선: 가운데 학생 하나
        title = headline("같은 학생, 두 세계")
        self.play(
            FadeOut(VGroup(chain.tablet, chain.give, chain.lead, chain.score)),
            FadeTransform(old_title, title),
            run_time=0.7,
        )

        # ─── Beat 1-b: "두 세계를 비교해야 해요" (발화 1.29~3.12s) ───
        # 남는 요소: 제목 / 새 요소: 학생 복제본, 좌우 세계 칸(아직 중립 회색)
        # 비워 두는 영역: 점수 줄 / 핵심 시선: 한 학생이 둘로 갈라지는 움직임
        # 다른 학생이 아니라 '같은 학생'임을 보이려고, 새 아이콘을 띄우지 않고 원래 학생을 복제해 가른다.
        twin = chain.student.copy()
        left.frame.set_stroke(GREY_C)
        right.frame.set_stroke(GREY_C)
        self.wait_until(self.cue(1, 1.29))
        self.play(
            ReplacementTransform(chain.student, left.student),
            ReplacementTransform(twin, right.student),
            run_time=0.9,
        )
        self.play(Create(left.frame), Create(right.frame), run_time=0.6)

        # ─── Beat 2-a: "태블릿을 받은 세계와" (청크2, 발화 3.53~5.37s) ───
        # 새 요소: 왼쪽 칸 청록 테두리 + 태블릿 아이콘 + "받음" / 핵심 시선: 왼쪽 칸
        self.wait_until(self.cue(2, 0.03))
        self.play(
            left.frame.animate.set_stroke(TABLET_COLOR),
            FadeIn(left.badge, shift=DOWN * 0.15),
            FadeIn(left.tag),
            run_time=0.6,
        )

        # ─── Beat 2-b: "받지 않은 세계" (발화 5.71~6.82s) ───
        # 새 요소: 오른쪽 칸 금색 테두리 + 꺼진 태블릿 아이콘 + "안 받음" / 핵심 시선: 오른쪽 칸
        self.wait_until(self.cue(2, 2.21))
        self.play(
            right.frame.animate.set_stroke(NO_TABLET_COLOR),
            FadeIn(right.badge, shift=DOWN * 0.15),
            FadeIn(right.tag),
            run_time=0.6,
        )

        # ─── Beat 3-a: "두 성적의 차이가" (청크3, 발화 7.45~8.90s) ───
        # 남는 요소: 두 세계 칸 / 새 요소: 칸 아래 두 점수, "가상 예시" 표시, 점수 사이 양방향 화살표
        # 비워 두는 영역: 상단 / 핵심 시선: 두 점수
        # 점수는 노트북 셀 10의 i=4 학생 값이며, 실제 데이터가 아니므로 "가상 예시"를 같이 띄운다.
        self.wait_until(self.cue(3, 0.08))
        self.play(
            FadeIn(VGroup(worlds.score_l, worlds.score_r), shift=UP * 0.15),
            FadeIn(worlds.example_tag),
            run_time=0.6,
        )
        self.wait_until(self.cue(3, 0.95))
        self.play(GrowFromCenter(worlds.effect), run_time=0.5)

        # ─── Beat 3-b: "바로 태블릿의 효과예요" (발화 9.18~11.10s) ───
        # 새 요소: 화살표 아래 "효과" / 핵심 시선: "효과"
        # 수식 대신 '차이 화살표 + 효과' 라벨로 개별 효과를 표현한다.
        self.wait_until(self.cue(3, 2.36))
        self.play(FadeIn(worlds.effect_label, shift=UP * 0.1), run_time=0.5)

        self.finish()


class Scene03_OneWorldObserved(ShortScene):
    """
    Scene 03: 핵심 — 실제로는 한쪽 결과만 관찰할 수 있다

    Core Claim:
    현실에서는 한쪽 세계만 일어난다. 실제로 태블릿을 받았다면,
    받지 않았을 때의 결과는 관찰할 수 없고, 이것을 반사실이라고 부른다.

    Expected Misconception:
    Scene 02의 두 점수를 실제로 둘 다 볼 수 있다고 생각하기 쉽다.

    Visual Pivot:
    Scene 02의 두 세계 화면에서 차이 화살표가 사라지고, 받지 않은 세계가 어두워진다.
    그 세계의 점수가 "눈 가림 + ?"로 바뀐 뒤 "반사실"이라는 이름이 붙는다.

    Scene Boundary:
    - 직전 Scene 마지막 문장: "두 성적의 차이가 바로 태블릿의 효과예요."
    - 현재 Scene 첫 문장: "하지만 현실에선 한쪽 세계만 일어나요."
    - 다음 Scene: 없음 (마지막 Scene)

    Notebook Reference: book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 8: 둘 중 하나의 현실만 존재, 실제로 일어난 쪽은 사실 / 일어나지 않은 쪽은 반사실
    - 셀 13: 현실 표에서 처치받은 학생(i=4)의 y0는 NaN → 화면에서는 '관찰 불가'(눈 가림 + ?)로 표현

    Script Reference: src/scripts/ko/03_one_world_observed.txt

    Asset Reference: Tabler Icons (MIT) — user, device-tablet, device-tablet-off, eye-off

    3Blue1Brown Reference: 3b1b/_2018/uncertainty.py - TwoCarsAtRedLight
    Reason: Scene 02와 같은 좌우 비교 구도를 유지한 채 한쪽만 바꾸는 흐름이라 같은 참조를 이어 쓴다.
    Project Reference: videos/why_causal_inference/src/why_causal_inference.py - Scene03_CounterfactualWorlds (반사실 칸 흐리기, eye-off)

    Script-to-Beat Mapping (03_one_world_observed.timings.json, 13.37s):
    1. 청크1 0.00~3.77  "하지만 현실에선 / 한쪽 세계만 일어나요." → 차이 화살표 정리·제목 교체, 받지 않은 세계 어둡게(1.66s)
    2. 청크2 3.77~9.22  "실제로 태블릿을 받았다면, / 받지 않았을 때의 결과는 볼 수 없어요."
       → 왼쪽 칸 강조 + "실제"(3.82s), 오른쪽 점수 → 눈 가림 + ?(6.44s)
    3. 청크3 9.22~13.37 "이 보이지 않는 결과를 / 반사실이라고 불러요." → ? 강조(9.26s), "반사실"(11.44s)
    """

    AUDIO = "03_one_world_observed"
    FALLBACK_STARTS = (0.0, 3.77, 9.22)
    FALLBACK_TOTAL = 13.37
    END_PAD = 0.8  # 마지막 정지 화면 0.6s + 여유 0.2s

    def construct(self):
        # 시작 화면 = Scene 02 마지막 화면 (두 세계 + 두 점수 + 효과)
        worlds = build_worlds()
        left, right = worlds.left, worlds.right
        old_title = headline("같은 학생, 두 세계")
        self.add(old_title, worlds.group)

        # ─── Beat 1-a: "하지만 현실에선" (청크1, 발화 0.00~1.38s) ───
        # 지워지는 요소: 차이 화살표, "효과" / 남는 요소: 두 세계, 두 점수, 가상 예시
        # 새 요소: 제목 "현실은 한 세계뿐" / 핵심 시선: 제목
        # 두 점수를 다 볼 수 없으니 차이(효과)도 바로 구할 수 없다. 그래서 효과 표시부터 걷어낸다.
        title = headline("현실은 한 세계뿐")
        self.play(
            FadeOut(VGroup(worlds.effect, worlds.effect_label)),
            FadeTransform(old_title, title),
            run_time=0.7,
        )

        # ─── Beat 1-b: "한쪽 세계만 일어나요" (발화 1.66~3.22s) ───
        # 바뀌는 요소: 오른쪽(받지 않은) 세계 전체를 어두운 회색으로 / 핵심 시선: 밝게 남은 왼쪽 세계
        # 학생 모양은 그대로 두고 색만 낮춰, 같은 학생의 '일어나지 않은' 세계임을 유지한다.
        self.wait_until(self.cue(1, 1.66))
        self.play(
            right.group.animate.set_color(DIM_COLOR),
            worlds.score_r.animate.set_color(DIM_COLOR),
            run_time=0.8,
        )

        # ─── Beat 2-a: "실제로 태블릿을 받았다면" (청크2, 발화 3.82~5.93s) ───
        # 새 요소: 왼쪽 칸 테두리 굵게 + 왼쪽 점수 아래 "실제" / 핵심 시선: 왼쪽 칸
        real_tag = ko("실제", 28, TABLET_COLOR).move_to([-PANEL_X, NOTE_Y, 0])
        self.wait_until(self.cue(2, 0.05))
        self.play(
            left.frame.animate.set_stroke(width=6),
            FadeIn(real_tag, shift=UP * 0.1),
            run_time=0.6,
        )

        # ─── Beat 2-b: "받지 않았을 때의 결과는 볼 수 없어요" (발화 6.44~8.88s) ───
        # 바뀌는 요소: 오른쪽 점수 "700점" → 눈 가림 아이콘 + "?" / 핵심 시선: 오른쪽 "?"
        # 노트북 표의 NaN처럼 '비어 있음'이 아니라 '관찰할 수 없음'으로 읽히도록 eye-off 아이콘을 붙인다.
        hidden = VGroup(icon("eye-off.svg", UNSEEN_COLOR, 0.42), ko("?", 44, UNSEEN_COLOR))
        hidden.arrange(RIGHT, buff=0.14).move_to([PANEL_X, SCORE_Y, 0])
        self.wait_until(self.cue(2, 2.67))
        self.play(FadeTransform(worlds.score_r, hidden), run_time=0.7)

        # ─── Beat 3-a: "이 보이지 않는 결과를" (청크3, 발화 9.26~11.07s) ───
        # 새 요소: "?" 주위를 잠깐 도는 강조선 / 핵심 시선: 오른쪽 "?"
        self.wait_until(self.cue(3, 0.04))
        self.play(Circumscribe(hidden, color=QUESTION_COLOR, buff=0.12), run_time=1.0)

        # ─── Beat 3-b: "반사실이라고 불러요" (발화 11.44~13.07s) ───
        # 새 요소: 오른쪽 "?" 아래 "반사실" / 핵심 시선: "반사실"
        # 왼쪽 "실제"와 같은 줄에 두어, 사실/반사실이 한 학생의 두 결과라는 대비로 끝낸다.
        counter_tag = ko("반사실", 32, QUESTION_COLOR).move_to([PANEL_X, NOTE_Y, 0])
        self.wait_until(self.cue(3, 2.22))
        self.play(FadeIn(counter_tag, shift=UP * 0.1), run_time=0.6)

        self.finish()
