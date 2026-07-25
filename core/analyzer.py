"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI
Video Analyzer
==================================================
"""

from yt_dlp import YoutubeDL


def analyze_video(url):

    opsi = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": False,
    }

    with YoutubeDL(opsi) as ydl:

        info = ydl.extract_info(url, download=False)

    # -------------------------------
    # Channel
    # -------------------------------

    channel = (
        info.get("channel")
        or info.get("uploader")
        or info.get("channel_id")
        or "-"
    )

    # -------------------------------
    # Views
    # -------------------------------

    views = info.get("view_count") or 0

    # -------------------------------
    # Duration
    # -------------------------------

    duration = info.get("duration") or 0

    # -------------------------------
    # Upload Date
    # -------------------------------

    upload_date = info.get("upload_date") or ""

    # -------------------------------
    # Thumbnail
    # -------------------------------

    thumbnail = info.get("thumbnail") or ""

    # -------------------------------
    # Resolution
    # -------------------------------

    width = info.get("width") or 0
    height = info.get("height") or 0

    if width and height:
        resolution = f"{width}x{height}"
    else:
        resolution = "-"

    # -------------------------------
    # FPS
    # -------------------------------

    fps = info.get("fps") or 0

    # -------------------------------
    # Return
    # -------------------------------

    return {

        "title": info.get("title", "-"),

        "channel": channel,

        "duration": duration,

        "views": views,

        "upload_date": upload_date,

        "thumbnail": thumbnail,

        "resolution": resolution,

        "fps": fps,

    }