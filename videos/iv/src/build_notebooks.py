"""Build book/iv/iv_ko.ipynb and iv_en.ipynb from inline cell specs.

Run from repo root:
    python videos/iv/src/build_notebooks.py

Pattern mirrors book/why_causal_inference/why_causal_inference_{ko,en}.ipynb:
- Section headers as markdown
- Math via LaTeX
- DAGs via graphviz
- Tables / simulations via pandas+numpy
- References at the end
"""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf


REPO_ROOT = Path(__file__).resolve().parents[3]
BOOK_DIR = REPO_ROOT / "book" / "iv"


def md(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_markdown_cell(text)


def code(text: str) -> nbf.NotebookNode:
    return nbf.v4.new_code_cell(text)


# ───────────────────────────────────────────────────────────────────
# Korean notebook content
# ───────────────────────────────────────────────────────────────────

KO_CELLS: list[nbf.NotebookNode] = [
    md(
        "**🌐 언어:** **한국어** | [English →](/iv-en)\n\n"
        "# 도구변수(Instrumental Variables) 한눈에 보기\n\n"
        "<small><em>인과추론 동료 학습 자료 · "
        "동반 영상: <a href=\"https://www.youtube.com/@CausalStudio\">Causal Studio</a></em></small>"
    ),
    md(
        "이 노트북은 7분짜리 동반 영상의 내용을 글과 코드로 풀어 놓은 자료입니다.\n\n"
        "전제 지식은 다음과 같습니다.\n"
        "- 선형회귀(OLS)의 의미\n"
        "- 무작위 배정(RCT)이 왜 인과효과를 깨끗하게 추정할 수 있는지\n"
        "- 단순 평균 차이에 편향이 섞일 수 있다는 직관\n\n"
        "여기서 더 나아가, 무작위 배정이 불가능한 현실에서 \"우리가 손에 쥔 다른 무작위성\"을 이용해 "
        "인과효과를 짚어 내는 방법, 즉 **도구변수**를 다룹니다."
    ),
    md(
        "## 1) 도입: 1854년 런던, 존 스노우의 우연\n\n"
        "1854년 런던에 콜레라가 휩쓸 때, 의사 존 스노우(John Snow)는 거리마다 사망률이 크게 다르다는 사실에 주목했습니다. "
        "당시 런던에는 두 곳의 수도 회사가 가정에 물을 공급했는데, 한 회사(Lambeth)는 상류의 깨끗한 물을, 다른 회사(Southwark & Vauxhall)는 하수가 섞인 강물을 끌어다 썼습니다.\n\n"
        "결정적으로, **어느 회사의 물이 어느 거리로 들어가는지는 가정의 형편이나 위생 습관과 거의 무관**했습니다. 거리마다 미리 깔린 배관망의 차이였을 뿐이죠.\n\n"
        "스노우는 이 우연을 붙잡았습니다. 실험자가 직접 동전을 던질 수 없는 상황에서, **자연이 던진 동전**이 도시 안에 이미 존재했던 셈입니다.\n\n"
        "도구변수(Instrumental Variable, IV)는 바로 이런 \"현실 속 우연\"을 찾아 인과효과를 짚어 내는 도구입니다."
    ),
    md(
        "## 2) 표기법과 출발점\n\n"
        "도구변수를 이야기하기 위해 세 가지 변수를 도입합니다.\n\n"
        "- $Z$ : **도구변수**. 실험자 또는 자연이 던진 동전. (예: 태블릿 배정 여부, 추첨 번호)\n"
        "- $T$ : **처치**. 실제로 받은 처치 여부. (예: 태블릿을 실제로 사용했는가)\n"
        "- $Y$ : **결과**. 우리가 알고 싶은 결과 변수. (예: 학업 성취도)\n\n"
        "그리고 잠재적 결과(potential outcomes) 표기:\n\n"
        "- $Y_0$ : 처치를 받지 않았을 때의 잠재적 결과\n"
        "- $Y_1$ : 처치를 받았을 때의 잠재적 결과\n\n"
        "이전 챕터에서 본 평균 처치 효과는 $ATE = E[Y_1 - Y_0]$이었습니다. "
        "이번 챕터의 핵심 결과는 **모든 사람의 평균이 아니라 일부 사람(순응자)의 평균에 한정된 효과**, 즉 **LATE**가 됩니다."
    ),
    md(
        "## 3) 비순응으로 단순 비교가 깨진다\n\n"
        "이전 챕터의 태블릿 RCT를 다시 가져옵시다. 연구진이 동전을 던져 일부 학교에는 태블릿을 \"배정\"했습니다. "
        "그런데 현실에서는 두 가지 일이 동시에 벌어집니다.\n\n"
        "1. **처치 배정 학교 중 일부가 태블릿을 거부**합니다 (\"교사가 쓰기 싫어요\", \"보관할 곳이 없어요\").\n"
        "2. **통제 배정 학교 중 일부가 사비로 태블릿을 구매**합니다 (\"우리는 어쨌든 쓸래요\").\n\n"
        "이 상황에서 \"실제 처치 여부\"로 두 집단의 평균을 비교하면, 두 집단은 더 이상 비교 가능하지 않습니다. "
        "거부한 학교는 새 기술에 회의적인 곳일 가능성이 높고, 사비로 산 학교는 원래 의지가 강한 곳일 가능성이 높기 때문입니다.\n\n"
        "**배정($Z$)은 무작위지만, 실제 처치($T$)는 무작위가 아닙니다.** 작은 시뮬레이션으로 이 깨짐을 확인해 봅시다."
    ),
    code(
        "import numpy as np\n"
        "import pandas as pd\n\n"
        "rng = np.random.default_rng(2026)\n"
        "n = 4000\n\n"
        "# 학교의 잠재적 처치-반응 유형: 60% 순응자, 20% 언제나 받음, 20% 절대 안 받음\n"
        "compliance_type = rng.choice(\n"
        "    [\"complier\", \"always_taker\", \"never_taker\"],\n"
        "    size=n, p=[0.60, 0.20, 0.20],\n"
        ")\n\n"
        "# 동전 배정: 절반에게 처치 배정\n"
        "Z = rng.binomial(1, 0.5, n)\n\n"
        "# 실제 처치 T는 유형 + 배정에 따라 결정\n"
        "T = np.where(\n"
        "    compliance_type == \"complier\", Z,                  # 순응자: 배정 = 처치\n"
        "    np.where(compliance_type == \"always_taker\", 1, 0)   # 언제나/절대\n"
        ")\n\n"
        "# 결과 Y: 진짜 처치 효과는 +5점. 단, 순응자와 그 외 그룹의 기본 점수가 다르다.\n"
        "baseline = np.where(\n"
        "    compliance_type == \"complier\", 70,\n"
        "    np.where(compliance_type == \"always_taker\", 80, 60)\n"
        ")\n"
        "true_effect = 5  # 진짜 LATE\n"
        "Y = baseline + true_effect * T + rng.normal(0, 5, n)\n\n"
        "df = pd.DataFrame(dict(Z=Z, T=T, Y=Y, type=compliance_type))\n"
        "df.head()"
    ),
    code(
        "# 단순 비교: 실제 처치 받은 학교 vs 받지 않은 학교\n"
        "naive_diff = df.loc[df[\"T\"] == 1, \"Y\"].mean() - df.loc[df[\"T\"] == 0, \"Y\"].mean()\n"
        "print(f\"단순 평균 차이 (실제 T 기준): {naive_diff:+.2f}\")\n"
        "print(f\"진짜 처치 효과:                  {true_effect:+.2f}\")"
    ),
    md(
        "단순 평균 차이는 진짜 처치 효과(+5점)와 크게 어긋납니다. "
        "이유는 단순합니다. 실제 처치를 받은 학교에는 \"언제나 받음(기본 점수 80)\"이 더 많고, 받지 않은 학교에는 \"절대 안 받음(기본 점수 60)\"이 더 많기 때문입니다. "
        "**유형 차이가 평균 차이로 흘러 들어와** 편향을 만든 것입니다.\n\n"
        "배정($Z$)으로 비교하면 어떨까요?"
    ),
    code(
        "itt = df.loc[df[\"Z\"] == 1, \"Y\"].mean() - df.loc[df[\"Z\"] == 0, \"Y\"].mean()\n"
        "print(f\"배정(ITT) 차이: {itt:+.2f}\")"
    ),
    md(
        "ITT(Intention-to-Treat) 차이는 약 +3점 부근으로 나옵니다. "
        "이 값은 \"동전을 던졌을 때 평균적으로 점수가 얼마나 달라지는가\"를 말해 줍니다. "
        "편향은 없지만, **진짜 처치 효과보다 작게** 측정됩니다. 동전을 따른 사람이 일부(순응자)뿐이기 때문입니다.\n\n"
        "도구변수의 핵심 아이디어는, **이 작은 차이를 \"실제로 움직인 사람의 비율\"로 환산**하면 한 명의 순응자에게 처치가 만든 효과가 나온다는 것입니다."
    ),
    md(
        "## 4) 세 가지 유형: 순응자, 언제나 받음, 절대 안 받음\n\n"
        "동전 $Z$가 사람들을 움직이는 방식은 세 가지로 나뉩니다.\n\n"
        "| 유형 | $Z = 1$일 때 $T$ | $Z = 0$일 때 $T$ | 비고 |\n"
        "|---|:---:|:---:|---|\n"
        "| **순응자** (Complier) | 1 | 0 | 동전을 따른다 |\n"
        "| **언제나 받음** (Always-taker) | 1 | 1 | 동전과 무관 |\n"
        "| **절대 안 받음** (Never-taker) | 0 | 0 | 동전과 무관 |\n"
        "| Defier (배반자) | 0 | 1 | 일반적으로 존재하지 않는다고 가정 |\n\n"
        "도구변수가 짚어 내는 효과는 **오직 순응자에 한정**됩니다. "
        "동전이 흔들지 않은 두 그룹(언제나 받음, 절대 안 받음)은 비교에 들어가도 차이를 만들지 않기 때문입니다. "
        "이것이 LATE(Local Average Treatment Effect)의 정의입니다."
    ),
    md(
        "## 5) 와알드 추정량: 숫자로 구하는 LATE\n\n"
        "$$\n"
        "\\text{LATE} \\;=\\; \\frac{E[Y \\mid Z=1] - E[Y \\mid Z=0]}{E[T \\mid Z=1] - E[T \\mid Z=0]}\n"
        "$$\n\n"
        "- 분자: **ITT** — 동전이 만든 결과 차이.\n"
        "- 분모: **순응자 비율** — 동전이 실제로 움직인 사람의 몫.\n\n"
        "둘을 나누면 \"한 명의 순응자에게 처치가 만든 효과\"가 됩니다. "
        "이 식을 와알드(Wald) 추정량이라고 부르며, 가장 단순한 도구변수 추정의 형태입니다."
    ),
    code(
        "num = df.loc[df[\"Z\"] == 1, \"Y\"].mean() - df.loc[df[\"Z\"] == 0, \"Y\"].mean()\n"
        "den = df.loc[df[\"Z\"] == 1, \"T\"].mean() - df.loc[df[\"Z\"] == 0, \"T\"].mean()\n"
        "wald = num / den\n"
        "print(f\"ITT (분자):       {num:+.3f}\")\n"
        "print(f\"순응자 비율 (분모): {den:.3f}\")\n"
        "print(f\"와알드 추정량:    {wald:+.3f}\")\n"
        "print(f\"진짜 LATE:         {true_effect:+.3f}\")"
    ),
    md(
        "와알드 추정량은 진짜 처치 효과(+5점)와 거의 일치합니다. "
        "단순 평균 차이는 유형 구성에 오염되어 있었지만, 동전이 만들어 낸 차이만을 골라내고 동전이 움직인 비율로 환산하면 깨끗한 효과가 회복됩니다.\n\n"
        "실무에서는 같은 추정을 **2SLS(Two-Stage Least Squares)**로 합니다. 1단계에서 $T$를 $Z$로 회귀해 적합값 $\\hat T$를 만들고, 2단계에서 $Y$를 $\\hat T$로 회귀합니다."
    ),
    code(
        "import statsmodels.api as sm\n\n"
        "# 1단계: T ~ Z\n"
        "first = sm.OLS(df[\"T\"], sm.add_constant(df[\"Z\"])).fit()\n"
        "df[\"T_hat\"] = first.predict(sm.add_constant(df[\"Z\"]))\n\n"
        "# 2단계: Y ~ T_hat\n"
        "second = sm.OLS(df[\"Y\"], sm.add_constant(df[\"T_hat\"])).fit()\n"
        "print(f\"2SLS 추정 처치 효과: {second.params['T_hat']:+.3f}\")"
    ),
    md(
        "## 6) 도구변수의 세 가지 가정\n\n"
        "와알드 식이 **인과효과**를 추정하려면 다음 세 조건이 모두 만족되어야 합니다. "
        "하나라도 깨지면 결과를 인과적으로 해석할 수 없습니다.\n\n"
        "**(a) 적합성 (Relevance)** — $Z$가 $T$를 실제로 움직여야 한다.\n"
        "$$\\operatorname{Cov}(Z, T) \\neq 0$$\n"
        "$Z$가 $T$를 거의 움직이지 못하면 분모가 0에 가까워져 추정량이 폭주합니다. \"약한 도구(weak instrument)\" 문제입니다.\n\n"
        "**(b) 배제 조건 (Exclusion Restriction)** — $Z$가 $Y$에 미치는 영향은 오직 $T$를 거쳐야 한다.\n"
        "태블릿을 받았다는 통보 자체가 — 태블릿을 쓰지 않더라도 — 학교 분위기를 바꾼다면 이 조건은 깨집니다.\n\n"
        "**(c) 독립성 (Independence)** — $Z$는 잠재적 결과와 독립이어야 한다.\n"
        "$$(Y_0, Y_1) \\perp Z$$\n"
        "RCT 배정이라면 설계상 만족됩니다. 자연이 던진 동전이라면, 정말 우연이었는지 따져 보아야 합니다.\n\n"
        "DAG로 그리면 다음과 같습니다."
    ),
    code(
        "import graphviz as gr\n\n"
        "g = gr.Digraph()\n"
        "g.attr(rankdir=\"LR\")\n"
        "g.node(\"Z\", \"Z (도구변수)\", color=\"orange\", fontcolor=\"orange\")\n"
        "g.node(\"T\", \"T (처치)\")\n"
        "g.node(\"Y\", \"Y (결과)\")\n"
        "g.node(\"U\", \"U (관측되지 않은 교란)\", style=\"dashed\")\n\n"
        "g.edge(\"Z\", \"T\")\n"
        "g.edge(\"T\", \"Y\")\n"
        "g.edge(\"U\", \"T\", style=\"dashed\")\n"
        "g.edge(\"U\", \"Y\", style=\"dashed\")\n\n"
        "g"
    ),
    md(
        "위 DAG에서 $U$는 $T$와 $Y$ 양쪽에 영향을 주는 관측되지 않은 교란입니다. "
        "단순 회귀 $Y \\sim T$는 이 $U$ 때문에 편향됩니다. "
        "하지만 $Z$가 $U$와 무관하고, $Z \\to Y$ 경로가 $T$를 거쳐서만 존재한다면, $Z$를 통해 \"오염되지 않은\" 변동만 골라 $T \\to Y$ 효과를 식별할 수 있습니다."
    ),
    md(
        "## 7) 국가 규모 사례: 베트남 징집 추첨 (Angrist 1990)\n\n"
        "1969년 미국. 베트남 전쟁을 위한 징집을 추첨 방식으로 결정했습니다. "
        "생일 365일이 적힌 공이 뽑혀, 낮은 번호가 뽑힌 사람부터 입대했습니다. **태어난 날짜는 본인이 고를 수 없고**, 추첨 번호는 학력·직업·집안과 무관했습니다. 거의 완벽한 자연의 동전이었습니다.\n\n"
        "경제학자 조슈아 앵그리스트(Joshua Angrist)는 이 추첨을 도구변수로 써서 **군 복무가 평생 소득에 미친 효과**를 추정했습니다.\n\n"
        "- $Z$ : 추첨 번호 기반 입대 자격\n"
        "- $T$ : 실제 군 복무 여부\n"
        "- $Y$ : 이후 소득\n\n"
        "단순히 참전 군인과 비참전 군인의 소득을 비교하면 \"참전을 선택한 사람\"과 \"회피한 사람\"의 차이가 섞여 들어옵니다. "
        "추첨 번호를 도구변수로 두면, 우연이 움직인 부분만 분리해 깨끗한 효과(LATE)를 얻을 수 있습니다.\n\n"
        "Angrist(1990)는 이 방법으로 군 복무가 백인 남성의 이후 소득을 약 **15% 감소**시킨 것으로 추정했습니다. 이는 \"참전 = 경험치 + 네트워크 = 소득 증가\"라는 단순 해석이 편향되어 있음을 보여 준 대표적 결과입니다."
    ),
    md(
        "## 8) 정리\n\n"
        "- **단순 평균 차이**: 교란이 있으면 인과효과와 일치하지 않는다.\n"
        "- **RCT**: 무작위 배정으로 편향을 제거하지만, 비순응이 끼어들면 \"실제 처치\" 기준 비교는 다시 깨진다.\n"
        "- **도구변수 (IV)**: 무작위 배정이 불가능한 현실에서, 실제로 처치에는 영향을 주지만 결과에는 처치를 통해서만 영향을 주는 변수 $Z$를 찾아 \"우연이 움직인 부분만\" 분리해 효과를 식별한다.\n"
        "- **와알드 추정량 / 2SLS**: ITT를 순응자 비율로 나눈 비율. 식별되는 효과는 LATE, 즉 **순응자에 한정된 평균 처치 효과**다.\n"
        "- **세 자물쇠**: 적합성, 배제 조건, 독립성. 모두 만족해야 도구변수의 문이 열린다.\n\n"
        "도구변수 분석에서 가장 어려운 일은 수식이 아니라 **현실 속에서 그럴듯한 우연을 찾아내는 일**입니다. 스노우의 수도 회사, 앵그리스트의 추첨, 또 어쩌면 여러분의 생일이 그런 우연이 될 수 있습니다."
    ),
    md(
        "## 참고 자료\n\n"
        "- Angrist, J. D. (1990). *Lifetime Earnings and the Vietnam Era Draft Lottery: Evidence from Social Security Administrative Records.* American Economic Review, 80(3), 313–336.\n"
        "- Imbens, G. W., & Angrist, J. D. (1994). *Identification and Estimation of Local Average Treatment Effects.* Econometrica, 62(2), 467–475.\n"
        "- Angrist, J. D., & Pischke, J.-S. (2009). *Mostly Harmless Econometrics: An Empiricist's Companion.* Princeton University Press. (Ch. 4)\n"
        "- Snow, J. (1855). *On the Mode of Communication of Cholera.* John Churchill.\n"
        "- Matheus Facure, *Python Causality Handbook*: [08 - Instrumental Variables](https://matheusfacure.github.io/python-causality-handbook/08-Instrumental-Variables.html)\n"
        "- 동반 영상: [Causal Studio · IV in a Nutshell (KO)](https://www.youtube.com/@CausalStudio)"
    ),
]


# ───────────────────────────────────────────────────────────────────
# English notebook content
# ───────────────────────────────────────────────────────────────────

EN_CELLS: list[nbf.NotebookNode] = [
    md(
        "**🌐 Language:** **English** | [한국어 →](/iv-ko)\n\n"
        "# Instrumental Variables in a Nutshell\n\n"
        "<small><em>Causal inference peer-learning material · "
        "Companion video: <a href=\"https://www.youtube.com/@CausalStudio\">Causal Studio</a></em></small>"
    ),
    md(
        "This notebook is the written-and-coded counterpart of a 7-minute companion video.\n\n"
        "Prerequisites:\n"
        "- Linear regression (OLS)\n"
        "- Why random assignment (RCTs) gives a clean estimate of a causal effect\n"
        "- The intuition that simple mean differences can be biased\n\n"
        "We build on those by asking: when random assignment is *not* possible, can we use some other randomness already lying around in the real world to identify a causal effect? "
        "That's the **instrumental variable**."
    ),
    md(
        "## 1) The Snow story: a coin flipped by nature\n\n"
        "When cholera devastated London in 1854, the physician John Snow noticed that death rates varied wildly from street to street. "
        "At the time, two companies piped water into London homes — Lambeth, which drew clean water from upstream, and Southwark & Vauxhall, which drew sewage-mixed water from the lower Thames.\n\n"
        "Crucially, **which company served which street had almost nothing to do with the household's income or hygiene**. It was a matter of which pipes had been laid decades earlier.\n\n"
        "Snow exploited that accident. The experimenter (Snow) couldn't flip a coin to decide who drank clean water, but **nature had already flipped one** on his behalf.\n\n"
        "An instrumental variable (IV) is exactly this kind of tool — one that catches accidents already present in the real world and uses them to pin down a causal effect."
    ),
    md(
        "## 2) Notation\n\n"
        "We need three variables:\n\n"
        "- $Z$ : the **instrument** — a coin flipped by the experimenter or by nature. (e.g., tablet assignment, lottery number)\n"
        "- $T$ : the **treatment actually taken**. (e.g., whether the school actually used the tablets)\n"
        "- $Y$ : the **outcome** we care about. (e.g., test scores)\n\n"
        "Plus potential outcomes:\n\n"
        "- $Y_0$ : the potential outcome under no treatment\n"
        "- $Y_1$ : the potential outcome under treatment\n\n"
        "The previous chapter introduced the average treatment effect, $ATE = E[Y_1 - Y_0]$. "
        "This chapter's main quantity is **an effect restricted to a particular subgroup (the compliers)** — the **LATE**."
    ),
    md(
        "## 3) Non-compliance breaks the naive comparison\n\n"
        "Take the tablet RCT from the previous chapter. Researchers flipped a coin and \"assigned\" some schools to receive tablets. In the real world, two things happen at once.\n\n"
        "1. **Some assigned-treatment schools refuse the tablets** (\"the teachers don't want them\", \"nowhere to store them\").\n"
        "2. **Some assigned-control schools buy tablets with their own budget** (\"we're going to use them anyway\").\n\n"
        "If we now compare \"actually treated\" vs. \"actually untreated\", the two groups are no longer comparable. "
        "Refusers are probably skeptical of new tech; self-buyers are probably more motivated to begin with.\n\n"
        "**Assignment ($Z$) is random, but actual treatment ($T$) is not.** A small simulation makes this concrete."
    ),
    code(
        "import numpy as np\n"
        "import pandas as pd\n\n"
        "rng = np.random.default_rng(2026)\n"
        "n = 4000\n\n"
        "# Each school has a latent compliance type: 60% compliers, 20% always-takers, 20% never-takers.\n"
        "compliance_type = rng.choice(\n"
        "    [\"complier\", \"always_taker\", \"never_taker\"],\n"
        "    size=n, p=[0.60, 0.20, 0.20],\n"
        ")\n\n"
        "# Random assignment: half get assigned to treatment.\n"
        "Z = rng.binomial(1, 0.5, n)\n\n"
        "# Actual treatment T depends on type AND assignment.\n"
        "T = np.where(\n"
        "    compliance_type == \"complier\", Z,                  # complier: assignment = treatment\n"
        "    np.where(compliance_type == \"always_taker\", 1, 0)   # always / never\n"
        ")\n\n"
        "# Outcome Y: true treatment effect = +5. But baseline scores differ by type.\n"
        "baseline = np.where(\n"
        "    compliance_type == \"complier\", 70,\n"
        "    np.where(compliance_type == \"always_taker\", 80, 60)\n"
        ")\n"
        "true_effect = 5  # true LATE\n"
        "Y = baseline + true_effect * T + rng.normal(0, 5, n)\n\n"
        "df = pd.DataFrame(dict(Z=Z, T=T, Y=Y, type=compliance_type))\n"
        "df.head()"
    ),
    code(
        "# Naive comparison: actually-treated vs actually-untreated\n"
        "naive_diff = df.loc[df[\"T\"] == 1, \"Y\"].mean() - df.loc[df[\"T\"] == 0, \"Y\"].mean()\n"
        "print(f\"Naive mean difference (by actual T): {naive_diff:+.2f}\")\n"
        "print(f\"True treatment effect:                {true_effect:+.2f}\")"
    ),
    md(
        "The naive difference is far from the true effect of +5. "
        "Why? The actually-treated pool is rich in always-takers (baseline 80) and the actually-untreated pool is rich in never-takers (baseline 60). "
        "**Type composition leaks into the mean difference** and becomes bias.\n\n"
        "What if we compare by assignment ($Z$) instead?"
    ),
    code(
        "itt = df.loc[df[\"Z\"] == 1, \"Y\"].mean() - df.loc[df[\"Z\"] == 0, \"Y\"].mean()\n"
        "print(f\"ITT (assignment) difference: {itt:+.2f}\")"
    ),
    md(
        "The intention-to-treat difference lands somewhere around +3 — unbiased, but **smaller than the true effect**, because only some of the schools (the compliers) actually moved with the coin.\n\n"
        "IV's core idea: **divide this small assignment-driven difference by the share of people the coin actually moved** to recover the effect on one mover."
    ),
    md(
        "## 4) Three types: complier, always-taker, never-taker\n\n"
        "Here is how the coin $Z$ moves people, organized by type:\n\n"
        "| Type | $T$ when $Z = 1$ | $T$ when $Z = 0$ | Note |\n"
        "|---|:---:|:---:|---|\n"
        "| **Complier** | 1 | 0 | follows the coin |\n"
        "| **Always-taker** | 1 | 1 | ignores the coin |\n"
        "| **Never-taker** | 0 | 0 | ignores the coin |\n"
        "| Defier | 0 | 1 | assumed not to exist (monotonicity) |\n\n"
        "IV recovers an effect for **the compliers only**, because the always-takers and never-takers behave the same in both arms and contribute nothing to the difference. "
        "This is the **Local Average Treatment Effect (LATE)**."
    ),
    md(
        "## 5) The Wald estimator: LATE in numbers\n\n"
        "$$\n"
        "\\text{LATE} \\;=\\; \\frac{E[Y \\mid Z=1] - E[Y \\mid Z=0]}{E[T \\mid Z=1] - E[T \\mid Z=0]}\n"
        "$$\n\n"
        "- Numerator: **ITT** — the effect the coin produced on the outcome.\n"
        "- Denominator: **share of compliers** — the fraction the coin actually moved.\n\n"
        "Dividing one by the other gives the effect of treatment on a single complier. "
        "This is the Wald estimator — the simplest form of IV estimation."
    ),
    code(
        "num = df.loc[df[\"Z\"] == 1, \"Y\"].mean() - df.loc[df[\"Z\"] == 0, \"Y\"].mean()\n"
        "den = df.loc[df[\"Z\"] == 1, \"T\"].mean() - df.loc[df[\"Z\"] == 0, \"T\"].mean()\n"
        "wald = num / den\n"
        "print(f\"ITT (numerator):           {num:+.3f}\")\n"
        "print(f\"Compliers share (denom):   {den:.3f}\")\n"
        "print(f\"Wald estimator:            {wald:+.3f}\")\n"
        "print(f\"True LATE:                 {true_effect:+.3f}\")"
    ),
    md(
        "The Wald estimator lines up with the true effect (+5). "
        "The naive comparison was contaminated by type composition; the Wald formula isolates the part the coin actually moved and rescales it by the compliers' share.\n\n"
        "In practice, the same estimate is computed via **2SLS (Two-Stage Least Squares)**: first regress $T$ on $Z$ to get fitted values $\\hat T$, then regress $Y$ on $\\hat T$."
    ),
    code(
        "import statsmodels.api as sm\n\n"
        "# Stage 1: T ~ Z\n"
        "first = sm.OLS(df[\"T\"], sm.add_constant(df[\"Z\"])).fit()\n"
        "df[\"T_hat\"] = first.predict(sm.add_constant(df[\"Z\"]))\n\n"
        "# Stage 2: Y ~ T_hat\n"
        "second = sm.OLS(df[\"Y\"], sm.add_constant(df[\"T_hat\"])).fit()\n"
        "print(f\"2SLS estimated treatment effect: {second.params['T_hat']:+.3f}\")"
    ),
    md(
        "## 6) Three assumptions for a valid instrument\n\n"
        "For the Wald formula to deliver a **causal** quantity, three conditions must hold simultaneously. If any one fails, the estimate is no longer causally interpretable.\n\n"
        "**(a) Relevance** — $Z$ must actually move $T$.\n"
        "$$\\operatorname{Cov}(Z, T) \\neq 0$$\n"
        "If $Z$ barely moves $T$, the denominator approaches zero and the estimator explodes — the \"weak instrument\" problem.\n\n"
        "**(b) Exclusion restriction** — $Z$ can affect $Y$ only through $T$.\n"
        "If being assigned tablets changes school morale even when no tablets are used, exclusion is broken.\n\n"
        "**(c) Independence** — $Z$ must be independent of the potential outcomes.\n"
        "$$(Y_0, Y_1) \\perp Z$$\n"
        "In an RCT this is satisfied by design. For a coin flipped by nature, you must argue it case by case.\n\n"
        "As a DAG:"
    ),
    code(
        "import graphviz as gr\n\n"
        "g = gr.Digraph()\n"
        "g.attr(rankdir=\"LR\")\n"
        "g.node(\"Z\", \"Z (instrument)\", color=\"orange\", fontcolor=\"orange\")\n"
        "g.node(\"T\", \"T (treatment)\")\n"
        "g.node(\"Y\", \"Y (outcome)\")\n"
        "g.node(\"U\", \"U (unobserved confounder)\", style=\"dashed\")\n\n"
        "g.edge(\"Z\", \"T\")\n"
        "g.edge(\"T\", \"Y\")\n"
        "g.edge(\"U\", \"T\", style=\"dashed\")\n"
        "g.edge(\"U\", \"Y\", style=\"dashed\")\n\n"
        "g"
    ),
    md(
        "$U$ is an unobserved variable that affects both $T$ and $Y$. "
        "A naive regression $Y \\sim T$ is biased because of $U$. "
        "But if $Z$ is independent of $U$ and the only path from $Z$ to $Y$ is through $T$, then $Z$ isolates a \"clean\" slice of variation in $T$ that we can use to identify the $T \\to Y$ effect."
    ),
    md(
        "## 7) National scale: the Vietnam draft lottery (Angrist 1990)\n\n"
        "The United States, 1969. To draft people for the Vietnam War, the government used a lottery: balls labeled with all 365 birthdays were drawn bingo-style, and the lowest numbers went first.\n\n"
        "Your birthday is something you can't pick, and the lottery number was unrelated to your education, occupation, or family. As close to a perfectly natural coin flip as you'll get.\n\n"
        "The economist Joshua Angrist used this lottery as an instrument for the effect of **military service on lifetime earnings**.\n\n"
        "- $Z$ : draft eligibility based on lottery number\n"
        "- $T$ : whether the person actually served\n"
        "- $Y$ : later earnings\n\n"
        "A naive veteran-vs-non-veteran comparison conflates the effect of service with the selection of who chose to serve and who avoided it. Using the lottery as an instrument isolates the part chance moved.\n\n"
        "Angrist (1990) estimated that military service reduced subsequent earnings of white male veterans by about **15%** — a result that overturns the casual \"service = experience = higher earnings\" intuition and remains one of the canonical IV findings."
    ),
    md(
        "## 8) Summary\n\n"
        "- **Naive mean differences** are biased whenever there is unobserved confounding.\n"
        "- **RCTs** break the bias by random assignment, but non-compliance reopens it for \"actually treated\" comparisons.\n"
        "- **Instrumental variables (IV)** rescue identification by finding a variable $Z$ that moves $T$ but only affects $Y$ through $T$ — isolating the part driven by chance.\n"
        "- **Wald estimator / 2SLS**: ITT divided by share of compliers. What you identify is **LATE** — the average treatment effect *for the compliers*.\n"
        "- **Three locks**: relevance, exclusion, independence. All three must open or the IV door stays shut.\n\n"
        "The hardest part of an IV analysis isn't the formula — it's **finding a plausible accident in the real world**. Snow's water companies, Angrist's lottery, and maybe your own birthday are all examples of accidents waiting to be used."
    ),
    md(
        "## References\n\n"
        "- Angrist, J. D. (1990). *Lifetime Earnings and the Vietnam Era Draft Lottery: Evidence from Social Security Administrative Records.* American Economic Review, 80(3), 313–336.\n"
        "- Imbens, G. W., & Angrist, J. D. (1994). *Identification and Estimation of Local Average Treatment Effects.* Econometrica, 62(2), 467–475.\n"
        "- Angrist, J. D., & Pischke, J.-S. (2009). *Mostly Harmless Econometrics: An Empiricist's Companion.* Princeton University Press. (Ch. 4)\n"
        "- Snow, J. (1855). *On the Mode of Communication of Cholera.* John Churchill.\n"
        "- Matheus Facure, *Python Causality Handbook*: [08 - Instrumental Variables](https://matheusfacure.github.io/python-causality-handbook/08-Instrumental-Variables.html)\n"
        "- Companion video: [Causal Studio · IV in a Nutshell (EN)](https://www.youtube.com/@CausalStudio)"
    ),
]


def build(cells: list[nbf.NotebookNode], out_path: Path) -> None:
    nb = nbf.v4.new_notebook()
    nb.cells = cells
    nb.metadata.update({
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        },
        "language_info": {
            "name": "python",
            "version": "3.12",
        },
    })
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        nbf.write(nb, f)
    print(f"wrote {out_path}  ({len(cells)} cells)")


if __name__ == "__main__":
    build(KO_CELLS, BOOK_DIR / "iv_ko.ipynb")
    build(EN_CELLS, BOOK_DIR / "iv_en.ipynb")
