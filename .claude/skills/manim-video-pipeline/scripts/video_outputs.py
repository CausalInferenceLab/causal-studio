"""Inspect rendered media, review transitions, and assemble publishable files."""

import json
import math
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
from unicodedata import category, east_asian_width


PUBLISH_FPS = 30
CAPTION_COLUMNS = 38
CAPTION_ROWS = 2


def probe(path):
    if not path.is_file():
        raise ValueError(f"Media file not found: {path}")
    if not shutil.which("ffprobe"):
        raise RuntimeError("Install FFmpeg (including ffprobe) to inspect video outputs.")
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
        capture_output=True, text=True, check=False,
    )
    if result.returncode:
        raise ValueError(f"Cannot inspect {path}: {result.stderr.strip()}")
    return json.loads(result.stdout)


def video_info(path):
    if not shutil.which("ffprobe"):
        # Manim already brings PyAV, so preview-only installations can still
        # report and validate their renders.
        import av

        with av.open(str(path)) as container:
            stream = next(iter(container.streams.video), None)
            if stream is None:
                raise ValueError(f"No video stream in {path}")
            duration = (float(stream.duration * stream.time_base) if stream.duration and stream.time_base
                        else (container.duration or 0) / av.time_base)
            fps = float(stream.average_rate or 0)
            if duration <= 0 or fps <= 0:
                raise ValueError(f"Invalid video duration or frame rate in {path}")
            return duration, fps, stream.width, stream.height, bool(container.streams.audio)
    info = probe(path)
    stream = next((stream for stream in info["streams"] if stream["codec_type"] == "video"), None)
    if stream is None:
        raise ValueError(f"No video stream in {path}")
    duration = float(stream.get("duration") or info["format"]["duration"])
    numerator, denominator = map(int, stream["avg_frame_rate"].split("/"))
    if not (math.isfinite(duration) and duration > 0 and numerator > 0 and denominator > 0):
        raise ValueError(f"Invalid video duration or frame rate in {path}")
    has_audio = any(track["codec_type"] == "audio" for track in info["streams"])
    return duration, numerator / denominator, stream["width"], stream["height"], has_audio


def run_ffmpeg(*args):
    if not shutil.which("ffmpeg"):
        raise RuntimeError("Install FFmpeg to review or package video outputs.")
    result = subprocess.run(["ffmpeg", "-nostdin", "-y", "-v", "error", *map(str, args)],
                            capture_output=True, text=True, check=False)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or f"FFmpeg exited with status {result.returncode}")


def extract_frame(video, seconds, target, *, width=None):
    scale = ["-vf", f"scale={width}:-2"] if width is not None else []
    run_ffmpeg("-ss", f"{seconds:.6f}", "-i", video, "-map", "0:v:0", *scale,
               "-frames:v", 1, "-update", 1, target)
    if not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError(f"No frame at {seconds:.3f}s in {video}")


def review(video, transitions, output):
    from PIL import Image, ImageDraw

    video = video.resolve()
    output = (output or video.with_name(f"{video.stem}.review")).resolve()
    duration, fps, *_ = video_info(video)
    last_frame = max(0, duration - 1 / fps)
    samples = []
    for number, (start, end) in enumerate(transitions, 1):
        if not 0 <= start < end <= duration:
            raise ValueError(f"Transition {number} must satisfy 0 <= start < end <= {duration:.3f}s")
        margin = max(0.15, 1 / fps)
        samples.append(tuple(zip(("before", "during", "after"),
                                 (max(0, start - margin), (start + end) / 2, min(last_frame, end + margin)))))
    output.mkdir(parents=True, exist_ok=True)
    sheet = output / "contact-sheet.png"
    rows = []
    with TemporaryDirectory(dir=output) as stage:
        stage = Path(stage)
        frames = []
        for number, sample in enumerate(samples, 1):
            row = []
            for position, (label, seconds) in enumerate(sample):
                seconds = min(last_frame, seconds)
                path = stage / f"{number:02d}-{label}.png"
                extract_frame(video, seconds, path, width=448)
                with Image.open(path) as frame:
                    frames.append((frame.copy(), number, position, label, seconds, path))
                row.append({"position": label, "seconds": round(seconds, 6), "path": str(output / path.name)})
            rows.append(row)
        cell_width, cell_height = 464, max(frame.height for frame, *_ in frames) + 38
        image = Image.new("RGB", (3 * cell_width, len(rows) * cell_height), "#202731")
        draw = ImageDraw.Draw(image)
        for frame, number, position, label, seconds, path in frames:
            x, y = position * cell_width + 8, (number - 1) * cell_height + 8
            image.paste(frame, (x, y))
            draw.text((x, y + frame.height + 8), f"{number:02d}  {label}  {seconds:.3f}s", fill="white")
            path.replace(output / path.name)
        image.save(stage / sheet.name)
        (stage / sheet.name).replace(sheet)
    return {"video": str(video), "sheet": str(sheet), "transitions": rows}


