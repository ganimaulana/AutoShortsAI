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
from .detector_result import DetectorResult


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

    start: float = 0.0

    end: float = 0.0

    duration: float = 0.0

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
    # Detector Results (NEW)
    # =================================================

    detectors: List[DetectorResult] = field(default_factory=list)

    # =================================================
    # Scores (Legacy Compatibility)
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
    # Detector Helpers
    # =================================================

    def add_detector_result(
        self,
        result: DetectorResult,
    ):

        self.detectors.append(result)

    def get_detector(
        self,
        detector_name: str,
    ):

        for detector in self.detectors:

            if detector.name == detector_name:

                return detector

        return None

    def clear_detectors(self):

        self.detectors.clear()

    # =================================================
    # Helpers
    # =================================================

    def add_segment(self, segment: Segment):

        self.segments.append(segment)

        if len(self.segments) == 1:

            self.start = segment.start

        self.end = segment.end

        self.duration = self.end - self.start

    def clear(self):

        self.segments.clear()

        self.segment_ids.clear()

        self.detectors.clear()

        self.text_cache = ""

        self.start = 0.0

        self.end = 0.0

        self.duration = 0.0

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

            "detectors": [

                detector.to_dict()

                for detector in self.detectors

            ],

            "segments": [

                s.id

                for s in self.segments

            ],

            "text": self.text

        }