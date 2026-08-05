from pipeline.base_pipeline import PipelineStep, StepResult
from application.candidate.candidate_builder import CandidateBuilder

class CandidatePipeline(PipelineStep):
    """Pipeline step to generate and store clip candidates."""

    name = "Candidate"

    def execute(self, job) -> StepResult:
        """Executes candidate generation and stores results in metadata."""
        segments = job.manifest.transcript_segments
        builder = CandidateBuilder()
        candidates = builder.build(segments)

        # TODO (Sprint 3):
        # Replace legacy metadata dictionaries with Manifest.candidates after downstream pipelines are migrated.
        job.metadata["approved_candidates"] = [
            {
                "id": i,
                "title": c.reason,
                "score": int(c.score),
                "start": c.start,
                "end": c.end,
            }
            for i, c in enumerate(candidates, start=1)
        ]

        return StepResult(
            success=True,
            message="Candidate generation completed"
        )
