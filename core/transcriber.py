"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI
Video Transcriber
==================================================
"""

from pathlib import Path
from faster_whisper import WhisperModel
import json

# ==================================================
# MODEL
# ==================================================

MODEL_NAME = "base"

model = WhisperModel(
    MODEL_NAME,
    device="cpu",
    compute_type="int8"
)

# ==================================================
# TRANSCRIBER
# ==================================================

def transcribe_video(
    video_path: Path,
    project_path: Path,
    language=None
):
    """
    Melakukan transkripsi video menggunakan Faster-Whisper.

    Parameters
    ----------
    video_path : Path
        Lokasi original.mp4

    project_path : Path
        Folder project

    language : str | None
        Misal "id", "en".
        Jika None maka Whisper akan mendeteksi otomatis.
    """

    video_path = Path(video_path)
    project_path = Path(project_path)

    if not video_path.exists():
        raise FileNotFoundError(video_path)

    transcript_file = project_path / "transcript.txt"
    json_file = project_path / "transcript.json"

    segments, info = model.transcribe(
        str(video_path),
        beam_size=5,
        language=language
    )

    transcript_lines = []
    json_segments = []

    for segment in segments:

        text = segment.text.strip()

        transcript_lines.append(
            f"[{segment.start:.2f} - {segment.end:.2f}] {text}"
        )

        json_segments.append({

            "start": round(segment.start, 2),

            "end": round(segment.end, 2),

            "duration": round(
                segment.end - segment.start,
                2
            ),

            "text": text

        })

    transcript_file.write_text(
        "\n".join(transcript_lines),
        encoding="utf-8"
    )

    with open(
        json_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            json_segments,
            f,
            indent=4,
            ensure_ascii=False
        )

    return {

        "language": info.language,

        "duration": round(info.duration, 2),

        "segments": len(json_segments),

        "transcript_file": transcript_file,

        "json_file": json_file

    }