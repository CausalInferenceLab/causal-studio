"""
단순 비교의 함정 — 녹내장 복합제는 정말 효과가 없을까? (한국어, 세로형 9:16)

수치 출처: 이 영상용 시뮬레이션 노트북의 실행 결과 (Scene 02부터 사용)
모든 수치는 가상 시뮬레이션 데이터이며, 수치가 나오는 화면에는 "가상 데이터"를 표시한다.

렌더 예시 (저해상도 확인용, 작업 폴더 기준):
    ../../.venv/Scripts/manim.exe -ql --media_dir build/manim src/psm_glaucoma.py Scene01_Opening
"""

import json
from pathlib import Path

from manim import *

# 이 영상 전용 9:16 세로 설정. 다른 영상의 config에는 영향을 주지 않는다.
# 프레임 9 x 16 단위, 540 x 960 px => 1단위 = 60px.
config.frame_width = 9.0
config.frame_height = 16.0
# 확인용(-ql 등 가로 기본값)이면 540 x 960. 최종 렌더처럼 CLI에서 세로 해상도(-r 720,1280)를 주면 그대로 둔다.
if config.pixel_width > config.pixel_height:
    config.pixel_width = 540
    config.pixel_height = 960
config.background_color = BLACK

FONT = "Noto Sans KR"

# 색상 의미 (Scene 간 공통, 노트북과 같은 배정)
MONO = "#3987e5"     # 단일제(PGA): 파랑
COMBO = "#eb6834"    # 복합제(PGA + timolol): 주황
GOOD = "#1baf7a"     # 목표 도달·균형: 초록
QUESTION = YELLOW_E  # 질문·강조: 노랑
INK = "#f0efec"      # 기본 글자·환자·눈
MUTED = "#8a8984"    # 보조 라벨·화살표

ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
TOPIC_DIR = Path(__file__).resolve().parents[1]


