import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from application.scoring.profile_registry import DEFAULT_PROFILES, ProfileRegistry
from domain.feature_vector import FeatureName
from domain.scoring_profile import (
    BonusRule,
    PenaltyRule,
    RuleCondition,
    RuleOperator,
    ScoringProfile,
)


def make_weights(value: float | None = None) -> dict[FeatureName, float]:
    if value is not None:
        return {feature: value for feature in FeatureName}

    weight = 1.0 / len(tuple(FeatureName))
    return {feature: weight for feature in FeatureName}


def test_scoring_profile_rejects_negative_weights() -> None:
    weights = make_weights()
    weights[FeatureName.HOOK_STRENGTH] = -0.1

    with pytest.raises(ValueError, match="greater than or equal to zero"):
        ScoringProfile(name="Invalid", weights=weights)


def test_scoring_profile_rejects_zero_total_weight() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        ScoringProfile(name="Invalid", weights=make_weights(0.0))


def test_scoring_profile_rejects_weights_that_do_not_sum_to_one() -> None:
    weights = make_weights()
    weights[FeatureName.HOOK_STRENGTH] += 0.1

    with pytest.raises(ValueError, match="sum to 1.0"):
        ScoringProfile(name="Invalid", weights=weights)


def test_scoring_profile_rejects_missing_feature_weight() -> None:
    weights = make_weights()
    del weights[FeatureName.CTA]

    with pytest.raises(ValueError, match="missing features"):
        ScoringProfile(name="Invalid", weights=weights)


def test_scoring_profile_rejects_unknown_feature_weight() -> None:
    weights = make_weights()
    weights["unknown"] = 0.0  # type: ignore[index]

    with pytest.raises(ValueError, match="FeatureName"):
        ScoringProfile(name="Invalid", weights=weights)


def test_rule_condition_rejects_invalid_operator() -> None:
    with pytest.raises(ValueError, match="RuleOperator"):
        RuleCondition(
            feature=FeatureName.CURIOSITY,
            operator="gte",  # type: ignore[arg-type]
            value=0.8,
        )


def test_rule_condition_supports_between_operator() -> None:
    condition = RuleCondition(
        feature=FeatureName.DURATION,
        operator=RuleOperator.BETWEEN,
        value=(8.0, 60.0),
    )

    assert condition.value == (8.0, 60.0)


def test_rule_condition_rejects_invalid_between_range() -> None:
    with pytest.raises(ValueError, match="lower bound"):
        RuleCondition(
            feature=FeatureName.DURATION,
            operator=RuleOperator.BETWEEN,
            value=(60.0, 8.0),
        )


def test_rule_rejects_empty_conditions() -> None:
    with pytest.raises(ValueError, match="conditions"):
        BonusRule(name="Invalid", conditions=(), points=1.0)


def test_rule_rejects_negative_points() -> None:
    with pytest.raises(ValueError, match="greater than or equal to zero"):
        PenaltyRule(
            name="Invalid",
            conditions=(RuleCondition(FeatureName.COVERAGE, RuleOperator.LT, 0.5),),
            points=-1.0,
        )


def test_profile_rejects_duplicate_bonus_rule_names() -> None:
    rule = BonusRule(
        name="duplicate",
        conditions=(RuleCondition(FeatureName.HOOK_STRENGTH, RuleOperator.GTE, 0.8),),
        points=1.0,
    )

    with pytest.raises(ValueError, match="duplicate bonus"):
        ScoringProfile(name="Invalid", weights=make_weights(), bonus_rules=(rule, rule))


def test_default_profiles_are_normalized() -> None:
    for profile in DEFAULT_PROFILES:
        assert sum(profile.weights.values()) == pytest.approx(1.0)


def test_default_profiles_define_every_feature() -> None:
    for profile in DEFAULT_PROFILES:
        assert set(profile.weights) == set(FeatureName)


def test_registry_rejects_duplicate_profile_names() -> None:
    profile = ScoringProfile(name="Duplicate", weights=make_weights())

    with pytest.raises(ValueError, match="Duplicate scoring profile name"):
        ProfileRegistry(profiles=(profile, profile))


def test_registry_lists_default_profiles() -> None:
    registry = ProfileRegistry()

    assert registry.list_profiles() == (
        "Educational",
        "Storytelling",
        "Podcast",
        "News",
    )


def test_registry_returns_profile_by_name() -> None:
    registry = ProfileRegistry()

    profile = registry.get_profile("Podcast")

    assert profile.name == "Podcast"


def test_registry_rejects_unknown_profile() -> None:
    registry = ProfileRegistry()

    with pytest.raises(KeyError, match="Unknown scoring profile"):
        registry.get_profile("Unknown")
