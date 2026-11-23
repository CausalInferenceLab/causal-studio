"""Use measured narration beats as deadlines in a Manim Scene."""

from contextlib import contextmanager
import json
import math

from manim import config


class BeatClock:
    def __init__(self, scene, timings_path, preview_durations):
        self.scene = scene
        self.frame = 1 / config.frame_rate
        self.index = 0
        self.windows = []
        cursor = 0.0
        if timings_path.is_file():
            metadata = json.loads(timings_path.read_text(encoding="utf-8"))
            chunks = metadata["chunks"]
            if len(chunks) != len(preview_durations):
                raise ValueError("Narration chunk count differs from the Scene beat count. Recheck the scene plan.")
            for chunk in chunks:
                start, end = float(chunk["start"]), float(chunk["end"])
                if not (math.isfinite(end) and cursor <= start < end):
                    raise ValueError("Narration timings must contain ordered, non-overlapping beats.")
                self.windows.append((start, end))
                cursor = end
            duration = float(metadata["totalDuration"])
            if not math.isfinite(duration) or duration <= 0:
                raise ValueError("Narration duration must be finite.")
            self.end = max(cursor, duration)
        else:
            for duration in preview_durations:
                self.windows.append((cursor, cursor + duration))
                cursor += duration
            self.end = cursor

    def wait_until(self, target, label):
        remaining = target - self.scene.time
        if remaining < -self.frame - 1e-6:
            raise ValueError(f"{label} missed by {-remaining:.2f}s. Shorten or split the animation before rendering.")
        if remaining > 1e-6:
            frames = math.ceil((remaining - 1e-6) / self.frame)
            self.scene.wait(math.nextafter(frames * self.frame, math.inf))

    @contextmanager
    def beat(self):
        if self.index >= len(self.windows):
            raise ValueError("The Scene has more animation beats than narration chunks.")
        start, end = self.windows[self.index]
        number = self.index + 1
        self.wait_until(start, f"Beat {number} start")
        yield end - start
        self.wait_until(end, f"Beat {number} end")
        self.index += 1

    def finish(self, tail=0.5):
        if self.index != len(self.windows):
            raise ValueError("The Scene has fewer animation beats than narration chunks.")
        self.wait_until(self.end + tail, "End of narration tail")
