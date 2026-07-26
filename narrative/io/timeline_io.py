"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Narrative Intelligence Engine (NIE)

Timeline IO
==================================================
"""

from domain.timeline import TimelineClip

from .base_io import BaseIO


class TimelineIO(BaseIO):
    """
    Read / Write TimelineClip objects.
    """

    # =================================================
    # Save
    # =================================================

    @staticmethod
    def save(path, timelines):
        """
        Save TimelineClip list into JSON.
        """

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

    @staticmethod
    def load(path):
        """
        Load TimelineClip list from JSON.
        """

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