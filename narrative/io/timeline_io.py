"""
==================================================
Gani Creative Studio
Powered by Naraseta

Narrative Intelligence Engine (NIE)

Timeline IO
==================================================
"""

from .base_io import BaseIO


class TimelineIO(BaseIO):

    @staticmethod
    def save(path, clips):

        output = {

            "clips": []

        }

        for clip in clips:

            output["clips"].append({

                "id": clip.id,

                "story_id": clip.story_id,

                "start": clip.start,

                "end": clip.end,

                "duration": clip.duration,

                "title": clip.title

            })

        BaseIO.save_json(
            path,
            output
        )

    @staticmethod
    def load(path):

        return BaseIO.load_json(path)