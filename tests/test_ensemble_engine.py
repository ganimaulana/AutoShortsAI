import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from application.scoring.ensemble_engine import EnsembleScoringEngine
from domain.feature_vector import FeatureVector
from domain.candidate_score import CandidateScore

def test_ensemble_engine_rules():
    engine = EnsembleScoringEngine()
    
    # Base feature vector (no bonuses/penalties)
    fv = FeatureVector(
        hook_strength=0.1, curiosity=0.1, conflict=0.1, emotion=0.1, novelty=0.1,
        ending_strength=0.1, pacing=0.1, people=0.1, numbers=0.1, question=0.1,
        cta=0.1, duration=0.1, coverage=0.5, hook_quality=0.1
    )
    cs = CandidateScore(total_score=50.0, weighted_scores={}, penalties={}, bonuses={})
    
    # 1. Test Synergy Rules (A+B)
    fv_synergy = FeatureVector(
        hook_strength=0.8, curiosity=0.8, conflict=0.1, emotion=0.1, novelty=0.1,
        ending_strength=0.8, pacing=0.1, people=0.1, numbers=0.1, question=0.1,
        cta=0.1, duration=0.1, coverage=0.5, hook_quality=0.8
    )
    result = engine.score(fv_synergy, cs)
    assert result.total_score == 55.0 # 50 + 2 (A) + 3 (B)
    assert "Hook + Curiosity synergy" in result.bonuses
    assert "Hook Quality + Ending Strength synergy" in result.bonuses
    
    # 2. Test Penalty Rule (E)
    fv_penalty = FeatureVector(
        hook_strength=0.1, curiosity=0.1, conflict=0.1, emotion=0.1, novelty=0.1,
        ending_strength=0.1, pacing=0.1, people=0.1, numbers=0.1, question=0.1,
        cta=0.1, duration=0.1, coverage=0.2, hook_quality=0.1
    )
    result = engine.score(fv_penalty, cs)
    assert result.total_score == 47.0 # 50 - 3 (E)
    assert "Low Coverage penalty" in result.penalties
    
    # 3. Test Confidence
    result_low_var = engine.score(fv, cs)
    result_high_var = engine.score(fv_synergy, cs)
    assert result_low_var.confidence > result_high_var.confidence
    assert 0.0 <= result_low_var.confidence <= 100.0

def test_ensemble_engine_determinism():
    engine = EnsembleScoringEngine()
    fv = FeatureVector(
        hook_strength=0.5, curiosity=0.5, conflict=0.5, emotion=0.5, novelty=0.5,
        ending_strength=0.5, pacing=0.5, people=0.5, numbers=0.5, question=0.5,
        cta=0.5, duration=0.5, coverage=0.5, hook_quality=0.5
    )
    cs = CandidateScore(total_score=50.0, weighted_scores={}, penalties={}, bonuses={})
    
    result1 = engine.score(fv, cs)
    result2 = engine.score(fv, cs)
    assert result1 == result2
