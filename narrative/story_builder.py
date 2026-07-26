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

        stories = self._merge_short_stories(
            stories
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

        # -------------------------------------------------

    def _should_start_new_story(
        self,
        story: Story,
        segment: Segment
    ) -> bool:

        if len(story) == 0:
            return False

        last = story.segments[-1]

        gap = segment.start - last.end

        if gap > MAX_SILENCE_GAP:
            return True

        if story.duration >= MAX_STORY_DURATION:
            return True

        if (
            story.duration >= TARGET_STORY_DURATION
            and gap >= 1.0
        ):
            return True

        return False

    # -------------------------------------------------

    def _finalize_story(
        self,
        story: Story
    ) -> Story:

        story.segment_ids = [

            s.id

            for s in story.segments

        ]

        story.text_cache = story.text

        return story

    # -------------------------------------------------

    def _merge_short_stories(
        self,
        stories: List[Story]
    ) -> List[Story]:

        if not stories:
            return stories

        merged = []

        for story in stories:

            if (
                merged
                and story.duration < MIN_STORY_DURATION
            ):

                previous = merged[-1]

                for seg in story.segments:
                    previous.add_segment(seg)

                previous.segment_ids = [

                    s.id

                    for s in previous.segments

                ]

                previous.text_cache = previous.text

            else:

                merged.append(story)

        return merged       
    
     # -------------------------------------------------

    def process(self, context):
        """
        Engine V2 wrapper.

        Input
        -----
        ProjectContext

        Output
        ------
        ProjectContext
        """

        transcript = context.transcript

        #
        # Support beberapa bentuk input
        #

        if isinstance(transcript, dict):

            # Jika nanti transcriber mengembalikan
            # {"segments": [...]}
            segments = transcript.get("segments", [])

        else:

            segments = transcript

        context.stories = self.build(
            segments
        )

        return context