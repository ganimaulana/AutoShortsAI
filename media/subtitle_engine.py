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
from media.burn_subtitle import burn_subtitle


class SubtitleEngine:

    def __init__(self):

        self.generator = ASSGenerator()

    # -------------------------------------------------

    def process(

        self,

        input_video,

        segments,

        output_video,

    ):

        input_video = Path(input_video)

        output_video = Path(output_video)

        output_video.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        subtitle_file = output_video.with_suffix(".ass")

        #
        # Generate ASS
        #

        self.generator.save(

            subtitle_file,

            segments

        )

        #
        # Burn Subtitle
        #

        burn_subtitle(

            input_video,

            subtitle_file,

            output_video,

        )

        #
        # Hapus file sementara
        #

        if subtitle_file.exists():

            subtitle_file.unlink()

        return output_video