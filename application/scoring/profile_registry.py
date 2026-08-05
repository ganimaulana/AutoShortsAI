from __future__ import annotations

from domain.feature_vector import FeatureName
from domain.scoring_profile import (
    BonusRule,
    PenaltyRule,
    RuleCondition,
    RuleOperator,
    ScoringProfile,
)


def _weights(values: dict[FeatureName, float]) -> dict[FeatureName, float]:
    return dict(values)


DEFAULT_PROFILES: tuple[ScoringProfile, ...] = (
    ScoringProfile(
        name="Educational",
        weights=_weights(
            {
                FeatureName.HOOK_STRENGTH: 0.12,
                FeatureName.CURIOSITY: 0.12,
                FeatureName.CONFLICT: 0.06,
                FeatureName.EMOTION: 0.05,
                FeatureName.NOVELTY: 0.09,
                FeatureName.ENDING_STRENGTH: 0.10,
                FeatureName.PACING: 0.08,
                FeatureName.PEOPLE: 0.06,
                FeatureName.NUMBERS: 0.14,
                FeatureName.QUESTION: 0.08,
                FeatureName.CTA: 0.02,
                FeatureName.DURATION: 0.03,
                FeatureName.COVERAGE: 0.05,
            }
        ),
        bonus_rules=(
            BonusRule(
                name="high_curiosity",
                conditions=(RuleCondition(FeatureName.CURIOSITY, RuleOperator.GTE, 0.8),),
                points=3.0,
            ),
            BonusRule(
                name="strong_evidence",
                conditions=(RuleCondition(FeatureName.NUMBERS, RuleOperator.GTE, 0.7),),
                points=3.0,
            ),
        ),
        penalty_rules=(
            PenaltyRule(
                name="low_coverage",
                conditions=(RuleCondition(FeatureName.COVERAGE, RuleOperator.LT, 0.5),),
                points=8.0,
            ),
            PenaltyRule(
                name="duration_outside_preferred_range",
                conditions=(
                    RuleCondition(FeatureName.DURATION, RuleOperator.BETWEEN, (0.0, 7.999)),
                ),
                points=6.0,
            ),
        ),
    ),
    ScoringProfile(
        name="Storytelling",
        weights=_weights(
            {
                FeatureName.HOOK_STRENGTH: 0.14,
                FeatureName.CURIOSITY: 0.10,
                FeatureName.CONFLICT: 0.13,
                FeatureName.EMOTION: 0.14,
                FeatureName.NOVELTY: 0.06,
                FeatureName.ENDING_STRENGTH: 0.13,
                FeatureName.PACING: 0.07,
                FeatureName.PEOPLE: 0.08,
                FeatureName.NUMBERS: 0.03,
                FeatureName.QUESTION: 0.05,
                FeatureName.CTA: 0.01,
                FeatureName.DURATION: 0.03,
                FeatureName.COVERAGE: 0.03,
            }
        ),
        bonus_rules=(
            BonusRule(
                name="hook_curiosity_synergy",
                conditions=(
                    RuleCondition(FeatureName.HOOK_STRENGTH, RuleOperator.GTE, 0.7),
                    RuleCondition(FeatureName.CURIOSITY, RuleOperator.GTE, 0.7),
                ),
                points=5.0,
            ),
            BonusRule(
                name="strong_ending",
                conditions=(RuleCondition(FeatureName.ENDING_STRENGTH, RuleOperator.GTE, 0.8),),
                points=3.0,
            ),
        ),
        penalty_rules=(
            PenaltyRule(
                name="weak_ending",
                conditions=(RuleCondition(FeatureName.ENDING_STRENGTH, RuleOperator.LT, 0.2),),
                points=5.0,
            ),
        ),
    ),
    ScoringProfile(
        name="Podcast",
        weights=_weights(
            {
                FeatureName.HOOK_STRENGTH: 0.09,
                FeatureName.CURIOSITY: 0.10,
                FeatureName.CONFLICT: 0.07,
                FeatureName.EMOTION: 0.12,
                FeatureName.NOVELTY: 0.05,
                FeatureName.ENDING_STRENGTH: 0.08,
                FeatureName.PACING: 0.12,
                FeatureName.PEOPLE: 0.14,
                FeatureName.NUMBERS: 0.04,
                FeatureName.QUESTION: 0.10,
                FeatureName.CTA: 0.02,
                FeatureName.DURATION: 0.03,
                FeatureName.COVERAGE: 0.04,
            }
        ),
        bonus_rules=(
            BonusRule(
                name="strong_conversation",
                conditions=(
                    RuleCondition(FeatureName.PEOPLE, RuleOperator.GTE, 0.7),
                    RuleCondition(FeatureName.QUESTION, RuleOperator.GTE, 0.5),
                ),
                points=4.0,
            ),
        ),
        penalty_rules=(
            PenaltyRule(
                name="extremely_low_pacing",
                conditions=(RuleCondition(FeatureName.PACING, RuleOperator.LT, 0.2),),
                points=6.0,
            ),
        ),
    ),
    ScoringProfile(
        name="News",
        weights=_weights(
            {
                FeatureName.HOOK_STRENGTH: 0.10,
                FeatureName.CURIOSITY: 0.08,
                FeatureName.CONFLICT: 0.12,
                FeatureName.EMOTION: 0.08,
                FeatureName.NOVELTY: 0.14,
                FeatureName.ENDING_STRENGTH: 0.07,
                FeatureName.PACING: 0.07,
                FeatureName.PEOPLE: 0.10,
                FeatureName.NUMBERS: 0.14,
                FeatureName.QUESTION: 0.04,
                FeatureName.CTA: 0.01,
                FeatureName.DURATION: 0.02,
                FeatureName.COVERAGE: 0.03,
            }
        ),
        bonus_rules=(
            BonusRule(
                name="high_novelty",
                conditions=(RuleCondition(FeatureName.NOVELTY, RuleOperator.GTE, 0.8),),
                points=4.0,
            ),
            BonusRule(
                name="high_coverage",
                conditions=(RuleCondition(FeatureName.COVERAGE, RuleOperator.GTE, 0.9),),
                points=3.0,
            ),
        ),
        penalty_rules=(
            PenaltyRule(
                name="low_coverage",
                conditions=(RuleCondition(FeatureName.COVERAGE, RuleOperator.LT, 0.5),),
                points=8.0,
            ),
        ),
    ),
)


class ProfileRegistry:
    """Registry for deterministic scoring profiles."""

    def __init__(self, profiles: tuple[ScoringProfile, ...] | None = None) -> None:
        configured_profiles = profiles if profiles is not None else DEFAULT_PROFILES
        self._profiles = self._build_profile_map(configured_profiles)

    def get_profile(self, name: str) -> ScoringProfile:
        try:
            return self._profiles[name]
        except KeyError as error:
            raise KeyError(f"Unknown scoring profile: {name}") from error

    def list_profiles(self) -> tuple[str, ...]:
        return tuple(self._profiles)

    @staticmethod
    def _build_profile_map(
        profiles: tuple[ScoringProfile, ...],
    ) -> dict[str, ScoringProfile]:
        profile_map: dict[str, ScoringProfile] = {}

        for profile in profiles:
            if profile.name in profile_map:
                raise ValueError(f"Duplicate scoring profile name: {profile.name}")

            profile_map[profile.name] = profile

        return profile_map
