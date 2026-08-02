from __future__ import annotations

from pathlib import Path

from yt_dlp import YoutubeDL

from domain.assets import Asset
from domain.job.status import JobStatus

from pipeline.base_pipeline import (
    PipelineStep,
    StepResult,
)


class DownloadPipeline(PipelineStep):

    name = "Download"

    status = JobStatus.DOWNLOADING

    retries = 3

    def execute(self, job):

        input_dir = job.workspace / "input"

        output_template = str(
            input_dir / "%(title)s.%(ext)s"
        )

        options = {

            "format": "bestvideo+bestaudio/best",

            "outtmpl": output_template,

            "merge_output_format": "mp4",

            "continuedl": True,

            "quiet": True,

            "noplaylist": True,

        }

        with YoutubeDL(options) as ydl:

            info = ydl.extract_info(

                job.url,

                download=True,

            )

            filename = Path(

                ydl.prepare_filename(info)

            ).with_suffix(".mp4")

        job.manifest.video = Asset(

            path=filename,

            exists=filename.exists(),

            size=filename.stat().st_size

            if filename.exists()

            else 0,

            created_by="DownloadPipeline",

            mime="video/mp4",

        )

        return StepResult(

            success=True,

            message="Video downloaded",

        )