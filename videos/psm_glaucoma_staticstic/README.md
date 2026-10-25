# 단순 비교의 함정 — 녹내장 복합제는 정말 효과가 없을까?

성향점수 매칭(PSM) 입문용 한국어 세로형(9:16) 영상입니다. 약 3분 30초, 6개 Scene으로 구성됩니다.

> ⚠️ 영상의 모든 수치와 그래프는 **가상 시뮬레이션 데이터**에서 계산한 값입니다. 실제 약물의 효과나 임상 결과를 나타내지 않습니다.
> 내레이션은 **AI 생성 음성**(OpenAI TTS)입니다.

| Scene | 클래스 | 핵심 메시지 | 길이 |
|---|---|---|---|
| 01 | `Scene01_Opening` | 단일제(PGA)와 복합제(PGA+timolol), 어느 쪽이 더 효과적일까? | 27.4초 |
| 02 | `Scene02_NaiveComparison` | 단순 비교하면 복합제의 목표 안압 도달률이 더 낮다 (73% vs 56%). 하지만 단정은 이르다 | 28.7초 |
| 03 | `Scene03_BaselineClue` | 복합제 환자는 기저 안압이 높아 출발선이 다르다. 21~28 mmHg에서 두 군이 겹친다 | 39.4초 |
| 04 | `Scene04_Confounding` | 기저 안압은 약 선택과 결과 양쪽에 영향을 주는 교란 변수다. RCT는 항상 할 수 없다 | 35.2초 |
| 05 | `Scene05_Matching` | 성향점수가 비슷한 환자끼리 1:1 매칭하면 출발선이 비슷해진다 (377쌍) | 47.5초 |
| 06 | `Scene06_Result` | 매칭 후에는 복합제가 더 높다 (57% vs 75%). 같은 데이터, 다른 비교 | 31.1초 |

## 파일 구성

```
videos/psm_glaucoma_staticstic/
├── README.md
├── notebooks/psm_simulation_ko.ipynb   # 가상 데이터 생성·PSM 계산 (영상 수치의 출처)
├── data/psm_numbers.json               # 노트북이 내보낸 수치. 영상 코드는 이 파일만 읽는다
├── src/
│   ├── psm_glaucoma.py                 # Manim CE 코드 (Scene별 클래스 6개)
│   └── scripts/ko/                     # 내레이션 원고 (실제로 읽는 문장만)
│       ├── 01_opening.txt
│       ├── 02_naive_comparison.txt
│       ├── 03_baseline_clue.txt
│       ├── 04_confounding.txt
│       ├── 05_matching.txt
│       └── 06_result.txt
├── build/                              # 생성물 (git 제외)
│   ├── audio/NN_name.mp3, NN_name.timings.json
│   ├── manim/                          # Manim 중간 파일, 확인용 프레임
│   └── final/NN_name_hq.mp4, psm_glaucoma.mp4
└── preview/NN_name_mux.mp4             # 저해상도 확인 영상 (git 제외)
```

## 필요한 환경

- 프로젝트 루트의 `.venv` (Manim CE, numpy, pandas, scikit-learn, matplotlib, nbconvert)
- Node.js (음성 생성 스크립트), ffmpeg / ffprobe
- 한글 폰트 **Noto Sans KR**
- 공용 아이콘 `videos/assets/tabler-icons/` (`video-assets-setup` 스킬로 설치)

### 환경변수

| 이름 | 필수 | 설명 |
|---|---|---|
| `OPENAI_API_KEY` | 예 | OpenAI TTS 키. 환경변수 또는 프로젝트 루트 `.env`(UTF-8)에 둔다. 키 값은 출력하거나 소스에 저장하지 않는다 |
| `OPENAI_TTS_VOICE` | 아니오 | voice 변경 (기본 `coral`) |
| `OPENAI_TTS_INSTRUCTIONS` | 아니오 | 말투 지시 (이 영상은 쓰지 않음) |

Windows PowerShell 5.1에서 `echo KEY=값 > .env`로 만든 파일은 UTF-16이라 Node가 읽지 못합니다. UTF-8로 저장하세요.

## 재현 명령

아래 명령은 별도 표시가 없으면 이 작업 폴더(`videos/psm_glaucoma_staticstic/`)에서 Git Bash로 실행합니다.

### 1. 시뮬레이션 데이터

```bash
cd notebooks
../../../.venv/Scripts/jupyter.exe nbconvert --to notebook --execute --inplace psm_simulation_ko.ipynb
cd ..
```

`data/psm_numbers.json`이 다시 만들어집니다 (seed=0, N=2000). 설정을 바꾸면 내레이션 원고의 숫자도 함께 고쳐야 합니다.

### 2. 음성 생성 (프로젝트 루트에서)

```bash
cd ../..
for s in 01:opening 02:naive_comparison 03:baseline_clue 04:confounding 05:matching 06:result; do
  n=${s%%:*}; name=${s#*:}
  node .claude/skills/manim-video-pipeline/scripts/generate_elevenlabs_audio.mjs \
    --topic psm_glaucoma_staticstic --scene $n --name $name \
    --script videos/psm_glaucoma_staticstic/src/scripts/ko/${n}_${name}.txt --dry-run   # 경로 확인 후 --dry-run 을 빼고 실제 생성
done
```

