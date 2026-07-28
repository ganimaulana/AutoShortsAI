"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Narrative Intelligence Engine (NIE)

Timeline IO
==================================================
"""

from pathlib import Path

from domain.timeline import TimelineClip

from .base_io import BaseIO


class TimelineIO(BaseIO):

    """
    Read / Write TimelineClip objects.
    """
    FILE_NAME = "timeline.json"

    # =================================================
    # PATH
    # =================================================

    @classmethod
    def path(cls, project_path) -> Path:
        return Path(project_path) / cls.FILE_NAME


    # =================================================
    # RESOLVE PATH
    # =================================================

    @classmethod
    def resolve_path(cls, path) -> Path:

        path = Path(path)

        if path.suffix.lower() == ".json":
            return path

        return path / cls.FILE_NAME


    # =================================================
    # EXISTS
    # =================================================

    @classmethod
    def exists(cls, path) -> bool:

        return cls.resolve_path(path).exists()

    # =================================================
    # Save
    # =================================================

    @classmethod
    def save(cls, path, timelines):
        """
        Save TimelineClip list into JSON.
        """

        path = cls.resolve_path(path)

        output = {

            "clips": []

        }

        for clip in timelines:

            output["clips"].append({

                "clip_id": clip.clip_id,

                "story_id": clip.story_id,

                "start": clip.start,

                "end": clip.end,

                "duration": clip.duration,

                "score": clip.score,

                "title": clip.title,

                "topic": clip.topic

            })

        BaseIO.save_json(

            path,

            output

        )

    # =================================================
    # Load
    # =================================================

    @classmethod
    def load(cls, path):
        """
        Load TimelineClip list from JSON.
        """

        path = cls.resolve_path(path)
        data = BaseIO.load_json(path)

        clips = []

        for item in data.get("clips", []):

            clip = TimelineClip(

                clip_id=item.get(
                    "clip_id",
                    0
                ),

                story_id=item.get(
                    "story_id",
                    0
                ),

                start=item.get(
                    "start",
                    0.0
                ),

                end=item.get(
                    "end",
                    0.0
                ),

                duration=item.get(
                    "duration",
                    0.0
                ),

                score=item.get(
                    "score",
                    0.0
                ),

                title=item.get(
                    "title",
                    ""
                ),

                topic=item.get(
                    "topic",
                    ""
                )

            )

            clips.append(

                clip

            )

        return clips