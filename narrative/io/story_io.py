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

from .base_io import BaseIO


class StoryIO(BaseIO):

    """
    Read / Write Story objects.
    """
    FILE_NAME = "story.json"

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
    def save(cls, path, stories):
        """
        Save Story list into JSON.
        """

        path = cls.resolve_path(path)
        

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

    @classmethod
    def load(cls, path):
        """
        Load Story list from JSON.
        """

        path = cls.resolve_path(path)




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