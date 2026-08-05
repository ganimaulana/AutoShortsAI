import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from application.candidate.story_candidate_builder import StoryCandidateBuilder
from application.candidate.story_patterns import StoryPattern, get_default_story_patterns
from domain.story_intelligence import StorySegment, StorySegmentType


def make_story_segment(
    segment_id: int,
    primary_type: StorySegmentType,
    start: float,
    end: float,
    types: list[StorySegmentType] | None = None,
) -> StorySegment:
    return StorySegment(
        id=segment_id,
        primary_type=primary_type,
        types=types or [primary_type],
        start=start,
        end=end,
        text=f"Segment {segment_id}",
    )


def test_build_returns_candidate_for_successful_pattern_match() -> None:
    builder = StoryCandidateBuilder(
        patterns=(
            StoryPattern(
                name="Hook -> Result",
                priority=1,
                sequence=(StorySegmentType.HOOK, StorySegmentType.RESULT),
                max_gap=0,
                minimum_duration=4.0,
                maximum_duration=10.0,
            ),
        )
    )

    candidates = builder.build(
        [
            make_story_segment(1, StorySegmentType.HOOK, 0.0, 2.0),
            make_story_segment(2, StorySegmentType.RESULT, 3.0, 6.0),
        ]
    )

    assert len(candidates) == 1
    assert candidates[0].start == 0.0
    assert candidates[0].end == 6.0
    assert candidates[0].score == 0.0
    assert candidates[0].reason == "Story Pattern: Hook -> Result"


def test_build_rejects_match_when_unmatched_segment_gap_exceeds_max_gap() -> None:
    builder = StoryCandidateBuilder(
        patterns=(
            StoryPattern(
                name="Hook -> Result",
                priority=1,
                sequence=(StorySegmentType.HOOK, StorySegmentType.RESULT),
                max_gap=0,
                minimum_duration=1.0,
                maximum_duration=20.0,
            ),
        )
    )

    candidates = builder.build(
        [
            make_story_segment(1, StorySegmentType.HOOK, 0.0, 2.0),
            make_story_segment(2, StorySegmentType.CONTEXT, 3.0, 4.0),
            make_story_segment(3, StorySegmentType.RESULT, 5.0, 7.0),
        ]
    )

    assert candidates == []


def test_build_matches_against_secondary_story_segment_types() -> None:
    builder = StoryCandidateBuilder(
        patterns=(
            StoryPattern(
                name="Question -> Fact -> Ending",
                priority=1,
                sequence=(
                    StorySegmentType.QUESTION,
                    StorySegmentType.FACT,
                    StorySegmentType.ENDING,
                ),
                max_gap=0,
                minimum_duration=6.0,
                maximum_duration=20.0,
            ),
        )
    )

    candidates = builder.build(
        [
            make_story_segment(
                1,
                StorySegmentType.HOOK,
                0.0,
                2.0,
                [StorySegmentType.HOOK, StorySegmentType.QUESTION],
            ),
            make_story_segment(
                2,
                StorySegmentType.CONTEXT,
                3.0,
                5.0,
                [StorySegmentType.CONTEXT, StorySegmentType.FACT],
            ),
            make_story_segment(3, StorySegmentType.ENDING, 6.0, 8.0),
        ]
    )

    assert len(candidates) == 1
    assert candidates[0].start == 0.0
    assert candidates[0].end == 8.0


def test_build_removes_duplicate_candidate_windows() -> None:
    builder = StoryCandidateBuilder(
        patterns=(
            StoryPattern(
                name="Primary",
                priority=1,
                sequence=(StorySegmentType.HOOK, StorySegmentType.RESULT),
                max_gap=0,
                minimum_duration=1.0,
                maximum_duration=10.0,
            ),
            StoryPattern(
                name="Duplicate",
                priority=2,
                sequence=(StorySegmentType.QUESTION, StorySegmentType.RESULT),
                max_gap=0,
                minimum_duration=1.0,
                maximum_duration=10.0,
            ),
        )
    )

    candidates = builder.build(
        [
            make_story_segment(
                1,
                StorySegmentType.HOOK,
                0.0,
                2.0,
                [StorySegmentType.HOOK, StorySegmentType.QUESTION],
            ),
            make_story_segment(2, StorySegmentType.RESULT, 3.0, 5.0),
        ]
    )

    assert len(candidates) == 1
    assert candidates[0].reason == "Story Pattern: Primary"


def test_maximum_candidates_is_enforced_after_deduplication() -> None:
    builder = StoryCandidateBuilder(
        patterns=(
            StoryPattern(
                name="Hook -> Result",
                priority=1,
                sequence=(StorySegmentType.HOOK, StorySegmentType.RESULT),
                max_gap=0,
                minimum_duration=1.0,
                maximum_duration=20.0,
            ),
        ),
        maximum_candidates=1,
    )

    candidates = builder.build(
        [
            make_story_segment(1, StorySegmentType.HOOK, 0.0, 1.0),
            make_story_segment(2, StorySegmentType.RESULT, 2.0, 3.0),
            make_story_segment(3, StorySegmentType.HOOK, 4.0, 5.0),
            make_story_segment(4, StorySegmentType.RESULT, 6.0, 7.0),
        ]
    )

    assert len(candidates) == 1
    assert candidates[0].start == 0.0


def test_story_pattern_rejects_invalid_configuration() -> None:
    with pytest.raises(ValueError, match="maximum_duration"):
        StoryPattern(
            name="Invalid",
            priority=1,
            sequence=(StorySegmentType.HOOK,),
            max_gap=1,
            minimum_duration=10.0,
            maximum_duration=5.0,
        )


def test_builder_rejects_invalid_maximum_candidates() -> None:
    with pytest.raises(ValueError, match="maximum_candidates"):
        StoryCandidateBuilder(maximum_candidates=0)


def test_default_story_patterns_are_sorted_by_priority() -> None:
    priorities = [pattern.priority for pattern in get_default_story_patterns()]

    assert priorities == sorted(priorities)


def test_build_returns_empty_list_for_empty_input() -> None:
    builder = StoryCandidateBuilder()

    assert builder.build([]) == []
