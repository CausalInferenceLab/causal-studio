<a id="top"></a>

# Causal Studio

🌐 Language: [English](./README.md) | 한국어

인과추론에 관한 교육 영상과 실행 가능한 노트북을 제공하는 플랫폼입니다.

- Book: <https://causalinferencelab.github.io/causal-studio/>
- YouTube: <https://www.youtube.com/@CausalStudio>

작업 규칙: [English](./CONTRIBUTING.md) | [한국어](./CONTRIBUTING-ko_kr.md)

## 학습 방법

1. 영상을 먼저 보기: 각 장의 명확한 애니메이션으로 개념을 시각적으로 이해합니다.
2. 코드를 직접 실행하기: Binder 또는 Colab에서 코드를 돌리며 손으로 익힙니다.
3. 더 깊게 보기: 노트북의 자세한 설명과 코드를 통해 개념을 완전히 정리합니다.

## 저장소 구조

```text
causal_studio/
├── book/
│   └── why_causal_inference/        한·영 노트북
├── videos/
│   └── why_causal_inference/
│       └── src/                     Scene 코드 + 나레이션 스크립트
├── .codex/skills/                   Codex 스킬
├── .claude/skills/                  Claude Code 스킬
├── requirements.txt                 전체 의존성 (book + video)
└── requirements-book.txt            book 전용 (CI/배포)
```

## 환경 세팅

새 환경에서 처음 클론한 경우:

```text
이 저장소 Python 환경 세팅해줘      → python-setup 스킬
영상 작업용 로컬 자산 설치해줘      → video-assets-setup 스킬
```

`video-assets-setup`은 아래 두 저장소를 로컬에 clone합니다 (git 미추적):
- `3b1b/` — 3b1b/videos 참조용
- `videos/assets/tabler-icons/` — Tabler Icons 아이콘셋

## CI/CD

`main` 브랜치에 `book/**` 변경사항이 push되면 GitHub Actions가 자동으로 GitHub Pages에 배포합니다.

배포 의존성: `requirements-book.txt`

## Our Contributors

<a href="https://github.com/CausalInferenceLab/causal-studio/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=CausalInferenceLab/causal-studio" />
</a>

<p align="right">
  <a href="#top">⬆️ Back to Top</a>
</p>

## 라이선스

이 저장소는 MIT입니다. 외부 자산(3b1b, Tabler Icons)은 각 upstream 라이선스를 따릅니다.
