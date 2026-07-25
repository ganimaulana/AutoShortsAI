"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Narrative Intelligence Engine

Story Builder
==================================================
"""

from typing import List

from config import (
    MIN_SEGMENT_WORDS,
    MIN_STORY_DURATION,
    TARGET_STORY_DURATION,
    MAX_STORY_DURATION,
    MAX_SILENCE_GAP,
)

from domain import Segment
from domain import Story


class StoryBuilder:
    """
    Build Story Unit from Whisper Segments.

    Input:
        List[Segment]

    Output:
        List[Story]
    """

    # -------------------------------------------------

    def __init__(self):

        self.story_id = 1

    # -------------------------------------------------

    def build(
        self,
        segments: List[Segment]
    ) -> List[Story]:

        if not segments:
            return []

        segments = self._merge_small_segments(
            segments
        )

        stories = []

        current_story = Story(
            id=self.story_id
        )

        for segment in segments:

            if self._should_start_new_story(
                current_story,
                segment
            ):

                if len(current_story):

                    stories.append(
                        self._finalize_story(
                            current_story
                        )
                    )

                    self.story_id += 1

                current_story = Story(
                    id=self.story_id
                )

            current_story.add_segment(
                segment
            )

        if len(current_story):

            stories.append(

                self._finalize_story(
                    current_story
                )

            )

        return stories

    # -------------------------------------------------

    def _merge_small_segments(

        self,

        segments: List[Segment]

    ) -> List[Segment]:

        """
        Merge very short Whisper segments.

        Example

        I lost

        500 million

        because overlot.

        →

        I lost 500 million because overlot.
        """

        if not segments:

            return []

        merged = []

        buffer = None

        for segment in segments:

            if buffer is None:

                buffer = Segment(

                    id=segment.id,

                    start=segment.start,

                    end=segment.end,

                    text=segment.text

                )

                continue

            #
            # merge jika buffer terlalu pendek
            #

            if buffer.word_count < MIN_SEGMENT_WORDS:

                buffer.end = segment.end

                buffer.text += " " + segment.text

            else:

                merged.append(buffer)

                buffer = Segment(

                    id=segment.id,

                    start=segment.start,

                    end=segment.end,

                    text=segment.text

                )

        if buffer:

            merged.append(buffer)

        return merged