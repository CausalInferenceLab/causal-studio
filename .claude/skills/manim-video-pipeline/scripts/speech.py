"""Synthesize narration in chunks and measure a shared timeline for either provider."""

import json
import math
import os
from contextlib import contextmanager
from pathlib import Path
import re
import shutil
import subprocess
from tempfile import TemporaryDirectory
from textwrap import wrap
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
import wave


SAMPLE_RATE = 44_100
MODELS = {"openai": "gpt-4o-mini-tts", "elevenlabs": "eleven_multilingual_v2"}


def add_audio_arguments(parser, repo_root):
    payload = parser.add_mutually_exclusive_group()
    payload.add_argument("--script", type=Path, help="Narration text file, with one blank line between beats")
    payload.add_argument("--text", help="Narration text supplied directly")
    parser.add_argument("--output", type=Path, help="Output .mp3 path (.timings.json is written beside it)")
    parser.add_argument("--provider", choices=MODELS, default="openai")
    parser.add_argument("--voice", help="OpenAI voice name or ElevenLabs voice ID")
    parser.add_argument("--model")
    parser.add_argument("--speed", type=float, default=1.0)
    parser.add_argument("--gap", type=float, default=0.0, help="Silence between chunks in seconds")
    parser.add_argument("--env-file", type=Path, default=repo_root / ".env")
    parser.add_argument("--dry-run", action="store_true", help="Show resolved inputs without synthesizing")
    for key in ("topic", "scene", "name", "lang"):
        parser.add_argument(f"--{key}", help="Causal Studio legacy path option")
    parser.set_defaults(repo_root=repo_root)


def parse_narration(text):
    text = "\n".join(line for line in text.splitlines() if not line.lstrip().startswith("#"))
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = " ".join(paragraph.split())
        if not paragraph:
            continue
        yield from wrap(paragraph, 650)


def settings_from(path):
    values = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip().removeprefix("export ")
            key, separator, value = line.partition("=")
            if separator and re.fullmatch(r"[A-Za-z_][A-Za-z_0-9]*", key.strip()):
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                else:
                    value = value.split(" #", 1)[0].rstrip()
                values[key.strip()] = value
    return {**values, **os.environ}


def speech_request(provider, text, voice, model, speed, settings):
    if provider == "openai":
        endpoint = "https://api.openai.com/v1/audio/speech"
        headers = {"Authorization": f"Bearer {settings['OPENAI_API_KEY']}"}
        body = {"model": model, "voice": voice, "input": text, "response_format": "mp3", "speed": speed}
        if settings.get("OPENAI_TTS_INSTRUCTIONS"):
            body["instructions"] = settings["OPENAI_TTS_INSTRUCTIONS"]
    else:
        endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{quote(voice, safe='')}?output_format=mp3_44100_128"
        headers = {"xi-api-key": settings["ELEVENLABS_API_KEY"]}
        body = {"model_id": model, "text": text, "voice_settings": {"speed": speed}}
    headers["Content-Type"] = "application/json"
    headers["Accept"] = "audio/mpeg"
    return Request(endpoint, data=json.dumps(body).encode(), headers=headers, method="POST")


def synthesize(request, provider, beat):
    try:
        with urlopen(request, timeout=90) as response:
            return response.read()
    except HTTPError as error:
        raise RuntimeError(f"{provider} returned HTTP {error.code} for narration beat {beat}. Check the key, voice, model, and available credits.") from error
    except URLError as error:
        raise RuntimeError(f"Could not connect to {provider} for narration beat {beat}: {error.reason}") from error


def media_duration(path):
    if not shutil.which("ffprobe"):
        raise RuntimeError("Install FFmpeg (including ffprobe) for audio and mux commands.")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        check=True, text=True, stdout=subprocess.PIPE,
    )
    duration = float(result.stdout.strip())
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError(f"Unable to determine media duration for {path}.")
    return duration


def audio_paths(args):
    if args.output:
        if args.script is None and args.text is None:
            raise ValueError("Use --script or --text with --output.")
        script = args.script
        output = args.output
    else:
        legacy = (args.topic, args.scene, args.name)
        if not all(value and re.fullmatch(r"[A-Za-z0-9_-]+", value) for value in legacy):
            raise ValueError("Use --script FILE --output FILE.mp3 (or the legacy --topic, --scene, and --name flags).")
        topic = args.repo_root / "videos" / args.topic
        basename = f"{args.scene}_{args.name}"
        candidates = [topic / "narration" / f"{basename}.txt", topic / "src" / "scripts" / f"{basename}.txt"]
        if args.lang:
            if not re.fullmatch(r"[A-Za-z0-9_-]+", args.lang):
                raise ValueError("--lang must be a language tag such as en, ko, or en-US.")
            candidates = [candidate.parent / args.lang / candidate.name for candidate in candidates] + candidates
        script = args.script or next((candidate for candidate in candidates if candidate.is_file()), candidates[0])
        output = topic / "build" / "audio" / f"{basename}.mp3"
    if output.suffix.lower() != ".mp3":
        raise ValueError("--output must end in .mp3.")
    return script, output.resolve()


