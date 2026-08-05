from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class TieBreakField(str, Enum):
    TOTAL_SCORE = "total_score"
    START = "start"
    END = "end"
    DURATION = "duration"
    REASON = "reason"


class SortDirection(str, Enum):
    ASC = "asc"
    DESC = "desc"


@dataclass(frozen=True, slots=True)
class TieBreakRule:
    field: TieBreakField
    direction: SortDirection

    def __post_init__(self) -> None:
        if not isinstance(self.field, TieBreakField):
            raise ValueError("field must be a TieBreakField.")
        if not isinstance(self.direction, SortDirection):
            raise ValueError("direction must be a SortDirection.")


@dataclass(frozen=True, slots=True)
class RankingRules:
    tie_breakers: tuple[TieBreakRule, ...]

    def __post_init__(self) -> None:
        if not self.tie_breakers:
            raise ValueError("tie_breakers must not be empty.")

        fields = [rule.field for rule in self.tie_breakers]
        if len(fields) != len(set(fields)):
            raise ValueError("duplicate tie-break fields are not allowed.")


DEFAULT_RANKING_RULES = RankingRules(
    tie_breakers=(
        TieBreakRule(TieBreakField.TOTAL_SCORE, SortDirection.DESC),
        TieBreakRule(TieBreakField.DURATION, SortDirection.DESC),
        TieBreakRule(TieBreakField.START, SortDirection.ASC),
        TieBreakRule(TieBreakField.END, SortDirection.ASC),
        TieBreakRule(TieBreakField.REASON, SortDirection.ASC),
    )
)
