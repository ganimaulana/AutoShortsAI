from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


@dataclass(slots=True)
class Sentence:
    """A normalized sentence derived from one or more transcript segments."""

    id: int
    start: float
    end: float
    text: str
    segment_ids: list[int] = field(default_factory=list)

    @property
    def duration(self) -> float:
        return self.end - self.start


class StorySegmentType(str, Enum):
    HOOK = "Hook"
    CONTEXT = "Context"
    QUESTION = "Question"
    FACT = "Fact"
    PROBLEM = "Problem"
    CONFLICT = "Conflict"
    BUILD_UP = "BuildUp"
    SOLUTION = "Solution"
    RESULT = "Result"
    ENDING = "Ending"
    CTA = "CTA"
    UNKNOWN = "Unknown"


@dataclass(slots=True)
class StorySegment:
    """A deterministic story role spanning one or more sentences."""

    id: int
    primary_type: StorySegmentType
    types: list[StorySegmentType]
    start: float
    end: float
    text: str
    sentence_ids: list[int] = field(default_factory=list)

    @property
    def duration(self) -> float:
        return self.end - self.start
