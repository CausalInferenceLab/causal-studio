---
name: "source-command-commit"
description: "변경사항을 분석하고 커밋 생성"
---

# source-command-commit

Use this skill when the user asks to run the migrated source command `commit`.

## Command Template

현재 Git 상태를 확인하고 커밋을 생성하세요.

## 프로젝트 커밋 규칙

```
feat: 새로운 기능 추가
fix: 버그 수정
docs: 문서 수정
style: 코드 포맷팅
refactor: 코드 리팩토링
test: 테스트 코드
chore: 빌드 업무 수정
```

## 작업 순서

1. `git status`로 변경된 파일 확인
2. `git diff`로 변경 내용 분석
3. `git log --oneline -5`로 최근 커밋 스타일 참고
4. 변경사항에 맞는 커밋 타입 선택
5. 한글로 간결한 커밋 메시지 작성
6. 사용자에게 커밋 메시지 제안 후 승인받으면 커밋 실행

## 커밋 메시지 형식

```
<type>: <description>

Co-Authored-By: Codex Opus 4.5 <noreply@anthropic.com>
```

## 주의사항

- .env, credentials 등 민감한 파일은 커밋하지 않기
- 커밋 전 사용자 승인 필수
- `--amend`, `--force` 옵션 사용 금지
