from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class Manifest:
    """
    Menyimpan seluruh asset yang dihasilkan selama satu Job.

    Untuk MVP seluruh asset masih berupa Path.
    Setelah v1.0 dapat direfactor menjadi Asset object apabila diperlukan.
    """

    # ==========================================================
    # Download
    # ==========================================================

    video: Path | None = None
    audio: Path | None = None
    thumbnail: Path | None = None
    metadata: Path | None = None

    # ==========================================================
    # Whisper
    # ==========================================================

    # File transcript asli (raw.json)
    transcript_raw: Path | None = None

    # Hasil transcript yang sudah berada di memory.
    # Digunakan oleh SubtitleStep agar tidak perlu membaca
    # ulang raw.json.
    transcript_segments: list[Any] = field(default_factory=list)

    # ==========================================================
    # AI
    # ==========================================================

    transcript_corrected: Path | None = None

    # ==========================================================
    # Subtitle
    # ==========================================================

    subtitle_srt: Path | None = None

    # Subtitle utama yang akan dipakai FFmpeg.
    subtitle_ass: Path | None = None

    # ==========================================================
    # Render
    # ==========================================================

    renders: list[Path] = field(default_factory=list)