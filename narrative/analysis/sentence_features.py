"""
===========================================================
AutoShortsAI
Video Intelligence Core (VIC)

Sentence Features
===========================================================

Represents a single analyzed sentence and its extracted
features.
"""

from __future__ import annotations

import json

from dataclasses import dataclass, field
from typing import Any

from .feature import Feature
from .feature_collection import FeatureCollection


@dataclass(slots=True)
class SentenceFeatures:
    """
    Represents a single analyzed sentence.

    A sentence contains:

    - transcript text
    - timestamps
    - extracted features
    - optional metadata
    """

    text: str

    start_time: float

    end_time: float

    features: FeatureCollection = field(
        default_factory=FeatureCollection
    )

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    # ======================================================
    # Properties
    # ======================================================

    @property
    def duration(self) -> float:
        """
        Duration of the sentence in seconds.
        """
        return self.end_time - self.start_time

    @property
    def feature_count(self) -> int:
        """
        Number of extracted features.
        """
        return self.features.count

    @property
    def has_features(self) -> bool:
        """
        Returns True if at least one feature exists.
        """
        return bool(self.features)

    # ======================================================
    # Feature Helpers
    # ======================================================

    def add_feature(
        self,
        feature: Feature,
    ) -> None:
        """
        Add a feature.
        """
        self.features.add(feature)

    def get_feature(
        self,
        name: str,
    ) -> Feature | None:
        """
        Get feature by name.
        """
        return self.features.get(name)

    def has_feature(
        self,
        name: str,
    ) -> bool:
        """
        Returns True if feature exists.
        """
        return self.features.has(name)

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict[str, Any]:
        """
        Convert sentence to dictionary.
        """
        return {
            "text": self.text,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "features": self.features.to_dict(),
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> "SentenceFeatures":
        """
        Create SentenceFeatures from dictionary.
        """
        return cls(
            text=data["text"],
            start_time=data["start_time"],
            end_time=data["end_time"],
            features=FeatureCollection.from_dict(
                data.get("features", {})
            ),
            metadata=data.get("metadata", {}),
        )

    def to_json(
        self,
        *,
        indent: int | None = 2,
    ) -> str:
        """
        Convert sentence to JSON.
        """
        return json.dumps(
            self.to_dict(),
            indent=indent,
            ensure_ascii=False,
        )

    @classmethod
    def from_json(
        cls,
        text: str,
    ) -> "SentenceFeatures":
        """
        Create SentenceFeatures from JSON.
        """
        return cls.from_dict(
            json.loads(text)
        )

    # ======================================================
    # Special Methods
    # ======================================================

    def __bool__(self) -> bool:
        """
        Returns True if sentence contains text.
        """
        return bool(self.text.strip())

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"start={self.start_time:.2f}, "
            f"end={self.end_time:.2f}, "
            f"features={self.feature_count})"
        )