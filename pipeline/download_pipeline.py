from __future__ import annotations

from pathlib import Path

from domain.job.job import Job
from domain.job.status import JobStatus

from core.downloader import download_video

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
        print("=" * 60)
        print("DOWNLOAD PIPELINE")
        print("JOB WORKSPACE     :", job.workspace)
        print("WORKSPACE EXISTS  :", job.workspace.exists())

        input_dir = job.workspace / "input"

        print("INPUT DIR         :", input_dir)
        print("INPUT EXISTS      :", input_dir.exists())
        print("=" * 60)
        
        print("DOWNLOAD 1")

        input_dir = job.workspace / "input"

        print("=" * 60)
        print("JOB WORKSPACE :", job.workspace)
        print("WORKSPACE EXISTS :", job.workspace.exists())
        print("INPUT PATH :", input_dir)
        print("PARENT EXISTS :", input_dir.parent.exists())
        print("=" * 60)

        input_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        print("DOWNLOAD 2")

        video_path = download_video(
            job.url,
            input_dir,
        )

        print("DOWNLOAD 3:", video_path)

        if not video_path.exists():

            print("DOWNLOAD 4")

            return StepResult(
                success=False,
                message="Downloaded video not found.",
            )

        print("DOWNLOAD 5")

        job.manifest.video = video_path

        print("DOWNLOAD 6")

        return StepResult(
            success=True,
            message="Video downloaded",
        )