# 같은 학생의 두 세계 — 태블릿의 효과는 어떻게 알까?

인과추론 입문자를 위한 **한국어 내레이션 세로형 쇼츠**(9:16, 약 47초)입니다.
"성적이 올랐다"는 관찰만으로는 태블릿의 효과를 알 수 없고, 효과는 **같은 학생**이 태블릿을 받은 세계와
받지 않은 세계의 차이인데, 현실에서는 한쪽만 관찰된다는 것, 즉 **반사실(counterfactual)** 개념을 전달합니다.

- 원본 개념: `book/why_causal_inference/why_causal_inference_ko.ipynb` 셀 [5](연관 ≠ 인과), 셀 [8](잠재적 결과·사실/반사실)
- 참고 영상 코드: `videos/why_causal_inference/src/why_causal_inference.py`의 `Scene03_CounterfactualWorlds`

## Scene 구성

| # | 클래스 | 핵심 메시지 | 음성 길이 |
|---|---|---|---|
| 01 | `Scene01_Question` | 성적이 올랐다는 사실만으로는 태블릿 덕분인지 알 수 없다 | 15.4초 |
| 02 | `Scene02_TwoWorlds` | 효과는 같은 학생의 두 세계(받음/안 받음)의 성적 차이다 | 13.6초 |
| 03 | `Scene03_Counterfactual` | 현실에선 한 세계만 보인다. 일어나지 않은 쪽의 결과가 반사실이다 | 17.1초 |

화면 문법(전 Scene 공통): 학생 = 흰색 아이콘 하나(서로 다른 학생을 비교하지 않음),
태블릿(처치) = 청록, 성적(결과) = 노랑, 아직 모름/반사실 = 주황, 보조 = 회색. 수식은 쓰지 않습니다.
성적 막대는 숫자 없는 **가상 예시**이며 화면에도 그렇게 표시합니다.

## 파일 구성

```text
videos/counterfactual_short_kwonhwijun/
├── README.md
├── src/
│   ├── counterfactual_short_ko.py      # Manim CE Scene 3개 (9:16 설정은 이 파일에만 적용)
│   └── scripts/ko/
│       ├── 01_question.txt             # 실제로 읽는 내레이션만 (빈 줄 = 청크 경계)
│       ├── 02_two_worlds.txt
│       └── 03_counterfactual.txt
├── build/                              # git 제외 — 생성물
│   ├── audio/NN_name.mp3, NN_name.timings.json
│   ├── manim/                          # Manim 중간 산출물
│   └── final/NN_name_hq.mp4, counterfactual_short_ko.mp4
└── preview/NN_name_mux.mp4             # git 제외 — 480p 확인용
```

`build/`, `preview/`, 생성된 음성·영상·`timings.json`은 Git에 포함하지 않습니다.

## 필요한 환경

- 프로젝트 `.venv` (`bash scripts/setup_environment.sh`로 준비, Manim CE 포함)
- 로컬 자산: `videos/assets/tabler-icons/` (`video-assets-setup` 스킬로 설치)
- 한글 폰트: **Pretendard** (`Pretendard Variable` family로 설치되어 있어야 함)
- Node.js + `.claude/skills/manim-video-pipeline/node_modules`
- 환경변수
  - `OPENAI_API_KEY` (필수) — 셸 환경변수 또는 저장소 루트 `.env`에 `OPENAI_API_KEY=...`. **키를 소스나 README에 쓰지 마세요.**
  - `OPENAI_TTS_VOICE`, `OPENAI_TTS_INSTRUCTIONS` (선택) — 이번 영상은 설정하지 않고 프로젝트 기본값(voice `coral`) 사용

## 재현 명령

모든 명령은 저장소 루트 기준입니다.

### 1) 음성 생성 (OpenAI TTS)

```bash
cd .claude/skills/manim-video-pipeline
for s in 01:question 02:two_worlds 03:counterfactual; do
  n=${s%%:*}; name=${s#*:}
  # 먼저 입력·출력 경로 확인
  npm run openai-audio -- --topic counterfactual_short_kwonhwijun --scene $n --name $name \
    --script ../../../videos/counterfactual_short_kwonhwijun/src/scripts/ko/${n}_${name}.txt --dry-run
  # 실제 생성 → build/audio/${n}_${name}.mp3, .timings.json
  npm run openai-audio -- --topic counterfactual_short_kwonhwijun --scene $n --name $name \
    --script ../../../videos/counterfactual_short_kwonhwijun/src/scripts/ko/${n}_${name}.txt
done
cd -
```

`timings.json`은 **청크(빈 줄로 나눈 문단) 단위** 타이밍입니다. 단어·음절 단위가 아니며,
Scene 코드는 각 청크의 `end` 시각에 맞춰 Beat를 넘깁니다(`load_chunk_ends`, `wait_until`).
TTS 결과는 생성할 때마다 길이가 조금씩 달라지므로, 음성을 다시 만들면 렌더도 다시 해야 합니다.

### 2) 확인용 저해상도 렌더 + 음성 합성 (480×854)

```bash
cd videos/counterfactual_short_kwonhwijun
../../.venv/bin/manim -ql --media_dir build/manim src/counterfactual_short_ko.py \
  Scene01_Question Scene02_TwoWorlds Scene03_Counterfactual
M=../../.claude/skills/manim-video-pipeline/scripts/mux_audio.sh
L=build/manim/videos/counterfactual_short_ko/854p15
$M $L/Scene01_Question.mp4       build/audio/01_question.mp3       preview/01_question_mux.mp4
$M $L/Scene02_TwoWorlds.mp4      build/audio/02_two_worlds.mp3     preview/02_two_worlds_mux.mp4
$M $L/Scene03_Counterfactual.mp4 build/audio/03_counterfactual.mp3 preview/03_counterfactual_mux.mp4
```

