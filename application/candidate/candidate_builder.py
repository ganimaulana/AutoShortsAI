from domain.segment import Segment
from domain.candidate import Candidate

class CandidateBuilder:
    """Pure business logic to generate clip candidates from transcript segments."""

    def build(self, segments: list[Segment]) -> list[Candidate]:
        """Generates candidates based on transcript segments."""
        if not segments:
            return []

        start = segments[0].start
        end = segments[-1].end

        # Legacy clamping logic: max 60 seconds
        end = min(end, start + 60)

        return [
            Candidate(
                start=start,
                end=end,
                score=100.0,
                reason="Auto Candidate"
            )
        ]
