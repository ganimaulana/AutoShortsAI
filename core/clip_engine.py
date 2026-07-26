"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Clip Engine
==================================================
"""

from pathlib import Path
from typing import List

from domain.timeline import TimelineClip
from media.clipper import clip_video


class ClipEngine:
    """
    Generate video clips from TimelineClip objects.
    """

    # -------------------------------------------------

    def generate(
        self,
        video_path: Path,
        timeline: List[TimelineClip],
        output_dir: Path,
    ) -> List[Path]:

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        generated = []

        for clip in timeline:

            output_file = (
                output_dir /
                f"clip{clip.clip_id:03}.mp4"
            )

            clip_video(
                input_video=video_path,
                output_video=output_file,
                start=clip.start,
                end=clip.end,
                pre_roll=0,
                post_roll=0,
            )

            generated.append(output_file)

        return generated

    # -------------------------------------------------
    # Engine V2 Wrapper
    # -------------------------------------------------

    def process(self, context):
        """
        Pipeline wrapper.

        Input
        -----
        ProjectContext

        Output
        ------
        ProjectContext
        """

        clips_dir = context.project_path / "clips"

        context.clips = self.generate(
            video_path=context.video_path,
            timeline=context.timeline,
            output_dir=clips_dir,
        )

        return context