---
name: git-pr
description: 현재 브랜치 변경사항을 분석하고 GitHub Pull Request를 생성한다. Use when asked to inspect branch status, verify PR commits against main, push a feature branch, or run gh pr create with assignee and a structured body.
---

# Git Pr

현재 브랜치의 변경사항을 분석하고 GitHub Pull Request를 생성한다.

직접적인 `git` / `gh` 명령을 우선 사용한다. 이 프로젝트의 PR base 브랜치는 항상 `main`이다.

## 기본 원칙

- 커밋되지 않은 변경사항이 있으면 PR 생성 전에 먼저 커밋을 안내한다.
- `main`에서 직접 PR을 만들지 않는다. 항상 feature 브랜치에서 PR을 생성한다.
- PR 생성 시 `--assignee @me`를 사용한다.
- PR 생성이 끝나면 PR URL을 반환한다.
- `reset --hard` 또는 `push --force-with-lease`가 필요한 경우에는 실행 전에 반드시 사용자 승인을 받는다.

## 확인 명령어

```bash
git status
git branch --show-current
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'
git log origin/main..HEAD --oneline
git diff origin/main...HEAD
```

## 작업 순서

1. `git status`로 커밋되지 않은 변경사항이 있는지 확인한다.
2. 변경사항이 남아 있으면 PR 생성 대신 먼저 커밋하라고 안내하고 멈춘다.
3. `git branch --show-current`로 현재 브랜치를 확인한다.
4. `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`으로 기본 브랜치를 확인하되, 이 프로젝트의 PR base는 항상 `main`으로 사용한다.
5. 현재 브랜치가 `main`인지 확인한다.
6. 현재 브랜치가 `main`이면 아래 "feature 브랜치 생성 절차"를 따른다.
7. `git log origin/main..HEAD --oneline`으로 PR에 포함될 커밋을 검토한다.
8. `git diff origin/main...HEAD`로 전체 변경사항을 분석한다.
9. 현재 feature 브랜치를 `git push -u origin <feature-branch>`로 푸시한다.
10. PR 제목과 본문을 작성한 뒤 `gh pr create`를 실행한다.
11. 생성된 PR URL을 사용자에게 전달한다.

## Feature 브랜치 생성 절차

현재 브랜치가 `main`인 경우에만 사용한다.

브랜치 이름은 커밋 타입/스코프 패턴을 사용한다.

- `feat/user-auth`
- `fix/login-bug`
- `chore/claude-commands`

필수 절차:

```bash
# 1. base 기준으로 새 feature 브랜치 생성
git checkout -b <type>/<scope> HEAD~<commit-count>

# 2. 대상 커밋 cherry-pick
git cherry-pick <commit-hash>

# 3. 원래 base 브랜치에서 해당 커밋 제거
git checkout main
git reset --hard HEAD~<commit-count>
git push --force-with-lease origin main

# 4. feature 브랜치로 돌아와 push
git checkout <feature-branch>
git push -u origin <feature-branch>
```

`git reset --hard` 와 `git push --force-with-lease` 는 파괴적이므로, 실제 실행 전 사용자 승인 없이는 수행하지 않는다.

## PR 제목 규칙

커밋 메시지와 동일한 prefix를 사용한다.

- `feat: 새로운 기능 설명`
- `fix: 버그 수정 설명`
- `docs: 문서 수정 설명`
- `refactor: 리팩토링 설명`
- `chore: 기타 작업 설명`

## PR 본문 템플릿

```bash
gh pr create --title "제목" --base main --body "$(cat <<'EOF'
### SUMMARY
- 항목 1
- 항목 2

### TESTING INSTRUCTIONS
- [ ] 테스트 항목 1
- [ ] 테스트 항목 2

🤖 Generated with [Codex](https://chatgpt.com/codex)
EOF
)" --assignee @me
```

## 작성 기준

- PR 제목은 커밋 prefix를 유지하면서 간결하게 쓴다.
- `SUMMARY`에는 사용자 관점의 변경사항을 1-3개 bullet로 정리한다.
- `TESTING INSTRUCTIONS`에는 검증 가능한 체크 항목을 넣는다.
- 사용자가 별도 요청하지 않으면 draft PR을 기본값으로 사용하지 않는다.