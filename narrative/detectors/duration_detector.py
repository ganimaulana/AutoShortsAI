"""
==================================================
Duration Detector
==================================================
"""

from config import (
    MIN_STORY_DURATION,
    TARGET_STORY_DURATION,
    MAX_STORY_DURATION,
)

from .base_detector import BaseDetector


class DurationDetector(BaseDetector):

    name = "Duration"

    weight = 15

    def score(self, story):

        duration = story.duration

        if duration < MIN_STORY_DURATION:

            return 0

        if duration > MAX_STORY_DURATION:

            return 5

        distance = abs(

            TARGET_STORY_DURATION - duration

        )

        return max(

            0,

            self.weight - distance

        )