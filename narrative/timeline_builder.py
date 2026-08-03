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

from config import settings

from domain import Story
from domain.timeline import TimelineClip
from narrative.io.timeline_io import TimelineIO
from utils.logger import logger


class TimelineBuilder:
    """
    Build TimelineClip objects from ranked stories.
    """

    def build(
        self,
        stories: List[Story],
    ) -> List[TimelineClip]:

        if not stories:
            return []

        ranked = sorted(
            stories,
            key=lambda s: s.score,
            reverse=True,
        )

        timelines: List[TimelineClip] = []

        max_clips = settings.timeline.max_clips
        pre_roll = settings.timeline.pre_roll
        post_roll = settings.timeline.post_roll

        for index, story in enumerate(
            ranked[:max_clips],
            start=1,
        ):

            start = max(
                0,
                story.start - pre_roll,
            )

            end = story.end + post_roll

            timelines.append(
                TimelineClip(
                    clip_id=index,
                    story_id=story.id,
                    start=start,
                    end=end,
                    duration=end - start,
                    score=story.score,
                    title=story.title,
                    topic=story.topic,
                )
            )

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

        if TimelineIO.exists(context.project_path):

            logger.info("Timeline cache found.")

            context.timeline = TimelineIO.load(
                context.project_path
            )

            logger.info(
                f"Loaded {len(context.timeline)} timeline clips."
            )

            return context

        context.timeline = self.build(
            context.stories
        )

        TimelineIO.save(
            context.project_path,
            context.timeline,
        )

        return context