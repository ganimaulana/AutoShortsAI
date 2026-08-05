from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FeatureName(str, Enum):
    HOOK_STRENGTH = "hook_strength"
    CURIOSITY = "curiosity"
    CONFLICT = "conflict"
    EMOTION = "emotion"
    NOVELTY = "novelty"
    ENDING_STRENGTH = "ending_strength"
    PACING = "pacing"
    PEOPLE = "people"
    NUMBERS = "numbers"
    QUESTION = "question"
    CTA = "cta"
    DURATION = "duration"
    COVERAGE = "coverage"


@dataclass(frozen=True, slots=True)
class FeatureVector:
    """Deterministic feature dimensions extracted from a story pattern match."""

    hook_strength: float
    curiosity: float
    conflict: float
    emotion: float
    novelty: float
    ending_strength: float
    pacing: float
    people: float
    numbers: float
    question: float
    cta: float
    duration: float
    coverage: float

    def get(self, feature: FeatureName) -> float:
        if not isinstance(feature, FeatureName):
            raise ValueError("feature must be a FeatureName.")

        return getattr(self, feature.value)
