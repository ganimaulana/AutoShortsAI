"""
===========================================================
AutoShortsAI
Video Intelligence Core (VIC)

Feature Collection
===========================================================

Container for Feature objects.
"""

from __future__ import annotations

import json

from dataclasses import dataclass, field
from typing import Iterator
from collections.abc import Callable

from .feature import Feature


@dataclass(slots=True)
class FeatureCollection:
    """
    Collection of Feature objects.

    Features are indexed by feature.name,
    providing O(1) lookup by name.
    """

    _features: dict[str, Feature] = field(
        default_factory=dict
    )

    # ======================================================
    # Properties
    # ======================================================

    @property
    def count(self) -> int:
        """
        Number of stored features.
        """
        return len(self._features)

    @property
    def is_empty(self) -> bool:
        """
        Returns True if no feature exists.
        """
        return not self._features

    # ======================================================
    # CRUD
    # ======================================================
    def add(
        self,
        feature: Feature,
    ) -> None:
        """
        Add or replace a feature.
        """

        if not isinstance(feature, Feature):
            raise TypeError(
                f"'feature' must be a Feature instance, "
                f"got {type(feature).__name__}"
            )

        self._features[feature.name] = feature

    def replace(
        self,
        feature: Feature,
    ) -> None:
        """
        Replace existing feature.
        Alias of add().
        """
        self.add(feature)

    def remove(
        self,
        name: str,
    ) -> bool:
        """
        Remove feature by name.

        Returns True if removed.
        """
        return (
            self._features.pop(name, None)
            is not None
        )

    def clear(self) -> None:
        """
        Remove all features.
        """
        self._features.clear()

    # ======================================================
    # Query
    # ======================================================

    def get(
        self,
        name: str,
        default: Feature | None = None,
    ) -> Feature | None:
        """
        Get feature by name.
        """
        return self._features.get(name, default)


    def has(
        self,
        name: str,
    ) -> bool:
        """
        Returns True if feature exists.
        """
        return name in self._features


    def names(self) -> list[str]:
        """
        Returns all feature names.
        """
        return list(self._features.keys())


    def values(self) -> list[Feature]:
        """
        Returns all Feature objects.
        """
        return list(self._features.values())


    def items(self) -> list[tuple[str, Feature]]:
        """
        Returns all name-feature pairs.
        """
        return list(self._features.items())

    # ======================================================
    # Iterator
    # ======================================================

    def __iter__(self) -> Iterator[Feature]:
        """
        Iterate over Feature objects.
        """
        return iter(self._features.values())


    def __len__(self) -> int:
        """
        Number of stored features.
        """
        return len(self._features)


    def __contains__(
        self,
        name: str,
    ) -> bool:
        """
        Support:
            "emotion" in features
        """
        return name in self._features


    def __getitem__(
        self,
        name: str,
    ) -> Feature:
        """
        Get feature by name.

        Raises
        ------
        KeyError
            If the feature does not exist.
        """
        return self._features[name]
    
    # ======================================================
    # Ranking
    # ======================================================

    def sorted(
        self,
        *,
        reverse: bool = True,
        key: Callable[[Feature], float] | None = None,
    ) -> list[Feature]:
        """
        Return features sorted by score or custom key.
        """
        key = key or (lambda feature: feature.score)

        return sorted(
            self._features.values(),
            key=key,
            reverse=reverse,
        )


    def top(
        self,
        count: int = 5,
    ) -> list[Feature]:
        """
        Return top N features by score.
        """
        if count <= 0:
            return []

        return self.sorted()[:count]


    def bottom(
        self,
        count: int = 5,
    ) -> list[Feature]:
        """
        Return bottom N features by score.
        """
        if count <= 0:
            return []

        return self.sorted(reverse=False)[:count]

    # ======================================================
    # Aggregate
    # ======================================================

    def total_score(self) -> float:
        """
        Sum of all feature scores.
        """
        return sum(
            feature.score
            for feature in self._features.values()
        )


    def average_score(self) -> float:
        """
        Average feature score.
        """
        if self.is_empty:
            return 0.0

        return self.total_score() / self.count


    def max_score(self) -> float:
        """
        Highest feature score.
        """
        if self.is_empty:
            return 0.0

        return max(
            feature.score
            for feature in self._features.values()
        )


    def min_score(self) -> float:
        """
        Lowest feature score.
        """
        if self.is_empty:
            return 0.0

        return min(
            feature.score
            for feature in self._features.values()
        )

    # ======================================================
    # Merge
    # ======================================================

    def merge(
        self,
        other: "FeatureCollection",
        *,
        overwrite: bool = True,
    ) -> None:
        """
        Merge another FeatureCollection into this one.
        """

        for feature in other:
            if not overwrite and feature.name in self:
                continue

            self.add(feature)

    def copy(self) -> "FeatureCollection":
        """
        Create a shallow copy.
        """
        return FeatureCollection(
            _features=self._features.copy()
        )

    # ======================================================
    # Serialization
    # ======================================================

    def to_dict(self) -> dict[str, dict]:
        """
        Convert collection to dictionary.
        """
        return {
            name: feature.to_dict()
            for name, feature in self._features.items()
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, dict],
    ) -> "FeatureCollection":
        """
        Create collection from dictionary.
        """
        collection = cls()

        for feature_data in data.values():
            collection.add(
                Feature.from_dict(feature_data)
            )

        return collection

    def to_json(
        self,
        *,
        indent: int | None = 2,
    ) -> str:
        """
        Convert collection to JSON.
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
    ) -> "FeatureCollection":
        """
        Create collection from JSON.
        """
        return cls.from_dict(
            json.loads(text)
        )

    def as_dict(self) -> dict[str, Feature]:
        """
        Return a shallow copy of the internal mapping.
        """
        return self._features.copy()

    # ======================================================
    # Special Methods
    # ======================================================

    def __bool__(self) -> bool:
        return not self.is_empty


    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(count={self.count})"
        )
    