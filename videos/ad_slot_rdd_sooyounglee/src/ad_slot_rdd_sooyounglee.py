import json
from pathlib import Path

import numpy as np

from manim import *


# ─── 16:9 가로형 기본 설정 (frame 14.2 x 8) ───
# 톤앤매너 참고: Apple WWDC26 "What's new in Swift"의 슬라이드 구간 (발표자 부분 제외)
#   - 아주 옅은 회백색 배경, 테두리 없는 평면 카드, 넓은 여백
#   - 좌상단 작은 회색 챕터 라벨, 왼쪽 정렬 제목
#   - 강조색은 한 번에 하나(주황)만, 나머지는 회색 톤
config.background_color = "#F5F5F7"

# 한글이 깔끔하게 보이도록 모든 Text에 Pretendard를 기본으로 쓴다.
FONT = "Pretendard"
Text.set_default(font=FONT)

INK = "#1f1f1f"           # 본문 글자·선
SUBTLE = "#6b6b6b"        # 보조 글자
MUTED = "#a0a0a0"         # 흐린 요소
AD_A_COLOR = TEAL_D       # 1위 광고 거북이
AD_B_COLOR = "#C98A2E"    # 2위 광고 거북이
HIGHLIGHT_COLOR = "#E67700"
QUALITY_COLOR = "#3B7DD8"  # 광고 품질 (교란 요인)
OK_COLOR = "#2E9E5B"
NG_COLOR = "#D9483B"
NODE_GREY = "#8E8E93"
CARD_FILL = "#F5F5F7"
PHONE_FILL = WHITE
ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
TOPIC_DIR = Path(__file__).resolve().parents[1]

# 화면 좌측 설명 구역의 중심과 우측 휴대폰 중심
LEFT_ZONE_X = -3.6
PHONE_X = 3.1