- 모델 `gpt-4o-mini-tts`, voice `coral`, mp3 (프로젝트 기본값). 스크립트 파일 이름은 레거시이며 내부는 OpenAI API입니다.
- 결과: `build/audio/NN_name.mp3`, `build/audio/NN_name.timings.json`
- **`timings.json`은 청크(원고의 빈 줄로 나눈 문단) 단위 타이밍입니다.** 단어·문장 단위가 아니므로, 청크 안의 문장 시작 시점은 Manim 코드에서 글자 수 비율로 추정했습니다 (각 Scene docstring의 Script-to-Beat Mapping 참고).
- TTS가 아라비아 숫자를 잘못 읽는 경우가 있어("18까지" → "열팔") 원고의 숫자는 한글로 적었습니다.
- Windows 주의: main 브랜치의 음성 스크립트는 저장소 루트 경로 계산 버그(`new URL(...).pathname`)로 Windows에서 실패합니다. 이 영상은 수정본(`fileURLToPath`, 반사실 쇼츠 PR #16 커밋 `361bc45`)을 임시로 꺼내 실행했습니다.

### 3. 렌더

```bash
# 확인용 (540x960, 15fps)
../../.venv/Scripts/manim.exe -ql --media_dir build/manim src/psm_glaucoma.py Scene01_Opening

# 최종 (720x1280, 30fps, 6개 Scene 동일 설정)
../../.venv/Scripts/manim.exe -r 720,1280 --fps 30 --media_dir build/manim src/psm_glaucoma.py \
  Scene01_Opening Scene02_NaiveComparison Scene03_BaselineClue Scene04_Confounding Scene05_Matching Scene06_Result
```

각 Scene은 `build/audio/NN_name.timings.json`의 청크 시간을 읽어 화면을 전환하고, 음성보다 0.7~1.0초 길게 끝나도록(`WAIT_TAIL`) 되어 있어 개별 실행이 가능합니다.

### 4. Scene별 음성 합성 (고화질)

```bash
M=../../.claude/skills/manim-video-pipeline/scripts
mkdir -p build/manim/padded_audio build/final
for s in 01_opening:Scene01_Opening 02_naive_comparison:Scene02_NaiveComparison 03_baseline_clue:Scene03_BaselineClue \
         04_confounding:Scene04_Confounding 05_matching:Scene05_Matching 06_result:Scene06_Result; do
  n=${s%%:*}; cls=${s#*:}
  V=build/manim/videos/psm_glaucoma/1280p30/$cls.mp4
  vd=$(ffprobe -v error -select_streams v:0 -show_entries stream=duration -of csv=p=0 $V)
  # 음성 뒤에 무음을 붙여 영상 길이와 맞춘 뒤 --shortest 로 합성 (WAIT_TAIL 구간을 자르지 않기 위해)
  ffmpeg -v error -y -i build/audio/$n.mp3 -af "apad=whole_dur=$vd" -ar 48000 build/manim/padded_audio/$n.wav
  bash $M/mux_audio.sh $V build/manim/padded_audio/$n.wav build/final/${n}_hq.mp4 --shortest
done
```

합본 전에 각 `_hq.mp4`의 영상·음성 트랙 길이 차이가 +0.1초를 넘지 않는지 `ffprobe`로 확인합니다.

### 5. 합본 (BGM 없음)

```bash
rm -f build/final/psm_glaucoma.mp4   # 합본 도구는 폴더의 mp4를 모두 모으므로 이전 결과를 먼저 지운다
bash ../../.claude/skills/manim-video-pipeline/scripts/concat_videos.sh build/final build/final/psm_glaucoma.mp4
```

Windows(Git Bash) 주의: 합본 도구가 목록에 `realpath` 결과(`/c/Users/...`)를 쓰는데 Windows용 ffmpeg는 이 경로를 열지 못합니다. 이 영상은 `realpath` 결과를 `cygpath -m`으로 바꿔 주는 임시 셈(shim)을 PATH 앞에 두고 실행했습니다.

## 사용한 자산과 출처

| 자산 | 출처 / 라이선스 |
|---|---|
| 아이콘 (eye, gauge, vaccine-bottle, droplet, clipboard-text, users, target, clock, cash) | [Tabler Icons](https://github.com/tabler/tabler-icons), MIT License |
| 폰트 | Noto Sans KR (Google), SIL Open Font License |
| 애니메이션 | [Manim Community Edition](https://www.manim.community/) |
| 내레이션 음성 | OpenAI TTS `gpt-4o-mini-tts`, voice `coral` — **AI 생성 음성** |
| 데이터 | `notebooks/psm_simulation_ko.ipynb`로 만든 가상 시뮬레이션 데이터 |
| 구성 참고 | `book/psm_glaucoma/psm_glaucoma_ko.ipynb`, `videos/psm_glaucoma/src/psm_glaucoma.py` |

배경음악은 사용하지 않았습니다.
