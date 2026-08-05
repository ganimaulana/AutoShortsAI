import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from application.scoring.scoring_engine import ScoringEngine
from domain.feature_vector import FeatureName, FeatureVector
from domain.scoring_profile import (
    BonusRule,
    PenaltyRule,
    RuleCondition,
    RuleOperator,
    ScoringProfile,
)


def make_weights() -> dict[FeatureName, float]:
    feature_count = len(tuple(FeatureName))
    return {feature: 1.0 / feature_count for feature in FeatureName}


def make_feature_vector(**overrides: float) -> FeatureVector:
    values = {feature.value: 0.0 for feature in FeatureName}
    values.update(overrides)

    return FeatureVector(**values)


def make_profile(
    bonus_rules: tuple[BonusRule, ...] = (),
    penalty_rules: tuple[PenaltyRule, ...] = (),
) -> ScoringProfile:
    return ScoringProfile(
        name="Test",
        weights=make_weights(),
        bonus_rules=bonus_rules,
        penalty_rules=penalty_rules,
    )


def test_score_calculates_weighted_scores_for_every_feature() -> None:
    weights = make_weights()
    vector = make_feature_vector(hook_strength=0.5, curiosity=0.25, coverage=1.0)

    score = ScoringEngine().score(
        vector,
        ScoringProfile(name="Test", weights=weights),
    )

    assert set(score.weighted_scores) == set(FeatureName)
    assert score.weighted_scores[FeatureName.HOOK_STRENGTH] == pytest.approx(
        0.5 * weights[FeatureName.HOOK_STRENGTH]
    )
    assert score.weighted_scores[FeatureName.CURIOSITY] == pytest.approx(
        0.25 * weights[FeatureName.CURIOSITY]
    )
    assert score.weighted_scores[FeatureName.COVERAGE] == pytest.approx(
        1.0 * weights[FeatureName.COVERAGE]
    )


def test_score_converts_weighted_sum_to_100_point_scale() -> None:
    vector = make_feature_vector(**{feature.value: 0.5 for feature in FeatureName})

    score = ScoringEngine().score(vector, make_profile())

    assert score.total_score == pytest.approx(50.0)


def test_score_applies_profile_bonus_rule() -> None:
    score = ScoringEngine().score(
        make_feature_vector(hook_strength=0.9),
        make_profile(
            bonus_rules=(
                BonusRule(
                    name="strong_hook",
                    conditions=(
                        RuleCondition(FeatureName.HOOK_STRENGTH, RuleOperator.GT, 0.8),
                    ),
                    points=5.0,
                ),
            )
        ),
    )

    assert score.bonuses == {"strong_hook": 5.0}


def test_score_applies_profile_penalty_rule() -> None:
    score = ScoringEngine().score(
        make_feature_vector(coverage=0.25),
        make_profile(
            penalty_rules=(
                PenaltyRule(
                    name="low_coverage",
                    conditions=(RuleCondition(FeatureName.COVERAGE, RuleOperator.LT, 0.5),),
                    points=8.0,
                ),
            )
        ),
    )

    assert score.penalties == {"low_coverage": 8.0}


def test_score_applies_multi_condition_bonus_rule_with_and_semantics() -> None:
    profile = make_profile(
        bonus_rules=(
            BonusRule(
                name="hook_curiosity_synergy",
                conditions=(
                    RuleCondition(FeatureName.HOOK_STRENGTH, RuleOperator.GTE, 0.7),
                    RuleCondition(FeatureName.CURIOSITY, RuleOperator.GTE, 0.7),
                ),
                points=6.0,
            ),
        )
    )

    matched = ScoringEngine().score(
        make_feature_vector(hook_strength=0.7, curiosity=0.8),
        profile,
    )
    unmatched = ScoringEngine().score(
        make_feature_vector(hook_strength=0.7, curiosity=0.6),
        profile,
    )

    assert matched.bonuses == {"hook_curiosity_synergy": 6.0}
    assert unmatched.bonuses == {}


def test_score_applies_multi_condition_penalty_rule_with_and_semantics() -> None:
    profile = make_profile(
        penalty_rules=(
            PenaltyRule(
                name="short_and_weak_ending",
                conditions=(
                    RuleCondition(FeatureName.DURATION, RuleOperator.LT, 8.0),
                    RuleCondition(FeatureName.ENDING_STRENGTH, RuleOperator.LTE, 0.2),
                ),
                points=10.0,
            ),
        )
    )

    matched = ScoringEngine().score(
        make_feature_vector(duration=5.0, ending_strength=0.2),
        profile,
    )
    unmatched = ScoringEngine().score(
        make_feature_vector(duration=5.0, ending_strength=0.3),
        profile,
    )

    assert matched.penalties == {"short_and_weak_ending": 10.0}
    assert unmatched.penalties == {}


