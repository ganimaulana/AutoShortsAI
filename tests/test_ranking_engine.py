import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from application.ranking.ranking_engine import RankingEngine
from application.ranking.ranking_rules import (
    RankingRules,
    SortDirection,
    TieBreakField,
    TieBreakRule,
)
from domain.candidate import Candidate
from domain.candidate_score import CandidateScore
from domain.ranked_candidate import RankedCandidate


def make_candidate(
    start: float,
    end: float,
    reason: str = "",
) -> Candidate:
    return Candidate(start=start, end=end, reason=reason)


def make_score(total_score: float) -> CandidateScore:
    return CandidateScore(
        total_score=total_score,
        weighted_scores={},
        penalties={},
        bonuses={},
    )


def rank(
    scored_candidates: list[tuple[Candidate, CandidateScore]],
    rules: RankingRules | None = None,
) -> list[RankedCandidate]:
    return RankingEngine().rank(scored_candidates, rules)


def test_rank_orders_candidates_by_total_score_descending_by_default() -> None:
    low = (make_candidate(0.0, 10.0), make_score(40.0))
    high = (make_candidate(10.0, 20.0), make_score(90.0))
    medium = (make_candidate(20.0, 30.0), make_score(60.0))

    ranked = rank([low, high, medium])

    assert [item.score.total_score for item in ranked] == [90.0, 60.0, 40.0]


def test_rank_assigns_one_based_ordinal_ranks() -> None:
    ranked = rank(
        [
            (make_candidate(0.0, 10.0), make_score(20.0)),
            (make_candidate(10.0, 20.0), make_score(30.0)),
        ]
    )

    assert [item.rank for item in ranked] == [1, 2]


def test_rank_returns_empty_list_for_empty_input() -> None:
    assert rank([]) == []


def test_rank_preserves_candidate_and_score_objects() -> None:
    candidate = make_candidate(1.0, 3.0, "Original")
    score = make_score(50.0)

    ranked = rank([(candidate, score)])

    assert ranked[0].candidate is candidate
    assert ranked[0].score is score


def test_rank_stores_input_index_explicitly() -> None:
    ranked = rank(
        [
            (make_candidate(0.0, 10.0), make_score(10.0)),
            (make_candidate(10.0, 20.0), make_score(20.0)),
        ]
    )

    assert [item.input_index for item in ranked] == [1, 0]


def test_rank_stores_tie_break_values_for_debugging() -> None:
    ranked = rank([(make_candidate(2.0, 7.0, "Reason"), make_score(80.0))])

    assert ranked[0].tie_break_values == {
        "total_score": 80.0,
        "duration": 5.0,
        "start": 2.0,
        "end": 7.0,
        "reason": "reason",
        "input_index": 0,
    }


def test_rank_tie_breaks_by_longer_duration_by_default() -> None:
    short = (make_candidate(0.0, 5.0), make_score(80.0))
    long = (make_candidate(10.0, 25.0), make_score(80.0))

    ranked = rank([short, long])

    assert [item.candidate for item in ranked] == [long[0], short[0]]


def test_rank_tie_breaks_by_earlier_start_by_default() -> None:
    later = (make_candidate(20.0, 30.0), make_score(80.0))
    earlier = (make_candidate(10.0, 20.0), make_score(80.0))

    ranked = rank([later, earlier])

    assert [item.candidate for item in ranked] == [earlier[0], later[0]]


def test_rank_tie_breaks_by_earlier_end_when_configured() -> None:
    rules = RankingRules(
        tie_breakers=(
            TieBreakRule(TieBreakField.TOTAL_SCORE, SortDirection.DESC),
            TieBreakRule(TieBreakField.END, SortDirection.ASC),
        )
    )
    later_end = (make_candidate(10.0, 22.0), make_score(80.0))
    earlier_end = (make_candidate(10.0, 20.0), make_score(80.0))

    ranked = rank([later_end, earlier_end], rules)

    assert [item.candidate for item in ranked] == [earlier_end[0], later_end[0]]


def test_rank_tie_breaks_by_reason_alphabetically_by_default() -> None:
    beta = (make_candidate(10.0, 20.0, "Beta"), make_score(80.0))
    alpha = (make_candidate(10.0, 20.0, "Alpha"), make_score(80.0))

    ranked = rank([beta, alpha])

    assert [item.candidate.reason for item in ranked] == ["Alpha", "Beta"]


def test_rank_supports_configurable_tie_breaking_for_shorter_duration() -> None:
    rules = RankingRules(
        tie_breakers=(
            TieBreakRule(TieBreakField.TOTAL_SCORE, SortDirection.DESC),
            TieBreakRule(TieBreakField.DURATION, SortDirection.ASC),
        )
    )
    short = (make_candidate(0.0, 5.0), make_score(80.0))
    long = (make_candidate(10.0, 25.0), make_score(80.0))

    ranked = rank([long, short], rules)

    assert [item.candidate for item in ranked] == [short[0], long[0]]


def test_rank_preserves_input_order_when_all_configured_fields_are_equal() -> None:
    first = (make_candidate(0.0, 10.0, "Same"), make_score(80.0))
    second = (make_candidate(0.0, 10.0, "Same"), make_score(80.0))

    ranked = rank([first, second])

    assert [item.input_index for item in ranked] == [0, 1]
    assert [item.candidate for item in ranked] == [first[0], second[0]]


def test_tie_break_rule_rejects_invalid_field() -> None:
    with pytest.raises(ValueError, match="TieBreakField"):
        TieBreakRule(field="total_score", direction=SortDirection.DESC)  # type: ignore[arg-type]


def test_tie_break_rule_rejects_invalid_sort_direction() -> None:
    with pytest.raises(ValueError, match="SortDirection"):
        TieBreakRule(field=TieBreakField.TOTAL_SCORE, direction="desc")  # type: ignore[arg-type]


def test_ranking_rules_reject_empty_tie_breakers() -> None:
    with pytest.raises(ValueError, match="tie_breakers"):
        RankingRules(tie_breakers=())


def test_ranking_rules_reject_duplicate_tie_break_fields() -> None:
    with pytest.raises(ValueError, match="duplicate"):
        RankingRules(
            tie_breakers=(
                TieBreakRule(TieBreakField.TOTAL_SCORE, SortDirection.DESC),
                TieBreakRule(TieBreakField.TOTAL_SCORE, SortDirection.ASC),
            )
        )
