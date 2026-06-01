import json
from pathlib import Path

from manim import *


ACCENT_COLOR = YELLOW_E
TABLET_COLOR = TEAL_D
LIBRARY_COLOR = GOLD_D
QUESTION_COLOR = MAROON_D
NEUTRAL_COLOR = GREY_B
ASSET_DIR = Path(__file__).resolve().parents[2] / "assets" / "tabler-icons" / "icons" / "outline"
TOPIC_DIR = Path(__file__).resolve().parents[1]


def load_icon(filename: str, color: str, height: float) -> SVGMobject:
    icon = SVGMobject(str(ASSET_DIR / filename))
    icon.set_stroke(color=color, width=2.6, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def load_scene_timing_durations(scene_basename: str) -> list[float]:
    # English audio lives in build/audio/en/
    timings_path = TOPIC_DIR / "build" / "audio" / "en" / f"{scene_basename}.timings.json"
    if not timings_path.exists():
        return []
    payload = json.loads(timings_path.read_text())
    return [float(chunk["duration"]) for chunk in payload.get("chunks", [])]


def make_tablet_icon(color: str) -> SVGMobject:
    return load_icon("device-tablet.svg", color, 1.45)


def make_library_icon(color: str) -> SVGMobject:
    return load_icon("book.svg", color, 1.45)


def make_budget_icon(color: str = WHITE) -> SVGMobject:
    return load_icon("coin.svg", color, 1.05)


def make_person_icon(color: str = WHITE, height: float = 1.35) -> SVGMobject:
    return load_icon("user.svg", color, height)


def make_academic_outcome_icon(color: str = WHITE) -> VGroup:
    return VGroup(load_icon("school.svg", color, 1.1))


def make_relation_icons(left_icon: str, right_icon: str, color: str) -> VGroup:
    left = load_icon(left_icon, color, 0.9)
    right = load_icon(right_icon, color, 0.9)
    left.move_to(LEFT * 0.9)
    right.move_to(RIGHT * 0.9)
    arrow = Arrow(
        left.get_right(),
        right.get_left(),
        buff=0.12,
        stroke_width=4,
        color=color,
    )
    return VGroup(left, arrow, right)


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
    src/scripts/en/01_why_causal_questions_matter.txt

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


def make_world_panel(
    treatment_icon: str,
    treatment_label: str,
    outcome_tex: str,
    color: str,
) -> VGroup:
    frame = RoundedRectangle(
        width=3.25,
        height=4.65,
        corner_radius=0.22,
        stroke_color=color,
        stroke_width=2.6,
    )
    treatment = MathTex(treatment_label).scale(0.88).set_color(color)
    treatment.next_to(frame.get_top(), DOWN, buff=0.34)

    person = make_person_icon(color, 1.1)
    person.move_to(frame.get_center() + UP * 0.62)

    icon = load_icon(treatment_icon, color, 0.92)
    icon.next_to(person, DOWN, buff=0.28)

    arrow = Arrow(
        person.get_bottom(),
        icon.get_top(),
        buff=0.12,
        stroke_width=3.2,
        color=color,
    )

    outcome = MathTex(outcome_tex).scale(1.08).set_color(WHITE)
    outcome.next_to(icon, DOWN, buff=0.42)

    school = load_icon("school.svg", WHITE, 0.78)
    school.next_to(outcome, DOWN, buff=0.28)

    return VGroup(frame, treatment, person, arrow, icon, outcome, school)


class Scene02_AssociationIsNotCausation(Scene):
    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("02_association_is_not_causation")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        left_icon = make_tablet_icon(TABLET_COLOR)
        left_icon.move_to(LEFT * 2.55 + DOWN * 0.1)
        right_icon = make_academic_outcome_icon(WHITE)
        right_icon.move_to(RIGHT * 2.55 + DOWN * 0.1)
        relation_arrow = Arrow(
            left_icon.get_right() + RIGHT * 0.1,
            right_icon.get_left() + LEFT * 0.1,
            buff=0.08,
            stroke_width=4,
            color=ACCENT_COLOR,
        )
        left_label = Text("Tablet given", font_size=24, color=TABLET_COLOR, weight=BOLD)
        left_label.next_to(left_icon, DOWN, buff=0.26)
        right_label = Text("High scores", font_size=24, color=ACCENT_COLOR, weight=BOLD)
        right_label.next_to(right_icon, DOWN, buff=0.26)

        confounder_chips = VGroup(
            VGroup(load_icon("coin.svg", GOLD_E, 0.55), Text("Funding", font_size=19, color=GOLD_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
            VGroup(load_icon("school-bell.svg", BLUE_E, 0.55), Text("Tutoring", font_size=19, color=BLUE_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
            VGroup(load_icon("users-group.svg", GREEN_E, 0.62), Text("Teachers", font_size=19, color=GREEN_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.38)
        confounder_title = Text("School conditions", font_size=24, color=WHITE, weight=BOLD)
        confounder_title.next_to(confounder_chips, UP, buff=0.22)
        confounder_box = RoundedRectangle(
            width=5.9,
            height=1.75,
            corner_radius=0.18,
            stroke_color=NEUTRAL_COLOR,
            stroke_width=2.2,
        )
        confounder_group = VGroup(confounder_box, confounder_title, confounder_chips)
        confounder_group.move_to(UP * 2.05)

        backdoor_left = CurvedArrow(
            confounder_group.get_bottom() + LEFT * 1.2,
            left_icon.get_top() + UP * 0.05,
            angle=0.32,
            color=NEUTRAL_COLOR,
            stroke_width=3.2,
        )
        backdoor_right = CurvedArrow(
            confounder_group.get_bottom() + RIGHT * 1.2,
            right_icon.get_top() + UP * 0.05,
            angle=-0.32,
            color=NEUTRAL_COLOR,
            stroke_width=3.2,
        )

        assoc = VGroup(
            Text("Correlation", font_size=34, color=WHITE, weight=BOLD),
            MathTex(r"\ne").scale(1.15).set_color(QUESTION_COLOR),
            Text("Causation", font_size=34, color=QUESTION_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.28)
        assoc.move_to(UP * 1.85)
        foot = Text("We can't attribute this to the tablet alone.", font_size=20, color=NEUTRAL_COLOR)
        foot.next_to(assoc, DOWN, buff=0.34)

        # Beat 1:
        self.play(FadeIn(left_icon, scale=0.9), FadeIn(right_icon, scale=0.9), run_time=0.9)
        self.play(
            GrowArrow(relation_arrow),
            FadeIn(left_label, shift=UP * 0.08),
            FadeIn(right_label, shift=UP * 0.08),
            run_time=0.9,
        )
        wait_for_chunks([1], spent=1.8)

        # Beat 2:
        self.play(FadeIn(confounder_group, shift=DOWN * 0.12), run_time=0.9)
        self.play(Create(backdoor_left), Create(backdoor_right), run_time=0.9)
        wait_for_chunks([2], spent=1.8)

        # Beat 3:
        self.play(
            FadeOut(relation_arrow),
            FadeOut(confounder_group),
            FadeOut(backdoor_left),
            FadeOut(backdoor_right),
            FadeOut(left_label),
            FadeOut(right_label),
            run_time=0.6,
        )
        self.play(FadeIn(assoc, shift=UP * 0.12), run_time=0.8)
        self.play(FadeIn(foot, shift=UP * 0.08), run_time=0.6)
        wait_for_chunks([3], spent=2.0)
        self.wait(self.WAIT_TAIL)


class Scene03_CounterfactualWorlds(Scene):
    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("03_counterfactual_worlds")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        treatment_seed = MathTex(r"T_i").scale(1.45).set_color(TABLET_COLOR)
        treatment_seed.move_to(LEFT * 2.35 + UP * 0.45)
        treatment_word = Text("Treatment", font_size=24, color=WHITE, weight=BOLD)
        treatment_word.next_to(treatment_seed, DOWN, buff=0.2)

        treatment_yes = VGroup(
            MathTex(r"T_i = 1").set_color(TABLET_COLOR),
            make_tablet_icon(TABLET_COLOR),
        ).arrange(RIGHT, buff=0.2)
        treatment_yes.move_to(RIGHT * 1.45 + UP * 1.45)

        treatment_no = VGroup(
            MathTex(r"T_i = 0").set_color(LIBRARY_COLOR),
            load_icon("device-tablet-off.svg", LIBRARY_COLOR, 1.45),
        ).arrange(RIGHT, buff=0.2)
        treatment_no.move_to(RIGHT * 1.45 + DOWN * 0.6)

        up_arrow = CurvedArrow(
            treatment_seed.get_right() + RIGHT * 0.05 + UP * 0.12,
            treatment_yes.get_left() + LEFT * 0.12 + DOWN * 0.04,
            angle=-0.52,
            stroke_width=3.6,
            color=TABLET_COLOR,
        )
        down_arrow = CurvedArrow(
            treatment_seed.get_right() + RIGHT * 0.05 + DOWN * 0.12,
            treatment_no.get_left() + LEFT * 0.12 + UP * 0.04,
            angle=0.52,
            stroke_width=3.6,
            color=LIBRARY_COLOR,
        )

        outcome_def = VGroup(
            MathTex(r"Y_i").scale(1.2).set_color(ACCENT_COLOR),
            Text("Academic achievement", font_size=22, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.22)
        outcome_def.move_to(UP * 0.45)
        outcome_icon = load_icon("school.svg", ACCENT_COLOR, 1.05)
        outcome_icon.next_to(outcome_def, DOWN, buff=0.34)

        treatment_group = VGroup(
            treatment_seed,
            treatment_word,
            up_arrow,
            down_arrow,
            treatment_yes,
            treatment_no,
        )

        left_world = make_world_panel("device-tablet.svg", r"T_i = 1", r"Y_{1i}", TABLET_COLOR)
        right_world = make_world_panel("device-tablet-off.svg", r"T_i = 0", r"Y_{0i}", LIBRARY_COLOR)
        worlds = VGroup(left_world, right_world).arrange(RIGHT, buff=1.1)
        worlds.move_to(DOWN * 0.15)

        left_label = Text("factual", font_size=22, color=TABLET_COLOR, weight=BOLD)
        left_label.next_to(left_world, UP, buff=0.22)
        right_label = Text("counterfactual", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
        right_label.next_to(right_world, UP, buff=0.22)

        unseen = load_icon("eye-off.svg", NEUTRAL_COLOR, 0.78)
        unseen.next_to(right_world[0], DOWN, buff=0.18)

        impossible = Text("Both cannot be observed at once", font_size=25, color=QUESTION_COLOR, weight=BOLD)
        impossible.to_edge(DOWN, buff=0.78)
        impossible_line = Underline(impossible, color=QUESTION_COLOR, buff=0.12, stroke_width=2.4)
        counter_shade = SurroundingRectangle(
            right_world,
            buff=0.08,
            corner_radius=0.18,
            stroke_opacity=0,
            fill_color=BLACK,
            fill_opacity=0.0,
        )

        factual_world_pos = LEFT * 3.0 + DOWN * 0.08
        counter_world_pos = RIGHT * 3.0 + DOWN * 0.08

        # Intro:
        wait_for_chunks([1])

        # Beat 1:
        self.play(FadeIn(treatment_seed, scale=0.9), FadeIn(treatment_word, shift=UP * 0.08), run_time=1.0)
        self.wait(2.6)
        self.play(Create(up_arrow), Create(down_arrow), run_time=1.1)
        self.play(FadeIn(treatment_yes, shift=LEFT * 0.08), FadeIn(treatment_no, shift=LEFT * 0.08), run_time=1.0)
        self.play(
            FadeOut(treatment_group, shift=LEFT * 0.08),
            FadeIn(outcome_def, shift=UP * 0.12),
            FadeIn(outcome_icon, scale=0.9),
            run_time=1.0,
        )
        wait_for_chunks([2, 3], spent=6.7)

        # Beat 2:
        self.play(
            FadeOut(VGroup(outcome_def, outcome_icon), shift=UP * 0.1),
            FadeIn(worlds, shift=UP * 0.12),
            run_time=1.1,
        )
        wait_for_chunks([4, 5], spent=1.1)

        # Beat 3:
        self.play(
            left_world.animate.move_to(factual_world_pos),
            right_world.animate.move_to(counter_world_pos),
            FadeIn(left_label, shift=UP * 0.1),
            FadeIn(right_label, shift=UP * 0.1),
            run_time=1.1,
        )
        counter_shade.move_to(right_world)
        self.play(
            counter_shade.animate.set_fill(opacity=0.5),
            FadeIn(unseen, scale=0.9),
            FadeIn(impossible, shift=UP * 0.08),
            Create(impossible_line),
            run_time=1.0,
        )
        wait_for_chunks([6], spent=2.1)
        self.wait(self.WAIT_TAIL)


class Scene04_MultiverseIteAteAtt(Scene):
    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("04_multiverse_ite_ate_att")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        ite_title = MathTex(r"ITE_i", r"=", r"Y_{1i}", r"-", r"Y_{0i}")
        ite_title.scale(1.08)
        ite_title[0].set_color(ACCENT_COLOR)
        ite_title[2].set_color(TABLET_COLOR)
        ite_title[4].set_color(LIBRARY_COLOR)
        ite_title.to_edge(UP, buff=0.65)

        left_frame = RoundedRectangle(
            width=2.55,
            height=2.6,
            corner_radius=0.18,
            stroke_color=TABLET_COLOR,
            stroke_width=2.6,
        )
        left_treat = MathTex(r"T_i = 1").scale(0.9).set_color(TABLET_COLOR)
        left_icon = load_icon("device-tablet.svg", TABLET_COLOR, 0.8)
        left_outcome = MathTex(r"Y_{1i}").scale(1.0).set_color(WHITE)
        left_group = VGroup(left_treat, left_icon, left_outcome).arrange(DOWN, buff=0.22)
        left_group.move_to(left_frame.get_center())
        left_world = VGroup(left_frame, left_group)
        left_world.move_to(LEFT * 2.2 + DOWN * 0.05)

        right_frame = RoundedRectangle(
            width=2.55,
            height=2.6,
            corner_radius=0.18,
            stroke_color=LIBRARY_COLOR,
            stroke_width=2.6,
        )
        right_treat = MathTex(r"T_i = 0").scale(0.9).set_color(LIBRARY_COLOR)
        right_icon = load_icon("device-tablet-off.svg", LIBRARY_COLOR, 0.8)
        right_outcome = MathTex(r"Y_{0i}").scale(1.0).set_color(WHITE)
        right_group = VGroup(right_treat, right_icon, right_outcome).arrange(DOWN, buff=0.22)
        right_group.move_to(right_frame.get_center())
        right_world = VGroup(right_frame, right_group)
        right_world.move_to(RIGHT * 2.2 + DOWN * 0.05)

        ite_arrow = DoubleArrow(
            left_world.get_right() + RIGHT * 0.08,
            right_world.get_left() + LEFT * 0.08,
            buff=0.1,
            stroke_width=4,
            color=ACCENT_COLOR,
        )

        ate_def = MathTex(r"ATE", r"=", r"E[Y_1 - Y_0]")
        ate_def.scale(0.98)
        ate_def[0].set_color(ACCENT_COLOR)
        ate_def.move_to(ORIGIN)
        ate_expand = VGroup(
            Text("Average", font_size=23, color=WHITE, weight=BOLD),
            Text("Treatment", font_size=23, color=ACCENT_COLOR, weight=BOLD),
            Text("Effect", font_size=23, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.16)
        ate_expand.next_to(ate_def, DOWN, buff=0.34)

        att_def = MathTex(r"ATT", r"=", r"E[Y_1 - Y_0 \mid T=1]")
        att_def.scale(0.94)
        att_def[0].set_color(QUESTION_COLOR)
        att_def.move_to(ORIGIN)
        att_expand = VGroup(
            Text("Average", font_size=22, color=WHITE, weight=BOLD),
            Text("Treatment", font_size=22, color=QUESTION_COLOR, weight=BOLD),
            Text("Effect", font_size=22, color=WHITE, weight=BOLD),
            Text("on the Treated", font_size=22, color=NEUTRAL_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.14)
        att_expand.next_to(att_def, DOWN, buff=0.34)

        avg_hint = Text("All units", font_size=25, color=NEUTRAL_COLOR, weight=BOLD)
        avg_hint.next_to(ate_expand, DOWN, buff=0.28)
        att_hint = Text("Treated units only", font_size=25, color=NEUTRAL_COLOR, weight=BOLD)
        att_hint.move_to(avg_hint)

        # Beat 1:
        self.play(FadeIn(ite_title, shift=UP * 0.08), run_time=0.8)
        self.play(
            FadeIn(left_world, shift=RIGHT * 0.18),
            FadeIn(right_world, shift=LEFT * 0.18),
            run_time=1.0,
        )
        self.play(GrowArrow(ite_arrow), run_time=0.7)
        wait_for_chunks([1, 2], spent=2.5)

        # Beat 2:
        self.play(
            FadeOut(ite_arrow),
            left_world.animate.move_to(LEFT * 2.2 + DOWN * 0.05),
            right_world.animate.move_to(RIGHT * 2.2 + DOWN * 0.05),
            run_time=0.9,
        )
        veil = Rectangle(
            width=right_world.width * 0.96,
            height=right_world.height * 0.96,
            stroke_width=0,
            fill_color=BLACK,
            fill_opacity=0.62,
        ).move_to(right_world)
        eye_off = load_icon("eye-off.svg", WHITE, 0.72).move_to(right_world.get_center() + DOWN * 0.15)

        self.play(Indicate(left_world, color=TABLET_COLOR, scale_factor=1.02), run_time=0.7)
        self.play(FadeIn(veil), FadeIn(eye_off), run_time=0.6)
        wait_for_chunks([3], spent=2.2)

        # Beat 3:
        self.play(
            FadeOut(VGroup(left_world, right_world, veil, eye_off), shift=DOWN * 0.1),
            FadeOut(ite_title, shift=UP * 0.08),
            run_time=0.9,
        )
        self.play(FadeIn(ate_def, shift=UP * 0.08), run_time=0.7)
        self.play(FadeIn(ate_expand, shift=UP * 0.08), run_time=0.6)
        self.play(FadeIn(avg_hint, shift=UP * 0.08), run_time=0.6)
        wait_for_chunks([4], spent=2.8)
        self.play(
            TransformMatchingTex(ate_def, att_def),
            FadeTransform(ate_expand, att_expand),
            FadeTransform(avg_hint, att_hint),
            run_time=0.9,
        )
        wait_for_chunks([5], spent=0.9)
        self.wait(self.WAIT_TAIL)


class Scene05_MultiverseTableAteAtt(Scene):
    WAIT_TAIL = 0.05

    def construct(self):
        chunk_durations = load_scene_timing_durations("05_multiverse_table_ate_att")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        def get_chunk_duration(index: int, fallback: float) -> float:
            if not chunk_durations or index - 1 >= len(chunk_durations):
                return fallback
            return chunk_durations[index - 1]

        def make_table_cell(content: Mobject, width: float, height: float, stroke_color=GREY_B) -> VGroup:
            box = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.08,
                stroke_color=stroke_color,
                stroke_width=1.8,
                fill_opacity=0.0,
            )
            content.move_to(box.get_center())
            return VGroup(box, content)

        headers = [
            (MathTex(r"i"), 0.58, 0.56, GREY_B),
            (MathTex(r"Y_0").set_color(LIBRARY_COLOR), 1.02, 0.56, LIBRARY_COLOR),
            (MathTex(r"Y_1").set_color(TABLET_COLOR), 1.02, 0.56, TABLET_COLOR),
            (MathTex(r"T").set_color(TABLET_COLOR), 0.64, 0.56, TABLET_COLOR),
            (MathTex(r"Y").set_color(WHITE), 0.92, 0.56, GREY_B),
            (MathTex(r"ITE").set_color(ACCENT_COLOR), 1.08, 0.56, ACCENT_COLOR),
        ]
        rows = [
            ["1", "500", "450", "0", "500", "-50"],
            ["2", "600", "600", "0", "600", "0"],
            ["3", "800", "600", "1", "600", "-200"],
            ["4", "700", "750", "1", "750", "50"],
        ]
        col_widths = [0.58, 1.02, 1.02, 0.64, 0.92, 1.08]

        header_cells = VGroup(
            *[
                make_table_cell(label.scale(0.74), width, height, color)
                for label, width, height, color in headers
            ]
        ).arrange(RIGHT, buff=0.08)

        body_rows = VGroup()
        for row in rows:
            row_cells = []
            for idx, value in enumerate(row):
                color = WHITE
                if idx == 1:
                    color = LIBRARY_COLOR
                elif idx == 2 or idx == 3:
                    color = TABLET_COLOR
                elif idx == 5:
                    color = ACCENT_COLOR
                cell = make_table_cell(
                    MathTex(value).scale(0.72).set_color(color),
                    col_widths[idx],
                    0.62,
                    GREY_B,
                )
                row_cells.append(cell)
            body_rows.add(VGroup(*row_cells).arrange(RIGHT, buff=0.08))
        body_rows.arrange(DOWN, buff=0.08)

        table_group = VGroup(header_cells, body_rows).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        table_group.move_to(UP * 0.2)

        treated_row_boxes = VGroup(*[cell[0] for row in (body_rows[2], body_rows[3]) for cell in row])
        treated_t_boxes = VGroup(body_rows[2][3][0], body_rows[3][3][0])
        treated_hint = VGroup(
            MathTex(r"T=1").scale(0.76).set_color(QUESTION_COLOR),
            Text("treated only", font_size=20, color=QUESTION_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        treated_hint.next_to(table_group, RIGHT, buff=0.42)
        treated_hint.align_to(VGroup(body_rows[2][3], body_rows[3][3]), UP)

        untreated_rows = VGroup(body_rows[0], body_rows[1])
        untreated_row_boxes = VGroup(*[cell[0] for row in untreated_rows for cell in row])
        untreated_y0_boxes = VGroup(body_rows[0][1][0], body_rows[1][1][0])
        untreated_y1_boxes = VGroup(body_rows[0][2][0], body_rows[1][2][0])
        untreated_y_boxes = VGroup(body_rows[0][4][0], body_rows[1][4][0])
        all_row_boxes = VGroup(*[cell[0] for row in body_rows for cell in row])
        y0_column_boxes = VGroup(*[row[1][0] for row in body_rows])
        y1_column_boxes = VGroup(*[row[2][0] for row in body_rows])
        t_column_boxes = VGroup(*[row[3][0] for row in body_rows])
        observed_y_boxes = VGroup(*[row[4][0] for row in body_rows])
        ite_column_boxes = VGroup(*[row[5][0] for row in body_rows])
        row_outcome_boxes = VGroup(*[box for row in body_rows for box in (row[1][0], row[2][0])])
        school1_boxes = VGroup(body_rows[0][1][0], body_rows[0][2][0], body_rows[0][5][0])
        school3_boxes = VGroup(body_rows[2][1][0], body_rows[2][2][0], body_rows[2][5][0])
        treated_y0_boxes = VGroup(body_rows[2][1][0], body_rows[3][1][0])
        treated_y1_boxes = VGroup(body_rows[2][2][0], body_rows[3][2][0])
        treated_y_boxes = VGroup(body_rows[2][4][0], body_rows[3][4][0])
        y0_boxes = VGroup(body_rows[2][1][0], body_rows[3][1][0])
        y1_boxes = VGroup(body_rows[2][2][0], body_rows[3][2][0])
        outcome_header_boxes = VGroup(header_cells[1][0], header_cells[2][0])

        portal = load_icon("world-question.svg", ACCENT_COLOR, 1.0)
        portal.move_to(UP * 2.0)
        portal_ring = Circle(radius=0.8, stroke_color=ACCENT_COLOR, stroke_width=2.8).move_to(portal)
        portal_label = Text("multiverse", font_size=22, color=ACCENT_COLOR, weight=BOLD)
        portal_label.next_to(portal_ring, DOWN, buff=0.16)

        school = load_icon("school.svg", WHITE, 0.95)
        school.move_to(DOWN * 0.15)
        school_tag = MathTex(r"i").scale(0.9).next_to(school, DOWN, buff=0.18)

        left_outcome = VGroup(
            MathTex(r"Y_0").set_color(LIBRARY_COLOR),
            MathTex(r"500").set_color(LIBRARY_COLOR),
        ).arrange(DOWN, buff=0.12)
        left_outcome.move_to(LEFT * 2.25 + DOWN * 0.2)
        right_outcome = VGroup(
            MathTex(r"Y_1").set_color(TABLET_COLOR),
            MathTex(r"450").set_color(TABLET_COLOR),
        ).arrange(DOWN, buff=0.12)
        right_outcome.move_to(RIGHT * 2.25 + DOWN * 0.2)

        left_arrow = CurvedArrow(
            school.get_left() + LEFT * 0.08 + UP * 0.2,
            left_outcome.get_right() + RIGHT * 0.1,
            angle=0.35,
            color=LIBRARY_COLOR,
            stroke_width=3.4,
        )
        right_arrow = CurvedArrow(
            school.get_right() + RIGHT * 0.08 + UP * 0.2,
            right_outcome.get_left() + LEFT * 0.1,
            angle=-0.35,
            color=TABLET_COLOR,
            stroke_width=3.4,
        )

        ate_formula = MathTex(r"ATE", r"=", r"\frac{-50 + 0 - 200 + 50}{4}", r"=", r"-50")
        ate_formula.scale(0.82)
        ate_formula[0].set_color(ACCENT_COLOR)
        ate_formula[-1].set_color(ACCENT_COLOR)
        ate_formula.next_to(table_group, DOWN, buff=0.52)

        att_formula = MathTex(r"ATT", r"=", r"\frac{-200 + 50}{2}", r"=", r"-75")
        att_formula.scale(0.82)
        att_formula[0].set_color(QUESTION_COLOR)
        att_formula[-1].set_color(QUESTION_COLOR)
        att_formula.move_to(ate_formula)

        untreated_fact_label = VGroup(
            MathTex(r"T=0").scale(0.68).set_color(WHITE),
            Text("Y0 factual", font_size=16, color=LIBRARY_COLOR, weight=BOLD),
            Text("Y1 counterfactual", font_size=16, color=TABLET_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        treated_fact_label = VGroup(
            MathTex(r"T=1").scale(0.68).set_color(WHITE),
            Text("Y1 factual", font_size=16, color=TABLET_COLOR, weight=BOLD),
            Text("Y0 counterfactual", font_size=16, color=LIBRARY_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        factual_legend = VGroup(untreated_fact_label, treated_fact_label).arrange(RIGHT, buff=0.42, aligned_edge=UP)
        factual_legend.next_to(table_group, DOWN, buff=0.3)

        # Beat 1:
        self.play(Create(portal_ring), FadeIn(portal, scale=0.9), FadeIn(portal_label, shift=UP * 0.08), run_time=0.9)
        self.play(FadeIn(school, scale=0.9), FadeIn(school_tag, shift=UP * 0.08), run_time=0.8)
        self.play(Create(left_arrow), Create(right_arrow), FadeIn(left_outcome), FadeIn(right_outcome), run_time=1.0)
        wait_for_chunks([1], spent=2.7)

        # Beat 2:
        self.play(
            FadeOut(VGroup(portal_ring, portal, portal_label, school, school_tag, left_arrow, right_arrow, left_outcome, right_outcome)),
            FadeIn(table_group, shift=UP * 0.12),
            run_time=1.0,
        )
        self.play(
            header_cells[1][0].animate.set_stroke(LIBRARY_COLOR, width=3.0),
            header_cells[2][0].animate.set_stroke(TABLET_COLOR, width=3.0),
            *[box.animate.set_stroke(LIBRARY_COLOR, width=2.8) for box in y0_column_boxes],
            *[box.animate.set_stroke(TABLET_COLOR, width=2.8) for box in y1_column_boxes],
            run_time=0.8,
        )
        self.play(
            LaggedStart(
                *[
                    AnimationGroup(
                        row[1][0].animate.set_fill(LIBRARY_COLOR, opacity=0.12),
                        row[2][0].animate.set_fill(TABLET_COLOR, opacity=0.12),
                    )
                    for row in body_rows
                ],
                lag_ratio=0.16,
            ),
            run_time=1.1,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=ACCENT_COLOR, scale_factor=1.02) for box in row_outcome_boxes],
                lag_ratio=0.05,
            ),
            run_time=0.9,
        )
        wait_for_chunks([2], spent=4.0)
        self.play(
            *[box.animate.set_fill(opacity=0.0) for box in row_outcome_boxes],
            run_time=0.25,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=QUESTION_COLOR, scale_factor=1.02) for box in VGroup(header_cells[3][0], *t_column_boxes)],
                lag_ratio=0.1,
            ),
            run_time=0.75,
        )
        self.wait(1.35)
        self.play(
            LaggedStart(
                *[Indicate(box, color=WHITE, scale_factor=1.02) for box in VGroup(header_cells[4][0], *observed_y_boxes)],
                lag_ratio=0.1,
            ),
            run_time=0.75,
        )
        wait_for_chunks([3], spent=2.85)
        self.play(
            *[box.animate.set_fill(ACCENT_COLOR, opacity=0.12).set_stroke(ACCENT_COLOR, width=2.6) for box in row_outcome_boxes],
            run_time=0.55,
        )
        self.play(
            LaggedStart(
                *[
                    Indicate(VGroup(row[1][0], row[2][0]), color=ACCENT_COLOR, scale_factor=1.02)
                    for row in body_rows
                ],
                lag_ratio=0.12,
            ),
            run_time=0.7,
        )
        self.play(
            header_cells[5][0].animate.set_stroke(ACCENT_COLOR, width=3.0),
            *[box.animate.set_fill(ACCENT_COLOR, opacity=0.14).set_stroke(ACCENT_COLOR, width=2.8) for box in ite_column_boxes],
            run_time=0.55,
        )
        wait_for_chunks([4], spent=1.25)
        self.play(
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in row_outcome_boxes],
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in ite_column_boxes],
            header_cells[5][0].animate.set_stroke(ACCENT_COLOR, width=1.8),
            run_time=0.2,
        )
        self.play(
            school3_boxes[0].animate.set_fill(LIBRARY_COLOR, opacity=0.18).set_stroke(LIBRARY_COLOR, width=3.0),
            school3_boxes[1].animate.set_fill(TABLET_COLOR, opacity=0.18).set_stroke(TABLET_COLOR, width=3.0),
            school3_boxes[2].animate.set_fill(ACCENT_COLOR, opacity=0.18).set_stroke(ACCENT_COLOR, width=3.0),
            school1_boxes[0].animate.set_fill(LIBRARY_COLOR, opacity=0.18).set_stroke(LIBRARY_COLOR, width=3.0),
            school1_boxes[1].animate.set_fill(TABLET_COLOR, opacity=0.18).set_stroke(TABLET_COLOR, width=3.0),
            school1_boxes[2].animate.set_fill(ACCENT_COLOR, opacity=0.18).set_stroke(ACCENT_COLOR, width=3.0),
            run_time=0.6,
        )
        self.play(Indicate(school1_boxes, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.45)
        self.play(
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in school1_boxes],
            run_time=0.15,
        )
        self.play(Indicate(school3_boxes, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.45)
        self.play(
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in school3_boxes],
            run_time=0.15,
        )
        wait_for_chunks([5], spent=1.8)
        self.play(
            *[box.animate.set_fill(opacity=0.0) for box in row_outcome_boxes],
            header_cells[1][0].animate.set_stroke(LIBRARY_COLOR, width=1.8),
            header_cells[2][0].animate.set_stroke(TABLET_COLOR, width=1.8),
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in y0_column_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in y1_column_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in t_column_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in observed_y_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in ite_column_boxes],
            run_time=0.5,
        )

        # Beat 3:
        self.play(
            *[box.animate.set_fill(ACCENT_COLOR, opacity=0.08) for box in all_row_boxes],
            *[box.animate.set_stroke(ACCENT_COLOR, width=2.1) for box in all_row_boxes],
            FadeIn(ate_formula, shift=UP * 0.08),
            run_time=0.7,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=ACCENT_COLOR, scale_factor=1.015) for box in all_row_boxes],
                lag_ratio=0.04,
            ),
            run_time=0.7,
        )
        wait_for_chunks([6], spent=1.4)
        wait_for_chunks([7])

        # Beat 4:
        self.play(
            untreated_rows.animate.set_opacity(0.28),
            *[box.animate.set_fill(opacity=0.0) for box in all_row_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in all_row_boxes],
            *[box.animate.set_fill(QUESTION_COLOR, opacity=0.12) for box in treated_row_boxes],
            *[box.animate.set_stroke(QUESTION_COLOR, width=2.4) for box in treated_row_boxes],
            *[box.animate.set_fill(QUESTION_COLOR, opacity=0.22) for box in treated_t_boxes],
            *[box.animate.set_stroke(QUESTION_COLOR, width=3.0) for box in treated_t_boxes],
            FadeIn(treated_hint, shift=RIGHT * 0.08),
            TransformMatchingTex(ate_formula, att_formula),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=QUESTION_COLOR, scale_factor=1.03) for box in treated_t_boxes],
                lag_ratio=0.12,
            ),
            run_time=0.6,
        )
        wait_for_chunks([8], spent=1.5)
        self.play(Indicate(att_formula[-1], color=QUESTION_COLOR, scale_factor=1.08), run_time=0.55)
        wait_for_chunks([9], spent=0.55)
        self.play(
            LaggedStart(
                *[Indicate(box, color=QUESTION_COLOR, scale_factor=1.025) for box in treated_row_boxes],
                lag_ratio=0.08,
            ),
            run_time=0.8,
        )
        wait_for_chunks([10], spent=0.8)

        # Beat 5:
        self.play(
            FadeOut(att_formula),
            FadeOut(treated_hint),
            untreated_rows.animate.set_opacity(1.0),
            *[box.animate.set_fill(BLACK, opacity=0.0) for box in untreated_row_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in untreated_row_boxes],
            *[box.animate.set_fill(opacity=0.0) for box in treated_row_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in treated_row_boxes],
            *[box.animate.set_fill(opacity=0.0) for box in treated_t_boxes],
            *[box.animate.set_stroke(GREY_B, width=1.8) for box in treated_t_boxes],
            run_time=0.6,
        )
        self.play(
            *[box.animate.set_stroke(LIBRARY_COLOR, width=2.4) for box in untreated_y0_boxes],
            *[box.animate.set_stroke(TABLET_COLOR, width=2.4) for box in untreated_y1_boxes],
            *[box.animate.set_stroke(TABLET_COLOR, width=2.4) for box in treated_y1_boxes],
            *[box.animate.set_stroke(LIBRARY_COLOR, width=2.4) for box in treated_y0_boxes],
            *[box.animate.set_fill(LIBRARY_COLOR, opacity=0.1) for box in untreated_y0_boxes],
            *[box.animate.set_fill(TABLET_COLOR, opacity=0.1) for box in treated_y1_boxes],
            *[box.animate.set_fill(TABLET_COLOR, opacity=0.06) for box in untreated_y1_boxes],
            *[box.animate.set_fill(LIBRARY_COLOR, opacity=0.06) for box in treated_y0_boxes],
            *[box.animate.set_stroke(WHITE, width=2.8) for box in untreated_y_boxes],
            *[box.animate.set_stroke(WHITE, width=2.8) for box in treated_y_boxes],
            FadeIn(factual_legend, shift=UP * 0.08),
            run_time=0.9,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=WHITE, scale_factor=1.02) for box in untreated_y_boxes],
                *[Indicate(box, color=WHITE, scale_factor=1.02) for box in treated_y_boxes],
                lag_ratio=0.08,
            ),
            run_time=0.8,
        )
        wait_for_chunks([11], spent=1.7)
        self.wait(self.WAIT_TAIL)


