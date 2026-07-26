"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Narrative Intelligence Engine

Timeline Builder
==================================================
"""

from typing import List

from config import (
    TIMELINE_PRE_ROLL,
    TIMELINE_POST_ROLL,
    MAX_CLIPS,
)

from domain import Story
from domain.timeline import TimelineClip


class TimelineBuilder:
    """
    Build TimelineClip objects from ranked stories.
    """

    def build(
        self,
        stories: List[Story]
    ) -> List[TimelineClip]:

        if not stories:
            return []

        #
        # Urutkan berdasarkan score tertinggi
        #

        ranked = sorted(

            stories,

            key=lambda s: s.score,

            reverse=True

        )

        timelines = []

        for index, story in enumerate(

            ranked[:MAX_CLIPS],

            start=1

        ):

            start = max(

                0,

                story.start - TIMELINE_PRE_ROLL

            )

            end = story.end + TIMELINE_POST_ROLL

            clip = TimelineClip(

                clip_id=index,

                story_id=story.id,

                start=start,

                end=end,

                duration=end - start,

                score=story.score,

                title=story.title,

                topic=story.topic

            )

            timelines.append(

                clip

            )

        return timelines