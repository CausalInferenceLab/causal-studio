<h1 align="center">Causal Studio</h1>

<p align="center"><strong>어려운 수학·통계 개념을 3Blue1Brown 스타일의 영상으로 만들어 보세요.</strong></p>

<p align="center">인과추론 강의 영상을 제작하며 다듬은 오픈소스 Manim 스킬입니다.<br>Claude Code나 Codex에 만들고 싶은 영상을 설명하기만 하면 됩니다.</p>

<p align="center">
  <a href="#첫-영상-만들기"><strong>영상 만들기</strong></a> ·
  <a href="https://www.youtube.com/@CausalStudio">YouTube에서 보기</a> ·
  <a href="https://causalinferencelab.github.io/causal-studio/">인과추론 교재</a> ·
  <a href="./README.md">English</a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-reduced-motion: reduce)" srcset="./docs/assets/did-preview.jpg">
    <img src="./docs/assets/did-animation.gif" width="820" alt="두 도시의 예금액 추세를 같은 기준선에 맞춰 광고 후 성장 폭의 차이를 보여주는 애니메이션.">
  </picture><br>
  <sub>이중차분법(Difference-in-Differences) · 옥외광고 사례</sub>
</p>

## 첫 영상 만들기

1. `skill-only` 브랜치를 클론하세요.

   ```bash
   git clone -b skill-only https://github.com/CausalInferenceLab/causal-studio
   ```

2. Claude Code나 Codex에서 해당 폴더를 열고 원하는 영상을 요청하세요.

   ```text
   manim-video-pipeline 스킬로 A/B 테스트에 왜 무작위 배정이 필요한지
   45초짜리 영상으로 만들어줘. 티켓을 사러 온 손님들이 한쪽 결제 화면에 몰려
   왜곡된 결과가 나오는 상황, 손님마다 동전을 던져 무작위로 배정하는 과정,
   배정 후 비교 결과를 세 장면에 걸쳐 보여줘.
   ```

참고할 대본이나 설명·그래프가 정리된 Jupyter 노트북이 있다면 파일 경로를 함께 알려주세요. 노트북 없이 주제 한 줄만으로도 시작할 수 있습니다. [노트북 예시](./book/rdd/01_rdd_basic_ko.ipynb)

첫 미리보기는 음성 API 키 없이도 렌더링할 수 있습니다.

## 영상 제작 흐름

1. **구성과 대본을 설계합니다.** 주제와 어울리는 3Blue1Brown 영상과 Manim 코드를 참고해 대본을 쓰고, 카메라의 이동 경로와 각 전환마다 강조할 시각적 요소를 정합니다.
2. **핵심 전환을 먼저 점검합니다.** 전환 전·중·후 프레임을 확인해 그래프나 텍스트가 겹치거나 잘리는 부분을 찾아냅니다. 어색한 부분이 있으면 해당 장면만 수정해 다시 렌더링합니다.
3. **음성을 입히고 최종 출력합니다.** 내레이션이 필요하면 OpenAI나 ElevenLabs로 음성을 생성하고, `*.timings.json`의 타임스탬프에 맞춰 애니메이션 싱크를 맞춥니다. 최종 결과물로 MP4 영상과 썸네일이 생성되며, 내레이션이 포함된 경우 SRT 자막도 함께 제공됩니다. [음성 설정](./docs/manim-starter.md#3-review-and-add-narration-if-you-want-it)

멀티 에이전트 위임(delegation)을 지원하는 환경이라면 레퍼런스 조사, 장면 설계, 초안 검수 역할을 나누어 진행하도록 요청할 수도 있습니다.

## 결과물 구조와 장면 수정

각 장면은 개별 Manim 코드와 대본 파일로 관리됩니다.

```text
videos/ab_test/ko/
├── project.toml              # 참고 자료와 기본 렌더링 장면 설정
├── lesson.md                 # 주제로 시작할 때 작성하는 기획 메모
├── scene_plan.md             # 레퍼런스, 화면 구도, 스토리보드
├── narration/                # 장면별 내레이션 대본
│   ├── 01_question.txt
│   ├── 02_assignment.txt
│   └── 03_comparison.txt
├── scenes/                   # 장면별 Manim 코드
│   ├── scene_01_question.py
│   ├── scene_02_assignment.py
│   └── scene_03_comparison.py
└── build/
    ├── audio/                # MP3 음성과 타이밍 파일
    ├── logs/                 # 렌더링 시도별 로그
    ├── manim/                # 렌더링된 개별 장면
    ├── review/               # 전환 프레임과 비교 시트
    └── final/                # 최종 MP4, 썸네일 PNG, SRT 자막(내레이션 포함 시)
```

> 2번 장면에서 배정이 바뀌는 동안 첫 번째 그룹이 화면에 계속 남아 있게 수정하고, 그 장면만 다시 렌더링해줘.

## Causal Studio 둘러보기

실제 강의에 사용된 대본과 코드는 RDD [한국어 프로젝트](./videos/rdd/ko/)와 [영어 프로젝트](./videos/rdd/en/)에서 확인할 수 있습니다. 교재나 기존 강의 영상을 함께 수정·활용하려면 동일한 스킬이 포함된 전체 저장소를 클론하세요.

```bash
git clone https://github.com/CausalInferenceLab/causal-studio
```

[스킬 보기](./.claude/skills/manim-video-pipeline/SKILL.md) · [기여하기](./CONTRIBUTING-ko_kr.md)

---

이 스킬이 영상 제작에 도움이 되었다면 Causal Studio 저장소에 Star를 눌러주세요.

MIT 라이선스를 따릅니다. 3Blue1Brown 레퍼런스 및 Tabler Icons 등 외부 자산에는 각 원저작자의 라이선스가 적용됩니다.