class Scene06_ObservedMeanDifferenceTrap(Scene):
    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("06_observed_mean_difference_trap")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        def make_table_cell(content: Mobject, width: float, height: float, stroke_color=GREY_B) -> VGroup:
            box = RoundedRectangle(
                width=width,
                height=height,
                corner_radius=0.08,
                stroke_color=stroke_color,
                stroke_width=1.8,
                fill_opacity=0.0,
            )
            content.move_to(box.get_center())
            return VGroup(box, content)

        headers = [
            (MathTex(r"i"), 0.54, 0.56, GREY_B),
            (MathTex(r"Y_0").set_color(LIBRARY_COLOR), 1.0, 0.56, LIBRARY_COLOR),
            (MathTex(r"Y_1").set_color(TABLET_COLOR), 1.0, 0.56, TABLET_COLOR),
            (MathTex(r"T").set_color(TABLET_COLOR), 0.66, 0.56, TABLET_COLOR),
            (MathTex(r"Y").set_color(WHITE), 0.9, 0.56, GREY_B),
            (MathTex(r"ITE").set_color(ACCENT_COLOR), 0.96, 0.56, ACCENT_COLOR),
        ]
        full_rows = [
            ["1", "500", "450", "0", "500", "-50"],
            ["2", "600", "600", "0", "600", "0"],
            ["3", "800", "600", "1", "600", "-200"],
            ["4", "700", "750", "1", "750", "50"],
        ]
        observed_rows = [
            ["1", "500", None, "0", "500", None],
            ["2", "600", None, "0", "600", None],
            ["3", None, "600", "1", "600", None],
            ["4", None, "750", "1", "750", None],
        ]
        col_widths = [0.54, 1.0, 1.0, 0.66, 0.9, 0.96]

        header_cells = VGroup(
            *[make_table_cell(label.scale(0.72), width, height, color) for label, width, height, color in headers]
        ).arrange(RIGHT, buff=0.08)

        body_rows = VGroup()
        for row in full_rows:
            row_cells = []
            for idx, value in enumerate(row):
                color = WHITE
                if idx == 1:
                    color = LIBRARY_COLOR
                elif idx == 2 or idx == 3:
                    color = TABLET_COLOR
                elif idx == 5:
                    color = ACCENT_COLOR
                cell = make_table_cell(
                    MathTex(value).scale(0.72).set_color(color),
                    col_widths[idx],
                    0.62,
                    GREY_B,
                )
                row_cells.append(cell)
            body_rows.add(VGroup(*row_cells).arrange(RIGHT, buff=0.08))
        body_rows.arrange(DOWN, buff=0.08)

        table_group = VGroup(header_cells, body_rows).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        table_group.scale(0.92)
        table_group.move_to(UP * 0.18)

        y0_boxes = VGroup(*[row[1][0] for row in body_rows])
        y1_boxes = VGroup(*[row[2][0] for row in body_rows])
        t_boxes = VGroup(*[row[3][0] for row in body_rows])
        y_boxes = VGroup(*[row[4][0] for row in body_rows])
        te_boxes = VGroup(*[row[5][0] for row in body_rows])

        hidden_y1 = VGroup(body_rows[0][2], body_rows[1][2])
        hidden_y0 = VGroup(body_rows[2][1], body_rows[3][1])
        all_ite_cells = VGroup(*[row[5] for row in body_rows])

        for row_idx, row in enumerate(observed_rows):
            for col_idx, value in enumerate(row):
                if value is None:
                    box = body_rows[row_idx][col_idx][0]
                    if col_idx == 5:
                        eye = load_icon("eye-off.svg", ACCENT_COLOR, 0.48)
                    elif col_idx == 1:
                        eye = load_icon("eye-off.svg", LIBRARY_COLOR, 0.48)
                    else:
                        eye = load_icon("eye-off.svg", TABLET_COLOR, 0.48)
                    body_rows[row_idx][col_idx][1].become(eye.move_to(box.get_center()))

        control_rows = VGroup(body_rows[0], body_rows[1])
        treated_rows = VGroup(body_rows[2], body_rows[3])
        control_y_boxes = VGroup(body_rows[0][4][0], body_rows[1][4][0])
        treated_y_boxes = VGroup(body_rows[2][4][0], body_rows[3][4][0])

        reality_label = Text("In reality, only observed outcomes remain", font_size=22, color=ACCENT_COLOR, weight=BOLD)
        reality_label.next_to(table_group, UP, buff=0.34)
        table_block = VGroup(table_group, reality_label)

        direct_calc_formula = MathTex(r"ITE_i,\ ATE,\ ATT").scale(0.92).set_color(ACCENT_COLOR)
        direct_calc_cross = Cross(direct_calc_formula, stroke_color=MAROON_E, stroke_width=7)
        direct_calc_block = VGroup(direct_calc_formula, direct_calc_cross)
        direct_calc_block.next_to(table_group, DOWN, buff=0.34)

        temptation = VGroup(
            Text("Why not just compare", font_size=26, color=NEUTRAL_COLOR, weight=BOLD),
            Text("the average of two groups?", font_size=30, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.18)
        temptation.scale(0.9)
        temptation.move_to(RIGHT * 3.95 + DOWN * 0.05)

        treated_mean_card = RoundedRectangle(width=3.45, height=1.6, corner_radius=0.16, stroke_color=TABLET_COLOR, stroke_width=2.4)
        control_mean_card = RoundedRectangle(width=3.45, height=1.6, corner_radius=0.16, stroke_color=LIBRARY_COLOR, stroke_width=2.4)
        treated_mean_card.move_to(RIGHT * 4.2 + UP * 0.95)
        control_mean_card.move_to(RIGHT * 4.2 + DOWN * 0.95)

        treated_mean = VGroup(
            Text("treated mean", font_size=20, color=TABLET_COLOR, weight=BOLD),
            MathTex(r"(600 + 750)/2 = 675").scale(0.68).set_color(WHITE),
        ).arrange(DOWN, buff=0.12).move_to(treated_mean_card)
        control_mean = VGroup(
            Text("control mean", font_size=20, color=LIBRARY_COLOR, weight=BOLD),
            MathTex(r"(500 + 600)/2 = 550").scale(0.68).set_color(WHITE),
        ).arrange(DOWN, buff=0.12).move_to(control_mean_card)

        observed_formula = MathTex(
            r"E[Y\mid T=1] - E[Y\mid T=0]",
            r"=",
            r"675 - 550",
            r"=",
            r"125",
        ).scale(0.84)
        observed_formula[0].set_color(WHITE)
        observed_formula[2].set_color(WHITE)
        observed_formula[4].set_color(TABLET_COLOR)
        observed_formula.move_to(ORIGIN + DOWN * 0.15)

        observed_positive = MathTex(r"+125").scale(1.5).set_color(TABLET_COLOR)
        observed_positive.move_to(ORIGIN + DOWN * 0.05)
        observed_positive_label = Text("Observed mean difference", font_size=22, color=TABLET_COLOR, weight=BOLD)
        observed_positive_label.next_to(observed_positive, UP, buff=0.28)

        true_ate = MathTex(r"-50").scale(1.5).set_color(MAROON_E)
        true_ate.move_to(ORIGIN + DOWN * 0.05)
        true_ate_label = Text("True ATE", font_size=22, color=ACCENT_COLOR, weight=BOLD)
        true_ate_label.next_to(true_ate, UP, buff=0.28)

        sign_flip = MathTex(r"+125", r"\ne", r"-50").scale(1.05)
        sign_flip[0].set_color(TABLET_COLOR)
        sign_flip[1].set_color(MAROON_E)
        sign_flip[2].set_color(MAROON_E)
        sign_flip.next_to(true_ate, DOWN, buff=0.42)

        closing = VGroup(
            Text("observed association", font_size=32, color=WHITE, weight=BOLD),
            MathTex(r"\ne").scale(1.2).set_color(ACCENT_COLOR),
            Text("causal effect", font_size=34, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.24)
        closing.move_to(UP * 0.55)
        why_next = Text("Where does this gap come from?", font_size=28, color=QUESTION_COLOR, weight=BOLD)
        why_next.next_to(closing, DOWN, buff=0.34)

        # Beat 1:
        self.play(FadeIn(reality_label, shift=UP * 0.08), FadeIn(table_group, shift=UP * 0.08), run_time=0.9)
        self.play(
            *[box.animate.set_fill(LIBRARY_COLOR, opacity=0.12).set_stroke(LIBRARY_COLOR, width=2.4) for box in VGroup(body_rows[0][1][0], body_rows[1][1][0])],
            *[box.animate.set_fill(TABLET_COLOR, opacity=0.12).set_stroke(TABLET_COLOR, width=2.4) for box in VGroup(body_rows[2][2][0], body_rows[3][2][0])],
            *[box.animate.set_fill(WHITE, opacity=0.08).set_stroke(WHITE, width=2.2) for box in y_boxes],
            run_time=0.7,
        )
        self.play(
            *[box.animate.set_fill(BLACK, opacity=0.38).set_stroke(TABLET_COLOR, width=2.2) for box in VGroup(hidden_y1[0][0], hidden_y1[1][0])],
            *[box.animate.set_fill(BLACK, opacity=0.38).set_stroke(LIBRARY_COLOR, width=2.2) for box in VGroup(hidden_y0[0][0], hidden_y0[1][0])],
            *[box.animate.set_fill(BLACK, opacity=0.42).set_stroke(ACCENT_COLOR, width=2.2) for box in VGroup(*[cell[0] for cell in all_ite_cells])],
            run_time=0.8,
        )
        self.wait(5.2)
        self.play(
            FadeIn(VGroup(*[cell[1] for cell in hidden_y1]), scale=0.9),
            FadeIn(VGroup(*[cell[1] for cell in hidden_y0]), scale=0.9),
            FadeIn(VGroup(*[cell[1] for cell in all_ite_cells]), scale=0.9),
            FadeIn(direct_calc_formula, shift=UP * 0.08),
            run_time=0.35,
        )
        self.wait(0.55)
        self.play(Create(direct_calc_cross), run_time=0.45)
        wait_for_chunks([1, 2], spent=9.1)

        # Beat 2:
        self.play(
            FadeOut(direct_calc_block, shift=DOWN * 0.08),
            FadeOut(reality_label, shift=UP * 0.08),
            table_group.animate.shift(LEFT * 1.45),
            FadeIn(temptation, shift=UP * 0.08),
            run_time=0.85,
        )
        wait_for_chunks([3], spent=0.85)

        # Beat 3:
        self.play(
            FadeOut(temptation, shift=UP * 0.08),
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in y0_boxes],
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in y1_boxes],
            *[box.animate.set_fill(opacity=0.0).set_stroke(GREY_B, width=1.8) for box in te_boxes],
            *[box.animate.set_stroke(TABLET_COLOR, width=2.5) for box in t_boxes],
            *[box.animate.set_stroke(WHITE, width=2.5) for box in y_boxes],
            run_time=0.7,
        )
        self.play(
            LaggedStart(
                *[Indicate(box, color=WHITE, scale_factor=1.025) for box in y_boxes],
                lag_ratio=0.08,
            ),
            run_time=0.7,
        )
        self.play(
            *[box.animate.set_fill(LIBRARY_COLOR, opacity=0.12).set_stroke(LIBRARY_COLOR, width=2.6) for box in control_y_boxes],
            FadeIn(control_mean_card),
            FadeIn(control_mean, shift=RIGHT * 0.08),
            run_time=0.75,
        )
        self.play(
            *[box.animate.set_fill(TABLET_COLOR, opacity=0.12).set_stroke(TABLET_COLOR, width=2.6) for box in treated_y_boxes],
            FadeIn(treated_mean_card),
            FadeIn(treated_mean, shift=RIGHT * 0.08),
            run_time=0.75,
        )
        wait_for_chunks([4], spent=2.9)

        # Beat 4:
        self.play(
            FadeOut(treated_mean_card),
            FadeOut(treated_mean),
            FadeOut(control_mean_card),
            FadeOut(control_mean),
            FadeOut(table_group, shift=LEFT * 0.18),
            FadeIn(observed_positive_label, shift=UP * 0.08),
            FadeIn(observed_formula, shift=UP * 0.08),
            run_time=0.7,
        )
        self.play(Indicate(observed_formula[-1], color=TABLET_COLOR, scale_factor=1.08), run_time=0.5)
        self.play(TransformMatchingTex(observed_formula, observed_positive), run_time=0.6)
        wait_for_chunks([5], spent=1.8)

        # Beat 5:
        self.play(
            FadeOut(observed_positive_label),
            FadeIn(true_ate_label, shift=UP * 0.08),
            TransformMatchingTex(observed_positive, true_ate),
            run_time=0.6,
        )
        self.play(
            FadeIn(sign_flip, shift=UP * 0.08),
            run_time=0.55,
        )
        wait_for_chunks([6], spent=1.15)

        # Beat 6:
        self.play(
            FadeOut(true_ate_label),
            FadeOut(true_ate),
            FadeOut(sign_flip),
            run_time=0.75,
        )
        self.play(FadeIn(closing, shift=UP * 0.08), run_time=0.6)
        self.play(FadeIn(why_next, shift=UP * 0.08), run_time=0.5)
        wait_for_chunks([7], spent=1.85)
        self.wait(self.WAIT_TAIL)


