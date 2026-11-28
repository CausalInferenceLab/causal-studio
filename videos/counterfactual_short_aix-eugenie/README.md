# 같은 학생의 두 세계 — 태블릿의 효과는 어떻게 알까?

인과추론 입문자를 위한 한국어 내레이션 세로형 쇼츠입니다.
한 학생의 성적이 오른 장면에서 출발해, 같은 학생의 "태블릿을 받은 세계 / 받지 않은 세계"를 비교하고,
현실에서는 한쪽 결과만 관찰되며 다른 쪽은 반사실(counterfactual)로 남는다는 점을 보여 줍니다.

| 항목 | 값 |
|---|---|
| 화면 | 9:16 세로, 720×1280, 30fps, 검정 배경 |
| 길이 | 약 40.2초 (Scene 3개) |
| 음성 | 한국어 AI 합성 음성 (OpenAI `gpt-4o-mini-tts`, voice `coral`) |
| 배경음악 | 없음 |
| 최종 파일 | `build/final/counterfactual_short_ko.mp4` (git 추적 제외) |

## Scene 구성

| Scene | 클래스 | 핵심 메시지 | 스크립트 | 음성 길이 |
|---|---|---|---|---|
| 01 질문 | `Scene01_TabletQuestion` | 성적이 올랐다는 사실만으로는 태블릿 덕분이라고 말할 수 없다 | `src/scripts/ko/01_tablet_question.txt` | 10.08초 |
| 02 비교 | `Scene02_TwoWorlds` | 태블릿의 효과는 같은 학생의 두 세계의 성적 차이다 | `src/scripts/ko/02_two_worlds.txt` | 15.41초 |
| 03 핵심 | `Scene03_OneWorldObserved` | 현실에서는 한 세계만 관찰되고, 받지 않았을 때의 성적은 반사실이다 | `src/scripts/ko/03_one_world_observed.txt` | 14.78초 |

- 화면에는 숫자 점수를 쓰지 않고 막대 높이로만 성적을 표현합니다.
- 서로 다른 학생을 비교하지 않습니다. 등장하는 학생은 한 명이며 Scene 02~03에서 같은 아이콘이 두 세계로 복제될 뿐입니다.
- 각 Scene의 핵심 주장, 노트북 참고 셀, 스크립트-Beat 대응, Beat별 화면 구획은 `src/counterfactual_short_ko.py`의 Scene docstring과 주석에 있습니다.

## 파일 구성

```text
videos/counterfactual_short_aix-eugenie/
├── README.md
├── src/
│   ├── counterfactual_short_ko.py      # Manim CE Scene 3개 + 이 영상 전용 9:16 설정
│   └── scripts/ko/                     # 내레이션 원문 (TTS 입력, 실제로 읽는 문장만)
│       ├── 01_tablet_question.txt
│       ├── 02_two_worlds.txt
│       └── 03_one_world_observed.txt
├── build/                              # gitignore (videos/*/build/)
│   ├── audio/{NN}_{name}.mp3           # TTS 음성
│   ├── audio/{NN}_{name}.timings.json  # 청크 단위 타이밍
│   ├── manim/                          # Manim 중간 산출물 (480p15 확인용, 1280p30 최종용)
│   └── final/
│       ├── {NN}_{name}_hq.mp4          # Scene별 고화질 + 음성
│       └── counterfactual_short_ko.mp4 # 최종 합본
└── preview/                            # gitignore (videos/*/preview/), 480p 확인용 mux
```

커밋 대상은 `README.md`, `src/` 아래 파일뿐입니다. 음성·렌더·합본 결과물은 모두 위 명령으로 다시 만들 수 있습니다.

## 필요한 환경

- 프로젝트 `.venv` (Python 3.11, Manim CE 0.22.0): `bash scripts/setup_environment.sh`
- 로컬 자산 `videos/assets/tabler-icons/`: 위 setup 스크립트가 함께 받습니다 (git 추적 제외)
- Node.js (`process.loadEnvFile` 지원 버전, 20.12 이상), `ffmpeg`, `ffprobe`
- 한글 폰트 `Apple SD Gothic Neo` (macOS 시스템 폰트). 다른 OS에서는 `src/counterfactual_short_ko.py`의 `FONT`를 설치된 한글 폰트로 바꿔야 합니다.

### 환경변수

