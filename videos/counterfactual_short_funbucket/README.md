# 같은 학생의 두 세계 — 태블릿의 효과는 어떻게 알까?

인과추론 입문자를 위한 한국어 세로형 쇼츠 실습이다. 수식과 점수 없이 학생 한 명의 두 가능성을 비교한다. 검정 배경에서 학생은 흰색, 태블릿 지급은 청록색, 질문과 반사실은 노란색으로 표시한다.

| Scene | 핵심 메시지 | 클래스 | 스크립트 |
|---|---|---|---|
| 01 | 성적 상승만으로 태블릿 효과를 단정할 수 없다. | `Scene01_TabletQuestion` | `01_tablet_question.txt` |
| 02 | 같은 학생이 같은 시험에서 태블릿을 받거나 받지 않은 두 경우를 비교한다. | `Scene02_SameStudentWorlds` | `02_same_student_worlds.txt` |
| 03 | 실제로 받았다면, 받지 않았을 때의 관찰할 수 없는 결과가 반사실이다. | `Scene03_OnlyOneOutcome` | `03_only_one_outcome.txt` |

## 커밋하는 소스

```text
README.md
src/counterfactual_short_ko.py
src/scripts/ko/01_tablet_question.txt
src/scripts/ko/02_same_student_worlds.txt
src/scripts/ko/03_only_one_outcome.txt
```

`.env`, `build/`, `preview/`, 생성된 MP3·MP4·timings JSON 및 공용 로컬 자산은 커밋하지 않는다. 각 Scene은 독립 실행할 수 있지만 해당 음성과 타이밍 파일을 먼저 생성해야 한다.

## 실행 환경

- 저장소 루트에서 `bash scripts/setup_environment.sh`로 전체 환경을 준비하고 `bash scripts/setup_environment.sh --check`로 검증한다.
- Python 3.11과 프로젝트 `.venv`를 사용한다. 최초 검증 환경은 Python 3.11.14, Manim CE 0.22.0, FFmpeg 8.0.1이다.
- `node`, `npm`, `ffmpeg`, `ffprobe`가 PATH에 있어야 한다. Node.js는 프로젝트 생성기가 사용하는 `process.loadEnvFile`을 지원해야 한다.
- 코드의 `FONT`는 macOS의 설치된 `Apple SD Gothic Neo`이다. 다른 운영체제에서는 설치된 한글 폰트로 `FONT`를 변경하고 레이아웃을 재검수한다.
- 공용 Tabler Icons는 `videos/assets/tabler-icons/`에 있어야 한다. 설정 스크립트가 설치하며 아이콘을 이 폴더에 복사하지 않는다.
- OpenAI TTS 생성기는 루트 `.env`를 읽는다. 이 파일을 로컬에 준비하고 `OPENAI_API_KEY`를 설정한다. 키가 환경변수에만 있다면 현재 생성기는 `.env` 파일도 요구하므로 빈 `.env` 파일을 준비한다. 키 값은 로그·소스·커밋 메시지에 넣지 않는다.
- 기본 음성은 `gpt-4o-mini-tts` / `coral`, 속도는 `1.0`이다. 기본값 재현 시 `OPENAI_TTS_VOICE`, `OPENAI_TTS_INSTRUCTIONS`의 별도 설정을 사용하지 않는다.

## 1. 음성과 타이밍 생성

아래 명령은 저장소 루트에서 시작한다. 각 스크립트 파일에는 실제 낭독할 문장만 들어 있다. 문단 구분이 TTS 청크 구분이 된다.

```bash
cd .claude/skills/manim-video-pipeline

generate_scene_audio() {
  local scene_no="$1"
  local scene_name="$2"
  local script_path="../../../videos/counterfactual_short_funbucket/src/scripts/ko/${scene_no}_${scene_name}.txt"

  npm run openai-audio -- \
    --topic counterfactual_short_funbucket \
    --scene "$scene_no" --name "$scene_name" \
    --script "$script_path" --dry-run || return

  npm run openai-audio -- \
    --topic counterfactual_short_funbucket \
    --scene "$scene_no" --name "$scene_name" \
    --script "$script_path"
}

generate_scene_audio 01 tablet_question
generate_scene_audio 02 same_student_worlds
generate_scene_audio 03 only_one_outcome
```

각 명령은 먼저 dry-run으로 경로와 입력을 확인한 뒤 API를 호출한다. 출력은 작업 폴더의 `build/audio/NN_scene_name.mp3`와 `build/audio/NN_scene_name.timings.json`이다.

TTS 결과는 생성마다 달라질 수 있다. 최초 음성 길이는 Scene 01부터 각각 10.320초, 12.048초, 15.240초였으며 합본은 약 37.58초였다. 바이트 단위로 동일한 음성이나 고정 길이를 보장하지 않는다. 재생성 후 음성을 듣고 청크 시간과 화면 전환을 확인한다. 코드 주석의 초 단위 값은 최초 생성본의 기록이며, 실행 시에는 새로 생성한 JSON을 읽는다.

