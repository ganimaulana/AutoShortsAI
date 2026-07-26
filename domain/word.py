"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Word Domain Model
==================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Word:
    """
    Word with timestamp.
    """

    text: str

    start: float

    end: float

    confidence: float = 1.0

    @property
    def duration(self):

        return self.end - self.start

    def to_dict(self):

        return {

            "text": self.text,

            "start": self.start,

            "end": self.end,

            "duration": self.duration,

            "confidence": self.confidence

        }