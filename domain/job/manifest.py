from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Manifest:
    """
    Menyimpan seluruh asset yang digunakan
    dan dihasilkan oleh satu Job.
    """

    # ---------- INPUT ----------
    source_url: str = ""

    video: Path | None = None
    audio: Path | None = None
    thumbnail: Path | None = None

    # ---------- TRANSCRIPT ----------
    transcript_raw: Path | None = None
    transcript_corrected: Path | None = None

    # ---------- AI ----------
    chapters: Path | None = None
    features: Path | None = None
    candidates: Path | None = None
    review: Path | None = None

    # ---------- OUTPUT ----------
    renders: list[Path] = field(default_factory=list)

    subtitles: list[Path] = field(default_factory=list)

    metadata: Path | None = None

    # ---------- LOG ----------
    pipeline_log: Path | None = None
    ai_log: Path | None = None
    ffmpeg_log: Path | None = None
    upload_log: Path | None = None