def load_icon(filename: str, color: str, height: float) -> SVGMobject:
    icon = SVGMobject(str(ASSET_DIR / filename))
    icon.set_stroke(color=color, width=6, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def make_label(text: str, color: str = INK, font_size: float = 48, weight=BOLD) -> Text:
    return Text(text, font=FONT, font_size=font_size, color=color, weight=weight)


def make_bottle(color: str, height: float = 2.4) -> SVGMobject:
    """점안약 병. 단일제·복합제 모두 같은 모양, 색으로만 구분한다."""
    return load_icon("vaccine-bottle.svg", color, height)


def make_drops(colors: list[str], height: float = 0.75) -> VGroup:
    """성분 수를 물방울 개수로 표시한다 (단일제 1개, 복합제 2개)."""
    return VGroup(*[load_icon("droplet.svg", c, height) for c in colors]).arrange(RIGHT, buff=0.2)


def make_patients(color: str, height: float = 2.0) -> SVGMobject:
    """환자 무리. 모든 Scene에서 같은 users 아이콘을 쓰고, 처방받은 약의 색으로 칠한다."""
    return load_icon("users.svg", color, height)


def virtual_tag() -> Text:
    """수치가 나오는 화면에 붙이는 표시 (오른쪽 아래 고정)."""
    return make_label("가상 데이터", MUTED, 26, NORMAL).to_corner(DR, buff=0.5)


def load_numbers() -> dict:
    """notebooks/psm_simulation_ko.ipynb 가 내보낸 수치. 영상의 모든 숫자는 여기서 읽는다."""
    return json.loads((TOPIC_DIR / "data" / "psm_numbers.json").read_text(encoding="utf-8"))


def pct(value: float) -> int:
    """화면 퍼센트 표기. 내레이션과 같게 사사오입한다 (파이썬 round는 72.5 -> 72)."""
    return int(value + 0.5)


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


class Scene01_Opening(TimedScene):
    """
    Scene 01: 오프닝 — 녹내장 안약에는 단일제와 복합제가 있는데, 어느 쪽이 더 효과적일까?

    Notebook Reference:
    book/psm_glaucoma/psm_glaucoma_ko.ipynb
    - 셀 0: 제목과 질문
    - 셀 1: 상황 설정 (단일제 PGA / 복합제 PGA + timolol, 병원 기록으로 비교)

    Script Reference:
    src/scripts/ko/01_opening.txt
    직전 Scene 마지막 문장: 없음 (첫 Scene)
    다음 Scene으로 넘기는 것: 목표 안압 18 mmHg, 도달률 막대 (여기서는 보여주지 않는다)

    Script-to-Beat Mapping (timings.json 기준, 청크 안 문장 시작은 글자 수 비율로 추정):
    청크 1 (0.00~10.20s)
      "녹내장은 시신경이 조금씩 손상되는 눈 질환이에요." -> 눈 아이콘(중앙 위), `녹내장`
      "치료의 핵심은 눈 속 압력, 즉 안압을 낮추는 거예요." -> 압력계 아이콘 + 아래 화살표, `안압 ↓`
    청크 2 (10.20~19.32s)
      "안압을 낮추는 안약은 크게 두 가지가 있어요." -> 눈·압력계를 지우고 점안약 병 2개 (파랑·주황)
      "성분이 하나인 단일제," -> 왼쪽 병 아래 물방울 1개, `단일제` / `PGA`
      "그리고 두 성분을 합친 복합제입니다." -> 오른쪽 병 아래 물방울 2개, `복합제` / `PGA + timolol`
    청크 3 (19.32~26.83s)
      "그렇다면 둘 중 어느 쪽이 더 효과적일까요?" -> 두 병 사이 큰 `?`, 상단 `어느 쪽이 더 효과적?`
      "병원 기록으로 한번 알아봅시다." -> 하단에 기록 아이콘, `병원 기록`
    """

    # 승인된 음성(26.83s)보다 화면이 약간 늦게 끝나도록 여백을 둔다.
    WAIT_TAIL = 0.7

    def construct(self):
        d1, d2, d3 = load_chunk_durations("01_opening", [10.2, 9.12, 7.512])
        t_c2 = d1
        t_c3 = d1 + d2
        t_end = d1 + d2 + d3
        # 청크 안 두 번째 문장 시작 시점 (글자 수 비율로 추정)
        t_iop = d1 * 0.44                      # "치료의 핵심은 ..."
        t_mono = t_c2 + d2 * 0.45              # "성분이 하나인 단일제"
        t_combo = t_c2 + d2 * 0.72             # "그리고 두 성분을 합친 복합제"
        t_record = t_c3 + d3 * 0.58            # "병원 기록으로 ..."

        # ─── Beat 1: 청크 1 앞 문장 — 녹내장은 눈 질환 ───
        # 화면 구획: 상단 제목 / 중앙 위 눈 / 중앙 아래 비움
        # 단일 시선 대상: 눈 아이콘
        title = make_label("녹내장", INK, 64).move_to(UP * 5.6)
        eye = load_icon("eye.svg", INK, 2.8).move_to(UP * 1.6)
        eye_note = make_label("시신경 손상", MUTED, 36, NORMAL).next_to(eye, DOWN, buff=0.35)

        self.play_t(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
        self.play_t(FadeIn(eye, scale=0.9), run_time=0.9)
        self.play_t(FadeIn(eye_note), run_time=0.5)

        # ─── Beat 2: 청크 1 뒤 문장 — 치료의 핵심은 안압을 낮추는 것 ───
        # 남는 요소: 제목, 눈
        # 새로 등장: 압력계 + 아래 화살표(중앙 아래), `안압 ↓`
        # 단일 시선 대상: 압력계와 아래 화살표
        self.wait_until(t_iop)
        gauge = load_icon("gauge.svg", INK, 2.2)
        down_arrow = Arrow(UP * 0.9, DOWN * 0.9, buff=0, stroke_width=14, max_stroke_width_to_length_ratio=10,
                           max_tip_length_to_length_ratio=0.35, color=GOOD)
        iop_group = VGroup(gauge, down_arrow).arrange(RIGHT, buff=0.5).move_to(DOWN * 2.8)
        iop_label = make_label("안압 ↓", GOOD, 56).next_to(iop_group, DOWN, buff=0.45)

        self.play_t(FadeIn(gauge, shift=UP * 0.2), run_time=0.8)
        self.play_t(GrowArrow(down_arrow), FadeIn(iop_label), run_time=0.8)
        self.wait_until(t_c2)

        # ─── Beat 3: 청크 2 앞 문장 — 안압을 낮추는 안약은 두 가지 ───
        # 먼저 지울 것: 눈, 시신경 라벨, 압력계, 화살표 (시선 경쟁 제거)
        # 제목 교체: `녹내장` -> `안압을 낮추는 안약`
        # 새로 등장: 점안약 병 2개 (왼쪽 파랑, 오른쪽 주황)
        # 단일 시선 대상: 두 병
        title2 = make_label("안압을 낮추는 안약", INK, 56).move_to(title)
        mono_bottle = make_bottle(MONO).move_to(LEFT * 2.6 + UP * 0.9)
        combo_bottle = make_bottle(COMBO).move_to(RIGHT * 2.6 + UP * 0.9)

        self.play_t(
            FadeOut(eye), FadeOut(eye_note), FadeOut(gauge), FadeOut(down_arrow), FadeOut(iop_label),
            ReplacementTransform(title, title2),
            run_time=0.8,
        )
        self.play_t(
            FadeIn(mono_bottle, shift=RIGHT * 0.3), FadeIn(combo_bottle, shift=LEFT * 0.3),
            run_time=0.9,
        )

        # ─── Beat 4: 청크 2 뒤 문장 앞부분 — 성분이 하나인 단일제 ───
        # 새로 등장: 왼쪽 병 아래 물방울 1개, `단일제` / `PGA`
        self.wait_until(t_mono)
        mono_drops = make_drops([MONO]).next_to(mono_bottle, DOWN, buff=0.45)
        mono_label = VGroup(
            make_label("단일제", MONO, 52),
            make_label("PGA", MUTED, 32, NORMAL),
        ).arrange(DOWN, buff=0.15).next_to(mono_drops, DOWN, buff=0.4)
        self.play_t(FadeIn(mono_drops, shift=DOWN * 0.2), FadeIn(mono_label), run_time=0.8)

        # ─── Beat 5: 청크 2 뒤 문장 뒷부분 — 두 성분을 합친 복합제 ───
        # 새로 등장: 오른쪽 병 아래 물방울 2개, `복합제` / `PGA + timolol`
        # 물방울 높이를 왼쪽과 맞춰 좌우 대칭을 유지한다.
        self.wait_until(t_combo)
        combo_drops = make_drops([COMBO, COMBO]).next_to(combo_bottle, DOWN, buff=0.45)
        combo_label = VGroup(
            make_label("복합제", COMBO, 52),
            make_label("PGA + timolol", MUTED, 32, NORMAL),
        ).arrange(DOWN, buff=0.15).next_to(combo_drops, DOWN, buff=0.4)
        combo_label.align_to(mono_label, UP)
        self.play_t(FadeIn(combo_drops, shift=DOWN * 0.2), FadeIn(combo_label), run_time=0.8)
        self.wait_until(t_c3)

        # ─── Beat 6: 청크 3 앞 문장 — 어느 쪽이 더 효과적일까? ───
        # 남는 요소: 두 병, 물방울, 라벨
        # 제목 교체: `안압을 낮추는 안약` -> `어느 쪽이 더 효과적?`
        # 새로 등장: 두 병 사이 큰 `?`
        # 단일 시선 대상: 물음표
        title3 = make_label("어느 쪽이 더 효과적?", QUESTION, 56).move_to(title2)
        question = Text("?", font=FONT, font_size=170, color=QUESTION, weight=BOLD)
        question.move_to(VGroup(mono_bottle, combo_bottle).get_center())
        self.play_t(ReplacementTransform(title2, title3), FadeIn(question, scale=0.6), run_time=0.9)

        # ─── Beat 7: 청크 3 뒤 문장 — 병원 기록으로 알아보자 ───
        # 새로 등장: 하단 기록 아이콘, `병원 기록` (Scene 02에서 데이터 비교로 이어질 자리)
        # 비워 두는 영역: 최하단 안전 영역
        self.wait_until(t_record)
        record = load_icon("clipboard-text.svg", INK, 1.8).move_to(DOWN * 5.0)
        record_label = make_label("병원 기록", INK, 40).next_to(record, DOWN, buff=0.3)
        self.play_t(FadeIn(record, shift=UP * 0.3), FadeIn(record_label), run_time=0.8)
        self.play_t(Indicate(question, color=QUESTION, scale_factor=1.15), run_time=1.0)

        self.wait_until(t_end + self.WAIT_TAIL)


class Scene02_NaiveComparison(TimedScene):
    """
    Scene 02: 단순 비교 — 그냥 비교하면 복합제의 목표 도달률이 더 낮지만, 이것만으로 단정할 수 없다.

    Notebook Reference:
    notebooks/psm_simulation_ko.ipynb
    - "1. 가상 환자 만들기": 환자 수 (data/psm_numbers.json 의 n)
    - "2. 단순 비교": 목표 안압 도달률 (naive_reach_pct)
    book/psm_glaucoma/psm_glaucoma_ko.ipynb 셀 6~8 (단순 비교와 "이상한 결과") 구성 참고

    Script Reference:
    src/scripts/ko/02_naive_comparison.txt
    직전 Scene 마지막 문장: "병원 기록으로 한번 알아봅시다."
    현재 Scene 첫 문장: "가상으로 만든 환자 2천 명의 기록을 살펴볼게요."
    다음 Scene으로 넘기는 것: 기저 안압 차이와 출발선 (여기서는 말하지 않는다)

    Script-to-Beat Mapping (timings.json 기준, 청크 안 문장 시작은 글자 수 비율로 추정):
    청크 1 (0.00~9.50s)
      "가상으로 만든 환자 2천 명의 기록을 살펴볼게요." -> 기록 아이콘 + `가상 환자 2,000명`, 환자 무리 2개(파랑·주황)와 인원 수
      "6개월 뒤 안압이 18 이하, 목표치까지 내려간 비율을 비교합니다." -> 하단 압력계 + `6개월 후 목표: 18 mmHg 이하`
    청크 2 (9.50~16.56s)
      "목표에 도달한 환자는 단일제가 73퍼센트, 복합제는 56퍼센트였어요." -> 막대그래프 2개가 차례로 자람, `73%` / `56%`
    청크 3 (16.56~28.13s)
      "성분이 두 개인데 오히려 더 낮죠." -> 주황 막대 강조
      "그럼 복합제가 더 효과가 없는 걸까요?" -> 하단에 노란 `복합제가 더 효과가 없다?`
      "이 숫자만으로 단정하기엔 아직 일러요." -> 문구에 회색 취소선, 아래 `아직 단정 X`
    가상 데이터 표시: 인원 수가 처음 나오는 순간부터 끝까지 오른쪽 아래에 유지
    """

    WAIT_TAIL = 0.7
    BASE_Y = -2.4        # 막대 바닥선 높이
    FULL_H = 5.6         # 100% 막대 높이
    BAR_X = 1.7          # 막대 중심의 좌우 거리
    BAR_W = 1.7

    def construct(self):
        nums = load_numbers()
        n_mono, n_combo = nums["n"]["mono"], nums["n"]["combo"]
        reach_mono = pct(nums["naive_reach_pct"]["mono"])
        reach_combo = pct(nums["naive_reach_pct"]["combo"])
        target = nums["target_iop"]

        d1, d2, d3 = load_chunk_durations("02_naive_comparison", [9.504, 7.056, 11.568])
        t_c2 = d1
        t_c3 = d1 + d2
        t_end = d1 + d2 + d3
        t_target = d1 * 0.43                  # "6개월 뒤 안압이 18 이하 ..."
        t_claim = t_c3 + d3 * 0.30            # "그럼 복합제가 더 효과가 없는 걸까요?"
        t_doubt = t_c3 + d3 * 0.65            # "이 숫자만으로 단정하기엔 아직 일러요."

        # ─── Beat 1: 청크 1 앞 문장 — 가상 환자 2천 명의 기록 ───
        # 화면 구획: 상단 제목(기록 아이콘 + 문구) / 중앙 환자 무리 좌우 / 하단 비움
        # 단일 시선 대상: 파랑·주황 환자 무리
        record = load_icon("clipboard-text.svg", INK, 0.9)
        header_text = make_label(f"가상 환자 {n_mono + n_combo:,}명", INK, 54)
        header = VGroup(record, header_text).arrange(RIGHT, buff=0.3).move_to(UP * 5.6)
        tag = virtual_tag()

        mono_group = make_patients(MONO).move_to(LEFT * 2.2 + UP * 2.0)
        combo_group = make_patients(COMBO).move_to(RIGHT * 2.2 + UP * 2.0)
        mono_n = VGroup(make_label("단일제", MONO, 44), make_label(f"{n_mono:,}명", INK, 36, NORMAL))
        mono_n.arrange(DOWN, buff=0.15).next_to(mono_group, DOWN, buff=0.35)
        combo_n = VGroup(make_label("복합제", COMBO, 44), make_label(f"{n_combo:,}명", INK, 36, NORMAL))
        combo_n.arrange(DOWN, buff=0.15).next_to(combo_group, DOWN, buff=0.35)

        self.play_t(FadeIn(header, shift=DOWN * 0.2), FadeIn(tag), run_time=0.8)
        self.play_t(
            FadeIn(mono_group, shift=RIGHT * 0.3), FadeIn(combo_group, shift=LEFT * 0.3),
            FadeIn(mono_n), FadeIn(combo_n),
            run_time=1.0,
        )

        # ─── Beat 2: 청크 1 뒤 문장 — 6개월 뒤 목표 안압 18 이하 ───
        # 남는 요소: 제목, 환자 무리
        # 새로 등장: 하단 압력계 + 목표 문구
        # 단일 시선 대상: 목표 문구
        self.wait_until(t_target)
        gauge = load_icon("gauge.svg", GOOD, 1.4)
        goal = VGroup(
            make_label("6개월 후 목표", INK, 40, NORMAL),
            make_label(f"안압 {target} mmHg 이하", GOOD, 48),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        goal_group = VGroup(gauge, goal).arrange(RIGHT, buff=0.4).move_to(DOWN * 3.2)
        self.play_t(FadeIn(gauge, shift=UP * 0.2), FadeIn(goal), run_time=0.9)
        self.wait_until(t_c2)

        # ─── Beat 3: 청크 2 — 도달률 막대그래프 ───
        # 먼저 지울 것: 환자 무리, 인원 수, 압력계 (막대와 시선 경쟁)
        # 제목 교체: `가상 환자 2,000명` -> `6개월 후 목표 도달률`
        # 새로 등장: 바닥선, 파랑 막대 -> 주황 막대 (말하는 순서대로)
        # 단일 시선 대상: 자라는 막대와 숫자
        title2 = make_label("6개월 후 목표 도달률", INK, 54).move_to(header)
        base = Line(
            [-(self.BAR_X + self.BAR_W), self.BASE_Y, 0], [self.BAR_X + self.BAR_W, self.BASE_Y, 0],
            color=MUTED, stroke_width=3,
        )

        def bar(value: float, color: str, x: float) -> RoundedRectangle:
            h = self.FULL_H * value / 100
            r = RoundedRectangle(width=self.BAR_W, height=h, corner_radius=0.1,
                                 color=color, fill_opacity=1, stroke_width=0)
            return r.move_to([x, self.BASE_Y + h / 2, 0])

        mono_bar = bar(reach_mono, MONO, -self.BAR_X)
        combo_bar = bar(reach_combo, COMBO, self.BAR_X)
        mono_val = make_label(f"{reach_mono}%", INK, 56).next_to(mono_bar, UP, buff=0.25)
        combo_val = make_label(f"{reach_combo}%", INK, 56).next_to(combo_bar, UP, buff=0.25)
        mono_cat = make_label("단일제", MONO, 44).move_to([-self.BAR_X, self.BASE_Y - 0.55, 0])
        combo_cat = make_label("복합제", COMBO, 44).move_to([self.BAR_X, self.BASE_Y - 0.55, 0])

        self.play_t(
            FadeOut(mono_group), FadeOut(combo_group), FadeOut(mono_n), FadeOut(combo_n),
            FadeOut(goal_group), ReplacementTransform(header, title2),
            run_time=0.8,
        )
        self.play_t(Create(base), FadeIn(mono_cat), FadeIn(combo_cat), run_time=0.5)
        # "단일제가 73퍼센트"
        self.play_t(GrowFromEdge(mono_bar, DOWN), run_time=1.0)
        self.play_t(FadeIn(mono_val, shift=UP * 0.2), run_time=0.4)
        # "복합제는 56퍼센트였어요" (청크 2 후반)
        self.wait_until(t_c2 + d2 * 0.55)
        self.play_t(GrowFromEdge(combo_bar, DOWN), run_time=1.0)
        self.play_t(FadeIn(combo_val, shift=UP * 0.2), run_time=0.4)
        self.wait_until(t_c3)

        # ─── Beat 4: 청크 3 앞 문장 — 성분이 두 개인데 오히려 더 낮다 ───
        # 남는 요소: 막대그래프 전체
        # 단일 시선 대상: 주황 막대 (단일제 막대는 흐리게)
        self.play_t(
            mono_bar.animate.set_opacity(0.35), mono_val.animate.set_opacity(0.5),
            Indicate(combo_val, color=COMBO, scale_factor=1.25),
            run_time=1.0,
        )

        # ─── Beat 5: 청크 3 가운데 문장 — "복합제가 더 효과가 없다?" ───
        # 새로 등장: 하단 노란 질문 문구 (바닥선·약 이름 아래)
        self.wait_until(t_claim)
        claim = make_label("복합제가 더 효과가 없다?", QUESTION, 44).move_to(DOWN * 4.6)
        self.play_t(FadeIn(claim, shift=UP * 0.2), run_time=0.8)

        # ─── Beat 6: 청크 3 끝 문장 — 이 숫자만으로 단정하기엔 아직 이르다 ───
        # 새로 등장: 질문 문구 위 회색 취소선, 아래 `아직 단정 X`
        # 단일 시선 대상: `아직 단정 X`
        self.wait_until(t_doubt)
        strike = Line(claim.get_left() + LEFT * 0.1, claim.get_right() + RIGHT * 0.1,
                      color=MUTED, stroke_width=6)
        verdict = make_label("아직 단정 X", INK, 48).next_to(claim, DOWN, buff=0.5)
        self.play_t(Create(strike), claim.animate.set_opacity(0.55), run_time=0.6)
        self.play_t(FadeIn(verdict, scale=0.9), run_time=0.6)

        self.wait_until(t_end + self.WAIT_TAIL)


class Scene03_BaselineClue(TimedScene):
    """
    Scene 03: 반전의 단서 — 복합제 환자는 처음부터 안압이 높아 출발선이 달랐지만, 중간 구간에서는 두 약의 환자가 겹친다.

    Notebook Reference:
    notebooks/psm_simulation_ko.ipynb
    - "3. 기저 안압 분포와 겹침": baseline_iop_mean, iop0_hist.before, overlap_21_28
    book/psm_glaucoma/psm_glaucoma_ko.ipynb 셀 9~11 (반전의 단서) 구성 참고

    Script Reference:
    src/scripts/ko/03_baseline_clue.txt
    직전 Scene 마지막 문장: "이 숫자만으로 단정하기엔 아직 일러요."
    현재 Scene 첫 문장: "단서는 약을 쓰기 전의 안압, 기저 안압에 있어요."
    다음 Scene으로 넘기는 것: `교란` 용어와 화살표 그림(DAG) (여기서는 쓰지 않는다)

    Script-to-Beat Mapping (timings.json 기준, 청크 안 문장 시작은 글자 수 비율로 추정):
    청크 1 (0.00~9.60s)
      "단서는 약을 쓰기 전의 안압, 기저 안압에 있어요." -> 제목 `기저 안압` / `약 쓰기 전`, 가로 눈금
      "평균을 보면 단일제는 21, 복합제는 약 29예요." -> 눈금 위 파랑 `21.0`, 주황 `28.9` 표시가 차례로
    청크 2 (9.60~24.60s)
      "의사는 안압이 높은 환자에게 복합제를 주곤 해요." -> 환자 무리가 각자 기저 안압 높이(세로 위치)에 등장
      "복합제 환자는 처음부터 더 높은 곳에서 출발한 거죠." -> 주황 출발선 강조, 제목 `출발선이 다르다`
      "출발선이 높으면, 약이 잘 들어도 18까지 내려오기 어렵습니다." -> 초록 점선 `목표 18`, 출발선에서 목표선까지 아래 화살표
    청크 3 (24.60~39.17s)
      "그런데 두 분포를 겹쳐 보면, 21에서 28 사이에는 두 약의 환자가 모두 있어요." -> 분포 막대 2개 겹침, 21~28 노란 띠 `겹치는 구간`
      "같은 안압이어도 어떤 환자는 단일제를, 어떤 환자는 복합제를 받은 거예요." -> 띠 아래 구간 환자 수
    가상 데이터 표시: 처음부터 끝까지 오른쪽 아래
    """

    WAIT_TAIL = 0.7

    def construct(self):
        nums = load_numbers()
        mean_mono = nums["baseline_iop_mean"]["mono"]
        mean_combo = nums["baseline_iop_mean"]["combo"]
        target = nums["target_iop"]
        hist = nums["iop0_hist"]
        overlap = nums["overlap_21_28"]

        d1, d2, d3 = load_chunk_durations("03_baseline_clue", [9.6, 15.0, 14.568])
        t_c2 = d1
        t_c3 = d1 + d2
        t_end = d1 + d2 + d3
        t_means = d1 * 0.49                    # "평균을 보면 ..."
        t_start = t_c2 + d2 * 0.30             # "복합제 환자는 처음부터 ..."
        t_hard = t_c2 + d2 * 0.62              # "출발선이 높으면 ..."
        t_counts = t_c3 + d3 * 0.53            # "같은 안압이어도 ..."

        tag = virtual_tag()

        # ─── Beat 1: 청크 1 — 기저 안압 평균 ───
        # 화면 구획: 상단 제목 / 중앙 가로 눈금(14~36 mmHg) / 하단 비움
        # 단일 시선 대상: 눈금 위 두 평균 표시
        title = VGroup(
            make_label("기저 안압", INK, 60),
            make_label("약 쓰기 전", MUTED, 36, NORMAL),
        ).arrange(DOWN, buff=0.2).move_to(UP * 5.4)

        axis = NumberLine(x_range=[14, 36, 2], length=7.6, color=MUTED, include_ticks=True,
                          tick_size=0.08, stroke_width=3).move_to(UP * 0.5)
        axis_nums = VGroup(*[
            make_label(str(v), MUTED, 28, NORMAL).next_to(axis.n2p(v), DOWN, buff=0.25)
            for v in (14, 20, 26, 32)
        ])
        axis_unit = make_label("mmHg", MUTED, 26, NORMAL).next_to(axis, DOWN, buff=0.8).align_to(axis, RIGHT)

        def mean_marker(v: float, color: str, name: str) -> VGroup:
            tri = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.22).rotate(PI)
            tri.next_to(axis.n2p(v), UP, buff=0.08)
            val = make_label(f"{v:.1f}", color, 52).next_to(tri, UP, buff=0.2)
            who = make_label(name, color, 34, NORMAL).next_to(val, UP, buff=0.12)
            return VGroup(tri, val, who)

        mono_mark = mean_marker(mean_mono, MONO, "단일제")
        combo_mark = mean_marker(mean_combo, COMBO, "복합제")

        self.play_t(FadeIn(title, shift=DOWN * 0.2), FadeIn(tag), run_time=0.8)
        self.play_t(Create(axis), FadeIn(axis_nums), FadeIn(axis_unit), run_time=1.0)
        # "단일제는 21"
        self.wait_until(t_means)
        self.play_t(FadeIn(mono_mark, shift=DOWN * 0.3), run_time=0.7)
        # "복합제는 약 29예요"
        self.wait_until(t_means + 2.0)
        self.play_t(FadeIn(combo_mark, shift=DOWN * 0.3), run_time=0.7)
        self.wait_until(t_c2)

        # ─── Beat 2: 청크 2 첫 문장 — 안압이 높은 환자가 복합제를 받는다 ───
        # 먼저 지울 것: 가로 눈금과 평균 표시
        # 새로 등장: 각자 기저 안압 높이에 선 환자 무리 (세로 위치 = 안압)
        # 단일 시선 대상: 높이가 다른 두 환자 무리
        def lvl(v: float) -> float:           # 세로 안압 눈금: 18 mmHg -> y=-4.0, 1 mmHg = 0.44
            return -4.0 + (v - target) * 0.44

        mono_line = Line(LEFT * 3.2, LEFT * 0.8, color=MONO, stroke_width=8).set_y(lvl(mean_mono))
        combo_line = Line(RIGHT * 0.8, RIGHT * 3.2, color=COMBO, stroke_width=8).set_y(lvl(mean_combo))
        mono_pt = make_patients(MONO, 1.5).next_to(mono_line, UP, buff=0.2)
        combo_pt = make_patients(COMBO, 1.5).next_to(combo_line, UP, buff=0.2)
        mono_v = make_label(f"{mean_mono:.1f}", MONO, 36).next_to(mono_line, LEFT, buff=0.2)
        combo_v = make_label(f"{mean_combo:.1f}", COMBO, 36).next_to(combo_line, LEFT, buff=0.2)

        self.play_t(
            FadeOut(axis), FadeOut(axis_nums), FadeOut(axis_unit), FadeOut(mono_mark), FadeOut(combo_mark),
            run_time=0.7,
        )
        self.play_t(
            FadeIn(mono_pt, shift=UP * 0.3), Create(mono_line), FadeIn(mono_v),
            FadeIn(combo_pt, shift=UP * 0.3), Create(combo_line), FadeIn(combo_v),
            run_time=1.2,
        )

        # ─── Beat 3: 청크 2 둘째 문장 — 처음부터 더 높은 곳에서 출발 ───
        # 제목 교체: `기저 안압` -> `출발선이 다르다`
        # 단일 시선 대상: 주황 출발선
        self.wait_until(t_start)
        title2 = make_label("출발선이 다르다", INK, 60).move_to(title)
        self.play_t(
            ReplacementTransform(title, title2),
            Indicate(combo_line, color=COMBO, scale_factor=1.1),
            run_time=1.0,
        )

        # ─── Beat 4: 청크 2 셋째 문장 — 18까지 내려오기 어렵다 ───
        # 새로 등장: 초록 점선 목표선 `목표 18`, 출발선에서 목표선까지 아래 화살표
        # 단일 시선 대상: 길이가 다른 두 화살표
        self.wait_until(t_hard)
        goal_line = DashedLine(LEFT * 3.8, RIGHT * 3.8, color=GOOD, stroke_width=5,
                               dash_length=0.25).set_y(lvl(target))
        goal_label = make_label(f"목표 {target}", GOOD, 38).next_to(goal_line, DOWN, buff=0.3)
        mono_drop = Arrow(mono_line.get_center(), [mono_line.get_x(), lvl(target), 0], buff=0.05,
                          stroke_width=10, max_tip_length_to_length_ratio=0.5, color=MONO)
        combo_drop = Arrow(combo_line.get_center(), [combo_line.get_x(), lvl(target), 0], buff=0.05,
                           stroke_width=10, max_tip_length_to_length_ratio=0.15, color=COMBO)
        self.play_t(Create(goal_line), FadeIn(goal_label), run_time=0.8)
        self.play_t(GrowArrow(mono_drop), GrowArrow(combo_drop), run_time=1.2)
        self.wait_until(t_c3)

        # ─── Beat 5: 청크 3 첫 문장 — 두 분포를 겹치면 21~28 구간에 두 약 환자가 모두 있다 ───
        # 먼저 지울 것: 세로 안압 화면 전체
        # 제목 교체: `출발선이 다르다` -> `기저 안압 분포`
        # 새로 등장: 분포 막대(반투명, 파랑·주황 겹침), 축, 범례, 21~28 노란 띠 `겹치는 구간`
        # 단일 시선 대상: 노란 띠 안의 겹친 막대
        bins = hist["bins"]
        lo, hi = bins[0], bins[-1]
        base_y = -2.6
        max_count = max(max(hist["before"]["mono"]), max(hist["before"]["combo"]))

        def hx(v: float) -> float:            # 10~42 mmHg -> x -4.0~4.0
            return -4.0 + (v - lo) * 8.0 / (hi - lo)

        def bars(counts: list, color: str) -> VGroup:
            group = VGroup()
            for left, c in zip(bins[:-1], counts):
                if c == 0:
                    continue
                h = 5.6 * c / max_count
                w = hx(left + 2) - hx(left)
                r = Rectangle(width=w, height=h, stroke_color=BLACK, stroke_width=1,
                              fill_color=color, fill_opacity=0.6)
                group.add(r.move_to([hx(left) + w / 2, base_y + h / 2, 0]))
            return group

        title3 = make_label("기저 안압 분포", INK, 60).move_to(title2)
        mono_bars = bars(hist["before"]["mono"], MONO)
        combo_bars = bars(hist["before"]["combo"], COMBO)
        h_axis = Line([hx(lo), base_y, 0], [hx(hi), base_y, 0], color=MUTED, stroke_width=3)
        h_nums = VGroup(*[
            make_label(str(v), MUTED, 28, NORMAL).move_to([hx(v), base_y - 0.4, 0]) for v in (10, 20, 30, 40)
        ])
        h_unit = make_label("mmHg", MUTED, 26, NORMAL).move_to([hx(hi) - 0.3, base_y - 0.85, 0])
        legend = VGroup(
            VGroup(Square(0.3, fill_color=MONO, fill_opacity=0.8, stroke_width=0),
                   make_label("단일제", MONO, 34)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.3, fill_color=COMBO, fill_opacity=0.8, stroke_width=0),
                   make_label("복합제", COMBO, 34)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.6).move_to(UP * 3.9)

        band = Rectangle(width=hx(28) - hx(21), height=6.0, stroke_width=0,
                         fill_color=QUESTION, fill_opacity=0.18)
        band.move_to([(hx(21) + hx(28)) / 2, base_y + 3.0, 0])
        band.set_z_index(-1)                  # 띠는 막대 뒤에 깔아 막대 색이 탁해지지 않게 한다
        band_edges = VGroup(
            DashedLine([hx(21), base_y, 0], [hx(21), base_y + 6.0, 0], color=QUESTION, stroke_width=3),
            DashedLine([hx(28), base_y, 0], [hx(28), base_y + 6.0, 0], color=QUESTION, stroke_width=3),
        )
        band_label = make_label("겹치는 구간 21~28", QUESTION, 40).next_to(band, DOWN, buff=0.95)

        self.play_t(
            FadeOut(VGroup(mono_line, combo_line, mono_pt, combo_pt, mono_v, combo_v,
                           goal_line, goal_label, mono_drop, combo_drop)),
            ReplacementTransform(title2, title3),
            run_time=0.8,
        )
        self.play_t(Create(h_axis), FadeIn(h_nums), FadeIn(h_unit), FadeIn(legend), run_time=0.6)
        self.play_t(
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in mono_bars], lag_ratio=0.05),
            LaggedStart(*[GrowFromEdge(b, DOWN) for b in combo_bars], lag_ratio=0.05),
            run_time=1.6,
        )
        self.play_t(FadeIn(band), Create(band_edges), FadeIn(band_label), run_time=0.9)

        # ─── Beat 6: 청크 3 둘째 문장 — 같은 안압이어도 받은 약이 다르다 ───
        # 새로 등장: 띠 아래 구간 환자 수 (단일제 / 복합제)
        # 단일 시선 대상: 구간 환자 수
        self.wait_until(t_counts)
        counts = VGroup(
            make_label(f"단일제 {overlap['mono']}명", MONO, 40),
            make_label(f"복합제 {overlap['combo']}명", COMBO, 40),
        ).arrange(RIGHT, buff=0.6).next_to(band_label, DOWN, buff=0.4)
        self.play_t(FadeIn(counts, shift=UP * 0.2), run_time=0.8)

        self.wait_until(t_end + self.WAIT_TAIL)