def load_icon(filename: str, color: str, height: float) -> SVGMobject:
    icon = SVGMobject(str(ASSET_DIR / filename))
    icon.set_stroke(color=color, width=2.4, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def load_audio_timings(scene_basename: str) -> tuple[list[float], float]:
    """chunk별 시작 시각과 mp3 전체 길이를 반환한다."""
    timings_path = TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json"
    payload = json.loads(timings_path.read_text())
    starts = [float(chunk["start"]) for chunk in payload["chunks"]]
    return starts, float(payload["totalDuration"])


def make_turtle(shell_color: str, height: float = 0.9) -> VGroup:
    """Tabler에 거북이 아이콘이 없어 도형으로 그린 귀여운 행운 거북이."""
    skin = interpolate_color(ManimColor(shell_color), WHITE, 0.45)
    dark = interpolate_color(ManimColor(shell_color), BLACK, 0.45)

    legs = VGroup(*[
        Ellipse(width=0.26, height=0.34, fill_color=skin, fill_opacity=1, stroke_width=0)
        .move_to([x, -0.32, 0])
        for x in (-0.38, -0.12, 0.14, 0.38)
    ])
    tail = Triangle(fill_color=skin, fill_opacity=1, stroke_width=0)
    tail.scale(0.1).rotate(PI / 2).move_to([-0.66, -0.12, 0])
    shell = Ellipse(width=1.3, height=0.86, fill_color=shell_color, fill_opacity=1)
    shell.set_stroke(dark, width=3)
    hexagon = RegularPolygon(6, radius=0.2, fill_color=dark, fill_opacity=0.55, stroke_width=0)
    hexagon.move_to(shell.get_center() + UP * 0.05)
    spots = VGroup(*[
        Circle(radius=0.07, fill_color=dark, fill_opacity=0.55, stroke_width=0).move_to(pos)
        for pos in ([-0.36, 0.08, 0], [0.36, 0.08, 0], [0, -0.22, 0])
    ])
    head = Circle(radius=0.26, fill_color=skin, fill_opacity=1, stroke_width=0)
    head.move_to([0.78, 0.12, 0])
    eye = Dot(radius=0.05, color=BLACK).move_to(head.get_center() + RIGHT * 0.08 + UP * 0.05)
    sparkle = Dot(radius=0.018, color=WHITE).move_to(eye.get_center() + UR * 0.02)
    blush = Ellipse(width=0.12, height=0.07, fill_color=PINK, fill_opacity=0.8, stroke_width=0)
    blush.move_to(head.get_center() + RIGHT * 0.06 + DOWN * 0.08)

    turtle = VGroup(legs, tail, shell, hexagon, spots, head, eye, sparkle, blush)
    turtle.height = height
    return turtle


def make_product_card(turtle_color: str | None, name: str, is_ad: bool) -> VGroup:
    """휴대폰 검색 결과 한 줄: 거북이 썸네일 + 상품명 + (광고 배지)."""
    card = RoundedRectangle(width=3.3, height=1.45, corner_radius=0.14)
    card.set_fill(CARD_FILL, opacity=1).set_stroke(width=0)

    if turtle_color is None:
        thumb = RoundedRectangle(width=1.0, height=0.8, corner_radius=0.1)
        thumb.set_fill("#E6E6E9", opacity=1).set_stroke(width=0)
    else:
        thumb = make_turtle(turtle_color, height=0.72)
    thumb.move_to(card.get_left() + RIGHT * 0.75)

    title = Text(name, font_size=24, color=INK if is_ad else MUTED)
    title.next_to(thumb, RIGHT, buff=0.3).align_to(card, UP).shift(DOWN * 0.32)
    parts = [card, thumb, title]

    if is_ad:
        badge_text = Text("광고", font_size=16, weight=BOLD, color=WHITE)
        badge = RoundedRectangle(width=0.62, height=0.32, corner_radius=0.08)
        badge.set_fill(SUBTLE, opacity=1).set_stroke(width=0)
        badge_text.move_to(badge)
        badge_group = VGroup(badge, badge_text)
        badge_group.next_to(title, DOWN, buff=0.18, aligned_edge=LEFT)
        parts.append(badge_group)

    return VGroup(*parts)


def make_phone() -> VGroup:
    """실제 스마트폰처럼 보이는 검색 화면 (베젤·카메라·상태바·옆 버튼).

    쿠팡 앱을 떠올리게 하되 실제 로고·UI는 따라 그리지 않는다.
    반환 순서: (기기 외형, 앱 제목, 검색창, 검색 아이콘). 기기 외형의 첫 요소가 바깥 프레임이다.
    """
    frame = RoundedRectangle(width=3.95, height=7.3, corner_radius=0.55)
    frame.set_fill("#1d1d1f", opacity=1).set_stroke("#3a3a3c", width=2)
    screen = RoundedRectangle(width=3.67, height=7.02, corner_radius=0.44)
    screen.set_fill(PHONE_FILL, opacity=1).set_stroke(width=0)
    screen.move_to(frame)

    buttons = VGroup(
        RoundedRectangle(width=0.06, height=0.7, corner_radius=0.03).next_to(frame, RIGHT, buff=0).shift(UP * 1.6),
        RoundedRectangle(width=0.06, height=0.5, corner_radius=0.03).next_to(frame, LEFT, buff=0).shift(UP * 2.0),
        RoundedRectangle(width=0.06, height=0.5, corner_radius=0.03).next_to(frame, LEFT, buff=0).shift(UP * 1.35),
    ).set_fill("#2c2c2e", opacity=1).set_stroke(width=0)

    camera = RoundedRectangle(width=1.0, height=0.3, corner_radius=0.15)
    camera.set_fill(BLACK, opacity=1).set_stroke(width=0)
    camera.move_to(screen.get_top() + DOWN * 0.3)

    clock = Text("9:41", font_size=18, weight=BOLD, color=INK)
    clock.move_to(screen.get_corner(UL) + RIGHT * 0.65 + DOWN * 0.3)
    status_icons = VGroup(
        load_icon("antenna-bars-5.svg", INK, 0.2),
        load_icon("wifi.svg", INK, 0.2),
        load_icon("battery-3.svg", INK, 0.22),
    ).arrange(RIGHT, buff=0.08)
    status_icons.move_to(screen.get_corner(UR) + LEFT * 0.7 + DOWN * 0.3)

    home_bar = RoundedRectangle(width=1.3, height=0.07, corner_radius=0.035)
    home_bar.set_fill(INK, opacity=1).set_stroke(width=0)
    home_bar.move_to(screen.get_bottom() + UP * 0.16)

    device = VGroup(frame, buttons, screen, camera, clock, status_icons, home_bar)

    header = Text("쿠팡", font_size=26, weight=BOLD, color=INK)
    header.move_to(screen.get_top() + DOWN * 0.78)
    bar = RoundedRectangle(width=3.3, height=0.55, corner_radius=0.27)
    bar.set_fill("#EFEFF2", opacity=1).set_stroke(width=0)
    bar.next_to(header, DOWN, buff=0.2)
    search_icon = load_icon("search.svg", SUBTLE, 0.3)
    search_icon.move_to(bar.get_left() + RIGHT * 0.3)
    return VGroup(device, header, bar, search_icon)


def make_office_worker(height: float = 2.6) -> VGroup:
    """지친 직장인 수영 씨 일러스트 (정장 + 사원증 + 감긴 눈 + 땀방울)."""
    skin = "#F3CDA8"
    hair_color = "#2b2b2e"
    suit = "#34435E"

    jacket = RoundedRectangle(width=2.1, height=1.35, corner_radius=0.55)
    jacket.set_fill(suit, opacity=1).set_stroke(width=0)
    jacket.move_to(DOWN * 1.15)
    shirt = Polygon([-0.36, -0.48, 0], [0.36, -0.48, 0], [0, -1.15, 0])
    shirt.set_fill(WHITE, opacity=1).set_stroke(width=0)
    tie = Polygon([-0.08, -0.52, 0], [0.08, -0.52, 0], [0.11, -1.0, 0], [0, -1.12, 0], [-0.11, -1.0, 0])
    tie.set_fill("#C0504D", opacity=1).set_stroke(width=0)
    neck = Rectangle(width=0.36, height=0.3).set_fill(skin, opacity=1).set_stroke(width=0)
    neck.move_to(DOWN * 0.42)

    hair_back = Ellipse(width=1.22, height=0.9).set_fill(hair_color, opacity=1).set_stroke(width=0)
    hair_back.move_to(UP * 0.3)
    head = Circle(radius=0.56).set_fill(skin, opacity=1).set_stroke(width=0)
    fringe = Ellipse(width=1.02, height=0.38).set_fill(hair_color, opacity=1).set_stroke(width=0)
    fringe.move_to(UP * 0.4)

    # 지친 표정: 아래로 처진 감긴 눈 + 살짝 내려간 입꼬리
    eyes = VGroup(*[
        Arc(radius=0.09, start_angle=PI, angle=PI, stroke_color=INK, stroke_width=4).move_to([x, -0.02, 0])
        for x in (-0.2, 0.2)
    ])
    mouth = Arc(radius=0.11, start_angle=PI / 6, angle=2 * PI / 3, stroke_color=INK, stroke_width=4)
    mouth.move_to(DOWN * 0.28)
    sweat = VGroup(
        Circle(radius=0.07),
        Triangle().scale(0.075).shift(UP * 0.07),
    ).set_fill("#7FB3E6", opacity=1).set_stroke(width=0)
    sweat.move_to([0.5, 0.2, 0])

    badge_card = RoundedRectangle(width=0.36, height=0.46, corner_radius=0.05)
    badge_card.set_fill(WHITE, opacity=1).set_stroke("#9aa5b8", width=1.5)
    badge_card.move_to([0.55, -1.3, 0])
    lanyard = VMobject(stroke_color="#5B7DB1", stroke_width=3)
    lanyard.set_points_as_corners([[0.3, -0.55, 0], [0.55, -1.07, 0]])

    worker = VGroup(jacket, shirt, tie, neck, hair_back, head, fringe, eyes, mouth, sweat, lanyard, badge_card)
    worker.height = height
    return worker


def load_filled_icon(filename: str, color: str, height: float) -> SVGMobject:
    """Tabler filled 아이콘 (면 채움). 사람 무리처럼 작게 여러 개 쓸 때 선 아이콘보다 잘 보인다."""
    icon = SVGMobject(str(ASSET_DIR.parent / "filled" / filename))
    icon.set_fill(color, opacity=1).set_stroke(width=0)
    icon.height = height
    return icon


def make_node(text: str, fill: str, width: float = 2.5, height: float = 0.85, font_size: int = 30) -> VGroup:
    """WWDC 다이어그램처럼 테두리 없는 평면 박스 + 흰 글자."""
    box = RoundedRectangle(width=width, height=height, corner_radius=0.16)
    box.set_fill(fill, opacity=1).set_stroke(width=0)
    label = Text(text, font_size=font_size, weight=BOLD, color=WHITE)
    label.move_to(box)
    return VGroup(box, label)


def make_pill(text: str, fill: str, font_size: int = 24) -> VGroup:
    """작은 둥근 태그 (예: 1위 / 2위 노출 라벨)."""
    label = Text(text, font_size=font_size, weight=BOLD, color=WHITE)
    pill = RoundedRectangle(width=label.width + 0.45, height=label.height + 0.28, corner_radius=0.18)
    pill.set_fill(fill, opacity=1).set_stroke(width=0)
    label.move_to(pill)
    return VGroup(pill, label)


def make_chapter_label(text: str) -> Text:
    """좌상단에 계속 떠 있는 작은 챕터 라벨."""
    label = Text(text, font_size=22, color=SUBTLE)
    label.to_corner(UL, buff=0.45)
    return label


class TimedScene(Scene):
    """오디오 chunk 시작 시각에 Beat를 맞추기 위한 공통 기반 Scene."""

    def wait_until(self, t: float):
        remaining = t - self.renderer.time
        if remaining > 0.01:
            self.wait(remaining)


class Scene01_Question(TimedScene):
    """
    Scene 01: Question — 쿠팡 검색 1위 광고 자리는 정말 그만큼의 값어치가 있을까?

    Core Claim:
    검색 결과 맨 위 광고 순서는 광고 경매(CPC 입찰)로 정해진다.
    알고 싶은 것은 "2위 광고를 1위로 올리면 클릭이 얼마나 늘어나는가"라는 위치 자체의 효과다.

    Expected Misconception:
    "1위가 2위보다 클릭이 많으니, 1위로 올리면 그 차이만큼 클릭이 늘어난다."
    (이 Scene에서는 오해를 교정하지 않고 질문만 던진다. 교정은 Scene 02~03 담당.)

    Visual Pivot:
    두 광고 거북이 카드가 1위/2위 자리에 고정돼 있다가,
    2위 카드가 1위 자리로 올라가는 순간 "자리만 바꾸면 클릭은?"이라는 질문으로 바뀐다.

    Scene 경계:
    - 직전 Scene 마지막 문장: 없음 (첫 Scene)
    - 현재 Scene 첫 문장: "직장에서 힘든 하루를 보낸 수영 씨는"
    - 현재 Scene 마지막 문장: "클릭은 얼마나 더 늘어날까요?"
    - 순위별 CTR 숫자(12%, 8%, 5%)는 Scene 02에서 처음 꺼낸다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 [3]: "새로운 광고 캠페인이 실제로 매출을 올려줄까?"처럼 일상 속 인과 질문을 던지는 도입 방식을 따른다.
    - 이 Scene의 쇼핑 화면·상품명은 노트북 데이터가 아닌 설명용 가상 예시다.

    Script Reference:
    src/scripts/ko/01_question.txt  ("값어치"는 TTS 발음 때문에 스크립트에서만 "가버치"로 표기)
    Audio: build/audio/01_question.mp3 (ElevenLabs eleven_multilingual_v2, speed 1.1, 22.93s)

    Asset Reference:
    Tabler Icons (MIT) — antenna-bars-5.svg, wifi.svg, battery-3.svg, battery-1.svg, cloud.svg, clover.svg,
    search.svg, gavel.svg, hand-click.svg. 거북이·직장인·스마트폰은 도형으로 직접 그렸다.

    3Blue1Brown Reference:
    3b1b/_2022/wordle/scenes.py - DrawPhone
    Reason:
    인물 옆에 휴대폰 화면을 띄워 "이 사람이 지금 이 화면을 보고 있다"를 먼저 세운 뒤
    화면 속 내용으로 시선을 옮기는 도입 리듬이 수영 씨 → 쿠팡 검색 화면 흐름과 같아서 참고했다.

    Script-to-Beat Mapping (.timings.json chunk 기준, 문장 경계는 음절 비율로 추정):
      Beat 1 → chunk 1 "직장에서 힘든 하루를 보낸 수영 씨는"            (0.00~약 2.6s)
      Beat 2 → chunk 1 "내일은 좋은 일이 생기길 바라며"                (약 2.6~4.4s)
      Beat 3 → chunk 1 "쿠팡에서 귀여운 행운 거북이를 검색했습니다."    (약 4.4~7.38s)
      Beat 4 → chunk 2 "맨 위 두 칸에는 광고 거북이가 떠 있습니다."      (7.38~약 10.3s)
      Beat 5 → chunk 2 "이 순서는 쿠팡의 씨피씨 입찰, 즉 광고 경매로…"  (약 10.3~14.26s)
      Beat 6 → chunk 3 "그렇다면 1위 자리는 정말 그만큼의 값어치가…"    (14.26~약 18.0s)
      Beat 7 → chunk 3 "2위에 있던 거북이 광고를 1위로 올리면, 클릭은…" (약 18.0s~끝)

    화면 구획 (가로 14.2 x 8):
      좌측 설명 구역 x≈-3.6 (인물 → 경매 라벨 → 질문 순으로 한 번에 하나만)
      우측 휴대폰 x≈+3.1 (Beat 3부터 끝까지 유지되는 기준축)
      순위 라벨(1위/2위)은 휴대폰 바깥 왼쪽에 고정해, 카드가 움직여도 자리 번호는 그대로 남긴다.
    """

    SCENE_BASENAME = "01_question"
    # chunk 안 문장 경계 비율 (음절 수 기준 추정)
    CHUNK1_SPLITS = (0.35, 0.60)
    CHUNK2_SPLIT = 0.42
    CHUNK3_SPLIT = 0.43
    WAIT_TAIL = 0.8

    def construct(self):
        starts, audio_end = load_audio_timings(self.SCENE_BASENAME)
        chunk_ends = starts[1:] + [audio_end]
        c1_len = chunk_ends[0] - starts[0]
        beat2_start = starts[0] + c1_len * self.CHUNK1_SPLITS[0]
        beat3_start = starts[0] + c1_len * self.CHUNK1_SPLITS[1]
        beat5_start = starts[1] + (chunk_ends[1] - starts[1]) * self.CHUNK2_SPLIT
        beat7_start = starts[2] + (chunk_ends[2] - starts[2]) * self.CHUNK3_SPLIT

        # ─── Beat 1: 힘든 하루를 보낸 수영 씨를 소개한다 ───
        # 처리 문장: "직장에서 힘든 하루를 보낸 수영 씨는"
        # 남는 요소: 없음 (첫 화면)
        # 새로 등장: 수영 씨 그룹(정장 차림 직장인 일러스트 + 방전 배터리) — 화면 중앙에서 시작
        # 비워 두는 영역: 우측 전체 (Beat 3에서 휴대폰이 들어올 자리)
        # 단일 핵심 시선: 지친 수영 씨
        person = make_office_worker(height=2.6)
        battery = load_icon("battery-1.svg", RED_C, 0.55)
        battery.next_to(person, UP, buff=0.2)
        suyoung = VGroup(person, battery)
        suyoung.move_to(ORIGIN)

        chapter = make_chapter_label("Part 1 · 1위 자리의 값어치")
        self.play(FadeIn(person, shift=UP * 0.2), FadeIn(chapter), run_time=0.8)
        self.play(FadeIn(battery, shift=DOWN * 0.15), run_time=0.7)
        self.wait_until(beat2_start)

        # ─── Beat 2: 내일은 좋은 일이 생기길 바라는 마음 ───
        # 처리 문장: "내일은 좋은 일이 생기길 바라며"
        # 남는 요소: 수영 씨 (방전 배터리는 생각 구름에 자리를 내주며 사라진다)
        # 새로 등장: 생각 구름 + 네잎클로버 (머리 오른쪽 위)
        # 비워 두는 영역: 우측 하단
        # 단일 핵심 시선: 구름 속 클로버(행운)
        cloud = load_icon("cloud.svg", MUTED, 1.5)
        cloud.next_to(person, UR, buff=0.1)
        clover = load_icon("clover.svg", GREEN_D, 0.6)
        clover.move_to(cloud.get_center() + DOWN * 0.05)
        dots = VGroup(*[
            Dot(radius=r, color=MUTED) for r in (0.05, 0.075)
        ]).arrange(UR, buff=0.08)
        dots.next_to(person, UR, buff=-0.15)
        wish = VGroup(dots, cloud, clover)

        self.play(FadeOut(battery), FadeIn(dots, lag_ratio=0.5), run_time=0.5)
        # 그룹째 이동할 때 사라진 배터리가 다시 붙지 않도록 그룹에서도 뺀다.
        suyoung.remove(battery)
        self.play(FadeIn(cloud, scale=0.8), GrowFromCenter(clover), run_time=0.8)
        self.wait_until(beat3_start)

        # ─── Beat 3: 쿠팡에서 행운 거북이를 검색한다 ───
        # 처리 문장: "쿠팡에서 귀여운 행운 거북이를 검색했습니다."
        # 남는 요소: 수영 씨(좌측으로 이동)
        # 지울 요소: 생각 구름 (휴대폰과 시선 경쟁하지 않도록 먼저 정리)
        # 새로 등장: 휴대폰 화면(우측) + 검색창에 '행운 거북이' 타이핑
        # 비워 두는 영역: 휴대폰 아래쪽 결과 영역(아직 비어 있음)
        # 단일 핵심 시선: 검색창에 입력되는 '행운 거북이'
        phone = make_phone()
        phone.move_to(RIGHT * PHONE_X).shift(UP * 0.1)
        device, header, bar, search_icon = phone
        body = device[0]
        query = Text("행운 거북이", font_size=24, color=INK)
        query.next_to(search_icon, RIGHT, buff=0.2)

        self.play(
            FadeOut(wish),
            suyoung.animate.move_to(RIGHT * LEFT_ZONE_X),
            FadeIn(phone, shift=LEFT * 0.4),
            run_time=1.0,
        )
        self.play(AddTextLetterByLetter(query), run_time=1.0)
        self.play(Indicate(bar, color=HIGHLIGHT_COLOR, scale_factor=1.04), run_time=0.6)
        self.wait_until(starts[1])

        # ─── Beat 4: 맨 위 두 칸은 광고 거북이 ───
        # 처리 문장: "맨 위 두 칸에는 광고 거북이가 떠 있습니다."
        # 남는 요소: 수영 씨(좌), 휴대폰 틀 + 검색창(우)
        # 새로 등장: 검색 결과 카드 3장 (광고 2장 + 흐린 일반 상품 1장), 휴대폰 아래 '설명용 예시'
        # 비워 두는 영역: 휴대폰 바깥 왼쪽 (순위 라벨 자리)
        # 단일 핵심 시선: 맨 위 두 장의 광고 카드
        card_a = make_product_card(AD_A_COLOR, "거북이 A", is_ad=True)
        card_b = make_product_card(AD_B_COLOR, "거북이 B", is_ad=True)
        card_c = make_product_card(None, "일반 상품", is_ad=False)
        cards = VGroup(card_a, card_b, card_c).arrange(DOWN, buff=0.2)
        cards.next_to(bar, DOWN, buff=0.3)
        card_c.set_opacity(0.45)
        example_note = Text("화면은 설명용 예시", font_size=18, color=MUTED)
        example_note.next_to(body, DOWN, buff=0.12)

        self.play(
            LaggedStart(*[FadeIn(card, shift=UP * 0.2) for card in cards], lag_ratio=0.25),
            FadeIn(example_note),
            run_time=1.3,
        )
        ad_box = SurroundingRectangle(VGroup(card_a, card_b), color=HIGHLIGHT_COLOR, buff=0.04)
        self.play(Create(ad_box), run_time=0.7)
        self.wait_until(beat5_start)

        # ─── Beat 5: 이 순서는 CPC 입찰, 즉 광고 경매로 정해진다 ───
        # 처리 문장: "이 순서는 쿠팡의 씨피씨 입찰, 즉 광고 경매로 정해집니다."
        # 남는 요소: 휴대폰 + 카드 (우)
        # 지울 요소: 수영 씨 (좌측 구역을 경매 설명에 넘긴다), 광고 묶음 박스
        # 새로 등장: 순위 라벨 1위/2위 (휴대폰 바깥 왼쪽), 경매봉 + 'CPC 입찰 = 광고 경매' (좌측 구역)
        # 단일 핵심 시선: 경매봉 라벨 → 순위 라벨로 이어지는 '순서'
        rank_1 = Text("1위", font_size=30, weight=BOLD, color=HIGHLIGHT_COLOR)
        rank_2 = Text("2위", font_size=30, weight=BOLD, color=SUBTLE)
        rank_1.next_to(body, LEFT, buff=0.25).match_y(card_a)
        rank_2.next_to(body, LEFT, buff=0.25).match_y(card_b)
        ranks = VGroup(rank_1, rank_2)

        gavel = load_icon("gavel.svg", HIGHLIGHT_COLOR, 1.5)
        auction_title = Text("CPC 입찰", font_size=44, weight=BOLD, color=INK)
        auction_sub = Text("= 광고 경매", font_size=34, color=SUBTLE)
        auction_text = VGroup(auction_title, auction_sub).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        auction = VGroup(gavel, auction_text).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        auction.move_to(ORIGIN).to_edge(LEFT, buff=0.9)

        self.play(FadeOut(suyoung), FadeOut(ad_box), run_time=0.5)
        self.play(
            FadeIn(gavel, shift=DOWN * 0.3),
            Write(auction_text),
            run_time=1.0,
        )
        self.play(Wiggle(gavel, scale_value=1.08), run_time=0.6)
        self.play(FadeIn(ranks, shift=RIGHT * 0.2, lag_ratio=0.3), run_time=0.7)
        self.wait_until(starts[2])

        # ─── Beat 6: 1위 자리는 정말 그만큼의 값어치가 있을까? ───
        # 처리 문장: "그렇다면 1위 자리는 정말 그만큼의 값어치가 있을까요?"
        # 남는 요소: 휴대폰 + 카드 + 순위 라벨 (우)
        # 지울 요소: 경매 그룹 (좌측 구역을 질문에 넘긴다)
        # 새로 등장: 1위 카드 강조 박스, 좌측 질문 '1위 자리의 값어치?'
        # 비워 두는 영역: 좌측 하단 (Beat 7의 클릭 라벨 자리)
        # 단일 핵심 시선: 1위 자리
        slot_box = SurroundingRectangle(card_a, color=HIGHLIGHT_COLOR, buff=0.04, stroke_width=5)
        question_1 = Text("1위 자리,", font_size=46, weight=BOLD, color=HIGHLIGHT_COLOR)
        question_2 = Text("그만큼의 값어치가 있을까?", font_size=34, color=INK)
        question = VGroup(question_1, question_2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        question.move_to(UP * 1.0).to_edge(LEFT, buff=0.9)

        self.play(FadeOut(auction), run_time=0.5)
        self.play(Create(slot_box), FadeIn(question, shift=UP * 0.2), run_time=1.0)
        self.wait_until(beat7_start)

        # ─── Beat 7: 2위 광고를 1위로 올리면 클릭은 얼마나 늘까? ───
        # 처리 문장: "2위에 있던 거북이 광고를 1위로 올리면, 클릭은 얼마나 더 늘어날까요?"
        # 남는 요소: 휴대폰, 순위 라벨(고정), 1위 자리 박스(고정 — '자리'를 뜻함)
        # 지울 요소: Beat 6 질문 (같은 좌측 상단을 새 질문으로 교체)
        # 새로 등장: 카드 A/B 자리 바꾸기, 좌측 '2위 → 1위로 올리면?' + 클릭 아이콘 '+?'
        # 단일 핵심 시선: 1위 자리로 올라가는 거북이 B 카드 → 클릭 '+?'
        swap_q1 = Text(
            "2위 → 1위로 올리면", font_size=40, weight=BOLD, color=INK, t2c={"2위": AD_B_COLOR}
        )
        swap_q2 = Text("클릭은 얼마나 늘까?", font_size=34, color=SUBTLE)
        swap_question = VGroup(swap_q1, swap_q2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        swap_question.move_to(question).align_to(question, LEFT)

        self.play(FadeOut(question, shift=UP * 0.2), FadeIn(swap_question, shift=UP * 0.2), run_time=0.7)
        pos_a, pos_b = card_a.get_center(), card_b.get_center()
        self.play(
            card_b.animate.move_to(pos_a),
            card_a.animate.move_to(pos_b),
            path_arc=-PI / 3,
            run_time=1.3,
        )
        self.play(Indicate(rank_1, color=HIGHLIGHT_COLOR), run_time=0.6)

        click_icon = load_icon("hand-click.svg", AD_B_COLOR, 1.1)
        click_gain = Text("+ ?", font_size=56, weight=BOLD, color=AD_B_COLOR)
        click_group = VGroup(click_icon, click_gain).arrange(RIGHT, buff=0.35)
        click_group.next_to(swap_question, DOWN, buff=0.8, aligned_edge=LEFT)
        self.play(FadeIn(click_icon, shift=UP * 0.2), Write(click_gain), run_time=0.9)
        self.play(Indicate(click_gain, color=HIGHLIGHT_COLOR, scale_factor=1.2), run_time=0.8)

        self.wait_until(audio_end)
        self.wait(self.WAIT_TAIL)


class Scene02_NaiveComparison(TimedScene):
    """
    Scene 02: Naive Comparison — 순위별 클릭률을 그대로 비교하면 1위가 2위보다 4%p 높다.

    Core Claim:
    가상 광고 기록에서 순위별 평균 클릭률은 1위 12%, 2위 8%, 3위 5%로, 위로 갈수록 높다.
    이 단순 비교만 보면 "2위를 1위로 올리면 클릭률이 4%p 오른다"고 읽고 싶어진다.

    Expected Misconception:
    "1위와 2위의 평균 차이 4%p = 2위 광고를 1위로 올렸을 때 생기는 효과."
    (이 Scene은 오해를 질문으로 세우기까지만 한다. 반박과 광고 품질 이야기는 Scene 03 담당.)

    Visual Pivot:
    1위·2위 막대 사이의 '4%p' 괄호가, 1위·2위 막대 위 거북이 A·B가 자리를 바꾸는 순간
    '+4%p ?'라는 질문으로 바뀐다.

    Scene 경계:
    - 직전 Scene 마지막 문장: "클릭은 얼마나 더 늘어날까요?"
    - 현재 Scene 첫 문장: "가상의 광고 기록을 하나 살펴봅시다."
    - 현재 Scene 마지막 문장: "클릭률도 사 퍼센트포인트 오를까요?"
    - "반드시 그렇지는 않다"와 경매가 좋은 광고를 위에 올린다는 설명은 Scene 03에서 꺼낸다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 [14]: "그냥 처치 집단과 비교 집단의 평균을 빼면 안 되나?" — 단순 평균 비교를 먼저 보여주고
      그 숫자를 효과로 읽고 싶게 만드는 흐름을 따른다.
    - 12% / 8% / 5%는 노트북 데이터가 아닌 설명용 가상 값이며 화면에 '가상 값'으로 표시한다.

    Script Reference:
    src/scripts/ko/02_naive_comparison.txt
    Audio: build/audio/02_naive_comparison.mp3 (ElevenLabs eleven_multilingual_v2, speed 1.1, 23.02s)

    Asset Reference:
    Tabler Icons (MIT) — file-analytics.svg(outline), user.svg(filled), hand-click.svg

    3Blue1Brown Reference:
    3b1b/_2020/med_test.py - LearnAboutPositiveResult (Scene 01 docstring 참조 영상과 같은 계열)
    Reason:
    결과 숫자를 먼저 또렷하게 보여준 뒤 그 숫자를 결론으로 읽고 싶게 만드는 리듬이
    '평균 차이 4%p → 올리면 4%p?' 흐름과 같아서 참고했다.
    톤앤매너는 Scene 01과 같은 WWDC 슬라이드 스타일(평면 막대, 회색 + 주황 강조 하나)을 따른다.

    Script-to-Beat Mapping (.timings.json chunk 기준, 문장 경계는 음절 비율로 추정):
      Beat 1 → chunk 1 "가상의 광고 기록을 하나 살펴봅시다."                  (0.00~약 2.5s)
      Beat 2 → chunk 1 "광고를 본 사람 중 몇 퍼센트가 눌렀는지, 즉 클릭률을…" (약 2.5~7.7s)
      Beat 3 → chunk 1 "1위 광고는 십이 퍼센트, 2위는 팔 퍼센트, 3위는 오…"   (약 7.7~13.0s)
      Beat 4 → chunk 2 "위로 갈수록 클릭률이 높아지네요."                     (13.0~약 15.2s)
      Beat 5 → chunk 2 "1위와 2위의 차이는 사 퍼센트포인트입니다."             (약 15.2~17.74s)
      Beat 6 → chunk 3 "그렇다면 2위 거북이 광고를 1위로 올리기만 하면,"       (17.74~약 20.9s)
      Beat 7 → chunk 3 "클릭률도 사 퍼센트포인트 오를까요?"                   (약 20.9s~끝)

    직전 Scene에서 이어받는 시각 요소:
      Scene 01 마지막 화면(우측 휴대폰, 1위 자리에 거북이 B, 주황 1위 박스)에서 시작해
      휴대폰을 치우고 같은 주황 = 1위, 금색 = 거북이 B 색 의미를 막대 그래프로 넘긴다.

    화면 구획 (가로 14.2 x 8):
      좌상단 챕터 라벨 / 제목 '순위별 클릭률'은 좌측 상단(왼쪽 정렬)
      막대 그래프는 중앙~우측 (1위·2위·3위 = 왼쪽→오른쪽), 1위 막대 왼쪽은 4%p 괄호 자리로 비워 둔다.
    """

    SCENE_BASENAME = "02_naive_comparison"
    CHUNK1_SPLITS = (0.19, 0.59)
    CHUNK2_SPLIT = 0.46
    CHUNK3_SPLIT = 0.60
    WAIT_TAIL = 0.8

    # 가상 값 (%). 화면의 막대 높이와 숫자 라벨이 모두 여기서 나온다.
    CTR_BY_RANK = {"1위": 12, "2위": 8, "3위": 5}
    BAR_UNIT = 0.36       # 1%p 당 막대 높이
    BASELINE_Y = -2.7
    BAR_XS = (0.2, 2.6, 5.0)

    def build_scene01_end_state(self) -> VGroup:
        """Scene 01 마지막 화면의 휴대폰 부분을 그대로 다시 세운다 (1위 자리에 거북이 B)."""
        phone = make_phone()
        phone.move_to(RIGHT * PHONE_X).shift(UP * 0.1)
        device, header, bar, search_icon = phone
        body = device[0]
        query = Text("행운 거북이", font_size=24, color=INK)
        query.next_to(search_icon, RIGHT, buff=0.2)
        card_b = make_product_card(AD_B_COLOR, "거북이 B", is_ad=True)
        card_a = make_product_card(AD_A_COLOR, "거북이 A", is_ad=True)
        card_c = make_product_card(None, "일반 상품", is_ad=False)
        cards = VGroup(card_b, card_a, card_c).arrange(DOWN, buff=0.2)
        cards.next_to(bar, DOWN, buff=0.3)
        card_c.set_opacity(0.45)
        example_note = Text("화면은 설명용 예시", font_size=18, color=MUTED)
        example_note.next_to(body, DOWN, buff=0.12)
        rank_1 = Text("1위", font_size=30, weight=BOLD, color=HIGHLIGHT_COLOR)
        rank_2 = Text("2위", font_size=30, weight=BOLD, color=SUBTLE)
        rank_1.next_to(body, LEFT, buff=0.25).match_y(card_b)
        rank_2.next_to(body, LEFT, buff=0.25).match_y(card_a)
        slot_box = SurroundingRectangle(card_b, color=HIGHLIGHT_COLOR, buff=0.04, stroke_width=5)

        # Scene 01 마지막 좌측 질문과 클릭 '+?'도 같은 자리에 다시 세워 Scene 경계에서 화면이 튀지 않게 한다.
        swap_q1 = Text(
            "2위 → 1위로 올리면", font_size=40, weight=BOLD, color=INK, t2c={"2위": AD_B_COLOR}
        )
        swap_q2 = Text("클릭은 얼마나 늘까?", font_size=34, color=SUBTLE)
        swap_question = VGroup(swap_q1, swap_q2).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        swap_question.move_to(UP * 1.0).to_edge(LEFT, buff=0.9)
        click_icon = load_icon("hand-click.svg", AD_B_COLOR, 1.1)
        click_gain = Text("+ ?", font_size=56, weight=BOLD, color=AD_B_COLOR)
        click_group = VGroup(click_icon, click_gain).arrange(RIGHT, buff=0.35)
        click_group.next_to(swap_question, DOWN, buff=0.8, aligned_edge=LEFT)
        return VGroup(phone, query, cards, example_note, rank_1, rank_2, slot_box, swap_question, click_group)

    def construct(self):
        starts, audio_end = load_audio_timings(self.SCENE_BASENAME)
        chunk_ends = starts[1:] + [audio_end]
        c1_len = chunk_ends[0] - starts[0]
        beat2_start = starts[0] + c1_len * self.CHUNK1_SPLITS[0]
        beat3_start = starts[0] + c1_len * self.CHUNK1_SPLITS[1]
        beat5_start = starts[1] + (chunk_ends[1] - starts[1]) * self.CHUNK2_SPLIT
        beat7_start = starts[2] + (chunk_ends[2] - starts[2]) * self.CHUNK3_SPLIT

        chapter = make_chapter_label("Part 1 · 1위 자리의 값어치")
        phone_state = self.build_scene01_end_state()
        self.add(chapter, phone_state)

        # ─── Beat 1: 가상의 광고 기록을 펼친다 ───
        # 처리 문장: "가상의 광고 기록을 하나 살펴봅시다."
        # 남는 요소: 챕터 라벨
        # 지울 요소: Scene 01의 마지막 화면 전체 (휴대폰 + 좌측 질문, 오른쪽으로 빠지며 퇴장)
        # 새로 등장: 기록 아이콘 + '가상의 광고 기록' (화면 중앙)
        # 비워 두는 영역: 하단 전체
        # 단일 핵심 시선: '가상의 광고 기록' 카드
        record_icon = load_icon("file-analytics.svg", INK, 1.4)
        record_title = Text("가상의 광고 기록", font_size=44, weight=BOLD, color=INK)
        record = VGroup(record_icon, record_title).arrange(RIGHT, buff=0.45)
        record.move_to(ORIGIN)

        self.play(FadeOut(phone_state, shift=RIGHT * 0.6), run_time=0.7)
        self.play(FadeIn(record, shift=UP * 0.2), run_time=0.7)
        self.wait_until(beat2_start)

        # ─── Beat 2: 클릭률 = 광고를 본 사람 중 누른 사람의 비율 ───
        # 처리 문장: "광고를 본 사람 중 몇 퍼센트가 눌렀는지, 즉 클릭률을 순위별로 모아 보면"
        # 남는 요소: 챕터 라벨
        # 지울 요소: 기록 카드
        # 새로 등장: 광고를 본 사람 10명 줄(중앙) → 그중 1명이 주황으로 바뀌며 클릭 아이콘, 아래 '누른 비율 = 클릭률'
        # 비워 두는 영역: 좌우 가장자리
        # 단일 핵심 시선: 사람 줄 중 주황으로 바뀌는 한 명 → 아래 정의
        viewers = VGroup(*[load_filled_icon("user.svg", MUTED, 0.75) for _ in range(10)])
        viewers.arrange(RIGHT, buff=0.32).move_to(UP * 0.5)
        viewers_label = Text("광고를 본 사람", font_size=30, color=SUBTLE)
        viewers_label.next_to(viewers, UP, buff=0.45).align_to(viewers, LEFT)
        clicker = viewers[3]
        click_icon = load_icon("hand-click.svg", HIGHLIGHT_COLOR, 0.6)
        click_icon.next_to(clicker, DR, buff=-0.05)
        definition = Text(
            "그중 누른 사람의 비율 = 클릭률 (CTR)",
            font_size=34,
            weight=BOLD,
            color=INK,
            t2c={"클릭률 (CTR)": HIGHLIGHT_COLOR},
        )
        definition.next_to(viewers, DOWN, buff=0.9)

        self.play(FadeOut(record, shift=UP * 0.2), run_time=0.5)
        self.play(
            LaggedStart(*[FadeIn(v, shift=UP * 0.15) for v in viewers], lag_ratio=0.08),
            FadeIn(viewers_label),
            run_time=1.2,
        )
        self.play(clicker.animate.set_fill(HIGHLIGHT_COLOR), FadeIn(click_icon, scale=0.6), run_time=0.6)
        self.play(Write(definition), run_time=1.1)
        self.wait_until(beat3_start)

        # ─── Beat 3: 순위별 클릭률 1위 12%, 2위 8%, 3위 5% ───
        # 처리 문장: "1위 광고는 십이 퍼센트, 2위는 팔 퍼센트, 3위는 오 퍼센트입니다."
        # 남는 요소: 챕터 라벨
        # 지울 요소: 사람 줄 + 정의 문장 (막대 그래프와 시선 경쟁하지 않게 먼저 비운다)
        # 새로 등장: 좌상단 제목 '순위별 클릭률' + '가상 값', 기준선, 막대 3개(1위 주황, 2·3위 회색)가 순서대로 솟음
        # 비워 두는 영역: 1위 막대 왼쪽 (Beat 5의 4%p 괄호 자리)
        # 단일 핵심 시선: 순서대로 올라오는 막대 숫자
        definition_group = VGroup(viewers, viewers_label, click_icon, definition)
        title = Text("순위별 클릭률", font_size=40, weight=BOLD, color=INK)
        virtual_note = Text("가상 값", font_size=22, color=MUTED)
        heading = VGroup(title, virtual_note).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        heading.move_to(UP * 2.2).to_edge(LEFT, buff=0.9)

        baseline = Line(
            [self.BAR_XS[0] - 1.2, self.BASELINE_Y, 0],
            [self.BAR_XS[-1] + 1.2, self.BASELINE_Y, 0],
            stroke_color="#C8C8CC",
            stroke_width=2,
        )
        bars, value_labels, rank_labels = VGroup(), VGroup(), VGroup()
        for x, (rank, ctr) in zip(self.BAR_XS, self.CTR_BY_RANK.items()):
            color = HIGHLIGHT_COLOR if rank == "1위" else "#B9B9BE"
            bar = Rectangle(width=1.5, height=ctr * self.BAR_UNIT)
            bar.set_fill(color, opacity=1).set_stroke(width=0)
            bar.move_to([x, self.BASELINE_Y, 0], aligned_edge=DOWN)
            value = Text(f"{ctr}%", font_size=36, weight=BOLD, color=HIGHLIGHT_COLOR if rank == "1위" else INK)
            value.next_to(bar, UP, buff=0.2)
            rank_label = Text(rank, font_size=28, color=SUBTLE)
            rank_label.next_to([x, self.BASELINE_Y, 0], DOWN, buff=0.25)
            bars.add(bar)
            value_labels.add(value)
            rank_labels.add(rank_label)

        self.play(FadeOut(definition_group), run_time=0.5)
        self.play(FadeIn(heading, shift=RIGHT * 0.2), Create(baseline), FadeIn(rank_labels), run_time=0.8)
        for bar, value in zip(bars, value_labels):
            self.play(GrowFromEdge(bar, DOWN), FadeIn(value, shift=UP * 0.15), run_time=0.75)
            self.wait(0.35)
        self.wait_until(starts[1])

        # ─── Beat 4: 위로 갈수록 클릭률이 높아진다 ───
        # 처리 문장: "위로 갈수록 클릭률이 높아지네요."
        # 남는 요소: 제목, 막대 그래프 전체
        # 새로 등장: 3위 → 1위 막대 꼭대기를 잇는 점선 상승 화살표
        # 단일 핵심 시선: 오른쪽 아래에서 왼쪽 위로 올라가는 화살표
        trend = DashedVMobject(
            Arrow(
                value_labels[2].get_top() + UP * 0.15,
                value_labels[0].get_right() + RIGHT * 0.3 + UP * 0.25,
                buff=0.1,
                stroke_width=4,
                color=SUBTLE,
                max_tip_length_to_length_ratio=0.08,
            ),
            num_dashes=18,
        )
        self.play(Create(trend), run_time=1.0)
        self.wait_until(beat5_start)

        # ─── Beat 5: 1위와 2위의 차이는 4%p ───
        # 처리 문장: "1위와 2위의 차이는 사 퍼센트포인트입니다."
        # 남는 요소: 제목, 막대 그래프
        # 지울 요소: 상승 화살표 (괄호와 겹치는 시선을 정리)
        # 새로 등장: 2위 높이에서 1위 막대까지 그은 점선, 1위 막대 왼쪽의 괄호 + '4%p'
        # 단일 핵심 시선: 1위 막대 윗부분의 4%p 구간
        bar_1, bar_2 = bars[0], bars[1]
        level_2 = DashedLine(
            [bar_1.get_left()[0] - 0.15, bar_2.get_top()[1], 0],
            bar_2.get_corner(UL),
            dash_length=0.12,
            stroke_color=SUBTLE,
            stroke_width=2.5,
        )
        gap_brace = BraceBetweenPoints(
            [bar_1.get_left()[0] - 0.2, bar_1.get_top()[1], 0],
            [bar_1.get_left()[0] - 0.2, bar_2.get_top()[1], 0],
            direction=LEFT,
            color=INK,
        )
        gap_label = Text("4%p", font_size=40, weight=BOLD, color=INK)
        gap_label.next_to(gap_brace, LEFT, buff=0.15)

        self.play(FadeOut(trend), run_time=0.4)
        self.play(Create(level_2), run_time=0.6)
        self.play(GrowFromCenter(gap_brace), FadeIn(gap_label, shift=RIGHT * 0.15), run_time=0.8)
        self.wait_until(starts[2])

        # ─── Beat 6: 2위 거북이 광고를 1위로 올리기만 하면 ───
        # 처리 문장: "그렇다면 2위 거북이 광고를 1위로 올리기만 하면,"
        # 남는 요소: 제목, 막대 그래프, 4%p 괄호
        # 새로 등장: 1위 막대 위 거북이 A, 2위 막대 위 거북이 B → 둘이 자리를 바꾼다
        #           (Scene 01 휴대폰 속 카드 자리 바꾸기를 그래프 위에서 그대로 반복)
        # 단일 핵심 시선: 1위 자리로 올라가는 거북이 B
        turtle_a = make_turtle(AD_A_COLOR, height=0.75)
        turtle_b = make_turtle(AD_B_COLOR, height=0.75)
        turtle_a.next_to(value_labels[0], UP, buff=0.12)
        turtle_b.next_to(value_labels[1], UP, buff=0.12)
        self.play(
            LaggedStart(FadeIn(turtle_a, shift=DOWN * 0.2), FadeIn(turtle_b, shift=DOWN * 0.2), lag_ratio=0.3),
            run_time=0.7,
        )
        pos_1, pos_2 = turtle_a.get_center(), turtle_b.get_center()
        self.play(
            turtle_b.animate.move_to(pos_1),
            turtle_a.animate.move_to(pos_2),
            path_arc=-PI / 2.5,
            run_time=1.2,
        )
        self.wait_until(beat7_start)

        # ─── Beat 7: 클릭률도 4%p 오를까? ───
        # 처리 문장: "클릭률도 사 퍼센트포인트 오를까요?"
        # 남는 요소: 막대 그래프, 괄호, 자리를 바꾼 거북이 B(1위)·A(2위)
        # 지울 요소: '4%p' 라벨 (같은 자리에서 '+4%p ?'로 바뀐다)
        # 단일 핵심 시선: 주황 '+4%p ?'
        gap_question = Text("+4%p ?", font_size=44, weight=BOLD, color=HIGHLIGHT_COLOR)
        gap_question.next_to(gap_brace, LEFT, buff=0.15)
        self.play(ReplacementTransform(gap_label, gap_question), run_time=0.7)
        self.play(Indicate(gap_question, color=HIGHLIGHT_COLOR, scale_factor=1.15), run_time=0.9)

        self.wait_until(audio_end)
        self.wait(self.WAIT_TAIL)


class Scene03_SelectionTrap(TimedScene):
    """
    Scene 03: Selection Trap — 4%p 안에는 '자리 효과'와 '광고가 원래 좋아서'가 섞여 있다.

    Core Claim:
    광고 경매는 보통 입찰가뿐 아니라 광고 품질(검색어와 잘 맞는지)도 함께 보므로,
    원래 잘 눌리는 광고가 윗자리에 오르기 쉽다. 그래서 순위별 평균 차이 4%p는 위치 효과와
    광고 자체의 차이가 섞인 값이다. 알고 싶은 것은 "똑같은 광고가 1위였다면?"이라는 반사실 질문이다.

    Expected Misconception:
    "1위와 2위의 평균 클릭률 차이가 곧 자리의 효과다."

    Visual Pivot:
    한 덩어리였던 4%p 막대가 '자리가 좋아서'(주황)와 '광고가 좋아서'(파랑) 두 칸으로 갈라지고,
    두 칸의 경계에 '?'가 붙어 "얼마씩인지 모른다"로 바뀐다.

    Scene 경계:
    - 직전 Scene 마지막 문장: "클릭률도 사 퍼센트포인트 오를까요?"
    - 현재 Scene 첫 문장: "꼭 그렇지는 않습니다."
    - 현재 Scene 마지막 문장: "이것이 바로 인과추론의 질문입니다."
    - 경계 근처 비교(RDD)는 Part 2(Scene 04~)에서 꺼낸다. 여기서는 질문만 세우고 끝낸다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 [17]: 단순 평균 차이 = 인과효과 + 편향. "두 집단은 애초에 비슷한 조건이 아니었다" → 4%p 두 칸 나누기
    - 셀 [19]~[20]: 학교 재정 → 태블릿 도입, 학교 재정 → 시험 성적, 태블릿 → 성적(점선 '알고 싶은 효과')
      그래프를 광고 품질 → 순위, 광고 품질 → 클릭률, 순위 → 클릭률(점선)로 옮겼다.
    - 셀 [8]: 같은 대상의 두 세계를 동시에 볼 수 없다(반사실) → '실제 2위' vs '만약 1위' 거북이 B

    Script Reference:
    src/scripts/ko/03_selection_trap.txt  ("입찰가"는 TTS 발음 때문에 스크립트에서만 "입찰까"로 표기)
    Audio: build/audio/03_selection_trap.mp3 (ElevenLabs eleven_multilingual_v2, speed 1.1, 29.61s)

    Asset Reference:
    Tabler Icons (MIT) — gavel.svg. 노드·막대·거북이는 도형으로 직접 그렸다.

    3Blue1Brown Reference:
    3b1b/_2020/med_test.py - LearnAboutPositiveResult (Scene 01·02와 같은 계열)
    Reason:
    결과 숫자를 보여준 뒤 "그 숫자 안에 무엇이 섞여 있는가"를 쪼개 보이는 전개가 같아서
    리듬만 참고했다. 화면 스타일은 WWDC 슬라이드 톤(평면 박스 + 얇은 화살표)을 유지한다.

    Script-to-Beat Mapping (.timings.json chunk 기준, 문장 경계는 음절 비율로 추정):
      Beat 1 → chunk 1 "꼭 그렇지는 않습니다."                                (0.00~약 1.7s)
      Beat 2 → chunk 1 "광고 경매는 보통 입찰가만 보지 않고,"                    (약 1.7~4.5s)
      Beat 3 → chunk 1 "검색어와 잘 맞는 좋은 광고인지도 함께 따집니다."          (약 4.5~8.3s)
      Beat 4 → chunk 1 "그래서 원래 잘 눌리는 광고가 위로 올라가기 쉽습니다."      (약 8.3~12.21s)
      Beat 5 → chunk 2 "결국 사 퍼센트포인트 안에는 두 가지가 섞여 있습니다."      (12.21~약 15.7s)
      Beat 6 → chunk 2 "자리가 좋아서 생긴 차이와, 광고 자체가 좋아서 생긴 차이"   (약 15.7~19.83s)
      Beat 7 → chunk 3 "우리가 정말 알고 싶은 건 이것입니다."                    (19.83~약 22.3s)
      Beat 8 → chunk 3 "똑같은 거북이 B 광고가 1위에 있었다면, 클릭률은 …"        (약 22.3~27.3s)
      Beat 9 → chunk 3 "이것이 바로 인과추론의 질문입니다."                      (약 27.3s~끝)

    직전 Scene에서 이어받는 시각 요소:
      Scene 02 마지막 화면(순위별 클릭률 막대, 자리를 바꾼 거북이 B·A, '+4%p ?')에서 시작한다.
      주황 = 1위 자리, 금색 = 거북이 B 의미를 유지하고, 새 요소 '광고 품질'에만 파랑을 하나 더 쓴다.

    화면 구획 (가로 14.2 x 8):
      Beat 2~4: 중앙 경매 다이어그램 (왼쪽 입력 박스 2개 → 경매봉 → 오른쪽 '순위')
      Beat 5~6: 중앙 4%p 가로 막대 한 개
      Beat 7~9: 왼쪽 교란 그래프(축소), 오른쪽 '실제 2위 / 만약 1위' 거북이 B, 하단 중앙 결론 문장
    """

    SCENE_BASENAME = "03_selection_trap"
    CHUNK1_SPLITS = (0.14, 0.37, 0.68)
    CHUNK2_SPLIT = 0.46
    CHUNK3_SPLITS = (0.25, 0.77)
    WAIT_TAIL = 0.8

    def build_scene02_end_state(self) -> tuple[VGroup, Text]:
        """Scene 02 마지막 화면(막대 그래프 + 거북이 + '+4%p ?')을 같은 좌표로 다시 세운다."""
        s2 = Scene02_NaiveComparison
        title = Text("순위별 클릭률", font_size=40, weight=BOLD, color=INK)
        virtual_note = Text("가상 값", font_size=22, color=MUTED)
        heading = VGroup(title, virtual_note).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        heading.move_to(UP * 2.2).to_edge(LEFT, buff=0.9)
        baseline = Line(
            [s2.BAR_XS[0] - 1.2, s2.BASELINE_Y, 0],
            [s2.BAR_XS[-1] + 1.2, s2.BASELINE_Y, 0],
            stroke_color="#C8C8CC",
            stroke_width=2,
        )
        bars, value_labels, rank_labels = VGroup(), VGroup(), VGroup()
        for x, (rank, ctr) in zip(s2.BAR_XS, s2.CTR_BY_RANK.items()):
            color = HIGHLIGHT_COLOR if rank == "1위" else "#B9B9BE"
            bar = Rectangle(width=1.5, height=ctr * s2.BAR_UNIT)
            bar.set_fill(color, opacity=1).set_stroke(width=0)
            bar.move_to([x, s2.BASELINE_Y, 0], aligned_edge=DOWN)
            value = Text(f"{ctr}%", font_size=36, weight=BOLD, color=HIGHLIGHT_COLOR if rank == "1위" else INK)
            value.next_to(bar, UP, buff=0.2)
            rank_label = Text(rank, font_size=28, color=SUBTLE)
            rank_label.next_to([x, s2.BASELINE_Y, 0], DOWN, buff=0.25)
            bars.add(bar)
            value_labels.add(value)
            rank_labels.add(rank_label)
        bar_1, bar_2 = bars[0], bars[1]
        level_2 = DashedLine(
            [bar_1.get_left()[0] - 0.15, bar_2.get_top()[1], 0],
            bar_2.get_corner(UL),
            dash_length=0.12,
            stroke_color=SUBTLE,
            stroke_width=2.5,
        )
        gap_brace = BraceBetweenPoints(
            [bar_1.get_left()[0] - 0.2, bar_1.get_top()[1], 0],
            [bar_1.get_left()[0] - 0.2, bar_2.get_top()[1], 0],
            direction=LEFT,
            color=INK,
        )
        gap_question = Text("+4%p ?", font_size=44, weight=BOLD, color=HIGHLIGHT_COLOR)
        gap_question.next_to(gap_brace, LEFT, buff=0.15)
        turtle_b = make_turtle(AD_B_COLOR, height=0.75).next_to(value_labels[0], UP, buff=0.12)
        turtle_a = make_turtle(AD_A_COLOR, height=0.75).next_to(value_labels[1], UP, buff=0.12)
        chart = VGroup(
            heading, baseline, bars, value_labels, rank_labels, level_2, gap_brace, gap_question, turtle_a, turtle_b
        )
        return chart, gap_question

    def construct(self):
        starts, audio_end = load_audio_timings(self.SCENE_BASENAME)
        chunk_ends = starts[1:] + [audio_end]

        def split(chunk: int, ratio: float) -> float:
            return starts[chunk] + (chunk_ends[chunk] - starts[chunk]) * ratio

        beat2_start, beat3_start, beat4_start = (split(0, r) for r in self.CHUNK1_SPLITS)
        beat6_start = split(1, self.CHUNK2_SPLIT)
        beat8_start, beat9_start = (split(2, r) for r in self.CHUNK3_SPLITS)

        chapter = make_chapter_label("Part 1 · 1위 자리의 값어치")
        chart, gap_question = self.build_scene02_end_state()
        self.add(chapter, chart)

        # ─── Beat 1: 꼭 그렇지는 않다 ───
        # 처리 문장: "꼭 그렇지는 않습니다."
        # 남는 요소: Scene 02 마지막 화면 전체
        # 새로 등장: 없음 — '+4%p ?'에 취소선을 긋고 회색으로 식혀 "그대로 믿으면 안 된다"를 보인다
        # 단일 핵심 시선: 취소선이 그어지는 '+4%p ?'
        strike = Line(gap_question.get_left(), gap_question.get_right(), stroke_color=INK, stroke_width=5)
        self.play(Create(strike), gap_question.animate.set_color(MUTED), run_time=0.8)
        self.wait_until(beat2_start)

        # ─── Beat 2: 광고 경매는 입찰가만 보지 않는다 ───
        # 처리 문장: "광고 경매는 보통 입찰가만 보지 않고,"
        # 남는 요소: 챕터 라벨
        # 지울 요소: Scene 02 막대 그래프 전체 + 취소선 (경매 다이어그램에 중앙을 넘긴다)
        # 새로 등장: 왼쪽 '입찰가' 박스 → 화살표 → 경매봉 → 화살표 → '순위' 박스 (중앙 한 줄)
        # 비워 두는 영역: '입찰가' 아래 칸 (Beat 3의 '광고 품질' 자리)
        # 단일 핵심 시선: 입찰가 → 경매 → 순위 흐름
        bid_node = make_node("입찰가", NODE_GREY)
        quality_node = make_node("광고 품질", QUALITY_COLOR)
        inputs = VGroup(bid_node, quality_node).arrange(DOWN, buff=0.7)
        inputs.move_to(LEFT * 4.2)
        gavel = load_icon("gavel.svg", INK, 1.3).move_to(ORIGIN)
        auction_label = Text("광고 경매", font_size=26, color=SUBTLE).next_to(gavel, DOWN, buff=0.25)
        rank_node = make_node("순위", HIGHLIGHT_COLOR, width=2.0).move_to(RIGHT * 4.2)
        arrow_kw = dict(buff=0.25, stroke_width=4, max_tip_length_to_length_ratio=0.12)
        bid_arrow = Arrow(bid_node.get_right(), gavel.get_left(), color=NODE_GREY, **arrow_kw)
        quality_arrow = Arrow(quality_node.get_right(), gavel.get_left(), color=QUALITY_COLOR, **arrow_kw)
        rank_arrow = Arrow(gavel.get_right(), rank_node.get_left(), color=INK, **arrow_kw)

        self.play(FadeOut(VGroup(chart, strike)), run_time=0.6)
        self.play(FadeIn(bid_node, shift=RIGHT * 0.2), run_time=0.5)
        self.play(GrowArrow(bid_arrow), FadeIn(gavel), FadeIn(auction_label), run_time=0.6)
        self.play(GrowArrow(rank_arrow), FadeIn(rank_node, shift=LEFT * 0.2), run_time=0.6)
        self.wait_until(beat3_start)

        # ─── Beat 3: 검색어와 잘 맞는 좋은 광고인지도 함께 따진다 ───
        # 처리 문장: "검색어와 잘 맞는 좋은 광고인지도 함께 따집니다."
        # 남는 요소: 입찰가 → 경매 → 순위 다이어그램
        # 새로 등장: '입찰가' 아래 파란 '광고 품질' 박스 + 경매봉으로 들어가는 파란 화살표, 박스 아래 작은 설명
        # 단일 핵심 시선: 새로 들어오는 파란 '광고 품질'
        quality_note = Text("검색어와 잘 맞는지", font_size=22, color=SUBTLE)
        quality_note.next_to(quality_node, DOWN, buff=0.2)
        self.play(FadeIn(quality_node, shift=RIGHT * 0.2), FadeIn(quality_note), run_time=0.7)
        self.play(GrowArrow(quality_arrow), run_time=0.6)
        self.play(Indicate(quality_node, color=QUALITY_COLOR, scale_factor=1.06), run_time=0.8)
        self.wait_until(beat4_start)

        # ─── Beat 4: 그래서 원래 잘 눌리는 광고가 위로 올라가기 쉽다 ───
        # 처리 문장: "그래서 원래 잘 눌리는 광고가 위로 올라가기 쉽습니다."
        # 남는 요소: 경매 다이어그램
        # 새로 등장: 광고 품질 → 경매 → 순위 경로가 파랑으로 물들고, '순위' 옆 위쪽 화살표 + '윗자리'
        # 단일 핵심 시선: 파랑으로 이어지는 품질 → 순위 경로
        up_arrow = Arrow(DOWN * 0.45, UP * 0.45, buff=0, stroke_width=6, color=QUALITY_COLOR)
        up_arrow.next_to(rank_node, UP, buff=0.25)
        up_label = Text("윗자리", font_size=26, weight=BOLD, color=QUALITY_COLOR)
        up_label.next_to(up_arrow, RIGHT, buff=0.15)
        self.play(
            ShowPassingFlash(quality_arrow.copy().set_stroke(QUALITY_COLOR, width=10), time_width=0.6),
            run_time=0.8,
        )
        self.play(rank_arrow.animate.set_color(QUALITY_COLOR), run_time=0.4)
        self.play(GrowArrow(up_arrow), FadeIn(up_label, shift=UP * 0.15), run_time=0.7)
        self.wait_until(starts[1])

        # ─── Beat 5: 4%p 안에는 두 가지가 섞여 있다 ───
        # 처리 문장: "결국 사 퍼센트포인트 안에는 두 가지가 섞여 있습니다."
        # 남는 요소: 챕터 라벨
        # 지울 요소: 경매 다이어그램 전체
        # 새로 등장: 중앙의 가로 막대 한 개 '1위와 2위의 차이 4%p' (주황 한 덩어리)
        # 단일 핵심 시선: 4%p 막대
        auction_group = VGroup(
            inputs, quality_note, gavel, auction_label, rank_node, bid_arrow, quality_arrow, rank_arrow, up_arrow, up_label
        )
        gap_bar = RoundedRectangle(width=8.0, height=1.1, corner_radius=0.14)
        gap_bar.set_fill(HIGHLIGHT_COLOR, opacity=1).set_stroke(width=0)
        gap_bar.move_to(UP * 0.3)
        gap_title = Text("1위와 2위의 차이", font_size=30, color=SUBTLE)
        gap_value = Text("4%p", font_size=40, weight=BOLD, color=INK)
        gap_head = VGroup(gap_title, gap_value).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        # 위쪽 여백은 Beat 6에서 경계선 위 '?'가 들어갈 자리로 남긴다.
        gap_head.next_to(gap_bar, UP, buff=0.85).align_to(gap_bar, LEFT)

        self.play(FadeOut(auction_group), run_time=0.6)
        self.play(FadeIn(gap_head, shift=UP * 0.15), GrowFromEdge(gap_bar, LEFT), run_time=1.0)
        self.wait_until(beat6_start)

        # ─── Beat 6: 자리가 좋아서 생긴 차이 + 광고 자체가 좋아서 생긴 차이 ───
        # 처리 문장: "자리가 좋아서 생긴 차이와, 광고 자체가 좋아서 생긴 차이입니다."
        # 남는 요소: 4%p 제목
        # 새로 등장: 막대가 주황 '자리가 좋아서' + 파랑 '광고가 좋아서' 두 칸으로 갈라짐, 경계에 '?' (비율은 모름)
        # 단일 핵심 시선: 두 칸으로 갈라진 막대와 경계의 '?'
        split_x = gap_bar.get_left()[0] + gap_bar.width * 0.45
        position_part = Rectangle(width=split_x - gap_bar.get_left()[0], height=gap_bar.height)
        position_part.set_fill(HIGHLIGHT_COLOR, opacity=1).set_stroke(width=0)
        position_part.move_to(gap_bar, aligned_edge=LEFT)
        quality_part = Rectangle(width=gap_bar.get_right()[0] - split_x, height=gap_bar.height)
        quality_part.set_fill(QUALITY_COLOR, opacity=1).set_stroke(width=0)
        quality_part.move_to(gap_bar, aligned_edge=RIGHT)
        position_label = Text("자리가 좋아서", font_size=30, weight=BOLD, color=HIGHLIGHT_COLOR)
        position_label.next_to(position_part, DOWN, buff=0.3)
        quality_label = Text("광고가 좋아서", font_size=30, weight=BOLD, color=QUALITY_COLOR)
        quality_label.next_to(quality_part, DOWN, buff=0.3)
        boundary = DashedLine(
            [split_x, gap_bar.get_top()[1] + 0.15, 0],
            [split_x, gap_bar.get_bottom()[1] - 0.15, 0],
            dash_length=0.1,
            stroke_color=INK,
            stroke_width=3,
        )
        boundary_q = Text("?", font_size=36, weight=BOLD, color=INK).next_to(boundary, UP, buff=0.08)

        self.play(FadeIn(position_part), FadeIn(quality_part), FadeOut(gap_bar), run_time=0.7)
        self.play(FadeIn(position_label, shift=UP * 0.15), FadeIn(quality_label, shift=UP * 0.15), run_time=0.7)
        self.play(Create(boundary), FadeIn(boundary_q, scale=0.7), run_time=0.6)
        self.wait_until(starts[2])

        # ─── Beat 7: 우리가 정말 알고 싶은 건 — 교란 그래프 ───
        # 처리 문장: "우리가 정말 알고 싶은 건 이것입니다."
        # 남는 요소: 챕터 라벨
        # 지울 요소: 4%p 막대 묶음
        # 새로 등장: 광고 품질(위) → 순위(왼쪽 아래), 광고 품질 → 클릭률(오른쪽 아래), 순위 → 클릭률 주황 점선 '알고 싶은 효과'
        # 단일 핵심 시선: 순위 → 클릭률 주황 점선
        split_group = VGroup(gap_head, position_part, quality_part, position_label, quality_label, boundary, boundary_q)
        dag_quality = make_node("광고 품질", QUALITY_COLOR)
        dag_rank = make_node("순위", NODE_GREY, width=2.0)
        dag_ctr = make_node("클릭률", NODE_GREY, width=2.0)
        dag_quality.move_to(UP * 1.6)
        dag_rank.move_to(LEFT * 2.8 + DOWN * 0.9)
        dag_ctr.move_to(RIGHT * 2.8 + DOWN * 0.9)
        edge_kw = dict(buff=0.2, stroke_width=4, color=QUALITY_COLOR, max_tip_length_to_length_ratio=0.1)
        edge_qr = Arrow(dag_quality.get_bottom(), dag_rank.get_top(), **edge_kw)
        edge_qc = Arrow(dag_quality.get_bottom(), dag_ctr.get_top(), **edge_kw)
        edge_rc = DashedVMobject(
            Arrow(dag_rank.get_right(), dag_ctr.get_left(), buff=0.2, stroke_width=5, color=HIGHLIGHT_COLOR),
            num_dashes=14,
        )
        edge_rc_label = Text("알고 싶은 효과", font_size=26, weight=BOLD, color=HIGHLIGHT_COLOR)
        edge_rc_label.next_to(edge_rc, DOWN, buff=0.2)
        dag = VGroup(dag_quality, dag_rank, dag_ctr, edge_qr, edge_qc, edge_rc, edge_rc_label)

        self.play(FadeOut(split_group), run_time=0.5)
        self.play(
            FadeIn(VGroup(dag_quality, dag_rank, dag_ctr), lag_ratio=0.2),
            GrowArrow(edge_qr),
            GrowArrow(edge_qc),
            run_time=0.9,
        )
        self.play(Create(edge_rc), FadeIn(edge_rc_label, shift=UP * 0.1), run_time=0.7)
        self.wait_until(beat8_start)

        # ─── Beat 8: 똑같은 거북이 B가 1위였다면? (반사실) ───
        # 처리 문장: "똑같은 거북이 B 광고가 1위에 있었다면, 클릭률은 얼마나 달라졌을까?"
        # 남는 요소: 교란 그래프 (축소해 왼쪽으로)
        # 새로 등장: 오른쪽에 '1위' 빈 자리(점선 카드) + '2위' 자리(실선 카드)에 거북이 B,
        #           B의 흐린 분신이 1위 자리로 올라가 '만약?', 오른쪽에 '클릭률 ?'
        # 비워 두는 영역: 하단 중앙 (Beat 9 결론 문장 자리)
        # 단일 핵심 시선: 1위 자리로 올라가는 흐린 거북이 B
        slot_kw = dict(width=3.0, height=1.2, corner_radius=0.14)
        slot_1 = RoundedRectangle(**slot_kw).set_fill(WHITE, opacity=1).set_stroke(width=0)
        slot_1_outline = DashedVMobject(RoundedRectangle(**slot_kw).set_stroke(HIGHLIGHT_COLOR, width=3), num_dashes=40)
        slot_2 = RoundedRectangle(**slot_kw).set_fill(WHITE, opacity=1).set_stroke(width=0)
        slots = VGroup(VGroup(slot_1, slot_1_outline), slot_2).arrange(DOWN, buff=0.35)
        slots.move_to(RIGHT * 3.6 + UP * 0.6)
        slot_1_outline.move_to(slot_1)
        rank_1 = Text("1위", font_size=28, weight=BOLD, color=HIGHLIGHT_COLOR).next_to(slot_1, LEFT, buff=0.25)
        rank_2 = Text("2위", font_size=28, weight=BOLD, color=SUBTLE).next_to(slot_2, LEFT, buff=0.25)
        real_b = make_turtle(AD_B_COLOR, height=0.7).move_to(slot_2.get_left() + RIGHT * 0.8)
        real_tag = Text("실제", font_size=24, color=SUBTLE).move_to(slot_2.get_center() + RIGHT * 0.65)
        ghost_b = real_b.copy().set_opacity(0.35)
        ghost_tag = Text("만약?", font_size=24, weight=BOLD, color=HIGHLIGHT_COLOR)
        ghost_tag.move_to(slot_1.get_center() + RIGHT * 0.65)
        ctr_question = Text("클릭률은 얼마나 달라질까?", font_size=30, weight=BOLD, color=INK)
        ctr_question.next_to(slots, DOWN, buff=0.45)

        self.play(dag.animate.scale(0.75).move_to(LEFT * 3.6 + UP * 0.5), run_time=0.8)
        self.play(
            FadeIn(slots),
            FadeIn(VGroup(rank_1, rank_2)),
            FadeIn(real_b, shift=UP * 0.15),
            FadeIn(real_tag),
            run_time=0.7,
        )
        self.add(ghost_b)
        self.play(
            ghost_b.animate.move_to(slot_1.get_left() + RIGHT * 0.8),
            path_arc=-PI / 3,
            run_time=1.0,
        )
        self.play(FadeIn(ghost_tag), Write(ctr_question), run_time=0.9)
        self.wait_until(beat9_start)

        # ─── Beat 9: 이것이 바로 인과추론의 질문 ───
        # 처리 문장: "이것이 바로 인과추론의 질문입니다."
        # 남는 요소: 교란 그래프(왼쪽), 거북이 B 두 자리 + 질문(오른쪽)
        # 새로 등장: 하단 중앙 결론 문장 '인과추론의 질문' (주황 강조)
        # 단일 핵심 시선: 하단 결론 문장
        conclusion = Text("이것이 인과추론의 질문", font_size=42, weight=BOLD, color=INK, t2c={"인과추론": HIGHLIGHT_COLOR})
        conclusion.move_to(DOWN * 3.05)
        self.play(FadeIn(conclusion, shift=UP * 0.2), run_time=0.8)
        self.play(Circumscribe(conclusion, color=HIGHLIGHT_COLOR, buff=0.15), run_time=1.0)

        self.wait_until(audio_end)
        self.wait(self.WAIT_TAIL)


class Scene04_CloseAuction(TimedScene):
    """
    Scene 04: Close Auction — 아슬아슬하게 1위가 된 광고와 2위가 된 광고를 비교한다 (RDD 아이디어).

    Core Claim:
    같은 광고를 두 자리에 동시에 띄울 수는 없지만, 경쟁 광고와의 경매 점수 차이(running variable)가
    0(cutoff)을 아주 조금 넘은 광고와 아주 조금 못 넘은 광고는 품질이 거의 같고 노출 자리(treatment)만 다르다.
    이 cutoff 바로 양옆을 비교하는 방법이 RDD(Regression Discontinuity Design)다.

    Expected Misconception:
    "RDD는 1위 광고 전체와 2위 광고 전체를 비교하는 방법이다." → 경계 바로 양옆만 비교한다.
    "실제 플랫폼에 고정된 기준 점수가 있다." → 기준은 고정 점수가 아니라 '경쟁 광고와의 점수 차이 0'이다.

    Visual Pivot:
    점수 막대 두 개가 '경매 점수 차이' 가로축으로 접히고, 0에 cutoff 세로선이 서면서
    왼쪽은 2위 노출, 오른쪽은 1위 노출 구역으로 갈린다. 그 선 바로 양옆에 거의 같은 거북이 두 마리가 놓인다.

    Scene 경계:
    - 직전 Scene 마지막 문장: "이것이 바로 인과추론의 질문입니다."
    - 현재 Scene 첫 문장: "하지만 같은 광고를 두 자리에 동시에 띄울 수는 없습니다."
    - 현재 Scene 마지막 문장: "RDD, Regression Discontinuity Design이라고 부릅니다."
    - cutoff에서 클릭률이 뛰는 그래프(7.9% → 9.8%)는 Scene 05에서 꺼낸다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 셀 [8]: 같은 대상의 두 세계를 동시에 볼 수 없다 → '두 자리에 동시에 X'
    - 셀 [42]: RCT가 어려울 때의 준실험(Quasi-experiment), 그중 RDD → Part 2의 출발점
    - running variable / cutoff / treatment 정의와 ±0.01 예시는 사용자 제공 설명 자료의 가상 예시를 따랐다.
      80.01점 / 80.00점도 설명용 가상 값이다.

    Script Reference:
    src/scripts/ko/04_close_auction.txt  ("cutoff"는 TTS가 끊어 읽도록 스크립트에서만 "cut off"로 표기)
    Audio: build/audio/04_close_auction.mp3 (ElevenLabs eleven_multilingual_v2, speed 1.1, 34.34s)

    Asset Reference:
    거북이·막대·축·태그는 도형으로 직접 그렸다.

    3Blue1Brown Reference:
    3b1b/_2020/med_test.py - LearnAboutPositiveResult (같은 계열 리듬 유지)
    Reason:
    한 장면 안에서 용어를 하나씩(점수 차이 → running variable → cutoff → treatment) 화면 요소에 붙여 가는
    누적 전개가 같아서 참고했다. 화면 스타일은 WWDC 슬라이드 톤을 유지한다.

    Script-to-Beat Mapping (.timings.json chunk 기준, 문장 경계는 음절 비율로 추정):
      Beat 1  → chunk 1 "하지만 같은 광고를 두 자리에 동시에 띄울 수는 없습니다."     (0.00~약 3.4s)
      Beat 2  → chunk 1 "그래서 경매의 아슬아슬한 순간을 이용합니다."               (약 3.4~6.27s)
      Beat 3  → chunk 2 "경쟁 광고와의 경매 점수 차이를 생각해 봅시다."             (6.27~약 9.8s)
      Beat 4  → chunk 2 "순위를 가르는 이 값을 running variable이라고 하고,"       (약 9.8~13.1s)
      Beat 5  → chunk 2 "점수 차이가 0인 경계를 cutoff라고 합니다."                (약 13.1~16.02s)
      Beat 6  → chunk 3 "cutoff를 아주 조금 넘어 1위가 된 광고와,"                 (16.02~약 18.7s)
      Beat 7  → chunk 3 "아주 조금 못 넘어 2위가 된 광고는 품질이 거의 비슷할 겁니다." (약 18.7~23.5s)
      Beat 8  → chunk 3 "다른 점은 딱 하나, 노출된 자리, 즉 treatment뿐입니다."      (약 23.5~27.21s)
      Beat 9  → chunk 4 "이렇게 cutoff 바로 양옆을 비교해 효과를 찾는 방법을"         (27.21~약 30.7s)
      Beat 10 → chunk 4 "RDD, Regression Discontinuity Design이라고 부릅니다."     (약 30.7s~끝)

    직전 Scene에서 이어받는 시각 요소:
      Scene 03 마지막 화면(교란 그래프, '실제 2위 / 만약 1위' 거북이 B, 결론 문장)에서 시작한다.
      거북이 B의 금색, 1위 = 주황, 품질 = 파랑 의미를 그대로 쓴다. 챕터 라벨만 Part 2로 바뀐다.

    화면 구획 (가로 14.2 x 8):
      상단 중앙 y≈2.6: Beat 10 RDD 타이틀 (그 전까지 비워 둔다)
      중앙: 가로축 y=-1.6, cutoff 세로선 x=0, 거북이 두 마리 x=±1.05
      왼쪽 x≈-4.3: '품질 거의 같음' / 오른쪽 x≈+4.3: 'treatment = 노출 자리'
      축 아래: ±0.01 값, running variable 라벨(가운데), 2위·1위 노출 구역 라벨(양 끝)
    """

    SCENE_BASENAME = "04_close_auction"
    CHUNK1_SPLIT = 0.55
    CHUNK2_SPLITS = (0.36, 0.70)
    CHUNK3_SPLITS = (0.24, 0.67)
    CHUNK4_SPLIT = 0.50
    WAIT_TAIL = 0.8

    AXIS_Y = -1.6
    AXIS_HALF = 5.6
    TURTLE_X = 1.05

    def build_scene03_end_state(self) -> tuple[VGroup, VGroup]:
        """Scene 03 마지막 화면을 같은 좌표로 다시 세운다. (교란 그래프+결론, 거북이 자리 묶음)을 돌려준다."""
        dag_quality = make_node("광고 품질", QUALITY_COLOR)
        dag_rank = make_node("순위", NODE_GREY, width=2.0)
        dag_ctr = make_node("클릭률", NODE_GREY, width=2.0)
        dag_quality.move_to(UP * 1.6)
        dag_rank.move_to(LEFT * 2.8 + DOWN * 0.9)
        dag_ctr.move_to(RIGHT * 2.8 + DOWN * 0.9)
        edge_kw = dict(buff=0.2, stroke_width=4, color=QUALITY_COLOR, max_tip_length_to_length_ratio=0.1)
        edge_rc = DashedVMobject(
            Arrow(dag_rank.get_right(), dag_ctr.get_left(), buff=0.2, stroke_width=5, color=HIGHLIGHT_COLOR),
            num_dashes=14,
        )
        edge_rc_label = Text("알고 싶은 효과", font_size=26, weight=BOLD, color=HIGHLIGHT_COLOR)
        edge_rc_label.next_to(edge_rc, DOWN, buff=0.2)
        dag = VGroup(
            dag_quality,
            dag_rank,
            dag_ctr,
            Arrow(dag_quality.get_bottom(), dag_rank.get_top(), **edge_kw),
            Arrow(dag_quality.get_bottom(), dag_ctr.get_top(), **edge_kw),
            edge_rc,
            edge_rc_label,
        )
        dag.scale(0.75).move_to(LEFT * 3.6 + UP * 0.5)

        slot_kw = dict(width=3.0, height=1.2, corner_radius=0.14)
        slot_1 = RoundedRectangle(**slot_kw).set_fill(WHITE, opacity=1).set_stroke(width=0)
        slot_1_outline = DashedVMobject(RoundedRectangle(**slot_kw).set_stroke(HIGHLIGHT_COLOR, width=3), num_dashes=40)
        slot_2 = RoundedRectangle(**slot_kw).set_fill(WHITE, opacity=1).set_stroke(width=0)
        slots = VGroup(VGroup(slot_1, slot_1_outline), slot_2).arrange(DOWN, buff=0.35)
        slots.move_to(RIGHT * 3.6 + UP * 0.6)
        slot_1_outline.move_to(slot_1)
        rank_1 = Text("1위", font_size=28, weight=BOLD, color=HIGHLIGHT_COLOR).next_to(slot_1, LEFT, buff=0.25)
        rank_2 = Text("2위", font_size=28, weight=BOLD, color=SUBTLE).next_to(slot_2, LEFT, buff=0.25)
        real_b = make_turtle(AD_B_COLOR, height=0.7).move_to(slot_2.get_left() + RIGHT * 0.8)
        real_tag = Text("실제", font_size=24, color=SUBTLE).move_to(slot_2.get_center() + RIGHT * 0.65)
        ghost_b = real_b.copy().set_opacity(0.35).move_to(slot_1.get_left() + RIGHT * 0.8)
        ghost_tag = Text("만약?", font_size=24, weight=BOLD, color=HIGHLIGHT_COLOR)
        ghost_tag.move_to(slot_1.get_center() + RIGHT * 0.65)
        ctr_question = Text("클릭률은 얼마나 달라질까?", font_size=30, weight=BOLD, color=INK)
        ctr_question.next_to(slots, DOWN, buff=0.45)
        conclusion = Text("이것이 인과추론의 질문", font_size=42, weight=BOLD, color=INK, t2c={"인과추론": HIGHLIGHT_COLOR})
        conclusion.move_to(DOWN * 3.05)

        slot_group = VGroup(slots, rank_1, rank_2, real_b, real_tag, ghost_b, ghost_tag)
        return VGroup(dag, ctr_question, conclusion), slot_group

    def construct(self):
        starts, audio_end = load_audio_timings(self.SCENE_BASENAME)
        chunk_ends = starts[1:] + [audio_end]

        def split(chunk: int, ratio: float) -> float:
            return starts[chunk] + (chunk_ends[chunk] - starts[chunk]) * ratio

        beat2_start = split(0, self.CHUNK1_SPLIT)
        beat4_start, beat5_start = (split(1, r) for r in self.CHUNK2_SPLITS)
        beat7_start, beat8_start = (split(2, r) for r in self.CHUNK3_SPLITS)
        beat10_start = split(3, self.CHUNK4_SPLIT)

        chapter_1 = make_chapter_label("Part 1 · 1위 자리의 값어치")
        leftovers, slot_group = self.build_scene03_end_state()
        self.add(chapter_1, leftovers, slot_group)

        # ─── Beat 1: 같은 광고를 두 자리에 동시에 띄울 수는 없다 ───
        # 처리 문장: "하지만 같은 광고를 두 자리에 동시에 띄울 수는 없습니다."
        # 남는 요소: 거북이 B 두 자리 묶음 (가운데로 옮겨 단독 시선)
        # 지울 요소: 교란 그래프, '클릭률은…' 질문, 결론 문장 / 챕터 라벨은 Part 2로 교체
        # 새로 등장: 두 자리 위의 빨간 X
        # 단일 핵심 시선: X가 그어지는 거북이 B 두 자리
        chapter_2 = make_chapter_label("Part 2 · RDD로 풀어보기")
        self.play(
            FadeOut(leftovers),
            ReplacementTransform(chapter_1, chapter_2),
            slot_group.animate.move_to(UP * 0.2),
            run_time=0.9,
        )
        ghost = slot_group[5]
        cross = Cross(slot_group[0], stroke_color=RED_D, stroke_width=8, scale_factor=0.75)
        self.play(ghost.animate.set_opacity(1), run_time=0.4)
        self.play(Create(cross), run_time=0.6)
        self.wait_until(beat2_start)

        # ─── Beat 2: 경매의 아슬아슬한 순간 ───
        # 처리 문장: "그래서 경매의 아슬아슬한 순간을 이용합니다."
        # 남는 요소: 챕터 라벨
        # 지울 요소: 거북이 두 자리 + X
        # 새로 등장: 경매 점수 막대 두 개 (거북이 B 80.01 vs 경쟁 광고 80.00) — 거의 같은 길이
        # 단일 핵심 시선: 끝이 거의 맞닿은 두 막대 끝과 '아슬아슬!'
        score_rows = VGroup()
        for name, color, score, length in (
            ("거북이 B", AD_B_COLOR, "80.01점", 7.02),
            ("경쟁 광고", "#B9B9BE", "80.00점", 7.0),
        ):
            row_name = Text(name, font_size=28, weight=BOLD, color=INK)
            row_bar = RoundedRectangle(width=length, height=0.6, corner_radius=0.1)
            row_bar.set_fill(color, opacity=1).set_stroke(width=0)
            row_score = Text(score, font_size=28, weight=BOLD, color=INK)
            score_rows.add(VGroup(row_name, row_bar, row_score))
        for row in score_rows:
            row_name, row_bar, row_score = row
            row_name.move_to(LEFT * 4.6)
            row_bar.move_to(LEFT * 3.7, aligned_edge=LEFT)
            row_score.next_to(row_bar, RIGHT, buff=0.3)
        score_rows[0].move_to(UP * 0.55, coor_mask=[0, 1, 0])
        score_rows[1].move_to(DOWN * 0.45, coor_mask=[0, 1, 0])
        score_note = Text("경매 점수 · 가상 값", font_size=22, color=MUTED)
        score_note.next_to(score_rows, UP, buff=0.45).align_to(score_rows, LEFT)
        close_call = Text("아슬아슬!", font_size=30, weight=BOLD, color=HIGHLIGHT_COLOR)
        close_call.next_to(score_rows, DOWN, buff=0.45).align_to(score_rows[0][1], RIGHT)

        self.play(FadeOut(VGroup(slot_group, cross)), run_time=0.5)
        self.play(
            FadeIn(score_note),
            *[FadeIn(row[0]) for row in score_rows],
            *[GrowFromEdge(row[1], LEFT) for row in score_rows],
            run_time=0.9,
        )
        self.play(*[FadeIn(row[2], shift=LEFT * 0.15) for row in score_rows], FadeIn(close_call, scale=0.8), run_time=0.6)
        self.wait_until(starts[1])

        # ─── Beat 3: 경쟁 광고와의 경매 점수 차이 ───
        # 처리 문장: "경쟁 광고와의 경매 점수 차이를 생각해 봅시다."
        # 남는 요소: 챕터 라벨
        # 지울 요소: 점수 막대 두 개 (차이 한 값으로 접힌다)
        # 새로 등장: 가로축 하나 (왼쪽 '−' 경쟁 광고보다 낮음, 오른쪽 '+' 높음), 0 눈금
        # 비워 두는 영역: 축 위 전체 (cutoff·거북이 자리), 상단 중앙 (RDD 타이틀 자리)
        # 단일 핵심 시선: 새로 그어지는 '점수 차이' 축
        axis = Arrow(
            [-self.AXIS_HALF, self.AXIS_Y, 0],
            [self.AXIS_HALF, self.AXIS_Y, 0],
            buff=0,
            stroke_width=3,
            color=INK,
            max_tip_length_to_length_ratio=0.02,
        )
        zero_tick = Line([0, self.AXIS_Y - 0.12, 0], [0, self.AXIS_Y + 0.12, 0], stroke_color=INK, stroke_width=3)
        zero_label = Text("0", font_size=26, color=INK).next_to(zero_tick, DOWN, buff=0.15)
        minus_label = Text("경쟁 광고보다 낮음  −", font_size=22, color=SUBTLE)
        minus_label.next_to(axis.get_start(), UP, buff=0.2, aligned_edge=LEFT)
        plus_label = Text("+  경쟁 광고보다 높음", font_size=22, color=SUBTLE)
        plus_label.next_to(axis.get_end(), UP, buff=0.2, aligned_edge=RIGHT)

        self.play(FadeOut(VGroup(score_rows, score_note, close_call), shift=DOWN * 0.3), run_time=0.6)
        self.play(GrowArrow(axis), FadeIn(zero_tick), FadeIn(zero_label), run_time=0.8)
        self.play(FadeIn(minus_label), FadeIn(plus_label), run_time=0.6)
        self.wait_until(beat4_start)

        # ─── Beat 4: 이 값이 running variable ───
        # 처리 문장: "순위를 가르는 이 값을 running variable이라고 하고,"
        # 남는 요소: 축
        # 새로 등장: 축 아래 가운데 'running variable' + '= 경쟁 광고와의 경매 점수 차이'
        # 단일 핵심 시선: running variable 라벨
        rv_title = Text("running variable", font_size=34, weight=BOLD, color=INK)
        rv_sub = Text("= 경쟁 광고와의 경매 점수 차이", font_size=24, color=SUBTLE)
        rv_label = VGroup(rv_title, rv_sub).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        rv_label.move_to([0, self.AXIS_Y - 1.25, 0])
        self.play(FadeIn(rv_label, shift=UP * 0.15), run_time=0.7)
        self.play(Indicate(axis, color=HIGHLIGHT_COLOR, scale_factor=1.0), run_time=0.8)
        self.wait_until(beat5_start)

        # ─── Beat 5: 점수 차이 0 = cutoff ───
        # 처리 문장: "점수 차이가 0인 경계를 cutoff라고 합니다."
        # 남는 요소: 축, running variable 라벨
        # 새로 등장: 0 위 세로 점선 + 'cutoff', 왼쪽 회색·오른쪽 주황 옅은 구역, 축 아래 양 끝 '2위 노출 / 1위 노출'
        # 단일 핵심 시선: 세로 cutoff 선
        cutoff_line = DashedLine([0, self.AXIS_Y, 0], [0, 1.25, 0], dash_length=0.15, stroke_color=INK, stroke_width=4)
        cutoff_label = Text("cutoff", font_size=32, weight=BOLD, color=INK).next_to(cutoff_line, UP, buff=0.15)
        region_h = 1.25 - self.AXIS_Y
        left_region = Rectangle(width=self.AXIS_HALF, height=region_h).set_fill("#B9B9BE", opacity=0.18).set_stroke(width=0)
        left_region.move_to([-self.AXIS_HALF / 2, self.AXIS_Y + region_h / 2, 0])
        right_region = Rectangle(width=self.AXIS_HALF, height=region_h).set_fill(HIGHLIGHT_COLOR, opacity=0.12).set_stroke(width=0)
        right_region.move_to([self.AXIS_HALF / 2, self.AXIS_Y + region_h / 2, 0])
        left_name = Text("2위 노출", font_size=26, weight=BOLD, color=SUBTLE)
        left_name.move_to([-self.AXIS_HALF + 1.0, self.AXIS_Y - 0.5, 0])
        right_name = Text("1위 노출", font_size=26, weight=BOLD, color=HIGHLIGHT_COLOR)
        right_name.move_to([self.AXIS_HALF - 1.0, self.AXIS_Y - 0.5, 0])

        self.play(Create(cutoff_line), FadeIn(cutoff_label, shift=DOWN * 0.15), run_time=0.8)
        self.play(FadeIn(left_region), FadeIn(right_region), FadeIn(left_name), FadeIn(right_name), run_time=0.7)
        self.wait_until(starts[2])

        # ─── Beat 6: cutoff를 아주 조금 넘어 1위가 된 광고 ───
        # 처리 문장: "cutoff를 아주 조금 넘어 1위가 된 광고와,"
        # 남는 요소: 축, cutoff, 구역, 라벨들
        # 새로 등장: cutoff 바로 오른쪽 거북이 + '+0.01' + 주황 '1위' 태그
        # 단일 핵심 시선: cutoff 오른쪽 거북이
        def place_turtle(x: float, value: str, pill_text: str, pill_color: str) -> VGroup:
            turtle = make_turtle(AD_B_COLOR, height=0.7)
            turtle.move_to([x, self.AXIS_Y + 0.6, 0])
            value_label = Text(value, font_size=24, weight=BOLD, color=INK).move_to([x, self.AXIS_Y - 0.5, 0])
            pill = make_pill(pill_text, pill_color).next_to(turtle, UP, buff=0.2)
            return VGroup(turtle, value_label, pill)

        winner = place_turtle(self.TURTLE_X, "+0.01", "1위", HIGHLIGHT_COLOR)
        loser = place_turtle(-self.TURTLE_X, "−0.01", "2위", NODE_GREY)
        self.play(FadeIn(winner[0], shift=DOWN * 0.2), FadeIn(winner[1]), run_time=0.7)
        self.play(FadeIn(winner[2], scale=0.7), run_time=0.5)
        self.wait_until(beat7_start)

        # ─── Beat 7: 아주 조금 못 넘어 2위가 된 광고 — 품질은 거의 같다 ───
        # 처리 문장: "아주 조금 못 넘어 2위가 된 광고는 품질이 거의 비슷할 겁니다."
        # 남는 요소: 1위 거북이
        # 새로 등장: cutoff 바로 왼쪽 같은 모양 거북이 + '−0.01' + 회색 '2위' 태그, 왼쪽 파란 '품질 거의 같음'
        # 단일 핵심 시선: cutoff를 사이에 둔 똑같은 두 거북이
        same_quality = VGroup(
            make_node("광고 품질", QUALITY_COLOR, width=2.2, height=0.7, font_size=24),
            Text("거의 같음", font_size=28, weight=BOLD, color=QUALITY_COLOR),
        ).arrange(DOWN, buff=0.2)
        same_quality.move_to([-4.3, 0.1, 0])
        self.play(FadeIn(loser[0], shift=DOWN * 0.2), FadeIn(loser[1]), FadeIn(loser[2], scale=0.7), run_time=0.8)
        self.play(FadeIn(same_quality, shift=RIGHT * 0.2), run_time=0.7)
        self.play(Indicate(VGroup(winner[0], loser[0]), color=QUALITY_COLOR, scale_factor=1.08), run_time=0.9)
        self.wait_until(beat8_start)

        # ─── Beat 8: 다른 점은 노출된 자리 = treatment ───
        # 처리 문장: "다른 점은 딱 하나, 노출된 자리, 즉 treatment뿐입니다."
        # 남는 요소: 두 거북이, 품질 같음(왼쪽)
        # 새로 등장: 1위·2위 태그를 감싸는 주황 박스, 오른쪽 'treatment = 노출된 자리'
        # 단일 핵심 시선: 태그 박스 → treatment 라벨
        tag_box = SurroundingRectangle(VGroup(winner[2], loser[2]), color=HIGHLIGHT_COLOR, buff=0.15, corner_radius=0.12)
        treatment = VGroup(
            Text("treatment", font_size=34, weight=BOLD, color=HIGHLIGHT_COLOR),
            Text("= 노출된 자리", font_size=26, color=INK),
        ).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        treatment.move_to([4.3, 0.1, 0])
        self.play(Create(tag_box), run_time=0.6)
        self.play(FadeIn(treatment, shift=LEFT * 0.2), run_time=0.7)
        self.wait_until(starts[3])

        # ─── Beat 9: cutoff 바로 양옆을 비교한다 ───
        # 처리 문장: "이렇게 cutoff 바로 양옆을 비교해 효과를 찾는 방법을"
        # 남는 요소: 축, cutoff, 두 거북이
        # 지울 요소: 품질 같음·treatment 라벨, 태그 박스 (양옆 띠에 시선을 모은다)
        # 새로 등장: cutoff 양옆 좁은 띠 강조 (나머지 구역은 흐리게)
        # 단일 핵심 시선: cutoff 바로 양옆 띠
        band = Rectangle(width=self.TURTLE_X * 2 + 1.3, height=region_h + 0.05)
        band.set_fill(HIGHLIGHT_COLOR, opacity=0.0).set_stroke(HIGHLIGHT_COLOR, width=4)
        band.move_to([0, self.AXIS_Y + region_h / 2, 0])
        self.play(FadeOut(VGroup(same_quality, treatment, tag_box)), run_time=0.5)
        self.play(
            Create(band),
            left_region.animate.set_fill(opacity=0.08),
            right_region.animate.set_fill(opacity=0.05),
            run_time=0.8,
        )
        self.wait_until(beat10_start)

        # ─── Beat 10: 이 방법이 RDD ───
        # 처리 문장: "RDD, Regression Discontinuity Design이라고 부릅니다."
        # 남는 요소: 축, cutoff, 띠, 두 거북이
        # 새로 등장: 상단 중앙 RDD 타이틀 (RDD + 영어 풀네임 + 회귀불연속설계)
        # 단일 핵심 시선: RDD 타이틀
        rdd_big = Text("RDD", font_size=72, weight=BOLD, color=HIGHLIGHT_COLOR)
        rdd_names = VGroup(
            Text("Regression Discontinuity Design", font_size=30, weight=BOLD, color=INK),
            Text("회귀불연속설계", font_size=24, color=SUBTLE),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        rdd_title = VGroup(rdd_big, rdd_names).arrange(RIGHT, buff=0.45)
        rdd_title.move_to(UP * 2.65)
        self.play(FadeIn(rdd_big, scale=0.8), run_time=0.6)
        self.play(FadeIn(rdd_names, shift=LEFT * 0.2), run_time=0.7)

        self.wait_until(audio_end)
        self.wait(self.WAIT_TAIL)


class Scene05_JumpAtCutoff(TimedScene):
    """
    Scene 05: Jump at Cutoff — cutoff에서 클릭률 선이 7.9%에서 9.8%로 뛴다. 이 1.9%p가 자리의 효과다.

    Core Claim:
    cutoff 근처 수많은 경매를 (점수 차이, 클릭률) 점으로 찍고 양쪽 추세선을 그으면 cutoff에서 선이 끊기며 뛴다.
    그 수직 간격 1.9%p가 위치 자체의 (국소적) 인과효과이고, 단순 비교 4%p의 절반도 안 된다.

    Expected Misconception:
    "RDD는 -0.01 광고 하나와 +0.01 광고 하나만 비교한다." → 경계 근처 많은 관측치로 양쪽 추세를 추정한다.

    Visual Pivot:
    흩어진 점구름 위에 좌우 추세선이 그어지면, cutoff에서 두 선의 끝이 어긋나 있는 '계단'이 드러난다.
    마지막에 4%p 막대 옆에 1.9%p 막대가 놓이며 단순 비교가 부풀려졌음이 보인다.

    Scene 경계:
    - 직전 Scene 마지막 문장: "RDD, Regression Discontinuity Design이라고 부릅니다."
    - 현재 Scene 첫 문장: "이제 cut off 근처의 수많은 경매를 점으로 찍어 봅시다."
    - 현재 Scene 마지막 문장: "단순 비교로 본 사 퍼센트포인트의 절반도 안 되는 값이죠."
    - RDD의 조건(경계에서 다른 요인 연속, 조작 불가)과 국소성은 Scene 06에서 꺼낸다.

    Notebook / Data Reference:
    - 7.9% / 9.8% / 1.9%p는 사용자 제공 설명 자료의 가상 예시 값이다. 화면에 '가상 값'으로 표시한다.
    - 점구름은 그 두 값을 cutoff 절편으로 갖는 좌우 직선 + 잡음으로 만든 설명용 가상 데이터다 (seed 고정).
    - 4%p는 Scene 02의 단순 비교 값(12% − 8%)을 그대로 이어받는다.
    - 기존 videos/rdd 영상 Scene06Visualization의 "산점도 → 좌우 회귀선 → 절편 차이" 순서를 따랐다.

    Script Reference:
    src/scripts/ko/05_jump_at_cutoff.txt
    Audio: build/audio/05_jump_at_cutoff.mp3 (ElevenLabs eleven_multilingual_v2, speed 1.1, 25.05s)

    3Blue1Brown Reference:
    3b1b/_2020/med_test.py - LearnAboutPositiveResult (같은 계열 리듬 유지)
    Reason:
    숫자 하나(1.9%p)를 그래프 위의 길이로 먼저 보이고 그다음 앞서 본 숫자(4%p)와 길이로 비교하는
    전개가 같아서 참고했다. 화면 스타일은 WWDC 슬라이드 톤을 유지한다.

    Script-to-Beat Mapping (.timings.json chunk 기준, 문장 경계는 음절 비율로 추정):
      Beat 1 → chunk 1 "이제 cut off 근처의 수많은 경매를 점으로 찍어 봅시다."   (0.00~약 3.9s)
      Beat 2 → chunk 1 "가로축은 경매 점수 차이, 세로축은 클릭률입니다."         (약 3.9~7.57s)
      Beat 3 → chunk 2 "양쪽 점들을 따라 선을 그어 보면,"                       (7.57~약 9.9s)
      Beat 4 → chunk 2 "cut off에서 선이 뚝 끊기며 위로 뛰어오릅니다."           (약 9.9~13.2s)
      Beat 5 → chunk 2 "2위 쪽은 칠 점 구 퍼센트, 1위 쪽은 구 점 팔 퍼센트."      (약 13.2~17.1s)
      Beat 6 → chunk 2 "이 일 점 구 퍼센트포인트가 바로 자리 자체의 효과입니다."   (약 17.1~21.18s)
      Beat 7 → chunk 3 "단순 비교로 본 사 퍼센트포인트의 절반도 안 되는 값이죠."   (21.18s~끝)

    직전 Scene에서 이어받는 시각 요소:
      Scene 04 마지막 화면의 가로축(y=-1.6), cutoff 점선(x=0), running variable 라벨을 그대로 두고
      그 위에 세로축 '클릭률'을 세운다. 왼쪽 회색 = 2위 노출, 오른쪽 주황 = 1위 노출 색 의미를 점 색으로 잇는다.

    화면 구획 (가로 14.2 x 8):
      그래프 영역 x∈[-5.6, 5.6], y∈[-1.6, 3.0] / 축 아래 running variable 라벨 유지
      cutoff 왼쪽 위: 7.9%·9.8% 값 라벨 / cutoff 오른쪽: 1.9%p 괄호와 '자리 자체의 효과'
      Beat 7: 그래프를 비우고 중앙에 가로 막대 두 개 (단순 비교 4%p / RDD 1.9%p)
    """

    SCENE_BASENAME = "05_jump_at_cutoff"
    CHUNK1_SPLIT = 0.52
    CHUNK2_SPLITS = (0.17, 0.41, 0.70)
    WAIT_TAIL = 0.8

    AXIS_Y = Scene04_CloseAuction.AXIS_Y
    AXIS_HALF = Scene04_CloseAuction.AXIS_HALF
    # 가상 값: cutoff 바로 왼쪽(2위) / 오른쪽(1위) 클릭률 (%)
    CTR_LEFT = 7.9
    CTR_RIGHT = 9.8
    SLOPE_LEFT = 1.6
    SLOPE_RIGHT = 1.4

    def build_scene04_end_state(self) -> dict:
        """Scene 04 마지막 화면을 같은 좌표로 다시 세운다. 이어 쓸 요소는 이름으로 꺼낸다."""
        s4 = Scene04_CloseAuction
        axis = Arrow(
            [-s4.AXIS_HALF, s4.AXIS_Y, 0],
            [s4.AXIS_HALF, s4.AXIS_Y, 0],
            buff=0,
            stroke_width=3,
            color=INK,
            max_tip_length_to_length_ratio=0.02,
        )
        zero_tick = Line([0, s4.AXIS_Y - 0.12, 0], [0, s4.AXIS_Y + 0.12, 0], stroke_color=INK, stroke_width=3)
        zero_label = Text("0", font_size=26, color=INK).next_to(zero_tick, DOWN, buff=0.15)
        minus_label = Text("경쟁 광고보다 낮음  −", font_size=22, color=SUBTLE)
        minus_label.next_to(axis.get_start(), UP, buff=0.2, aligned_edge=LEFT)
        plus_label = Text("+  경쟁 광고보다 높음", font_size=22, color=SUBTLE)
        plus_label.next_to(axis.get_end(), UP, buff=0.2, aligned_edge=RIGHT)
        rv_label = VGroup(
            Text("running variable", font_size=34, weight=BOLD, color=INK),
            Text("= 경쟁 광고와의 경매 점수 차이", font_size=24, color=SUBTLE),
        ).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        rv_label.move_to([0, s4.AXIS_Y - 1.25, 0])
        cutoff_line = DashedLine([0, s4.AXIS_Y, 0], [0, 1.25, 0], dash_length=0.15, stroke_color=INK, stroke_width=4)
        cutoff_label = Text("cutoff", font_size=32, weight=BOLD, color=INK).next_to(cutoff_line, UP, buff=0.15)
        region_h = 1.25 - s4.AXIS_Y
        left_region = Rectangle(width=s4.AXIS_HALF, height=region_h).set_fill("#B9B9BE", opacity=0.08).set_stroke(width=0)
        left_region.move_to([-s4.AXIS_HALF / 2, s4.AXIS_Y + region_h / 2, 0])
        right_region = Rectangle(width=s4.AXIS_HALF, height=region_h).set_fill(HIGHLIGHT_COLOR, opacity=0.05).set_stroke(width=0)
        right_region.move_to([s4.AXIS_HALF / 2, s4.AXIS_Y + region_h / 2, 0])
        left_name = Text("2위 노출", font_size=26, weight=BOLD, color=SUBTLE)
        left_name.move_to([-s4.AXIS_HALF + 1.0, s4.AXIS_Y - 0.5, 0])
        right_name = Text("1위 노출", font_size=26, weight=BOLD, color=HIGHLIGHT_COLOR)
        right_name.move_to([s4.AXIS_HALF - 1.0, s4.AXIS_Y - 0.5, 0])

        turtles = VGroup()
        for x, value, pill_text, pill_color in (
            (s4.TURTLE_X, "+0.01", "1위", HIGHLIGHT_COLOR),
            (-s4.TURTLE_X, "−0.01", "2위", NODE_GREY),
        ):
            turtle = make_turtle(AD_B_COLOR, height=0.7).move_to([x, s4.AXIS_Y + 0.6, 0])
            value_label = Text(value, font_size=24, weight=BOLD, color=INK).move_to([x, s4.AXIS_Y - 0.5, 0])
            pill = make_pill(pill_text, pill_color).next_to(turtle, UP, buff=0.2)
            turtles.add(VGroup(turtle, value_label, pill))
        band = Rectangle(width=s4.TURTLE_X * 2 + 1.3, height=region_h + 0.05)
        band.set_fill(opacity=0).set_stroke(HIGHLIGHT_COLOR, width=4)
        band.move_to([0, s4.AXIS_Y + region_h / 2, 0])

        rdd_big = Text("RDD", font_size=72, weight=BOLD, color=HIGHLIGHT_COLOR)
        rdd_names = VGroup(
            Text("Regression Discontinuity Design", font_size=30, weight=BOLD, color=INK),
            Text("회귀불연속설계", font_size=24, color=SUBTLE),
        ).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        rdd_title = VGroup(rdd_big, rdd_names).arrange(RIGHT, buff=0.45).move_to(UP * 2.65)

        return dict(
            keep=VGroup(axis, zero_tick, zero_label, rv_label, cutoff_line),
            fade=VGroup(
                minus_label, plus_label, cutoff_label, left_region, right_region,
                left_name, right_name, turtles, band, rdd_title,
            ),
            cutoff_line=cutoff_line,
        )

    def construct(self):
        starts, audio_end = load_audio_timings(self.SCENE_BASENAME)
        chunk_ends = starts[1:] + [audio_end]

        def split(chunk: int, ratio: float) -> float:
            return starts[chunk] + (chunk_ends[chunk] - starts[chunk]) * ratio

        beat2_start = split(0, self.CHUNK1_SPLIT)
        beat4_start, beat5_start, beat6_start = (split(1, r) for r in self.CHUNK2_SPLITS)

        chapter = make_chapter_label("Part 2 · RDD로 풀어보기")
        state = self.build_scene04_end_state()
        self.add(chapter, state["keep"], state["fade"])

        # 그래프 좌표계: Scene 04 가로축과 같은 자리에 x축이 오도록 맞춘다 (점수 차이 −1~1, 클릭률 4~13%)
        plane = Axes(
            x_range=[-1, 1, 0.5],
            y_range=[4, 13, 1],
            x_length=self.AXIS_HALF * 2,
            y_length=4.6,
            tips=False,
            axis_config={"stroke_opacity": 0},
        )
        plane.shift(np.array([-self.AXIS_HALF, self.AXIS_Y, 0]) - plane.c2p(-1, 4))
        y_axis = Arrow(
            plane.c2p(-1, 4), plane.c2p(-1, 13), buff=0, stroke_width=3, color=INK,
            max_tip_length_to_length_ratio=0.03,
        )
        y_label = Text("클릭률", font_size=28, weight=BOLD, color=INK).next_to(y_axis, RIGHT, buff=0.2).align_to(y_axis, UP)
        virtual_note = Text("가상 값", font_size=22, color=MUTED).to_corner(UR, buff=0.45)
        cutoff_tall = DashedLine(
            plane.c2p(0, 4), plane.c2p(0, 13), dash_length=0.15, stroke_color=INK, stroke_width=4,
        )

        rng = np.random.default_rng(7)
        left_x = np.sort(rng.uniform(-1, -0.02, 42))
        right_x = np.sort(rng.uniform(0.02, 1, 42))
        left_y = self.CTR_LEFT + self.SLOPE_LEFT * left_x + rng.normal(0, 0.45, left_x.size)
        right_y = self.CTR_RIGHT + self.SLOPE_RIGHT * right_x + rng.normal(0, 0.45, right_x.size)
        left_dots = VGroup(*[Dot(plane.c2p(x, y), radius=0.055, color="#9C9CA3") for x, y in zip(left_x, left_y)])
        right_dots = VGroup(*[Dot(plane.c2p(x, y), radius=0.055, color=HIGHLIGHT_COLOR) for x, y in zip(right_x, right_y)])
        left_dots.set_opacity(0.75)
        right_dots.set_opacity(0.75)

        # ─── Beat 1: cutoff 근처 수많은 경매를 점으로 ───
        # 처리 문장: "이제 cut off 근처의 수많은 경매를 점으로 찍어 봅시다."
        # 남는 요소: 가로축, 0 눈금, running variable 라벨, cutoff 점선
        # 지울 요소: 거북이 두 마리·태그·띠·구역·RDD 타이틀 등 Scene 04 설명 요소
        # 새로 등장: cutoff 점선이 그래프 높이로 길어지고, 양쪽에 점구름 (왼쪽 회색, 오른쪽 주황)
        # 비워 두는 영역: 오른쪽 위 ('가상 값' 자리)
        # 단일 핵심 시선: 흩뿌려지는 점들
        self.play(
            FadeOut(state["fade"]),
            ReplacementTransform(state["cutoff_line"], cutoff_tall),
            run_time=0.8,
        )
        self.play(
            LaggedStart(*[FadeIn(d, scale=0.5) for d in [*left_dots, *right_dots]], lag_ratio=0.02),
            FadeIn(virtual_note),
            run_time=1.6,
        )
        self.wait_until(beat2_start)

        # ─── Beat 2: 가로축은 점수 차이, 세로축은 클릭률 ───
        # 처리 문장: "가로축은 경매 점수 차이, 세로축은 클릭률입니다."
        # 남는 요소: 점구름, 가로축, running variable 라벨
        # 새로 등장: 왼쪽 세로축 + '클릭률'
        # 단일 핵심 시선: 가로축 라벨 → 새 세로축
        self.play(Indicate(state["keep"][3], color=HIGHLIGHT_COLOR, scale_factor=1.05), run_time=0.8)
        self.play(GrowArrow(y_axis), FadeIn(y_label, shift=RIGHT * 0.15), run_time=0.8)
        self.wait_until(starts[1])

        # ─── Beat 3: 양쪽 점들을 따라 선을 긋는다 ───
        # 처리 문장: "양쪽 점들을 따라 선을 그어 보면,"
        # 남는 요소: 그래프 전체
        # 새로 등장: cutoff 왼쪽 추세선(진회색), 오른쪽 추세선(진주황) — 각각 따로 긋는다
        # 단일 핵심 시선: 그어지는 두 선
        left_line = Line(
            plane.c2p(-1, self.CTR_LEFT - self.SLOPE_LEFT), plane.c2p(0, self.CTR_LEFT),
            stroke_color="#4A4A50", stroke_width=6,
        )
        right_line = Line(
            plane.c2p(0, self.CTR_RIGHT), plane.c2p(1, self.CTR_RIGHT + self.SLOPE_RIGHT),
            stroke_color="#B85C00", stroke_width=6,
        )
        self.play(Create(left_line), run_time=0.9)
        self.play(Create(right_line), run_time=0.9)
        self.wait_until(beat4_start)

        # ─── Beat 4: cutoff에서 선이 뚝 끊기며 위로 뛴다 ───
        # 처리 문장: "cut off에서 선이 뚝 끊기며 위로 뛰어오릅니다."
        # 남는 요소: 점구름(흐리게), 두 추세선
        # 새로 등장: 두 선 끝점 사이를 잇는 주황 위쪽 화살표 (계단)
        # 단일 핵심 시선: cutoff에서 어긋난 두 선 끝
        jump_arrow = Arrow(
            plane.c2p(0, self.CTR_LEFT), plane.c2p(0, self.CTR_RIGHT),
            buff=0.05, stroke_width=6, color=HIGHLIGHT_COLOR, max_tip_length_to_length_ratio=0.25,
        )
        self.play(left_dots.animate.set_opacity(0.25), right_dots.animate.set_opacity(0.25), run_time=0.6)
        self.play(GrowArrow(jump_arrow), run_time=0.7)
        self.play(Flash(plane.c2p(0, self.CTR_RIGHT), color=HIGHLIGHT_COLOR, line_length=0.25), run_time=0.6)
        self.wait_until(beat5_start)

        # ─── Beat 5: 2위 쪽 7.9%, 1위 쪽 9.8% ───
        # 처리 문장: "2위 쪽은 칠 점 구 퍼센트, 1위 쪽은 구 점 팔 퍼센트."
        # 남는 요소: 두 추세선, 점프 화살표
        # 새로 등장: 두 끝점 동그라미 + cutoff 왼쪽에 '7.9%', '9.8%'
        # 단일 핵심 시선: 두 값 라벨
        end_left = Dot(plane.c2p(0, self.CTR_LEFT), radius=0.11, color="#4A4A50")
        end_right = Dot(plane.c2p(0, self.CTR_RIGHT), radius=0.11, color="#B85C00")
        label_left = Text(f"{self.CTR_LEFT}%", font_size=34, weight=BOLD, color="#4A4A50")
        # 왼쪽 추세선이 끝점 왼쪽으로 지나가므로 라벨은 선 아래로 내린다.
        label_left.next_to(end_left, LEFT, buff=0.3).shift(DOWN * 0.55)
        label_right = Text(f"{self.CTR_RIGHT}%", font_size=34, weight=BOLD, color=HIGHLIGHT_COLOR)
        label_right.next_to(end_right, LEFT, buff=0.3).shift(UP * 0.2)
        self.play(FadeIn(end_left, scale=0.5), FadeIn(label_left, shift=RIGHT * 0.15), run_time=0.6)
        self.wait(0.5)
        self.play(FadeIn(end_right, scale=0.5), FadeIn(label_right, shift=RIGHT * 0.15), run_time=0.6)
        self.wait_until(beat6_start)

        # ─── Beat 6: 이 1.9%p가 자리 자체의 효과 ───
        # 처리 문장: "이 일 점 구 퍼센트포인트가 바로 자리 자체의 효과입니다."
        # 남는 요소: 두 추세선, 점프 화살표, 값 라벨
        # 새로 등장: cutoff 오른쪽 괄호 + '1.9%p' + '자리 자체의 효과'
        # 단일 핵심 시선: 1.9%p 괄호
        jump_brace = BraceBetweenPoints(
            plane.c2p(0.06, self.CTR_RIGHT), plane.c2p(0.06, self.CTR_LEFT), direction=RIGHT, color=INK,
        )
        effect = VGroup(
            Text(f"{self.CTR_RIGHT - self.CTR_LEFT:.1f}%p", font_size=44, weight=BOLD, color=HIGHLIGHT_COLOR),
            Text("자리 자체의 효과", font_size=26, weight=BOLD, color=INK),
        ).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        effect.next_to(jump_brace, RIGHT, buff=0.2)
        self.play(GrowFromCenter(jump_brace), run_time=0.6)
        self.play(FadeIn(effect, shift=LEFT * 0.15), run_time=0.7)
        self.wait_until(starts[2])

        # ─── Beat 7: 단순 비교 4%p의 절반도 안 된다 ───
        # 처리 문장: "단순 비교로 본 사 퍼센트포인트의 절반도 안 되는 값이죠."
        # 남는 요소: 챕터 라벨, '가상 값'
        # 지울 요소: 그래프 전체
        # 새로 등장: 중앙 가로 막대 두 개 — '단순 비교 4%p'(회색) / 'RDD 1.9%p'(주황), 길이 비율 그대로
        # 단일 핵심 시선: 4%p 막대 절반에도 못 미치는 1.9%p 막대
        graph = VGroup(
            state["keep"], cutoff_tall, y_axis, y_label, left_dots, right_dots, left_line, right_line,
            jump_arrow, end_left, end_right, label_left, label_right, jump_brace, effect,
        )
        unit = 2.0
        compare_rows = VGroup()
        for name, value, color in (("단순 비교", 4.0, "#B9B9BE"), ("RDD", self.CTR_RIGHT - self.CTR_LEFT, HIGHLIGHT_COLOR)):
            row_name = Text(name, font_size=30, weight=BOLD, color=INK)
            row_bar = RoundedRectangle(width=value * unit, height=0.75, corner_radius=0.12)
            row_bar.set_fill(color, opacity=1).set_stroke(width=0)
            row_value = Text(f"{value:.1f}%p" if value % 1 else f"{value:.0f}%p", font_size=32, weight=BOLD, color=INK)
            compare_rows.add(VGroup(row_name, row_bar, row_value))
        # RDD 값은 '절반' 점선과 겹치지 않도록 막대 안쪽 오른쪽 끝에 흰 글자로 둔다.
        for row, y in zip(compare_rows, (0.7, -0.5)):
            row_name, row_bar, row_value = row
            row_name.move_to([-4.6, y, 0])
            row_bar.move_to([-3.4, y, 0], aligned_edge=LEFT)
            row_value.next_to(row_bar, RIGHT, buff=0.3)
        rdd_value = compare_rows[1][2]
        rdd_value.set_color(WHITE).move_to(compare_rows[1][1].get_right() + LEFT * (rdd_value.width / 2 + 0.25))
        half_mark = DashedLine(
            [-3.4 + 2.0 * unit, 1.3, 0], [-3.4 + 2.0 * unit, -1.1, 0], dash_length=0.12, stroke_color=SUBTLE, stroke_width=3,
        )
        half_label = Text("4%p의 절반", font_size=22, color=SUBTLE).next_to(half_mark, DOWN, buff=0.15)

        self.play(FadeOut(graph), run_time=0.5)
        self.play(
            *[FadeIn(row[0]) for row in compare_rows],
            *[GrowFromEdge(row[1], LEFT) for row in compare_rows],
            *[FadeIn(row[2]) for row in compare_rows],
            run_time=0.9,
        )
        self.play(Create(half_mark), FadeIn(half_label), run_time=0.6)

        self.wait_until(audio_end)
        self.wait(self.WAIT_TAIL)


class Scene06_Conditions(TimedScene):
    """
    Scene 06: Conditions — RDD가 통하려면 cutoff에서 자리 말고는 매끄러워야 하고, 결과는 cutoff 근처에만 해당한다.

    Core Claim:
    (1) cutoff 근처에서 노출 자리 외의 요인(광고 품질 등)이 갑자기 달라지면 안 된다.
        광고주가 경쟁 점수를 정확히 알고 딱 넘길 수 있다면(점수 조작) cutoff 바로 위에 광고가 몰리고 비교가 무너진다.
    (2) RDD 추정치는 cutoff 근처 광고들의 국소적 효과다. 모든 광고에 그대로 일반화할 수 없다.

    Expected Misconception:
    "RDD로 구한 1.9%p는 모든 광고에 똑같이 적용되는 1위 효과다."
    "경계만 있으면 RDD는 언제나 성립한다."

    Visual Pivot:
    왼쪽 카드의 매끄러운 파란 품질선(✓)과, cutoff 바로 위에 막대가 솟은 분포(✗)가 나란히 놓이며
    '경계에서 자리만 달라야 한다'가 그림으로 보인다. 오른쪽 카드에서는 cutoff 근처 띠만 밝고 양 끝은 '?'로 남는다.

    Scene 경계:
    - 직전 Scene 마지막 문장: "단순 비교로 본 사 퍼센트포인트의 절반도 안 되는 값이죠."
    - 현재 Scene 첫 문장: "물론 조건이 있습니다."
    - 현재 Scene 마지막 문장: "모든 광고에 그대로 적용되지는 않습니다."
    - 실제 논문 결과와 광고비 질문은 Scene 07에서 꺼낸다.

    Notebook / Data Reference:
    - 사용자 제공 설명 자료의 "경계 전후에 다른 요인이 불연속적으로 달라지지 않는지 검증",
      "RDD는 경계 근처 광고들의 국소적 인과효과" 문단을 입문자 말로 옮겼다.
    - 기존 videos/rdd 영상 Scene03KeyAssumptions(연속성, 조작 불가)와 같은 조건을 다룬다.
    - 미니 그래프의 선과 막대 모양은 설명용 그림이며 실제 데이터가 아니다.

    Script Reference:
    src/scripts/ko/06_conditions.txt
    Audio: build/audio/06_conditions.mp3 (ElevenLabs eleven_multilingual_v2, speed 1.1, 17.17s)

    Asset Reference:
    Tabler Icons (MIT) — circle-check.svg, circle-x.svg

    3Blue1Brown Reference:
    3b1b/_2020/med_test.py - LearnAboutPositiveResult (같은 계열 리듬 유지)
    Reason:
    결론(1.9%p)을 보인 직후 "이 숫자를 믿으려면 무엇이 필요한가"를 짧은 카드로 정리하는 마무리 리듬을 따랐다.
    화면 스타일은 WWDC 슬라이드 톤(흰 카드, 왼쪽 정렬 제목, 강조색 최소)을 유지한다.

    Script-to-Beat Mapping (.timings.json chunk 기준, 문장 경계는 음절 비율로 추정):
      Beat 1 → chunk 1 "물론 조건이 있습니다."                                       (0.00~약 1.45s)
      Beat 2 → chunk 1 "cut off 근처에서는 자리 말고 다른 것이 갑자기 달라지면 안 됩니다." (약 1.45~5.8s)
      Beat 3 → chunk 1 "광고주가 경쟁 점수를 정확히 알고 딱 넘길 수 있다면, …무너집니다." (약 5.8~11.15s)
      Beat 4 → chunk 2 "또 이 값은 cut off 근처 광고들의 효과일 뿐,"                    (11.15~약 14.3s)
      Beat 5 → chunk 2 "모든 광고에 그대로 적용되지는 않습니다."                        (약 14.3s~끝)

    직전 Scene에서 이어받는 시각 요소:
      Scene 05 마지막 화면(단순 비교 4%p / RDD 1.9%p 막대)에서 시작해, RDD 막대를 지우며 체크리스트로 넘어간다.
      주황 = 1위 노출(cutoff 오른쪽), 파랑 = 광고 품질 의미를 미니 그래프에 그대로 쓴다.

    화면 구획 (가로 14.2 x 8):
      좌상단 제목 y≈2.72 / 왼쪽 카드 x≈-3.5 (조건 ① 두 줄) / 오른쪽 카드 x≈+3.5 (② 국소 효과)
    """

    SCENE_BASENAME = "06_conditions"
    CHUNK1_SPLITS = (0.13, 0.52)
    CHUNK2_SPLIT = 0.53
    WAIT_TAIL = 0.8

    CARD_W = 6.3
    CARD_H = 5.2
    CARD_Y = -0.4

    def make_card(self, x: float, header: str) -> VGroup:
        card = RoundedRectangle(width=self.CARD_W, height=self.CARD_H, corner_radius=0.22)
        card.set_fill(WHITE, opacity=1).set_stroke(width=0)
        card.move_to([x, self.CARD_Y, 0])
        title = Text(header, font_size=28, weight=BOLD, color=INK)
        title.move_to(card.get_corner(UL) + RIGHT * (title.width / 2 + 0.4) + DOWN * 0.5)
        return VGroup(card, title)

    def make_mini_axis(self, center: np.ndarray, width: float = 4.4, height: float = 1.3) -> VGroup:
        """카드 안 작은 그래프 틀: 가로축 + 가운데 cutoff 점선."""
        base = Line(center + LEFT * width / 2 + DOWN * height / 2, center + RIGHT * width / 2 + DOWN * height / 2)
        base.set_stroke(INK, width=2.5)
        cut = DashedLine(center + DOWN * height / 2, center + UP * height / 2, dash_length=0.1)
        cut.set_stroke(INK, width=2.5)
        return VGroup(base, cut)

    def construct(self):
        starts, audio_end = load_audio_timings(self.SCENE_BASENAME)
        chunk_ends = starts[1:] + [audio_end]

        def split(chunk: int, ratio: float) -> float:
            return starts[chunk] + (chunk_ends[chunk] - starts[chunk]) * ratio

        beat2_start, beat3_start = (split(0, r) for r in self.CHUNK1_SPLITS)
        beat5_start = split(1, self.CHUNK2_SPLIT)

        # Scene 05 마지막 화면 (단순 비교 4%p / RDD 1.9%p 막대) 재구성
        chapter = make_chapter_label("Part 2 · RDD로 풀어보기")
        virtual_note = Text("가상 값", font_size=22, color=MUTED).to_corner(UR, buff=0.45)
        unit = 2.0
        rdd_effect = Scene05_JumpAtCutoff.CTR_RIGHT - Scene05_JumpAtCutoff.CTR_LEFT
        compare_rows = VGroup()
        for name, value, color, y in (("단순 비교", 4.0, "#B9B9BE", 0.7), ("RDD", rdd_effect, HIGHLIGHT_COLOR, -0.5)):
            row_name = Text(name, font_size=30, weight=BOLD, color=INK).move_to([-4.6, y, 0])
            row_bar = RoundedRectangle(width=value * unit, height=0.75, corner_radius=0.12)
            row_bar.set_fill(color, opacity=1).set_stroke(width=0).move_to([-3.4, y, 0], aligned_edge=LEFT)
            row_value = Text(f"{value:.1f}%p" if value % 1 else f"{value:.0f}%p", font_size=32, weight=BOLD, color=INK)
            row_value.next_to(row_bar, RIGHT, buff=0.3)
            compare_rows.add(VGroup(row_name, row_bar, row_value))
        rdd_value = compare_rows[1][2]
        rdd_value.set_color(WHITE).move_to(compare_rows[1][1].get_right() + LEFT * (rdd_value.width / 2 + 0.25))
        half_mark = DashedLine(
            [-3.4 + 2.0 * unit, 1.3, 0], [-3.4 + 2.0 * unit, -1.1, 0], dash_length=0.12, stroke_color=SUBTLE, stroke_width=3,
        )
        half_label = Text("4%p의 절반", font_size=22, color=SUBTLE).next_to(half_mark, DOWN, buff=0.15)
        compare = VGroup(compare_rows, half_mark, half_label)
        self.add(chapter, virtual_note, compare)

        # ─── Beat 1: 물론 조건이 있다 ───
        # 처리 문장: "물론 조건이 있습니다."
        # 남는 요소: 챕터 라벨
        # 지울 요소: 비교 막대, '가상 값'
        # 새로 등장: 좌상단 제목 'RDD를 믿으려면'
        # 단일 핵심 시선: 제목
        heading = Text("RDD를 믿으려면", font_size=38, weight=BOLD, color=INK)
        heading.move_to(UP * 2.72).to_edge(LEFT, buff=0.9)
        self.play(FadeOut(compare, shift=DOWN * 0.2), FadeOut(virtual_note), run_time=0.5)
        self.play(FadeIn(heading, shift=RIGHT * 0.2), run_time=0.6)
        self.wait_until(beat2_start)

        # ─── Beat 2: cutoff 근처에서 자리 말고 다른 것이 갑자기 달라지면 안 된다 ───
        # 처리 문장: "cut off 근처에서는 자리 말고 다른 것이 갑자기 달라지면 안 됩니다."
        # 남는 요소: 제목
        # 새로 등장: 왼쪽 카드 '① cutoff에서는 자리만 달라야' + 위쪽 미니 그래프(파란 품질선이 cutoff를 매끄럽게 통과) + ✓
        # 비워 두는 영역: 왼쪽 카드 아래쪽 (Beat 3 미니 그래프 자리), 오른쪽 카드 자리
        # 단일 핵심 시선: cutoff를 끊김 없이 지나가는 파란 선
        card_1 = self.make_card(-3.55, "① cutoff에서는 자리만 달라야")
        plot_a_center = np.array([-3.85, 0.75, 0])
        axis_a = self.make_mini_axis(plot_a_center)
        quality_line = Line(
            plot_a_center + LEFT * 2.2 + DOWN * 0.35, plot_a_center + RIGHT * 2.2 + UP * 0.3,
            stroke_color=QUALITY_COLOR, stroke_width=6,
        )
        quality_label = Text("광고 품질", font_size=20, weight=BOLD, color=QUALITY_COLOR)
        quality_label.next_to(quality_line.get_start(), UP, buff=0.2, aligned_edge=LEFT)
        ok_icon = load_icon("circle-check.svg", OK_COLOR, 0.6).next_to(axis_a, RIGHT, buff=0.25)
        ok_note = Text("매끄럽게 이어짐", font_size=20, color=OK_COLOR)
        ok_note.next_to(axis_a, DOWN, buff=0.15)

        self.play(FadeIn(card_1, shift=UP * 0.2), run_time=0.6)
        self.play(Create(axis_a), run_time=0.5)
        self.play(Create(quality_line), FadeIn(quality_label), run_time=0.9)
        self.play(FadeIn(ok_icon, scale=0.6), FadeIn(ok_note), run_time=0.5)
        self.wait_until(beat3_start)

        # ─── Beat 3: 점수를 정확히 맞춰 넘길 수 있다면 비교가 무너진다 ───
        # 처리 문장: "광고주가 경쟁 점수를 정확히 알고 딱 넘길 수 있다면, 이 비교는 무너집니다."
        # 남는 요소: 제목, 왼쪽 카드 위쪽 그래프 + ✓
        # 새로 등장: 왼쪽 카드 아래쪽 미니 분포 — 고르게 퍼진 광고 막대가, cutoff 바로 오른쪽에서 솟는다 + ✗
        # 단일 핵심 시선: cutoff 바로 위에 솟는 주황 막대
        plot_b_center = np.array([-3.85, -1.45, 0])
        axis_b = self.make_mini_axis(plot_b_center)
        bar_xs = np.linspace(-2.0, 2.0, 11)
        base_y = plot_b_center[1] - 0.65
        spread = VGroup(*[
            Rectangle(width=0.3, height=0.45 + 0.05 * (i % 3)).set_fill("#B9B9BE" if x < 0 else HIGHLIGHT_COLOR, opacity=0.8)
            .set_stroke(width=0).move_to([plot_b_center[0] + x + (0.18 if x >= 0 else -0.18), base_y, 0], aligned_edge=DOWN)
            for i, x in enumerate(bar_xs) if abs(x) > 0.05
        ])
        spike = Rectangle(width=0.3, height=1.25).set_fill(HIGHLIGHT_COLOR, opacity=1).set_stroke(width=0)
        spike.move_to([plot_b_center[0] + 0.18, base_y, 0], aligned_edge=DOWN)
        spike_start = spike.copy().stretch_to_fit_height(0.45, about_edge=DOWN)
        ng_icon = load_icon("circle-x.svg", NG_COLOR, 0.6).next_to(axis_b, RIGHT, buff=0.25)
        ng_note = Text("점수를 맞춰 넘기면 → cutoff 위로 몰림", font_size=20, color=NG_COLOR)
        ng_note.next_to(axis_b, DOWN, buff=0.15)

        self.play(Create(axis_b), FadeIn(spread, lag_ratio=0.05), FadeIn(spike_start), run_time=0.9)
        self.play(Transform(spike_start, spike), run_time=0.8)
        self.play(FadeIn(ng_icon, scale=0.6), FadeIn(ng_note), run_time=0.6)
        self.play(Wiggle(ng_icon, scale_value=1.15), run_time=0.7)
        self.wait_until(starts[1])

        # ─── Beat 4: 이 값은 cutoff 근처 광고들의 효과 ───
        # 처리 문장: "또 이 값은 cut off 근처 광고들의 효과일 뿐,"
        # 남는 요소: 제목, 왼쪽 카드 전체
        # 새로 등장: 오른쪽 카드 '② cutoff 근처의 효과' + 점수 차이 축, cutoff 양옆 주황 띠 '1.9%p는 여기'
        # 비워 두는 영역: 오른쪽 카드의 양 끝 (Beat 5 '?' 자리)
        # 단일 핵심 시선: cutoff 근처 주황 띠
        card_2 = self.make_card(3.55, "② cutoff 근처의 효과")
        line_y = -0.9
        track = Line([3.55 - 2.6, line_y, 0], [3.55 + 2.6, line_y, 0], stroke_color=INK, stroke_width=3)
        cut_2 = DashedLine([3.55, line_y - 0.9, 0], [3.55, line_y + 1.4, 0], dash_length=0.12, stroke_color=INK, stroke_width=3)
        cut_2_label = Text("cutoff", font_size=22, weight=BOLD, color=INK).next_to(cut_2, UP, buff=0.1)
        near_band = RoundedRectangle(width=1.6, height=2.1, corner_radius=0.12)
        near_band.set_fill(HIGHLIGHT_COLOR, opacity=0.18).set_stroke(HIGHLIGHT_COLOR, width=3)
        near_band.move_to([3.55, line_y + 0.2, 0])
        near_label = Text("1.9%p는 여기", font_size=24, weight=BOLD, color=HIGHLIGHT_COLOR)
        near_label.next_to(near_band, DOWN, buff=0.2)

        self.play(FadeIn(card_2, shift=UP * 0.2), run_time=0.6)
        self.play(Create(track), Create(cut_2), FadeIn(cut_2_label), run_time=0.6)
        self.play(FadeIn(near_band, scale=0.9), FadeIn(near_label, shift=UP * 0.1), run_time=0.7)
        self.wait_until(beat5_start)

        # ─── Beat 5: 모든 광고에 그대로 적용되지는 않는다 ───
        # 처리 문장: "모든 광고에 그대로 적용되지는 않습니다."
        # 남는 요소: 두 카드, 주황 띠
        # 새로 등장: 축 양 끝(cutoff에서 먼 광고) 회색 '?' 두 개 + '멀리 있는 광고는 다를 수 있음'
        # 단일 핵심 시선: 양 끝의 '?'
        far_marks = VGroup(*[
            Text("?", font_size=44, weight=BOLD, color=MUTED).move_to([3.55 + dx, line_y + 0.55, 0])
            for dx in (-2.0, 2.0)
        ])
        far_note = Text("멀리 있는 광고는 다를 수 있음", font_size=20, color=SUBTLE)
        # 띠·'1.9%p는 여기' 아래, 카드 맨 아래 줄에 둔다.
        far_note.move_to([3.55, self.CARD_Y - self.CARD_H / 2 + 0.4, 0])
        self.play(FadeIn(far_marks, scale=0.6, lag_ratio=0.3), run_time=0.7)
        self.play(FadeIn(far_note), run_time=0.5)

        self.wait_until(audio_end)
        self.wait(self.WAIT_TAIL)


class Scene07_RealStudyOutro(Scene06_Conditions):
    """
    Scene 07: Real Study & Outro — 실제 연구도 단순 비교가 순위 효과를 부풀린다고 보여 줬다. 1위 값은 그만큼 가치가 있을까?

    Core Claim:
    Narayanan & Kalyanam (2015, Marketing Science)은 검색광고 순위 효과를 RDD로 분석해,
    단순 비교가 순위 효과를 크게 과대평가할 수 있음을 보였다. 그러니 1위 자리에 더 높은 입찰가를 내기 전에
    "늘어나는 클릭이 더 내는 광고비만큼의 값어치가 있는가"를 따져야 한다.

    Expected Misconception:
    "논문 결과가 지금의 모든 플랫폼(쿠팡 포함)에 그대로 적용된다." → 2015년 당시 검색광고 데이터 결과임을 화면에 명시한다.
    "CTR이 오르면 무조건 이득이다." → 클릭 증가와 광고비(CPC) 증가를 함께 봐야 한다 (별도 분석이 필요함을 질문으로 남긴다).

    Visual Pivot:
    논문 카드 아래 '단순 비교' 긴 막대가 'RDD' 짧은 막대로 줄어들고, 마지막에는 1위 거북이 B를 사이에 두고
    '늘어나는 클릭'과 '더 내는 광고비'가 양쪽에 놓여 질문으로 끝난다.

    Scene 경계:
    - 직전 Scene 마지막 문장: "모든 광고에 그대로 적용되지는 않습니다."
    - 현재 Scene 첫 문장: "실제 연구에서도 비슷한 결과가 나왔습니다."
    - 현재 Scene 마지막 문장: "늘어나는 클릭이, 더 내는 광고비만큼의 값어치가 있을까?" (영상의 마지막 문장)

    Source Reference:
    Narayanan, S., & Kalyanam, K. (2015). Position Effects in Search Advertising and Their Moderators:
    A Regression Discontinuity Approach. Marketing Science, 34(3), 388–407.
    - Stanford GSB 요약: RD 추정치가 단순(상관) 추정치보다 훨씬 작고, 일부 순위에서만 효과가 있었다.
    - 화면의 막대 길이는 개념도이며 논문의 실제 수치가 아니다 ('개념도' 표시).

    Script Reference:
    src/scripts/ko/07_real_study_outro.txt  ("값어치"는 TTS 발음 때문에 스크립트에서만 "가버치"로 표기)
    Audio: build/audio/07_real_study_outro.mp3 (ElevenLabs eleven_multilingual_v2, speed 1.1, 21.91s)

    Asset Reference:
    Tabler Icons (MIT) — file-text.svg, hand-click.svg, coins.svg

    3Blue1Brown Reference:
    3b1b/_2020/med_test.py - LearnAboutPositiveResult (같은 계열 리듬 유지)
    Reason:
    결과를 실제 근거로 한 번 더 확인한 뒤, 시청자에게 다음 질문을 남기며 닫는 마무리 리듬을 따랐다.
    화면 스타일은 WWDC 슬라이드 톤을 유지한다.

    Script-to-Beat Mapping (.timings.json chunk 기준, 문장 경계는 음절 비율로 추정):
      Beat 1 → chunk 1 "실제 연구에서도 비슷한 결과가 나왔습니다."                         (0.00~약 3.2s)
      Beat 2 → chunk 1 "나라야난과 칼리야남의 2015년 연구는 RDD로 검색광고 순위의 효과를 분석했는데," (약 3.2~10.2s)
      Beat 3 → chunk 1 "단순 비교가 순위 효과를 크게 부풀린다는 것을 보여 줬습니다."         (약 10.2~14.72s)
      Beat 4 → chunk 2 "그러니 1위에 더 비싼 값을 내기 전에 물어봐야 합니다."               (14.72~약 18.2s)
      Beat 5 → chunk 2 "늘어나는 클릭이, 더 내는 광고비만큼의 값어치가 있을까?"             (약 18.2s~끝)

    직전 Scene에서 이어받는 시각 요소:
      Scene 06 마지막 화면(제목 + 카드 두 장)에서 시작한다. 마지막 장면에서 Scene 01의 1위 거북이 B를 다시 불러
      영상의 첫 질문("1위 자리는 정말 그만큼의 값어치가 있을까?")으로 되돌아간다.

    화면 구획 (가로 14.2 x 8):
      Beat 2: 중앙 논문 카드 / Beat 3: 상단으로 줄인 카드 + 중앙 개념 막대 + 하단 단서 문구
      Beat 4~5: 상단 중앙 1위 거북이 B, 왼쪽 '늘어나는 클릭', 오른쪽 '더 내는 광고비', 하단 마지막 질문
    """

    SCENE_BASENAME = "07_real_study_outro"
    CHUNK1_SPLITS = (0.22, 0.69)
    CHUNK2_SPLIT = 0.49
    WAIT_TAIL = 1.5

    def build_scene06_end_state(self) -> VGroup:
        """Scene 06 마지막 화면(제목 + 카드 두 장)을 같은 좌표로 다시 세운다."""
        heading = Text("RDD를 믿으려면", font_size=38, weight=BOLD, color=INK)
        heading.move_to(UP * 2.72).to_edge(LEFT, buff=0.9)

        card_1 = self.make_card(-3.55, "① cutoff에서는 자리만 달라야")
        plot_a_center = np.array([-3.85, 0.75, 0])
        axis_a = self.make_mini_axis(plot_a_center)
        quality_line = Line(
            plot_a_center + LEFT * 2.2 + DOWN * 0.35, plot_a_center + RIGHT * 2.2 + UP * 0.3,
            stroke_color=QUALITY_COLOR, stroke_width=6,
        )
        quality_label = Text("광고 품질", font_size=20, weight=BOLD, color=QUALITY_COLOR)
        quality_label.next_to(quality_line.get_start(), UP, buff=0.2, aligned_edge=LEFT)
        ok_icon = load_icon("circle-check.svg", OK_COLOR, 0.6).next_to(axis_a, RIGHT, buff=0.25)
        ok_note = Text("매끄럽게 이어짐", font_size=20, color=OK_COLOR).next_to(axis_a, DOWN, buff=0.15)

        plot_b_center = np.array([-3.85, -1.45, 0])
        axis_b = self.make_mini_axis(plot_b_center)
        base_y = plot_b_center[1] - 0.65
        spread = VGroup(*[
            Rectangle(width=0.3, height=0.45 + 0.05 * (i % 3)).set_fill("#B9B9BE" if x < 0 else HIGHLIGHT_COLOR, opacity=0.8)
            .set_stroke(width=0).move_to([plot_b_center[0] + x + (0.18 if x >= 0 else -0.18), base_y, 0], aligned_edge=DOWN)
            for i, x in enumerate(np.linspace(-2.0, 2.0, 11)) if abs(x) > 0.05
        ])
        spike = Rectangle(width=0.3, height=1.25).set_fill(HIGHLIGHT_COLOR, opacity=1).set_stroke(width=0)
        spike.move_to([plot_b_center[0] + 0.18, base_y, 0], aligned_edge=DOWN)
        ng_icon = load_icon("circle-x.svg", NG_COLOR, 0.6).next_to(axis_b, RIGHT, buff=0.25)
        ng_note = Text("점수를 맞춰 넘기면 → cutoff 위로 몰림", font_size=20, color=NG_COLOR)
        ng_note.next_to(axis_b, DOWN, buff=0.15)

        card_2 = self.make_card(3.55, "② cutoff 근처의 효과")
        line_y = -0.9
        track = Line([3.55 - 2.6, line_y, 0], [3.55 + 2.6, line_y, 0], stroke_color=INK, stroke_width=3)
        cut_2 = DashedLine([3.55, line_y - 0.9, 0], [3.55, line_y + 1.4, 0], dash_length=0.12, stroke_color=INK, stroke_width=3)
        cut_2_label = Text("cutoff", font_size=22, weight=BOLD, color=INK).next_to(cut_2, UP, buff=0.1)
        near_band = RoundedRectangle(width=1.6, height=2.1, corner_radius=0.12)
        near_band.set_fill(HIGHLIGHT_COLOR, opacity=0.18).set_stroke(HIGHLIGHT_COLOR, width=3)
        near_band.move_to([3.55, line_y + 0.2, 0])
        near_label = Text("1.9%p는 여기", font_size=24, weight=BOLD, color=HIGHLIGHT_COLOR)
        near_label.next_to(near_band, DOWN, buff=0.2)
        far_marks = VGroup(*[
            Text("?", font_size=44, weight=BOLD, color=MUTED).move_to([3.55 + dx, line_y + 0.55, 0])
            for dx in (-2.0, 2.0)
        ])
        far_note = Text("멀리 있는 광고는 다를 수 있음", font_size=20, color=SUBTLE)
        far_note.move_to([3.55, self.CARD_Y - self.CARD_H / 2 + 0.4, 0])

        return VGroup(
            heading,
            card_1, axis_a, quality_line, quality_label, ok_icon, ok_note,
            axis_b, spread, spike, ng_icon, ng_note,
            card_2, track, cut_2, cut_2_label, near_band, near_label, far_marks, far_note,
        )

    def construct(self):
        starts, audio_end = load_audio_timings(self.SCENE_BASENAME)
        chunk_ends = starts[1:] + [audio_end]

        def split(chunk: int, ratio: float) -> float:
            return starts[chunk] + (chunk_ends[chunk] - starts[chunk]) * ratio

        beat2_start, beat3_start = (split(0, r) for r in self.CHUNK1_SPLITS)
        beat5_start = split(1, self.CHUNK2_SPLIT)

        chapter = make_chapter_label("Part 2 · RDD로 풀어보기")
        previous = self.build_scene06_end_state()
        self.add(chapter, previous)

        # ─── Beat 1: 실제 연구에서도 ───
        # 처리 문장: "실제 연구에서도 비슷한 결과가 나왔습니다."
        # 남는 요소: 챕터 라벨
        # 지울 요소: Scene 06 제목과 카드 두 장
        # 새로 등장: 좌상단 제목 '실제 연구에서는'
        # 단일 핵심 시선: 제목
        heading = Text("실제 연구에서는", font_size=38, weight=BOLD, color=INK)
        heading.move_to(UP * 2.72).to_edge(LEFT, buff=0.9)
        self.play(FadeOut(previous, shift=DOWN * 0.2), run_time=0.6)
        self.play(FadeIn(heading, shift=RIGHT * 0.2), run_time=0.6)
        self.wait_until(beat2_start)

        # ─── Beat 2: Narayanan & Kalyanam (2015) ───
        # 처리 문장: "나라야난과 칼리야남의 2015년 연구는 RDD로 검색광고 순위의 효과를 분석했는데,"
        # 남는 요소: 제목
        # 새로 등장: 중앙 논문 카드 (문서 아이콘 + 저자·연도 + 제목 + 학술지), 카드 안 'RDD' 태그
        # 단일 핵심 시선: 논문 카드
        paper_icon = load_icon("file-text.svg", INK, 1.2)
        paper_author = Text("Narayanan & Kalyanam (2015)", font_size=32, weight=BOLD, color=INK)
        paper_title = Text(
            "Position Effects in Search Advertising and Their Moderators:\nA Regression Discontinuity Approach",
            font_size=22, color=INK, line_spacing=0.8,
        )
        paper_journal = Text("Marketing Science, 34(3), 388–407", font_size=20, color=SUBTLE)
        paper_text = VGroup(paper_author, paper_title, paper_journal).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        rdd_tag = make_pill("RDD", HIGHLIGHT_COLOR, font_size=22)
        rdd_tag.next_to(paper_author, RIGHT, buff=0.3)
        paper_body = VGroup(paper_icon, VGroup(paper_text, rdd_tag)).arrange(RIGHT, buff=0.5)
        paper_card = RoundedRectangle(width=paper_body.width + 1.0, height=paper_body.height + 0.8, corner_radius=0.22)
        paper_card.set_fill(WHITE, opacity=1).set_stroke(width=0).move_to(paper_body)
        paper = VGroup(paper_card, paper_body).move_to(UP * 0.2)

        self.play(FadeIn(paper_card, shift=UP * 0.2), FadeIn(paper_icon), run_time=0.7)
        self.play(FadeIn(paper_text, shift=RIGHT * 0.15, lag_ratio=0.15), run_time=1.0)
        self.play(FadeIn(rdd_tag, scale=0.7), run_time=0.5)
        self.wait_until(beat3_start)

        # ─── Beat 3: 단순 비교가 순위 효과를 크게 부풀린다 ───
        # 처리 문장: "단순 비교가 순위 효과를 크게 부풀린다는 것을 보여 줬습니다."
        # 남는 요소: 논문 카드 (위로 줄여 올린다)
        # 지울 요소: 제목 (카드가 상단을 차지)
        # 새로 등장: 개념 막대 '단순 비교'(긴 회색) → 'RDD'(짧은 주황), 오른쪽 '크게 부풀려짐', 하단 단서 문구
        # 단일 핵심 시선: 긴 막대와 짧은 막대의 차이
        self.play(FadeOut(heading), paper.animate.scale(0.72).move_to(UP * 2.15), run_time=0.7)
        concept_rows = VGroup()
        for name, width, color in (("단순 비교", 8.0, "#B9B9BE"), ("RDD", 2.6, HIGHLIGHT_COLOR)):
            row_name = Text(name, font_size=28, weight=BOLD, color=INK)
            row_bar = RoundedRectangle(width=width, height=0.65, corner_radius=0.12)
            row_bar.set_fill(color, opacity=1).set_stroke(width=0)
            concept_rows.add(VGroup(row_name, row_bar))
        for row, y in zip(concept_rows, (0.25, -0.75)):
            row[0].move_to([-5.0, y, 0])
            row[1].move_to([-3.9, y, 0], aligned_edge=LEFT)
        inflate_brace = BraceBetweenPoints(
            [concept_rows[1][1].get_right()[0], -1.2, 0], [concept_rows[0][1].get_right()[0], -1.2, 0],
            direction=DOWN, color=SUBTLE,
        )
        inflate_label = Text("크게 부풀려짐", font_size=26, weight=BOLD, color=SUBTLE).next_to(inflate_brace, DOWN, buff=0.1)
        concept_note = Text(
            "개념도 · 2015년 당시 검색광고 데이터 결과로, 모든 플랫폼에 그대로 일반화할 수는 없음",
            font_size=18, color=MUTED,
        ).move_to(DOWN * 3.3)

        self.play(FadeIn(concept_rows[0][0]), GrowFromEdge(concept_rows[0][1], LEFT), run_time=0.7)
        self.play(FadeIn(concept_rows[1][0]), GrowFromEdge(concept_rows[1][1], LEFT), run_time=0.7)
        self.play(GrowFromCenter(inflate_brace), FadeIn(inflate_label), FadeIn(concept_note), run_time=0.7)
        self.wait_until(starts[1])

        # ─── Beat 4: 1위에 더 비싼 값을 내기 전에 ───
        # 처리 문장: "그러니 1위에 더 비싼 값을 내기 전에 물어봐야 합니다."
        # 남는 요소: 챕터 라벨
        # 지울 요소: 논문 카드, 개념 막대, 단서 문구
        # 새로 등장: 상단 중앙 1위 카드 속 거북이 B (Scene 01 휴대폰 1위 칸의 재등장) + 오른쪽 '더 내는 광고비' 동전
        # 비워 두는 영역: 왼쪽 ('늘어나는 클릭' 자리), 하단 (마지막 질문 자리)
        # 단일 핵심 시선: 1위 거북이 B와 동전
        study = VGroup(paper, concept_rows, inflate_brace, inflate_label, concept_note)
        slot_card = make_product_card(AD_B_COLOR, "거북이 B", is_ad=True).scale(1.15)
        slot_pill = make_pill("1위", HIGHLIGHT_COLOR).next_to(slot_card, LEFT, buff=0.3)
        slot = VGroup(slot_pill, slot_card).move_to(UP * 1.7)
        slot_box = SurroundingRectangle(slot_card, color=HIGHLIGHT_COLOR, buff=0.05, stroke_width=5)

        cost_icon = load_icon("coins.svg", HIGHLIGHT_COLOR, 1.3)
        cost_label = VGroup(
            Text("더 내는 광고비", font_size=30, weight=BOLD, color=INK),
            Text("CPC ↑", font_size=24, color=SUBTLE),
        ).arrange(DOWN, buff=0.12)
        cost = VGroup(cost_icon, cost_label).arrange(DOWN, buff=0.3).move_to([3.6, -0.9, 0])

        self.play(FadeOut(study), run_time=0.5)
        self.play(FadeIn(slot, shift=DOWN * 0.2), Create(slot_box), run_time=0.8)
        self.play(FadeIn(cost, shift=UP * 0.2), run_time=0.7)
        self.wait_until(beat5_start)

        # ─── Beat 5: 늘어나는 클릭이 더 내는 광고비만큼 값어치가 있을까? ───
        # 처리 문장: "늘어나는 클릭이, 더 내는 광고비만큼의 값어치가 있을까?"
        # 남는 요소: 1위 거북이 B, 오른쪽 광고비
        # 새로 등장: 왼쪽 '늘어나는 클릭', 가운데 '?', 하단 마지막 질문 문장
        # 단일 핵심 시선: 클릭 ↔ 광고비 사이의 '?' → 마지막 질문
        gain_icon = load_icon("hand-click.svg", AD_B_COLOR, 1.3)
        gain_label = VGroup(
            Text("늘어나는 클릭", font_size=30, weight=BOLD, color=INK),
            Text("RDD로 본 자리 효과", font_size=24, color=SUBTLE),
        ).arrange(DOWN, buff=0.12)
        gain = VGroup(gain_icon, gain_label).arrange(DOWN, buff=0.3).move_to([-3.6, -0.9, 0])
        versus = Text("?", font_size=80, weight=BOLD, color=HIGHLIGHT_COLOR).move_to([0, -0.7, 0])
        final_question = Text(
            "1위 자리, 정말 그만큼의 값어치가 있을까?",
            font_size=36, weight=BOLD, color=INK, t2c={"값어치": HIGHLIGHT_COLOR},
        ).move_to(DOWN * 3.1)

        self.play(FadeIn(gain, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(versus, scale=0.6), run_time=0.5)
        self.play(Write(final_question), run_time=1.2)

        self.wait_until(audio_end)
        self.wait(self.WAIT_TAIL)
