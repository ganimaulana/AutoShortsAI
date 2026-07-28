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
from narrative.io.timeline_io import TimelineIO
from utils.logger import logger


class TimelineBuilder:
    """
    Build TimelineClip objects from ranked stories.
    """

    # -------------------------------------------------

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

            timelines.append(clip)

        return timelines

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

        #
        # Smart Timeline Cache
        #

        if TimelineIO.exists(context.project_path):

            logger.info("Timeline cache found.")

            context.timeline = TimelineIO.load(
                context.project_path
            )

            logger.info(
                f"Loaded {len(context.timeline)} timeline clips."
            )

            return context

        #
        # Build Timeline
        #

        context.timeline = self.build(
            context.stories
        )

        TimelineIO.save(
            context.project_path,
            context.timeline,
        )

        return context