def test_score_ignores_unmatched_bonus_and_penalty_rules() -> None:
    score = ScoringEngine().score(
        make_feature_vector(hook_strength=0.8, coverage=0.5),
        make_profile(
            bonus_rules=(
                BonusRule(
                    name="strong_hook",
                    conditions=(
                        RuleCondition(FeatureName.HOOK_STRENGTH, RuleOperator.GT, 0.8),
                    ),
                    points=5.0,
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

    assert score.bonuses == {}
    assert score.penalties == {}


@pytest.mark.parametrize(
    ("operator", "expected", "actual"),
    (
        (RuleOperator.GT, 0.4, 0.5),
        (RuleOperator.GTE, 0.5, 0.5),
        (RuleOperator.LT, 0.6, 0.5),
        (RuleOperator.LTE, 0.5, 0.5),
        (RuleOperator.EQ, 0.5, 0.5),
        (RuleOperator.NEQ, 0.4, 0.5),
        (RuleOperator.BETWEEN, (0.4, 0.6), 0.5),
    ),
)
def test_score_supports_all_rule_operators(
    operator: RuleOperator,
    expected: float | tuple[float, float],
    actual: float,
) -> None:
    score = ScoringEngine().score(
        make_feature_vector(curiosity=actual),
        make_profile(
            bonus_rules=(
                BonusRule(
                    name="operator_match",
                    conditions=(RuleCondition(FeatureName.CURIOSITY, operator, expected),),
                    points=4.0,
                ),
            )
        ),
    )

    assert score.bonuses == {"operator_match": 4.0}


def test_score_clamps_below_zero() -> None:
    score = ScoringEngine().score(
        make_feature_vector(),
        make_profile(
            penalty_rules=(
                PenaltyRule(
                    name="large_penalty",
                    conditions=(RuleCondition(FeatureName.COVERAGE, RuleOperator.LTE, 0.0),),
                    points=25.0,
                ),
            )
        ),
    )

    assert score.total_score == 0.0


def test_score_clamps_above_100() -> None:
    score = ScoringEngine().score(
        make_feature_vector(**{feature.value: 1.0 for feature in FeatureName}),
        make_profile(
            bonus_rules=(
                BonusRule(
                    name="large_bonus",
                    conditions=(RuleCondition(FeatureName.COVERAGE, RuleOperator.GTE, 1.0),),
                    points=25.0,
                ),
            )
        ),
    )

    assert score.total_score == 100.0


def test_score_breakdown_contains_only_applied_bonuses_and_penalties() -> None:
    score = ScoringEngine().score(
        make_feature_vector(hook_strength=0.9, coverage=0.4, emotion=0.6),
        make_profile(
            bonus_rules=(
                BonusRule(
                    name="applied_bonus",
                    conditions=(
                        RuleCondition(FeatureName.HOOK_STRENGTH, RuleOperator.GT, 0.8),
                    ),
                    points=3.0,
                ),
                BonusRule(
                    name="unmatched_bonus",
                    conditions=(RuleCondition(FeatureName.CURIOSITY, RuleOperator.GT, 0.8),),
                    points=3.0,
                ),
            ),
            penalty_rules=(
                PenaltyRule(
                    name="applied_penalty",
                    conditions=(RuleCondition(FeatureName.COVERAGE, RuleOperator.LT, 0.5),),
                    points=2.0,
                ),
                PenaltyRule(
                    name="unmatched_penalty",
                    conditions=(RuleCondition(FeatureName.EMOTION, RuleOperator.LT, 0.5),),
                    points=2.0,
                ),
            ),
        ),
    )

    assert score.bonuses == {"applied_bonus": 3.0}
    assert score.penalties == {"applied_penalty": 2.0}


def test_score_handles_zero_feature_vector() -> None:
    score = ScoringEngine().score(make_feature_vector(), make_profile())

    assert score.total_score == 0.0
    assert all(value == 0.0 for value in score.weighted_scores.values())
    assert score.bonuses == {}
    assert score.penalties == {}


def test_score_handles_perfect_feature_vector() -> None:
    score = ScoringEngine().score(
        make_feature_vector(**{feature.value: 1.0 for feature in FeatureName}),
        make_profile(),
    )

    assert score.total_score == pytest.approx(100.0)
    assert sum(score.weighted_scores.values()) == pytest.approx(1.0)