class Scene04_Confounding(TimedScene):
    """
    Scene 04: 교란 — 기저 안압이 약 선택과 결과 양쪽에 영향을 준다. RCT가 이상적이지만 항상 할 수는 없다.

    Notebook Reference:
    book/psm_glaucoma/psm_glaucoma_ko.ipynb 셀 12 (교란 변수, 적응증에 의한 교란, RCT)
    notebooks/psm_simulation_ko.ipynb "1. 가상 환자 만들기" (처방이 기저 안압에 따라 정해지는 설계)

    Script Reference:
    src/scripts/ko/04_confounding.txt
    직전 Scene 마지막 문장: "같은 안압이어도 어떤 환자는 단일제를, 어떤 환자는 복합제를 받은 거예요."
    현재 Scene 첫 문장: "화살표로 정리해 볼게요."
    다음 Scene으로 넘기는 것: 성향점수와 짝짓기 (여기서는 말하지 않는다)

    Script-to-Beat Mapping (timings.json 기준, 청크 안 문장 시작은 글자 수 비율로 추정):
    청크 1 (0.00~9.86s)
      "화살표로 정리해 볼게요." -> 세 마디(기저 안압 / 약 선택 / 목표 도달) 배치
      "기저 안압이 높으면 복합제를 받을 가능성이 커지고," -> 기저 안압 -> 약 선택 화살표
      "동시에 목표 안압에 도달하기도 어려워져요." -> 기저 안압 -> 목표 도달 화살표, 약 선택 -> 목표 도달 `?`
    청크 2 (9.86~20.57s)
      "이렇게 약 선택과 결과 양쪽에 영향을 주는 변수를 교란 변수라고 불러요." -> 기저 안압 노랑, `교란 변수`
      "그러면 약의 효과와 출발선 차이가 뒤섞여 버려요." -> 세 화살표 함께 깜빡임, 하단 `약효 + 출발선 차이 = 뒤섞임`
    청크 3 (20.57~34.63s)
      "가장 확실한 방법은 무작위 배정 임상시험, 알씨티예요." -> 하단 문구 교체, 동전 + `무작위 배정 (RCT)`
      "동전 던지기로 약을 정하면, 기저 안압이 끼어들 수 없죠." -> 동전이 약 선택을 가리킴, 기저 안압 -> 약 선택 화살표에 X
      "하지만 비용과 시간이 많이 들어 항상 할 수는 없어요." -> 시계 + 돈 아이콘, `항상 할 수는 없다`
    가상 데이터 표시: 없음 (데이터 수치가 나오지 않는 Scene)
    """

    WAIT_TAIL = 0.7

    def construct(self):
        d1, d2, d3 = load_chunk_durations("04_confounding", [9.864, 10.704, 14.064])
        t_c2 = d1
        t_c3 = d1 + d2
        t_end = d1 + d2 + d3
        t_to_drug = d1 * 0.21                  # "기저 안압이 높으면 복합제를 ..."
        t_to_out = d1 * 0.62                   # "동시에 목표 안압에 ..."
        t_mixed = t_c2 + d2 * 0.60             # "그러면 약의 효과와 ..."
        t_coin = t_c3 + d3 * 0.33              # "동전 던지기로 ..."
        t_cost = t_c3 + d3 * 0.68              # "하지만 비용과 시간이 ..."

        # ─── Beat 1: 청크 1 첫 문장 — 세 마디 배치 ───
        # 화면 구획: 상단 제목 / 중앙 삼각형 DAG (위 1개, 아래 좌우 2개) / 하단 문구 자리 비움
        # 단일 시선 대상: 세 마디
        title = make_label("화살표로 보기", INK, 56).move_to(UP * 5.6)

        def node(icon: Mobject, text: str, color: str) -> VGroup:
            label = make_label(text, color, 46)
            body = VGroup(icon, label).arrange(DOWN, buff=0.25)
            frame = SurroundingRectangle(body, buff=0.3, corner_radius=0.2, color=color, stroke_width=4)
            return VGroup(frame, body)

        conf_node = node(load_icon("gauge.svg", INK, 1.4), "기저 안압", INK).move_to(UP * 2.2)
        drug_icon = VGroup(make_bottle(MONO, 1.25), make_bottle(COMBO, 1.25)).arrange(RIGHT, buff=0.25)
        drug_node = node(drug_icon, "약 선택", INK).move_to(LEFT * 2.5 + DOWN * 2.1)
        out_node = node(load_icon("target.svg", GOOD, 1.3), "목표 도달", INK).move_to(RIGHT * 2.5 + DOWN * 2.1)

        self.play_t(FadeIn(title, shift=DOWN * 0.2), run_time=0.6)
        self.play_t(FadeIn(conf_node), FadeIn(drug_node), FadeIn(out_node), run_time=0.9)

        # ─── Beat 2: 청크 1 둘째·셋째 부분 — 기저 안압에서 두 갈래 화살표, 약효 화살표 `?` ───
        # 새로 등장: 기저 안압 -> 약 선택, 기저 안압 -> 목표 도달, 약 선택 -> 목표 도달(?)
        # 단일 시선 대상: 지금 말하는 화살표
        to_drug = Arrow(conf_node.get_bottom() + LEFT * 0.5, drug_node.get_top() + RIGHT * 0.3,
                        buff=0.1, stroke_width=8, color=INK)
        to_out = Arrow(conf_node.get_bottom() + RIGHT * 0.5, out_node.get_top() + LEFT * 0.3,
                       buff=0.1, stroke_width=8, color=INK)
        effect = Arrow(drug_node.get_right(), out_node.get_left(), buff=0.1, stroke_width=8, color=MUTED)
        effect_q = make_label("?", QUESTION, 56).next_to(effect, DOWN, buff=0.15)

        self.wait_until(t_to_drug)
        self.play_t(GrowArrow(to_drug), run_time=0.8)
        self.wait_until(t_to_out)
        self.play_t(GrowArrow(to_out), run_time=0.8)
        self.play_t(GrowArrow(effect), FadeIn(effect_q), run_time=0.7)
        self.wait_until(t_c2)

        # ─── Beat 3: 청크 2 첫 문장 — 교란 변수 ───
        # 기저 안압 마디와 두 갈래 화살표를 노랑으로, 위에 `교란 변수`
        # 단일 시선 대상: 노란 기저 안압
        conf_tag = make_label("교란 변수", QUESTION, 44).next_to(conf_node, UP, buff=0.3)
        self.play_t(
            conf_node[0].animate.set_color(QUESTION), conf_node[1][1].animate.set_color(QUESTION),
            to_drug.animate.set_color(QUESTION), to_out.animate.set_color(QUESTION),
            FadeIn(conf_tag, shift=DOWN * 0.2),
            run_time=0.9,
        )

        # ─── Beat 4: 청크 2 둘째 문장 — 약효와 출발선 차이가 뒤섞인다 ───
        # 새로 등장: 하단 `약효 + 출발선 차이 = 뒤섞임`
        # 단일 시선 대상: 함께 깜빡이는 세 화살표
        self.wait_until(t_mixed)
        mixed = VGroup(
            make_label("약효", MUTED, 40),
            make_label("+", INK, 40),
            make_label("출발선 차이", QUESTION, 40),
        ).arrange(RIGHT, buff=0.25)
        mixed_eq = make_label("= 뒤섞임", INK, 44).next_to(mixed, DOWN, buff=0.3)
        mixed_group = VGroup(mixed, mixed_eq).move_to(DOWN * 5.3)
        self.play_t(
            Indicate(effect, color=MUTED), Indicate(to_drug, color=QUESTION), Indicate(to_out, color=QUESTION),
            FadeIn(mixed_group, shift=UP * 0.2),
            run_time=1.2,
        )
        self.wait_until(t_c3)

        # ─── Beat 5: 청크 3 첫 문장 — 무작위 배정 임상시험(RCT) ───
        # 먼저 지울 것: 하단 뒤섞임 문구
        # 제목 교체: `화살표로 보기` -> `가장 확실한 방법`
        # 새로 등장: 하단 동전 + `무작위 배정 (RCT)`
        # 단일 시선 대상: 동전
        title2 = make_label("가장 확실한 방법", INK, 56).move_to(title)
        # 동전: Tabler coin 아이콘은 $ 표시라 돈으로 읽히므로 앞/뒤 면을 직접 그린다
        coin = VGroup(
            Circle(radius=0.6, color=QUESTION, stroke_width=6),
            Circle(radius=0.42, color=QUESTION, stroke_width=3),
            make_label("앞", QUESTION, 30),
        )
        rct_label = make_label("무작위 배정 (RCT)", QUESTION, 44)
        rct = VGroup(coin, rct_label).arrange(RIGHT, buff=0.35).move_to(DOWN * 5.4)
        self.play_t(FadeOut(mixed_group), ReplacementTransform(title, title2), run_time=0.7)
        self.play_t(FadeIn(rct, shift=UP * 0.2), run_time=0.8)

        # ─── Beat 6: 청크 3 둘째 문장 — 동전이 약을 정하면 기저 안압이 끼어들 수 없다 ───
        # 새로 등장: 동전 -> 약 선택 화살표, 기저 안압 -> 약 선택 화살표 위 X (화살표는 흐리게)
        # 단일 시선 대상: X 표시
        self.wait_until(t_coin)
        coin_arrow = Arrow(coin.get_top(), drug_node.get_bottom(), buff=0.15, stroke_width=8, color=QUESTION)
        cross = Cross(scale_factor=0.35, stroke_color=COMBO, stroke_width=10).move_to(to_drug.get_center())
        self.play_t(GrowArrow(coin_arrow), run_time=0.8)
        self.play_t(to_drug.animate.set_opacity(0.3), Create(cross), run_time=0.8)

        # ─── Beat 7: 청크 3 셋째 문장 — 비용과 시간 때문에 항상 할 수는 없다 ───
        # 먼저 지울 것: 동전 줄과 동전 화살표
        # 새로 등장: 하단 시계 + 돈 아이콘, `항상 할 수는 없다`
        # 단일 시선 대상: 하단 한계 문구
        self.wait_until(t_cost)
        limits = VGroup(load_icon("clock.svg", MUTED, 1.1), load_icon("cash.svg", MUTED, 1.1)).arrange(RIGHT, buff=0.4)
        limit_label = make_label("항상 할 수는 없다", INK, 44)
        limit_group = VGroup(limits, limit_label).arrange(DOWN, buff=0.3).move_to(DOWN * 5.4)
        self.play_t(FadeOut(rct), FadeOut(coin_arrow), run_time=0.6)
        self.play_t(FadeIn(limit_group, shift=UP * 0.2), run_time=0.8)

        self.wait_until(t_end + self.WAIT_TAIL)


