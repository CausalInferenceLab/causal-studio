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
    icon.set_stroke(color=color, width=2 .6, opacity=1)
    icon.set_fill(opacity=0)
    icon.height = height
    return icon


def load_scene_timing_durations(scene_basename: str) -> list[float]:
    timings_path = TOPIC_DIR / "build" / "audio" / f"{scene_basename}.timings.json"
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


def make_badge(icon: Mobject) -> VGroup:
    return VGroup(icon.copy())


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


class Scene02_AssociationIsNotCausation(Scene):
    """
    Scene 02: Association Is Not Causation

    Core Claim:
    태블릿이 있는 학교의 성적이 높아 보여도,
    그 차이를 태블릿 효과라고 바로 해석할 수는 없다.

    Expected Misconception:
    태블릿이 있는 학교의 평균 성적이 더 높으면,
    태블릿이 성취도를 높였다고 곧바로 결론 내리기 쉽다.

    Visual Pivot:
    태블릿 학교와 높은 성적의 연결선이 먼저 나타난 뒤,
    재정, 보충수업, 교사 확보 같은 다른 요인이 끼어들면서
    마지막에는 '연관관계'만 남는다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - Section 1 opening:
      태블릿 학교의 높은 성적은 인과가 아니라 연관일 수 있다는 직관 설명

    Script Reference:
    src/scripts/02_association_is_not_causation.txt

    Asset Reference:
    Tabler Icons (MIT)
    - device-tablet.svg
    - school.svg
    - coin.svg
    - users-group.svg
    - school-bell.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py - IntroQuestion
    3b1b/videos/_2024/transformers/ml_basics.py
    Reason:
    앞쪽은 단순한 질문 구조를,
    뒤쪽은 짧은 라벨 여러 개를 깔끔하게 비교하는 배치를 참고했다.

    Script-to-Beat Mapping:
    1. 태블릿 학교와 높은 성적이 같이 보이는 장면
    2. 재정, 보충수업, 교사 확보가 이미 달랐을 수 있다는 점 제시
    3. 태블릿만으로 결론 내릴 수 없고, 남는 것은 연관관계라는 점 정리
    """

    WAIT_TAIL = 8.8

    def construct(self):
        # Beat 1 준비:
        # 태블릿과 높은 성적의 동시 관찰을 먼저 보여준다.
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
        left_label = Text("태블릿 지급", font_size=24, color=TABLET_COLOR, weight=BOLD)
        left_label.next_to(left_icon, DOWN, buff=0.26)
        right_label = Text("높은 성적", font_size=24, color=ACCENT_COLOR, weight=BOLD)
        right_label.next_to(right_icon, DOWN, buff=0.26)

        # Beat 2 준비:
        # 태블릿 외에도 학교를 다르게 만드는 기존 여건이
        # 처치와 결과에 동시에 영향을 준다는 구조를 위쪽에서 내려오게 만든다.
        confounder_chips = VGroup(
            VGroup(load_icon("coin.svg", GOLD_E, 0.55), Text("재정", font_size=19, color=GOLD_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
            VGroup(load_icon("school-bell.svg", BLUE_E, 0.55), Text("보충수업", font_size=19, color=BLUE_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
            VGroup(load_icon("users-group.svg", GREEN_E, 0.62), Text("교사 확보", font_size=19, color=GREEN_E, weight=BOLD)).arrange(RIGHT, buff=0.12),
        ).arrange(RIGHT, buff=0.38)
        confounder_title = Text("학교 여건", font_size=24, color=WHITE, weight=BOLD)
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

        # Beat 3 준비:
        # 마지막에는 인과 화살표를 지우고, 연관관계만 남긴다.
        assoc = VGroup(
            Text("상관관계", font_size=34, color=WHITE, weight=BOLD),
            MathTex(r"\ne").scale(1.15).set_color(QUESTION_COLOR),
            Text("인과관계", font_size=34, color=QUESTION_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.28)
        assoc.move_to(UP * 1.85)
        foot = Text("태블릿 효과라고 바로 말할 수는 없다", font_size=24, color=NEUTRAL_COLOR)
        foot.next_to(assoc, DOWN, buff=0.34)

        # Beat 1:
        # "태블릿이 있는 학교의 성적이 높다"는 관찰 자체를 보여준다.
        self.play(FadeIn(left_icon, scale=0.9), FadeIn(right_icon, scale=0.9), run_time=0.9)
        self.play(
            GrowArrow(relation_arrow),
            FadeIn(left_label, shift=UP * 0.08),
            FadeIn(right_label, shift=UP * 0.08),
            run_time=0.9,
        )
        self.wait(4.6)

        # Beat 2:
        # 태블릿 말고도 학교를 다르게 만드는 요인이 이미 있었고,
        # 그 요인들이 처치와 결과에 동시에 영향을 준다는 점을 보여준다.
        self.play(FadeIn(confounder_group, shift=DOWN * 0.12), run_time=0.9)
        self.play(Create(backdoor_left), Create(backdoor_right), run_time=0.9)
        self.wait(12.8)  # chunk2 종료(20.99s)까지 Beat2가 1.8s 부족 → 12.8s로 늘려 싱크+끊김 보정

        # Beat 3:
        # 태블릿만으로는 결론을 낼 수 없고, 남는 것은 연관관계뿐이라는 점으로 정리한다.
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
        self.wait(self.WAIT_TAIL)


class Scene03_CounterfactualWorlds(Scene):
    """
    Scene 03: Counterfactual Worlds

    Core Claim:
    인과추론은 먼저 T_i와 Y_i를 정의하고,
    같은 대상의 잠재적 결과 Y_{1i}, Y_{0i}를 상정한 뒤,
    현실에서는 둘을 동시에 관찰할 수 없다는 문제를 마주한다.

    Expected Misconception:
    처치 여부와 결과 변수를 정의하면 인과효과도 곧바로 관찰할 수 있을 것처럼 보인다.

    Visual Pivot:
    T_i와 Y_i 표기에서 시작해 한 학생이 두 세계로 갈라지고,
    마지막에는 한쪽만 남아 사실 / 반사실 구조로 수렴한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - Section 1: 반사실과 잠재적 결과
    - T_i, Y_i 정의
    - Y_1, Y_0 도입과 반사실 관찰 불가능성

    Script Reference:
    src/scripts/03_counterfactual_worlds.txt

    Asset Reference:
    Tabler Icons (MIT)
    - user.svg
    - device-tablet.svg
    - book-off.svg
    - school.svg
    - eye-off.svg
    - arrows-split-2.svg
    - circle-x.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py - IntroQuestion
    3b1b/videos/_2018/uncertainty.py
    Reason:
    전자는 질문을 단계적으로 분해하는 인트로 리듬을,
    후자는 동시에 볼 수 없는 두 가능 상태를 대비시키는 분위기를 참고했다.

    Script-to-Beat Mapping:
    1. T_i와 Y_i를 먼저 정의
    2. 두 가능한 세계 Y_{1i}, Y_{0i}를 바로 제시
    3. 둘 중 하나만 현실에 존재한다는 근본 문제 제시
    4. 사실 / 반사실 대비로 마무리
    """

    WAIT_TAIL = 10.0

    def construct(self):
        # Beat 1 준비:
        # 첫 화면은 표기법만 좁게 보여준다.
        # 먼저 T_i를 소개하고, 그 다음에 T_i = 1 / 0 두 갈래로 분기시킨다.
        treatment_seed = MathTex(r"T_i").scale(1.45).set_color(TABLET_COLOR)
        treatment_seed.move_to(LEFT * 2.35 + UP * 0.45)
        treatment_word = Text("처치", font_size=24, color=WHITE, weight=BOLD)
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

        # Beat 1 -> Beat 2 연결:
        # 처치 표기법이 정리된 뒤에만 Y_i를 보여준다.
        # 처치와 결과 변수를 같은 화면에서 한꺼번에 설명하지 않기 위한 분리다.
        outcome_def = VGroup(
            MathTex(r"Y_i").scale(1.2).set_color(ACCENT_COLOR),
            Text("학업 성취도", font_size=26, color=ACCENT_COLOR, weight=BOLD),
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

        impossible = Text("둘 다 관찰할 수는 없다", font_size=25, color=QUESTION_COLOR, weight=BOLD)
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

        # Beat 3 목표 상태:
        # 먼저 두 세계를 좌우에 정리한 뒤, 반사실 세계 위에 반투명 가림막을 올린다.
        # 원래 색을 유지하면서 "관찰 불가"만 읽히게 하기 위한 처리다.
        factual_world_pos = LEFT * 3.0 + DOWN * 0.08
        counter_world_pos = RIGHT * 3.0 + DOWN * 0.08

        # Intro:
        # 첫 문장 "이제 직관을 넘어서..."는 빈 화면으로 받는다.
        # 표기법을 정리하겠다는 선언이므로, 시각 정보 없이 호흡만 확보한다.
        self.wait(6.2)

        # Beat 1:
        # 스크립트의 "먼저 T_i는 처치 여부를 뜻한다"를 처리한다.
        # 이어서 T_i = 1, T_i = 0 두 상태를 분기시켜 처치 개념을 시각적으로 고정한다.
        self.play(FadeIn(treatment_seed, scale=0.9), FadeIn(treatment_word, shift=UP * 0.08), run_time=1.0)
        self.wait(2.6)
        self.play(Create(up_arrow), Create(down_arrow), run_time=1.1)
        self.play(FadeIn(treatment_yes, shift=LEFT * 0.08), FadeIn(treatment_no, shift=LEFT * 0.08), run_time=1.0)
        self.wait(7.6)
        # 같은 화면에 정보를 더 쌓지 않고, 이제 결과 변수 Y_i로 전환한다.
        self.play(
            FadeOut(treatment_group, shift=LEFT * 0.08),
            FadeIn(outcome_def, shift=UP * 0.12),
            FadeIn(outcome_icon, scale=0.9),
            run_time=1.0,
        )
        self.wait(9.2)

        # Beat 2:
        # 스크립트의 "근본적인 문제"와 "잠재적 결과 도입"을 한 흐름으로 처리한다.
        # 두 세계를 충분히 오래 유지해, 문제 제기와 Y_{1i}/Y_{0i} 설명을 모두 받는다.
        self.play(
            FadeOut(VGroup(outcome_def, outcome_icon), shift=UP * 0.1),
            FadeIn(worlds, shift=UP * 0.12),
            run_time=1.1,
        )
        self.wait(24.8)

        # Beat 3:
        # 스크립트의 "실제로 관찰할 수 있는 것은 둘 중 하나뿐"을 처리한다.
        # factual / counterfactual 대비와 더 정리된 하단 문구로 관찰 불가능성을 정리한다.
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
        self.wait(self.WAIT_TAIL)


class Scene04_MultiverseIteAteAtt(Scene):
    """
    Scene 04: ITE, ATE, ATT 정의

    Core Claim:
    반사실 개념 위에서 ITE를 정의할 수 있고,
    현실에서는 ITE를 직접 계산할 수 없기 때문에 ATE와 ATT 같은 평균 효과를 본다.

    Expected Misconception:
    ITE, ATE, ATT 표기가 한꺼번에 나오면
    모두 다른 개념처럼 보이지만, 사실은 같은 차이를 어디에 대해 평균내느냐의 차이다.

    Visual Pivot:
    먼저 같은 학교의 두 결과 차이로 ITE를 보여준 뒤,
    ITE는 직접 계산하기 어렵다는 제약을 강조하고,
    마지막에 ATE와 ATT를 평균 효과 두 줄로 정리한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "실제로 일어난 쪽은 factual이고, 일어나지 않은 다른 한쪽은 counterfactual로 남습니다."
    - 현재 Scene 첫 문장:
      "이 개념을 바탕으로 개별 처치 효과, 즉 ITE를 정의할 수 있습니다."
    - Cell 6 tail:
      ITE 정의 ~ ATE 정의 ~ ATT 정의

    Script Reference:
    src/scripts/04_multiverse_ite_ate_att.txt

    Asset Reference:
    none

    3Blue1Brown Reference:
    3b1b/videos/_2024/transformers/ml_basics.py
    Reason:
    짧은 수식 정의를 먼저 놓고, 그 다음 핵심 제약과 평균 효과를 단계적으로 정리하는 리듬이 유사하다.

    Script-to-Beat Mapping:
    1. ITE를 같은 학교의 두 잠재적 결과 차이로 정의
    2. 반사실을 관찰할 수 없어서 ITE를 직접 계산할 수 없다고 정리
    3. ATE와 ATT를 평균 효과로 정리
    """

    WAIT_TAIL = 8.2

    def construct(self):
        # Beat 1 준비:
        # 직전 Scene에서 factual / counterfactual 두 결과를 동시에 볼 수 없다는 점을 다뤘다.
        # 여기서는 바로 그 두 결과 차이가 ITE라는 것을 같은 학교 한 곳의 두 작은 상태 카드로 압축해 보여준다.
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
        # Beat 2 준비:
        # ITE는 직관적으로 명확하지만 반사실을 관찰할 수 없어서 직접 계산할 수 없다는 제약을 보여준다.
        # 새 박스를 더하지 않고 기존 두 카드만 남긴 채, 오른쪽 카드만 가려서 반사실의 비관측성을 표현한다.
        # Beat 3 준비:
        # ITE의 차이를 전체 평균과 처치집단 평균으로 확장해 ATE, ATT를 정의한다.
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

        avg_hint = Text("전체 집단", font_size=25, color=NEUTRAL_COLOR, weight=BOLD)
        avg_hint.next_to(ate_expand, DOWN, buff=0.28)
        att_hint = Text("처치받은 집단만", font_size=25, color=NEUTRAL_COLOR, weight=BOLD)
        att_hint.move_to(avg_hint)

        # Beat 1:
        # 스크립트의 "ITE를 정의할 수 있다"와 "Y_1 - Y_0" 설명을 처리한다.
        # 상단에는 정의 하나, 가운데에는 두 상태 카드만 둬 겹침 없이 '차이' 자체를 먼저 고정한다.
        self.play(FadeIn(ite_title, shift=UP * 0.08), run_time=0.8)
        self.play(
            FadeIn(left_world, shift=RIGHT * 0.18),
            FadeIn(right_world, shift=LEFT * 0.18),
            run_time=1.0,
        )
        self.play(GrowArrow(ite_arrow), run_time=0.7)
        self.wait(11.0)

        # Beat 2:
        # 스크립트의 "반사실을 관찰할 수 없으므로 ITE는 직접 계산할 수 없다"를 처리한다.
        # 두 카드 자체는 유지하고, 오른쪽 카드만 가려 새 요소 난립 없이 비관측성을 표현한다.
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
        self.wait(4.8)

        # Beat 3:
        # 스크립트의 "현실적인 대안으로 ATE", "처치받은 사람들에게 한정한 ATT"를 처리한다.
        # 직접 계산 불가라는 제약을 평균 효과로 넘기되, '누구에 대한 평균인가'가 바뀌는 점을 순차적으로 보여준다.
        self.play(
            FadeOut(VGroup(left_world, right_world, veil, eye_off), shift=DOWN * 0.1),
            FadeOut(ite_title, shift=UP * 0.08),
            run_time=0.9,
        )
        self.play(FadeIn(ate_def, shift=UP * 0.08), run_time=0.7)
        self.play(FadeIn(ate_expand, shift=UP * 0.08), run_time=0.6)
        self.play(FadeIn(avg_hint, shift=UP * 0.08), run_time=0.6)
        self.wait(8.4)
        self.play(
            TransformMatchingTex(ate_def, att_def),
            FadeTransform(ate_expand, att_expand),
            FadeTransform(avg_hint, att_hint),
            run_time=0.9,
        )
        self.wait(self.WAIT_TAIL)


class Scene05_MultiverseTableAteAtt(Scene):
    """
    Scene 05: 멀티버스 표에서 ATE와 ATT 계산

    Core Claim:
    반사실까지 모두 볼 수 있는 가상의 멀티버스에서는
    각 학교의 ITE를 직접 계산할 수 있고, 그 위에서 ATE와 ATT도 바로 계산된다.

    Expected Misconception:
    ATE와 ATT 식이 추상적으로 보이지만,
    반사실 데이터가 있다면 결국 각 학교의 차이를 평균내는 단순한 계산이다.

    Visual Pivot:
    멀티버스에서 한 학교의 Y_0, Y_1을 동시에 보는 장면으로 시작해,
    네 학교 표로 확장한 뒤 ITE 열의 평균이 ATE와 ATT로 이어지는 구조로 수렴한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "또 전체 집단이 아닌, 실제로 처치를 받은 사람들에게 처치가 얼마나 효과적이었는지를 보는 지표인 ATT를 활용할 수 있습니다."
    - 현재 Scene 첫 문장:
      "이해를 돕기 위해, 멀티버스를 넘나들며 반사실을 볼 수 있다고 가정해 볼게요."
    - Cell 7 ~ Cell 9:
      멀티버스 가정, 4개 학교 데이터 표, ITE 평균으로서의 ATE와 ATT 계산

    Script Reference:
    src/scripts/05_multiverse_table_ate_att.txt

    Asset Reference:
    Tabler Icons (MIT)
    - school.svg
    - device-tablet.svg
    - device-tablet-off.svg
    - world-question.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py
    Reason:
    하나의 가정 실험을 먼저 시각적으로 세운 뒤, 그 가정 위에서 표와 수식을 단계적으로 꺼내는 전개 리듬이 유사하다.

    Script-to-Beat Mapping:
    1. 멀티버스라면 한 학교의 Y_1과 Y_0를 동시에 볼 수 있다고 도입
    2. 네 학교 데이터 표로 확장하고 ITE를 직접 계산 가능하다고 제시
    3. ITE 평균으로 ATE를 계산
    4. T = 1인 학교만 골라 ATT를 계산
    5. 계산이 가능했던 이유가 factual과 counterfactual을 모두 봤기 때문이라고 정리
    """

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

        # Beat 1 준비:
        # 첫 문장의 "멀티버스를 넘나든다"는 가정을 길게 설명하지 않고,
        # 한 학교에서 Y_0와 Y_1을 동시에 보는 그림으로 바로 압축한다.
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

        # Beat 3, 4 준비:
        # 수식은 표 아래에 한 번에 하나만 둬서 표와 계산이 서로 경쟁하지 않게 한다.
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
        # 멀티버스 가정과 "한 학교의 Y_0, Y_1을 동시에 볼 수 있다"는 핵심만 먼저 보여준다.
        self.play(Create(portal_ring), FadeIn(portal, scale=0.9), FadeIn(portal_label, shift=UP * 0.08), run_time=0.9)
        self.play(FadeIn(school, scale=0.9), FadeIn(school_tag, shift=UP * 0.08), run_time=0.8)
        self.play(Create(left_arrow), Create(right_arrow), FadeIn(left_outcome), FadeIn(right_outcome), run_time=1.0)
        wait_for_chunks([1], spent=2.7)

        # Beat 2:
        # 한 학교 그림을 네 학교 데이터 표로 바꾼다.
        # 여기서 Y_0, Y_1, T, Y, ITE가 모두 실제 숫자로 채워져 있음을 보여준다.
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
                    Indicate(VGroup(r ow[1][0], row[2][0]), color=ACCENT_COLOR, scale_factor=1.02)
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
        # ITE 열을 따로 늘어놓지 않고, 표 전체를 가볍게 물들여
        # "전체 집단 평균"이라는 점만 먼저 읽히게 한다.
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
        # 이제 처치를 받은 학교만 골라 ATT를 계산한다.
        # 비처치 행은 어둡게 밀어내고 T=1 두 행과 T열 셀을 직접 채워서
        # "누구에 대한 평균인가"가 한눈에 보이게 만든다.
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
        # 계산이 가능했던 이유는 각 행에서 factual/counterfactual을 모두 알고 있었기 때문이라는 점으로 정리한다.
        # T=0 행에서는 Y0가 factual, T=1 행에서는 Y1이 factual이라는 점이 같이 드러나야 한다.
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
    """
    Scene 06: 관찰된 평균 차이의 함정

    Core Claim:
    현실에서는 관찰된 집단 평균 차이를 곧바로 인과효과로 읽을 수 없고,
    같은 데이터에서도 관찰 차이와 진짜 ATE의 부호가 뒤집힐 수 있다.

    Expected Misconception:
    처치 집단 평균과 비교 집단 평균만 계산하면
    평균 효과를 충분히 근사할 수 있다고 오해하기 쉽다.

    Visual Pivot:
    Scene 05의 full table이 ipynb Cell 11의 observed table로 직접 바뀌고,
    그 표에서 계산한 `125`가 직전 Scene의 `ATE=-50`과 정면 충돌한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "ATE, ATT 모두 사실과 반사실이라는 두 세계를 모두 볼 수 있었기 때문에 계산할 수 있었던 것입니다."
    - 현재 Scene 첫 문장:
      "이제 현실로 돌아와 보겠습니다."
    - Cell 8:
      full table 데이터
    - Cell 11:
      observed table 데이터 (`y0`, `y1`, `te`에 `np.nan` 포함)
    - Cell 12:
      관찰 평균 차이 125와 진짜 `ATE=-50` 비교

    Notebook Code/Data Reference:
    - Cell 8 code:
      `pd.DataFrame(dict(i=[1,2,3,4], y0=[500,600,800,700], y1=[450,600,600,750], t=[0,0,1,1], y=[500,600,600,750], ite=[-50,0,-200,50]))`
    - Cell 11 code:
      `pd.DataFrame(dict(i=[1,2,3,4], y0=[500,600,np.nan,np.nan], y1=[np.nan,np.nan,600,750], t=[0,0,1,1], y=[500,600,600,750], te=[np.nan,np.nan,np.nan,np.nan]))`

    Previous Scene Continuity:
    - 직전 Scene 코드:
      `Scene05_MultiverseTableAteAtt`
    - 이어받는 시각 요소:
      같은 4개 학교 표, 같은 `Y_0 / Y_1 / T / Y` 열 의미, 같은 색 체계
    - 바뀌는 점:
      full-data table에서 관찰 가능한 셀만 남기고 counterfactual/ITE를 지운다.

    Script Reference:
    src/scripts/06_observed_mean_difference_trap.txt

    Asset Reference:
    Tabler Icons (MIT)
    - school.svg
    - eye-off.svg
    - device-tablet.svg
    - device-tablet-off.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py
    Reason:
    같은 데이터 구조를 유지한 채 관찰 가능한 정보만 남겨 의미를 뒤집는 비교 연출이 필요해서 참고했다.

    Script-to-Beat Mapping:
    1. Scene 05의 table grammar를 이어받아, 현실에서는 counterfactual과 ITE가 비어 버린다고 정리
    2. 그래도 `E[Y|T=1]-E[Y|T=0]`를 써보고 싶어지는 유혹을 질문으로 제시
    3. observed table의 `Y` 열만 이용해 treated 평균 675, control 평균 550을 계산
    4. 관찰 차이 125가 양의 효과처럼 보인다고 강조
    5. 직전 Scene에서 계산한 진짜 `ATE=-50`과 비교해 부호가 뒤집힌다고 보여줌
    6. 관찰 연관성을 인과효과로 읽으면 틀릴 수 있다는 질문으로 다음 Scene에 넘김

    Timing-to-Beat Mapping:
    - chunk 1 -> Beat 1
    - chunk 2 -> Beat 2
    - chunk 3 -> Beat 3
    - chunk 4 -> Beat 4
    - chunk 5 -> Beat 5
    - chunk 6 -> Beat 6
    """

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

        reality_label = Text("현실에서는 관찰된 결과만 남습니다", font_size=25, color=ACCENT_COLOR, weight=BOLD)
        reality_label.next_to(table_group, UP, buff=0.34)
        table_block = VGroup(table_group, reality_label)

        direct_calc_formula = MathTex(r"ITE_i,\ ATE,\ ATT").scale(0.92).set_color(ACCENT_COLOR)
        direct_calc_cross = Cross(direct_calc_formula, stroke_color=MAROON_E, stroke_width=7)
        direct_calc_block = VGroup(direct_calc_formula, direct_calc_cross)
        direct_calc_block.next_to(table_group, DOWN, buff=0.34)

        temptation = VGroup(
            Text("그냥 두 집단 평균을", font_size=26, color=NEUTRAL_COLOR, weight=BOLD),
            Text("비교하면 안 될까?", font_size=30, color=ACCENT_COLOR, weight=BOLD),
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
        observed_positive_label = Text("관찰 평균 차이", font_size=22, color=TABLET_COLOR, weight=BOLD)
        observed_positive_label.next_to(observed_positive, UP, buff=0.28)

        true_ate = MathTex(r"-50").scale(1.5).set_color(MAROON_E)
        true_ate.move_to(ORIGIN + DOWN * 0.05)
        true_ate_label = Text("진짜 ATE", font_size=22, color=ACCENT_COLOR, weight=BOLD)
        true_ate_label.next_to(true_ate, UP, buff=0.28)

        sign_flip = MathTex(r"+125", r"\ne", r"-50").scale(1.05)
        sign_flip[0].set_color(TABLET_COLOR)
        sign_flip[1].set_color(MAROON_E)
        sign_flip[2].set_color(MAROON_E)
        sign_flip.next_to(true_ate, DOWN, buff=0.42)

        # Beat 6 준비:
        # 마지막 장면은 표의 기억을 남기기 위해 작은 표 실루엣은 지우고, 결론 문장과 다음 질문만 남긴다.
        closing = VGroup(
            Text("observed association", font_size=32, color=WHITE, weight=BOLD),
            MathTex(r"\ne").scale(1.2).set_color(ACCENT_COLOR),
            Text("causal effect", font_size=34, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(RIGHT, buff=0.24)
        closing.move_to(UP * 0.55)
        why_next = Text("왜 이런 차이가 생길까?", font_size=28, color=QUESTION_COLOR, weight=BOLD)
        why_next.next_to(closing, DOWN, buff=0.34)

        # Beat 1:
        # Scene 05의 표 문법을 그대로 이어받아 full table을 먼저 보여준 뒤,
        # Cell 11 데이터대로 counterfactual과 ITE를 비워 현실 표로 바꾼다.
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
        # 앞 두 문장 동안은 표만 남겨 두고,
        # "그래서 개별 처치 효과인 ITE..."가 시작될 때 eye-off와 식을 함께 띄운다.
        self.wait(5.2)
        self.play(
            FadeIn(VGroup(*[cell[1] for cell in hidden_y1]), scale=0.9),
            FadeIn(VGroup(*[cell[1] for cell in hidden_y0]), scale=0.9),
            FadeIn(VGroup(*[cell[1] for cell in all_ite_cells]), scale=0.9),
            FadeIn(direct_calc_formula, shift=UP * 0.08),
            run_time=0.35,
        )
        # 식이 읽히기 시작한 직후, "직접 계산할 수 없고"에 맞춰 X를 올린다.
        self.wait(0.55)
        self.play(Create(direct_calc_cross), run_time=0.45)
        wait_for_chunks([1], spent=9.1)

        # Beat 2:
        # 직접 계산은 막혔지만, 평균 차이를 써보고 싶은 유혹이 자연스럽게 이어진다.
        # 초반 설명에만 필요했던 reality label은 여기서 바로 걷어내고,
        # 표만 좌측으로 밀어 다음 Beat 계산 공간을 연다.
        self.play(
            FadeOut(direct_calc_block, shift=DOWN * 0.08),
            FadeOut(reality_label, shift=UP * 0.08),
            table_group.animate.shift(LEFT * 1.45),
            FadeIn(temptation, shift=UP * 0.08),
            run_time=0.85,
        )
        wait_for_chunks([2], spent=0.85)

        # Beat 3:
        # Cell 12의 계산처럼 관찰 가능한 Y 열만 사용해 treated/control 평균을 계산한다.
        # 여기서는 표를 더 이상 이동시키지 않고, 열린 공간에서 바로 평균 계산으로 들어간다.
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
        wait_for_chunks([3], spent=3.6)

        # Beat 4:
        # 관찰 평균 차이만 먼저 읽히게 한다.
        # 여기서는 표를 배경으로 남기지 않고, Scene 5처럼 한 번 비워서 숫자만 보이게 만든다.
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
        wait_for_chunks([4], spent=1.45)

        # Beat 5:
        # 여기서 처음으로 진짜 ATE를 꺼내 관찰 차이 해석을 뒤집는다.
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
        wait_for_chunks([5], spent=1.15)

        # Beat 6:
        # 마지막에는 표와 계산 카드를 지우고, 관찰 연관성과 인과효과를 구분해야 한다는 문장으로 다음 질문을 남긴다.
        self.play(
            FadeOut(true_ate_label),
            FadeOut(true_ate),
            FadeOut(sign_flip),
            run_time=0.75,
        )
        self.play(FadeIn(closing, shift=UP * 0.08), run_time=0.6)
        self.play(FadeIn(why_next, shift=UP * 0.08), run_time=0.5)
        wait_for_chunks([6], spent=1.35)
        self.wait(self.WAIT_TAIL)


class Scene07_BiasDecomposition(Scene):
    """
    Scene 07: 편향 분해

    Core Claim:
    관찰 평균 차이는 처치 효과 하나만이 아니라, 원래 집단 차이에서 오는 편향까지 함께 섞인 값이다.

    Expected Misconception:
    단순 평균 차이가 틀리는 이유를 "표본이 작아서" 정도로만 이해하고,
    구조적으로 어떤 항이 섞였는지는 놓치기 쉽다.

    Visual Pivot:
    관찰 평균 차이 식이 `ATT + Bias` 분해식으로 다시 쓰이고,
    마지막에는 학교 여건이 처치와 결과 양쪽으로 향하는 교란 구조로 수렴한다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "즉, 관찰된 연관성을 인과효과로 곧장 읽으면 틀릴 수 있습니다. 그렇다면 왜 이런 차이가 생기는 걸까요?"
    - 현재 Scene 첫 문장:
      "핵심은 단순 평균 차이에 편향(Bias) 이 섞여 있기 때문입니다."
    - Cell 14:
      태블릿 예시의 직관 설명, `E[Y|T=1]-E[Y|T=0]` 분해, 편향과 교란변수 설명

    Previous Scene Continuity:
    - 직전 Scene 코드:
      `Scene06_ObservedMeanDifferenceTrap`
    - 이어받는 시각 요소:
      태블릿 학교 vs 비교 학교 구도, 관찰 평균 차이 문제 제기
    - 바뀌는 점:
      숫자 계산 장면에서 벗어나, 왜 그런 차이가 생기는지 식과 구조로 해부한다.

    Script Reference:
    src/scripts/07_bias_decomposition.txt

    Asset Reference:
    Tabler Icons (MIT)
    - device-tablet.svg
    - device-tablet-off.svg
    - coin.svg
    - map-pin.svg
    - users-group.svg
    - school.svg

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py
    Reason:
    하나의 식을 점진적으로 재배열해 의미를 분리하고, 마지막에 원인 구조로 묶는 리듬을 참고했다.

    Script-to-Beat Mapping:
    1. 단순 평균 차이에 편향이 섞인다는 핵심 주장 제시
    2. 태블릿 학교가 원래 더 좋은 조건이었을 수 있다는 직관 예시
    3. `E[Y_0|T=1] > E[Y_0|T=0]`로 잠재적 결과 해석
    4. 관찰 연관성 식 제시
    5. `ATT + Bias` 분해식으로 재정리
    6. ATT와 Bias의 의미를 각각 읽게 함
    7. 교란변수 구조와 편향 제거 필요성으로 마무리

    Timing-to-Beat Mapping:
    - chunk 1 -> Beat 1
    - chunk 2 -> Beat 2
    - chunk 3 -> Beat 3
    - chunk 4-5 -> Beat 4-5
    - chunk 6-7 -> Beat 6
    - chunk 8-11 -> Beat 7
    """

    WAIT_TAIL = 1.5  # mp3(92.87s) > video(92.38s) → 0.49s 부족, 1.5s로 늘려 나레이션 끊김 해소

    def construct(self):
        chunk_durations = load_scene_timing_durations("07_bias_decomposition")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        bias_word = Text("단순 평균 차이는 왜 인과효과가 아닐까?", font_size=34, color=QUESTION_COLOR, weight=BOLD)
        bias_word.move_to(ORIGIN + UP * 0.7)

        avg_diff_box = RoundedRectangle(
            width=4.3,
            height=0.8,
            corner_radius=0.2,
            stroke_color=WHITE,
            stroke_width=1.8,
        )
        avg_diff_label = Text("관찰된 평균 차이", font_size=26, color=WHITE, weight=BOLD).move_to(avg_diff_box)
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
            Text("태블릿 지급", font_size=24, color=TABLET_COLOR, weight=BOLD),
            VGroup(
                load_icon("school.svg", WHITE, 0.64),
                load_icon("arrow-up.svg", TABLET_COLOR, 0.56),
            ).arrange(RIGHT, buff=0.18),
            Text("원래 성적이 높았을 수 있음", font_size=20, color=WHITE, weight=BOLD),
        ).arrange(DOWN, buff=0.18).move_to(treated_card)
        control_group = VGroup(
            MathTex(r"T=0").set_color(LIBRARY_COLOR).scale(0.82),
            Text("태블릿 미지급", font_size=24, color=LIBRARY_COLOR, weight=BOLD),
            VGroup(
                load_icon("school.svg", WHITE, 0.64),
                load_icon("arrow-down.svg", LIBRARY_COLOR, 0.56),
            ).arrange(RIGHT, buff=0.18),
            Text("원래 성적이 낮았을 수 있음", font_size=20, color=WHITE, weight=BOLD),
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
        att_note = Text("실제 인과효과", font_size=24, color=ACCENT_COLOR, weight=BOLD).next_to(att_focus, RIGHT, buff=0.28)
        bias_note = Text("원래 집단 차이", font_size=24, color=QUESTION_COLOR, weight=BOLD).next_to(bias_focus, RIGHT, buff=0.28)

        confounder_box = RoundedRectangle(width=4.4, height=1.7, corner_radius=0.18, stroke_color=NEUTRAL_COLOR, stroke_width=2.2).move_to(UP * 1.45)
        confounder_label = Text("학교 여건", font_size=28, color=WHITE, weight=BOLD)
        confounder_label.move_to(confounder_box.get_top() + DOWN * 0.36)
        budget_chip = VGroup(
            load_icon("coin.svg", GOLD_E, 0.3),
            Text("재정", font_size=20, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        location_chip = VGroup(
            load_icon("map-pin.svg", BLUE_E, 0.3),
            Text("위치", font_size=20, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        teacher_chip = VGroup(
            load_icon("user-star.svg", GREEN_E, 0.3),
            Text("교사의 질", font_size=20, color=WHITE, weight=BOLD),
        ).arrange(RIGHT, buff=0.1)
        confounder_factors = VGroup(budget_chip, location_chip, teacher_chip).arrange(RIGHT, buff=0.28)
        confounder_factors.move_to(confounder_box.get_center() + DOWN * 0.22)
        t_node = VGroup(Circle(radius=0.56, stroke_color=TABLET_COLOR, stroke_width=2.6), MathTex(r"T").set_color(TABLET_COLOR)).move_to(LEFT * 2.6 + DOWN * 0.35)
        y_node = VGroup(Circle(radius=0.56, stroke_color=ACCENT_COLOR, stroke_width=2.6), MathTex(r"Y").set_color(ACCENT_COLOR)).move_to(RIGHT * 2.6 + DOWN * 0.35)
        t_label = Text("처치", font_size=23, color=TABLET_COLOR, weight=BOLD).next_to(t_node, DOWN, buff=0.18)
        y_label = Text("결과", font_size=23, color=ACCENT_COLOR, weight=BOLD).next_to(y_node, DOWN, buff=0.18)
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
        # 남는 요소: 없음.
        # 새로 등장하는 요소: bias_word, 평균 차이 배지.
        # 비워 두는 영역: 하단 카드 영역 전체.
        # 질문을 먼저 던지고, 바로 아래 배지가 effect + bias로 갈라지는 흐름으로 편향을 예고한다.
        self.play(FadeIn(bias_word, scale=0.9), run_time=0.8)
        self.play(FadeIn(avg_diff_group, shift=UP * 0.06), run_time=0.7)
        self.play(
            Transform(avg_diff_group, split_group),
            run_time=0.9,
        )
        wait_for_chunks([1], spent=2.4)

        # Beat 2:
        # 남는 요소: 없음.
        # 새로 등장하는 요소: 두 집단 카드.
        # 비워 두는 영역: 하단 수식 영역.
        # 직관 예시는 카드 2개만 남긴다. 긴 인용문 박스는 쓰지 않고 Y0 차이만 카드 내부에 둔다.
        self.play(FadeOut(bias_word, scale=0.95), FadeOut(avg_diff_group), run_time=0.3)
        self.play(
            FadeIn(treated_card, scale=0.96),
            FadeIn(control_card, scale=0.96),
            FadeIn(treated_group, shift=UP * 0.06),
            FadeIn(control_group, shift=UP * 0.06),
            run_time=0.95,
        )
        wait_for_chunks([2], spent=1.2)

        # Beat 3:
        # 남는 요소: title, 두 카드.
        # 새로 등장하는 요소: inequality.
        # 비워 두는 영역: 화면 상단 제목 외 대부분은 카드 2개와 하단 수식으로만 사용.
        # 카드의 Y0 차이를 잠재적 결과 부등식으로 압축한다.
        self.play(FadeIn(inequality, shift=UP * 0.08), run_time=0.65)
        self.play(
            Indicate(treated_group[-1], color=TABLET_COLOR, scale_factor=1.04),
            Indicate(control_group[-1], color=LIBRARY_COLOR, scale_factor=1.04),
            run_time=0.6,
        )
        wait_for_chunks([3], spent=1.25)

        # Beat 4:
        # 남는 요소: 없음.
        # 새로 등장하는 요소: observed_formula.
        # 비워 두는 영역: 좌우 카드 영역을 비워 수식 하나만 읽히게 한다.
        # 카드 장면을 완전히 정리한 뒤 관찰 데이터 식만 단독으로 올린다.
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
        wait_for_chunks([4], spent=1.35)

        # Beat 5:
        # 남는 요소: decomp_summary, detail 식.
        # 새로 등장하는 요소: att/bias highlight와 짧은 note.
        # 비워 두는 영역: 좌우 측면.
        # 분해식만 화면 중앙에 두고 ATT와 Bias를 번갈아 읽게 한다.
        self.play(TransformMatchingTex(observed_formula, decomp_summary), run_time=0.95)
        self.play(FadeIn(att_detail, shift=UP * 0.06), FadeIn(bias_detail, shift=UP * 0.06), run_time=0.5)
        wait_for_chunks([5], spent=0.95)
        self.play(FadeIn(att_focus), FadeIn(att_note, shift=UP * 0.06), run_time=0.45)
        self.play(Indicate(att_focus, color=ACCENT_COLOR, scale_factor=1.02), run_time=0.5)
        # chunk 6 앞부분의 "하나는 ... ATT" 설명이 먼저 충분히 지나가도록 잠시 유지한다.
        self.wait(3.4)
        self.play(
            FadeOut(att_focus),
            FadeOut(att_note),
            FadeIn(bias_focus),
            FadeIn(bias_note, shift=UP * 0.06),
            run_time=0.45,
        )
        self.play(Indicate(bias_focus, color=QUESTION_COLOR, scale_factor=1.02), run_time=0.5)
        wait_for_chunks([6, 7], spent=5.3)

        # Beat 6:
        # 남는 요소: confounder DAG, 하단 비교 패널.
        # 새로 등장하는 요소: 교란 세부 요인, 교란 경로 차단 표시, 정렬된 비교 패널.
        # 비워 두는 영역: 상단 수식 영역까지 모두 비워 DAG와 작은 하단 패널만 읽히게 한다.
        # 후반부는 "교란이 있으면 출발선이 다르고, 경로를 끊으면 비교 가능해진다"를 도형 변화로만 마무리한다.
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
        wait_for_chunks([8, 9], spent=9.65)
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
        wait_for_chunks([10, 11], spent=6.95)
        self.wait(self.WAIT_TAIL)


class Scene08_WhenAssociationBecomesCausation(Scene):
    """
    Scene 08: 언제 연관성이 인과관계가 될까?

    Core Claim:
    편향 항이 0일 때, 즉 두 집단이 처치 여부를 제외하면 비교 가능한 상태일 때만
    단순 평균 차이가 인과효과(ATT)와 같아진다.
    나아가 처치 반응이 동질하면 ATT=ATC=ATE로 확장된다.

    Expected Misconception:
    "편향=0 조건만 충족되면 평균 차이=ATE"로 곧바로 이해하고,
    ATT=ATC 조건(동질 반응)이 별도로 필요하다는 점을 놓치기 쉽다.

    Visual Pivot:
    ATT+Bias 분해식에서 Bias 항이 사라지는 순간,
    그리고 ATT → ATC → ATE로 등식이 한 단계씩 확장되는 수식 흐름.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "편향을 제거하지 않으면 관찰된 연관성은 인과효과와 다르다."
    - 현재 Scene 첫 문장:
      "그렇다면 언제 연관성이 인과관계가 될까요?"
    - Cell 17-18: 비교 가능성 조건, E[Y_0|T=1]=E[Y_0|T=0], ATT=ATC=ATE 등식

    Previous Scene Continuity:
    - 직전 Scene: Scene07_BiasDecomposition
    - 이어받는 시각 요소: ATT+Bias 분해식 구조 (리콜), 집단 비교 구도
    - 바뀌는 점: 편향 분해 분석 → 편향 제거 조건과 결과로 전진

    Script Reference:
    src/scripts/08_when_association_becomes_causation.txt

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py
    Reason:
    단일 수식이 점진적으로 변형되며 의미가 확장되는 리듬을 참고했다.

    Script-to-Beat Mapping:
    1. 질문 제기: "언제 연관성이 인과관계가 될까?" (chunk 1)
    2. 앞서 본 ATT+Bias 분해식 리콜 (chunk 2)
    3. 편향 항 = 0 조건 강조 (chunk 3)
    4. 비교 가능성 수식 E[Y_0|T=1]=E[Y_0|T=0] 도입 (chunk 4)
    5. 직관 예시: 두 집단 카드 (chunk 5)
    6. "비교 가능한 상태" 요약 배지 (chunk 6)
    7. 조건 충족 시 편향 소거 → 평균 차이 = ATT (chunk 7)
    8. ATT = ATC (chunk 8)
    9. 결국 평균 차이 = ATE (chunk 9)
    10. 정리: 비교 가능성 (chunk 10)
    11. 다음 질문 예고 (chunk 11)

    Timing-to-Beat Mapping:
    - chunk 1  -> Beat 1  (0 – 3.30s)
    - chunk 2  -> Beat 2  (3.30 – 10.17s)
    - chunk 3  -> Beat 3  (10.17 – 15.84s)
    - chunk 4  -> Beat 4  (15.84 – 26.80s)
    - chunk 5  -> Beat 5  (26.80 – 38.17s)
    - chunk 6  -> Beat 6  (38.17 – 43.37s)
    - chunk 7  -> Beat 7  (43.37 – 48.90s)
    - chunk 8  -> Beat 8  (48.90 – 57.45s)
    - chunk 9  -> Beat 9  (57.45 – 62.93s)
    - chunk 10 -> Beat 10 (62.93 – 67.94s)
    - chunk 11 -> Beat 11 (67.94 – 74.40s)
    """

    WAIT_TAIL = 0.3

    def construct(self):
        chunk_durations = load_scene_timing_durations("08_when_association_becomes_causation")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        # ── 사전 Mobject 정의 ──────────────────────────────────────────────────

        # Beat 1: 질문 텍스트
        question = Text(
            "언제 연관성이 인과관계가 될까요?",
            font_size=36,
            color=QUESTION_COLOR,
            weight=BOLD,
        )
        question.move_to(ORIGIN)

        # Beat 2: ATT+Bias 분해식 리콜 - 요약 한 줄 + 세부 두 줄로 분리해 가로 넘침 방지
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

        # Beat 3: Bias = 0 조건 라벨 (사각형 대신 Indicate + FadeIn)
        bias_zero = MathTex(r"\text{Bias} = 0", color=QUESTION_COLOR).scale(0.9)
        bias_zero.next_to(bias_recall_detail, DOWN, buff=0.45)

        # Beat 4: 비교 가능성 조건 수식 (편향=0의 수식적 의미)
        comparability_formula = MathTex(
            r"E[Y_0\mid T=1]",
            r"=",
            r"E[Y_0\mid T=0]",
        ).scale(1.1)
        comparability_formula[0].set_color(TABLET_COLOR)
        comparability_formula[1].set_color(WHITE)
        comparability_formula[2].set_color(LIBRARY_COLOR)
        comparability_formula.move_to(ORIGIN)

        # Beat 5: 상단에 수식 작게, 중앙에 두 집단 카드
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
            Text("태블릿 지급", font_size=22, color=TABLET_COLOR, weight=BOLD),
            Text("태블릿 없어도", font_size=19, color=WHITE),
            Text("비슷한 성적", font_size=20, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.16).move_to(treated_card8)

        control_content8 = VGroup(
            MathTex(r"T=0").set_color(LIBRARY_COLOR).scale(0.78),
            Text("태블릿 미지급", font_size=22, color=LIBRARY_COLOR, weight=BOLD),
            Text("기준 집단", font_size=19, color=WHITE),
            Text("평균 성적", font_size=20, color=ACCENT_COLOR, weight=BOLD),
        ).arrange(DOWN, buff=0.16).move_to(control_card8)

        card_equal = MathTex(r"\approx").scale(1.3).set_color(ACCENT_COLOR)
        card_equal.move_to(ORIGIN + DOWN * 0.3)

        # Beat 6: "비교 가능한 상태" 강조 배지 (하단)
        comparable_badge = RoundedRectangle(
            width=5.0, height=0.9, corner_radius=0.22,
            stroke_color=ACCENT_COLOR, stroke_width=2.5,
            fill_color=ACCENT_COLOR, fill_opacity=0.1,
        )
        comparable_label = Text("비교 가능한 상태", font_size=30, color=ACCENT_COLOR, weight=BOLD)
        comparable_badge.move_to(comparable_label)
        comparable_group = VGroup(comparable_badge, comparable_label)
        comparable_group.to_edge(DOWN, buff=0.65)

        # Beat 7: 편향 소거 → 평균차이 = ATT
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

        # Beat 8: ATT = ATC
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

        # Beat 9: = ATE
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

        # Beat 10: 정리 - "비교 가능성" → "연관성 = 인과관계"
        summary_text = Text(
            "비교 가능성",
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
            "연관성 = 인과관계",
            font_size=28,
            color=WHITE,
        )
        causation_text.next_to(arrow_down, DOWN, buff=0.22)

        # Beat 11: 다음 질문 예고
        next_question = Text(
            "현실에서 어떻게\n비교 가능한 집단을 만들 수 있을까요?",
            font_size=32,
            color=QUESTION_COLOR,
            weight=BOLD,
            line_spacing=1.2,
        )
        next_question.move_to(ORIGIN)

        # ── Beat 1: 질문 제기 ────────────────────────────────────────────────
        # 남는 요소: 없음
        # 새로 등장하는 요소: question (중앙)
        # 비워두는 영역: 전체
        # 핵심 시선 대상: question
        self.play(FadeIn(question, scale=0.9), run_time=0.85)
        wait_for_chunks([1], spent=0.85)

        # ── Beat 2: ATT+Bias 분해식 리콜 ────────────────────────────────────
        # 남는 요소: 없음 (question FadeOut)
        # 새로 등장하는 요소: decomp_summary_recall (상단), 세부 두 줄 (중앙)
        # 비워두는 영역: 하단
        # 핵심 시선 대상: 요약 식 → ATT → Bias 순으로 Indicate
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

        # ── Beat 3: Bias = 0 조건 강조 ──────────────────────────────────────
        # 남는 요소: decomp_recall_group (유지)
        # 새로 등장하는 요소: bias_zero (하단)
        # 비워두는 영역: 좌/우 여백
        # 핵심 시선 대상: Bias = 0 라벨
        self.play(
            Indicate(decomp_summary_recall[4], color=QUESTION_COLOR, scale_factor=1.15),
            Indicate(bias_recall_detail, color=QUESTION_COLOR, scale_factor=1.08),
            run_time=0.65,
        )
        self.play(FadeIn(bias_zero, shift=UP * 0.07), run_time=0.55)
        wait_for_chunks([3], spent=1.2)

        # ── Beat 4: 비교 가능성 수식 도입 ───────────────────────────────────
        # 남는 요소: 없음 (분해식 일체 FadeOut)
        # 새로 등장하는 요소: comparability_formula (중앙, 크게)
        # 비워두는 영역: 상단/하단
        # 핵심 시선 대상: E[Y_0|T=1] = E[Y_0|T=0]
        self.play(
            FadeOut(decomp_recall_group),
            FadeOut(bias_zero),
            run_time=0.55,
        )
        self.play(FadeIn(comparability_formula, shift=UP * 0.07), run_time=0.75)
        self.play(Indicate(comparability_formula[0], color=TABLET_COLOR, scale_factor=1.04), run_time=0.5)
        self.play(Indicate(comparability_formula[2], color=LIBRARY_COLOR, scale_factor=1.04), run_time=0.5)
        wait_for_chunks([4], spent=2.3)

        # ── Beat 5: 직관 예시 (두 집단 카드) ────────────────────────────────
        # 남는 요소: comparability_small (수식 축소 → 상단으로 이동)
        # 새로 등장하는 요소: 두 카드 + card_equal (중앙)
        # 비워두는 영역: 하단
        # 핵심 시선 대상: 두 카드의 동등성 (card_equal)
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

        # ── Beat 6: "비교 가능한 상태" 배지 ─────────────────────────────────
        # 남는 요소: 카드 2개, comparability_formula (상단 작게)
        # 새로 등장하는 요소: comparable_group (하단)
        # 비워두는 영역: 상단 수식 외 중앙 카드/배지만 유지
        # 핵심 시선 대상: "비교 가능한 상태" 텍스트
        self.play(FadeIn(comparable_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(comparable_badge, color=ACCENT_COLOR, scale_factor=1.03), run_time=0.55)
        wait_for_chunks([6], spent=1.15)

        # ── Beat 7: 편향 소거 → 평균차이 = ATT ─────────────────────────────
        # 남는 요소: 없음 (카드/배지 일체 FadeOut)
        # 새로 등장하는 요소: result_att (상단), bias_zero_condition (하단)
        # 비워두는 영역: 좌/우 여백
        # 핵심 시선 대상: 평균차이 = ATT 수식
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

        # ── Beat 8: ATT = ATC ───────────────────────────────────────────────
        # 남는 요소: 수식 (result_att → result_att_atc Transform)
        # 새로 등장하는 요소: ATC 항 추가, 조건식 교체
        # 비워두는 영역: 좌/우 여백
        # 핵심 시선 대상: ATT = ATC 관계
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

        # ── Beat 9: = ATE ────────────────────────────────────────────────────
        # 남는 요소: 전체 등식 (result_full로 확장)
        # 새로 등장하는 요소: ATE 항 추가
        # 비워두는 영역: 하단 조건식 제거
        # 핵심 시선 대상: ATE 항
        self.play(
            TransformMatchingTex(result_att_atc, result_full),
            FadeOut(atc_condition),
            run_time=0.85,
        )
        self.play(Indicate(result_full[6], color=YELLOW_E, scale_factor=1.06), run_time=0.55)
        wait_for_chunks([9], spent=1.4)

        # ── Beat 10: 정리 ────────────────────────────────────────────────────
        # 남는 요소: 없음 (수식 FadeOut)
        # 새로 등장하는 요소: summary_text (상단), arrow_down, causation_text (하단)
        # 비워두는 영역: 좌/우
        # 핵심 시선 대상: "비교 가능성" 키워드
        self.play(FadeOut(result_full), run_time=0.55)
        self.play(FadeIn(summary_text, scale=0.9), run_time=0.7)
        self.play(GrowArrow(arrow_down), run_time=0.5)
        self.play(FadeIn(causation_text, shift=UP * 0.06), run_time=0.5)
        wait_for_chunks([10], spent=2.25)

        # ── Beat 11: 다음 질문 예고 ──────────────────────────────────────────
        # 남는 요소: 없음 (정리 요소 FadeOut)
        # 새로 등장하는 요소: next_question (중앙)
        # 비워두는 영역: 전체
        # 핵심 시선 대상: 다음 질문 텍스트
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
    """
    Scene 09: 무작위 실험 (RCT)

    Core Claim:
    무작위 배정은 (Y_0,Y_1)⊥T 조건을 만들어,
    편향 제거(조건 1)와 동질 반응(조건 2)을 동시에 확보한다.
    그 결과 단순 평균 차이가 ATE와 같아진다.

    Expected Misconception:
    "무작위이면 두 집단이 완벽하게 같아진다"고 오해하기 쉽다.
    실제로는 평균적으로 비슷해지는 것이며,
    두 가지 조건이 별도로 충족되어야 ATE까지 연결된다는 점을 놓치기 쉽다.

    Visual Pivot:
    Scene07에서 교란 → T 화살표가 있던 DAG와 달리,
    이번엔 교란 → T 경로가 없는 DAG로 무작위 배정의 구조적 차이를 보여준다.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "현실에서 어떻게 이런 비교 가능한 집단을 만들 수 있을까요?"
    - 현재 Scene 첫 문장:
      "바로 무작위 배정입니다."
    - Cell 19-20: 무작위 배정 개념, (Y_0,Y_1)⊥T, 두 조건, ATT=ATC=ATE

    Previous Scene Continuity:
    - 직전 Scene: Scene08_WhenAssociationBecomesCausation
    - 이어받는 시각 요소: ATT=ATC=ATE 등식 구조, 비교 가능성 개념
    - 바뀌는 점: "조건이 필요하다"에서 "무작위 배정으로 조건을 확보한다"로 전환

    Script Reference:
    src/scripts/09_randomized_experiment.txt

    3Blue1Brown Reference:
    3b1b/videos/_2020/covid.py
    Reason:
    단일 독립 조건에서 두 결론이 자동으로 도출되는 점진적 수식 전개 리듬 참고.

    Script-to-Beat Mapping:
    1. "무작위 배정" 핵심 키워드 제시 (chunk 1)
    2. 교란 → T 없는 DAG: 배정이 교란과 무관함 (chunk 2)
    3. 두 집단 막대 동등화: 처치 여부 외 모든 면 비슷 (chunk 3)
    4. (Y_0,Y_1)⊥T 독립 수식 (chunk 4)
    5. "두 조건 자동 충족" 예고 (chunk 5)
    6. 조건 1: E[Y_0|T=1]=E[Y_0|T=0] → 편향=0 (chunk 6)
    7. 조건 2: E[Y_1|T=1]=E[Y_1|T=0] → ATT=ATC (chunk 7)
    8. 결론: 평균차이=ATE (chunk 8)
    9. RCT = gold standard 마무리 (chunk 9)

    Timing-to-Beat Mapping:
    - chunk 1 -> Beat 1  (0 – 1.67s)
    - chunk 2 -> Beat 2  (1.67 – 11.19s)
    - chunk 3 -> Beat 3  (11.19 – 17.69s)
    - chunk 4 -> Beat 4  (17.69 – 23.41s)
    - chunk 5 -> Beat 5  (23.41 – 27.82s)
    - chunk 6 -> Beat 6  (27.82 – 42.77s)
    - chunk 7 -> Beat 7  (42.77 – 53.50s)
    - chunk 8 -> Beat 8  (53.50 – 56.98s)
    - chunk 9 -> Beat 9  (56.98 – 69.15s)
    """

    WAIT_TAIL = 0.3

    def construct(self):
        chunk_durations = load_scene_timing_durations("09_randomized_experiment")

        def wait_for_chunks(indices: list[int], spent: float = 0.0, extra: float = 0.0) -> None:
            if not chunk_durations:
                return
            total = sum(chunk_durations[index - 1] for index in indices) - spent + extra
            if total > 0:
                self.wait(total)

        # ── 사전 Mobject 정의 ──────────────────────────────────────────────────

        # Beat 1: "무작위 배정" 핵심 키워드
        random_label = Text("무작위 배정", font_size=52, color=ACCENT_COLOR, weight=BOLD)
        random_label.move_to(ORIGIN)

        # Beat 2-3: 산점도 — 학교 여건(x) × 시험 점수(y)
        # Beat 2: 편향 있는 분포 → 무작위 배정 후 섞인 분포 (점 이동 애니메이션)
        # Beat 3: 무작위화 후 평균선 + 레이블 (처치 효과 = 두 그룹 평균 차이)
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
        scatter_x_label = Text("학교 여건", font_size=19, color=NEUTRAL_COLOR)
        scatter_x_label.next_to(scatter_axes.x_axis, DOWN, buff=0.22)
        scatter_y_label = VGroup(*[
            Text(ch, font_size=19, color=NEUTRAL_COLOR) for ch in "시험점수"
        ]).arrange(DOWN, buff=0.05)
        scatter_y_label.next_to(scatter_axes.y_axis, LEFT, buff=0.22)
        scatter_axes_group = VGroup(scatter_axes, scatter_x_label, scatter_y_label)

        # 편향 있는 배정: T=1 우상단, T=0 좌하단 (교란요인과 처치가 상관됨)
        biased_t1_coords = [
            (5.5, 5.5), (6.5, 7.0), (7.0, 6.0), (8.0, 8.0), (9.0, 7.5),
            (7.5, 8.5), (8.5, 6.5), (6.0, 8.0), (9.0, 9.0), (7.0, 7.5),
        ]
        biased_t0_coords = [
            (1.0, 2.0), (2.0, 1.0), (2.5, 3.0), (3.5, 2.5), (4.0, 1.5),
            (1.5, 3.5), (3.0, 4.0), (4.5, 3.5), (2.0, 4.5), (4.0, 4.5),
        ]
        # 무작위화 후: x 전역 분포, 두 그룹이 y 방향으로 교차(interleaved)
        # T=1 평균 y ≈ 6.0, T=0 평균 y ≈ 4.45 — 개별 점은 겹침
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

        # Beat 3: 평균선 — T=1 평균 y≈6.8, T=0 평균 y≈3.5
        _x0 = scatter_axes.coords_to_point(0, 0)[0]
        _x1 = scatter_axes.coords_to_point(10, 0)[0]
        _my1 = scatter_axes.coords_to_point(0, 6.0)[1]  # T=1 무작위화 후 평균
        _my0 = scatter_axes.coords_to_point(0, 4.45)[1]  # T=0 무작위화 후 평균
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

        # Beat 4: (Y_0, Y_1) ⊥ T 독립 수식
        indep_formula = MathTex(
            r"(Y_0,\,Y_1)",
            r"\perp",
            r"T",
        ).scale(1.5)
        indep_formula[0].set_color(ACCENT_COLOR)
        indep_formula[1].set_color(WHITE)
        indep_formula[2].set_color(TABLET_COLOR)
        indep_formula.move_to(ORIGIN)

        # Beat 5: "두 조건 자동 충족" 예고 (수식 작게 상단)
        indep_small = MathTex(
            r"(Y_0,\,Y_1)\perp T"
        ).scale(0.75).set_color(NEUTRAL_COLOR)
        indep_small.to_edge(UP, buff=0.5)

        cond_preview = Text("두 조건이 자동으로 충족됩니다", font_size=30, color=WHITE)
        cond_preview.move_to(ORIGIN)

        # Beat 6: 조건 1 수식 + 편향=0 결과
        # 구획: 상단(조건 수식), 하단(편향=0 배지)
        cond1_formula = MathTex(
            r"E[Y_0\mid T=1]",
            r"=",
            r"E[Y_0\mid T=0]",
        ).scale(1.05)
        cond1_formula[0].set_color(TABLET_COLOR)
        cond1_formula[1].set_color(WHITE)
        cond1_formula[2].set_color(LIBRARY_COLOR)
        cond1_formula.move_to(ORIGIN + UP * 0.55)

        cond1_num = Text("① 조건", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
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

        # Beat 7: 조건 1 작게 + 조건 2 수식 + ATT=ATC
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

        cond2_num = Text("② 조건", font_size=22, color=NEUTRAL_COLOR, weight=BOLD)
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

        # Beat 8: 결론 수식 (평균차이 = ATE)
        conclusion_formula = MathTex(
            r"E[Y\mid T=1]-E[Y\mid T=0]",
            r"=",
            r"ATE",
        ).scale(1.05)
        conclusion_formula[2].set_color(YELLOW_E)
        conclusion_formula.move_to(ORIGIN)

        # Beat 9: RCT gold standard 배지
        rct_label = Text("RCT", font_size=64, color=ACCENT_COLOR, weight=BOLD)
        rct_label.move_to(ORIGIN + UP * 0.5)
        gold_badge = RoundedRectangle(
            width=5.6, height=0.9, corner_radius=0.22,
            stroke_color=YELLOW_E, stroke_width=2.2,
            fill_color=YELLOW_E, fill_opacity=0.08,
        )
        gold_label = Text("인과효과 추정의 gold standard", font_size=26, color=YELLOW_E, weight=BOLD)
        gold_badge.move_to(gold_label)
        gold_group = VGroup(gold_badge, gold_label)
        gold_group.next_to(rct_label, DOWN, buff=0.55)

        # ── Beat 1: "무작위 배정" 키워드 ────────────────────────────────────
        # 남는 요소: 없음
        # 새로 등장: random_label (중앙)
        # 비워두는 영역: 전체
        # 핵심 시선: "무작위 배정" 텍스트
        self.play(FadeIn(random_label, scale=0.85), run_time=0.75)
        wait_for_chunks([1], spent=0.75)

        # ── Beat 2: 산점도 — 편향 분포 → 무작위 섞임 ────────────────────────
        # 남는 요소: 없음 (random_label FadeOut)
        # 새로 등장: scatter_axes_group → biased dots → 점 이동 애니메이션
        # 비워두는 영역: 우측 (Beat3 레이블 공간 확보)
        # 핵심 시선: 점들이 섞이는 순간 (무작위 배정의 시각적 의미)
        self.play(FadeOut(random_label, scale=0.95), run_time=0.35)
        self.play(FadeIn(scatter_axes_group), run_time=0.7)
        self.play(
            FadeIn(biased_t1_dots, lag_ratio=0.12),
            FadeIn(biased_t0_dots, lag_ratio=0.12),
            run_time=0.9,
        )
        # 편향 상태를 잠깐 보여준 뒤 무작위 배정으로 점들이 섞임
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

        # ── Beat 3: 평균선 + 레이블 — 두 그룹 평균 비교 ─────────────────────
        # 남는 요소: scatter_axes_group + biased_t1/t0_dots (무작위화 후 위치)
        # 새로 등장: mean_line_t1, mean_line_t0, mean_label_t1, mean_label_t0
        # 비워두는 영역: 우측 레이블 공간
        # 핵심 시선: 두 평균선의 간격 = 순수한 처치 효과
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

        # ── Beat 4: (Y_0, Y_1) ⊥ T 독립 수식 ──────────────────────────────
        # 남는 요소: 없음 (scatter 일체 FadeOut)
        # 새로 등장: indep_formula (중앙, 크게)
        # 비워두는 영역: 상단/하단
        # 핵심 시선: ⊥ 기호 (독립 조건)
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

        # ── Beat 5: "두 조건 자동 충족" 예고 ────────────────────────────────
        # 남는 요소: indep_small (수식 축소 → 상단)
        # 새로 등장: cond_preview (중앙)
        # 비워두는 영역: 하단
        # 핵심 시선: "두 조건" 텍스트
        self.play(Transform(indep_formula, indep_small), run_time=0.6)
        self.play(FadeIn(cond_preview, shift=UP * 0.07), run_time=0.6)
        wait_for_chunks([5], spent=1.2)

        # ── Beat 6: 조건 1 — E[Y_0|T=1] = E[Y_0|T=0] + 편향=0 ─────────────
        # 남는 요소: 없음 (cond_preview FadeOut, indep_formula 제거)
        # 새로 등장: cond1_num, cond1_formula (상단), bias_zero_group (하단)
        # 비워두는 영역: 좌/우 여백
        # 핵심 시선: cond1_formula
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

        # ── Beat 7: 조건 2 — E[Y_1|T=1] = E[Y_1|T=0] + ATT=ATC ────────────
        # 남는 요소: cond1_small (조건1 축소 → 상단)
        # 새로 등장: cond2_num, cond2_formula, att_atc_group
        # 비워두는 영역: 좌/우 여백, 상단은 조건1 small
        # 핵심 시선: cond2_formula + ATT=ATC
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

        # ── Beat 8: 결론 — 평균차이 = ATE ──────────────────────────────────
        # 남는 요소: 없음 (조건들 FadeOut)
        # 새로 등장: conclusion_formula (중앙)
        # 비워두는 영역: 상단/하단
        # 핵심 시선: ATE 항
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

        # ── Beat 9: RCT = gold standard ──────────────────────────────────
        # 남는 요소: 없음 (conclusion_formula FadeOut)
        # 새로 등장: rct_label (상단), gold_group (하단)
        # 비워두는 영역: 좌/우 여백
        # 핵심 시선: "RCT" 텍스트 + gold_group 배지
        self.play(FadeOut(conclusion_formula), run_time=0.5)
        self.play(FadeIn(rct_label, scale=0.85), run_time=0.75)
        self.play(FadeIn(gold_group, shift=UP * 0.07), run_time=0.6)
        self.play(Indicate(gold_badge, color=YELLOW_E, scale_factor=1.03), run_time=0.55)
        wait_for_chunks([9], spent=2.4)
        self.wait(self.WAIT_TAIL)


class Scene10_OnlineClassroomRCT(Scene):
    """
    Scene 10: 온라인 수업 RCT 사례

    Core Claim:
    실제 RCT 데이터(온라인 수업 실험)를 통해 단순 평균 차이 = ATE 직접 확인.
    대면 78.55 vs 온라인 73.64 → ATE ≈ -4.91점.
    무작위 배정이 선택 편향을 설계 단계에서 제거하기 때문에 인과 해석 가능.

    Expected Misconception:
    "온라인 학생이 원래 더 우수/열등할 수 있다"는 선택 편향 우려.
    RCT는 설계 단계에서 이를 제거하므로 단순 평균 차이 = ATE.

    Notebook Reference:
    book/why_causal_inference/why_causal_inference_ko.ipynb
    - 직전 Scene 마지막 문장:
      "무작위 배정 하나로, 비교 가능성의 두 조건을 동시에 확보할 수 있습니다."
    - 현재 Scene 첫 문장:
      "실제 데이터로 확인해 볼게요."
    - Cell 22: 온라인 수업 실험 소개 (대면/온라인/혼합 무작위 배정)
    - Cell 23-24: face_to_face=78.55, blended=77.09, online=73.64
    - Cell 25: ATE≈-4.91, 균형 검증 (gender/asian/black/hispanic/white)

    Script-to-Beat Mapping:
    - Beat 1: chunk 1 (0-1.8s) + chunk 2 (1.8-11.2s) → 실험 소개 타이틀
    - Beat 2: chunk 3 (11.2-26.1s) → 세 수업 방식 카드 + 무작위 배정
    - Beat 3: chunk 4 (26.1-50.7s) → 선택 편향 문제 + RCT 해결
    - Beat 4: chunk 5 (50.7-56.6s) + chunk 6 (56.6-72.4s) + chunk 7 (72.4-83.9s) → 결과 표 + ATE
    - Beat 5: chunk 8 (83.9-110.9s) → 균형 검증 표
    """

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

        # ── Beat 1: 실험 소개 — 아이콘으로 T/Y 시각화 (chunk 1-2, 11.05s) ──────
        # 남는: 없음 / 새로: title, T 아이콘 3개+레이블, 화살표, Y 아이콘+레이블
        # 핵심: "처치 T = 수업 방식 → 결과 Y = 기말 점수" 관계
        title = Text("온라인 수업 실험", font_size=40, color=WHITE)
        title.move_to(UP * 2.0)

        # T 섹션: 처치 T 헤더 + 수업방식 아이콘 3개
        t_header = Text("처치  T", font_size=22, color=NEUTRAL_COLOR)
        icon_f1 = load_icon("school.svg", FACE_COLOR, 0.5)
        icon_b1 = load_icon("devices.svg", BLEND_COLOR, 0.5)
        icon_o1 = load_icon("device-desktop.svg", ONLINE_COLOR, 0.5)
        lbl_f1 = Text("대면", font_size=16, color=FACE_COLOR)
        lbl_b1 = Text("혼합", font_size=16, color=BLEND_COLOR)
        lbl_o1 = Text("온라인", font_size=16, color=ONLINE_COLOR)
        col_f1 = VGroup(icon_f1, lbl_f1).arrange(DOWN, buff=0.1)
        col_b1 = VGroup(icon_b1, lbl_b1).arrange(DOWN, buff=0.1)
        col_o1 = VGroup(icon_o1, lbl_o1).arrange(DOWN, buff=0.1)
        t_icons = VGroup(col_f1, col_b1, col_o1).arrange(RIGHT, buff=0.35)
        t_section = VGroup(t_header, t_icons).arrange(DOWN, buff=0.28)
        t_section.move_to(LEFT * 2.8 + DOWN * 0.3)

        # Y 섹션: 결과 Y 헤더 + 체크리스트 아이콘 + 레이블
        y_header = Text("결과  Y", font_size=22, color=NEUTRAL_COLOR)
        icon_y = load_icon("checklist.svg", ACCENT_COLOR, 0.55)
        lbl_y = Text("기말 시험 점수", font_size=16, color=ACCENT_COLOR)
        y_col = VGroup(icon_y, lbl_y).arrange(DOWN, buff=0.1)
        y_section = VGroup(y_header, y_col).arrange(DOWN, buff=0.28)
        y_section.move_to(RIGHT * 2.5 + DOWN * 0.3)

        # T → Y 화살표
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

        # ── Beat 2: 세 수업 방식 카드 (chunk 3, 14.9s) ───────────────────────
        # 남는: title(상단 축소) / 제거: ty_labels / 새로: 카드 3개 + RCT 배지→화살표
        # 핵심: 대면/혼합/온라인 카드

        def make_format_card(icon, label, color):
            lbl = Text(label, font_size=24, color=color)
            grp = VGroup(icon, lbl).arrange(DOWN, buff=0.2)
            rect = SurroundingRectangle(
                grp, buff=0.25, color=color,
                stroke_opacity=0.7, fill_opacity=0.06, fill_color=color,
            )
            return VGroup(rect, grp)

        card_f = make_format_card(icon_face, "대면", FACE_COLOR)
        card_b = make_format_card(icon_blend, "혼합", BLEND_COLOR)
        card_o = make_format_card(icon_online, "온라인", ONLINE_COLOR)
        cards = VGroup(card_f, card_b, card_o).arrange(RIGHT, buff=0.55)
        cards.move_to(ORIGIN)

        rct_badge = Text("무작위 배정", font_size=22, color=ACCENT_COLOR)
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

        # ── Beat 2 Phase 2: "처치는 수업 방식, 결과는 기말 점수" (chunk 3 후반) ──
        # 카드 좌측 축소 이동 + 우측에 T→Y 다이어그램 등장
        # chunk 3 = 16.02s, phase1 spent ≈ 1.8s → 나머지 ~9s 대기 후 전환
        self.wait(8.5)

        # rct_badge/arr FadeOut 후 카드 축소+이동, Y 섹션 등장
        t_lbl = Text("처치  T", font_size=21, color=NEUTRAL_COLOR)
        icon_y2 = load_icon("checklist.svg", ACCENT_COLOR, 0.6)
        y_lbl2 = Text("기말 시험 점수", font_size=18, color=ACCENT_COLOR)
        y_hdr2 = Text("결과  Y", font_size=21, color=NEUTRAL_COLOR)
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
        # spent(chunk3): 0.55+1.0+0.8+8.5+0.65+0.4+0.7 = 12.6s → wait 16.02-12.6 = 3.42s
        wait_for_chunks([3], spent=12.6)

        # ── Beat 3: 선택 편향 문제 → RCT 해결 (chunk 4, 23.87s) ──────────────
        # 남는: 없음 (모두 FadeOut) / 핵심: 선택 편향 DAG → 무작위 배정이 차단
        # 이 Beat 시작은 chunk 4 시작 시점 (0.5s FadeOut 포함)
        self.play(
            FadeOut(cards), FadeOut(t_lbl), FadeOut(ty_mid_arr), FadeOut(y_sec2), FadeOut(title),
            run_time=0.5,
        )

        # DAG 노드 헬퍼: SurroundingRectangle + 텍스트
        def dag_node(label, color, fsize=22):
            txt = Text(label, font_size=fsize, color=color)
            box = SurroundingRectangle(txt, buff=0.22, color=color, stroke_opacity=0.8,
                                       fill_color=color, fill_opacity=0.08)
            return VGroup(box, txt)

        node_bg = dag_node("학생 배경", QUESTION_COLOR)       # 교란변수 (상단 중앙)
        node_T  = dag_node("수업 방식 T", ONLINE_COLOR)       # 처치 (좌하단)
        node_Y  = dag_node("성적 Y", ACCENT_COLOR)            # 결과 (우하단)

        node_bg.move_to(UP * 1.5)
        node_T.move_to(LEFT * 3.0 + DOWN * 0.8)
        node_Y.move_to(RIGHT * 3.0 + DOWN * 0.8)

        # 화살표 3개: 배경→T (교란 경로), 배경→Y, T→Y (인과)
        def dag_arrow(src, dst, color, stroke=2.2):
            return Arrow(
                src.get_boundary_point(dst.get_center() - src.get_center()),
                dst.get_boundary_point(src.get_center() - dst.get_center()),
                buff=0.08, stroke_width=stroke, color=color,
                max_tip_length_to_length_ratio=0.12,
            )

        arr_bg_T = dag_arrow(node_bg, node_T, QUESTION_COLOR)   # 교란 경로 (나중에 X)
        arr_bg_Y = dag_arrow(node_bg, node_Y, QUESTION_COLOR)
        arr_T_Y  = dag_arrow(node_T,  node_Y, NEUTRAL_COLOR)

        # 교란 경로 라벨: "배경 → 수업 선택"
        conf_label = Text("자기주도? 저소득?", font_size=18, color=QUESTION_COLOR)
        conf_label.next_to(arr_bg_T, LEFT, buff=0.08)

        # X 마크 (교란 경로 차단) + RCT 설명
        cross = Text("✕", font_size=38, color=ACCENT_COLOR)
        cross.move_to(arr_bg_T.get_center())
        rct_cut = Text("무작위 배정이 이 경로를 차단합니다", font_size=21, color=ACCENT_COLOR)
        rct_cut.move_to(DOWN * 2.5)

        bq = Text("무작위 배정 없었다면?", font_size=28, color=ACCENT_COLOR)
        bq.move_to(UP * 3.0)

        # Beat 3 애니메이션: DAG 구축 → 교란 경로 강조 → 차단
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
        # 교란 경로 강조 (빨갛게 Indicate)
        self.play(Indicate(arr_bg_T, color=RED_D, scale_factor=1.1), run_time=0.7)
        self.wait(5.0)
        # RCT가 교란 경로 차단
        self.play(
            arr_bg_T.animate.set_opacity(0.25),
            conf_label.animate.set_opacity(0.25),
            run_time=0.5,
        )
        self.play(FadeIn(cross, scale=0.5), run_time=0.5)
        self.play(FadeIn(rct_cut, shift=UP * 0.05), run_time=0.6)
        # spent(chunk4): 0.5+0.6+2.0+0.9+0.8+0.5+4.0+0.7+5.0+0.5+0.5+0.6 = 16.6s
        wait_for_chunks([4], spent=16.6)

        # ── Beat 4: 결과 표 + ATE (chunk 5-7, 33.2s) ─────────────────────────
        # 남는: 없음 / 새로: 결과 표(3행×2열) + ATE 수식
        # 핵심: 78.55 vs 73.64, ATE≈−4.91
        self.play(
            FadeOut(bq), FadeOut(node_bg), FadeOut(node_T), FadeOut(node_Y),
            FadeOut(arr_bg_T), FadeOut(arr_bg_Y), FadeOut(arr_T_Y),
            FadeOut(conf_label), FadeOut(cross), FadeOut(rct_cut),
            run_time=0.5,
        )

        # 고정 열 x 좌표 (2열: 수업방식 | 평균점수)
        col_xs = [-1.8, 1.4]
        row_ys = [1.6, 0.7, -0.1, -0.9]
        res_data = [
            ("수업 방식", "평균 점수"),
            ("대면",     "78.55"),
            ("혼합",     "77.09"),
            ("온라인",   "73.64"),
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

        ate_eq = VGroup(
            MathTex(r"\widehat{ATE} = 78.55 - 73.64 \approx -4.91", font_size=30).set_color(WHITE),
            Text("점", font_size=28, color=WHITE),
        ).arrange(RIGHT, buff=0.05)
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
        # chunk 5: 에이티이 추정 방법 간단 (5.9s)
        wait_for_chunks([5], spent=0.5 + 0.7 + 0.9)  # FadeOut + 표 표시

        self.play(FadeIn(ate_eq, shift=UP * 0.05), run_time=0.7)
        self.play(Indicate(ate_eq, color=ACCENT_COLOR, scale_factor=1.06), run_time=0.6)
        # chunk 6: 수치 결과 (15.7s)
        wait_for_chunks([6], spent=1.3)

        # chunk 7: 걱정 불필요 — 결과 표에서 두 값 Indicate
        self.play(Indicate(VGroup(*res_cells[2:4]), color=FACE_COLOR, scale_factor=1.06), run_time=0.5)
        self.play(Indicate(VGroup(*res_cells[6:8]), color=ONLINE_COLOR, scale_factor=1.06), run_time=0.5)
        # chunk 7: 11.5s
        wait_for_chunks([7], spent=1.0)

        # ── Beat 5: 균형 검증 표 (chunk 8, 27.1s) ────────────────────────────
        # 남는: 없음 / 새로: 균형 검증 표(6행×5열)
        # 핵심: 흑인계(△) — 소규모 표본의 한계
        self.play(
            FadeOut(res_table), FadeOut(divider), FadeOut(ate_eq),
            run_time=0.5,
        )

        bal_title = Text("무작위화 균형 검증", font_size=24, color=NEUTRAL_COLOR)
        bal_title.move_to(UP * 2.8)

        # 5열: 변수 | 대면 | 혼합 | 온라인 | 균형
        col_xs_b = [-3.1, -1.5, -0.6, 0.3, 1.2]
        row_ys_b = [2.0, 1.3, 0.6, -0.1, -0.8, -1.5]
        bal_data = [
            ("변수",    "대면",  "혼합",  "온라인", ""),
            ("성별",    "0.63", "0.55", "0.54",  "✓"),
            ("아시아계", "0.20", "0.22", "0.23",  "✓"),
            ("흑인계",  "0.07", "0.10", "0.03",  "△"),
            ("히스패닉", "0.01", "0.01", "0.03",  "✓"),
            ("백인",    "0.72", "0.63", "0.70",  "✓"),
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
                elif r == 3:   # 흑인계 행 경고색
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
            "소규모 표본에서는 우연한 불균형이 생길 수 있다",
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
        # chunk 8: 27.1s, spent = 0.5(FadeOut)+0.5+0.6+1.2+0.6+0.6 = 4.0s
        wait_for_chunks([8], spent=4.0)
        self.wait(self.WAIT_TAIL)


class Scene11_RctLimitsAndBeyond(Scene):
    """
    RCT의 한계와 준실험 방법론 소개

    직전 Scene (Scene10) 마지막: 무작위화 균형 검증 표
    현재 Scene 첫 문장: "알씨티는 간단하면서도 강력한 방법입니다."

    ipynb 범위: RCT 한계 섹션 ~ 준실험 방법론 목록

    핵심 주장: RCT는 강력하지만 현실적 제약이 있다.
               준실험 방법론들이 그 대안이다.
    오해 교정: 관찰 연구도 조건을 충족하면 인과 추론이 가능하다.
    visual pivot:
    - Beat 1: 좌우 분할 프레임(RCT ✓ vs 현실 ✗) — mlp.py MLPStepsPreview 패턴
    - Beat 2: 아이콘 팝업(비용/윤리/정책) + 흡연 예시 — med_test.py 순차 등장
    - Beat 3: 이상적 실험 질문 박스 → 관찰 연구 기준점
    - Beat 4: DAG 단계 빌드업 (①T→Y ②X 등장·문제 ③X 제어·해결)
    - Beat 5: 방법론 5개 계단 배치 (좌상→우하)
    - Beat 6: 카드 opacity 0.2 + 목표 텍스트 강조 — embedding.py 패턴

    Beat별 script-to-beat mapping:
    - Beat 1 (chunk 1, 6.3s): "알씨티는 강력하지만 항상 가능하지는 않습니다"
    - Beat 2 (chunk 2, 15.3s): 세 가지 한계 아이콘 + 흡연 예시 패널
    - Beat 3 (chunk 3, 11.8s): 이상적 실험 질문 박스 → 관찰 연구 기준점
    - Beat 4 (chunk 4, 18.3s): DAG 3단계 빌드업
    - Beat 5 (chunk 5, 11.1s): 방법론 5개 계단 배치
    - Beat 6 (chunk 6, 6.9s): 카드 dim + 비교 가능성 목표 강조
    """

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

        # ── Beat 1: 좌우 분할 프레임 — RCT ✓ vs 현실 ✗ (chunk 1, 6.3s) ───────
        # mlp.py MLPStepsPreview: 수직선으로 두 패널 나눠 대비
        # 남는: 없음 / 새로: 분할선 + 좌(RCT✓) + 우(현실✗) / 핵심: 좌우 대비
        divider = Line(
            UP * 3.8, DOWN * 3.8,
            stroke_width=1.5, color=NEUTRAL_COLOR, stroke_opacity=0.45,
        )

        rct_lbl = Text("RCT", font_size=60, color=GREEN_D, weight=BOLD)
        rct_check = Text("✓", font_size=52, color=GREEN_D)
        rct_sub = Text("이상적 설계", font_size=20, color=GREEN_D)
        rct_left_grp = VGroup(rct_lbl, rct_check, rct_sub).arrange(DOWN, buff=0.22)
        rct_left_grp.move_to(LEFT * 3.2)

        real_lbl = Text("현실에서는", font_size=34, color=WHITE)
        real_cross = Text("✗", font_size=52, color=RED_D)
        real_sub = Text("항상 가능하지 않다", font_size=20, color=NEUTRAL_COLOR)
        rct_right_grp = VGroup(real_lbl, real_cross, real_sub).arrange(DOWN, buff=0.22)
        rct_right_grp.move_to(RIGHT * 3.2)

        self.play(Create(divider), run_time=0.5)
        self.play(
            FadeIn(rct_left_grp, shift=RIGHT * 0.12),
            FadeIn(rct_right_grp, shift=LEFT * 0.12),
            run_time=0.7,
        )
        # chunk 1: 6.3s, spent = 0.5 + 0.7 = 1.2s
        wait_for_chunks([1], spent=1.2)

        # ── Beat 2: 한계 아이콘 팝업 + 흡연 예시 (chunk 2, 15.3s) ─────────────
        # med_test.py NewContrastThreeContexts: 3개 항목 순차 등장 패턴
        # 제거: divider + 좌우 / 새로: 아이콘 3개(팝업) + 흡연 패널 / 핵심: 아이콘 순차
        self.play(
            FadeOut(divider), FadeOut(rct_left_grp), FadeOut(rct_right_grp),
            run_time=0.5,
        )

        icons_meta = [
            ("coin.svg",          COST_COLOR,   "비용 과다",    "대규모 임상 수십억 원",    LEFT * 3.8),
            ("scale.svg",         ETHICS_COLOR, "윤리 제약",    "흡연·무기 노출 배정 불가",  ORIGIN),
            ("building-bank.svg", POLICY_COLOR, "정책 통제",    "국가 단위 무작위 배정 불가", RIGHT * 3.8),
        ]

        icon_cols_grp = VGroup()
        for icon_file, color, title, desc, pos in icons_meta:
            icon = load_icon(icon_file, color, 1.1)
            title_txt = Text(title, font_size=21, color=color, weight=BOLD)
            desc_txt = Text(desc, font_size=17, color=NEUTRAL_COLOR)
            col = VGroup(icon, VGroup(title_txt, desc_txt).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.28)
            col.move_to(pos + UP * 0.4)
            icon_cols_grp.add(col)

        # 아이콘 순차 팝업 (scale=0.82: 약간 작게서 커지는 느낌)
        for col in icon_cols_grp:
            self.play(FadeIn(col, scale=0.82), run_time=0.8)
            self.wait(0.3)

        # "가령 임산부에게" 직전 (~chunk 2의 7.5s 지점) — 흡연 예시 패널
        no_smoking = load_icon("smoking-no.svg", RED_D, 0.65)
        smoke_txt = Text("임산부에게 흡연 무작위 배정 불가", font_size=19, color=NEUTRAL_COLOR)
        smoking_row = VGroup(no_smoking, smoke_txt).arrange(RIGHT, buff=0.3)
        smoking_box_rect = SurroundingRectangle(
            smoking_row, buff=0.24, color=NEUTRAL_COLOR,
            stroke_width=1.2, corner_radius=0.1, stroke_opacity=0.45,
        )
        smoking_panel = VGroup(smoking_box_rect, smoking_row)
        smoking_panel.move_to(DOWN * 2.3)

        self.wait(3.5)
        self.play(FadeIn(smoking_panel, shift=UP * 0.06), run_time=0.6)
        # chunk 2: 15.3s, spent = 0.5 + 3*(0.8+0.3) + 3.5 + 0.6 = 7.9s
        wait_for_chunks([2], spent=7.9)

        # ── Beat 3: 이상적 실험 사고 실험 (chunk 3, 11.8s) ──────────────────
        # 제거: 아이콘 그룹 + 흡연 패널 / 새로: 질문 박스 + 기준점 / 핵심: 질문 박스
        self.play(FadeOut(icon_cols_grp), FadeOut(smoking_panel), run_time=0.5)

        question_txt = Text(
            '"이상적인 실험이라면 어떻게 설계할까?"',
            font_size=26, color=ACCENT_COLOR,
        )
        question_box = SurroundingRectangle(
            question_txt, buff=0.3, color=ACCENT_COLOR,
            corner_radius=0.12, stroke_width=1.8,
        )
        question_grp = VGroup(question_box, question_txt)
        question_grp.move_to(UP * 0.6)

        anchor_txt = Text("관찰 연구 설계의 기준점", font_size=22, color=WHITE)
        anchor_txt.next_to(question_grp, DOWN, buff=0.55)
        anchor_arr = Arrow(
            question_grp.get_bottom() + DOWN * 0.08,
            anchor_txt.get_top() + UP * 0.08,
            stroke_width=2.5, color=NEUTRAL_COLOR, buff=0,
            max_tip_length_to_length_ratio=0.3,
        )

        self.play(FadeIn(question_grp, shift=UP * 0.08), run_time=0.7)
        self.play(GrowArrow(anchor_arr), FadeIn(anchor_txt, shift=UP * 0.05), run_time=0.6)
        # chunk 3: 11.8s, spent = 0.5 + 0.7 + 0.6 = 1.8s
        wait_for_chunks([3], spent=1.8)

        # ── Beat 4: 준실험 개념 DAG 3단계 빌드업 (chunk 4, 18.3s) ────────────
        # mlp.py LaggedStartMap(GrowArrow): 화살표 단계별 등장으로 인과 이야기 구축
        # 제거: 질문 박스 → 새로: ①T→Y ②X 등장(문제) ③X 제어(해결)
        # 핵심: 각 단계에서 바뀌는 화살표 색/opacity
        self.play(
            FadeOut(question_grp), FadeOut(anchor_arr), FadeOut(anchor_txt),
            run_time=0.5,
        )

        quasi_title = Text("준실험 방법론", font_size=28, color=WHITE, weight=BOLD)
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

        node_T = q_node("처치 T", GOLD_D)
        node_Y = q_node("결과 Y", TEAL_D)
        node_T.move_to(LEFT * 2.6 + UP * 0.2)
        node_Y.move_to(RIGHT * 2.6 + UP * 0.2)

        # get_right/get_left + 동일 y 좌표 고정 → 완전 수평 화살표
        ty_y = node_T.get_center()[1]  # 두 노드 동일 y (UP * 0.2)
        arr_T_Y = Arrow(
            [node_T.get_right()[0], ty_y, 0],
            [node_Y.get_left()[0], ty_y, 0],
            buff=0, stroke_width=3.0, color=ACCENT_COLOR,
            max_tip_length_to_length_ratio=0.25,
        )
        goal_lbl = Text("알고 싶은 인과 효과", font_size=17, color=NEUTRAL_COLOR)
        goal_lbl.next_to(arr_T_Y, DOWN, buff=0.2)

        # ① T→Y: "이게 알고 싶은 인과 관계"
        self.play(FadeIn(quasi_title), run_time=0.4)
        self.play(FadeIn(node_T), FadeIn(node_Y), run_time=0.6)
        self.play(Create(arr_T_Y), FadeIn(goal_lbl), run_time=0.6)
        self.wait(3.0)  # 오디오: "알씨티처럼 처치가 잠재적 결과와 독립이라는..."

        # ② 교란변수 X 등장 — 관찰 연구의 문제
        node_X = q_node("교란 변수 X", QUESTION_COLOR, fsize=18)
        node_X.move_to(UP * 2.0)
        arr_X_T = q_arrow(node_X, node_T, QUESTION_COLOR)
        arr_X_Y = q_arrow(node_X, node_Y, QUESTION_COLOR)
        problem_lbl = Text("교란 변수가 처치와 결과 모두에 영향", font_size=18, color=QUESTION_COLOR)
        problem_lbl.move_to(DOWN * 1.5)

        self.play(FadeIn(node_X, shift=DOWN * 0.1), run_time=0.5)
        self.play(
            LaggedStart(Create(arr_X_T), Create(arr_X_Y), lag_ratio=0.4),
            run_time=0.7,
        )
        self.play(FadeIn(problem_lbl, shift=UP * 0.05), run_time=0.5)
        self.wait(3.5)  # 오디오: "어떤 공변량을 통제하면 처치가 사실상..."

        # ③ 교란 경로 제어 — 준실험의 해결
        midpt = (node_X.get_center() + node_T.get_center()) / 2
        ctrl_lbl = Text("통 제", font_size=17, color=NEUTRAL_COLOR)
        ctrl_lbl.move_to(midpt + RIGHT * 0.5)
        solution_lbl = Text("처치가 사실상 무작위처럼 보이도록", font_size=20, color=ACCENT_COLOR)
        solution_lbl.move_to(DOWN * 1.5)

        self.play(
            arr_X_T.animate.set_stroke(color=NEUTRAL_COLOR, opacity=0.25),
            arr_X_Y.animate.set_stroke(color=NEUTRAL_COLOR, opacity=0.25),
            FadeOut(problem_lbl),
            run_time=0.7,
        )
        self.play(FadeIn(ctrl_lbl), run_time=0.4)
        self.play(FadeIn(solution_lbl, shift=UP * 0.05), run_time=0.5)
        # chunk 4: 18.3s, spent = 0.5+0.4+0.6+0.6+3.0+0.5+0.7+0.5+3.5+0.7+0.4+0.5 = 11.9s
        wait_for_chunks([4], spent=11.9)

        # ── Beat 5: 방법론 5개 — 2행 그리드 3+2 (chunk 5, 11.1s) ──────────────
        # 제거: 준실험 DAG 전체 / 새로: 상단 3개 + 하단 2개 그리드 / 핵심: 카드 배치
        beat4_all = VGroup(
            quasi_title, node_T, node_Y, arr_T_Y, goal_lbl,
            node_X, arr_X_T, arr_X_Y, ctrl_lbl, solution_lbl,
        )
        self.play(FadeOut(beat4_all), run_time=0.5)

        method_header = Text("앞으로 다룰 방법론들", font_size=22, color=NEUTRAL_COLOR)
        method_header.move_to(UP * 2.2)

        method_names = ["매칭", "이중차분법", "합성통제법", "도구변수", "회귀불연속"]
        method_colors = [BLUE_D, GREEN_D, GOLD_D, MAROON_D, TEAL_D]

        def make_method_card(name, color):
            txt = Text(name, font_size=18, color=color)
            box = RoundedRectangle(
                width=2.1, height=0.9, corner_radius=0.12,
                color=color, stroke_width=1.8,
            )
            box.set_fill(color=color, opacity=0.08)
            txt.move_to(box.get_center())
            return VGroup(box, txt)

        cards = VGroup(*[make_method_card(n, c) for n, c in zip(method_names, method_colors)])
        # 2행 그리드: 상단 3개(x=-3,0,3 / y=0.0), 하단 2개(x=-1.5,1.5 / y=-1.1)
        grid_pos = [(-3.0, 0.0), (0.0, 0.0), (3.0, 0.0), (-1.5, -1.1), (1.5, -1.1)]
        for card, (x, y) in zip(cards, grid_pos):
            card.move_to([x, y, 0])

        self.play(FadeIn(method_header), run_time=0.4)
        # 상단 3개 먼저, 하단 2개 이어서
        self.play(
            LaggedStart(*[FadeIn(cards[i], shift=UP * 0.08) for i in range(3)], lag_ratio=0.25),
            run_time=1.0,
        )
        self.play(
            LaggedStart(*[FadeIn(cards[i], shift=UP * 0.08) for i in range(3, 5)], lag_ratio=0.3),
            run_time=0.7,
        )
        # chunk 5: 11.1s, spent = 0.5+0.4+1.0+0.7 = 2.6s
        wait_for_chunks([5], spent=2.6)

        # ── Beat 6: 카드 opacity 0.2 + 목표 텍스트 강조 (chunk 6, 6.9s) ───────
        # embedding.py: 비포커스 항목 opacity 0.2, 핵심 목표만 선명하게
        # 카드·헤더: opacity 0.2(유지) / 새로: 목표 텍스트(카드 위 여백) / 핵심: 목표
        self.play(
            cards.animate.set_opacity(0.2),
            method_header.animate.set_opacity(0.2),
            run_time=0.6,
        )

        # 새 스크립트: "방법은 달라도 목표는 하나입니다. 두 집단을 비교 가능하게 만드는 것."
        goal_line1 = Text("방법은 달라도 목표는 하나입니다.", font_size=28, color=WHITE, weight=BOLD)
        goal_line2 = Text(
            "두 집단을 비교 가능하게 만드는 것.",
            font_size=21, color=ACCENT_COLOR,
        )
        goal_grp = VGroup(goal_line1, goal_line2).arrange(DOWN, buff=0.3)
        goal_grp.move_to(UP * 1.4)  # 상단 카드(y=0.0, top≈0.45) 위 여백

        self.play(FadeIn(goal_grp, shift=UP * 0.06), run_time=0.6)
        # chunk 6: 9.94s, spent = 0.6 + 0.6 = 1.2s
        wait_for_chunks([6], spent=1.2)

        # ── Beat 7: 에필로그 — 자연스러운 페이드아웃 ──
        # dim 상태 그대로 머물렀다가 부드럽게 페이드아웃 — 갑작스러운 밝아짐 없이
        self.wait(1.5)
        self.play(
            FadeOut(VGroup(cards, method_header, goal_grp)),
            run_time=2.5,
        )
        self.wait(self.WAIT_TAIL)
