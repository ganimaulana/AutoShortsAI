"""
==================================================
AutoShortsAI
Transcriber Integration Test
==================================================
"""

from pathlib import Path

from core.transcriber import transcribe_video


def test_transcriber():

    project = Path("temp/test_project")

    video = project / "original.mp4"

    assert video.exists(), (
        f"Video tidak ditemukan:\n{video}"
    )

    result = transcribe_video(

        video_path=video,

        project_path=project,

        language=None

    )

    assert result["transcript_file"].exists()

    assert result["json_file"].exists()

    print()

    print("==========================")

    print("Transkripsi berhasil")

    print(result)

    print("==========================")


if __name__ == "__main__":

    test_transcriber()