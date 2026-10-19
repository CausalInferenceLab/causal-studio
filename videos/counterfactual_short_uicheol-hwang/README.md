# 같은 학생의 두 세계 — 태블릿의 효과는 어떻게 알까?

인과추론 입문자를 위한 한국어 세로형 쇼츠입니다. 태블릿을 받은 뒤 성적이 올랐다는 관찰에서 출발해, **같은 학생**의 두 가능한 세계를 비교해야 함을 보여줍니다. 실제로 태블릿을 받았다면 받지 않았을 때의 결과는 관찰할 수 없는 반사실입니다. 점수나 수식은 사용하지 않았고 배경음악도 없습니다.

## 파일 구성

- `src/scripts/ko/01_tablet_question.txt`, `02_two_worlds.txt`, `03_counterfactual.txt`: Scene별 실제 내레이션
- `src/counterfactual_short_ko.py`: Manim CE Scene 01–03, 공통 화면 설정과 아이콘 배치
- `build/audio/`: 생성한 MP3와 `.timings.json` (Git 제외)
- `build/manim/`: 렌더 중간 파일 (Git 제외)
- `build/final/`: Scene별 음성 합성본과 최종 영상 (Git 제외)
- `preview/`: 확인용 영상 (Git 제외)

`.timings.json`의 `start`/`end`는 **내레이션 문단 청크 단위** 시간입니다. 단어별 강제 정렬이나 자막 타임코드가 아닙니다. 영상 코드는 이 시간을 화면 전환의 기준으로 사용합니다.
TTS를 다시 생성하면 같은 스크립트라도 음성 길이가 달라질 수 있으므로 새 `.timings.json`과 렌더 길이를 확인한 뒤 Scene의 `wait` 시간을 조정해야 합니다.

## 재현

저장소 루트에서 실행합니다. 프로젝트 `.venv`, Node.js, ffmpeg/ffprobe, Manim CE, 공용 Tabler Icons와 `Apple SD Gothic Neo` 한글 폰트가 필요합니다. 프로젝트의 오디오 명령은 루트 `.env`를 읽으므로 그 파일에 `OPENAI_API_KEY`를 설정해야 합니다. `.env`는 Git에서 제외됩니다. 선택적으로 `OPENAI_TTS_VOICE`, `OPENAI_TTS_INSTRUCTIONS`를 지정할 수 있으며, 기본 모델·voice는 프로젝트 오디오 명령의 설정을 따릅니다.

```bash
cd .claude/skills/manim-video-pipeline
for item in 01:tablet_question 02:two_worlds 03:counterfactual; do
  scene=${item%%:*}; name=${item#*:}
  script="../../../videos/counterfactual_short_uicheol-hwang/src/scripts/ko/${scene}_${name}.txt"
  npm run openai-audio -- --topic counterfactual_short_uicheol-hwang --scene "$scene" --name "$name" --lang ko --script "$script" --dry-run
  npm run openai-audio -- --topic counterfactual_short_uicheol-hwang --scene "$scene" --name "$name" --lang ko --script "$script"
done
```

다음 명령은 기존에 생성한 음성을 사용해 모든 Scene을 720×1280, 30fps로 렌더하고 `--shortest`로 합성합니다. 영상이 음성보다 짧다면 합성으로 숨기지 말고 Scene 타이밍을 고쳐 다시 렌더합니다.

```bash
cd videos/counterfactual_short_uicheol-hwang
../../.venv/bin/manim -qh --disable_caching --media_dir build/manim -o 01_tablet_question_hq.mp4 src/counterfactual_short_ko.py Scene01_TabletQuestion
../../.venv/bin/manim -qh --disable_caching --media_dir build/manim -o 02_two_worlds_hq.mp4 src/counterfactual_short_ko.py Scene02_TwoWorlds
../../.venv/bin/manim -qh --disable_caching --media_dir build/manim -o 03_counterfactual_hq.mp4 src/counterfactual_short_ko.py Scene03_Counterfactual

mkdir -p build/final
for item in 01:tablet_question 02:two_worlds 03:counterfactual; do
  scene=${item%%:*}; name=${item#*:}
  ../../.claude/skills/manim-video-pipeline/scripts/mux_audio.sh \
    "build/manim/videos/counterfactual_short_ko/1280p30/${scene}_${name}_hq.mp4" \
    "build/audio/${scene}_${name}.mp3" \
    "build/final/${scene}_${name}_hq.mp4" --shortest
done

# 합본 도구가 디렉터리의 모든 MP4를 읽으므로 기존 최종본은 먼저 제거합니다.
rm -f build/final/counterfactual_short_ko.mp4
../../.claude/skills/manim-video-pipeline/scripts/concat_videos.sh \
  build/final build/final/counterfactual_short_ko.mp4
```

## 자산과 출처

- 개념 설명: [`book/why_causal_inference/why_causal_inference_ko.ipynb`](../../book/why_causal_inference/why_causal_inference_ko.ipynb)
- 기존 영상 표현 참고: [`videos/why_causal_inference/src/why_causal_inference.py`](../why_causal_inference/src/why_causal_inference.py)
- 아이콘: 공용 로컬 자산 `videos/assets/tabler-icons/`의 [Tabler Icons](https://tabler.io/icons), MIT License
- 폰트: 로컬 설치 `Apple SD Gothic Neo`
- 내레이션: OpenAI TTS로 AI 생성한 음성입니다.
