from __future__ import annotations

from domain.job.job import Job
from domain.job.status import JobStatus
from domain.segment import Segment
from media.subtitle_engine import SubtitleEngine
from pipeline.base_pipeline import PipelineStep, StepResult
from utils.logger import logger


class SubtitlePipeline(PipelineStep):
    """Generate ASS subtitle files for the current approved candidates."""

    name = "Subtitle"

    status = JobStatus.CORRECTING_SUBTITLE

    retries = 1

    def __init__(self) -> None:
        self.engine = SubtitleEngine()

    def execute(self, job: Job) -> StepResult:
        candidates = job.metadata.get("approved_candidates", [])

        if not candidates:
            raise RuntimeError("No approved candidates available for subtitle generation.")

        for index, candidate in enumerate(candidates, start=1):
            start = candidate["start"]
            end = candidate["end"]
            segments = self._clip_segments(
                job.manifest.transcript_segments,
                start,
                end,
            )
            subtitle_file = job.workspace / "subtitle" / f"clip_{index:03d}.ass"

            self.engine.generate(segments, subtitle_file)

            logger.info("Generated subtitle asset: %s", subtitle_file)

        return StepResult(
            success=True,
            message="Subtitle assets generated",
        )

    @staticmethod
    def _clip_segments(
        transcript: list[Segment],
        clip_start: float,
        clip_end: float,
    ) -> list[Segment]:
        segments: list[Segment] = []

        for index, segment in enumerate(transcript, start=1):
            start = max(segment.start, clip_start)
            end = min(segment.end, clip_end)

            if end <= start:
                continue

            segments.append(
                Segment(
                    id=index,
                    start=start - clip_start,
                    end=end - clip_start,
                    text=segment.text,
                )
            )

        return segments
