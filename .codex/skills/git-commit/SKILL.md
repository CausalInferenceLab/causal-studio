---
name: git-commit
description: 변경사항을 분석하고 작업 단위별로 커밋을 준비한다. Use when asked to inspect git changes, split work into coherent commits, suggest a commit message, stage files, or run git commit.
---

# Git Commit

현재 Git 상태를 확인하고, 변경사항을 논리적인 작업 단위로 나눈 뒤 커밋을 생성한다.

## Allowed Git Commands

```bash
git status --short
git diff --stat
git diff
git log --oneline -5
git add <files>
git commit
```

## 프로젝트 커밋 규칙

```bash
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 코드
chore: 빌드 업무 수정
```

## 작업 순서

1. `git status`로 변경된 파일을 확인한다.
2. `git diff`와 `git diff --stat`로 변경 내용을 분석한다.
3. `git log --oneline -5`로 최근 커밋 스타일을 참고한다.
4. 변경사항을 논리적인 작업 단위로 나눈다.
   - 관련 없는 수정은 한 커밋에 섞지 않는다.
   - 필요한 경우 파일 단위 또는 hunk 단위로 나눠 스테이징한다.
5. 각 작업 단위에 맞는 커밋 타입을 선택한다.
6. 한글로 간결한 커밋 메시지를 작성해 사용자에게 먼저 제안한다.
7. 사용자 승인 후에만 `git add`와 `git commit`을 실행한다.

## 커밋 메시지 형식

```text
<type>(<scope>): <description>
```

- `<scope>`는 선택사항이다.
- 범위가 분명하지 않으면 scope 없이 써도 된다.
- 메시지는 한글로 짧고 명확하게 쓴다.

## 주의사항

- `.env`, credentials 등 민감한 파일은 커밋하지 않는다.
- 커밋 전 사용자 승인 필수.
- `git add -A`를 기본값처럼 사용하지 않는다. 커밋 대상이 명확할 때만 필요한 파일을 선택적으로 스테이징한다.
- `--amend`, `--force` 옵션은 사용하지 않는다.
- 이미 작업 트리에 여러 성격의 수정이 섞여 있다면, 먼저 어떤 단위로 나눌지 사용자에게 제안한다.