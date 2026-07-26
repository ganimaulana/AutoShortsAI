"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Subtitle Presets
==================================================
"""

from media.subtitle_styles import SubtitleStyle


PRESETS = {

    "default": SubtitleStyle(

        name="Default",

        font="Arial",

        size=58,

        bold=True,

        outline=2.0,

        shadow=0.8,

        margin_v=70,

    ),

    "tiktok": SubtitleStyle(

        name="TikTok",

        font="Arial",

        size=68,

        bold=True,

        outline=2.5,

        shadow=1.2,

        margin_v=110,

    ),

    "capcut": SubtitleStyle(

        name="CapCut",

        font="Arial",

        size=64,

        bold=True,

        outline=2.0,

        shadow=0.5,

        margin_v=90,

    ),

    "gaming": SubtitleStyle(

        name="Gaming",

        font="Arial",

        size=72,

        bold=True,

        outline=3,

        shadow=1,

        margin_v=120,

    ),

    "podcast": SubtitleStyle(

        name="Podcast",

        font="Arial",

        size=56,

        bold=False,

        outline=1.5,

        shadow=0.5,

        margin_v=60,

    ),

    "minimal": SubtitleStyle(

        name="Minimal",

        font="Arial",

        size=50,

        bold=False,

        outline=1,

        shadow=0,

        margin_v=60,

    ),

    "cinema": SubtitleStyle(

        name="Cinema",

        font="Georgia",

        size=52,

        bold=False,

        outline=1,

        shadow=0,

        margin_v=80,

    )

}


def get_style(name: str):

    return PRESETS.get(

        name.lower(),

        PRESETS["default"]

    )