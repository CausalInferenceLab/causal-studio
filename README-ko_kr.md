# Causal Studio

[English](./README.md) | 한국어

인과추론 코드북(Jupyter Book)과 Manim 교육 영상을 함께 관리하는 저장소입니다.

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

## 스킬

| 스킬 | 용도 |
|---|---|
| `python-setup` | `.venv` 생성 및 초기 의존성 설치 |
| `video-assets-setup` | `3b1b/`, `tabler-icons/` 로컬 자산 설치·업데이트 |
| `pip-install` | `.venv`에 패키지 설치 후 `requirements.txt` 동기화 |
| `book-serve` | Jupyter Book 로컬 서버 실행 |
| `book-publish` | 노트북을 book TOC에 추가하고 빌드 검증 |
| `ipynb-to-english` | 한국어 노트북을 영어 `_en.ipynb`로 번역 |
| `ipynb-youtube-embed` | 노트북에 YouTube iframe 임베드 (Jupyter Book 렌더링을 위해 outputs까지 저장) |
| `manim-video-pipeline` | scene 설계 / 스크립트 / 렌더 / 오디오 / mux / 합본 전 과정 |
| `manim-thumbnail` | Manim으로 3b1b 스타일 YouTube 썸네일 PNG 생성 |
| `git-commit` | 변경 분석 및 커밋 |
| `git-pr` | PR 생성 |
| `skill-creator` | 프로젝트 스킬 생성·수정 |

## CI/CD

`main` 브랜치에 `book/**` 변경사항이 push되면 GitHub Actions가 자동으로 GitHub Pages에 배포합니다.

배포 의존성: `requirements-book.txt`

## 라이선스

이 저장소는 MIT입니다. 외부 자산(3b1b, Tabler Icons)은 각 upstream 라이선스를 따릅니다.
