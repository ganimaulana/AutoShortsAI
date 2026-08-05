import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from unittest.mock import MagicMock
from pipeline.candidate_pipeline import CandidatePipeline
from domain.job.job import Job
from domain.segment import Segment
from domain.ranked_candidate import RankedCandidate
from domain.candidate import Candidate
from domain.candidate_score import CandidateScore
from application.ranking.diversity_rules import DiversityRules

def test_candidate_pipeline_uses_legacy_builder_by_default() -> None:
    job = MagicMock(spec=Job)
    job.manifest.transcript_segments = [Segment(id=1, start=0.0, end=10.0, text="test")]
    job.metadata = {"USE_STORY_PIPELINE": False}
    
    legacy_builder = MagicMock()
    legacy_builder.build.return_value = []
    
    pipeline = CandidatePipeline(legacy_builder=legacy_builder)
    pipeline.execute(job)
    
    legacy_builder.build.assert_called_once()

def test_candidate_pipeline_falls_back_on_story_pipeline_failure() -> None:
    job = MagicMock(spec=Job)
    job.manifest.transcript_segments = [Segment(id=1, start=0.0, end=10.0, text="test")]
    job.metadata = {"USE_STORY_PIPELINE": True, "STRICT_STORY_PIPELINE": False}
    
    story_pipeline = MagicMock()
    story_pipeline.build_ranked_candidates.side_effect = Exception("Pipeline error")
    
    legacy_builder = MagicMock()
    legacy_builder.build.return_value = []
    
    pipeline = CandidatePipeline(legacy_builder=legacy_builder, story_pipeline=story_pipeline)
    pipeline.execute(job)
    
    legacy_builder.build.assert_called_once()
    assert story_pipeline.build_ranked_candidates.called

def test_candidate_pipeline_strict_mode_raises_on_failure() -> None:
    job = MagicMock(spec=Job)
    job.metadata = {"USE_STORY_PIPELINE": True, "STRICT_STORY_PIPELINE": True}
    
    story_pipeline = MagicMock()
    story_pipeline.build_ranked_candidates.side_effect = Exception("Pipeline error")
    
    pipeline = CandidatePipeline(story_pipeline=story_pipeline)
    
    with pytest.raises(Exception, match="Pipeline error"):
        pipeline.execute(job)

def test_candidate_pipeline_story_pipeline_integration() -> None:
    job = MagicMock(spec=Job)
    job.manifest.transcript_segments = [Segment(id=1, start=0.0, end=10.0, text="test")]
    job.metadata = {"USE_STORY_PIPELINE": True}
    
    candidate = Candidate(start=0.0, end=10.0, score=0.0, reason="test reason")
    ranked = RankedCandidate(
        candidate=candidate, 
        score=CandidateScore(total_score=10.0, weighted_scores={}, penalties={}, bonuses={}), 
        rank=1, 
        input_index=0, 
        tie_break_values={}
    )
    
    story_pipeline = MagicMock()
    story_pipeline.build_ranked_candidates.return_value = [ranked]
    
    pipeline = CandidatePipeline(story_pipeline=story_pipeline)
    pipeline.execute(job)
    
    assert job.metadata["approved_candidates"][0]["title"] == "test reason"
    assert job.metadata["approved_candidates"][0]["score"] == 10

def test_candidate_pipeline_preserves_order_and_reasons() -> None:
    job = MagicMock(spec=Job)
    job.manifest.transcript_segments = [Segment(id=1, start=0.0, end=10.0, text="test")]
    job.metadata = {"USE_STORY_PIPELINE": True}
    
    c1 = Candidate(start=0.0, end=5.0, score=0.0, reason="reason 1")
    c2 = Candidate(start=5.0, end=10.0, score=0.0, reason="reason 2")
    
    ranked1 = RankedCandidate(candidate=c1, score=CandidateScore(total_score=20.0, weighted_scores={}, penalties={}, bonuses={}), rank=1, input_index=0, tie_break_values={})
    ranked2 = RankedCandidate(candidate=c2, score=CandidateScore(total_score=10.0, weighted_scores={}, penalties={}, bonuses={}), rank=2, input_index=1, tie_break_values={})
    
    story_pipeline = MagicMock()
    story_pipeline.build_ranked_candidates.return_value = [ranked1, ranked2]
    
    pipeline = CandidatePipeline(story_pipeline=story_pipeline)
    pipeline.execute(job)
    
    assert job.metadata["approved_candidates"][0]["title"] == "reason 1"
    assert job.metadata["approved_candidates"][1]["title"] == "reason 2"
    assert job.metadata["approved_candidates"][0]["score"] == 20
    assert job.metadata["approved_candidates"][1]["score"] == 10
