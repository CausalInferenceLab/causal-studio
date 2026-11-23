# Causal Studio

[English](./README.md)

**Claude Code나 Codex에 아이디어, 강의 원고, 노트북을 주고 Manim 설명 영상을 만들어 보세요.**

Causal Studio는 인과추론 애니메이션과 실행 가능한 노트북을 제공하고, 영상 제작에 사용한 스킬을 공유합니다.

**[첫 영상 만들기](#첫-영상-만들기)** · [영상 보기](https://www.youtube.com/@CausalStudio) · [노트북 열기](https://causalinferencelab.github.io/causal-studio/)

[![장학금 기준인 370점 양쪽의 GPA 산점도와 회귀선을 보여주는 RDD 장면](./docs/assets/rdd-preview.jpg)](https://www.youtube.com/watch?v=65C9J1yJwhc)

## 첫 영상 만들기

1. Causal Studio를 클론합니다.

   ```bash
   git clone https://github.com/CausalInferenceLab/causal-studio.git
   ```

2. 클론한 폴더를 Claude Code나 Codex에서 열고 아래 요청을 붙여넣습니다.

   ```text
   manim-video-pipeline 스킬로 중학생 대상 광합성 설명 영상의 첫 장면을 만들어줘.
   필요한 영상 환경도 준비하고, 음성 없이 확인할 수 있는 MP4를 보여줘.
   ```

3. 미리보기를 보고 바꾸고 싶은 부분을 말합니다. 예를 들어 자막을 조금 더 오래 보여달라고 요청할 수 있습니다.

자기 영상은 주제 한 줄로 시작하거나 Markdown, 텍스트, `.ipynb` 파일 경로를 알려주면 됩니다. 무음 미리보기에는 음성 합성 API 키가 필요 없습니다. [예제 프롬프트와 음성 추가 방법](./docs/manim-starter.md)

<details>
<summary>Manim 스킬만 클론하기</summary>

```bash
git clone --branch skill-only --single-branch --depth 1 https://github.com/CausalInferenceLab/causal-studio.git causal-studio-skill
```

`causal-studio-skill`을 Claude Code나 Codex에서 열고 같은 프롬프트를 붙여넣습니다.

</details>

---

[기여 가이드와 전체 환경 설정](./CONTRIBUTING-ko_kr.md) · [Manim 스킬](./.claude/skills/manim-video-pipeline/SKILL.md)

영상 제작에 도움이 됐다면 GitHub에서 스타를 눌러주세요.

MIT. 외부 자산(3Blue1Brown 레퍼런스와 Tabler Icons)은 각자의 라이선스를 따릅니다.
