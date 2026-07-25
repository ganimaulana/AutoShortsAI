"""
==================================================
Narrative Intelligence Engine (NIE)

Segment Model
==================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Segment:
    """
    Whisper segment.
    """

    id: int

    start: float

    end: float

    text: str

    @property
    def duration(self) -> float:
        return self.end - self.start

    @property
    def word_count(self) -> int:
        return len(self.text.split())