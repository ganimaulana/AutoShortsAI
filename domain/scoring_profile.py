from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from domain.feature_vector import FeatureName

WEIGHT_SUM_TOLERANCE = 0.000001


class RuleOperator(str, Enum):
    GT = "gt"
    GTE = "gte"
    LT = "lt"
    LTE = "lte"
    EQ = "eq"
    NEQ = "neq"
    BETWEEN = "between"


@dataclass(frozen=True, slots=True)
class RuleCondition:
    feature: FeatureName
    operator: RuleOperator
    value: float | tuple[float, float]

    def __post_init__(self) -> None:
        if not isinstance(self.feature, FeatureName):
            raise ValueError("feature must be a FeatureName.")
        if not isinstance(self.operator, RuleOperator):
            raise ValueError("operator must be a RuleOperator.")

        if self.operator == RuleOperator.BETWEEN:
            self._validate_between_value()
            return

        if isinstance(self.value, tuple):
            raise ValueError("non-BETWEEN operators require a numeric value.")

    def _validate_between_value(self) -> None:
        if not isinstance(self.value, tuple) or len(self.value) != 2:
            raise ValueError("BETWEEN requires a two-item tuple value.")

        lower, upper = self.value
        if lower > upper:
            raise ValueError("BETWEEN lower bound must be less than or equal to upper bound.")


@dataclass(frozen=True, slots=True)
class BonusRule:
    name: str
    conditions: tuple[RuleCondition, ...]
    points: float

    def __post_init__(self) -> None:
        _validate_rule(self.name, self.conditions, self.points)


@dataclass(frozen=True, slots=True)
class PenaltyRule:
    name: str
    conditions: tuple[RuleCondition, ...]
    points: float

    def __post_init__(self) -> None:
        _validate_rule(self.name, self.conditions, self.points)


@dataclass(frozen=True, slots=True)
class ScoringProfile:
    name: str
    weights: dict[FeatureName, float]
    bonus_rules: tuple[BonusRule, ...] = ()
    penalty_rules: tuple[PenaltyRule, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("name must not be empty.")

        self._validate_weights()
        self._validate_duplicate_rule_names(self.bonus_rules, "bonus")
        self._validate_duplicate_rule_names(self.penalty_rules, "penalty")

    def _validate_weights(self) -> None:
        if not self.weights:
            raise ValueError("weights must not be empty.")

        invalid_features = [
            feature
            for feature in self.weights
            if not isinstance(feature, FeatureName)
        ]
        if invalid_features:
            raise ValueError("all weight keys must be FeatureName values.")

        expected_features = set(FeatureName)
        configured_features = set(self.weights)

        missing_features = expected_features - configured_features
        if missing_features:
            missing_names = ", ".join(sorted(feature.value for feature in missing_features))
            raise ValueError(f"weights are missing features: {missing_names}")

        unknown_features = configured_features - expected_features
        if unknown_features:
            unknown_names = ", ".join(str(feature) for feature in unknown_features)
            raise ValueError(f"weights contain unknown features: {unknown_names}")

        if any(weight < 0.0 for weight in self.weights.values()):
            raise ValueError("weights must be greater than or equal to zero.")

        total_weight = sum(self.weights.values())
        if total_weight <= 0.0:
            raise ValueError("total weight must be greater than zero.")

        if abs(total_weight - 1.0) > WEIGHT_SUM_TOLERANCE:
            raise ValueError("weights must sum to 1.0.")

    @staticmethod
    def _validate_duplicate_rule_names(
        rules: tuple[BonusRule, ...] | tuple[PenaltyRule, ...],
        rule_type: str,
    ) -> None:
        names = [rule.name for rule in rules]
        if len(names) != len(set(names)):
            raise ValueError(f"duplicate {rule_type} rule names are not allowed.")


def _validate_rule(
    name: str,
    conditions: tuple[RuleCondition, ...],
    points: float,
) -> None:
    if not name.strip():
        raise ValueError("rule name must not be empty.")
    if not conditions:
        raise ValueError("rule conditions must not be empty.")
    if points < 0.0:
        raise ValueError("rule points must be greater than or equal to zero.")
