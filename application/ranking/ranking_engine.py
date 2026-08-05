from __future__ import annotations

import logging
from dataclasses import dataclass

from application.ranking.ranking_rules import (
    DEFAULT_RANKING_RULES,
    RankingRules,
    SortDirection,
    TieBreakField,
)
from domain.candidate import Candidate
from domain.candidate_score import CandidateScore
from domain.ranked_candidate import RankedCandidate

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class _RankingRecord:
    input_index: int
    candidate: Candidate
    score: CandidateScore


class RankingEngine:
    """Orders scored candidates deterministically and assigns ordinal ranks."""

    def rank(
        self,
        scored_candidates: list[tuple[Candidate, CandidateScore]],
        rules: RankingRules | None = None,
    ) -> list[RankedCandidate]:
        if not scored_candidates:
            return []

        ranking_rules = rules if rules is not None else DEFAULT_RANKING_RULES
        records = [
            _RankingRecord(
                input_index=index,
                candidate=candidate,
                score=score,
            )
            for index, (candidate, score) in enumerate(scored_candidates)
        ]

        ordered_records = self._sort_records(records, ranking_rules)
        filtered_records = self._apply_post_sort_filters(ordered_records, ranking_rules)

        logger.debug(
            "Ranked %d scored candidates with %d tie-break rules.",
            len(filtered_records),
            len(ranking_rules.tie_breakers),
        )

        return [
            RankedCandidate(
                candidate=record.candidate,
                score=record.score,
                rank=rank,
                input_index=record.input_index,
                tie_break_values=self._tie_break_values(record, ranking_rules),
            )
            for rank, record in enumerate(filtered_records, start=1)
        ]

    def _sort_records(
        self,
        records: list[_RankingRecord],
        rules: RankingRules,
    ) -> list[_RankingRecord]:
        ordered_records = list(records)
        ordered_records.sort(key=lambda record: record.input_index)

        for rule in reversed(rules.tie_breakers):
            ordered_records.sort(
                key=lambda record, field=rule.field: self._field_value(record, field),
                reverse=rule.direction == SortDirection.DESC,
            )

        return ordered_records

    def _apply_post_sort_filters(
        self,
        records: list[_RankingRecord],
        rules: RankingRules,
    ) -> list[_RankingRecord]:
        """Extension point for future diversity/overlap filtering."""

        return records

    def _tie_break_values(
        self,
        record: _RankingRecord,
        rules: RankingRules,
    ) -> dict[str, float | int | str]:
        values = {
            rule.field.value: self._field_value(record, rule.field)
            for rule in rules.tie_breakers
        }
        values["input_index"] = record.input_index
        return values

    @staticmethod
    def _field_value(
        record: _RankingRecord,
        field: TieBreakField,
    ) -> float | str:
        if field == TieBreakField.TOTAL_SCORE:
            return record.score.total_score
        if field == TieBreakField.START:
            return record.candidate.start
        if field == TieBreakField.END:
            return record.candidate.end
        if field == TieBreakField.DURATION:
            return record.candidate.end - record.candidate.start
        if field == TieBreakField.REASON:
            return record.candidate.reason.lower()

        raise ValueError(f"Unsupported tie-break field: {field}")
