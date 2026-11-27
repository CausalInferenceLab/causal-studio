<h1 align="center">Causal Studio</h1>

<p align="center"><strong>어려운 수학·통계 개념을 3Blue1Brown 스타일의 영상으로 만들어 보세요.</strong></p>

<p align="center">인과추론 강의 영상을 만들며 다듬은 오픈소스 Manim 스킬입니다.<br>Claude Code나 Codex에 만들고 싶은 영상을 설명해 주세요.</p>

<p align="center">
  <a href="#첫-영상-만들기"><strong>영상 만들기</strong></a> ·
  <a href="https://www.youtube.com/@CausalStudio">YouTube에서 보기</a> ·
  <a href="https://causalinferencelab.github.io/causal-studio/">인과추론 교재</a> ·
  <a href="./README.md">English</a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="./docs/assets/did-preview.jpg">
    <img src="./docs/assets/did-animation.gif" width="820" alt="두 도시의 예금액 추세를 같은 출발점에 맞춰 광고 후 성장 폭의 차이를 보여주는 애니메이션.">
  </picture><br>
  <sub>차분의 차분 · 옥외광고 사례</sub>
</p>

## 첫 영상 만들기

1. `skill-only` 브랜치를 클론하세요.

   ```bash
   git clone -b skill-only https://github.com/CausalInferenceLab/causal-studio
   ```

2. Claude Code나 Codex에서 폴더를 열고 영상을 요청하세요.

   ```text
   manim-video-pipeline 스킬로 A/B 테스트에 왜 무작위 배정이 필요한지
   45초짜리 영상으로 만들어줘. 티켓을 사러 온 손님이 한쪽 결제 화면에 더 많이
   배정된 결과, 손님마다 동전을 던져 배정하는 과정, 배정 후 결과를 세 장면으로 보여줘.
   ```

영상에 참고할 대본이나 설명·그래프를 정리한 Jupyter 노트북이 있다면 파일 경로를 함께 알려주세요. 주제 한 줄로도 시작할 수 있습니다. [노트북 예시](./book/rdd/01_rdd_basic_ko.ipynb)

첫 미리보기는 음성 API 키 없이 렌더링할 수 있습니다.

## 영상 제작 흐름

1. **화면과 대본을 잡습니다.** 주제에 맞는 3Blue1Brown 영상과 Manim 코드를 참고합니다. 카메라가 무엇을 따라가고, 움직임이 끝난 화면에서 무엇이 새로 보일지 정합니다.
2. **핵심 전환을 먼저 확인합니다.** 전환 전·중·후 화면에서 그래프나 글자가 겹치거나 잘리는 곳을 찾습니다. 설명이 끊기는 부분이 있으면 그 장면만 고쳐 다시 렌더링합니다.
3. **음성을 맞추고 내보냅니다.** 내레이션을 원하면 OpenAI나 ElevenLabs로 내레이션을 만들고, `*.timings.json`에 기록된 시간에 맞춰 최종 애니메이션을 만듭니다. MP4와 썸네일, 내레이션이 있는 영상에는 SRT 자막도 제공됩니다. [음성 설정](./docs/manim-starter.md#3-review-and-add-narration-if-you-want-it)

에이전트 분업을 지원하는 환경에서는 레퍼런스 조사, 화면 설계, 독립 시사 검수를 나눠 맡겨 달라고 요청할 수 있습니다.

## 결과물과 장면 수정

장면별로 Manim 코드와 대본을 확인할 수 있습니다. 내레이션 대본은 음성을 넣을 때 사용합니다.

```text
videos/ab_test/ko/
├── project.toml              # 참고 자료와 기본 렌더 장면
├── lesson.md                 # 주제로 시작할 때 작성하는 제작 메모
├── scene_plan.md             # 레퍼런스, 구도, 장면 순서
├── narration/                # 장면별 대본
│   ├── 01_question.txt
│   ├── 02_assignment.txt
│   └── 03_comparison.txt
├── scenes/                   # 장면별 Manim 코드
│   ├── scene_01_question.py
│   ├── scene_02_assignment.py
│   └── scene_03_comparison.py
└── build/
    ├── audio/                # MP3와 타이밍 파일
    ├── logs/                 # 렌더 시도별 로그
    ├── manim/                # 렌더링한 장면
    ├── review/               # 전환 프레임과 비교 이미지
    └── final/                # MP4, 썸네일 PNG, 음성이 있다면 SRT
```

> 2번 장면에서 배정이 바뀌는 동안 첫 그룹이 화면에 남게 해줘. 그 장면만 다시 렌더링해줘.

## Causal Studio 둘러보기

강의 영상의 대본과 코드는 RDD [한국어 프로젝트](./videos/rdd/ko/)와 [영어 프로젝트](./videos/rdd/en/)에서 볼 수 있습니다. 교재나 기존 영상도 작업하려면 같은 영상 스킬이 들어 있는 전체 저장소를 받으세요.

```bash
git clone https://github.com/CausalInferenceLab/causal-studio
```

[스킬 보기](./.claude/skills/manim-video-pipeline/SKILL.md) · [기여하기](./CONTRIBUTING-ko_kr.md)

---

스킬이 영상 제작에 도움이 됐다면 Causal Studio에 스타를 눌러주세요.

MIT. 3Blue1Brown 레퍼런스와 Tabler Icons 같은 외부 자산은 각자의 라이선스를 따릅니다.
