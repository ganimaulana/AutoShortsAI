"""
==================================================
Gani Creative Studio
Powered by Naraseta

Video Downloader
==================================================
"""

from pathlib import Path
from yt_dlp import YoutubeDL


def download_video(url: str, output_dir: Path) -> Path:
    """
    Download video YouTube ke folder project.

    Parameters
    ----------
    url : str
        URL video YouTube.

    output_dir : Path
        Folder project.

    Returns
    -------
    Path
        Lokasi file original.mp4
    """

    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "original.%(ext)s"

    options = {

        # Video terbaik + audio terbaik
        "format": "bv*+ba/b",

        # Output
        "outtmpl": str(output_file),

        # Paksa hasil akhir MP4
        "merge_output_format": "mp4",

        # Overwrite jika sudah ada
        "overwrites": True,

        # Jangan download playlist
        "noplaylist": True,

        # Lebih rapi
        "quiet": True,
        "no_warnings": True,

    }

    with YoutubeDL(options) as ydl:
        ydl.download([url])

    return output_dir / "original.mp4"