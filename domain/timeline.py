"""
==================================================
Narrative Intelligence Engine (NIE)

Timeline Model
==================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class TimelineClip:

    id: int

    start: float

    end: float

    story_id: int

    title: str = ""

    @property
    def duration(self):

        return self.end - self.start