## 2. 개별 Scene 렌더

이후 모든 명령은 작업 폴더에서 실행한다.

```bash
# 위의 TTS 명령을 실행한 디렉터리에서 이동한다.
cd ../../../videos/counterfactual_short_funbucket

# 저해상도 확인본: 360×640, 15fps
../../.venv/bin/python -m manim -ql --disable_caching \
  --media_dir build/manim src/counterfactual_short_ko.py \
  Scene01_TabletQuestion Scene02_SameStudentWorlds Scene03_OnlyOneOutcome

# 최종 렌더: 1080×1920, 30fps
../../.venv/bin/python -m manim -qh --disable_caching \
  --media_dir build/manim src/counterfactual_short_ko.py \
  Scene01_TabletQuestion Scene02_SameStudentWorlds Scene03_OnlyOneOutcome
```

클래스 하나만 지정하면 해당 Scene만 렌더한다. 9:16 설정은 이 파일의 Scene 생성·렌더 중에만 임시 적용하며 공용 `manim.cfg`를 변경하지 않는다. 모든 렌더 중간 파일은 `build/manim/`에 모인다.

대표 프레임에서 겹침, 잘림, 간격, 시선 경쟁, 정보 과밀을 확인한다. Scene 01은 첫 화면 전체가 사라진 다음 질문 하나가 중앙으로 올라온다. Scene 02·03은 학생 아이콘 하나에서 두 경우로 갈라지는 같은 배치를 사용한다.

## 3. 길이 검사와 음성 합성

다음 명령은 각 렌더가 음성보다 짧지 않은지 확인하고 프로젝트 mux 도구를 사용한다. 영상이 짧으면 Scene 코드의 대기 시간을 수정하고 다시 렌더한다. 합본용 파일은 `--shortest`로 만들고 두 트랙의 길이 차이도 검사한다.

```bash
../../.venv/bin/python - <<'PY'
import json
import subprocess
from pathlib import Path

scenes = [
    ("01_tablet_question", "Scene01_TabletQuestion"),
    ("02_same_student_worlds", "Scene02_SameStudentWorlds"),
    ("03_only_one_outcome", "Scene03_OnlyOneOutcome"),
]

def probe(path):
    return json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration:stream=codec_type,duration", "-of", "json", str(path),
    ], text=True))

for name, scene_class in scenes:
    timing = json.loads(Path(f"build/audio/{name}.timings.json").read_text())
    for resolution, output, mode in [
        ("640p15", f"preview/{name}_mux.mp4", "--full"),
        ("1920p30", f"build/final/scenes/{name}_hq.mp4", "--shortest"),
    ]:
        video = f"build/manim/videos/counterfactual_short_ko/{resolution}/{scene_class}.mp4"
        assert float(probe(video)["format"]["duration"]) >= timing["totalDuration"], video
        subprocess.run([
            "bash", "../../.claude/skills/manim-video-pipeline/scripts/mux_audio.sh",
            video, f"build/audio/{name}.mp3", output, mode,
        ], check=True)
        tracks = {track["codec_type"]: track for track in probe(output)["streams"]}
        assert "video" in tracks and "audio" in tracks, output
        if mode == "--shortest":
            difference = float(tracks["video"]["duration"]) - float(tracks["audio"]["duration"])
            assert abs(difference) < 0.1, (output, difference)
PY
```

## 4. 전체 합본

```bash
bash ../../.claude/skills/manim-video-pipeline/scripts/concat_videos.sh \
  build/final/scenes build/final/counterfactual_short_ko_full.mp4

ffprobe -v error -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  build/final/counterfactual_short_ko_full.mp4

ffmpeg -hide_banner -loglevel error \
  -i build/final/counterfactual_short_ko_full.mp4 -f null -
```

`build/final/scenes/`에는 이번 세 Scene의 HQ 합성본만 둔다. 합본 후 전체 길이가 35~45초인지 확인하고 장면 경계와 마지막 음성까지 재생해 검수한다. 확인용 개별 영상은 `preview/`, 전체 고해상도 영상은 `build/final/counterfactual_short_ko_full.mp4`에 생성된다.

## 참고 자료

- `book/why_causal_inference/why_causal_inference_ko.ipynb`: 전체 셀을 1부터 계산해 셀 4·6·9를 사용했다.
- `videos/why_causal_inference/src/why_causal_inference.py`: 공용 SVG와 반사실 대비 화면의 구조를 참고했다.
- `3b1b/_2020/covid.py`의 `IntroQuestion`: 질문을 순차 제시하고 앞 요소를 지우는 전환 리듬을 참고했다.
