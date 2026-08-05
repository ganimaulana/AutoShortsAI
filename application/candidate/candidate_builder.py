import logging

from domain.candidate import Candidate
from domain.segment import Segment

logger = logging.getLogger(__name__)


class CandidateBuilder:
    """Pure business logic to generate clip candidates from transcript segments."""

    def __init__(
        self,
        minimum_duration: float = 25.0,
        target_duration: float = 35.0,
        maximum_duration: float = 60.0,
        stride: float = 10.0,
        maximum_candidates: int = 100,
    ) -> None:
        self.minimum_duration = minimum_duration
        self.target_duration = target_duration
        self.maximum_duration = maximum_duration
        self.stride = stride
        self.maximum_candidates = maximum_candidates
        self._validate_configuration()

    def build(self, segments: list[Segment]) -> list[Candidate]:
        """Generates candidates based on transcript segments."""
        if not segments:
            return []

        ordered_segments = sorted(segments, key=lambda segment: segment.start)
        transcript_start = ordered_segments[0].start
        transcript_end = ordered_segments[-1].end
        transcript_duration = transcript_end - transcript_start

        if transcript_duration < self.minimum_duration:
            logger.info(
                "Transcript too short for candidate generation: %.2fs",
                transcript_duration,
            )
            return []

        candidates: list[Candidate] = []
        seen_windows: set[tuple[float, float]] = set()

        for anchor in self._generate_window_anchors(
            transcript_start,
            transcript_end,
        ):
            start = self._find_nearest_segment_start(
                ordered_segments,
                anchor,
            )
            end = self._find_best_segment_end(
                ordered_segments,
                start,
                transcript_end,
            )

            if not self._is_valid_window(start, end):
                continue

            window_key = (round(start, 3), round(end, 3))

            if window_key in seen_windows:
                continue

            seen_windows.add(window_key)
            candidates.append(
                Candidate(
                    start=start,
                    end=end,
                    score=0.0,
                    reason="Auto Candidate",
                )
            )

            if len(candidates) >= self.maximum_candidates:
                break

        logger.info("Generated %s clip candidates.", len(candidates))
        return candidates

    def _validate_configuration(self) -> None:
        if self.minimum_duration <= 0:
            raise ValueError("minimum_duration must be greater than zero.")

        if self.target_duration < self.minimum_duration:
            raise ValueError(
                "target_duration must be greater than or equal to minimum_duration."
            )

        if self.maximum_duration < self.target_duration:
            raise ValueError(
                "maximum_duration must be greater than or equal to target_duration."
            )

        if self.stride <= 0:
            raise ValueError("stride must be greater than zero.")

        if self.maximum_candidates <= 0:
            raise ValueError("maximum_candidates must be greater than zero.")

    def _generate_window_anchors(
        self,
        transcript_start: float,
        transcript_end: float,
    ) -> list[float]:
        anchors: list[float] = []
        last_valid_start = transcript_end - self.minimum_duration
        anchor = transcript_start

        while anchor <= last_valid_start:
            anchors.append(anchor)
            anchor += self.stride

        return anchors

    @staticmethod
    def _find_nearest_segment_start(
        segments: list[Segment],
        anchor: float,
    ) -> float:
        return min(
            (segment.start for segment in segments),
            key=lambda start: (abs(start - anchor), start),
        )

    def _find_best_segment_end(
        self,
        segments: list[Segment],
        start: float,
        transcript_end: float,
    ) -> float:
        minimum_end = start + self.minimum_duration
        target_end = start + self.target_duration
        maximum_end = min(start + self.maximum_duration, transcript_end)

        valid_segments = [
            segment
            for segment in segments
            if minimum_end <= segment.end <= maximum_end
        ]

        if not valid_segments:
            return maximum_end

        sentence_boundary_segments = [
            segment
            for segment in valid_segments
            if self._is_sentence_boundary(segment)
        ]

        preferred_segments = sentence_boundary_segments or valid_segments

        return min(
            preferred_segments,
            key=lambda segment: (abs(segment.end - target_end), segment.end),
        ).end

    @staticmethod
    def _is_sentence_boundary(segment: Segment) -> bool:
        text = segment.text.strip()

        return text.endswith((".", "!", "?", "..."))

    def _is_valid_window(
        self,
        start: float,
        end: float,
    ) -> bool:
        if end <= start:
            return False

        return end - start >= self.minimum_duration