class Scene05_Matching(TimedScene):
    """
    Scene 05: PSM — 복합제를 받을 확률(성향점수)이 비슷한 환자끼리 1:1로 짝지으면 출발선이 비슷한 두 그룹이 만들어진다.

    Notebook Reference:
    notebooks/psm_simulation_ko.ipynb
    - "4. 성향점수와 1:1 매칭": 공변량 4개, matched_pairs
    - "5. 균형 확인": matched_baseline_iop_mean, iop0_hist.after
    book/psm_glaucoma/psm_glaucoma_ko.ipynb 셀 13~22 구성 참고

    Script Reference:
    src/scripts/ko/05_matching.txt
    직전 Scene 마지막 문장: "하지만 비용과 시간이 많이 들어 항상 할 수는 없어요."
    현재 Scene 첫 문장: "그래서 쓰는 방법이 성향점수 매칭이에요."
    다음 Scene으로 넘기는 것: 매칭 후 목표 도달률 (여기서는 말하지 않는다)

    Script-to-Beat Mapping (timings.json 기준, 청크 안 문장 시작은 글자 수 비율로 추정):
    청크 1 (0.00~14.90s)
      "그래서 쓰는 방법이 성향점수 매칭이에요." -> 제목 `성향점수 매칭` / `PSM`
      "먼저 환자마다 기저 안압, 나이, 녹내장 유형, 각막 두께를 보고 ..." -> 특성 카드 4장 -> 환자 아이콘 -> 0~1 막대 표시
      "이 확률이 성향점수예요." -> `성향점수 = 복합제를 받을 확률`
    청크 2 (14.90~32.26s) — 개념 그림 (실제 데이터 아님, `개념 그림` 표시)
      "그다음 복합제 환자 한 명마다, 성향점수가 가장 비슷한 단일제 환자 한 명을 짝지어요." -> 눈금 위 주황 점, 아래 파랑 점, 가까운 점끼리 선
      "짝은 두 약의 환자가 겹치는 중간 구간에서만 지을 수 있어요." -> 노란 띠 `겹치는 구간`
      "안압이 아주 높거나 낮아서 비교 상대가 없는 환자는 빠지게 됩니다." -> 양 끝 점 회색, `짝 없음`
    청크 3 (32.26~46.97s)
      "이렇게 삼백칠십칠 쌍이 만들어졌어요." -> `377쌍`
      "짝지은 두 그룹의 기저 안압 평균은 이십오 점 일과 이십오 점 삼으로, 거의 같아졌어요." -> 매칭 전/후 평균 눈금 (21.0·28.9 -> 25.1·25.3)
      "이제 출발선이 비슷한 환자끼리 비교할 수 있습니다." -> 매칭 후 분포 겹침, `출발선 비슷`
    가상 데이터 표시: 청크 3 (수치 화면)에만. 청크 2는 `개념 그림`
    """

    WAIT_TAIL = 0.7

    def construct(self):
        nums = load_numbers()
        pairs = nums["matched_pairs"]
        before = nums["baseline_iop_mean"]
        after = nums["matched_baseline_iop_mean"]
        hist = nums["iop0_hist"]

        d1, d2, d3 = load_chunk_durations("05_matching", [14.904, 17.352, 14.712])
        t_c2 = d1
        t_c3 = d1 + d2
        t_end = d1 + d2 + d3
        t_feat = d1 * 0.26                     # "먼저 환자마다 ..."
        t_ps = d1 * 0.84                       # "이 확률이 성향점수예요."
        t_band = t_c2 + d2 * 0.40              # "짝은 두 약의 환자가 겹치는 ..."
        t_drop = t_c2 + d2 * 0.68              # "안압이 아주 높거나 낮아서 ..."
        t_means = t_c3 + d3 * 0.21             # "짝지은 두 그룹의 기저 안압 평균은 ..."
        t_same = t_c3 + d3 * 0.72              # "이제 출발선이 비슷한 ..."

        # ─── Beat 1: 청크 1 첫 문장 — 성향점수 매칭 ───
        title = VGroup(
            make_label("성향점수 매칭", INK, 60),
            make_label("PSM", MUTED, 36, NORMAL),
        ).arrange(DOWN, buff=0.15).move_to(UP * 5.5)
        self.play_t(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)

        # ─── Beat 2: 청크 1 둘째 문장 — 특성 4개로 복합제를 받을 확률 계산 ───
        # 화면 구획: 상단 특성 카드 2x2 / 가운데 환자 아이콘 / 아래 0~1 막대
        # 단일 시선 대상: 카드 -> 환자 -> 막대로 흐르는 화살표
        self.wait_until(t_feat)
        chips = VGroup(*[
            VGroup(
                RoundedRectangle(width=3.4, height=0.9, corner_radius=0.2, color=MUTED, stroke_width=3),
                make_label(text, INK, 36),
            )
            for text in ("기저 안압", "나이", "녹내장 유형", "각막 두께")
        ])
        for chip in chips:
            chip[1].move_to(chip[0])
        chips.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.35)).move_to(UP * 2.6)
        patient = make_patients(INK, 1.4).move_to(DOWN * 0.4)
        feed = VGroup(*[
            Arrow(chip.get_bottom(), patient.get_top(), buff=0.12, stroke_width=4, color=MUTED,
                  max_tip_length_to_length_ratio=0.12)
            for chip in chips[2:]
        ])

        bar_left, bar_right, bar_y = -3.4, 3.4, -2.6
        ps_bar = Rectangle(width=bar_right - bar_left, height=0.35, stroke_width=0, fill_opacity=1)
        # Manim 그라데이션은 목록 역순으로 칠해지므로, 0쪽이 파랑이 되도록 [주황, 파랑] 순서로 준다
        ps_bar.set_fill(color=[COMBO, MONO]).move_to([0, bar_y, 0])
        zero = make_label("0", MUTED, 30, NORMAL).next_to(ps_bar, LEFT, buff=0.2)
        one = make_label("1", MUTED, 30, NORMAL).next_to(ps_bar, RIGHT, buff=0.2)
        marker = Triangle(color=INK, fill_opacity=1, stroke_width=0).scale(0.2).rotate(PI)
        marker.next_to([bar_left + 0.68 * (bar_right - bar_left), bar_y + 0.175, 0], UP, buff=0.05)
        to_bar = Arrow(patient.get_bottom(), marker.get_top(), buff=0.12, stroke_width=5, color=INK)

        self.play_t(LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in chips], lag_ratio=0.25), run_time=1.6)
        self.play_t(*[GrowArrow(a) for a in feed], FadeIn(patient), run_time=0.9)
        self.play_t(FadeIn(ps_bar), FadeIn(zero), FadeIn(one), GrowArrow(to_bar), FadeIn(marker), run_time=0.9)

        # ─── Beat 3: 청크 1 셋째 문장 — 이 확률이 성향점수 ───
        self.wait_until(t_ps)
        ps_label = VGroup(
            make_label("성향점수", QUESTION, 44),
            make_label("= 복합제를 받을 확률", INK, 40, NORMAL),
        ).arrange(DOWN, buff=0.15).next_to(ps_bar, DOWN, buff=0.5)
        self.play_t(FadeIn(ps_label, shift=UP * 0.2), run_time=0.7)
        self.wait_until(t_c2)

        # ─── Beat 4: 청크 2 첫 문장 — 성향점수가 비슷한 환자끼리 1:1 짝 ───
        # 먼저 지울 것: 카드·환자·막대 전부 (제목 교체 `1:1 짝짓기`)
        # 새로 등장: 성향점수 눈금, 위 주황 점(복합제), 아래 파랑 점(단일제), `개념 그림` 표시
        # 단일 시선 대상: 차례로 이어지는 짝 선
        title2 = make_label("1:1 짝짓기", INK, 60).move_to(title)
        concept_tag = make_label("개념 그림", MUTED, 26, NORMAL).to_corner(DR, buff=0.5)
        axis = Line(LEFT * 4.0, RIGHT * 4.0, color=MUTED, stroke_width=3).move_to(DOWN * 0.2)
        axis_name = make_label("성향점수", MUTED, 32, NORMAL).next_to(axis, DOWN, buff=1.7)
        low = make_label("낮음", MUTED, 28, NORMAL).next_to(axis.get_left(), DOWN, buff=0.25).shift(RIGHT * 0.3)
        high = make_label("높음", MUTED, 28, NORMAL).next_to(axis.get_right(), DOWN, buff=0.25).shift(LEFT * 0.3)

        # 개념 그림용 점 위치: 단일제는 왼쪽(낮은 성향점수), 복합제는 오른쪽에 몰리게 배치
        mono_x = [-3.7, -3.2, -2.6, -1.9, -1.2, -0.6, 0.1, 0.8]
        combo_x = [-1.1, -0.5, 0.2, 0.9, 1.6, 2.3, 3.0, 3.6]
        y_combo, y_mono = 1.2, -1.6
        combo_dots = VGroup(*[Dot([x, y_combo, 0], radius=0.2, color=COMBO) for x in combo_x])
        mono_dots = VGroup(*[Dot([x, y_mono, 0], radius=0.2, color=MONO) for x in mono_x])
        combo_name = make_label("복합제", COMBO, 36).next_to(combo_dots, UP, buff=0.35)
        mono_name = make_label("단일제", MONO, 36).next_to(mono_dots, DOWN, buff=0.35)
        # 짝: 복합제 0~3번 <-> 단일제 4~7번 (성향점수가 가장 가까운 상대)
        pair_idx = [(0, 4), (1, 5), (2, 6), (3, 7)]
        pair_lines = VGroup(*[
            Line(combo_dots[c].get_center(), mono_dots[m].get_center(), color=INK, stroke_width=4)
            for c, m in pair_idx
        ])

        self.play_t(
            FadeOut(VGroup(chips, feed, patient, ps_bar, zero, one, marker, to_bar, ps_label)),
            ReplacementTransform(title, title2), FadeIn(concept_tag),
            run_time=0.8,
        )
        self.play_t(
            Create(axis), FadeIn(low), FadeIn(high),
            LaggedStart(*[FadeIn(d, scale=0.5) for d in combo_dots], lag_ratio=0.1),
            LaggedStart(*[FadeIn(d, scale=0.5) for d in mono_dots], lag_ratio=0.1),
            FadeIn(combo_name), FadeIn(mono_name),
            run_time=1.4,
        )
        self.play_t(LaggedStart(*[Create(l) for l in pair_lines], lag_ratio=0.4), run_time=2.0)

        # ─── Beat 5: 청크 2 둘째 문장 — 겹치는 중간 구간에서만 짝 ───
        # 새로 등장: 짝이 있는 구간 뒤 노란 띠 + `겹치는 구간`
        self.wait_until(t_band)
        band = Rectangle(width=2.8, height=4.4, stroke_width=0, fill_color=QUESTION, fill_opacity=0.15)
        band.move_to([-0.15, (y_combo + y_mono) / 2, 0]).set_z_index(-1)
        band_label = make_label("겹치는 구간", QUESTION, 40).next_to(axis, DOWN, buff=2.6)
        self.play_t(FadeIn(band), FadeIn(band_label), run_time=0.8)

        # ─── Beat 6: 청크 2 셋째 문장 — 비교 상대가 없는 환자는 빠진다 ───
        # 짝 없는 점(양 끝)을 회색으로 흐리고 `짝 없음`
        self.wait_until(t_drop)
        unpaired = VGroup(*[mono_dots[i] for i in range(4)], *[combo_dots[i] for i in range(4, 8)])
        no_pair_l = make_label("짝 없음", MUTED, 30, NORMAL).next_to(mono_dots[1], DOWN, buff=0.35)
        no_pair_r = make_label("짝 없음", MUTED, 30, NORMAL).next_to(combo_dots[6], DOWN, buff=0.35)
        self.play_t(unpaired.animate.set_color(MUTED).set_opacity(0.45),
                    FadeIn(no_pair_l), FadeIn(no_pair_r), run_time=1.0)
        self.wait_until(t_c3)

        # ─── Beat 7: 청크 3 첫 문장 — 377쌍 ───
        # 먼저 지울 것: 개념 그림 전체 (`개념 그림` -> `가상 데이터` 표시)
        # 새로 등장: 큰 `377쌍`
        title3 = make_label("매칭 결과", INK, 60).move_to(title2)
        tag = virtual_tag()
        pair_count = make_label(f"{pairs}쌍", INK, 80).move_to(UP * 3.7)
        self.play_t(
            FadeOut(VGroup(axis, low, high, combo_dots, mono_dots, combo_name, mono_name, pair_lines,
                           band, band_label, no_pair_l, no_pair_r)),
            ReplacementTransform(title2, title3), ReplacementTransform(concept_tag, tag),
            run_time=0.8,
        )
        self.play_t(FadeIn(pair_count, scale=0.8), run_time=0.7)

        # ─── Beat 8: 청크 3 둘째 문장 — 기저 안압 평균이 거의 같아짐 ───
        # 새로 등장: `매칭 전` / `매칭 후` 두 줄의 평균 눈금 (18~32 mmHg)
        # 단일 시선 대상: 매칭 후 줄에서 거의 겹친 두 표시
        self.wait_until(t_means)

        def mean_row(m_mono: float, m_combo: float, label: str, y: float) -> VGroup:
            line = NumberLine(x_range=[18, 32, 2], length=6.0, color=MUTED, stroke_width=3,
                              tick_size=0.06).move_to([0.9, y, 0])
            name = make_label(label, INK, 36).next_to(line, LEFT, buff=0.35)
            dm = Dot(line.n2p(m_mono), radius=0.17, color=MONO)
            dc = Dot(line.n2p(m_combo), radius=0.17, color=COMBO)
            vm = make_label(f"{m_mono:.1f}", MONO, 34).next_to(dm, UP, buff=0.2)
            vc = make_label(f"{m_combo:.1f}", COMBO, 34).next_to(dc, DOWN, buff=0.2)
            return VGroup(line, name, dm, dc, vm, vc)

        row_before = mean_row(before["mono"], before["combo"], "매칭 전", 1.6)
        row_after = mean_row(after["mono"], after["combo"], "매칭 후", -0.6)
        self.play_t(FadeIn(row_before), run_time=0.7)
        self.play_t(FadeIn(row_after), run_time=0.7)
        self.play_t(Indicate(VGroup(row_after[2], row_after[3]), color=GOOD, scale_factor=1.3), run_time=0.9)

        # ─── Beat 9: 청크 3 셋째 문장 — 출발선이 비슷한 환자끼리 비교 ───
        # 새로 등장: 매칭 후 기저 안압 분포(파랑·주황 거의 겹침), `출발선 비슷`
        self.wait_until(t_same)
        bins = hist["bins"]
        counts_m, counts_c = hist["after"]["mono"], hist["after"]["combo"]
        top = max(max(counts_m), max(counts_c))
        base_y = -5.6

        def hx(v: float) -> float:            # 14~38 mmHg -> x -3.6~3.6
            return -3.6 + (v - 14) * 7.2 / 24

        after_bars = VGroup()
        # 두 분포가 거의 같아 색을 겹치면 탁해지므로: 단일제는 채운 파랑, 복합제는 주황 테두리만
        for counts, color in ((counts_m, MONO), (counts_c, COMBO)):
            for left, c in zip(bins[:-1], counts):
                if c == 0 or left < 14 or left >= 38:
                    continue
                h = 2.8 * c / top
                w = hx(left + 2) - hx(left)
                if color == MONO:
                    r = Rectangle(width=w, height=h, stroke_color=BLACK, stroke_width=1,
                                  fill_color=MONO, fill_opacity=0.75)
                else:
                    r = Rectangle(width=w, height=h, stroke_color=COMBO, stroke_width=4, fill_opacity=0)
                after_bars.add(r.move_to([hx(left) + w / 2, base_y + h / 2, 0]))
        same = make_label("출발선 비슷", GOOD, 44).next_to(after_bars, UP, buff=0.35)
        self.play_t(LaggedStart(*[GrowFromEdge(b, DOWN) for b in after_bars], lag_ratio=0.03), run_time=1.2)
        self.play_t(FadeIn(same, shift=UP * 0.2), run_time=0.6)

        self.wait_until(t_end + self.WAIT_TAIL)


