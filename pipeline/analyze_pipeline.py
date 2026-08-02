from __future__ import annotations

from yt_dlp import YoutubeDL

from domain.job.status import JobStatus
from pipeline.base_pipeline import (
    PipelineStep,
    StepResult,
)


class AnalyzePipeline(PipelineStep):

    name = "Analyze"

    status = JobStatus.ANALYZING

    retries = 2

    def execute(self, job):

        options = {

            "quiet": True,

            "skip_download": True,

            "extract_flat": False,

        }

        with YoutubeDL(options) as ydl:

            info = ydl.extract_info(

                job.url,

                download=False,

            )

        job.metadata = {

            "id": info.get("id"),

            "title": info.get("title"),

            "channel": info.get("channel"),

            "uploader": info.get("uploader"),

            "duration": info.get("duration"),

            "view_count": info.get("view_count"),

            "like_count": info.get("like_count"),

            "upload_date": info.get("upload_date"),

            "thumbnail": info.get("thumbnail"),

            "description": info.get("description"),

            "language": info.get("language"),

            "categories": info.get("categories"),

            "tags": info.get("tags"),

            "fps": info.get("fps"),

            "width": info.get("width"),

            "height": info.get("height"),

        }

        return StepResult(
            success=True,
            message="Analyze completed",
        )