from __future__ import annotations
from dataclasses import dataclass, field
from statistics import variance
from domain.feature_vector import FeatureVector
from domain.candidate_score import CandidateScore
from application.scoring.decision_trace import DecisionTrace, DecisionStep

@dataclass(frozen=True, slots=True)
class EnsembleResult:
    total_score: float
    confidence: float
    bonuses: dict[str, float]
    penalties: dict[str, float]
    explanation: list[str]

class EnsembleScoringEngine:
    """Combines deterministic feature signals into an ensemble score."""

    def score(
        self,
        feature_vector: FeatureVector,
        candidate_score: CandidateScore,
        trace: DecisionTrace | None = None,
    ) -> EnsembleResult:
        bonuses = {}
        penalties = {}
        explanations = []

        # Rule A: Hook Strength + Curiosity Synergy
        if feature_vector.hook_strength >= 0.7 and feature_vector.curiosity >= 0.7:
            bonuses["Hook + Curiosity synergy"] = 2.0
            explanations.append("Hook + Curiosity synergy")

        # Rule B: Hook Quality + Ending Strength Synergy
        if feature_vector.hook_quality >= 0.7 and feature_vector.ending_strength >= 0.7:
            bonuses["Hook Quality + Ending Strength synergy"] = 3.0
            explanations.append("Hook Quality + Ending Strength synergy")

        # Rule E: Low Coverage Penalty
        if feature_vector.coverage < 0.4:
            penalties["Low Coverage penalty"] = 3.0
            explanations.append("Low Coverage penalty")

        total_score = min(100.0, max(0.0, candidate_score.total_score + sum(bonuses.values()) - sum(penalties.values())))
        
        # Confidence based on variance
        features = [
            feature_vector.hook_strength, feature_vector.curiosity, feature_vector.conflict,
            feature_vector.emotion, feature_vector.novelty, feature_vector.ending_strength,
            feature_vector.pacing, feature_vector.people, feature_vector.numbers,
            feature_vector.question, feature_vector.cta, feature_vector.duration,
            feature_vector.coverage, feature_vector.hook_quality
        ]
        
        # Simple deterministic confidence: lower variance -> higher confidence
        var = variance(features) if len(features) > 1 else 0.0
        confidence = max(0.0, min(100.0, 100.0 - (var * 100.0)))
        
        if trace:
            trace.add_step(DecisionStep(
                stage="Ensemble Scoring",
                input_summary={
                    "hook_strength": feature_vector.hook_strength,
                    "hook_quality": feature_vector.hook_quality,
                    "coverage": feature_vector.coverage,
                },
                output_summary={
                    "total_score": total_score,
                    "confidence": confidence,
                    "bonus_count": len(bonuses),
                    "penalty_count": len(penalties),
                },
                explanation=f"Applied {len(bonuses)} bonus(es) and {len(penalties)} penalty(ies)."
            ))
        
        return EnsembleResult(
            total_score=total_score,
            confidence=confidence,
            bonuses=bonuses,
            penalties=penalties,
            explanation=explanations
        )
