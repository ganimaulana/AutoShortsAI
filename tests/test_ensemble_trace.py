import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from application.scoring.ensemble_engine import EnsembleScoringEngine
from application.scoring.decision_trace import DecisionTrace
from domain.feature_vector import FeatureVector
from domain.candidate_score import CandidateScore

def test_ensemble_engine_trace():
    engine = EnsembleScoringEngine()
    fv = FeatureVector(
        hook_strength=0.8, curiosity=0.8, conflict=0.1, emotion=0.1, novelty=0.1,
        ending_strength=0.1, pacing=0.1, people=0.1, numbers=0.1, question=0.1,
        cta=0.1, duration=0.1, coverage=0.5, hook_quality=0.1
    )
    cs = CandidateScore(total_score=50.0, weighted_scores={}, penalties={}, bonuses={})
    trace = DecisionTrace()
    
    # Test with trace
    result1 = engine.score(fv, cs, trace=trace)
    
    assert len(trace.steps) == 1
    assert trace.steps[0].stage == "Ensemble Scoring"
    assert "Applied 1 bonus(es) and 0 penalty(ies)." in trace.steps[0].explanation
    assert trace.steps[0].output_summary["total_score"] == result1.total_score
    
    # Test without trace (should be identical to without)
    result2 = engine.score(fv, cs, trace=None)
    assert result1 == result2

def test_ensemble_engine_determinism_with_trace():
    engine = EnsembleScoringEngine()
    fv = FeatureVector(
        hook_strength=0.5, curiosity=0.5, conflict=0.5, emotion=0.5, novelty=0.5,
        ending_strength=0.5, pacing=0.5, people=0.5, numbers=0.5, question=0.5,
        cta=0.5, duration=0.5, coverage=0.5, hook_quality=0.5
    )
    cs = CandidateScore(total_score=50.0, weighted_scores={}, penalties={}, bonuses={})
    trace1 = DecisionTrace()
    trace2 = DecisionTrace()
    
    result1 = engine.score(fv, cs, trace=trace1)
    result2 = engine.score(fv, cs, trace=trace2)
    
    assert result1 == result2
    assert trace1.to_dict() == trace2.to_dict()