def caption_cell_width(character):
    if category(character) in {"Mn", "Me", "Cf"}:
        return 0
    return 2 if east_asian_width(character) in {"F", "W"} else 1


def caption_lines(text):
    """Wrap at spaces, breaking a word only when it is wider than a whole line."""
    line = ""
    columns = 0
    for word in text.split():
        widths = [caption_cell_width(character) for character in word]
        word_width = sum(widths)
        if line and columns + 1 + word_width > CAPTION_COLUMNS:
            yield line
            line, columns = "", 0
        if word_width > CAPTION_COLUMNS:
            start = columns = 0
            for index, width in enumerate(widths):
                if columns + width > CAPTION_COLUMNS:
                    yield word[start:index]
                    start, columns = index, 0
                columns += width
            line = word[start:]
        elif line:
            line += " " + word
            columns += 1 + word_width
        else:
            line, columns = word, word_width
    if line:
        yield line


def split_caption(text, start, end):
    """Estimate cue boundaries within a measured narration beat."""
    lines = list(caption_lines(text))
    blocks = ["\n".join(lines[i:i + CAPTION_ROWS]) for i in range(0, len(lines), CAPTION_ROWS)]
    weights = [sum(not character.isspace() for character in block) for block in blocks]

    # Work at SRT precision so adjacent cues share a boundary and each has visible duration.
    start_ms, end_ms = round(start * 1000), round(end * 1000)
    duration = end_ms - start_ms
    if duration < len(blocks):
        raise ValueError(f"Narration at {start:g}–{end:g}s is too short to split into SRT cues.")
    total_weight = sum(weights)
    cursor, consumed = start_ms, 0
    for index, (block, weight) in enumerate(zip(blocks, weights, strict=True), 1):
        consumed += weight
        ideal_end = start_ms + round(duration * consumed / total_weight)
        boundary = min(max(cursor + 1, ideal_end), end_ms - (len(blocks) - index))
        yield cursor / 1000, boundary / 1000, block
        cursor = boundary


def narration_cues(audio, offset, scene_length):
    info = probe(audio)
    if not any(stream["codec_type"] == "audio" for stream in info["streams"]):
        raise ValueError(f"No audio stream in {audio}")
    audio_length = float(info["format"]["duration"])
    if not math.isfinite(audio_length) or audio_length <= 0 or audio_length > scene_length + 0.02:
        raise ValueError(f"Narration ({audio_length:.3f}s) does not fit the scene ({scene_length:.3f}s): {audio}")
    timing_path = audio.with_suffix(".timings.json")
    if not timing_path.is_file():
        raise ValueError(f"Missing narration timings: {timing_path}")
    metadata = json.loads(timing_path.read_text(encoding="utf-8"))
    if not metadata["chunks"] or not math.isclose(float(metadata["totalDuration"]), audio_length, abs_tol=0.08):
        raise ValueError(f"Narration timings do not match the audio length: {timing_path}")
    cues = []
    previous_end = 0.0
    cue_limit = min(audio_length, scene_length)
    for chunk in metadata["chunks"]:
        start, end = float(chunk["start"]), float(chunk["end"])
        text = " ".join(chunk["text"].split())
        if not text or not previous_end <= start < end <= cue_limit + 1e-6:
            raise ValueError(f"Invalid narration cue in {timing_path}: {start:g}–{end:g}s")
        cues.extend(split_caption(text, offset + start, offset + min(end, cue_limit)))
        previous_end = end
    return cues


def srt_time(seconds):
    whole, millis = divmod(round(seconds * 1000), 1000)
    minutes, second = divmod(whole, 60)
    hour, minute = divmod(minutes, 60)
    return f"{hour:02d}:{minute:02d}:{second:02d},{millis:03d}"


