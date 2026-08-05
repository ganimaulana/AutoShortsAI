from __future__ import annotations

from dataclasses import dataclass

from domain.candidate import Candidate
from domain.candidate_score import CandidateScore


@dataclass(frozen=True, slots=True)
class RankedCandidate:
    """Candidate plus deterministic rank metadata."""

    candidate: Candidate
    score: CandidateScore
    rank: int
    input_index: int
    tie_break_values: dict[str, float | int | str]
