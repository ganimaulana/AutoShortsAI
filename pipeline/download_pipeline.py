from __future__ import annotations

from pathlib import Path

from domain.job.job import Job
from domain.job.status import JobStatus

from infrastructure.downloader import download_video

from pipeline.base_pipeline import (
    PipelineStep,
    StepResult,
)


class DownloadPipeline(PipelineStep):

    name = "Download"

    status = JobStatus.DOWNLOADING

    retries = 3

    def execute(
        self,
        job: Job,
    ) -> StepResult:

        input_dir = job.workspace / "input"

        input_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        video_path = download_video(
            job.url,
            input_dir,
        )

        if not video_path.exists():

            return StepResult(
                success=False,
                message="Downloaded video not found.",
            )

        job.manifest.video = video_path

        return StepResult(
            success=True,
            message="Video downloaded",
        )