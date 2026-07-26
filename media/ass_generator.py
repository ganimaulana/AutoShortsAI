"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

ASS Subtitle Generator
==================================================
"""

from pathlib import Path

from media.subtitle_styles import DEFAULT_STYLE
from media.text_layout import TextLayout


class ASSGenerator:

    def __init__(
        self,
        style=None,
        layout=None,
    ):

        self.style = style or DEFAULT_STYLE
        self.layout = layout or TextLayout()

    # =================================================
    # Time
    # =================================================

    @staticmethod
    def format_time(seconds: float) -> str:

        hours = int(seconds // 3600)

        minutes = int((seconds % 3600) // 60)

        secs = seconds % 60

        return f"{hours}:{minutes:02}:{secs:05.2f}"

    # =================================================
    # ASS Escape
    # =================================================

    @staticmethod
    def escape(text: str) -> str:

        return (

            text

            .replace("\\", "\\\\")

            .replace("{", "\\{")

            .replace("}", "\\}")

        )

    # =================================================
    # Header
    # =================================================

    def header(self):

        s = self.style

        return f"""[Script Info]
Title: AutoShortsAI
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding

Style: Default,{s.font},{s.size},{s.primary_color},&H000000FF,{s.outline_color},{s.back_color},{-1 if s.bold else 0},{-1 if s.italic else 0},0,0,100,100,0,0,1,{s.outline},{s.shadow},{s.alignment},{s.margin_l},{s.margin_r},{s.margin_v},1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""

    # =================================================
    # Dialogue
    # =================================================

    def dialogue(self, segment):

        text = self.layout.format(

            self.escape(

                segment.text

            )

        )

        return (

            f"Dialogue: 0,"

            f"{self.format_time(segment.start)},"

            f"{self.format_time(segment.end)},"

            f"Default,,0,0,0,,"

            f"{text}"

        )

    # =================================================
    # Build
    # =================================================

    def build(self, segments):

        lines = [

            self.header()

        ]

        for seg in segments:

            lines.append(

                self.dialogue(seg)

            )

        return "\n".join(lines)

    # =================================================
    # Save
    # =================================================

    def save(

        self,

        path,

        segments,

    ):

        path = Path(path)

        path.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        path.write_text(

            self.build(segments),

            encoding="utf-8"

        )

        return path