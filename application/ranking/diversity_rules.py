from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DiversityRules:
    """Configuration for deterministic temporal diversity filtering."""

    overlap_threshold: float
    maximum_candidates: int

    def __post_init__(self) -> None:
        if not 0.0 <= self.overlap_threshold <= 1.0:
            raise ValueError("overlap_threshold must be between 0.0 and 1.0.")
        if self.maximum_candidates <= 0:
            raise ValueError("maximum_candidates must be greater than zero.")
