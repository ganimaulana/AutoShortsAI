"""
==================================================
AutoShortsAI
Clipper Integration Test
==================================================
"""

from pathlib import Path

from media.clipper import clip_video


def test_clipper():

    input_video = Path(
        "downloads/1.mp4"
    )

    output_video = Path(
        "output/test_clip.mp4"
    )

    assert input_video.exists(), (
        f"Video tidak ditemukan:\n{input_video}"
    )

    result = clip_video(
        input_video=input_video,
        output_video=output_video,
        start=10,
        end=20,
    )

    assert result.exists()

    print()

    print("====================================")

    print("Clip berhasil dibuat")

    print(result)

    print("====================================")


if __name__ == "__main__":

    test_clipper()