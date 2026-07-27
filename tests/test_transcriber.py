"""
==================================================
AutoShortsAI
Transcriber Test
==================================================
"""

from pathlib import Path

from core.downloader import download_video
from core.transcriber import transcribe_video


TEST_URL = "https://www.youtube.com/watch?v=Frcu00VNXtE"


def test_transcriber(tmp_path):

    #
    # Download sample
    #

    video = download_video(

        TEST_URL,

        tmp_path,

    )

    assert video.exists()

    #
    # Transcribe
    #

    transcript = transcribe_video(

        video_path=video,

        project_path=tmp_path,

        language=None,

    )

    #
    # Validate
    #

    assert transcript is not None

    assert "segments" in transcript

    assert len(
        transcript["segments"]
    ) > 0