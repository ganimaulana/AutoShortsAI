import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from application.candidate.story_candidate_builder import StoryPatternMatch
from application.candidate.story_patterns import StoryPattern
from application.feature.feature_extractor import FeatureExtractor
from domain.story_intelligence import StorySegment, StorySegmentType


def make_segment(
    segment_id: int,
    primary_type: StorySegmentType,
    start: float,
    end: float,
    text: str,
    types: list[StorySegmentType] | None = None,
) -> StorySegment:
    return StorySegment(
        id=segment_id,
        primary_type=primary_type,
        types=types or [primary_type],
        start=start,
        end=end,
        text=text,
    )


def make_match(*segments: StorySegment) -> StoryPatternMatch:
    sequence = tuple(segment.primary_type for segment in segments)
    if not sequence:
        sequence = (StorySegmentType.UNKNOWN,)

    return StoryPatternMatch(
        pattern=StoryPattern(
            name="Test Pattern",
            priority=1,
            sequence=sequence,
            max_gap=1,
            minimum_duration=1.0,
            maximum_duration=120.0,
        ),
        matched_segments=segments,
    )


def extract(*segments: StorySegment):
    return FeatureExtractor().extract(make_match(*segments))


def test_extract_returns_normalized_hook_strength_from_multiple_signals() -> None:
    vector = extract(
        make_segment(
            1,
            StorySegmentType.HOOK,
            0.0,
            4.0,
            "Did you know the hidden reason 500 teams failed?",
        )
    )

    assert 0.9 <= vector.hook_strength <= 1.0


def test_extract_curiosity_increases_with_multiple_open_loop_signals() -> None:
    single_signal = extract(
        make_segment(1, StorySegmentType.CONTEXT, 0.0, 4.0, "The hidden detail matters.")
    )
    multi_signal = extract(
        make_segment(
            1,
            StorySegmentType.CONTEXT,
            0.0,
            4.0,
            "The hidden detail matters because before the launch...",
        )
    )

    assert multi_signal.curiosity > single_signal.curiosity
    assert 0.0 < single_signal.curiosity < 1.0


def test_extract_conflict_combines_text_and_segment_type_signals() -> None:
    vector = extract(
        make_segment(
            1,
            StorySegmentType.CONFLICT,
            0.0,
            4.0,
            "But the launch went wrong after the team was blocked.",
        )
    )

    assert vector.conflict > 0.7


def test_extract_emotion_combines_keywords_intensity_and_exclamation() -> None:
    vector = extract(
        make_segment(
            1,
            StorySegmentType.RESULT,
            0.0,
            4.0,
            "The team was extremely shocked and happy!",
        )
    )

    assert vector.emotion > 0.7


def test_extract_novelty_combines_novelty_and_surprising_number() -> None:
    vector = extract(
        make_segment(
            1,
            StorySegmentType.FACT,
            0.0,
            4.0,
            "For the first time, 1000 people saw the new result.",
        )
    )

    assert vector.novelty > 0.6


def test_extract_ending_strength_combines_ending_and_result_signals() -> None:
    vector = extract(
        make_segment(
            1,
            StorySegmentType.ENDING,
            0.0,
            4.0,
            "In the end, the lesson worked.",
        )
    )

    assert vector.ending_strength > 0.8


def test_extract_ending_strength_applies_cta_penalty_without_closing_phrase() -> None:
    cta_result = extract(
        make_segment(
            1,
            StorySegmentType.RESULT,
            0.0,
            4.0,
            "The result worked, subscribe and follow.",
        )
    )
    plain_result = extract(
        make_segment(
            1,
            StorySegmentType.RESULT,
            0.0,
            4.0,
            "The result worked.",
        )
    )

    assert cta_result.ending_strength < plain_result.ending_strength


def test_extract_normalizes_pacing() -> None:
    ideal = extract(
        make_segment(1, StorySegmentType.FACT, 0.0, 2.0, "one two three four five")
    )
    slow = extract(
        make_segment(1, StorySegmentType.FACT, 0.0, 10.0, "one two")
    )
    fast = extract(
        make_segment(
            1,
            StorySegmentType.FACT,
            0.0,
            1.0,
            "one two three four five six seven",
        )
    )

    assert ideal.pacing == 1.0
    assert slow.pacing < ideal.pacing
    assert fast.pacing < ideal.pacing


def test_extract_detects_people_numbers_question_and_cta_as_normalized_values() -> None:
    vector = extract(
        make_segment(
            1,
            StorySegmentType.HOOK,
            0.0,
            4.0,
            "Why did Jane Smith tell 300 people to follow?",
        )
    )

    assert 0.0 < vector.people <= 1.0
    assert 0.0 < vector.numbers <= 1.0
    assert 0.0 < vector.question <= 1.0
    assert 0.0 < vector.cta <= 1.0


def test_extract_calculates_duration_from_match_window() -> None:
    vector = extract(
        make_segment(1, StorySegmentType.HOOK, 3.5, 5.0, "Hook."),
        make_segment(2, StorySegmentType.RESULT, 7.0, 9.0, "Result."),
    )

    assert vector.duration == 5.5


def test_extract_calculates_coverage_ratio_for_gapped_segments() -> None:
    vector = extract(
        make_segment(1, StorySegmentType.HOOK, 0.0, 2.0, "Hook."),
        make_segment(2, StorySegmentType.RESULT, 6.0, 8.0, "Result."),
    )

    assert vector.coverage == pytest.approx(0.5)


def test_extract_returns_zero_for_empty_match() -> None:
    vector = FeatureExtractor().extract(make_match())

    assert vector.hook_strength == 0.0
    assert vector.curiosity == 0.0
    assert vector.conflict == 0.0
    assert vector.emotion == 0.0
    assert vector.novelty == 0.0
    assert vector.ending_strength == 0.0
    assert vector.pacing == 0.0
    assert vector.people == 0.0
    assert vector.numbers == 0.0
    assert vector.question == 0.0
    assert vector.cta == 0.0
    assert vector.duration == 0.0
    assert vector.coverage == 0.0
