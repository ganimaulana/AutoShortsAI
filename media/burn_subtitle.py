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

    input_video = Path(input_video).resolve()
    subtitle_file = Path(subtitle_file).resolve()
    output_video = Path(output_video).resolve()

    output_video.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    #
    # Windows membutuhkan path absolute
    #
    ass_path = subtitle_file.as_posix()

    #
    # Escape :
    #
    ass_path = ass_path.replace(":", "\\:")

    vf = f"ass='{ass_path}'"

    command = [
        "ffmpeg",
        "-y",

        "-i",
        str(input_video),

        "-vf",
        vf,

        "-map",
        "0:v",

        "-map",
        "0:a?",

        "-c:v",
        "libx264",

        "-preset",
        "veryfast",

        "-crf",
        "18",

        "-c:a",
        "copy",

        str(output_video),
    ]

    print("=" * 80)
    print("FFMPEG COMMAND")
    print("=" * 80)
    print(" ".join(command))
    print()
    print("=" * 80)
    print("INPUT VIDEO")
    print(input_video)

    print("OUTPUT VIDEO")
    print(output_video)

    print("SUBTITLE")
    print(subtitle_file)

    print("=" * 80)
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    print("=" * 80)
    print("STDOUT")
    print("=" * 80)
    print(result.stdout)

    print("=" * 80)
    print("STDERR")
    print("=" * 80)
    print(result.stderr)

    if result.returncode != 0:
        raise RuntimeError(result.stderr)

    return output_video