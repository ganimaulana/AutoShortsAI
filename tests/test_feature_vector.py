import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain.feature_vector import FeatureName, FeatureVector


def make_feature_vector() -> FeatureVector:
    return FeatureVector(
        hook_strength=0.1,
        curiosity=0.2,
        conflict=0.3,
        emotion=0.4,
        novelty=0.5,
        ending_strength=0.6,
        pacing=0.7,
        people=0.8,
        numbers=0.9,
        question=1.0,
        cta=0.0,
        duration=12.0,
        coverage=0.75,
    )


def test_feature_vector_get_returns_value_for_feature_name() -> None:
    vector = make_feature_vector()

    assert vector.get(FeatureName.HOOK_STRENGTH) == 0.1
    assert vector.get(FeatureName.DURATION) == 12.0
    assert vector.get(FeatureName.COVERAGE) == 0.75


def test_feature_vector_rejects_unknown_feature_key() -> None:
    vector = make_feature_vector()

    with pytest.raises(ValueError, match="FeatureName"):
        vector.get("hook_strength")  # type: ignore[arg-type]


def test_feature_name_values_match_feature_vector_fields() -> None:
    vector_fields = set(FeatureVector.__dataclass_fields__)
    feature_names = {feature.value for feature in FeatureName}

    assert feature_names == vector_fields
