from manim import *

from videos.why_causal_inference.shared.common import (
    ACCENT_COLOR,
    LIBRARY_COLOR,
    NEUTRAL_COLOR,
    QUESTION_COLOR,
    TABLET_COLOR,
    make_academic_outcome_icon,
    make_budget_icon,
    make_library_icon,
    make_relation_icons,
    make_tablet_icon,
)


class Scene01_WhyCausalQuestionsMatter(Scene):
    """
    Scene 01: Why Causal Questions Matter (EN)

    Core Claim:
    Causal inference is about answering "what if" questions —
    and the gap between correlation and causation is easy to state but hard to explain.

    Expected Misconception:
    Comparing averages or choosing between policies seems enough to answer causal questions,
    but separating the effect of a cause from background differences requires a different lens.

    Visual Pivot:
    A budget splits into two policy options (tablet vs library), which compress into
    an academic outcome icon + causal prompt, then broaden into three cross-domain
    relation diagrams, and finally collapse into "Correlation ≠ Causation."

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_en.ipynb
    - Cell 1: Tablet vs library example, everyday causal questions, intro to correlation vs causation

    Script Reference:
    narration/01_why_causal_questions_matter.txt

    Asset Reference:
    Tabler Icons (MIT)
    - device-tablet.svg, book.svg, coin.svg, school.svg
    - currency-dollar.svg, smoking-no.svg, ad.svg, chart-line.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py - IntroQuestion
    Reason: Sequential question delivery rhythm and convergence to a final question.

    Script-to-Beat Mapping:
    Beat 1 | chunks 1-2 | 0→5.6s  | "What if?" hook
    Beat 2 | chunk 3    | 5.6→13.5s | Budget → tablet/library split
    Beat 3 | chunk 4    | 13.5→16.9s | Academic outcome + causal question
    Beat 4 | chunk 5    | 19.88→31.21s | Three cross-domain relation diagrams
    Beat 5 | chunk 6    | 31.21→42.40s | Correlation ≠ Causation close
    Audio: speed=0.85, total=42.59s
    """

    WAIT_TAIL = 10.0

    def construct(self):
        # ── Beat 1 ──────────────────────────────────────────────────
        # 남는 요소: hook_group (ring + ? + "What if?")
        # 새로 등장: hook_ring, hook, hook_word
        # 제거: 없음
        # 핵심 시선: "What if?" 텍스트
        # chunks 1-2 (0→7.11s) 처리. 훅을 충분히 유지한다.
        hook = MathTex("?").scale(3.2).set_color(ACCENT_COLOR)
        hook.move_to(UP * 0.9)
        hook_ring = Circle(radius=0.78, stroke_color=ACCENT_COLOR, stroke_width=3).move_to(hook)
        hook_word = Text("What if?", font_size=30, weight=BOLD, color=WHITE)
        hook_word.next_to(hook, DOWN, buff=0.32)
        hook_group = VGroup(hook_ring, hook, hook_word)

        self.play(Create(hook_ring), FadeIn(hook, scale=0.85), run_time=0.8)
        self.play(FadeIn(hook_word, shift=UP * 0.12), run_time=0.6)
        self.wait(5.7)  # 0.8+0.6+5.7 = 7.1s ≈ chunk 1-2 end (7.11s)

        # ── Beat 2 ──────────────────────────────────────────────────
        # 남는 요소: budget, left_arrow, right_arrow, tablet, library
        # 새로 등장: budget coin, arrows, tablet/library icons
        # 제거: hook_group
        # 핵심 시선: 두 선택지로 갈라지는 예산
        # chunk 3 (7.11→16.35s, 9.24s) 처리. 두 선택지를 오래 보여준다.
        budget = make_budget_icon().move_to(UP * 1.25)

        tablet = VGroup(make_tablet_icon(TABLET_COLOR))
        library = VGroup(make_library_icon(LIBRARY_COLOR))
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
        self.wait(7.2)  # 0.8+1.2+7.2 = 9.2s ≈ chunk 3 duration (9.24s) ✓

        # ── Beat 3 ──────────────────────────────────────────────────
        # 남는 요소: result_icon, cause_prompt, tablet_dim(faded), library_dim(faded)
        # 새로 등장: result_icon (school), cause_prompt text
        # 제거: budget, arrows; tablet/library dimmed and pushed aside
        # 핵심 시선: 인과 질문 텍스트
        # chunk 4 (16.35→19.88s, 3.53s) 처리.
        result_icon = make_academic_outcome_icon(WHITE).move_to(DOWN * 0.1)
        cause_prompt = Text("Which boosts academic achievement?", font_size=22, weight=BOLD, color=ACCENT_COLOR)
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
        self.wait(1.7)  # 1.1+0.7+1.7 = 3.5s ≈ chunk 4 duration (3.53s) ✓

        # ── Beat 4 ──────────────────────────────────────────────────
        # 남는 요소: relations (세 개 순차 등장)
        # 새로 등장: 관계 다이어그램 3개 (education→income, price→smoking, ad→sales)
        # 제거: tablet_dim, library_dim, result_icon, cause_prompt
        # 핵심 시선: 각 관계 다이어그램 하나씩 순서대로
        # chunk 5 (19.88→31.21s, 11.33s) 처리. 각 다이어그램을 또렷하게 보여준다.
        # 0.65(fadeout) + 3×(0.8 fadein + 2.76 wait) = 0.65 + 10.68 = 11.33s ✓
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
            self.wait(2.76)

        # ── Beat 5 ──────────────────────────────────────────────────
        # 남는 요소: formula (Correlation ≠ Causation), tag
        # 새로 등장: formula 텍스트, subtitle tag
        # 제거: 모든 relations
        # 핵심 시선: "Correlation ≠ Causation" 수식
        # chunk 6 (25.9→35.4s, 9.6s) 처리. 결론을 충분히 유지한다.
        formula = VGroup(
            Text("Correlation", font_size=34, color=WHITE, weight=BOLD),
            MathTex(r"\ne").scale(1.2).set_color(ACCENT_COLOR),
            Text("Causation", font_size=34, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.28)
        formula.move_to(UP * 0.5)

        tag = Text("...but explaining exactly why isn't.", font_size=22, color=NEUTRAL_COLOR)
        tag.next_to(formula, DOWN, buff=0.34)

        self.play(
            LaggedStart(*[FadeOut(rel, shift=LEFT * 0.14) for rel in relations], lag_ratio=0.1),
            run_time=0.8,
        )
        self.play(FadeIn(formula, shift=UP * 0.14), run_time=0.7)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.6)
        self.wait(self.WAIT_TAIL)
