"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Video Downloader
==================================================
"""

from pathlib import Path

from yt_dlp import YoutubeDL


def download_video(
    url: str,
    output_dir: Path,
) -> Path:
    """
    Download video YouTube.

    Parameters
    ----------
    url : str

    output_dir : Path

    Returns
    -------
    Path
        Downloaded video path.
    """

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    #
    # Hapus file original lama
    #

    for file in output_dir.glob("original.*"):
        try:
            file.unlink()
        except Exception:
            pass

    output_template = output_dir / "original.%(ext)s"

    options = {

        #
        # Format terbaik
        #

        "format": "bestvideo*+bestaudio/best",

        #
        # Output
        #

        "outtmpl": str(output_template),

        #
        # Jangan download playlist
        #

        "noplaylist": True,

        #
        # Overwrite
        #

        "overwrites": True,

        #
        # Quiet
        #

        "quiet": False,
        "no_warnings": False,
        "progress_hooks": [
            lambda d: print(
                "[yt-dlp]",
                d.get("status"),
                d.get("downloaded_bytes", 0),
                "/",
                d.get("total_bytes") or d.get("total_bytes_estimate"),
            )
        ],

    }

    with YoutubeDL(options) as ydl:

        ydl.download([url])

    #
    # Cari hasil download
    #

    candidates = sorted(

        output_dir.glob("original.*")

    )

    if not candidates:

        raise FileNotFoundError(

            "Downloaded video not found."

        )

    #
    # Ambil file pertama
    #

    return candidates[0]