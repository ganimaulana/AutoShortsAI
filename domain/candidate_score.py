from __future__ import annotations

from dataclasses import dataclass

from domain.feature_vector import FeatureName


@dataclass(frozen=True, slots=True)
class CandidateScore:
    """Detailed deterministic score breakdown for one candidate."""

    total_score: float
    weighted_scores: dict[FeatureName, float]
    penalties: dict[str, float]
    bonuses: dict[str, float]
