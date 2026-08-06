import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from application.evaluation.evaluation_engine import EvaluationEngine
from application.evaluation.human_feedback import HumanFeedback, HumanFeedbackDataset
from domain.ranked_candidate import RankedCandidate
from domain.candidate import Candidate
from domain.candidate_score import CandidateScore

def create_ranked_candidate(start: float, end: float) -> RankedCandidate:
    return RankedCandidate(
        candidate=Candidate(start=start, end=end, score=0.0, reason="test"),
        score=CandidateScore(total_score=10.0, weighted_scores={}, penalties={}, bonuses={}),
        rank=1, input_index=0, tie_break_values={}
    )

def test_perfect_match():
    engine = EvaluationEngine()
    dataset = HumanFeedbackDataset()
    dataset.add(HumanFeedback(0.0, 10.0, 5, True, "Match"))
    
    candidates = [create_ranked_candidate(0.0, 10.0)]
    result = engine.evaluate(candidates, dataset)
    
    assert result.matched_candidates == 1
    assert result.average_rating == 5.0
    assert result.selection_accuracy == 1.0

def test_no_match():
    engine = EvaluationEngine()
    dataset = HumanFeedbackDataset()
    dataset.add(HumanFeedback(0.0, 10.0, 5, True, "No match"))
    
    candidates = [create_ranked_candidate(20.0, 30.0)]
    result = engine.evaluate(candidates, dataset)
    
    assert result.matched_candidates == 0
    assert result.average_rating == 0.0
    assert result.selection_accuracy == 0.0

def test_partial_match():
    engine = EvaluationEngine()
    dataset = HumanFeedbackDataset()
    dataset.add(HumanFeedback(0.0, 10.0, 4, True, "Partial"))
    
    # Partial match: [0.0, 10.0] vs [5.0, 15.0]. IoU = 5/15 = 0.33 < 0.5 (Default threshold)
    candidates = [create_ranked_candidate(5.0, 15.0)]
    result = engine.evaluate(candidates, dataset, iou_threshold=0.3) # Set low to test partial match
    
    assert result.matched_candidates == 1
    assert result.average_rating == 4.0

def test_determinism():
    engine = EvaluationEngine()
    dataset = HumanFeedbackDataset()
    dataset.add(HumanFeedback(0.0, 10.0, 5, True, "Match"))
    candidates = [create_ranked_candidate(0.0, 10.0)]
    
    result1 = engine.evaluate(candidates, dataset)
    result2 = engine.evaluate(candidates, dataset)
    assert result1 == result2
