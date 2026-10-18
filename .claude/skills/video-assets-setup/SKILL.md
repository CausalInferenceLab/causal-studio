---
name: video-assets-setup
description: Clone, update, or validate local-only 3Blue1Brown references and Tabler Icons. Use during full initial setup, when video references or icons are missing, or when asked to install or update video assets.
---

# Video Assets Setup

저장소 루트에서 모든 스킬 사본이 공유하는 스크립트를 실행한다.

```bash
bash scripts/setup_video_assets.sh
```

- `https://github.com/3b1b/videos.git`를 `3b1b/`에 직접 clone한다.
- `https://github.com/tabler/tabler-icons.git`를 `videos/assets/tabler-icons/`에 clone한다.
- 기존 Git 저장소는 `git pull --ff-only`로 갱신한다. Git 저장소가 아닌 기존 경로는 건너뛰지 말고 실패로 보고하며 임의로 삭제하지 않는다.
- 두 경로는 `.gitignore`로 관리하는 로컬 전용 자산이다.
- 전체 초기 세팅에서는 `python-setup`의 공통 스크립트가 이 단계를 반드시 실행한다.

## 완료 검증

```bash
bash scripts/setup_video_assets.sh --check
```

이 명령은 네트워크 갱신 없이 두 Git 저장소와 아래 파일을 확인한다.

- `3b1b/_2020/covid.py` (`3b1b/videos/`가 아님)
- `videos/assets/tabler-icons/icons/outline/device-tablet.svg`

두 검증을 모두 통과한 경우에만 준비 완료로 보고하고 `manim-video-pipeline`으로 진행한다. clone, pull 또는 필수 파일 검증 실패 시 누락 상태와 실패 원인을 보고한다.
