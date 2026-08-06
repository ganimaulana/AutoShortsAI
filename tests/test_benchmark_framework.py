import sys
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from application.benchmark.loader import BenchmarkLoader
from application.benchmark.runner import BenchmarkRunner
from application.benchmark.report import BenchmarkReporter
from pipeline.story_pipeline import StoryPipeline
from domain.scoring_profile import ScoringProfile

def test_benchmark_framework_execution():
    # Setup mocks
    pipeline = MagicMock(spec=StoryPipeline)
    runner = BenchmarkRunner(pipeline)
    
    # Fixtures
    fixture_dir = ROOT / "tests" / "benchmark" / "fixtures"
    transcript_path = fixture_dir / "transcript_01.json"
    expected_path = fixture_dir / "expected_01.json"
    
    segments = BenchmarkLoader.load_transcript(transcript_path)
    expected_candidates = BenchmarkLoader.load_expected_candidates(expected_path)
    
    # Mock pipeline return - RankedCandidates
    from domain.ranked_candidate import RankedCandidate
    from domain.candidate import Candidate
    from domain.candidate_score import CandidateScore
    
    ranked = RankedCandidate(
        candidate=Candidate(start=0.0, end=15.0, score=0.0, reason="test"),
        score=CandidateScore(total_score=10.0, weighted_scores={}, penalties={}, bonuses={}),
        rank=1, input_index=0, tie_break_values={}
    )
    pipeline.build_ranked_candidates.return_value = [ranked]
    
    # Run benchmark
    result = runner.run(segments, expected_candidates, MagicMock(spec=ScoringProfile))
    
    # Verify
    assert result.precision_at_k == 1.0
    assert result.recall_at_k == 1.0
    
    # Report
    report = BenchmarkReporter.report("Test Case 1", result)
    assert "Precision@K: 1.00" in report
    assert "Recall@K: 1.00" in report
