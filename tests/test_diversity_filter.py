import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from application.ranking.diversity_filter import DiversityFilter
from application.ranking.diversity_rules import DiversityRules
from domain.candidate import Candidate
from domain.candidate_score import CandidateScore
from domain.ranked_candidate import RankedCandidate


def make_ranked_candidate(
    start: float,
    end: float,
    rank: int,
) -> RankedCandidate:
    return RankedCandidate(
        candidate=Candidate(start=start, end=end),
        score=CandidateScore(
            total_score=100.0 - rank,
            weighted_scores={},
            penalties={},
            bonuses={},
        ),
        rank=rank,
        input_index=rank - 1,
        tie_break_values={"input_index": rank - 1},
    )


def make_rules(
    overlap_threshold: float = 0.8,
    maximum_candidates: int = 10,
) -> DiversityRules:
    return DiversityRules(
        overlap_threshold=overlap_threshold,
        maximum_candidates=maximum_candidates,
    )


def test_filter_returns_empty_list_for_empty_input() -> None:
    filtered = DiversityFilter().filter([], make_rules())

    assert filtered == []


def test_filter_keeps_candidates_with_no_overlap() -> None:
    first = make_ranked_candidate(0.0, 10.0, 1)
    second = make_ranked_candidate(20.0, 30.0, 2)

    filtered = DiversityFilter().filter([first, second], make_rules())

    assert filtered == [first, second]


def test_filter_discards_complete_overlap_and_keeps_earlier_ranked_candidate() -> None:
    first = make_ranked_candidate(0.0, 30.0, 1)
    second = make_ranked_candidate(5.0, 25.0, 2)

    filtered = DiversityFilter().filter([first, second], make_rules(overlap_threshold=0.8))

    assert filtered == [first]


def test_filter_keeps_partial_overlap_below_threshold() -> None:
    first = make_ranked_candidate(0.0, 30.0, 1)
    second = make_ranked_candidate(20.0, 50.0, 2)

    filtered = DiversityFilter().filter([first, second], make_rules(overlap_threshold=0.8))

    assert DiversityFilter.overlap_ratio(first, second) == pytest.approx(10.0 / 30.0)
    assert filtered == [first, second]


def test_filter_discards_overlap_above_threshold() -> None:
    first = make_ranked_candidate(0.0, 30.0, 1)
    second = make_ranked_candidate(5.0, 35.0, 2)

    filtered = DiversityFilter().filter([first, second], make_rules(overlap_threshold=0.8))

    assert DiversityFilter.overlap_ratio(first, second) == pytest.approx(25.0 / 30.0)
    assert filtered == [first]


def test_filter_discards_identical_windows() -> None:
    first = make_ranked_candidate(0.0, 30.0, 1)
    second = make_ranked_candidate(0.0, 30.0, 2)

    filtered = DiversityFilter().filter([first, second], make_rules(overlap_threshold=0.8))

    assert DiversityFilter.overlap_ratio(first, second) == 1.0
    assert filtered == [first]


def test_filter_respects_maximum_candidates() -> None:
    first = make_ranked_candidate(0.0, 10.0, 1)
    second = make_ranked_candidate(20.0, 30.0, 2)
    third = make_ranked_candidate(40.0, 50.0, 3)

    filtered = DiversityFilter().filter(
        [first, second, third],
        make_rules(maximum_candidates=2),
    )

    assert filtered == [first, second]


def test_filter_output_is_deterministic_and_preserves_ranking_order() -> None:
    first = make_ranked_candidate(0.0, 30.0, 1)
    second = make_ranked_candidate(5.0, 35.0, 2)
    third = make_ranked_candidate(40.0, 50.0, 3)
    candidates = [first, second, third]

    first_result = DiversityFilter().filter(candidates, make_rules(overlap_threshold=0.8))
    second_result = DiversityFilter().filter(candidates, make_rules(overlap_threshold=0.8))

    assert first_result == second_result
    assert first_result == [first, third]
    assert [candidate.rank for candidate in first_result] == [1, 3]


def test_diversity_rules_reject_invalid_overlap_threshold() -> None:
    with pytest.raises(ValueError, match="overlap_threshold"):
        DiversityRules(overlap_threshold=1.1, maximum_candidates=10)


def test_diversity_rules_reject_invalid_maximum_candidates() -> None:
    with pytest.raises(ValueError, match="maximum_candidates"):
        DiversityRules(overlap_threshold=0.8, maximum_candidates=0)
