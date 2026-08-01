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

    def generate(
        self,
        segments,
        output,
    ):

        output = Path(output)

        output.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.generator.save(
            output,
            segments,
        )

        return output

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

        #
        # Simpan subtitle ke folder subtitles
        #

        subtitle_dir = output_video.parent.parent / "subtitles"
        subtitle_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        subtitle_file = subtitle_dir / f"{output_video.stem}.ass"

        #
        # DEBUG
        #

        print("=" * 80)
        print("SUBTITLE DEBUG")
        print("=" * 80)
        print("Input :", input_video)
        print("Output:", output_video)
        print("ASS   :", subtitle_file)
        print("Segments :", len(segments))

        #
        # Generate ASS
        #

        self.generator.save(
            subtitle_file,
            segments,
        )

        if subtitle_file.exists():

            print("ASS Size :", subtitle_file.stat().st_size, "bytes")

            with open(
                subtitle_file,
                "r",
                encoding="utf-8"
            ) as f:

                dialogue = 0

                for line in f:

                    if line.startswith("Dialogue:"):

                        dialogue += 1

                print("Dialogue Count :", dialogue)

        else:

            print("ASS FILE NOT CREATED")

        #
        # Burn Subtitle
        #

        burn_subtitle(
            input_video,
            subtitle_file,
            output_video,
        )

        #
        # DEBUG
        #

        print("=" * 80)
        print("Subtitle Finished")
        print("=" * 80)

        #
        # JANGAN HAPUS ASS
        # Agar bisa dicek manual
        #

        return output_video