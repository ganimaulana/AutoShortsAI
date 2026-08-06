import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.story_pipeline import StoryPipeline
from domain.segment import Segment
from domain.scoring_profile import ScoringProfile
from domain.ranked_candidate import RankedCandidate
from domain.candidate import Candidate
from domain.candidate_score import CandidateScore

def test_story_pipeline_logging_does_not_affect_output():
    # Setup mocks
    splitter = MagicMock()
    extractor = MagicMock()
    analyzer = MagicMock()
    builder = MagicMock()
    feature_extractor = MagicMock()
    scorer = MagicMock()
    ranking_engine = MagicMock()
    diversity_filter = MagicMock()

    pipeline = StoryPipeline(
        splitter, extractor, analyzer, builder, feature_extractor, scorer, ranking_engine, diversity_filter
    )
    
    # Mock data
    segments = [Segment(id=1, start=0.0, end=10.0, text="test")]
    profile = MagicMock(spec=ScoringProfile)
    ranked = RankedCandidate(
        candidate=Candidate(start=0.0, end=10.0, score=0.0, reason="test"),
        score=CandidateScore(total_score=10.0, weighted_scores={}, penalties={}, bonuses={}),
        rank=1, input_index=0, tie_break_values={}
    )
    
    # Setup workflow returns
    splitter.split.return_value = []
    extractor.extract.return_value = []
    analyzer.analyze.return_value = []
    builder.build_matches.return_value = []
    ranking_engine.rank.return_value = []
    diversity_filter.filter.return_value = [ranked]

    # Run without logging
    result1 = pipeline.build_ranked_candidates(segments, profile, enable_logging=False)
    
    # Run with logging
    with patch.object(pipeline.logger, 'info') as mock_info:
        result2 = pipeline.build_ranked_candidates(segments, profile, enable_logging=True)
        assert mock_info.called
    
    assert result1 == result2
    
    # Run with logging disabled explicitly
    with patch.object(pipeline.logger, 'info') as mock_info:
        result3 = pipeline.build_ranked_candidates(segments, profile, enable_logging=False)
        assert not mock_info.called
        assert result3 == result1
