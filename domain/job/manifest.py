from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class Manifest:
    """
    Semua file yang dihasilkan selama pipeline.

    Untuk MVP kita gunakan Path.
    Setelah MVP selesai baru direfactor menjadi Asset jika diperlukan.
    """

    # Download
    video: Path | None = None
    audio: Path | None = None
    thumbnail: Path | None = None
    metadata: Path | None = None

    # Whisper
    transcript_raw: Path | None = None

    # AI
    transcript_corrected: Path | None = None

    # Subtitle
    subtitle_srt: Path | None = None

    # Render
    renders: list[Path] = field(default_factory=list)