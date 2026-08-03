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

from domain.segment import Segment
from domain.word import Word
from narrative.io.transcript_io import TranscriptIO
from utils.logger import logger

from config import settings



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

        logger.info(
            "Loading Faster-Whisper model..."
        )

        _model = WhisperModel(
            settings.whisper.model,
            device=settings.whisper.device,
            compute_type=settings.whisper.compute_type,
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
    json_file = TranscriptIO.resolve_path(
        project_path
    )

    #
    # Smart Cache
    #

    if TranscriptIO.exists(project_path):

        logger.info("Transcript cache found.")

        segments = TranscriptIO.load(project_path)

        logger.info(
            f"Loaded {len(segments)} transcript segments."
        )

        return {
            "language": language,
            "duration": None,
            "segments": segments,
            "segment_count": len(segments),
            "transcript_file": transcript_file,
            "json_file": json_file,
        }

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

                

        domain_segment = Segment(
            id=index,
            start=round(segment.start, 2),
            end=round(segment.end, 2),
            text=text,
            words=words,
        )

        segments.append(domain_segment)

        

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

    TranscriptIO.save(
        project_path,
        segments,
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