| 변수 | 필수 | 설명 |
|---|---|---|
| `OPENAI_API_KEY` | 예 | OpenAI TTS API 키. 저장소 루트 `.env`에 `OPENAI_API_KEY=...` 형식으로 둡니다. |
| `OPENAI_TTS_VOICE` | 아니요 | 기본값 `coral`. 이 영상은 기본값으로 만들었습니다. |
| `OPENAI_TTS_INSTRUCTIONS` | 아니요 | 톤 지시문. 이 영상은 지정하지 않았습니다(빈 값). |

- 음성 생성 스크립트는 저장소 루트의 `.env`를 항상 읽습니다. 셸 환경변수에 `OPENAI_API_KEY`가 있으면 그 값이 우선하지만, `.env` 파일 자체가 없으면 실행이 실패합니다.
- `.env`는 `.gitignore`에 포함되어 있습니다. 키 값을 출력하거나 소스·README·커밋에 넣지 마세요.

## 재현 명령

1단계는 저장소 루트에서 시작하고, 2~5단계는 작업 폴더(`videos/counterfactual_short_aix-eugenie/`)에서 실행합니다.

### 1. 음성 생성 (mp3 + timings.json)

프로젝트 Skill의 `openai-audio` 명령을 씁니다. 먼저 `--dry-run`으로 입력·출력 경로와 청크를 확인한 뒤 실제로 생성합니다.
이 영상과 같은 기본값을 쓰려면 `OPENAI_TTS_VOICE`, `OPENAI_TTS_INSTRUCTIONS`를 비운 채 실행합니다.

```bash
cd .claude/skills/manim-video-pipeline
for n in 01_tablet_question 02_two_worlds 03_one_world_observed; do
  env -u OPENAI_TTS_VOICE -u OPENAI_TTS_INSTRUCTIONS npm run --silent openai-audio -- \
    --topic counterfactual_short_aix-eugenie --scene "${n%%_*}" --name "${n#*_}" \
    --script ../../../videos/counterfactual_short_aix-eugenie/src/scripts/ko/$n.txt --dry-run
done
# 확인 후 같은 명령에서 --dry-run을 빼고 실행
cd ../../..
```

TTS는 실행할 때마다 억양과 길이가 조금씩 달라질 수 있습니다. 다시 생성했다면 아래 "길이 검증"을 다시 통과해야 합니다.

### 2. 저해상도 확인 렌더 + 확인용 mux (480×854, 15fps)

```bash
cd videos/counterfactual_short_aix-eugenie
../../.venv/bin/manim -ql --media_dir build/manim src/counterfactual_short_ko.py \
  Scene01_TabletQuestion Scene02_TwoWorlds Scene03_OneWorldObserved
../../.claude/skills/manim-video-pipeline/scripts/mux_audio.sh \
  build/manim/videos/counterfactual_short_ko/854p15/Scene01_TabletQuestion.mp4 \
  build/audio/01_tablet_question.mp3 preview/01_tablet_question_mux.mp4
# Scene02_TwoWorlds → 02_two_worlds, Scene03_OneWorldObserved → 03_one_world_observed 도 같은 방식
```

### 3. 최종 렌더 (720×1280, 30fps)

`-qm`(1280×720, 30fps)을 지정하면 파일 상단의 9:16 설정이 가로·세로를 바꿔 720×1280으로 렌더합니다.
이 설정은 이 모듈에만 적용되며 다른 영상에는 영향이 없습니다.

```bash
cd videos/counterfactual_short_aix-eugenie
../../.venv/bin/manim -qm --media_dir build/manim src/counterfactual_short_ko.py \
  Scene01_TabletQuestion Scene02_TwoWorlds Scene03_OneWorldObserved
```

### 4. 길이 검증 + Scene별 고화질 mux (`--shortest`)

mux 전에 각 Scene의 렌더 영상이 mp3보다 0.5초 이상 긴지 확인합니다. 짧으면 mux 옵션으로 덮지 말고 Scene 코드의 `WAIT_TAIL`이나 Beat 대기 시간을 고친 뒤 다시 렌더합니다.
고화질 mux는 Skill 규칙에 따라 `--shortest`를 씁니다.

```bash
D=build/manim/videos/counterfactual_short_ko/1280p30
MUX=../../.claude/skills/manim-video-pipeline/scripts/mux_audio.sh
for pair in Scene01_TabletQuestion:01_tablet_question Scene02_TwoWorlds:02_two_worlds Scene03_OneWorldObserved:03_one_world_observed; do
  cls=${pair%%:*}; base=${pair#*:}
  echo "$base video=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $D/$cls.mp4)" \
       "mp3=$(ffprobe -v error -show_entries format=duration -of csv=p=0 build/audio/$base.mp3)"
  $MUX $D/$cls.mp4 build/audio/$base.mp3 build/final/${base}_hq.mp4 --shortest
done
```

