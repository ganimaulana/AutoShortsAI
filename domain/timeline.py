"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Timeline Domain Model
==================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class TimelineClip:
    """
    Timeline clip generated from a Story.
    """

    # =================================================
    # Identity
    # =================================================

    clip_id: int

    story_id: int

    # =================================================
    # Timeline
    # =================================================

    start: float

    end: float

    duration: float

    # =================================================
    # Ranking
    # =================================================

    score: float

    # =================================================
    # Metadata
    # =================================================

    title: str = ""

    topic: str = ""