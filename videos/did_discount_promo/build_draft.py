"""macOS에서 5컷 DID 영상 초안을 렌더한다."""

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


run(REPO / ".venv" / "bin" / "python", TOPIC / "src" / "slides.py")
timings = []
for number, script in enumerate(sorted((TOPIC / "src" / "scripts" / "ko").glob("*.txt")), 1):
    raw = AUDIO / f"{number:02d}.aiff"
    run("say", "-v", "Yuna", "-r", "180", "-f", script, "-o", raw)
    target = round(duration(raw) + 2.2, 2)
    timings.append(target)
    run("ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", "apad", "-t", target,
        "-ar", "48000", "-ac", "2", AUDIO / f"{number:02d}.wav")

(BUILD / "durations.json").write_text(json.dumps(timings, ensure_ascii=False))
concat = AUDIO / "concat.txt"
concat.write_text("\n".join(f"file '{AUDIO / f'{i:02d}.wav'}'" for i in range(1, 6)) + "\n")
run("ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", concat,
    "-c:a", "pcm_s16le", AUDIO / "narration.wav")

run(REPO / ".venv" / "bin" / "manim", "-ql", "-r", "1280,720", "--fps", "15", "--disable_caching",
    "--media_dir", BUILD / "manim", TOPIC / "src" / "did_discount_promo_ko.py", "DIDDiscountPromoDraft")
renders = list((BUILD / "manim").rglob("DIDDiscountPromoDraft.mp4"))
if not renders:
    raise RuntimeError("Manim 렌더 파일을 찾지 못했습니다")
render = max(renders, key=lambda p: p.stat().st_mtime)
output = PREVIEW / "did_discount_promo_draft.mp4"
run("ffmpeg", "-y", "-loglevel", "error", "-i", render, "-i", AUDIO / "narration.wav",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", output)
print(f"video: {output}")
print(f"durations: {timings}, total={sum(timings):.2f}s")
