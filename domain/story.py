"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Story Domain Model
==================================================
"""

from dataclasses import dataclass, field
from typing import List

from .segment import Segment


@dataclass(slots=True)
class Story:
    """
    Story Unit.

    Satu Story terdiri dari beberapa Whisper Segment
    yang membentuk satu konteks cerita.
    """

    # =================================================
    # Identity
    # =================================================

    id: int

    # =================================================
    # Content
    # =================================================

    segments: List[Segment] = field(default_factory=list)

    segment_ids: List[int] = field(default_factory=list)

    text_cache: str = ""

    # =================================================
    # AI Metadata
    # =================================================

    title: str = ""

    summary: str = ""

    topic: str = ""

    emotion: str = ""

    tags: List[str] = field(default_factory=list)

    # =================================================
    # Scores
    # =================================================

    hook_score: float = 0.0

    conflict_score: float = 0.0

    ending_score: float = 0.0

    engagement_score: float = 0.0

    clip_priority: float = 0.0

    score: float = 0.0

    # =================================================
    # Properties
    # =================================================

    @property
    def start(self):

        if not self.segments:
            return 0

        return self.segments[0].start

    @property
    def end(self):

        if not self.segments:
            return 0

        return self.segments[-1].end

    @property
    def duration(self):

        return self.end - self.start

    @property
    def text(self):

        if self.segments:

            return " ".join(
                s.text.strip()
                for s in self.segments
            )

        return self.text_cache

    @property
    def word_count(self):

        return len(
            self.text.split()
        )

    # =================================================
    # Helpers
    # =================================================

    def add_segment(self, segment: Segment):

        self.segments.append(segment)

    def clear(self):

        self.segments.clear()

    def __len__(self):

        return len(self.segments)

    # =================================================
    # Export
    # =================================================

    def to_dict(self):

        return {

            "id": self.id,

            "start": self.start,

            "end": self.end,

            "duration": self.duration,

            "word_count": self.word_count,

            "title": self.title,

            "summary": self.summary,

            "topic": self.topic,

            "emotion": self.emotion,

            "tags": self.tags,

            "hook_score": self.hook_score,

            "conflict_score": self.conflict_score,

            "ending_score": self.ending_score,

            "engagement_score": self.engagement_score,

            "clip_priority": self.clip_priority,

            "score": self.score,

            "segments": [

                s.id

                for s in self.segments

            ],

            "text": self.text

        }