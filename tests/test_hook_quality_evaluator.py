import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from application.story.hook_quality_evaluator import HookQualityEvaluator
from domain.story_intelligence import StorySegment, StorySegmentType

def test_hook_quality_evaluator_empty_segments():
    evaluator = HookQualityEvaluator()
    assert evaluator.evaluate([]) == 0.0

def test_hook_quality_evaluator_hook_segment():
    evaluator = HookQualityEvaluator()
    segment = StorySegment(
        id=1,
        primary_type=StorySegmentType.HOOK,
        types=[StorySegmentType.HOOK],
        start=0.0,
        end=5.0,
        text="Hook."
    )
    assert evaluator.evaluate([segment]) == 50.0

def test_hook_quality_evaluator_question_segment():
    evaluator = HookQualityEvaluator()
    segment = StorySegment(
        id=1,
        primary_type=StorySegmentType.QUESTION,
        types=[StorySegmentType.QUESTION],
        start=0.0,
        end=5.0,
        text="Question?"
    )
    assert evaluator.evaluate([segment]) == 30.0

def test_hook_quality_evaluator_conflict_segment():
    evaluator = HookQualityEvaluator()
    segment = StorySegment(
        id=1,
        primary_type=StorySegmentType.CONFLICT,
        types=[StorySegmentType.CONFLICT],
        start=0.0,
        end=5.0,
        text="Conflict!"
    )
    assert evaluator.evaluate([segment]) == 20.0

def test_hook_quality_evaluator_combined_score():
    evaluator = HookQualityEvaluator()
    segment = StorySegment(
        id=1,
        primary_type=StorySegmentType.HOOK,
        types=[StorySegmentType.HOOK, StorySegmentType.QUESTION, StorySegmentType.CONFLICT],
        start=0.0,
        end=5.0,
        text="Hook, Question, Conflict."
    )
    # HOOK=50, QUESTION=30, CONFLICT=20 => 100
    assert evaluator.evaluate([segment]) == 100.0

def test_hook_quality_evaluator_realistic_story_pattern_hook_question():
    evaluator = HookQualityEvaluator()
    # Pattern: Hook -> Question
    segment1 = StorySegment(id=1, primary_type=StorySegmentType.HOOK, types=[StorySegmentType.HOOK], start=0.0, end=5.0, text="Hook")
    segment2 = StorySegment(id=2, primary_type=StorySegmentType.QUESTION, types=[StorySegmentType.QUESTION], start=5.0, end=10.0, text="Question")
    
    # Evaluate only first segment as per implementation
    assert evaluator.evaluate([segment1, segment2]) == 50.0

def test_hook_quality_evaluator_realistic_story_pattern_conflict():
    evaluator = HookQualityEvaluator()
    # Pattern: Conflict -> Solution
    segment1 = StorySegment(id=1, primary_type=StorySegmentType.CONFLICT, types=[StorySegmentType.CONFLICT], start=0.0, end=5.0, text="Conflict")
    segment2 = StorySegment(id=2, primary_type=StorySegmentType.SOLUTION, types=[StorySegmentType.SOLUTION], start=5.0, end=10.0, text="Solution")
    
    assert evaluator.evaluate([segment1, segment2]) == 20.0
