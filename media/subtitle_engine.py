"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Subtitle Engine
==================================================
"""

from pathlib import Path

from media.ass_generator import ASSGenerator


class SubtitleEngine:

    def __init__(self):

        self.generator = ASSGenerator()

    # -------------------------------------------------

    def generate(

        self,

        segments,

        output_file,

    ):

        output_file = Path(output_file)

        output_file.parent.mkdir(

            parents=True,

            exist_ok=True

        )

        return self.generator.save(

            output_file,

            segments

        )