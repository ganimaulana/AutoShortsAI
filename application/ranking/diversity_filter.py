from __future__ import annotations

import logging

from application.ranking.diversity_rules import DiversityRules
from domain.ranked_candidate import RankedCandidate

logger = logging.getLogger(__name__)


class DiversityFilter:
    """Removes highly overlapping ranked candidates without reordering."""

    def filter(
        self,
        ranked_candidates: list[RankedCandidate],
        rules: DiversityRules,
    ) -> list[RankedCandidate]:
        accepted: list[RankedCandidate] = []

        for ranked_candidate in ranked_candidates:
            if len(accepted) >= rules.maximum_candidates:
                break

            if self._overlaps_accepted_candidate(ranked_candidate, accepted, rules):
                logger.debug(
                    "Discarded ranked candidate %d due to temporal overlap.",
                    ranked_candidate.rank,
                )
                continue

            accepted.append(ranked_candidate)

        return accepted

    def _overlaps_accepted_candidate(
        self,
        candidate: RankedCandidate,
        accepted_candidates: list[RankedCandidate],
        rules: DiversityRules,
    ) -> bool:
        return any(
            self.overlap_ratio(candidate, accepted_candidate) >= rules.overlap_threshold
            for accepted_candidate in accepted_candidates
        )

    @staticmethod
    def overlap_ratio(
        first: RankedCandidate,
        second: RankedCandidate,
    ) -> float:
        first_duration = DiversityFilter._duration(first)
        second_duration = DiversityFilter._duration(second)
        shorter_duration = min(first_duration, second_duration)

        if shorter_duration <= 0.0:
            return 0.0

        overlap_start = max(first.candidate.start, second.candidate.start)
        overlap_end = min(first.candidate.end, second.candidate.end)
        overlap_duration = max(0.0, overlap_end - overlap_start)

        return overlap_duration / shorter_duration

    @staticmethod
    def _duration(candidate: RankedCandidate) -> float:
        return max(0.0, candidate.candidate.end - candidate.candidate.start)
