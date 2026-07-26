"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Segment Domain Model
==================================================
"""

from dataclasses import dataclass, field
from typing import Any

from .word import Word


@dataclass(slots=True)
class Segment:
    """
    Whisper Segment.

    Dapat digunakan untuk transcript biasa maupun
    transcript dengan word timestamp.
    """

    # ==================================================
    # Identity
    # ==================================================

    id: int

    # ==================================================
    # Timeline
    # ==================================================

    start: float

    end: float

    # ==================================================
    # Content
    # ==================================================

    text: str

    words: list[Word] = field(default_factory=list)

    # ==================================================
    # AI Metadata
    # ==================================================

    confidence: float | None = None

    speaker: str | None = None

    metadata: dict[str, Any] = field(default_factory=dict)

    # ==================================================
    # Properties
    # ==================================================

    @property
    def duration(self) -> float:

        return self.end - self.start

    @property
    def word_count(self) -> int:

        return len(self.text.split())

    @property
    def has_words(self) -> bool:

        return len(self.words) > 0

    # ==================================================
    # Helpers
    # ==================================================

    def add_word(self, word: Word):

        self.words.append(word)

    # ==================================================
    # Export
    # ==================================================

    def to_dict(self):

        return {

            "id": self.id,

            "start": self.start,

            "end": self.end,

            "duration": self.duration,

            "text": self.text,

            "confidence": self.confidence,

            "speaker": self.speaker,

            "words": [

                w.to_dict()

                for w in self.words

            ],

            "metadata": self.metadata

        }