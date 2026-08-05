from __future__ import annotations

from dataclasses import dataclass

from application.candidate.story_patterns import StoryPattern, get_default_story_patterns
from domain.candidate import Candidate
from domain.story_intelligence import StorySegment, StorySegmentType


@dataclass(frozen=True, slots=True)
class StoryPatternMatch:
    pattern: StoryPattern
    matched_segments: tuple[StorySegment, ...]


@dataclass(frozen=True, slots=True)
class StoryCandidateMatch:
    match: StoryPatternMatch
    candidate: Candidate


class StoryCandidateBuilder:
    """Builds clip candidates from deterministic story pattern matches."""

    def __init__(
        self,
        patterns: tuple[StoryPattern, ...] | None = None,
        maximum_candidates: int = 100,
    ) -> None:
        configured_patterns = patterns if patterns is not None else get_default_story_patterns()
        self.patterns = tuple(
            sorted(configured_patterns, key=lambda pattern: (pattern.priority, pattern.name))
        )
        self.maximum_candidates = maximum_candidates
        self._validate_configuration()

    def build(self, story_segments: list[StorySegment]) -> list[Candidate]:
        return [
            candidate_match.candidate
            for candidate_match in self.build_matches(story_segments)
        ]

    def build_matches(self, story_segments: list[StorySegment]) -> list[StoryCandidateMatch]:
        if not story_segments:
            return []

        candidate_matches: list[StoryCandidateMatch] = []

        for pattern_match in self._find_matches(story_segments):
            if not self._validate_match(pattern_match):
                continue

            candidate = self._build_candidate(pattern_match)

            if self._validate_candidate(pattern_match.pattern, candidate):
                candidate_matches.append(
                    StoryCandidateMatch(
                        match=pattern_match,
                        candidate=candidate,
                    )
                )

        return self._deduplicate_matches(candidate_matches)[: self.maximum_candidates]

    def _validate_configuration(self) -> None:
        if not self.patterns:
            raise ValueError("patterns must not be empty.")
        if self.maximum_candidates <= 0:
            raise ValueError("maximum_candidates must be greater than zero.")

    def _find_matches(self, story_segments: list[StorySegment]) -> list[StoryPatternMatch]:
        ordered_segments = sorted(
            story_segments,
            key=lambda segment: (segment.start, segment.end, segment.id),
        )
        matches: list[StoryPatternMatch] = []

        for pattern in self.patterns:
            for start_index, segment in enumerate(ordered_segments):
                if not self._segment_matches_type(segment, pattern.sequence[0]):
                    continue

                matched_segments = self._match_from_index(
                    pattern,
                    ordered_segments,
                    start_index,
                )

                if matched_segments is not None:
                    matches.append(
                        StoryPatternMatch(
                            pattern=pattern,
                            matched_segments=matched_segments,
                        )
                    )

        return matches

    def _match_from_index(
        self,
        pattern: StoryPattern,
        ordered_segments: list[StorySegment],
        start_index: int,
    ) -> tuple[StorySegment, ...] | None:
        matched_segments = [ordered_segments[start_index]]
        search_start_index = start_index + 1

        for expected_type in pattern.sequence[1:]:
            previous_match_index = search_start_index - 1
            next_match_index = self._find_next_match_index(
                ordered_segments,
                search_start_index,
                previous_match_index,
                expected_type,
                pattern.max_gap,
            )

            if next_match_index is None:
                return None

            matched_segments.append(ordered_segments[next_match_index])
            search_start_index = next_match_index + 1

        return tuple(matched_segments)

    def _find_next_match_index(
        self,
        ordered_segments: list[StorySegment],
        search_start_index: int,
        previous_match_index: int,
        expected_type: StorySegmentType,
        max_gap: int,
    ) -> int | None:
        last_allowed_index = min(
            len(ordered_segments) - 1,
            previous_match_index + max_gap + 1,
        )

        for index in range(search_start_index, last_allowed_index + 1):
            if self._segment_matches_type(ordered_segments[index], expected_type):
                return index

        return None

    @staticmethod
    def _segment_matches_type(
        segment: StorySegment,
        expected_type: StorySegmentType,
    ) -> bool:
        return segment.primary_type == expected_type or expected_type in segment.types

    @staticmethod
    def _validate_match(pattern_match: StoryPatternMatch) -> bool:
        return len(pattern_match.matched_segments) == len(pattern_match.pattern.sequence)

    @staticmethod
    def _build_candidate(pattern_match: StoryPatternMatch) -> Candidate:
        return Candidate(
            start=pattern_match.matched_segments[0].start,
            end=pattern_match.matched_segments[-1].end,
            score=0.0,
            reason=f"Story Pattern: {pattern_match.pattern.name}",
        )

    @staticmethod
    def _validate_candidate(pattern: StoryPattern, candidate: Candidate) -> bool:
        duration = candidate.end - candidate.start
        return pattern.minimum_duration <= duration <= pattern.maximum_duration

    @staticmethod
    def _deduplicate(candidates: list[Candidate]) -> list[Candidate]:
        deduplicated_candidates: list[Candidate] = []
        seen_windows: set[tuple[float, float]] = set()

        for candidate in candidates:
            window_key = StoryCandidateBuilder._candidate_window_key(candidate)

            if window_key in seen_windows:
                continue

            seen_windows.add(window_key)
            deduplicated_candidates.append(candidate)

        return deduplicated_candidates

    @staticmethod
    def _deduplicate_matches(
        candidate_matches: list[StoryCandidateMatch],
    ) -> list[StoryCandidateMatch]:
        deduplicated_matches: list[StoryCandidateMatch] = []
        seen_windows: set[tuple[float, float]] = set()

        for candidate_match in candidate_matches:
            window_key = StoryCandidateBuilder._candidate_window_key(
                candidate_match.candidate
            )

            if window_key in seen_windows:
                continue

            seen_windows.add(window_key)
            deduplicated_matches.append(candidate_match)

        return deduplicated_matches

    @staticmethod
    def _candidate_window_key(candidate: Candidate) -> tuple[float, float]:
        return (round(candidate.start, 3), round(candidate.end, 3))