합본 전에 각 `_hq.mp4`의 `video 길이 - audio 길이`가 +0.1초 이하인지 확인합니다.

```bash
for f in build/final/0*_hq.mp4; do
  echo "$f video=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 $f)" \
       "audio=$(ffprobe -v error -select_streams a:0 -show_entries stream=duration -of csv=p=0 $f)"
done
```

### 5. 합본 (01 → 02 → 03)

`concat_videos.sh`는 입력 폴더의 모든 `*.mp4`를 파일명 순서로 잇습니다.
다시 만들 때 이전 최종 파일이 함께 이어 붙지 않도록 먼저 지웁니다.

```bash
rm -f build/final/counterfactual_short_ko.mp4
../../.claude/skills/manim-video-pipeline/scripts/concat_videos.sh build/final build/final/counterfactual_short_ko.mp4
ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate,duration -of compact \
  build/final/counterfactual_short_ko.mp4
```

직접 연결(`-c copy`)이 실패하면 이 도구는 1280×720 가로 화면으로 재인코딩합니다. 그 경우 세로 화면이 깨지므로, 결과가 720×1280인지 꼭 확인합니다.

## timings.json은 청크 단위 타이밍입니다

- 청크는 스크립트 txt에서 빈 줄로 나눈 문단 하나입니다. 문단마다 TTS를 따로 호출하고, 그 mp3들을 이어 붙여 Scene 음성을 만듭니다.
- `start`, `end`, `duration`은 각 청크 mp3의 길이를 `ffprobe`로 재서 누적한 값입니다. 단어나 문장 단위 타이밍이 아니고, 청크 안의 쉼도 포함합니다.
- Scene 코드는 이 값을 읽어 Beat 시작 시각으로 씁니다(`load_chunk_durations`). 청크 안의 세부 시점(예: "올랐습니다"에 맞춘 막대 상승)은 코드에서 청크 시작 기준 오프셋으로 맞췄습니다.
- 스크립트의 문단 수가 바뀌면 청크 수가 달라져 코드가 승인 당시 측정값(`FALLBACK_DURATIONS`)으로 돌아갑니다. 스크립트를 고치면 음성과 Scene 코드 타이밍을 함께 갱신하세요.

## 사용한 자산과 출처

| 자산 | 출처 / 라이선스 | 사용 방식 |
|---|---|---|
| 아이콘 `user`, `device-tablet`, `device-tablet-off`, `eye`, `eye-off` | [Tabler Icons](https://github.com/tabler/tabler-icons), MIT License | 로컬 클론 `videos/assets/tabler-icons/`의 outline SVG를 `SVGMobject`로 사용 |
| 한글 폰트 Apple SD Gothic Neo | macOS 시스템 폰트 | 화면 문구 렌더링에만 사용, 폰트 파일은 포함하지 않음 |
| 내용 원본 | `book/why_causal_inference/why_causal_inference_ko.ipynb` 셀 3, 5, 8, 9~10, 13 (노트북은 Facure, *Causal Inference for the Brave and True*를 참고) | 개념과 예시 흐름만 사용, 표의 점수는 쓰지 않음 |
| 연출 참고 | [3Blue1Brown videos](https://github.com/3b1b/videos) `_2020/covid.py`(IntroQuestion), `_2018/uncertainty.py` | 질문 인트로 리듬, 두 상태 대비 구성만 참고. 코드는 복사하지 않고 Manim CE로 새로 작성 |
| 애니메이션 엔진 | [Manim Community Edition](https://www.manim.community/) 0.22.0, MIT License | 렌더링 |

## AI 생성 음성 사용

- 이 영상의 내레이션은 실제 사람의 목소리가 아니라 OpenAI `gpt-4o-mini-tts`(voice `coral`)로 만든 AI 합성 음성입니다.
- 영상을 게시할 때는 설명란 등에 "내레이션은 AI 생성 음성입니다"처럼 AI 음성을 사용했다는 사실을 밝혀 주세요.
- 음성은 승인한 스크립트 원문을 그대로 읽게 했고, 속도 조절이나 톤 지시는 쓰지 않았습니다.