def assemble_audio(provider, paragraphs, voice, model, speed, gap, settings, temp, output):
    timings = []
    cursor = 0
    silent_frames = round(gap * SAMPLE_RATE)
    merged = temp / "narration.wav"
    with wave.open(str(merged), "wb") as narration:
        narration.setparams((1, 2, SAMPLE_RATE, 0, "NONE", "not compressed"))
        for index, text in enumerate(paragraphs, 1):
            request = speech_request(provider, text, voice, model, speed, settings)
            raw = temp / "chunk.mp3"
            pcm = temp / "chunk.wav"
            raw.write_bytes(synthesize(request, provider, index))
            subprocess.run(
                ["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-ac", "1",
                 "-ar", str(SAMPLE_RATE), "-c:a", "pcm_s16le", str(pcm)],
                check=True,
            )
            with wave.open(str(pcm), "rb") as chunk:
                frames = chunk.getnframes()
                if frames <= 0:
                    raise ValueError(f"No audio for beat {index}.")
                narration.writeframes(chunk.readframes(frames))
            start = cursor / SAMPLE_RATE
            cursor += frames
            timings.append(dict(index=index, text=text, start=start, end=cursor / SAMPLE_RATE,
                                duration=frames / SAMPLE_RATE))
            if index < len(paragraphs) and silent_frames:
                narration.writeframes(bytes(silent_frames * 2))
                cursor += silent_frames
    subprocess.run(
        ["ffmpeg", "-y", "-v", "error", "-i", str(merged), "-c:a", "libmp3lame", "-b:a", "128k", str(output)],
        check=True,
    )
    return timings


@contextmanager
def exclusive_output(output):
    marker = output.with_name(f".{output.name}.lock")
    try:
        marker.touch(exist_ok=False)
    except FileExistsError as error:
        raise ValueError(f"Narration output is locked at {marker}. Remove the lock only if no generation is running.") from error
    try:
        yield
    finally:
        marker.unlink(missing_ok=True)


def generate_audio(args):
    script, output = audio_paths(args)
    text = args.text if args.text is not None else script.read_text(encoding="utf-8")
    paragraphs = list(parse_narration(text))
    if not paragraphs:
        raise ValueError("The narration contains no speakable paragraphs.")
    speed_min, speed_max = (0.25, 4.0) if args.provider == "openai" else (0.7, 1.2)
    if not speed_min <= args.speed <= speed_max or not 0 <= args.gap <= 10:
        raise ValueError(f"Use --speed between {speed_min} and {speed_max} and --gap between 0 and 10.")
    settings = settings_from(args.env_file)
    is_openai = args.provider == "openai"
    voice = args.voice or settings.get("OPENAI_TTS_VOICE" if is_openai else "ELEVENLABS_VOICE_ID")
    if not voice and is_openai:
        voice = "coral"
    model = args.model or MODELS[args.provider]
    target = output.with_suffix(".timings.json")
    if args.dry_run:
        print(json.dumps(dict(provider=args.provider, voice=voice, modelId=model, outputPath=str(output),
                              timingsPath=str(target), chunkCount=len(paragraphs), chunks=paragraphs), ensure_ascii=False, indent=2))
        return
    key = "OPENAI_API_KEY" if is_openai else "ELEVENLABS_API_KEY"
    if not settings.get(key):
        raise ValueError(f"Set {key} in your environment or in {args.env_file}.")
    if not voice:
        raise ValueError("Set ELEVENLABS_VOICE_ID or supply --voice.")
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("Install FFmpeg (including ffprobe) before generating narration.")
    output.parent.mkdir(parents=True, exist_ok=True)
    with exclusive_output(output), TemporaryDirectory(prefix=".narration-", dir=output.parent) as directory:
        temp = Path(directory)
        audio = temp / "narration.mp3"
        chunks = assemble_audio(args.provider, paragraphs, voice, model, args.speed, args.gap, settings, temp, audio)
        metadata = dict(provider=args.provider, voice=voice, modelId=model, outputFormat="mp3",
                        scriptPath=str(script) if script else None, outputPath=str(output),
                        topic=args.topic, scene=args.scene, sceneName=args.name, speed=args.speed, gap=args.gap,
                        totalDuration=media_duration(audio), chunkCount=len(chunks), chunks=chunks)
        timings = temp / "narration.timings.json"
        timings.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        audio.replace(output)
        timings.replace(target)
    print(f"{output}\n{target}")
