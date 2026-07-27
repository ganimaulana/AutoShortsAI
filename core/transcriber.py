"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Video Transcriber
==================================================
"""

from pathlib import Path
import json

from faster_whisper import WhisperModel

from domain.segment import Segment
from domain.word import Word

# ==================================================
# CONFIG
# ==================================================

MODEL_NAME = "base"

#
# Lazy Loaded Model
#

_model = None


# ==================================================
# MODEL
# ==================================================

def get_model() -> WhisperModel:
    """
    Load Whisper model only once.
    """

    global _model

    if _model is None:

        print("Loading Faster-Whisper model...")

        _model = WhisperModel(
            MODEL_NAME,
            device="cpu",
            compute_type="int8",
        )

    return _model


# ==================================================
# TRANSCRIBER
# ==================================================

def transcribe_video(
    video_path: Path,
    project_path: Path,
    language=None,
):
    """
    Transcribe video using Faster-Whisper.

    Returns
    -------
    dict
    """

    video_path = Path(video_path)
    project_path = Path(project_path)

    if not video_path.exists():
        raise FileNotFoundError(video_path)

    transcript_file = project_path / "transcript.txt"
    json_file = project_path / "transcript.json"

    #
    # Lazy Load Model
    #

    model = get_model()

    whisper_segments, info = model.transcribe(
        str(video_path),
        beam_size=5,
        language=language,
        word_timestamps=True,
    )

    transcript_lines = []

    json_segments = []

    segments = []

    # ==================================================

    for index, segment in enumerate(
        whisper_segments,
        start=1,
    ):

        text = segment.text.strip()

        transcript_lines.append(
            f"[{segment.start:.2f} - {segment.end:.2f}] {text}"
        )

        words = []

        json_words = []

        if getattr(segment, "words", None):

            for w in segment.words:

                word = Word(
                    text=w.word.strip(),
                    start=round(w.start, 3),
                    end=round(w.end, 3),
                    confidence=getattr(
                        w,
                        "probability",
                        None,
                    ),
                )

                words.append(word)

                json_words.append(
                    {
                        "text": word.text,
                        "start": word.start,
                        "end": word.end,
                        "confidence": word.confidence,
                    }
                )

        domain_segment = Segment(
            id=index,
            start=round(segment.start, 2),
            end=round(segment.end, 2),
            text=text,
            words=words,
        )

        segments.append(domain_segment)

        json_segments.append(
            {
                "id": index,
                "start": round(segment.start, 2),
                "end": round(segment.end, 2),
                "duration": round(
                    segment.end - segment.start,
                    2,
                ),
                "text": text,
                "words": json_words,
            }
        )

    # ==================================================
    # TXT
    # ==================================================

    transcript_file.write_text(
        "\n".join(transcript_lines),
        encoding="utf-8",
    )

    # ==================================================
    # JSON
    # ==================================================

    with open(
        json_file,
        "w",
        encoding="utf-8",
    ) as f:

        json.dump(
            json_segments,
            f,
            indent=4,
            ensure_ascii=False,
        )

    # ==================================================
    # RETURN
    # ==================================================

    return {
        "language": info.language,
        "duration": round(info.duration, 2),
        "segments": segments,
        "segment_count": len(segments),
        "transcript_file": transcript_file,
        "json_file": json_file,
    }