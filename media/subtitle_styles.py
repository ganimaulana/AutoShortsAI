"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Subtitle Styles
==================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class SubtitleStyle:

    name: str

    font: str = "Arial"

    size: int = 58

    primary_color: str = "&H00FFFFFF"

    outline_color: str = "&H00000000"

    back_color: str = "&H64000000"

    bold: bool = True

    italic: bool = False

    outline: float = 2.0

    shadow: float = 0.8

    alignment: int = 2

    margin_v: int = 70

    margin_l: int = 40

    margin_r: int = 40


# ======================================================
# Built-in Styles
# ======================================================

DEFAULT_STYLE = SubtitleStyle(
    name="Default"
)

TIKTOK_STYLE = SubtitleStyle(

    name="TikTok",

    font="Arial",

    size=64,

    bold=True,

    outline=2.5,

    shadow=1.0,

    margin_v=90

)

CAPCUT_STYLE = SubtitleStyle(

    name="CapCut",

    font="Arial",

    size=62,

    bold=True,

    outline=2.2,

    shadow=0.5,

    margin_v=80

)