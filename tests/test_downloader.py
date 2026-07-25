"""
==================================================
AutoShortsAI
Downloader Integration Test
==================================================
"""

from pathlib import Path

from core.downloader import download_video


def test_downloader():

    url = (
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )

    project = Path("temp/test_project")

    video = download_video(
        url=url,
        output_dir=project
    )

    assert video.exists()

    print()

    print("==========================")

    print("Download berhasil")

    print(video)

    print("==========================")


if __name__ == "__main__":

    test_downloader()