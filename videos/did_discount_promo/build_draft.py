"""문장별 ElevenLabs 타이밍에 맞춰 DID 영상 초안을 렌더한다."""

import argparse
import json
import subprocess
from pathlib import Path


TOPIC = Path(__file__).resolve().parent
REPO = TOPIC.parents[1]
BUILD = TOPIC / "build"
AUDIO = BUILD / "audio"
PREVIEW = TOPIC / "preview"
AUDIO.mkdir(parents=True, exist_ok=True)
PREVIEW.mkdir(parents=True, exist_ok=True)


def run(*args):
    subprocess.run([str(arg) for arg in args], check=True, cwd=TOPIC)


def duration(path):
    result = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True,
    )
    return float(result.strip())


def prepare_audio():
    run("node", TOPIC / "src" / "generate_elevenlabs_audio.mjs")
    beats = json.loads((AUDIO / "beat_manifest.json").read_text())
    gap = 0.12
    cursor = 0.0
    wavs = []
    for beat in beats:
        source = AUDIO / beat["file"]
        speech_duration = duration(source)
        target_duration = round(speech_duration + gap, 3)
        wav = AUDIO / f"{source.stem}.wav"
        run("ffmpeg", "-y", "-loglevel", "error", "-i", source, "-af", "apad",
            "-t", target_duration, "-ar", "48000", "-ac", "2", wav)
        beat.update(start=round(cursor, 3), speech_end=round(cursor + speech_duration, 3),
                    end=round(cursor + target_duration, 3), duration=target_duration)
        cursor += target_duration
        wavs.append(wav)
    if cursor > 140:
        raise RuntimeError(f"내레이션 {cursor:.1f}초: 2분 20초를 넘습니다. 대본을 줄여 주세요.")
    (BUILD / "timings.json").write_text(json.dumps({"total": round(cursor, 3), "beats": beats}, ensure_ascii=False, indent=2))
    concat = AUDIO / "concat.txt"
    concat.write_text("\n".join(f"file '{wav}'" for wav in wavs) + "\n")
    run("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", concat,
        "-c:a", "pcm_s16le", AUDIO / "narration.wav")
    print(f"narration: {cursor:.2f}s, {len(beats)} beats, no tempo change")


def render():
    if not (BUILD / "timings.json").exists():
        raise FileNotFoundError("먼저 --audio-only로 타이밍을 생성해 주세요.")
    run(REPO / ".venv" / "bin" / "manim", "-ql", "-r", "1280,720", "--fps", "15",
        "--disable_caching", "--media_dir", BUILD / "manim",
        TOPIC / "src" / "did_discount_promo_ko.py", "DIDDiscountPromoDraft")
    renders = list((BUILD / "manim").rglob("DIDDiscountPromoDraft.mp4"))
    if not renders:
        raise RuntimeError("Manim 렌더 파일을 찾지 못했습니다")
    rendered = max(renders, key=lambda p: p.stat().st_mtime)
    output = PREVIEW / "did_discount_promo_draft.mp4"
    run("ffmpeg", "-y", "-loglevel", "error", "-i", rendered, "-i", AUDIO / "narration.wav",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", output)
    print(f"video: {output} ({duration(output):.2f}s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--audio-only", action="store_true")
    parser.add_argument("--render-only", action="store_true")
    args = parser.parse_args()
    if args.audio_only and args.render_only:
        parser.error("한 번에 한 단계만 선택할 수 있습니다")
    if not args.render_only:
        prepare_audio()
    if not args.audio_only:
        render()
