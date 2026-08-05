import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from application.story.sentence_feature_extractor import SentenceFeatureExtractor
from application.story.sentence_splitter import SentenceSplitter
from application.story.story_analyzer import StoryAnalyzer
from domain.segment import Segment
from domain.story_intelligence import StorySegmentType


def test_sentence_splitter_splits_by_punctuation_and_preserves_segment_ids():
    segments = [
        Segment(id=1, start=0.0, end=2.0, text="Did you know this?"),
        Segment(id=2, start=2.1, end=4.0, text="It changed everything."),
    ]

    sentences = SentenceSplitter().split(segments)

    assert [sentence.text for sentence in sentences] == [
        "Did you know this?",
        "It changed everything.",
    ]
    assert sentences[0].segment_ids == [1]
    assert sentences[1].segment_ids == [2]
    assert sentences[0].duration == 2.0


def test_sentence_splitter_handles_multiple_sentences_in_one_segment():
    segments = [
        Segment(
            id=1,
            start=0.0,
            end=5.0,
            text="First problem happened. Then they fixed it!",
        )
    ]

    sentences = SentenceSplitter().split(segments)

    assert [sentence.text for sentence in sentences] == [
        "First problem happened.",
        "Then they fixed it!",
    ]
    assert [sentence.segment_ids for sentence in sentences] == [[1], [1]]


def test_sentence_splitter_uses_silence_gap_fallback():
    segments = [
        Segment(id=1, start=0.0, end=1.0, text="This has no punctuation"),
        Segment(id=2, start=3.0, end=4.0, text="But the gap creates a boundary"),
    ]

    sentences = SentenceSplitter().split(segments)

    assert [sentence.segment_ids for sentence in sentences] == [[1], [2]]


def test_feature_extractor_detects_question_fact_and_hook_tags():
    sentences = SentenceSplitter().split(
        [
            Segment(
                id=1,
                start=0.0,
                end=2.0,
                text="Did you know 50 percent of teams fail?",
            )
        ]
    )

    features = SentenceFeatureExtractor().extract(sentences)

    assert StorySegmentType.QUESTION in features[0].matched_types
    assert StorySegmentType.FACT in features[0].matched_types
    assert StorySegmentType.HOOK in features[0].matched_types
    assert features[0].duration == 2.0


def test_story_analyzer_applies_priority_and_groups_adjacent_segments():
    sentences = SentenceSplitter().split(
        [
            Segment(id=1, start=0.0, end=1.0, text="Did you know this problem?"),
            Segment(id=2, start=1.0, end=2.0, text="This problem became difficult."),
            Segment(id=3, start=2.0, end=3.0, text="The issue created risk."),
            Segment(id=4, start=3.0, end=4.0, text="Then they found the solution."),
        ]
    )
    features = SentenceFeatureExtractor().extract(sentences)

    story_segments = StoryAnalyzer().analyze(features)

    assert story_segments[0].primary_type == StorySegmentType.HOOK
    assert story_segments[1].primary_type == StorySegmentType.PROBLEM
    assert story_segments[1].sentence_ids == [2, 3]
    assert story_segments[2].primary_type == StorySegmentType.BUILD_UP
    assert StorySegmentType.SOLUTION in story_segments[2].types
    assert story_segments[1].duration == 2.0


def test_story_analyzer_uses_unknown_fallback():
    sentences = SentenceSplitter().split(
        [
            Segment(id=1, start=0.0, end=1.0, text="Plain neutral sentence."),
        ]
    )
    features = SentenceFeatureExtractor().extract(sentences)

    story_segments = StoryAnalyzer().analyze(features)

    assert story_segments[0].primary_type == StorySegmentType.UNKNOWN
    assert story_segments[0].types == [StorySegmentType.UNKNOWN]
