"""
===========================================================
AutoShortsAI
Video Intelligence Core (VIC)

Feature Model

Copyright (c) Gani Creative Studio
Powered by Naraseta AI
===========================================================

This module defines the smallest unit of AI knowledge used
throughout the Video Intelligence pipeline.

Every detector, classifier, ranking engine, timeline builder,
and future AI model communicates through Feature objects.

Example:

    Feature(
        name="emotion",
        value=0.82,
        feature_type=FeatureType.NUMERIC,
        confidence=0.91,
        source=FeatureSource.RULE_ENGINE,
        reason="Contains sadness keywords"
    )

Design Goals

- Immutable
- Serializable
- Explainable
- Plugin Friendly
- Type Safe
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any
import json
import math

# ==========================================================
# Type Aliases
# ==========================================================

FeatureValue = (
    float
    | bool
    | str
    | list[Any]
    | dict[str, Any]
)

# ==========================================================
# Feature Type
# ==========================================================


class FeatureType(str, Enum):
    """
    Defines the underlying data type stored by a Feature.
    """

    NUMERIC = "numeric"

    BOOLEAN = "boolean"

    TEXT = "text"

    CATEGORY = "category"

    VECTOR = "vector"

    OBJECT = "object"


# ==========================================================
# Feature Source
# ==========================================================


class FeatureSource(str, Enum):
    """
    Indicates where a feature originated.
    """

    UNKNOWN = "unknown"

    RULE_ENGINE = "rule_engine"

    REGEX = "regex"

    KEYWORD = "keyword"

    MACHINE_LEARNING = "machine_learning"

    LLM = "llm"

    GPT = "gpt"

    GEMINI = "gemini"

    CLAUDE = "claude"

    HUMAN = "human"

    API = "api"

    CUSTOM = "custom"


# ==========================================================
# Feature
# ==========================================================


@dataclass(frozen=True, slots=True)
class Feature:
    """
    Represents one AI feature.

    Examples
    --------

    emotion

    curiosity

    authority

    humor

    surprise

    speaker_change

    etc.
    """

    # -----------------------------
    # Identity
    # -----------------------------

    name: str

    # -----------------------------
    # Value
    # -----------------------------

    raw_value: FeatureValue

    value: FeatureValue

    feature_type: FeatureType

    # -----------------------------
    # Quality
    # -----------------------------

    confidence: float = 1.0

    weight: float = 1.0

    # -----------------------------
    # Explainability
    # -----------------------------

    source: FeatureSource = FeatureSource.UNKNOWN

    reason: str = ""

    version: str = "1.0"

    metadata: dict[str, Any] = field(default_factory=dict)

    # ======================================================

    def __post_init__(self) -> None:
        """
        Validate feature.
        """

        if self.is_vector and not isinstance(
            self.value,
            (list, tuple),
        ):
            raise TypeError(
                f"{self.name} expects vector."
            )

        if self.is_object and not isinstance(
            self.value,
            dict,
        ):
            raise TypeError(
                f"{self.name} expects dict."
            )


        if not self.name.strip():
            raise ValueError("Feature name cannot be empty.")

        if not isinstance(self.confidence, (int, float)):
            raise TypeError(
                "Confidence must be numeric."
            )

        if math.isnan(float(self.confidence)):
            raise ValueError(
                "Confidence cannot be NaN."
            )

        if not isinstance(self.weight, (int, float)):
            raise TypeError(
                "Weight must be numeric."
            )

        if math.isnan(float(self.weight)):
            raise ValueError(
                "Weight cannot be NaN."
            )

        if float(self.weight) < 0:
            raise ValueError(
                "Weight must be >= 0."
            )

        object.__setattr__(
            self,
            "confidence",
            max(0.0, min(1.0, self.confidence)),
        )

        if self.is_numeric and not isinstance(
            self.value,
            (int, float),
        ):
            raise TypeError(
                f"{self.name} expects numeric value."
            )

        if self.is_boolean and not isinstance(
            self.value,
            bool,
        ):
            raise TypeError(
                f"{self.name} expects bool."
            )

        if self.is_text and not isinstance(
            self.value,
            str,
        ):
            raise TypeError(
                f"{self.name} expects string."
            )

        if self.is_category and not isinstance(
            self.value,
            str,
        ):
            raise TypeError(
                f"{self.name} expects category string."
            )

    # ======================================================

    @property
    def score(self) -> float:
        """
        Returns weighted score.

        Numeric:
            value * confidence * weight

        Boolean:
            1/0 * confidence * weight

        Others:
            confidence * weight
        """

        if self.is_numeric:

            try:

                return (
                    float(self.value)
                    * self.confidence
                    * self.weight
                )

            except (TypeError, ValueError):

                return 0.0

        if self.is_boolean:

            return (
                (1.0 if self.value else 0.0)
                * self.confidence
                * self.weight
            )

        return (
            self.confidence
            * self.weight
        )

    # ======================================================

    @property
    def is_numeric(self) -> bool:

        return self.feature_type is FeatureType.NUMERIC

    @property
    def is_boolean(self) -> bool:

        return self.feature_type is FeatureType.BOOLEAN

    @property
    def is_text(self) -> bool:

        return self.feature_type is FeatureType.TEXT

    @property
    def is_category(self) -> bool:

        return self.feature_type is FeatureType.CATEGORY

    @property
    def is_vector(self) -> bool:

        return self.feature_type is FeatureType.VECTOR

    

    @property
    def is_object(self) -> bool:

         return self.feature_type is FeatureType.OBJECT
    
    @property
    def is_empty(self) -> bool:
        """
        Returns True if value is empty.
        """

        return (
            self.value is None
            or self.value == ""
        )    


    # ======================================================

    def copy_with(
        self,
        *,
        raw_value: FeatureValue | None = None,
        value: FeatureValue | None = None,
        confidence: float | None = None,
        weight: float | None = None,
        source: FeatureSource | None = None,
        reason: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "Feature":
        """
        Create modified immutable copy.
        """

        return replace(
            self,
            raw_value=self.raw_value if raw_value is None else raw_value,
            value=self.value if value is None else value,
            confidence=self.confidence if confidence is None else confidence,
            weight=self.weight if weight is None else weight,
            source=self.source if source is None else source,
            reason=self.reason if reason is None else reason,
            metadata=self.metadata if metadata is None else metadata,
        )

        # ======================================================

    def clamp(
        self,
        minimum: float = 0.0,
        maximum: float = 1.0,
    ) -> "Feature":
        """
        Clamp numeric feature value.

        Non-numeric features are returned unchanged.
        """

        if not self.is_numeric:
            return self

        try:
            value = float(self.value)
        except (TypeError, ValueError):
            return self

        value = max(minimum, min(maximum, value))

        return self.copy_with(value=value)

    # ======================================================

    def normalized(
        self,
        minimum: float,
        maximum: float,
    ) -> "Feature":
        """
        Normalize numeric feature into [0, 1].

        If maximum == minimum the original object is returned.
        """

        if not self.is_numeric:
            return self

        if maximum <= minimum:
            return self

        try:
            value = float(self.value)
        except (TypeError, ValueError):
            return self

        normalized = (value - minimum) / (maximum - minimum)

        normalized = max(0.0, min(1.0, normalized))

        return self.copy_with(
            raw_value=self.raw_value,
            value=normalized,
        )

    # ======================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize feature.
        """

        return {

            "name": self.name,

            "raw_value": self.raw_value,

            "value": self.value,

            "feature_type": self.feature_type.value,

            "confidence": self.confidence,

            "weight": self.weight,

            "score": self.score,

            "source": self.source.value,

            "reason": self.reason,

            "version": self.version,

            "metadata": self.metadata,
        }

    # ======================================================

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "Feature":
        """
        Create Feature from dictionary.
        """

        return cls(

            name=data["name"],

            raw_value=data.get(
            "raw_value",
            data.get("value"),
        ),

            value=data.get("value"),

            feature_type=FeatureType(
                data.get(
                    "feature_type",
                    FeatureType.OBJECT.value,
                )
            ),

            confidence=float(
                data.get(
                    "confidence",
                    1.0,
                )
            ),

            weight=float(
                data.get(
                    "weight",
                    1.0,
                )
            ),

            source=FeatureSource(
                data.get(
                    "source",
                    FeatureSource.UNKNOWN.value,
                )
            ),

            reason=data.get(
                "reason",
                "",
            ),

            version=data.get(
                "version",
                "1.0",
            ),

            metadata=data.get(
                "metadata",
                {},
            ),
        )

    # ======================================================

    def to_json(
        self,
        *,
        indent: int = 2,
    ) -> str:
        """
        Serialize feature to JSON.
        """

        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False,
        )

    # ======================================================

    @classmethod
    def from_json(
        cls,
        text: str,
    ) -> "Feature":
        """
        Deserialize JSON into Feature.
        """

        return cls.from_dict(
            json.loads(text)
        )

    # ======================================================

    def debug_string(self) -> str:
        """
        Human-readable debugging string.
        """

        return (
            f"[{self.name}] "
            f"raw={self.raw_value} "
            f"normalized={self.value} "
            f"type={self.feature_type.value} "
            f"confidence={self.confidence:.2f} "
            f"weight={self.weight:.2f} "
            f"score={self.score:.2f} "
            f"source={self.source.value}"
        )

    # ======================================================

    def explain(self) -> str:
        """
        Explain why this feature exists.
        """

        if self.reason:
            return self.reason

        return "No explanation available."

    @property
    def display_value(self) -> str:
        """
        Returns formatted value for GUI.
        """

        if self.is_numeric:

            value = float(self.value)

            if 0.0 <= value <= 1.0:
                return f"{value:.1%}"

            return f"{value:.2f}"

        return str(self.value)

    # ======================================================

    def __str__(self) -> str:

        return self.debug_string()

    # ======================================================

    def __repr__(self) -> str:

        return (
            "Feature("
            f"name={self.name!r}, "
            f"raw_value={self.raw_value!r}, "
            f"normalized={self.value!r}, "
            f"type={self.feature_type.value!r}, "
            f"confidence={self.confidence:.2f}, "
            f"weight={self.weight:.2f}"
            ")"
        )

    # ======================================================
    # Validation
    # ======================================================

    def is_valid(self) -> bool:
        """
        Returns True if the feature contains a valid value.
        """

        if math.isnan(float(self.confidence)):
            return False

        if not (0.0 <= self.confidence <= 1.0):
            return False

        if self.is_numeric:

            try:
                value = float(self.value)

                if math.isnan(value):
                    return False

                if math.isinf(value):
                    return False

            except (TypeError, ValueError):
                return False

        return True

        # ======================================================

    def __lt__(self, other: object) -> bool:

        if not isinstance(other, Feature):
            return NotImplemented

        return self.score < other.score

    # ======================================================

    def __le__(self, other: object) -> bool:

        if not isinstance(other, Feature):
            return NotImplemented

        return self.score <= other.score

    # ======================================================

    def __gt__(self, other: object) -> bool:

        if not isinstance(other, Feature):
            return NotImplemented

        return self.score > other.score

    # ======================================================

    def __ge__(self, other: object) -> bool:

        if not isinstance(other, Feature):
            return NotImplemented

        return self.score >= other.score

        # ======================================================
    # Factory
    # ======================================================

    @classmethod
    def numeric(
        cls,
        name: str,
        value: float,
        *,
        confidence: float = 1.0,
        source: FeatureSource = FeatureSource.UNKNOWN,
        reason: str = "",
    ) -> "Feature":

        return cls(
            name=name,

            raw_value=value,

            value=float(value),

            feature_type=FeatureType.NUMERIC,

            confidence=confidence,

            source=source,

            reason=reason,
        )

    # ======================================================

    @classmethod
    def boolean(
        cls,
        name: str,
        value: bool,
        *,
        confidence: float = 1.0,
        source: FeatureSource = FeatureSource.UNKNOWN,
        reason: str = "",
    ) -> "Feature":

        return cls(
            name=name,

            raw_value=value,

            value=bool(value),

            feature_type=FeatureType.BOOLEAN,

            confidence=confidence,

            source=source,

            reason=reason,
        )

    # ======================================================

    @classmethod
    def text(
        cls,
        name: str,
        value: str,
        *,
        confidence: float = 1.0,
        source: FeatureSource = FeatureSource.UNKNOWN,
        reason: str = "",
    ) -> "Feature":

        return cls(
            name=name,

            raw_value=value,

            value=value,

            feature_type=FeatureType.TEXT,

            confidence=confidence,

            source=source,

            reason=reason,
        )

    # ======================================================

    @classmethod
    def category(
        cls,
        name: str,
        value: str,
        *,
        confidence: float = 1.0,
        source: FeatureSource = FeatureSource.UNKNOWN,
        reason: str = "",
    ) -> "Feature":

        return cls(
            name=name,
            raw_value=value,
            value=value,
            feature_type=FeatureType.CATEGORY,
            confidence=confidence,
            source=source,
            reason=reason,
        )


    # ======================================================

    @classmethod
    def vector(
        cls,
        name: str,
        value: list[Any],
        *,
        confidence: float = 1.0,
        source: FeatureSource = FeatureSource.UNKNOWN,
        reason: str = "",
    ) -> "Feature":

        return cls(
            name=name,
            raw_value=value,
            value=value,
            feature_type=FeatureType.VECTOR,
            confidence=confidence,
            source=source,
            reason=reason,
        )


    @classmethod
    def object(
        cls,
        name: str,
        value: dict[str, Any],
        *,
        confidence: float = 1.0,
        source: FeatureSource = FeatureSource.UNKNOWN,
        reason: str = "",
    ) -> "Feature":

        return cls(
            name=name,
            raw_value=value,
            value=value,
            feature_type=FeatureType.OBJECT,
            confidence=confidence,
            source=source,
            reason=reason,
        )

