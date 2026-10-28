"""ATE에서 CATE, 프로모션 타기팅까지: 승인된 단일 스크립트의 영상."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from manim import *


TOPIC = Path(__file__).resolve().parents[1]
REPO = TOPIC.parents[1]
ICONS = REPO / "videos/assets/tabler-icons/icons/outline"
FONT = "Apple SD Gothic Neo"
BG = "#0B1018"
INK = "#F0F3F8"
MUTED = "#A4B0C3"
RULE = "#304157"
TREAT = "#57D6BB"
CONTROL = "#8F9EB3"
GROUP_A = "#78B6FF"
GROUP_B = "#F4A98C"
EFFECT = "#FFD477"


def label(text, size=30, color=INK, **kwargs):
    return Text(text, font=FONT, font_size=size, color=color, **kwargs)


def icon(name, color=INK, height=0.8):
    return (
        SVGMobject(str(ICONS / f"{name}.svg"))
        .set_fill(opacity=0)
        .set_stroke(color, width=2.6)
        .set_height(height)
    )


def customers(count=20, columns=10, colors=None, spacing=0.32, radius=0.09):
    marks = VGroup(
        *[
            Dot(radius=radius, color=colors[i] if colors else MUTED)
            for i in range(count)
        ]
    )
    marks.arrange_in_grid(cols=columns, buff=spacing - 2 * radius)
    return marks


class Scene01_AteToCate(Scene):
    """
    Scene 01 개정: 평균 효과 확인 → 투자 대비 이익 최대화 → CATE 기반 타기팅.

    원본: src/scripts/ko/01_ate_to_cate.txt 전체 8문단. ipynb는 만들지 않는다.
    첫 문장: '프로모션을 하면, 평균적으로 효과가 있을까요?'
    마지막 문장: '씨에이티이를 활용해 이익을 높일 대상을 선택합니다.'
    직전 Scene 없음. 승인된 기존 영상에 대한 사용자의 흐름 수정 요청을 반영한다.
    데이터: A/B 각 50%, 비용 반영 예상 추가 이익 2,000/8,000원,
    전체 ATE 5,000원. 동일 비용 100명 선택 시 50만/80만 원. 모두 가상 예시다.
    CATE는 특성별 평균 효과이며 각 개인의 실제 효과를 관측한 것으로 묘사하지 않는다.

    논문: Zou, Du, Lee & Pedersen (2020), arXiv:2004.09702.
    §2.1 Eq.(1): CATE; §3 Eq.(4): 성과/비용과 예산을 고려한 대상 선택;
    §3.4: 같은 투자에서 추가 성과 비교; §4.1.1: 이전 무작위 실험 데이터 활용.
    논문은 예산 아래 추가 고객 유지/성과 극대화 문제다. 영상의 추가 이익 예시는
    그 의사결정 관점을 설명하기 위한 것이며, 논문의 수익률/실험 결과가 아니다.
    마지막 화면의 저자·제목·링크는 src/references.json에서 읽는다.
    시각 참조: 3b1b/_2023/clt/main.py의 get_mean_labels/realign_distributions.
    선택 이유: 다른 집단의 색을 유지하면서 전체 평균을 기준선으로 나타내는 전환.
    기존 영상에서 A/B 색과 100개 점의 화면 문법만 이어받고 불필요한 도식은 제거한다.

    타이밍: ElevenLabs 문자별 정렬. 문단→Beat:
    1 ATE의 질문, 2 현업의 목표, 3 CATE, 4 추가 이익 예시,
    5 타기팅 비교, 6 쿠폰 할인액 차이, 7 우버의 고객 유지 마케팅, 8 정리.
    하단 상시 문구를 넣지 않는다. 참고 문헌에는 서지 정보만 제시한다.
    실행: .venv/bin/manim -ql --media_dir videos/uplift_modeling/build/manim \
        videos/uplift_modeling/src/uplift_modeling_ko.py Scene01_AteToCate
    """

    def construct(self):
        # 실제 출력 프레임으로 시간을 계산해 캐시 재사용 시의 누적 시간차를 막는다.
        config.disable_caching = True
        self.camera.background_color = BG
        self.timing = json.loads((TOPIC / "build/audio/01_ate_to_cate.timings.json").read_text())
        script = (TOPIC / "src/scripts/ko/01_ate_to_cate.txt").read_bytes()
        if hashlib.sha256(script).hexdigest() != self.timing["scriptSha256"]:
            raise ValueError("수정 스크립트와 음성의 타이밍이 일치하지 않습니다.")
        reference = json.loads((TOPIC / "src/references.json").read_text())["primary"]
        self.events, self.content = [], []
        self.heading = label("ATE가 답하는 질문", 38).move_to(UP * 3.15)
        self.rule = Line(LEFT * 6.25 + UP * 2.66, RIGHT * 6.25 + UP * 2.66,
                         color=RULE, stroke_width=1.3)
        self.add(self.heading, self.rule)

        # 1. 남는 요소: 제목. 새 요소: 중앙 ATE와 질문 한 덩어리.
        # 핵심 그룹 1개. 좌우와 하단은 비우고 '평균적으로 효과가 있는가'만 읽는다.
        ate = VGroup(label("ATE", 76, EFFECT),
                     label("프로모션이 평균적으로 효과가 있을까?", 38),
                     label("평균 처치 효과", 28, MUTED)).arrange(DOWN, buff=0.48)
        self.show(0.15, ate)
        self.at(self.when(1, "평균적으로 결과"), Indicate(ate[1], color=EFFECT), run_time=0.8)
        self.at(self.when(1, "에이티이"), Indicate(ate[0], color=EFFECT), run_time=0.7)

        # 2. ATE 정의 전체를 지우고 현업의 목표 한 덩어리만 중앙에 올린다.
        # 코인 위/목표 중/대상 질문 아래. 핵심 그룹 1개, 시선은 추가 이익 최대화.
        goal = VGroup(icon("coins", EFFECT, 0.9),
                      label("정해진 투자와 예산", 30, MUTED),
                      label("추가 이익 최대화", 53, TREAT)).arrange(DOWN, buff=0.42)
        self.stage(self.when(2), "현업에서는, 같은 투자로 더 큰 이익을", goal)
        target_question = label("누구에게 제공할까?", 34).move_to(DOWN * 2.2)
        self.show(self.when(2, "누구에게"), target_question)

        # 3. 목표 그림을 먼저 지운다. 중앙 CATE 정의 1개, 하단에 짧은 흐름 1개.
        # 한 번에 읽을 대상은 정의, 이어서 '실험 데이터 → 타기팅'이다.
        cate = VGroup(label("CATE", 76, EFFECT),
                      label("조건부 평균 처치 효과", 31),
                      label("고객 특성에 따른 평균 추가 이익", 31, MUTED))
        cate.arrange(DOWN, buff=0.45)
        self.stage(self.when(3), "이때 활용하는 것이 CATE", cate)
        learning = label("실험 데이터 → 효과 차이 학습 → 타기팅", 29, TREAT).move_to(DOWN * 2.35)
        self.show(self.when(3, "실험 데이터"), learning)

        # 4. 정의와 흐름을 모두 제거. 중앙 막대 비교 1개에 A/B를 순차 공개한다.
        # 왼쪽은 평균 주석용으로 비워 두고, 후반에 ATE 기준선을 연결한다.
        # 핵심 시선: A 2천 원 → B 8천 원 → 전체 평균 5천 원.
        share = label("A 50% · B 50%", 24, MUTED).move_to(UP * 2.1)
        base_y, unit = -1.55, 0.00034
        baseline = Line([-3.25, base_y, 0], [4.1, base_y, 0], color=RULE)
        self.stage(self.when(4), "같은 프로모션, 다른 추가 이익", VGroup(share, baseline))
        a_bar = Rectangle(width=1.4, height=2000 * unit, stroke_width=0,
                          fill_color=GROUP_A, fill_opacity=0.9).move_to([-1.6, base_y + 1000 * unit, 0])
        b_bar = Rectangle(width=1.4, height=8000 * unit, stroke_width=0,
                          fill_color=GROUP_B, fill_opacity=0.9).move_to([2.2, base_y + 4000 * unit, 0])
        a = VGroup(a_bar, label("A 유형", 29, GROUP_A).next_to(a_bar, DOWN, buff=0.28),
                   label("+2,000원", 35, GROUP_A).next_to(a_bar, UP, buff=0.22))
        b = VGroup(b_bar, label("B 유형", 29, GROUP_B).next_to(b_bar, DOWN, buff=0.28),
                   label("+8,000원", 35, GROUP_B).next_to(b_bar, UP, buff=0.22))
        self.show(self.when(4, "에이는"), a, grow=a_bar)
        self.show(self.when(4, "비는"), b, grow=b_bar)
        mean_y = base_y + 5000 * unit
        mean_line = DashedLine([-3.15, mean_y, 0], [4.05, mean_y, 0],
                               color=EFFECT, stroke_width=2.5, dash_length=0.13)
        mean = VGroup(label("ATE", 28, EFFECT), label("+5,000원", 31, EFFECT))
        mean.arrange(DOWN, buff=0.16).move_to([-4.8, mean_y, 0])
        self.show(self.when(4, "전체 평균 효과"), VGroup(mean_line, mean))
        self.at(self.when(4, "어느 고객"), Indicate(a[2], color=GROUP_A),
                Indicate(b[2], color=GROUP_B), run_time=0.9)

        # 5. 평균 기준선과 막대를 먼저 제거. 같은 비용/인원 제약 한 줄 뒤에 두 정책 비교.
        # 좌/우 두 그룹만 유지, 하단은 각 정책의 예상 추가 이익을 읽는 공간으로 쓴다.
        constraint = label("같은 예산 · 100명에게 제공", 40, EFFECT)
        self.stage(self.when(5), "같은 투자, 더 큰 이익", constraint)
        random_grid = customers(100, 10, colors=[GROUP_A] * 50 + [GROUP_B] * 50,
                                spacing=0.23, radius=0.065).move_to([-3.15, 0.1, 0])
        random_group = VGroup(random_grid,
                              label("무작위 100명", 31).move_to([-3.15, 1.9, 0]),
                              label("기대 구성  A 50 · B 50", 22, MUTED).move_to([-3.15, -1.45, 0]))
        self.stage(self.when(5, "무작위로"), "같은 비용으로 100명에게 제공", random_group)
        random_value = label("+50만 원", 48, EFFECT).move_to([-3.15, -2.45, 0])
        self.show(self.when(5, "오십만 원"), random_value)
        targeted_grid = customers(100, 10, colors=[GROUP_B] * 100,
                                  spacing=0.23, radius=0.065).move_to([3.15, 0.1, 0])
        targeted_group = VGroup(targeted_grid,
                                label("B 유형 100명", 31, GROUP_B).move_to([3.15, 1.9, 0]),
                                label("추가 이익이 큰 고객 우선", 22, MUTED).move_to([3.15, -1.45, 0]))
        self.show(self.when(5, "비 유형 백 명"), targeted_group)
        targeted_value = label("+80만 원", 48, EFFECT).move_to([3.15, -2.45, 0])
        self.show(self.when(5, "팔십만 원"), targeted_value)
        self.at(self.when(5, "같은 투자로"), Circumscribe(targeted_value, color=TREAT, buff=0.18), run_time=1)

        # 6. 이전 타기팅 비교를 제거. 좌/우 쿠폰 2개로 할인액의 차이를 보여 준다.
        # 상단은 같은 추가 매출, 하단은 남는 이익 차이의 해석을 위한 공간으로 비워 둔다.
        # 핵심 시선은 3천 원 → 1만 원 → 할인 비용에 따른 이익의 차이다.
        small_coupon = icon("ticket", GROUP_A, 1.25).move_to(LEFT * 2.7 + UP * 0.25)
        large_coupon = icon("ticket", GROUP_B, 1.25).move_to(RIGHT * 2.7 + UP * 0.25)
        self.stage(self.when(6), "고객마다 쿠폰 할인액이 다를 수 있다",
                   VGroup(small_coupon, large_coupon))
        small_amount = label("3,000원 할인", 37, GROUP_A).next_to(small_coupon, DOWN, buff=0.45)
        large_amount = label("10,000원 할인", 37, GROUP_B).next_to(large_coupon, DOWN, buff=0.45)
        self.show(self.when(6, "삼천 원"), small_amount)
        self.show(self.when(6, "만 원"), large_amount)
        same_sales = label("같은 추가 매출", 30, MUTED).move_to(UP * 1.95)
        self.show(self.when(6, "같은 추가 매출"), same_sales)
        remaining = label("할인 비용 차이 → 남는 이익 차이", 32, TREAT).move_to(DOWN * 2.2)
        self.show(self.when(6, "할인에 쓴 돈"), remaining)

        # 7. 비용 예시 전체를 지운다. 승차 쿠폰 → 재이용의 단일 도식으로 우버 상황 제시.
        # 쿠폰은 고객 유지 문제를 이해하기 위한 예시이며, 실험/선택 흐름은 논문 §4.1.1.
        # 핵심 그룹 1개, 좌 쿠폰/우 자동차. 하단에는 필요한 두 라벨만 유지한다.
        coupon = icon("ticket", EFFECT, 1.2).move_to(LEFT * 3.05 + UP * 0.2)
        car = icon("car", TREAT, 1.25).move_to(RIGHT * 3.05 + UP * 0.2)
        reuse = VGroup(coupon, car,
                       Arrow(coupon.get_right(), car.get_left(), buff=0.5, color=MUTED),
                       label("승차 할인 쿠폰", 29, EFFECT).next_to(coupon, DOWN, buff=0.5),
                       label("서비스 재이용", 29, TREAT).next_to(car, DOWN, buff=0.5))
        self.stage(self.when(7), "우버 · 고객 유지 마케팅", reuse)

        # 쿠폰 그림을 먼저 지운 뒤 실험 데이터와 학습할 두 결과만 좌/우에 배치한다.
        # 핵심 그룹 2개. 읽을 대상은 효과와 비용이며 다른 성과 숫자를 새로 넣지 않는다.
        experiment = VGroup(customers(20, 10, colors=[CONTROL] * 10 + [TREAT] * 10),
                            label("무작위 혜택 실험", 29, MUTED)).arrange(DOWN, buff=0.5)
        experiment.move_to(LEFT * 3.1)
        outcomes = VGroup(label("추가 이용 효과", 35, TREAT),
                          label("혜택 비용", 35, EFFECT)).arrange(DOWN, buff=0.6).move_to(RIGHT * 2.75)
        learning_arrow = Arrow(LEFT * 1.15, RIGHT * 0.8, color=MUTED, buff=0.1)
        self.stage(self.when(7, "연구진은"), "실험 데이터로 효과와 비용을 학습한다",
                   VGroup(experiment, learning_arrow, outcomes))

        # 학습 도식 제거. 중앙 선택 결과 한 덩어리만 남겨 예산과 다음 캠페인을 연결한다.
        chosen = customers(20, 10, colors=[TREAT] * 8 + [RULE] * 12, spacing=0.4)
        decision = VGroup(label("정해진 예산", 29, MUTED), chosen,
                          label("추가 이용이 늘어날 고객 선택", 38, TREAT))
        decision.arrange(DOWN, buff=0.7)
        self.stage(self.when(7, "예산에 맞춰"), "다음 캠페인의 대상을 정한다", decision)

        # 8. 우버 도식을 지운 뒤 위 ATE/아래 CATE의 두 줄로 마무리한다.
        # 핵심 시선: 평균 효과 확인 → 이익을 높일 대상 선택. 하단 상시 문구는 없다.
        summary_ate = VGroup(label("ATE", 45, EFFECT), label("평균 효과 확인", 34))
        summary_ate.arrange(RIGHT, buff=0.75).move_to(UP * 0.75)
        summary_cate = VGroup(label("CATE", 45, EFFECT), label("이익을 높일 대상 선택", 34))
        summary_cate.arrange(RIGHT, buff=0.75).move_to(DOWN * 0.75)
        self.stage(self.when(8), "평균 효과에서 타기팅 결정으로", summary_ate)
        self.show(self.when(8, "씨에이티이"), summary_cate)

        # 마지막에는 요약을 지우고 제목/저자/연도/링크로 이루어진 참고 문헌 하나만 제시.
        # 설명용 꼬리말이나 반복 요약을 붙이지 않는다. 읽을 시간을 확보한 뒤 끝낸다.
        title_lines = ["Heterogeneous Causal Learning", "for Effectiveness Optimization", "in User Marketing"]
        if " ".join(title_lines) != reference["title"]:
            raise ValueError("화면의 참고 문헌 제목이 원문과 다릅니다.")
        paper_title = VGroup(*[label(t, 33) for t in title_lines]).arrange(DOWN, buff=0.15)
        paper_title.move_to(UP * 1.15)
        authors = label(" · ".join(reference["authors"]), 23, MUTED).move_to(DOWN * 0.25)
        year = label(f"{reference['organization']}  ·  {reference['year']}", 25, MUTED).move_to(DOWN * 0.95)
        url = label(reference["pdf"].removeprefix("https://"), 28, GROUP_A).move_to(DOWN * 1.8)
        citation = VGroup(paper_title, authors, year, url)
        self.stage(self.timing["totalDuration"] + 0.3, "참고 문헌", citation)
        self.go(self.timing["totalDuration"] + 6)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=0.5)
        qa = TOPIC / "build/qa"
        qa.mkdir(parents=True, exist_ok=True)
        (qa / "animation_events.json").write_text(json.dumps(self.events, ensure_ascii=False, indent=2))

    def when(self, paragraph, phrase=None):
        chunk = self.timing["chunks"][paragraph - 1]
        if phrase is None:
            return chunk["start"]
        text = "".join(chunk["alignment"]["characters"])
        index = text.find(phrase)
        if index < 0:
            raise ValueError(f"문단 {paragraph}에 없는 타이밍 기준 문구: {phrase}")
        return chunk["alignment"]["character_start_times_seconds"][index]

    def go(self, target):
        if target > self.renderer.time:
            self.wait(target - self.renderer.time)

    def at(self, target, *animations, run_time=0.6):
        self.go(target)
        actual = self.renderer.time
        if actual - target > 1.4:
            raise ValueError(f"음성과 애니메이션의 지연이 큽니다: {target:.2f} -> {actual:.2f}")
        self.events.append({"target": target, "actual": actual, "duration": run_time})
        self.play(*animations, run_time=run_time)

    def show(self, target, mob, grow=None):
        if grow is None:
            self.at(target, FadeIn(mob, shift=UP * 0.08))
        else:
            rest = VGroup(*[m for m in mob if m is not grow])
            self.at(target, GrowFromEdge(grow, DOWN), FadeIn(rest))
        self.content.append(mob)
        self.bounds(mob)

    def stage(self, target, title, mob):
        self.go(target)
        # 이전 큰 요소부터 제거한 뒤 다음 핵심 그룹을 올려 정보가 겹치지 않게 한다.
        # 한글 글자 모양을 변형하지 않고 기존 제목을 지운 뒤 새 제목을 부드럽게 올린다.
        self.play(FadeOut(VGroup(self.heading, *self.content)), run_time=0.25)
        self.content = []
        self.heading = label(title, 38).move_to(UP * 3.15)
        self.at(max(target, self.renderer.time), FadeIn(self.heading),
                FadeIn(mob, shift=UP * 0.08), run_time=0.55)
        self.content.append(mob)
        self.bounds(mob)

    @staticmethod
    def bounds(mob):
        # 실제 렌더 영역을 검사해 본문이 제목이나 화면 하단 여백에 침범하면 중단한다.
        # 숫자와 본문의 안전 여백을 지켜 화면 밖에서 잘리는 요소를 막는다.
        if mob.width > 12.9 or mob.get_top()[1] > 2.5 or mob.get_bottom()[1] < -3.2:
            raise ValueError(f"본문이 안전 영역 밖입니다: 위 {mob.get_top()}, 아래 {mob.get_bottom()}")
