"""
==================================================
Gani Creative Studio
Powered by Naraseta

Narrative Intelligence Engine (NIE)

Story IO
==================================================
"""

from domain import Story

from .base_io import BaseIO


class StoryIO(BaseIO):
    """
    Read / Write Story objects.
    """

    # =================================================
    # Save
    # =================================================

    @staticmethod
    def save(path, stories):
        """
        Save Story list into JSON.
        """

        output = {

            "stories": [

                story.to_dict()

                for story in stories

            ]

        }

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
        Load Story list from JSON.
        """

        data = BaseIO.load_json(path)

        stories = []

        for item in data.get("stories", []):

            story = Story(

                id=item.get("id", 0)

            )

            # -----------------------------------------
            # Timeline
            # -----------------------------------------

            story.start = item.get(

                "start",

                0.0

            )

            story.end = item.get(

                "end",

                0.0

            )

            story.duration = item.get(

                "duration",

                0.0

            )

            # -----------------------------------------
            # Cache
            # -----------------------------------------

            story.text_cache = item.get(

                "text",

                ""

            )

            story.segment_ids = item.get(

                "segments",

                []

            )

            # -----------------------------------------
            # Metadata
            # -----------------------------------------

            story.title = item.get(

                "title",

                ""

            )

            story.summary = item.get(

                "summary",

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

            story.tags = item.get(

                "tags",

                []

            )

            # -----------------------------------------
            # Scores
            # -----------------------------------------

            story.hook_score = item.get(

                "hook_score",

                0.0

            )

            story.conflict_score = item.get(

                "conflict_score",

                0.0

            )

            story.ending_score = item.get(

                "ending_score",

                0.0

            )

            story.engagement_score = item.get(

                "engagement_score",

                0.0

            )

            story.clip_priority = item.get(

                "clip_priority",

                0.0

            )

            story.score = item.get(

                "score",

                0.0

            )

            stories.append(

                story

            )

        return stories