class Scene06_Result(TimedScene):
    """
    Scene 06: 결과 — 같은 데이터인데 비교 방법만 바꿨더니, 매칭 후에는 복합제의 도달률이 더 높다.

    Notebook Reference:
    notebooks/psm_simulation_ko.ipynb "6. 매칭 후 결과": matched_reach_pct, naive_reach_pct
    book/psm_glaucoma/psm_glaucoma_ko.ipynb 셀 23~26 (결론 뒤집힘, 정리와 한계) 구성 참고

    Script Reference:
    src/scripts/ko/06_result.txt
    직전 Scene 마지막 문장: "이제 출발선이 비슷한 환자끼리 비교할 수 있습니다."
    현재 Scene 첫 문장: "이제 짝지은 환자끼리 목표 도달률을 비교해 볼게요."

    Script-to-Beat Mapping (timings.json 기준, 청크 안 문장 시작은 글자 수 비율로 추정):
    청크 1 (0.00~9.46s)
      "이제 짝지은 환자끼리 목표 도달률을 비교해 볼게요." -> 제목 `매칭 후 목표 도달률`, 바닥선 (Scene 02와 같은 막대 배치)
      "단일제는 오십칠 퍼센트, 복합제는 칠십오 퍼센트예요." -> 파랑 `57%` -> 주황 `75%` 막대
    청크 2 (9.46~18.62s)
      "처음 비교와 결론이 정반대로 뒤집혔죠." -> 막대를 오른쪽으로 줄이고 왼쪽에 `단순 비교` 막대, 가운데 `뒤집힘` 화살표
      "데이터는 그대로인데, 무엇과 무엇을 비교하느냐만 바꿨을 뿐이에요." -> 하단 `같은 데이터, 다른 비교`
    청크 3 (18.62~30.24s)
      "다만 이 결론은 짝을 찾은 중간 범위 환자에게 해당해요." -> 매칭 후 그래프 아래 회색 `짝을 찾은 중간 범위 환자 기준`
      "단순 비교만으로 약효를 단정하면 안 되는 이유, 이제 보이시나요?" -> 그래프를 지우고 마지막 문구 `단순 비교 ≠ 약효`
    가상 데이터 표시: 처음부터 끝까지 오른쪽 아래
    """

    WAIT_TAIL = 1.0
    BASE_Y = -2.4        # Scene 02와 같은 막대 바닥선
    FULL_H = 5.6         # 100% 막대 높이
    BAR_X = 1.7
    BAR_W = 1.7

    def chart(self, mono: int, combo: int, caption: str, caption_color: str) -> VGroup:
        """두 막대 그래프. 반환 순서: [바닥선, 파랑 막대, 주황 막대, 파랑 값, 주황 값, 약 이름 2개, 그래프 이름]"""
        base = Line([-(self.BAR_X + self.BAR_W), self.BASE_Y, 0], [self.BAR_X + self.BAR_W, self.BASE_Y, 0],
                    color=MUTED, stroke_width=3)

        def bar(value: int, color: str, x: float) -> RoundedRectangle:
            h = self.FULL_H * value / 100
            r = RoundedRectangle(width=self.BAR_W, height=h, corner_radius=0.1,
                                 color=color, fill_opacity=1, stroke_width=0)
            return r.move_to([x, self.BASE_Y + h / 2, 0])

        mono_bar = bar(mono, MONO, -self.BAR_X)
        combo_bar = bar(combo, COMBO, self.BAR_X)
        mono_val = make_label(f"{mono}%", INK, 56).next_to(mono_bar, UP, buff=0.25)
        combo_val = make_label(f"{combo}%", INK, 56).next_to(combo_bar, UP, buff=0.25)
        cats = VGroup(
            make_label("단일제", MONO, 44).move_to([-self.BAR_X, self.BASE_Y - 0.55, 0]),
            make_label("복합제", COMBO, 44).move_to([self.BAR_X, self.BASE_Y - 0.55, 0]),
        )
        name = make_label(caption, caption_color, 52).move_to([0, self.BASE_Y + self.FULL_H + 0.9, 0])
        return VGroup(base, mono_bar, combo_bar, mono_val, combo_val, cats, name)

    def construct(self):
        nums = load_numbers()
        m_mono, m_combo = pct(nums["matched_reach_pct"]["mono"]), pct(nums["matched_reach_pct"]["combo"])
        n_mono, n_combo = pct(nums["naive_reach_pct"]["mono"]), pct(nums["naive_reach_pct"]["combo"])

        d1, d2, d3 = load_chunk_durations("06_result", [9.456, 9.168, 11.616])
        t_c2 = d1
        t_c3 = d1 + d2
        t_end = d1 + d2 + d3
        t_mono = d1 * 0.48                     # "단일제는 오십칠 퍼센트"
        t_combo = d1 * 0.72                    # "복합제는 칠십오 퍼센트예요"
        t_same = t_c2 + d2 * 0.37              # "데이터는 그대로인데 ..."
        t_final = t_c3 + d3 * 0.46             # "단순 비교만으로 약효를 ..."

        tag = virtual_tag()

        # ─── Beat 1: 청크 1 — 매칭 후 도달률 막대 ───
        # 화면 구획: 상단 제목 / 중앙 막대 2개 (Scene 02와 같은 위치·색) / 하단 비움
        # 단일 시선 대상: 자라는 막대와 숫자
        title = make_label("매칭 후 목표 도달률", INK, 54).move_to(UP * 5.6)
        after = self.chart(m_mono, m_combo, "매칭 후", GOOD)
        base, mono_bar, combo_bar, mono_val, combo_val, cats, after_name = after

        self.play_t(FadeIn(title, shift=DOWN * 0.2), FadeIn(tag), run_time=0.8)
        self.play_t(Create(base), FadeIn(cats), run_time=0.6)
        self.wait_until(t_mono)
        self.play_t(GrowFromEdge(mono_bar, DOWN), run_time=0.9)
        self.play_t(FadeIn(mono_val, shift=UP * 0.2), run_time=0.4)
        self.wait_until(t_combo)
        self.play_t(GrowFromEdge(combo_bar, DOWN), run_time=0.9)
        self.play_t(FadeIn(combo_val, shift=UP * 0.2), run_time=0.4)
        # 같은 play 안에서 FadeIn과 Indicate를 함께 쓰면 Indicate가 투명 상태로 되돌려 버리므로 따로 실행
        self.play_t(Indicate(combo_val, color=COMBO), run_time=0.6)
        self.wait_until(t_c2)

        # ─── Beat 2: 청크 2 첫 문장 — 처음 비교와 결론이 뒤집혔다 ───
        # 매칭 후 그래프를 오른쪽 절반으로 줄이고, 왼쪽에 단순 비교 그래프(같은 축척)를 놓는다
        # 제목 교체: `매칭 후 목표 도달률` -> `결론이 뒤집혔다`
        # 단일 시선 대상: 가운데 `뒤집힘` 화살표
        scale = 0.6
        title2 = make_label("결론이 뒤집혔다", INK, 58).move_to(title)
        naive = self.chart(n_mono, n_combo, "단순 비교", MUTED)
        naive.scale(scale).move_to(LEFT * 2.3 + UP * 0.4)
        after_target = after.copy()
        after_target[6].set_opacity(1)
        after_target.scale(scale).move_to(RIGHT * 2.3 + UP * 0.4)

        self.play_t(
            ReplacementTransform(title, title2),
            Transform(VGroup(base, mono_bar, combo_bar, mono_val, combo_val, cats), VGroup(*after_target[:6])),
            run_time=1.0,
        )
        after_name_small = after_target[6]
        flip = CurvedArrow(LEFT * 0.8 + UP * 3.6, RIGHT * 0.8 + UP * 3.6, angle=-PI / 2.5, color=QUESTION, stroke_width=6)
        flip_label = make_label("뒤집힘", QUESTION, 40).next_to(flip, UP, buff=0.15)
        self.play_t(FadeIn(naive), FadeIn(after_name_small), run_time=0.8)
        self.play_t(Create(flip), FadeIn(flip_label), run_time=0.8)

        # ─── Beat 3: 청크 2 둘째 문장 — 같은 데이터, 다른 비교 ───
        self.wait_until(t_same)
        same = make_label("같은 데이터, 다른 비교", INK, 48).move_to(DOWN * 3.4)
        self.play_t(FadeIn(same, shift=UP * 0.2), run_time=0.8)
        self.wait_until(t_c3)

        # ─── Beat 4: 청크 3 첫 문장 — 짝을 찾은 중간 범위 환자에 대한 결론 ───
        # 새로 등장: 하단 회색 한계 문구 (결론을 과장하지 않기 위한 단서)
        note = make_label("짝을 찾은 중간 범위 환자 기준", MUTED, 34, NORMAL).next_to(same, DOWN, buff=0.45)
        self.play_t(FadeIn(note), run_time=0.7)

        # ─── Beat 5: 청크 3 둘째 문장 — 단순 비교만으로 약효를 단정하지 말 것 ───
        # 먼저 지울 것: 그래프·문구 전부
        # 새로 등장: 화면 가운데 마지막 문구 `단순 비교 ≠ 약효`
        self.wait_until(t_final)
        final = VGroup(
            make_label("단순 비교", INK, 72),
            make_label("≠", QUESTION, 72),
            make_label("약효", INK, 72),
        ).arrange(RIGHT, buff=0.35).move_to(UP * 0.4)
        self.play_t(
            FadeOut(VGroup(title2, naive, base, mono_bar, combo_bar, mono_val, combo_val, cats,
                           after_name_small, flip, flip_label, same, note)),
            run_time=0.8,
        )
        self.play_t(FadeIn(final, scale=0.9), run_time=0.9)

        self.wait_until(t_end + self.WAIT_TAIL)
