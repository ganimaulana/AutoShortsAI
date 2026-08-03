"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Subtitle Presets
==================================================
"""

from config import settings
from media.subtitle_styles import SubtitleStyle


def _style(
    name: str,
    font: str,
    size: int,
    bold: bool,
    outline: float,
    shadow: float,
    margin_v: int,
) -> SubtitleStyle:

    return SubtitleStyle(
        name=name,
        font=font,
        size=size,
        bold=bold,
        outline=outline,
        shadow=shadow,
        margin_v=margin_v,
    )


PRESETS = {

    "default": _style(
        name="Default",
        font="Arial",
        size=settings.subtitle.font_size,
        bold=True,
        outline=2.0,
        shadow=0.8,
        margin_v=settings.subtitle.margin_bottom,
    ),

    "tiktok": _style(
        name="TikTok",
        font="Arial",
        size=max(
            settings.subtitle.font_size,
            68,
        ),
        bold=True,
        outline=2.5,
        shadow=1.2,
        margin_v=max(
            settings.subtitle.margin_bottom,
            110,
        ),
    ),

    "capcut": _style(
        name="CapCut",
        font="Arial",
        size=max(
            settings.subtitle.font_size,
            64,
        ),
        bold=True,
        outline=2.0,
        shadow=0.5,
        margin_v=max(
            settings.subtitle.margin_bottom,
            90,
        ),
    ),

    "gaming": _style(
        name="Gaming",
        font="Arial",
        size=max(
            settings.subtitle.font_size,
            72,
        ),
        bold=True,
        outline=3.0,
        shadow=1.0,
        margin_v=max(
            settings.subtitle.margin_bottom,
            120,
        ),
    ),

    "podcast": _style(
        name="Podcast",
        font="Arial",
        size=settings.subtitle.font_size,
        bold=False,
        outline=1.5,
        shadow=0.5,
        margin_v=settings.subtitle.margin_bottom,
    ),

    "minimal": _style(
        name="Minimal",
        font="Arial",
        size=max(
            settings.subtitle.font_size - 4,
            32,
        ),
        bold=False,
        outline=1.0,
        shadow=0.0,
        margin_v=settings.subtitle.margin_bottom,
    ),

    "cinema": _style(
        name="Cinema",
        font="Georgia",
        size=max(
            settings.subtitle.font_size - 2,
            32,
        ),
        bold=False,
        outline=1.0,
        shadow=0.0,
        margin_v=settings.subtitle.margin_bottom,
    ),
}


def get_style(name: str) -> SubtitleStyle:
    """
    Get subtitle style by preset name.

    Falls back to the default preset if the requested
    preset does not exist.
    """

    if not name:
        name = "default"

    return PRESETS.get(
        name.lower(),
        PRESETS["default"],
    )