class Scene07_BiasDecomposition(Scene):
    WAIT_TAIL = 0.2

    def construct(self):
        chunk_durations = load_scene_timing_durations("07_bias_decomposition")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        bias_word = Text("Why isn't the simple mean difference a causal effect?", font_size=28, color=QUESTION_COLOR, weight=BOLD)
        bias_word.move_to(ORIGIN + UP * 0.7)

        avg_diff_box = RoundedRectangle(
            width=4.3,
            height=0.8,
            corner_radius=0.2,
            stroke_color=WHITE,
            stroke_width=1.8,
        )
        avg_diff_label = Text("Observed mean difference", font_size=26, color=WHITE, weight=BOLD).move_to(avg_diff_box)
        avg_diff_group = VGroup(avg_diff_box, avg_diff_label)
        avg_diff_group.move_to(ORIGIN + DOWN * 0.15)

        effect_box = RoundedRectangle(
            width=1.85,
            height=0.72,
            corner_radius=0.18,
            stroke_color=ACCENT_COLOR,
            stroke_width=1.8,
            fill_color=ACCENT_COLOR,
            fill_opacity=0.12,
        )
        effect_label = Text("effect", font_size=22, color=ACCENT_COLOR, weight=BOLD).move_to(effect_box)
        effect_group = VGroup(effect_box, effect_label)

        plus = MathTex(r"+").scale(0.9).set_color(WHITE)

        bias_box = RoundedRectangle(
            width=1.55,
            height=0.72,
            corner_radius=0.18,
            stroke_color=QUESTION_COLOR,
            stroke_width=1.8,
            fill_color=QUESTION_COLOR,
            fill_opacity=0.12,
        )
        bias_label = Text("bias", font_size=22, color=QUESTION_COLOR, weight=BOLD).move_to(bias_box)
        bias_group = VGroup(bias_box, bias_label)

        split_group = VGroup(effect_group, plus, bias_group).arrange(RIGHT, buff=0.24)
        split_group.move_to(avg_diff_group)

        treated_card = RoundedRectangle(width=3.55, height=3.0, corner_radius=0.18, stroke_color=TABLET_COLOR, stroke_width=2.6)
        control_card = RoundedRectangle(width=3.55, height=3.0, corner_radius=0.18, stroke_color=LIBRARY_COLOR, stroke_width=2.6)
        treated_card.move_to(LEFT * 2.7 + DOWN * 0.05)
        control_card.move_to(RIGHT * 2.7 + DOWN * 0.05)

        treated_group = VGroup(
            MathTex(r"T=1").set_color(TABLET_COLOR).scale(0.82),
            Text("Tablet given", font_size=24, color=TABLET_COLOR, weight=BOLD),
            VGroup(
                load_icon("school.svg", WHITE, 0.64),
                load_icon("arrow-up.svg", TABLET_COLOR, 0.56),
            ).arrange(RIGHT, buff=0.18),
            Text("May have scored\nhigher to begin with", font_size=18, color=WHITE, weight=BOLD),
        ).arrange(DOWN, buff=0.18).move_to(treated_card)
        control_group = VGroup(
            MathTex(r"T=0").set_color(LIBRARY_COLOR).scale(0.82),
            Text("No tablet", font_size=24, color=LIBRARY_COLOR, weight=BOLD),
            VGroup(
                load_icon("school.svg", WHITE, 0.64),
                load_icon("arrow-down.svg", LIBRARY_COLOR, 0.56),
            ).arrange(RIGHT, buff=0.18),
            Text("May have scored\nlower to begin with", font_size=18, color=WHITE, weight=BOLD),
        ).arrange(DOWN, buff=0.18).move_to(control_card)

        inequality = MathTex(r"E[Y_0\mid T=1]", r">", r"E[Y_0\mid T=0]").scale(1.0)
        inequality[0].set_color(TABLET_COLOR)
        inequality[1].set_color(ACCENT_COLOR)
        inequality[2].set_color(LIBRARY_COLOR)
        inequality.to_edge(DOWN, buff=0.7)

        observed_formula = MathTex(
            r"E[Y\mid T=1] - E[Y\mid T=0]",
            r"=",
            r"E[Y_1\mid T=1] - E[Y_0\mid T=0]",
        ).scale(0.9)
        observed_formula.move_to(ORIGIN)

        decomp_summary = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
            r"+",
            r"Bias",
        ).scale(1.0)
        decomp_summary[2].set_color(ACCENT_COLOR)
        decomp_summary[4].set_color(QUESTION_COLOR)
        decomp_summary.move_to(ORIGIN + UP * 0.5)

        att_detail = MathTex(r"ATT = E[Y_1-Y_0\mid T=1]").scale(0.84).set_color(ACCENT_COLOR)
        bias_detail = MathTex(r"Bias = E[Y_0\mid T=1]-E[Y_0\mid T=0]").scale(0.84).set_color(QUESTION_COLOR)
        att_detail.next_to(decomp_summary, DOWN, buff=0.5)
        bias_detail.next_to(att_detail, DOWN, buff=0.28)

        att_focus = SurroundingRectangle(att_detail, color=ACCENT_COLOR, buff=0.16, corner_radius=0.1)
        bias_focus = SurroundingRectangle(bias_detail, color=QUESTION_COLOR, buff=0.16, corner_radius=0.1)
        att_note = Text("True causal effect", font_size=20, color=ACCENT_COLOR, weight=BOLD).next_to(att_focus, RIGHT, buff=0.22)
        bias_note = Text("Pre-existing\ngroup difference", font_size=18, color=QUESTION_COLOR, weight=BOLD).next_to(bias_focus, RIGHT, buff=0.22)

        confounder_box = RoundedRectangle(width=4.4, height=2.1, corner_radius=0.18, stroke_color=NEUTRAL_COLOR, stroke_width=2.2).move_to(UP * 1.45)
        confounder_label = Text("School conditions", font_size=24, color=WHITE, weight=BOLD)
        confounder_label.move_to(confounder_box.get_top() + DOWN * 0.38)
        budget_chip = VGroup(
            load_icon("coin.svg", GOLD_E, 0.26),
            Text("Funding", font_size=17, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        location_chip = VGroup(
            load_icon("map-pin.svg", BLUE_E, 0.26),
            Text("Location", font_size=17, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        teacher_chip = VGroup(
            load_icon("user-star.svg", GREEN_E, 0.26),
            Text("Teacher quality", font_size=17, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        _row1_chips = VGroup(budget_chip, location_chip).arrange(RIGHT, buff=0.22)
        confounder_factors = VGroup(_row1_chips, teacher_chip).arrange(DOWN, buff=0.12)
        confounder_factors.move_to(confounder_box.get_center() + DOWN * 0.28)
        t_node = VGroup(Circle(radius=0.56, stroke_color=TABLET_COLOR, stroke_width=2.6), MathTex(r"T").set_color(TABLET_COLOR)).move_to(LEFT * 2.6 + DOWN * 0.35)
        y_node = VGroup(Circle(radius=0.56, stroke_color=ACCENT_COLOR, stroke_width=2.6), MathTex(r"Y").set_color(ACCENT_COLOR)).move_to(RIGHT * 2.6 + DOWN * 0.35)
        t_label = Text("Treatment", font_size=23, color=TABLET_COLOR, weight=BOLD).next_to(t_node, DOWN, buff=0.18)
        y_label = Text("Outcome", font_size=23, color=ACCENT_COLOR, weight=BOLD).next_to(y_node, DOWN, buff=0.18)
        c_to_t = Arrow(confounder_box.get_bottom() + LEFT * 0.42, t_node.get_top(), buff=0.12, color=NEUTRAL_COLOR, stroke_width=3.0)
        c_to_y = Arrow(confounder_box.get_bottom() + RIGHT * 0.42, y_node.get_top(), buff=0.12, color=NEUTRAL_COLOR, stroke_width=3.0)
        t_to_y = Arrow(t_node.get_right(), y_node.get_left(), buff=0.18, color=TABLET_COLOR, stroke_width=3.2)
        compare_axis = Line(LEFT * 1.7, RIGHT * 1.7, color=NEUTRAL_COLOR, stroke_width=2.2)
        compare_axis.to_edge(DOWN, buff=0.58)

        treated_bar = RoundedRectangle(
            width=0.56,
            height=1.18,
            corner_radius=0.1,
            stroke_color=TABLET_COLOR,
            stroke_width=2.4,
            fill_color=TABLET_COLOR,
            fill_opacity=0.15,
        )
        treated_bar.align_to(compare_axis, DOWN).shift(LEFT * 1.0)

        control_bar = RoundedRectangle(
            width=0.56,
            height=0.7,
            corner_radius=0.1,
            stroke_color=LIBRARY_COLOR,
            stroke_width=2.4,
            fill_color=LIBRARY_COLOR,
            fill_opacity=0.15,
        )
        control_bar.align_to(compare_axis, DOWN).shift(RIGHT * 1.0)

        treated_mark = MathTex(r"T=1").scale(0.68).set_color(TABLET_COLOR).next_to(treated_bar, DOWN, buff=0.12)
        control_mark = MathTex(r"T=0").scale(0.68).set_color(LIBRARY_COLOR).next_to(control_bar, DOWN, buff=0.12)
        compare_icon = load_icon("git-compare.svg", WHITE, 0.46).move_to(compare_axis.get_center() + UP * 0.48)
        compare_group = VGroup(compare_axis, treated_bar, control_bar, treated_mark, control_mark, compare_icon)

        balanced_axis = compare_axis.copy()
        balanced_treated_bar = RoundedRectangle(
            width=0.56,
            height=0.94,
            corner_radius=0.1,
            stroke_color=TABLET_COLOR,
            stroke_width=2.4,
            fill_color=TABLET_COLOR,
            fill_opacity=0.15,
        )
        balanced_treated_bar.align_to(balanced_axis, DOWN).shift(LEFT * 1.0)
        balanced_control_bar = RoundedRectangle(
            width=0.56,
            height=0.94,
            corner_radius=0.1,
            stroke_color=LIBRARY_COLOR,
            stroke_width=2.4,
            fill_color=LIBRARY_COLOR,
            fill_opacity=0.15,
        )
        balanced_control_bar.align_to(balanced_axis, DOWN).shift(RIGHT * 1.0)
        balanced_treated_mark = treated_mark.copy().next_to(balanced_treated_bar, DOWN, buff=0.12)
        balanced_control_mark = control_mark.copy().next_to(balanced_control_bar, DOWN, buff=0.12)
        equal_icon = load_icon("equal.svg", ACCENT_COLOR, 0.48).move_to(compare_icon)
        check_icon = load_icon("check.svg", ACCENT_COLOR, 0.38).next_to(equal_icon, UP, buff=0.08)
        balanced_icon = VGroup(equal_icon, check_icon)
        balanced_group = VGroup(
            balanced_axis,
            balanced_treated_bar,
            balanced_control_bar,
            balanced_treated_mark,
            balanced_control_mark,
            balanced_icon,
        )
        balanced_group.move_to(compare_group)

        confounder_cross = Cross(confounder_box, stroke_color=QUESTION_COLOR, stroke_width=5.5)
        confounder_cross.scale(1.05)

        # Beat 1:
        self.play(FadeIn(bias_word, scale=0.9), run_time=0.8)
        self.play(FadeIn(avg_diff_group, shift=UP * 0.06), run_time=0.7)
        self.play(
            Transform(avg_diff_group, split_group),
            run_time=0.9,
        )
        wait_for_chunks([1, 2], spent=2.4)

        # Beat 2:
        self.play(FadeOut(bias_word, scale=0.95), FadeOut(avg_diff_group), run_time=0.3)
        self.play(
            FadeIn(treated_card, scale=0.96),
            FadeIn(control_card, scale=0.96),
            FadeIn(treated_group, shift=UP * 0.06),
            FadeIn(control_group, shift=UP * 0.06),
            run_time=0.95,
        )
        wait_for_chunks([3], spent=1.2)

        # Beat 3:
        self.play(FadeIn(inequality, shift=UP * 0.08), run_time=0.65)
        self.play(
            Indicate(treated_group[-1], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(control_group[-1], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        wait_for_chunks([4], spent=1.25)

        # Beat 4:
        self.play(
            FadeOut(treated_card),
            FadeOut(control_card),
            FadeOut(treated_group),
            FadeOut(control_group),
            FadeOut(inequality),
            FadeIn(observed_formula, shift=UP * 0.08),
            run_time=0.85,
        )
        self.play(Indicate(observed_formula[2], color=WHITE, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([5], spent=1.35)

        # Beat 5:
        self.play(TransformMatchingTex(observed_formula, decomp_summary), run_time=0.95)
        self.play(FadeIn(att_detail, shift=UP * 0.06), FadeIn(bias_detail, shift=UP * 0.06), run_time=0.5)
        wait_for_chunks([6], spent=0.95)
        self.play(FadeIn(att_focus), FadeIn(att_note, shift=UP * 0.06), run_time=0.45)
        self.play(Indicate(att_focus, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.5)
        self.wait(3.4)
        self.play(
            FadeOut(att_focus),
            FadeOut(att_note),
            FadeIn(bias_focus),
            FadeIn(bias_note, shift=UP * 0.06),
            run_time=0.45,
        )
        self.play(Indicate(bias_focus, color=QUESTION_COLOR, scale_factor=1.02), run_time=0.5)
        wait_for_chunks([7, 8], spent=5.3)

        # Beat 6:
        self.play(
            FadeOut(bias_focus),
            FadeOut(bias_note),
            FadeOut(decomp_summary),
            FadeOut(att_detail),
            FadeOut(bias_detail),
            run_time=0.75,
        )
        self.play(
            FadeIn(confounder_box, shift=DOWN * 0.08),
            FadeIn(confounder_label, shift=DOWN * 0.08),
            FadeIn(t_node, scale=0.92),
            FadeIn(y_node, scale=0.92),
            FadeIn(t_label, shift=UP * 0.06),
            FadeIn(y_label, shift=UP * 0.06),
            run_time=0.9,
        )
        self.play(Create(c_to_t), Create(c_to_y), GrowArrow(t_to_y), run_time=0.85)
        self.play(FadeIn(compare_group, shift=UP * 0.06), run_time=0.55)
        self.play(
            Indicate(confounder_box, color=QUESTION_COLOR, scale_factor=1.03),
            Indicate(compare_icon, color=WHITE, scale_factor=1.05),
            run_time=0.55,
        )
        self.wait(4.9)
        self.play(FadeIn(budget_chip, shift=UP * 0.05), run_time=0.35)
        self.play(FadeIn(location_chip, shift=UP * 0.05), run_time=0.35)
        self.play(FadeIn(teacher_chip, shift=UP * 0.05), run_time=0.45)
        wait_for_chunks([9, 10], spent=9.65)
        self.play(
            Create(confounder_cross),
            c_to_t.animate.set_stroke(opacity=0.22),
            c_to_y.animate.set_stroke(opacity=0.22),
            confounder_box.animate.set_stroke(opacity=0.32),
            confounder_label.animate.set_opacity(0.32),
            confounder_factors.animate.set_opacity(0.32),
            run_time=0.7,
        )
        self.wait(4.2)
        self.play(Transform(compare_group, balanced_group), run_time=0.8)
        self.play(Indicate(compare_group[5], color=ACCENT_COLOR, scale_factor=1.08), run_time=0.45)
        wait_for_chunks([11, 12], spent=6.95)
        self.wait(self.WAIT_TAIL)


class Scene08_WhenAssociationBecomesCausation(Scene):
    WAIT_TAIL = 0.3

    def construct(self):
        chunk_durations = load_scene_timing_durations("08_when_association_becomes_causation")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        # Beat 1:
        question = Text(
            "When does association become causation?",
            font_size=34,
            color=QUESTION_COLOR,
            weight=BOLD,
        )
        question.move_to(ORIGIN)

        # Beat 2:
        decomp_summary_recall = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
            r"+",
            r"Bias",
        ).scale(0.95)
        decomp_summary_recall[2].set_color(ACCENT_COLOR)
        decomp_summary_recall[4].set_color(QUESTION_COLOR)
        decomp_summary_recall.move_to(ORIGIN + UP * 0.7)

        att_recall_detail = MathTex(
            r"ATT = E[Y_1-Y_0\mid T=1]"
        ).scale(0.8).set_color(ACCENT_COLOR)
        bias_recall_detail = MathTex(
            r"Bias = E[Y_0\mid T=1]-E[Y_0\mid T=0]"
        ).scale(0.8).set_color(QUESTION_COLOR)
        att_recall_detail.next_to(decomp_summary_recall, DOWN, buff=0.42)
        bias_recall_detail.next_to(att_recall_detail, DOWN, buff=0.25)
        decomp_recall_group = VGroup(decomp_summary_recall, att_recall_detail, bias_recall_detail)

        # Beat 3:
        bias_zero = MathTex(r"\text{Bias} = 0", color=QUESTION_COLOR).scale(0.9)
        bias_zero.next_to(bias_recall_detail, DOWN, buff=0.45)

        # Beat 4:
        comparability_formula = MathTex(
            r"E[Y_0\mid T=1]",
            r"=",
            r"E[Y_0\mid T=0]",
        ).scale(1.1)
        comparability_formula[0].set_color(TABLET_COLOR)
        comparability_formula[1].set_color(WHITE)
        comparability_formula[2].set_color(LIBRARY_COLOR)
        comparability_formula.move_to(ORIGIN)

        # Beat 5:
        comparability_small = MathTex(
            r"E[Y_0\mid T=1] = E[Y_0\mid T=0]",
        ).scale(0.7).set_color(NEUTRAL_COLOR)
        comparability_small.to_edge(UP, buff=0.5)

        treated_card8 = RoundedRectangle(
            width=3.3, height=2.5, corner_radius=0.18,
            stroke_color=TABLET_COLOR, stroke_width=2.4,
        )
        control_card8 = RoundedRectangle(
            width=3.3, height=2.5, corner_radius=0.18,
            stroke_color=LIBRARY_COLOR, stroke_width=2.4,
        )
        treated_card8.move_to(LEFT * 2.5 + DOWN * 0.3)
        control_card8.move_to(RIGHT * 2.5 + DOWN * 0.3)

        treated_content8 = VGroup(
            MathTex(r"T=1").set_color(TABLET_COLOR).scale(0.78),
            Text("Tablet given", font_size=22, color=TABLET_COLOR, weight=BOLD),
            Text("Even without a tablet", font_size=19, color=WHITE),
            Text("similar scores", font_size=20, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.16).move_to(treated_card8)

        control_content8 = VGroup(
            MathTex(r"T=0").set_color(LIBRARY_COLOR).scale(0.78),
            Text("No tablet", font_size=22, color=LIBRARY_COLOR, weight=BOLD),
            Text("Control group", font_size=19, color=WHITE),
            Text("Average scores", font_size=20, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.16).move_to(control_card8)

        card_equal = MathTex(r"\approx").scale(1.3).set_color(ACCENT_COLOR)
        card_equal.move_to(ORIGIN + DOWN * 0.3)

        # Beat 6:
        comparable_badge = RoundedRectangle(
            width=5.0, height=0.9, corner_radius=0.22,
            stroke_color=ACCENT_COLOR, stroke_width=2.5,
            fill_color=ACCENT_COLOR, fill_opacity=0.1,
        )
        comparable_label = Text("Comparable", font_size=30, color=ACCENT_COLOR, weight=BOLD)
        comparable_badge.move_to(comparable_label)
        comparable_group = VGroup(comparable_badge, comparable_label)
        comparable_group.to_edge(DOWN, buff=0.65)

        # Beat 7:
        result_att = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
        ).scale(1.05)
        result_att[2].set_color(ACCENT_COLOR)
        result_att.move_to(ORIGIN + UP * 0.45)

        bias_zero_condition = MathTex(
            r"\because\;E[Y_0\mid T=1]=E[Y_0\mid T=0]"
        ).scale(0.75).set_color(NEUTRAL_COLOR)
        bias_zero_condition.next_to(result_att, DOWN, buff=0.5)

        # Beat 8:
        result_att_atc = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
            r"=",
            r"ATC",
        ).scale(1.0)
        result_att_atc[2].set_color(ACCENT_COLOR)
        result_att_atc[4].set_color(LIBRARY_COLOR)
        result_att_atc.move_to(ORIGIN + UP * 0.45)

        atc_condition = MathTex(
            r"\because\;E[Y_1-Y_0\mid T=1]=E[Y_1-Y_0\mid T=0]"
        ).scale(0.72).set_color(NEUTRAL_COLOR)
        atc_condition.next_to(result_att_atc, DOWN, buff=0.5)

        # Beat 9:
        result_full = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATT",
            r"=",
            r"ATC",
            r"=",
            r"ATE",
        ).scale(0.95)
        result_full[2].set_color(ACCENT_COLOR)
        result_full[4].set_color(LIBRARY_COLOR)
        result_full[6].set_color(YELLOW_E)
        result_full.move_to(ORIGIN + UP * 0.45)

        # Beat 10:
        summary_text = Text(
            "Comparability",
            font_size=46,
            color=ACCENT_COLOR,
            weight=BOLD,
        )
        summary_text.move_to(ORIGIN + UP * 0.5)
        arrow_down = Arrow(
            summary_text.get_bottom() + DOWN * 0.1,
            summary_text.get_bottom() + DOWN * 0.85,
            color=WHITE,
            stroke_width=2.5,
        )
        causation_text = Text(
            "Association = Causation",
            font_size=28,
            color=WHITE,
        )
        causation_text.next_to(arrow_down, DOWN, buff=0.22)

        # Beat 11:
        next_question = Text(
            "How can we create\ncomparable groups in practice?",
            font_size=32,
            color=QUESTION_COLOR,
            weight=BOLD,
            line_spacing=1.2,
        )
        next_question.move_to(ORIGIN)

        # ── Beat 1 ──
        self.play(FadeIn(question, scale=0.9), run_time=0.85)
        wait_for_chunks([1], spent=0.85)

        # ── Beat 2 ──
        self.play(FadeOut(question, scale=0.95), run_time=0.4)
        self.play(FadeIn(decomp_summary_recall, shift=UP * 0.07), run_time=0.75)
        self.play(
            FadeIn(att_recall_detail, shift=UP * 0.06),
            FadeIn(bias_recall_detail, shift=UP * 0.06),
            run_time=0.6,
        )
        self.play(Indicate(decomp_summary_recall[2], color=ACCENT_COLOR, scale_factor=1.04), run_time=0.5)
        self.play(Indicate(decomp_summary_recall[4], color=QUESTION_COLOR, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([2], spent=2.25)

        # ── Beat 3 ──
        self.play(
            Indicate(decomp_summary_recall[4], color=QUESTION_COLOR, scale_factor=1.15),
            Indicate(bias_recall_detail, color=QUESTION_COLOR, scale_factor=1.08),
            run_time=0.65,
        )
        self.play(FadeIn(bias_zero, shift=UP * 0.07), run_time=0.55)
        wait_for_chunks([3], spent=1.2)

        # ── Beat 4 ──
        self.play(
            FadeOut(decomp_recall_group),
            FadeOut(bias_zero),
            run_time=0.55,
        )
        self.play(FadeIn(comparability_formula, shift=UP * 0.07), run_time=0.75)
        self.play(Indicate(comparability_formula[0], color=TABLET_COLOR, scale_factor=1.04), run_time=0.5)
        self.play(Indicate(comparability_formula[2], color=LIBRARY_COLOR, scale_factor=1.04), run_time=0.5)
        wait_for_chunks([4], spent=2.3)

        # ── Beat 5 ──
        self.play(Transform(comparability_formula, comparability_small), run_time=0.6)
        self.play(
            FadeIn(treated_card8, scale=0.95),
            FadeIn(control_card8, scale=0.95),
            FadeIn(treated_content8, shift=UP * 0.07),
            FadeIn(control_content8, shift=UP * 0.07),
            run_time=0.9,
        )
        self.play(FadeIn(card_equal, scale=0.9), run_time=0.5)
        wait_for_chunks([5], spent=2.0)

        # ── Beat 6 ──
        self.play(FadeIn(comparable_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(comparable_badge, color=ACCENT_COLOR, scale_factor=1.03), run_time=0.55)
        wait_for_chunks([6], spent=1.15)

        # ── Beat 7 ──
        self.play(
            FadeOut(treated_card8),
            FadeOut(control_card8),
            FadeOut(treated_content8),
            FadeOut(control_content8),
            FadeOut(card_equal),
            FadeOut(comparable_group),
            FadeOut(comparability_formula),
            run_time=0.65,
        )
        self.play(FadeIn(result_att, shift=UP * 0.07), run_time=0.75)
        self.play(FadeIn(bias_zero_condition, shift=UP * 0.06), run_time=0.55)
        wait_for_chunks([7], spent=1.3)

        # ── Beat 8 ──
        self.play(
            TransformMatchingTex(result_att, result_att_atc),
            FadeOut(bias_zero_condition),
            run_time=0.85,
        )
        self.play(FadeIn(atc_condition, shift=UP * 0.06), run_time=0.55)
        self.play(
            Indicate(result_att_atc[2], color=ACCENT_COLOR, scale_factor=1.04),
            Indicate(result_att_atc[4], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        wait_for_chunks([8], spent=2.0)

        # ── Beat 9 ──
        self.play(
            TransformMatchingTex(result_att_atc, result_full),
            FadeOut(atc_condition),
            run_time=0.85,
        )
        self.play(Indicate(result_full[6], color=YELLOW_E, scale_factor=1.06), run_time=0.55)
        wait_for_chunks([9], spent=1.4)

        # ── Beat 10 ──
        self.play(FadeOut(result_full), run_time=0.55)
        self.play(FadeIn(summary_text, scale=0.9), run_time=0.7)
        self.play(GrowArrow(arrow_down), run_time=0.5)
        self.play(FadeIn(causation_text, shift=UP * 0.06), run_time=0.5)
        wait_for_chunks([10], spent=2.25)

        # ── Beat 11 ──
        self.play(
            FadeOut(summary_text),
            FadeOut(arrow_down),
            FadeOut(causation_text),
            run_time=0.55,
        )
        self.play(FadeIn(next_question, scale=0.9), run_time=0.8)
        wait_for_chunks([11], spent=0.8)
        self.wait(self.WAIT_TAIL)


class Scene09_RandomizedExperiment(Scene):
    WAIT_TAIL = 0.3

    def construct(self):
        chunk_durations = load_scene_timing_durations("09_randomized_experiment")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        # Beat 1:
        random_label = Text("Randomization", font_size=52, color=ACCENT_COLOR, weight=BOLD)
        random_label.move_to(ORIGIN)

        # Beat 2-3: scatter plot — Conditions(x) × Score(y)
        scatter_axes = Axes(
            x_range=[0, 10, 10],
            y_range=[0, 10, 10],
            x_length=5.2,
            y_length=3.6,
            axis_config={
                "include_tip": True, "tip_length": 0.18,
                "stroke_width": 1.8, "color": NEUTRAL_COLOR, "include_ticks": False,
            },
        )
        scatter_axes.move_to(LEFT * 0.8 + DOWN * 0.1)
        scatter_x_label = Text("Conditions", font_size=19, color=NEUTRAL_COLOR)
        scatter_x_label.next_to(scatter_axes.x_axis, DOWN, buff=0.22)
        scatter_y_label = VGroup(*[
            Text(ch, font_size=19, color=NEUTRAL_COLOR) for ch in "Score"
        ]).arrange(DOWN, buff=0.05)
        scatter_y_label.next_to(scatter_axes.y_axis, LEFT, buff=0.22)
        scatter_axes_group = VGroup(scatter_axes, scatter_x_label, scatter_y_label)

        biased_t1_coords = [
            (5.5, 5.5), (6.5, 7.0), (7.0, 6.0), (8.0, 8.0), (9.0, 7.5),
            (7.5, 8.5), (8.5, 6.5), (6.0, 8.0), (9.0, 9.0), (7.0, 7.5),
        ]
        biased_t0_coords = [
            (1.0, 2.0), (2.0, 1.0), (2.5, 3.0), (3.5, 2.5), (4.0, 1.5),
            (1.5, 3.5), (3.0, 4.0), (4.5, 3.5), (2.0, 4.5), (4.0, 4.5),
        ]
        random_t1_coords = [
            (1.0, 4.5), (2.0, 7.0), (3.5, 5.0), (5.0, 8.0), (6.5, 6.5),
            (8.0, 4.0), (9.0, 7.5), (4.0, 3.5), (7.0, 6.0), (2.5, 8.0),
        ]
        random_t0_coords = [
            (1.5, 3.0), (3.0, 6.5), (4.5, 2.5), (6.0, 5.5), (7.5, 3.5),
            (9.0, 6.0), (2.0, 4.0), (5.5, 2.0), (8.5, 4.5), (3.5, 7.0),
        ]

        dot_r = 0.11
        biased_t1_dots = VGroup(*[
            Dot(scatter_axes.coords_to_point(x, y), radius=dot_r, color=TABLET_COLOR, fill_opacity=0.9)
            for x, y in biased_t1_coords
        ])
        biased_t0_dots = VGroup(*[
            Dot(scatter_axes.coords_to_point(x, y), radius=dot_r, color=LIBRARY_COLOR, fill_opacity=0.9)
            for x, y in biased_t0_coords
        ])

        _x0 = scatter_axes.coords_to_point(0, 0)[0]
        _x1 = scatter_axes.coords_to_point(10, 0)[0]
        _my1 = scatter_axes.coords_to_point(0, 6.0)[1]
        _my0 = scatter_axes.coords_to_point(0, 4.45)[1]
        mean_line_t1 = DashedLine(
            [_x0, _my1, 0], [_x1, _my1, 0],
            color=TABLET_COLOR, stroke_width=2.2, dash_length=0.12,
        )
        mean_line_t0 = DashedLine(
            [_x0, _my0, 0], [_x1, _my0, 0],
            color=LIBRARY_COLOR, stroke_width=2.2, dash_length=0.12,
        )
        mean_label_t1 = MathTex(r"E[Y\mid T=1]").scale(0.6).set_color(TABLET_COLOR)
        mean_label_t0 = MathTex(r"E[Y\mid T=0]").scale(0.6).set_color(LIBRARY_COLOR)
        mean_label_t1.next_to(mean_line_t1, RIGHT, buff=0.18)
        mean_label_t0.next_to(mean_line_t0, RIGHT, buff=0.18)

        # Beat 4:
        indep_formula = MathTex(
            r"(Y_0,\,Y_1)",
            r"\perp",
            r"T",
        ).scale(1.5)
        indep_formula[0].set_color(ACCENT_COLOR)
        indep_formula[1].set_color(WHITE)
        indep_formula[2].set_color(TABLET_COLOR)
        indep_formula.move_to(ORIGIN)

        # Beat 5:
        indep_small = MathTex(
            r"(Y_0,\,Y_1)\perp T"
        ).scale(0.75).set_color(NEUTRAL_COLOR)
        indep_small.to_edge(UP, buff=0.5)

        cond_preview = Text("Both conditions are automatically satisfied", font_size=28, color=WHITE)
        cond_preview.move_to(ORIGIN)

        # Beat 6:
        cond1_formula = MathTex(
            r"E[Y_0\mid T=1]",
            r"=",
            r"E[Y_0\mid T=0]",
        ).scale(1.05)
        cond1_formula[0].set_color(TABLET_COLOR)
        cond1_formula[1].set_color(WHITE)
        cond1_formula[2].set_color(LIBRARY_COLOR)
        cond1_formula.move_to(ORIGIN + UP * 0.55)

        cond1_num = Text("① Condition", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
        cond1_num.next_to(cond1_formula, LEFT, buff=0.3)

        bias_zero_badge = RoundedRectangle(
            width=3.2, height=0.78, corner_radius=0.2,
            stroke_color=ACCENT_COLOR, stroke_width=2.2,
            fill_color=ACCENT_COLOR, fill_opacity=0.1,
        )
        bias_zero_label = MathTex(r"\text{Bias} = 0").scale(0.88).set_color(ACCENT_COLOR)
        bias_zero_badge.move_to(bias_zero_label)
        bias_zero_group = VGroup(bias_zero_badge, bias_zero_label)
        bias_zero_group.next_to(cond1_formula, DOWN, buff=0.55)

        # Beat 7:
        cond1_small = MathTex(
            r"E[Y_0\mid T=1]=E[Y_0\mid T=0]"
        ).scale(0.68).set_color(NEUTRAL_COLOR)
        cond1_small.to_edge(UP, buff=0.5)

        cond2_formula = MathTex(
            r"E[Y_1\mid T=1]",
            r"=",
            r"E[Y_1\mid T=0]",
        ).scale(1.05)
        cond2_formula[0].set_color(TABLET_COLOR)
        cond2_formula[1].set_color(WHITE)
        cond2_formula[2].set_color(LIBRARY_COLOR)
        cond2_formula.move_to(ORIGIN + UP * 0.55)

        cond2_num = Text("② Condition", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
        cond2_num.next_to(cond2_formula, LEFT, buff=0.3)

        att_atc_badge = RoundedRectangle(
            width=3.8, height=0.78, corner_radius=0.2,
            stroke_color=ACCENT_COLOR, stroke_width=2.2,
            fill_color=ACCENT_COLOR, fill_opacity=0.1,
        )
        att_atc_label = MathTex(r"ATT = ATC").scale(0.88).set_color(ACCENT_COLOR)
        att_atc_badge.move_to(att_atc_label)
        att_atc_group = VGroup(att_atc_badge, att_atc_label)
        att_atc_group.next_to(cond2_formula, DOWN, buff=0.55)

        # Beat 8:
        conclusion_formula = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATE",
        ).scale(1.05)
        conclusion_formula[2].set_color(YELLOW_E)
        conclusion_formula.move_to(ORIGIN)

        # Beat 9:
        rct_label = Text("RCT", font_size=64, color=ACCENT_COLOR, weight=BOLD)
        rct_label.move_to(ORIGIN + UP * 0.5)
        gold_badge = RoundedRectangle(
            width=5.6, height=0.9, corner_radius=0.22,
            stroke_color=YELLOW_E, stroke_width=2.2,
            fill_color=YELLOW_E, fill_opacity=0.08,
        )
        gold_label = Text("Gold standard for causal inference", font_size=26, color=YELLOW_E, weight=BOLD)
        gold_badge.move_to(gold_label)
        gold_group = VGroup(gold_badge, gold_label)
        gold_group.next_to(rct_label, DOWN, buff=0.55)

        # ── Beat 1 ──
        self.play(FadeIn(random_label, scale=0.85), run_time=0.75)
        wait_for_chunks([1], spent=0.75)

        # ── Beat 2 ──
        self.play(FadeOut(random_label, scale=0.95), run_time=0.35)
        self.play(FadeIn(scatter_axes_group), run_time=0.7)
        self.play(
            FadeIn(biased_t1_dots, lag_ratio=0.12),
            FadeIn(biased_t0_dots, lag_ratio=0.12),
            run_time=0.9,
        )
        self.wait(2.4)
        self.play(
            *[biased_t1_dots[i].animate.move_to(
                scatter_axes.coords_to_point(*random_t1_coords[i])
              ) for i in range(len(random_t1_coords))],
            *[biased_t0_dots[i].animate.move_to(
                scatter_axes.coords_to_point(*random_t0_coords[i])
              ) for i in range(len(random_t0_coords))],
            run_time=1.2,
        )
        wait_for_chunks([2], spent=5.55)

        # ── Beat 3 ──
        self.play(
            Create(mean_line_t1),
            Create(mean_line_t0),
            run_time=0.7,
        )
        self.play(
            FadeIn(mean_label_t1, shift=LEFT * 0.05),
            FadeIn(mean_label_t0, shift=LEFT * 0.05),
            run_time=0.55,
        )
        wait_for_chunks([3], spent=1.25)

        # ── Beat 4 ──
        self.play(
            FadeOut(scatter_axes_group),
            FadeOut(biased_t1_dots),
            FadeOut(biased_t0_dots),
            FadeOut(mean_line_t1),
            FadeOut(mean_line_t0),
            FadeOut(mean_label_t1),
            FadeOut(mean_label_t0),
            run_time=0.5,
        )
        self.play(FadeIn(indep_formula, scale=0.9), run_time=0.8)
        self.play(Indicate(indep_formula[1], color=WHITE, scale_factor=1.1), run_time=0.55)
        wait_for_chunks([4], spent=1.85)

        # ── Beat 5 ──
        self.play(Transform(indep_formula, indep_small), run_time=0.6)
        self.play(FadeIn(cond_preview, shift=UP * 0.07), run_time=0.6)
        wait_for_chunks([5], spent=1.2)

        # ── Beat 6 ──
        self.play(
            FadeOut(cond_preview),
            FadeOut(indep_formula),
            run_time=0.5,
        )
        self.play(
            FadeIn(cond1_num, shift=RIGHT * 0.05),
            FadeIn(cond1_formula, shift=UP * 0.07),
            run_time=0.75,
        )
        self.play(
            Indicate(cond1_formula[0], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(cond1_formula[2], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        self.wait(3.5)
        self.play(FadeIn(bias_zero_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(bias_zero_badge, color=ACCENT_COLOR, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([6], spent=6.45)

        # ── Beat 7 ──
        self.play(
            Transform(cond1_formula, cond1_small),
            FadeOut(cond1_num),
            FadeOut(bias_zero_group),
            run_time=0.6,
        )
        self.play(
            FadeIn(cond2_num, shift=RIGHT * 0.05),
            FadeIn(cond2_formula, shift=UP * 0.07),
            run_time=0.75,
        )
        self.play(
            Indicate(cond2_formula[0], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(cond2_formula[2], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        self.wait(2.5)
        self.play(FadeIn(att_atc_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(att_atc_badge, color=ACCENT_COLOR, scale_factor=1.03), run_time=0.5)
        wait_for_chunks([7], spent=5.55)

        # ── Beat 8 ──
        self.play(
            FadeOut(cond1_formula),
            FadeOut(cond2_num),
            FadeOut(cond2_formula),
            FadeOut(att_atc_group),
            run_time=0.55,
        )
        self.play(FadeIn(conclusion_formula, shift=UP * 0.07), run_time=0.75)
        self.play(Indicate(conclusion_formula[2], color=YELLOW_E, scale_factor=1.08), run_time=0.5)
        wait_for_chunks([8], spent=1.8)

        # ── Beat 9 ──
        self.play(FadeOut(conclusion_formula), run_time=0.5)
        self.play(FadeIn(rct_label, scale=0.85), run_time=0.75)
        self.play(FadeIn(gold_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(gold_badge, color=YELLOW_E, scale_factor=1.03), run_time=0.55)
        wait_for_chunks([9], spent=2.4)
        self.wait(self.WAIT_TAIL)


class Scene10_OnlineClassroomRCT(Scene):
    WAIT_TAIL = 0.3

    def construct(self):
        chunk_durations = load_scene_timing_durations("10_online_classroom_rct")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            total = sum(chunk_durations[i - 1] for i in indices) - spent + extra
            if total > 0:
                self.wait(total)

        FACE_COLOR = BLUE_D
        ONLINE_COLOR = MAROON_D
        BLEND_COLOR = GREEN_D

        icon_face = load_icon("school.svg", FACE_COLOR, 0.72)
        icon_online = load_icon("device-desktop.svg", ONLINE_COLOR, 0.72)
        icon_blend = load_icon("devices.svg", BLEND_COLOR, 0.72)

        # ── Beat 1 ──
        title = Text("Online Classroom Experiment", font_size=40, color=WHITE)
        title.move_to(UP * 2.0)

        t_header = Text("Treatment  T", font_size=22, color=NEUTRAL_COLOR)
        icon_f1 = load_icon("school.svg", FACE_COLOR, 0.5)
        icon_b1 = load_icon("devices.svg", BLEND_COLOR, 0.5)
        icon_o1 = load_icon("device-desktop.svg", ONLINE_COLOR, 0.5)
        lbl_f1 = Text("In-person", font_size=16, color=FACE_COLOR)
        lbl_b1 = Text("Hybrid", font_size=16, color=BLEND_COLOR)
        lbl_o1 = Text("Online", font_size=16, color=ONLINE_COLOR)
        col_f1 = VGroup(icon_f1, lbl_f1).arrange(DOWN, buff=0.1)
        col_b1 = VGroup(icon_b1, lbl_b1).arrange(DOWN, buff=0.1)
        col_o1 = VGroup(icon_o1, lbl_o1).arrange(DOWN, buff=0.1)
        t_icons = VGroup(col_f1, col_b1, col_o1).arrange(RIGHT, buff=0.35)
        t_section = VGroup(t_header, t_icons).arrange(DOWN, buff=0.28)
        t_section.move_to(LEFT * 2.8 + DOWN * 0.3)

        y_header = Text("Outcome  Y", font_size=22, color=NEUTRAL_COLOR)
        icon_y = load_icon("checklist.svg", ACCENT_COLOR, 0.55)
        lbl_y = Text("Final exam score", font_size=16, color=ACCENT_COLOR)
        y_col = VGroup(icon_y, lbl_y).arrange(DOWN, buff=0.1)
        y_section = VGroup(y_header, y_col).arrange(DOWN, buff=0.28)
        y_section.move_to(RIGHT * 2.5 + DOWN * 0.3)

        ty_arrow = Arrow(
            t_section.get_right() + RIGHT * 0.1,
            y_section.get_left() + LEFT * 0.1,
            buff=0.05, stroke_width=2.5, color=NEUTRAL_COLOR,
            max_tip_length_to_length_ratio=0.1,
        )

        ty_visual = VGroup(t_section, ty_arrow, y_section)

        self.play(FadeIn(title, shift=UP * 0.06), run_time=0.6)
        self.play(
            LaggedStart(
                FadeIn(t_section, shift=RIGHT * 0.05),
                GrowArrow(ty_arrow),
                FadeIn(y_section, shift=LEFT * 0.05),
                lag_ratio=0.3,
            ),
            run_time=1.1,
        )
        wait_for_chunks([1, 2], spent=1.7)

        # ── Beat 2 ──
        def make_format_card(icon, label, color):
            lbl = Text(label, font_size=24, color=color)
            grp = VGroup(icon, lbl).arrange(DOWN, buff=0.2)
            rect = SurroundingRectangle(
                grp, buff=0.25, color=color,
                stroke_opacity=0.7, fill_opacity=0.06, fill_color=color,
            )
            return VGroup(rect, grp)

        card_f = make_format_card(icon_face, "In-person", FACE_COLOR)
        card_b = make_format_card(icon_blend, "Hybrid", BLEND_COLOR)
        card_o = make_format_card(icon_online, "Online", ONLINE_COLOR)
        cards = VGroup(card_f, card_b, card_o).arrange(RIGHT, buff=0.55)
        cards.move_to(ORIGIN)

        rct_badge = Text("Randomization", font_size=22, color=ACCENT_COLOR)
        rct_badge.move_to(UP * 2.4)
        rct_arr = Arrow(
            rct_badge.get_bottom() + DOWN * 0.05,
            cards.get_top() + UP * 0.05,
            buff=0.1, stroke_width=2.0, color=ACCENT_COLOR,
            max_tip_length_to_length_ratio=0.12,
        )

        self.play(
            title.animate.scale(0.65).to_edge(UP, buff=0.25),
            FadeOut(ty_visual),
            run_time=0.55,
        )
        self.play(
            LaggedStart(
                FadeIn(card_f, shift=UP * 0.05),
                FadeIn(card_b, shift=UP * 0.05),
                FadeIn(card_o, shift=UP * 0.05),
                lag_ratio=0.2,
            ),
            run_time=1.0,
        )
        self.play(FadeIn(rct_badge), Create(rct_arr), run_time=0.8)

        self.wait(8.5)

        t_lbl = Text("Course format T", font_size=21, color=NEUTRAL_COLOR)
        icon_y2 = load_icon("checklist.svg", ACCENT_COLOR, 0.6)
        y_lbl2 = Text("Final exam score", font_size=18, color=ACCENT_COLOR)
        y_hdr2 = Text("Outcome  Y", font_size=21, color=NEUTRAL_COLOR)
        y_col2 = VGroup(icon_y2, y_lbl2).arrange(DOWN, buff=0.12)
        y_sec2 = VGroup(y_hdr2, y_col2).arrange(DOWN, buff=0.28)
        y_sec2.move_to(RIGHT * 3.0)

        ty_mid_arr = Arrow(
            LEFT * 0.6, RIGHT * 1.8,
            buff=0.0, stroke_width=2.5, color=NEUTRAL_COLOR,
            max_tip_length_to_length_ratio=0.1,
        )

        self.play(
            FadeOut(rct_badge), FadeOut(rct_arr),
            cards.animate.scale(0.72).move_to(LEFT * 3.0),
            run_time=0.65,
        )
        t_lbl.next_to(cards, UP, buff=0.18)
        self.play(FadeIn(t_lbl), run_time=0.4)
        self.play(GrowArrow(ty_mid_arr), FadeIn(y_sec2, shift=LEFT * 0.05), run_time=0.7)
        wait_for_chunks([3], spent=12.6)

        # ── Beat 3 ──
        self.play(
            FadeOut(cards), FadeOut(t_lbl), FadeOut(ty_mid_arr), FadeOut(y_sec2), FadeOut(title),
            run_time=0.5,
        )

        def dag_node(label, color, fsize=22):
            txt = Text(label, font_size=fsize, color=color)
            box = SurroundingRectangle(txt, buff=0.22, color=color, stroke_opacity=0.8,
                                       fill_color=color, fill_opacity=0.08)
            return VGroup(box, txt)

        node_bg = dag_node("Student background", QUESTION_COLOR)
        node_T  = dag_node("Course format T", ONLINE_COLOR)
        node_Y  = dag_node("Grade Y", ACCENT_COLOR)

        node_bg.move_to(UP * 1.5)
        node_T.move_to(LEFT * 3.0 + DOWN * 0.8)
        node_Y.move_to(RIGHT * 3.0 + DOWN * 0.8)

        def dag_arrow(src, dst, color, stroke=2.2):
            return Arrow(
                src.get_boundary_point(dst.get_center() - src.get_center()),
                dst.get_boundary_point(src.get_center() - dst.get_center()),
                buff=0.08, stroke_width=stroke, color=color,
                max_tip_length_to_length_ratio=0.12,
            )

        arr_bg_T = dag_arrow(node_bg, node_T, QUESTION_COLOR)
        arr_bg_Y = dag_arrow(node_bg, node_Y, QUESTION_COLOR)
        arr_T_Y  = dag_arrow(node_T,  node_Y, NEUTRAL_COLOR)

        conf_label = Text("Self-motivated? Low-income?", font_size=18, color=QUESTION_COLOR)
        conf_label.next_to(arr_bg_T, LEFT, buff=0.08)

        cross = Text("✕", font_size=38, color=ACCENT_COLOR)
        cross.move_to(arr_bg_T.get_center())
        rct_cut = Text("Randomization blocks this path", font_size=21, color=ACCENT_COLOR)
        rct_cut.move_to(DOWN * 2.5)

        bq = Text("What if there was no randomization?", font_size=28, color=ACCENT_COLOR)
        bq.move_to(UP * 3.0)

        self.play(FadeIn(bq), run_time=0.6)
        self.wait(2.0)
        self.play(
            LaggedStart(FadeIn(node_bg), FadeIn(node_T), FadeIn(node_Y), lag_ratio=0.25),
            run_time=0.9,
        )
        self.play(
            Create(arr_bg_T), Create(arr_bg_Y), Create(arr_T_Y),
            run_time=0.8,
        )
        self.play(FadeIn(conf_label, shift=RIGHT * 0.04), run_time=0.5)
        self.wait(4.0)
        self.play(Indicate(arr_bg_T, color=RED_D, scale_factor=1.1), run_time=0.7)
        self.wait(5.0)
        self.play(
            arr_bg_T.animate.set_opacity(0.25),
            conf_label.animate.set_opacity(0.25),
            run_time=0.5,
        )
        self.play(FadeIn(cross, scale=0.5), run_time=0.5)
        self.play(FadeIn(rct_cut, shift=UP * 0.05), run_time=0.6)
        wait_for_chunks([4], spent=16.6)

        # ── Beat 4 ──
        self.play(
            FadeOut(bq), FadeOut(node_bg), FadeOut(node_T), FadeOut(node_Y),
            FadeOut(arr_bg_T), FadeOut(arr_bg_Y), FadeOut(arr_T_Y),
            FadeOut(conf_label), FadeOut(cross), FadeOut(rct_cut),
            run_time=0.5,
        )

        col_xs = [-1.8, 1.4]
        row_ys = [1.6, 0.7, -0.1, -0.9]
        res_data = [
            ("Course format", "Mean score"),
            ("In-person",     "78.55"),
            ("Hybrid",        "77.09"),
            ("Online",        "73.64"),
        ]
        res_colors = [
            [NEUTRAL_COLOR, NEUTRAL_COLOR],
            [FACE_COLOR,    FACE_COLOR],
            [BLEND_COLOR,   BLEND_COLOR],
            [ONLINE_COLOR,  ONLINE_COLOR],
        ]
        res_fsizes = [22, 26, 26, 26]

        res_cells = []
        for r, (row_data, cols_color, fsize) in enumerate(zip(res_data, res_colors, res_fsizes)):
            for c, (val, color) in enumerate(zip(row_data, cols_color)):
                cell = Text(val, font_size=fsize, color=color)
                cell.move_to([col_xs[c], row_ys[r], 0])
                res_cells.append(cell)
        res_table = VGroup(*res_cells)

        divider = Line(
            [col_xs[0] - 0.6, row_ys[0] - 0.42, 0],
            [col_xs[1] + 0.8, row_ys[0] - 0.42, 0],
            stroke_width=1.5, color=NEUTRAL_COLOR, stroke_opacity=0.5,
        )

        ate_eq = MathTex(r"\widehat{ATE} = 78.55 - 73.64 \approx -4.91", font_size=30).set_color(WHITE)
        ate_eq.move_to(DOWN * 2.0)

        self.play(FadeIn(VGroup(*res_cells[:2])), Create(divider), run_time=0.7)
        self.play(
            LaggedStart(
                FadeIn(VGroup(*res_cells[2:4])),
                FadeIn(VGroup(*res_cells[4:6])),
                FadeIn(VGroup(*res_cells[6:8])),
                lag_ratio=0.35,
            ),
            run_time=0.9,
        )
        wait_for_chunks([5], spent=0.5 + 0.7 + 0.9)

        self.play(FadeIn(ate_eq, shift=UP * 0.05), run_time=0.7)
        self.play(Indicate(ate_eq, color=ACCENT_COLOR, scale_factor=1.06), run_time=0.6)
        wait_for_chunks([6], spent=1.3)

        self.play(Indicate(VGroup(*res_cells[2:4]), color=FACE_COLOR, scale_factor=1.06), run_time=0.5)
        self.play(Indicate(VGroup(*res_cells[6:8]), color=ONLINE_COLOR, scale_factor=1.06), run_time=0.5)
        wait_for_chunks([7], spent=1.0)

        # ── Beat 5 ──
        self.play(
            FadeOut(res_table), FadeOut(divider), FadeOut(ate_eq),
            run_time=0.5,
        )

        bal_title = Text("Randomization Balance Check", font_size=24, color=NEUTRAL_COLOR)
        bal_title.move_to(UP * 2.8)

        col_xs_b = [-3.1, -1.5, -0.6, 0.3, 1.2]
        row_ys_b = [2.0, 1.3, 0.6, -0.1, -0.8, -1.5]
        bal_data = [
            ("Variable",  "In-person", "Hybrid",  "Online", ""),
            ("Gender",    "0.63", "0.55", "0.54",  "✓"),
            ("Asian",     "0.20", "0.22", "0.23",  "✓"),
            ("Black",     "0.07", "0.10", "0.03",  "△"),
            ("Hispanic",  "0.01", "0.01", "0.03",  "✓"),
            ("White",     "0.72", "0.63", "0.70",  "✓"),
        ]

        bal_row_groups = []
        for r, row_data in enumerate(bal_data):
            row_cells = []
            for c, val in enumerate(row_data):
                if r == 0:
                    color, fsize = NEUTRAL_COLOR, 18
                elif c == 0:
                    color, fsize = NEUTRAL_COLOR, 19
                elif c == 4:
                    color, fsize = (YELLOW_E if val == "△" else TEAL_D), 19
                elif r == 3:
                    color, fsize = YELLOW_E, 19
                else:
                    color, fsize = WHITE, 19
                cell = Text(val, font_size=fsize, color=color)
                cell.move_to([col_xs_b[c], row_ys_b[r], 0])
                row_cells.append(cell)
            bal_row_groups.append(VGroup(*row_cells))

        bal_divider = Line(
            [col_xs_b[0] - 0.4, row_ys_b[0] - 0.42, 0],
            [col_xs_b[4] + 0.35, row_ys_b[0] - 0.42, 0],
            stroke_width=1.5, color=NEUTRAL_COLOR, stroke_opacity=0.5,
        )

        bal_note = Text(
            "Small samples can produce random imbalances",
            font_size=19, color=NEUTRAL_COLOR,
        )
        bal_note.move_to(DOWN * 2.1)

        self.play(FadeIn(bal_title), run_time=0.5)
        self.play(FadeIn(bal_row_groups[0]), Create(bal_divider), run_time=0.6)
        self.play(
            LaggedStart(*[FadeIn(bal_row_groups[i]) for i in range(1, 6)], lag_ratio=0.25),
            run_time=1.2,
        )
        self.play(Indicate(bal_row_groups[3], color=YELLOW_E, scale_factor=1.08), run_time=0.6)
        self.play(FadeIn(bal_note, shift=UP * 0.05), run_time=0.6)
        wait_for_chunks([8], spent=4.0)
        self.wait(self.WAIT_TAIL)


class Scene11_RctLimitsAndBeyond(Scene):
    WAIT_TAIL = 1.0

    def construct(self):
        chunk_durations = load_scene_timing_durations("11_rct_limits_and_beyond")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            total = sum(chunk_durations[i - 1] for i in indices) - spent + extra
            if total > 0:
                self.wait(total)

        COST_COLOR = GOLD_D
        ETHICS_COLOR = BLUE_D
        POLICY_COLOR = TEAL_D

        # ── Beat 1 ──
        divider = Line(
            UP * 3.8, DOWN * 3.8,
            stroke_width=1.5, color=NEUTRAL_COLOR, stroke_opacity=0.45,
        )

        rct_lbl = Text("RCT", font_size=60, color=GREEN_D, weight=BOLD)
        rct_check = Text("✓", font_size=52, color=GREEN_D)
        rct_sub = Text("Ideal design", font_size=20, color=GREEN_D)
        rct_left_grp = VGroup(rct_lbl, rct_check, rct_sub).arrange(DOWN, buff=0.22)
        rct_left_grp.move_to(LEFT * 3.2)

        real_lbl = Text("In practice", font_size=34, color=WHITE)
        real_cross = Text("✗", font_size=52, color=RED_D)
        real_sub = Text("not always possible", font_size=20, color=NEUTRAL_COLOR)
        rct_right_grp = VGroup(real_lbl, real_cross, real_sub).arrange(DOWN, buff=0.22)
        rct_right_grp.move_to(RIGHT * 3.2)

        self.play(Create(divider), run_time=0.5)
        self.play(
            FadeIn(rct_left_grp, shift=RIGHT * 0.12),
            FadeIn(rct_right_grp, shift=LEFT * 0.12),
            run_time=0.7,
        )
        wait_for_chunks([1], spent=1.2)

        # ── Beat 2 ──
        self.play(
            FadeOut(divider), FadeOut(rct_left_grp), FadeOut(rct_right_grp),
            run_time=0.5,
        )

        icons_meta = [
            ("coin.svg",          COST_COLOR,   "High cost",      "Billions for large-scale trials",   LEFT * 3.8),
            ("scale.svg",         ETHICS_COLOR, "Ethical limits", "Can't assign smoking or weapons",    ORIGIN),
            ("building-bank.svg", POLICY_COLOR, "Policy scale",   "National-level RCT infeasible",      RIGHT * 3.8),
        ]

        icon_cols_grp = VGroup()
        for icon_file, color, title, desc, pos in icons_meta:
            icon = load_icon(icon_file, color, 1.1)
            title_txt = Text(title, font_size=21, color=color, weight=BOLD)
            desc_txt = Text(desc, font_size=17, color=NEUTRAL_COLOR)
            col = VGroup(icon, VGroup(title_txt, desc_txt).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.28)
            col.move_to(pos + UP * 0.4)
            icon_cols_grp.add(col)

        for col in icon_cols_grp:
            self.play(FadeIn(col, scale=0.82), run_time=0.8)
            self.wait(0.3)

        no_smoking = load_icon("smoking-no.svg", RED_D, 0.65)
        smoke_txt = Text("Can't randomize smoking in pregnant women", font_size=19, color=NEUTRAL_COLOR)
        smoking_row = VGroup(no_smoking, smoke_txt).arrange(RIGHT, buff=0.3)
        smoking_box_rect = SurroundingRectangle(
            smoking_row, buff=0.24, color=NEUTRAL_COLOR,
            stroke_width=1.2, corner_radius=0.1, stroke_opacity=0.45,
        )
        smoking_panel = VGroup(smoking_box_rect, smoking_row)
        smoking_panel.move_to(DOWN * 2.3)

        self.wait(3.5)
        self.play(FadeIn(smoking_panel, shift=UP * 0.06), run_time=0.6)
        wait_for_chunks([2], spent=7.9)

        # ── Beat 3 ──
        self.play(FadeOut(icon_cols_grp), FadeOut(smoking_panel), run_time=0.5)

        question_txt = Text(
            '"If we could run the ideal experiment, how would we design it?"',
            font_size=20, color=ACCENT_COLOR,
        )
        question_box = SurroundingRectangle(
            question_txt, buff=0.3, color=ACCENT_COLOR,
            corner_radius=0.12, stroke_width=1.8,
        )
        question_grp = VGroup(question_box, question_txt)
        question_grp.move_to(UP * 0.6)

        anchor_txt = Text("Benchmark for observational research", font_size=22, color=WHITE)
        anchor_txt.next_to(question_grp, DOWN, buff=0.55)
        anchor_arr = Arrow(
            question_grp.get_bottom() + DOWN * 0.08,
            anchor_txt.get_top() + UP * 0.08,
            stroke_width=2.5, color=NEUTRAL_COLOR, buff=0,
            max_tip_length_to_length_ratio=0.3,
        )

        self.play(FadeIn(question_grp, shift=UP * 0.08), run_time=0.7)
        self.play(GrowArrow(anchor_arr), FadeIn(anchor_txt, shift=UP * 0.05), run_time=0.6)
        wait_for_chunks([3], spent=1.8)

        # ── Beat 4 ──
        self.play(
            FadeOut(question_grp), FadeOut(anchor_arr), FadeOut(anchor_txt),
            run_time=0.5,
        )

        quasi_title = Text("Quasi-experimental methods", font_size=28, color=WHITE, weight=BOLD)
        quasi_title.move_to(UP * 3.0)

        def q_node(label, color, fsize=20):
            txt = Text(label, font_size=fsize, color=color)
            box = SurroundingRectangle(
                txt, buff=0.22, color=color, corner_radius=0.1, stroke_width=1.8,
            )
            return VGroup(box, txt)

        def q_arrow(src, dst, color, stroke=2.2):
            dir_vec = dst.get_center() - src.get_center()
            return Arrow(
                src.get_boundary_point(dir_vec),
                dst.get_boundary_point(-dir_vec),
                buff=0.1, stroke_width=stroke, color=color,
                max_tip_length_to_length_ratio=0.25,
            )

        node_T = q_node("Treatment T", GOLD_D)
        node_Y = q_node("Outcome Y", TEAL_D)
        node_T.move_to(LEFT * 2.6 + UP * 0.2)
        node_Y.move_to(RIGHT * 2.6 + UP * 0.2)

        ty_y = node_T.get_center()[1]
        arr_T_Y = Arrow(
            [node_T.get_right()[0], ty_y, 0],
            [node_Y.get_left()[0], ty_y, 0],
            buff=0, stroke_width=3.0, color=ACCENT_COLOR,
            max_tip_length_to_length_ratio=0.25,
        )
        goal_lbl = Text("Causal effect of interest", font_size=17, color=NEUTRAL_COLOR)
        goal_lbl.next_to(arr_T_Y, DOWN, buff=0.2)

        self.play(FadeIn(quasi_title), run_time=0.4)
        self.play(FadeIn(node_T), FadeIn(node_Y), run_time=0.6)
        self.play(Create(arr_T_Y), FadeIn(goal_lbl), run_time=0.6)
        self.wait(3.0)

        node_X = q_node("Confounder X", QUESTION_COLOR, fsize=18)
        node_X.move_to(UP * 2.0)
        arr_X_T = q_arrow(node_X, node_T, QUESTION_COLOR)
        arr_X_Y = q_arrow(node_X, node_Y, QUESTION_COLOR)
        problem_lbl = Text("Confounder affects both treatment and outcome", font_size=18, color=QUESTION_COLOR)
        problem_lbl.move_to(DOWN * 1.5)

        self.play(FadeIn(node_X, shift=DOWN * 0.1), run_time=0.5)
        self.play(
            LaggedStart(Create(arr_X_T), Create(arr_X_Y), lag_ratio=0.4),
            run_time=0.7,
        )
        self.play(FadeIn(problem_lbl, shift=UP * 0.05), run_time=0.5)
        self.wait(3.5)

        midpt = (node_X.get_center() + node_T.get_center()) / 2
        ctrl_lbl = Text("Control", font_size=17, color=NEUTRAL_COLOR)
        ctrl_lbl.move_to(midpt + RIGHT * 0.5)
        solution_lbl = Text("Make treatment look as good as random", font_size=20, color=ACCENT_COLOR)
        solution_lbl.move_to(DOWN * 1.5)

        self.play(
            arr_X_T.animate.set_stroke(color=NEUTRAL_COLOR, opacity=0.25),
            arr_X_Y.animate.set_stroke(color=NEUTRAL_COLOR, opacity=0.25),
            FadeOut(problem_lbl),
            run_time=0.7,
        )
        self.play(FadeIn(ctrl_lbl), run_time=0.4)
        self.play(FadeIn(solution_lbl, shift=UP * 0.05), run_time=0.5)
        wait_for_chunks([4], spent=11.9)

        # ── Beat 5 ──
        beat4_all = VGroup(
            quasi_title, node_T, node_Y, arr_T_Y, goal_lbl,
            node_X, arr_X_T, arr_X_Y, ctrl_lbl, solution_lbl,
        )
        self.play(FadeOut(beat4_all), run_time=0.5)

        method_header = Text("Methods ahead", font_size=22, color=NEUTRAL_COLOR)
        method_header.move_to(UP * 2.2)

        method_names = ["Matching", "Diff-in-Diff", "Synthetic Control", "IV", "RDD"]
        method_colors = [BLUE_D, GREEN_D, GOLD_D, MAROON_D, TEAL_D]

        def make_method_card(name, color):
            txt = Text(name, font_size=14, color=color)
            box = RoundedRectangle(
                width=2.4, height=0.9, corner_radius=0.12,
                color=color, stroke_width=1.8,
            )
            box.set_fill(color=color, opacity=0.08)
            txt.move_to(box.get_center())
            return VGroup(box, txt)

        cards = VGroup(*[make_method_card(n, c) for n, c in zip(method_names, method_colors)])
        grid_pos = [(-3.3, 0.0), (0.0, 0.0), (3.3, 0.0), (-1.65, -1.1), (1.65, -1.1)]
        for card, (x, y) in zip(cards, grid_pos):
            card.move_to([x, y, 0])

        self.play(FadeIn(method_header), run_time=0.4)
        self.play(
            LaggedStart(*[FadeIn(cards[i], shift=UP * 0.08) for i in range(3)], lag_ratio=0.25),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[FadeIn(cards[i], shift=UP * 0.08) for i in range(3, 5)], lag_ratio=0.3),
            run_time=0.7,
        )
        wait_for_chunks([5], spent=2.6)

        # ── Beat 6 ──
        self.play(
            cards.animate.set_opacity(0.2),
            method_header.animate.set_opacity(0.2),
            run_time=0.6,
        )

        goal_line1 = Text("Different tools, one goal.", font_size=28, color=WHITE, weight=BOLD)
        goal_line2 = Text(
            "Making groups comparable.",
            font_size=21, color=ACCENT_COLOR,
        )
        goal_grp = VGroup(goal_line1, goal_line2).arrange(DOWN, buff=0.3)
        goal_grp.move_to(UP * 1.4)

        self.play(FadeIn(goal_grp, shift=UP * 0.06), run_time=0.6)
        wait_for_chunks([6], spent=1.2)

        self.wait(1.5)
        self.play(
            FadeOut(VGroup(cards, method_header, goal_grp)),
            run_time=2.5,
        )
        self.wait(self.WAIT_TAIL)
