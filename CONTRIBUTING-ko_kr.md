# 기여하기

[English](./CONTRIBUTING.md)

## 환경 설정

저장소 루트에서 실행하세요.

```bash
bash scripts/setup_environment.sh
source .venv/bin/activate
```

교재만 작업하려면 `--book-only`, 영상만 작업하려면 `--video-only`를 붙이세요. 영상 전용 환경은 `.venv-video`에 생성됩니다.

## PR 올리기

- `main`에서 브랜치를 만들고 하나의 변경에 집중하세요.
- **교재** — 수정한 노트북을 처음부터 끝까지 실행하고 교재 출력을 확인하세요. 경로와 의존성은 Binder에서도 동작해야 합니다.
- **영상** — 수정한 장면을 렌더링해 확인하세요. 공용 Manim 스킬을 수정할 때는 [유지보수 가이드](./.claude/skills/manim-skill-maintenance/SKILL.md)를 따르세요.
- PR에는 변경 내용과 확인 방법을 적으세요.

API 키와 생성 결과물은 로컬에 두세요. 의존성 파일과 저장소 스킬은 [저장소 작업 규칙](./AGENTS.md)을 참고하세요.
