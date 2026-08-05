from __future__ import annotations

from dataclasses import dataclass

from domain.story_intelligence import StorySegmentType


@dataclass(frozen=True, slots=True)
class StoryPattern:
    """Defines an ordered story shape that can produce a clip candidate."""

    name: str
    priority: int
    sequence: tuple[StorySegmentType, ...]
    max_gap: int
    minimum_duration: float
    maximum_duration: float

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be empty.")
        if self.priority < 0:
            raise ValueError("priority must be greater than or equal to zero.")
        if not self.sequence:
            raise ValueError("sequence must not be empty.")
        if self.max_gap < 0:
            raise ValueError("max_gap must be greater than or equal to zero.")
        if self.minimum_duration <= 0:
            raise ValueError("minimum_duration must be greater than zero.")
        if self.maximum_duration < self.minimum_duration:
            raise ValueError(
                "maximum_duration must be greater than or equal to minimum_duration."
            )


DEFAULT_STORY_PATTERNS: tuple[StoryPattern, ...] = (
    StoryPattern(
        name="Hook -> Problem -> Solution",
        priority=10,
        sequence=(
            StorySegmentType.HOOK,
            StorySegmentType.PROBLEM,
            StorySegmentType.SOLUTION,
        ),
        max_gap=1,
        minimum_duration=8.0,
        maximum_duration=60.0,
    ),
    StoryPattern(
        name="Hook -> Result",
        priority=20,
        sequence=(StorySegmentType.HOOK, StorySegmentType.RESULT),
        max_gap=1,
        minimum_duration=6.0,
        maximum_duration=45.0,
    ),
    StoryPattern(
        name="Question -> Fact -> Ending",
        priority=30,
        sequence=(
            StorySegmentType.QUESTION,
            StorySegmentType.FACT,
            StorySegmentType.ENDING,
        ),
        max_gap=1,
        minimum_duration=8.0,
        maximum_duration=60.0,
    ),
    StoryPattern(
        name="Problem -> Conflict -> Result",
        priority=40,
        sequence=(
            StorySegmentType.PROBLEM,
            StorySegmentType.CONFLICT,
            StorySegmentType.RESULT,
        ),
        max_gap=1,
        minimum_duration=8.0,
        maximum_duration=60.0,
    ),
)


def get_default_story_patterns() -> tuple[StoryPattern, ...]:
    return tuple(sorted(DEFAULT_STORY_PATTERNS, key=lambda pattern: (pattern.priority, pattern.name)))
