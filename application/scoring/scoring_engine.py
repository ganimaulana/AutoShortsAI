from __future__ import annotations

import logging

from domain.candidate_score import CandidateScore
from domain.feature_vector import FeatureVector
from domain.scoring_profile import RuleCondition, RuleOperator, ScoringProfile

logger = logging.getLogger(__name__)


class ScoringEngine:
    """Calculates deterministic scores from profile-defined scoring behavior."""

    def score(
        self,
        feature_vector: FeatureVector,
        profile: ScoringProfile,
    ) -> CandidateScore:
        weighted_scores = self._calculate_weighted_scores(feature_vector, profile)
        bonuses = self._evaluate_bonus_rules(feature_vector, profile)
        penalties = self._evaluate_penalty_rules(feature_vector, profile)

        base_points = sum(weighted_scores.values()) * 100.0
        total_score = self._clamp(
            base_points + sum(bonuses.values()) - sum(penalties.values())
        )

        logger.debug(
            "Calculated candidate score: base_points=%.3f bonuses=%.3f penalties=%.3f total=%.3f",
            base_points,
            sum(bonuses.values()),
            sum(penalties.values()),
            total_score,
        )

        return CandidateScore(
            total_score=total_score,
            weighted_scores=weighted_scores,
            penalties=penalties,
            bonuses=bonuses,
        )

    @staticmethod
    def _calculate_weighted_scores(
        feature_vector: FeatureVector,
        profile: ScoringProfile,
    ) -> dict:
        return {
            feature: feature_vector.get(feature) * weight
            for feature, weight in profile.weights.items()
        }

    def _evaluate_bonus_rules(
        self,
        feature_vector: FeatureVector,
        profile: ScoringProfile,
    ) -> dict[str, float]:
        return {
            rule.name: rule.points
            for rule in profile.bonus_rules
            if self._matches_all_conditions(feature_vector, rule.conditions)
        }

    def _evaluate_penalty_rules(
        self,
        feature_vector: FeatureVector,
        profile: ScoringProfile,
    ) -> dict[str, float]:
        return {
            rule.name: rule.points
            for rule in profile.penalty_rules
            if self._matches_all_conditions(feature_vector, rule.conditions)
        }

    def _matches_all_conditions(
        self,
        feature_vector: FeatureVector,
        conditions: tuple[RuleCondition, ...],
    ) -> bool:
        return all(
            self._matches_condition(feature_vector, condition)
            for condition in conditions
        )

    def _matches_condition(
        self,
        feature_vector: FeatureVector,
        condition: RuleCondition,
    ) -> bool:
        actual = feature_vector.get(condition.feature)
        expected = condition.value

        if condition.operator == RuleOperator.GT:
            return actual > self._numeric_value(expected, condition.operator)
        if condition.operator == RuleOperator.GTE:
            return actual >= self._numeric_value(expected, condition.operator)
        if condition.operator == RuleOperator.LT:
            return actual < self._numeric_value(expected, condition.operator)
        if condition.operator == RuleOperator.LTE:
            return actual <= self._numeric_value(expected, condition.operator)
        if condition.operator == RuleOperator.EQ:
            return actual == self._numeric_value(expected, condition.operator)
        if condition.operator == RuleOperator.NEQ:
            return actual != self._numeric_value(expected, condition.operator)
        if condition.operator == RuleOperator.BETWEEN:
            lower, upper = self._range_value(expected, condition.operator)
            return lower <= actual <= upper

        raise ValueError(f"Unsupported rule operator: {condition.operator}")

    @staticmethod
    def _numeric_value(
        value: float | tuple[float, float],
        operator: RuleOperator,
    ) -> float:
        if isinstance(value, tuple):
            raise ValueError(f"Operator {operator.value} requires a numeric value.")

        return value

    @staticmethod
    def _range_value(
        value: float | tuple[float, float],
        operator: RuleOperator,
    ) -> tuple[float, float]:
        if not isinstance(value, tuple) or len(value) != 2:
            raise ValueError(f"Operator {operator.value} requires a two-item range.")

        return value

    @staticmethod
    def _clamp(value: float) -> float:
        return min(100.0, max(0.0, value))