def package(scene_inputs, output, thumbnail_at):
    output = output.resolve()
    if output.suffix.lower() != ".mp4":
        raise ValueError("Set an .mp4 output path for the package.")
    thumbnail = output.with_suffix(".png")
    captions = output.with_suffix(".srt")
    inputs = []
    filters = []
    audio_filters = []
    subtitles = []
    duration = 0.0
    has_any_audio = False
    for index, scene in enumerate(scene_inputs):
        if not 1 <= len(scene) <= 2:
            raise ValueError("Use --scene VIDEO [NARRATION] for each scene.")
        video, *narration = (Path(value).resolve() for value in scene)
        if any(path in {output, thumbnail, captions} for path in (video, *narration)):
            raise ValueError("Choose an output separate from the input media.")
        length, _, width, height, embedded_audio = video_info(video)
        if index == 0:
            size = f"{width + width % 2}:{height + height % 2}"
        frames = math.ceil(length * PUBLISH_FPS - 1e-5)
        scene_length = frames / PUBLISH_FPS
        video_input = len(inputs) // 2
        inputs.extend(("-i", video))
        filters.append(
            f"[{video_input}:v:0]setpts=PTS-STARTPTS,fps={PUBLISH_FPS},"
            f"scale={size}:force_original_aspect_ratio=decrease:force_divisible_by=2,"
            f"pad={size}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p,"
            f"tpad=stop_mode=clone:stop_duration=1,trim=end_frame={frames}[v{index}]"
        )
        if narration:
            audio = narration[0]
            subtitles.extend(narration_cues(audio, duration, length))
            audio_source = f"[{len(inputs) // 2}:a:0]"
            inputs.extend(("-i", audio))
        else:
            audio_source = f"[{video_input}:a:0]" if embedded_audio else "anullsrc=r=48000:cl=stereo,"
        has_any_audio = has_any_audio or bool(narration) or embedded_audio
        audio_filters.append(
            f"{audio_source}aformat=sample_rates=48000:channel_layouts=stereo,apad,"
            f"atrim=end_sample={frames * (48000 // PUBLISH_FPS)},asetpts=PTS-STARTPTS[a{index}]"
        )
        duration += scene_length

    count = len(scene_inputs)
    filters.append("".join(f"[v{i}]" for i in range(count)) + f"concat=n={count}:v=1:a=0[video]")
    maps = ["-map", "[video]"]
    if has_any_audio:
        filters.extend(audio_filters)
        filters.append("".join(f"[a{i}]" for i in range(count)) + f"concat=n={count}:v=0:a=1[audio]")
        maps.extend(("-map", "[audio]", "-c:a", "aac", "-b:a", "128k"))
    if thumbnail_at is None:
        thumbnail_at = duration / 2
    if not 0 <= thumbnail_at < duration:
        raise ValueError(f"Choose a thumbnail time from 0 to before {duration:.3f}s.")

    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(dir=output.parent) as stage:
        stage = Path(stage)
        video_path = stage / output.name
        image_path = stage / thumbnail.name
        run_ffmpeg(*inputs, "-filter_complex_threads", 1, "-filter_complex", ";".join(filters), *maps,
                   "-c:v", "libx264", "-preset", "fast", "-crf", 19, "-movflags", "+faststart", video_path)
        actual_length, fps, *_ = video_info(video_path)
        if abs(actual_length - duration) > 1 / PUBLISH_FPS:
            raise RuntimeError(f"Packaged video length {actual_length:.3f}s differs from the scene total {duration:.3f}s")
        extract_frame(video_path, min(thumbnail_at, max(0, actual_length - 1 / fps)), image_path)
        if subtitles:
            (stage / captions.name).write_text("\n".join(
                f"{number}\n{srt_time(start)} --> {srt_time(end)}\n{text}\n"
                for number, (start, end, text) in enumerate(subtitles, 1)
            ), encoding="utf-8")
        video_path.replace(output)
        image_path.replace(thumbnail)
        if subtitles:
            (stage / captions.name).replace(captions)
    return {"video": str(output), "thumbnail": str(thumbnail),
            "captions": str(captions) if subtitles else None, "duration": round(actual_length, 6)}
