"""
==================================================
Gani Creative Studio
Powered by Naraseta

Video Clipper
==================================================
"""

from pathlib import Path
import subprocess


def clip_video(
    input_video: Path,
    output_video: Path,
    start: float,
    end: float,
    pre_roll: float = 1.0,
    post_roll: float = 1.0,
):
    """
    Memotong video menggunakan FFmpeg.

    Parameters
    ----------
    input_video : Path
    output_video : Path
    start : float
    end : float
    pre_roll : float
    post_roll : float
    """

    input_video = Path(input_video)
    output_video = Path(output_video)

    output_video.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    start_time = max(0, start - pre_roll)
    duration = (end - start) + pre_roll + post_roll

    command = [

        "ffmpeg",

        "-y",

        "-ss",
        str(start_time),

        "-i",
        str(input_video),

        "-t",
        str(duration),

        "-c",
        "copy",

        str(output_video)

    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:

        raise RuntimeError(result.stderr)

    return output_video