### 3) 최종 렌더 (720×1280, 30fps) + Scene별 고화질 합성

```bash
cd videos/counterfactual_short_kwonhwijun
../../.venv/bin/manim -r 720,1280 --fps 30 --media_dir build/manim src/counterfactual_short_ko.py \
  Scene01_Question Scene02_TwoWorlds Scene03_Counterfactual

H=build/manim/videos/counterfactual_short_ko/1280p30
mkdir -p build/final && rm -f build/final/*.mp4   # 합본 도구가 폴더 안 mp4를 모두 잇기 때문에 먼저 비운다
for p in 01_question:Scene01_Question 02_two_worlds:Scene02_TwoWorlds 03_counterfactual:Scene03_Counterfactual; do
  a=${p%%:*}; s=${p#*:}
  # 렌더 길이 ≥ mp3 길이인지 먼저 확인 (짧으면 코드의 TAIL_PAD/타이밍을 고치고 재렌더)
  ffprobe -v error -show_entries format=duration -of csv=p=0 $H/$s.mp4 build/audio/$a.mp3
  # 음성 뒤를 무음으로 채운 뒤(apad) 영상 길이에서 자른다(-shortest)
  ffmpeg -y -i $H/$s.mp4 -i build/audio/$a.mp3 -filter_complex "[1:a]apad[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest build/final/${a}_hq.mp4
done
```

> 왜 `mux_audio.sh --shortest` 대신 `apad + -shortest`인가:
> `mux_audio.sh --shortest`로 합성하면 AAC 프레임 단위 때문에 Scene마다 음성 트랙이 영상보다 5~75ms 길게 남고,
> `-c copy` 합본에서 이 차이가 누적되어 Scene 03 음성이 영상보다 **232ms** 늦어졌습니다.
> 음성을 영상 길이에 정확히 맞추면 누적이 사라집니다(아래 검증 결과).
> `-shortest` 규칙(영상과 음성 중 짧은 쪽에 맞춤)은 그대로 지킵니다.

### 4) 합본 (01 → 02 → 03, BGM 없음)

```bash
cd videos/counterfactual_short_kwonhwijun
../../.claude/skills/manim-video-pipeline/scripts/concat_videos.sh build/final build/final/counterfactual_short_ko.mp4
```

주의: `concat_videos.sh`는 `build/final/`의 **모든 mp4를 파일명 순서로** 잇습니다. 다시 실행할 때는
기존 `counterfactual_short_ko.mp4`를 먼저 지우세요. 또한 직접 연결이 실패해 재인코딩으로 넘어가면 1280×720 **가로**로
변환되므로, 세 Scene의 해상도·fps·코덱을 반드시 같게 맞춥니다.

## 검증 결과 (2026-10-19)

| 항목 | 결과 |
|---|---|
| 해상도·fps | 720×1280, 30fps (세 Scene과 최종본 모두 동일, 재인코딩 없이 직접 연결) |
| 전체 길이 | **46.6초** (영상 46.63초, 음성 46.65초) — 목표 35~45초보다 약 1.6초 김 |
| Scene별 영상−음성 차이 | +0.027 / +0.028 / +0.030초 (모두 0.1초 이내) |
| 음성 싱크 (영상 컷 대비 음성 시작) | +43ms / +59ms / +73ms (경계마다 약 15ms 누적, 이전 방식은 +232ms) |
| 경계 클릭·끊김 | 경계 ±50ms 샘플 변화 0.0000, 경계 직전·직후 프레임 동일(이전 Scene 마지막 화면에서 다음 Scene 시작) |
| 레이아웃 | 대표 프레임 QA에서 과밀 2건(Scene 01 물음표 영역, Scene 03 흐림 처리) 수정 후 겹침·잘림 없음 |

길이 초과 수정안(음성 가속 없이): Scene 03 마지막 청크를 "일어나지 않은 쪽의 결과, 이것이 반사실입니다."처럼
줄이거나 Scene 02 마지막 청크의 "이 학생에게"를 빼면 약 1~2초 줄어듭니다. (스크립트 변경은 승인 후 반영)

## 사용한 자산과 출처

- **아이콘**: [Tabler Icons](https://tabler.io/icons) (MIT License) — `user`, `device-tablet`, `trending-up`,
  `question-mark`, `eye-off` (outline). 로컬 `videos/assets/tabler-icons/`에서 불러오며 저장소에는 포함하지 않습니다.
- **폰트**: [Pretendard](https://github.com/orioncactus/pretendard) (SIL Open Font License 1.1), 로컬 설치본 사용.
- **연출 참고**: 3Blue1Brown `3b1b/_2020/covid.py`(IntroQuestion), `3b1b/_2018/uncertainty.py` — 화면 리듬·대비 방식만
  참고했고 코드는 Manim CE로 새로 작성했습니다.
- **개념·예시**: 본 저장소 노트북 `why_causal_inference_ko.ipynb` (Facure, *Causal Inference for the Brave and True* 1장 기반).

## AI 생성 음성 고지

이 영상의 내레이션은 **OpenAI TTS로 생성한 AI 음성**입니다 (모델 `gpt-4o-mini-tts`, voice `coral`).
사람 성우의 녹음이 아니며, 공개 시 설명란 등에 AI 생성 음성임을 밝혀 주세요.
