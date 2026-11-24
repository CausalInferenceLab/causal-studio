from manim import *

from iv_common import (
    ACCENT,
    CLEAN_WATER,
    INSTRUMENT,
    SOFT,
    load_icon,
    load_scene_timing_durations,
)


class Scene07_Outro(Scene):
    """
    Scene 07: 아웃트로 — 현실 속 우연 찾기.

    Core Claim:
    도구변수 분석에서 가장 어려운 일은 수식이 아니라, 현실 속에
    이미 존재하는 우연을 찾아내는 일이다. 무작위 배정이 불가능한
    질문 앞에서, 자연이 던진 동전을 찾는 안목이 다음 단계다.

    Visual Pivot:
    세 역사적 장면(수도 회사, 빙고볼, 생일)이 한 줄로 등장한 뒤,
    공통점인 "우연"이 한 단어로 응축되는 순간.

    Script: src/scripts/07_outro.txt — 3 chunks, 33.86s
    """

    WAIT_TAIL = 1.5

    def construct(self):
        durations = load_scene_timing_durations("07_outro")
        # durations ≈ [16.56, 8.35, 8.95]

        # Beat 1 (0~16.56s): 세 장면 회상
        title = Text("우연은 이미 우리 곁에 있다", font_size=32, weight=BOLD, color=ACCENT).to_edge(UP, buff=0.5)
        # 세 미니 카드
        snow = self._make_vignette("droplet.svg", CLEAN_WATER, "1854 런던", "수도 회사")
        draft = self._make_vignette("dice.svg", ACCENT, "1969 미국", "징집 추첨")
        birth = self._make_vignette("cake.svg", PINK, "어쩌면", "여러분의 생일")
        vignettes = VGroup(snow, draft, birth).arrange(RIGHT, buff=0.9).move_to(ORIGIN + UP * 0.2)
        common = Text("모두 현실 속 우연", font_size=24, color=SOFT).to_edge(DOWN, buff=1.2)

        self.play(FadeIn(title, shift=DOWN * 0.1), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(v, shift=UP * 0.2) for v in vignettes], lag_ratio=0.25), run_time=1.8)
        self.play(Write(common), run_time=1.2)
        self.wait(16.56 - 3.7)

        # Beat 2 (16.56~24.91s): 가장 어려운 일은 우연 찾기
        self.play(FadeOut(common), run_time=0.4)
        hard_line = Text("가장 어려운 일은 수식이 아니라", font_size=26, color=WHITE).move_to(DOWN * 1.4)
        hard_line2 = Text("우연을 찾아내는 일이다", font_size=30, weight=BOLD, color=INSTRUMENT).next_to(hard_line, DOWN, buff=0.3)
        self.play(Write(hard_line), run_time=1.2)
        self.play(Write(hard_line2), run_time=1.4)
        self.wait(8.35 - 3.0)

        # Beat 3 (24.91~33.86s): 닫기 카드
        self.play(FadeOut(VGroup(title, vignettes, hard_line, hard_line2)), run_time=0.7)
        close_line1 = Text("무작위 배정을 할 수 없다면,", font_size=30, color=WHITE).move_to(UP * 0.6)
        close_line2 = Text("자연이 이미 던진 동전을 찾아내세요.", font_size=30, weight=BOLD, color=INSTRUMENT).next_to(close_line1, DOWN, buff=0.4)
        end_tag = Text("그게 인과추론의 다음 단계입니다.", font_size=22, color=SOFT).next_to(close_line2, DOWN, buff=0.6)

        self.play(Write(close_line1), run_time=1.2)
        self.play(Write(close_line2), run_time=1.4)
        self.play(FadeIn(end_tag, shift=UP * 0.1), run_time=1.0)
        self.wait(8.95 - 3.6)
        self.wait(self.WAIT_TAIL)

    @staticmethod
    def _make_vignette(icon_name: str, color: str, year: str, name: str) -> VGroup:
        try:
            icon = load_icon(icon_name, color, 0.9)
        except Exception:
            # 폴백: 색 원
            icon = Circle(radius=0.4, color=color, stroke_width=3)
        year_text = Text(year, font_size=20, color=color, weight=BOLD)
        name_text = Text(name, font_size=18, color=WHITE)
        block = VGroup(icon, year_text, name_text).arrange(DOWN, buff=0.25)
        return block
