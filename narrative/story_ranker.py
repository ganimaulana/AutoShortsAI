"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Narrative Intelligence Engine

Story Ranker
==================================================
"""

from typing import List

from domain import Story

from narrative.story_rules import (
    HOOK_WORDS,
    CONFLICT_WORDS,
    EMOTION_WORDS,
    ENDING_WORDS,
    ENGAGEMENT_WORDS,
)


class StoryRanker:
    """
    Rank Story berdasarkan kualitas.

    Input:
        List[Story]

    Output:
        List[Story] (sudah diberi score)
    """

    # -------------------------------------------------

    def rank(
        self,
        stories: List[Story]
    ) -> List[Story]:

        for story in stories:

            story.hook_score = self._score_hook(story)

            story.conflict_score = self._score_conflict(story)

            story.ending_score = self._score_ending(story)

            story.engagement_score = self._score_engagement(story)

            story.score = self._calculate_score(story)

            story.clip_priority = story.score

        stories.sort(

            key=lambda s: s.score,

            reverse=True

        )

        return stories

    # -------------------------------------------------

    def _count_keywords(

        self,

        text: str,

        words: List[str]

    ) -> int:

        text = text.lower()

        total = 0

        for word in words:

            if word.lower() in text:

                total += 1

        return total

    # -------------------------------------------------

    def _score_hook(

        self,

        story: Story

    ) -> float:

        count = self._count_keywords(

            story.text,

            HOOK_WORDS

        )

        return min(

            count * 5,

            30

        )

    # -------------------------------------------------

    def _score_conflict(

        self,

        story: Story

    ) -> float:

        count = self._count_keywords(

            story.text,

            CONFLICT_WORDS

        )

        return min(

            count * 5,

            25

        )

    # -------------------------------------------------

    def _score_ending(

        self,

        story: Story

    ) -> float:

        count = self._count_keywords(

            story.text,

            ENDING_WORDS

        )

        return min(

            count * 4,

            20

        )

    # -------------------------------------------------

    def _score_engagement(

        self,

        story: Story

    ) -> float:

        count = self._count_keywords(

            story.text,

            ENGAGEMENT_WORDS

        )

        return min(

            count * 5,

            25

        )

    # -------------------------------------------------

    def _calculate_score(

        self,

        story: Story

    ) -> float:

        return (

            story.hook_score

            + story.conflict_score

            + story.ending_score

            + story.engagement_score

        )