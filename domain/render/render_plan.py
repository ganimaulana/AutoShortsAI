from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class RenderPlan:
    """
    Semua informasi yang dibutuhkan FFmpeg.
    """

    input_video: Path

    output_video: Path

    start: float

    end: float

    subtitle_file: Path | None = None

    crop_vertical: bool = True

    burn_subtitle: bool = True

    add_intro: bool = False

    add_outro: bool = False

    zoom_face: bool = False

    normalize_audio: bool = True