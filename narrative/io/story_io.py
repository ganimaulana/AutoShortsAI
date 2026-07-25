"""
==================================================
Gani Creative Studio
Powered by Naraseta

Narrative Intelligence Engine (NIE)

Story IO
==================================================
"""

from pathlib import Path

from domain import Story
from domain import Segment

from .base_io import BaseIO


class StoryIO(BaseIO):
    """
    Read / Write Story objects.
    """

    @staticmethod
    def save(path, stories):

        output = {

            "stories": []

        }

        for story in stories:

            output["stories"].append({

                "id": story.id,

                "start": story.start,

                "end": story.end,

                "duration": story.duration,

                "word_count": story.word_count,

                "score": story.score,

                "title": story.title,

                "topic": story.topic,

                "emotion": story.emotion,

                "summary": story.summary,

                "segments": [

                    s.id for s in story.segments

                ],

                "text": story.text

            })

        BaseIO.save_json(
            path,
            output
        )

    @staticmethod
    def load(path):

        data = BaseIO.load_json(path)

        stories = []

        for item in data["stories"]:

            story = Story(

                id=item["id"]

            )

            #
            # Segment object belum dimuat
            # karena hanya ID yang disimpan
            #

            story.score = item.get(
                "score",
                0
            )

            story.title = item.get(
                "title",
                ""
            )

            story.topic = item.get(
                "topic",
                ""
            )

            story.emotion = item.get(
                "emotion",
                ""
            )

            story.summary = item.get(
                "summary",
                ""
            )

            #
            # Simpan segment ID sementara
            #

            story.segment_ids = item.get(
                "segments",
                []
            )

            story.cached_text = item.get(
                "text",
                ""
            )

            stories.append(
                story
            )

        return stories