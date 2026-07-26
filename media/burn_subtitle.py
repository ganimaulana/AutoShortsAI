"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Burn Subtitle
==================================================
"""

from pathlib import Path
import subprocess


def burn_subtitle(

    input_video,

    subtitle_file,

    output_video,

):

    input_video = Path(input_video)

    subtitle_file = Path(subtitle_file)

    output_video = Path(output_video)

    output_video.parent.mkdir(

        parents=True,

        exist_ok=True

    )

    command = [

        "ffmpeg",

        "-y",

        "-i",
        str(input_video),

        "-vf",
        f"ass={subtitle_file.as_posix()}",

        "-c:a",
        "copy",

        str(output_video)

    ]

    result = subprocess.run(

        command,

        capture_output=True,

        text=True

    )

    if result.returncode != 0:

        raise RuntimeError(

            result.stderr

        )

    return output_video