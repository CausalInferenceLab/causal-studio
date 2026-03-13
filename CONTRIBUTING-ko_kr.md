# Contributing

[English](./CONTRIBUTING.md) | 한국어

이 프로젝트는 Jupyter Book과 로컬 전용 Manim 영상 워크플로우를 함께 다룹니다. 변경은 작고 명확하게 유지하고, 로컬 개발 환경과 호스팅된 book 환경 모두에서 동작하도록 맞추세요.

## 핵심 규칙

1. 먼저 저장소 스킬을 사용합니다.
   - Codex 워크플로우는 `.codex/skills/`에 있습니다.
   - Claude 브리지 워크플로우는 작업이 해당 트리거와 맞을 때 `.claude/skills/`를 사용합니다.

2. book 의존성과 video 의존성을 분리합니다.
   - `requirements.txt`는 book + video 전체 로컬 작업용 환경입니다.
   - `requirements-book.txt`는 book, Binder, GitHub Pages 스타일 빌드용 최소 런타임입니다.
   - `book/` 아래 노트북이 런타임에서 패키지를 import하면 `requirements-book.txt`도 함께 업데이트합니다.
   - Binder에 시스템 패키지가 필요하면 `binder/apt.txt`를 업데이트합니다.

3. Binder-safe한 노트북 경로를 사용합니다.
   - 현재 작업 디렉터리가 노트북 디렉터리라고 가정하지 않습니다.
   - 저장소 루트 실행과 노트북 로컬 실행 모두에서 동작하는 경로를 우선합니다.
   - book 내부 데이터는 가능하면 `pathlib.Path`와 저장소 루트 기준 경로, 그리고 필요한 경우 로컬 fallback을 사용합니다.

4. 로컬 전용 자산은 로컬 전용으로 취급합니다.
   - `3b1b/`와 `videos/assets/tabler-icons/`는 설정 자산이지 핵심 저장소 콘텐츠가 아닙니다.
   - 변경 목적에 꼭 필요하지 않다면 생성 캐시, 렌더 결과물, 머신 로컬 설정은 커밋하지 않습니다.

5. 수정한 경로를 검증합니다.
   - book 변경: 영향받는 book 콘텐츠를 빌드하거나 그에 준해 검증합니다.
   - Binder 관련 변경: Binder 설정과 노트북 런타임 가정을 함께 점검합니다.
   - video 파이프라인 변경: 임시 셸 스크립트 대신 번들된 스킬 스크립트를 우선 사용합니다.

## 커밋 범위

- 관련 없는 변경은 같은 커밋에 섞지 않습니다.
- `.env`, 로컬 설정, 기타 머신별 파일은 커밋하지 않습니다.
- 배포되는 노트북에 영향을 주는 변경이면 관련 의존성/설정 업데이트를 같은 PR에 포함합니다.
