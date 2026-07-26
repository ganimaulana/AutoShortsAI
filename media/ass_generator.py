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


class ASSGenerator:

    def __init__(self, style=None):

        self.style = style or DEFAULT_STYLE

    # -------------------------------------------------

    @staticmethod
    def format_time(seconds: float):

        h = int(seconds // 3600)

        m = int((seconds % 3600) // 60)

        s = seconds % 60

        return f"{h}:{m:02}:{s:05.2f}"

    # -------------------------------------------------

    def header(self):

        s = self.style

        return f"""
[Script Info]
ScriptType: v4.00+

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding

Style: Default,{s.font},{s.size},{s.primary_color},&H000000FF,{s.outline_color},{s.back_color},{-1 if s.bold else 0},{-1 if s.italic else 0},0,0,100,100,0,0,1,{s.outline},{s.shadow},{s.alignment},{s.margin_l},{s.margin_r},{s.margin_v},1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""

    # -------------------------------------------------

    def build(self, segments):

        output = [self.header()]

        for seg in segments:

            output.append(

                f"Dialogue: 0,{self.format_time(seg.start)},{self.format_time(seg.end)},Default,,0,0,0,,{seg.text}"

            )

        return "\n".join(output)

    # -------------------------------------------------

    def save(self, path, segments):

        path = Path(path)

        path.write_text(

            self.build(segments),

            encoding="utf-8"

        )

        return path