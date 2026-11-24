from manim import *

from why_causal_inference_common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    make_academic_outcome_icon,
    make_badge,
    make_budget_icon,
    make_library_icon,
    make_relation_icons,
    make_tablet_icon,
)


class Scene01_WhyCausalQuestionsMatter(Scene):
    """
    Scene 01: Why Causal Questions Matter

    Core Claim:
    인과추론의 출발점은 '무엇이 실제 변화를 만들었는가'를 묻는 질문이다.

    Expected Misconception:
    정책 선택이나 평균 비교만 보면 답이 쉬워 보이지만,
    실제로는 결과 변화의 원인을 따로 떼어 묻는 일이 필요하다.

    Visual Pivot:
    예산이 두 선택지로 갈라지는 그림이 결과 아이콘과 큰 물음표로 압축된 뒤,
    마지막에 `corr \ne cause` 수식으로 수렴한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - Cell 1: 태블릿 vs 도서관 예시, 일상적 인과 질문, 상관관계는 익숙하지만 설명은 어렵다는 도입

    Script Reference:
    src/scripts/01_why_causal_questions_matter.txt

    Asset Reference:
    Tabler Icons (MIT)
    - device-tablet.svg
    - book.svg
    - coin.svg
    - school.svg
    - currency-dollar.svg
    - smoking-no.svg
    - ad.svg
    - chart-line.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py - IntroQuestion
    3b1b/videos/_2024/transformers/ml_basics.py
    Reason:
    전자는 질문을 순차적으로 던지고 마지막 질문으로 수렴하는 리듬을 참고했고,
    후자는 짧은 라벨 두 개를 균형 있게 배치하는 단순한 비교 화면 구성을 참고했다.

    Script-to-Beat Mapping:
    1. '만약에'라는 질문 도입
    2. 한정된 예산이 두 정책 선택지로 갈라지는 장면
    3. 선택지보다 중요한 것은 결과 변화의 원인이라는 점으로 수렴
    4. 교육, 가격, 광고 예시를 같은 구조의 관계 다이어그램으로 제시
    5. 상관관계와 인과관계의 차이로 마무리
    """

    WAIT_TAIL = 10.9

    def construct(self):
        hook = MathTex("?").scale(3.2).set_color(ACCENT_COLOR)
        hook.move_to(UP * 0.9)
        hook_ring = Circle(radius=0.78, stroke_color=ACCENT_COLOR, stroke_width=3).move_to(hook)
        hook_word = Text("What if?", font_size=30, weight=BOLD, color=WHITE)
        hook_word.next_to(hook, DOWN, buff=0.32)
        hook_group = VGroup(hook_ring, hook, hook_word)

        # Beat 1:
        # chunk 1-2를 처리한다.
        # 첫 질문과 "What if?"를 충분히 받기 위해 초반 훅을 더 길게 유지한다.
        self.play(Create(hook_ring), FadeIn(hook, scale=0.85), run_time=0.8)
        self.play(FadeIn(hook_word, shift=UP * 0.12), run_time=0.6)
        self.wait(6.0)

        # Beat 2:
        # chunk 3을 처리한다.
        # 예산이 두 정책 선택지로 갈라지는 비교 장면을 오래 보여줘야 한다.
        budget = make_budget_icon().move_to(UP * 1.25)

        tablet = make_badge(make_tablet_icon(TABLET_COLOR))
        library = make_badge(make_library_icon(LIBRARY_COLOR))
        tablet.move_to(LEFT * 2.35 + DOWN * 0.45)
        library.move_to(RIGHT * 2.35 + DOWN * 0.45)

        left_arrow = Arrow(budget.get_bottom(), tablet[0].get_top(), buff=0.18, stroke_width=4, color=TABLET_COLOR)
        right_arrow = Arrow(budget.get_bottom(), library[0].get_top(), buff=0.18, stroke_width=4, color=LIBRARY_COLOR)

        self.play(
            FadeOut(hook_group, shift=UP * 0.2),
            FadeIn(budget, scale=0.9),
            run_time=0.8,
        )
        self.play(
            GrowArrow(left_arrow),
            GrowArrow(right_arrow),
            Create(tablet),
            Create(library),
            run_time=1.2,
        )
        self.wait(10.2)

        # Beat 3:
        # chunk 4를 처리한다.
        # 핵심 질문으로 빠르게 수렴하고, 이 장면 자체는 길게 끌지 않는다.
        result_icon = make_academic_outcome_icon(WHITE).move_to(DOWN * 0.1)
        cause_prompt = Text("어느 쪽이 학업 성취도를 높일까?", font_size=23, weight=BOLD, color=ACCENT_COLOR)
        cause_prompt.next_to(result_icon, DOWN, buff=0.34)
        tablet_dim = tablet.copy().scale(0.72).move_to(LEFT * 3.0 + DOWN * 0.05)
        library_dim = library.copy().scale(0.72).move_to(RIGHT * 3.0 + DOWN * 0.05)
        tablet_dim.set_stroke(opacity=0.45)
        library_dim.set_stroke(opacity=0.45)

        self.play(
            FadeOut(budget),
            FadeOut(left_arrow),
            FadeOut(right_arrow),
            Transform(tablet, tablet_dim),
            Transform(library, library_dim),
            FadeIn(result_icon, scale=0.9),
            run_time=1.1,
        )
        self.play(FadeIn(cause_prompt, shift=UP * 0.1), run_time=0.7)
        self.wait(1.3)

        # Beat 4:
        # chunk 5를 처리한다.
        # 교육, 가격, 광고 예시는 각각 하나씩 또렷하게 보이고 넘어간다.
        relations = VGroup(
            make_relation_icons("school.svg", "currency-dollar.svg", QUESTION_COLOR),
            make_relation_icons("coin.svg", "smoking-no.svg", QUESTION_COLOR),
            make_relation_icons("ad.svg", "chart-line.svg", QUESTION_COLOR),
        ).arrange(DOWN, buff=0.6)
        relations.move_to(ORIGIN)

        self.play(
            FadeOut(tablet),
            FadeOut(library),
            FadeOut(result_icon),
            FadeOut(cause_prompt),
            run_time=0.65,
        )
        for rel in relations:
            self.play(FadeIn(rel, shift=RIGHT * 0.16), run_time=0.8)
            self.wait(2.8)
        self.wait(1.85)  # chunk5 종료(35.99s)까지 0.94s 부족 → 1.85s로 늘려 싱크 보정

        # Beat 5:
        # chunk 6을 처리한다.
        # 마지막 정리 문장을 받기 위해 결론 화면을 충분히 오래 유지한다.
        formula = VGroup(
            Text("상관관계", font_size=34, color=WHITE, weight=BOLD),
            MathTex(r"\ne").scale(1.2).set_color(ACCENT_COLOR),
            Text("인과관계", font_size=34, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.28)
        formula.move_to(UP * 0.5)

        tag = Text("설명은 더 어렵다", font_size=24, color=NEUTRAL_COLOR)
        tag.next_to(formula, DOWN, buff=0.34)

        self.play(
            LaggedStart(*[FadeOut(rel, shift=LEFT * 0.14) for rel in relations], lag_ratio=0.1),
            run_time=0.8,
        )
        self.play(FadeIn(formula, shift=UP * 0.14), run_time=0.7)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.6)
        self.wait(self.WAIT_TAIL)
