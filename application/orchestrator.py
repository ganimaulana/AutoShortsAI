from __future__ import annotations

from pathlib import Path

from domain.job.job import Job

from pipeline.runner import PipelineRunner

from infrastructure.filesystem.workspace_manager import (
    WorkspaceManager,
)


class JobOrchestrator:
    """
    Mengatur seluruh lifecycle Job.
    """

    def __init__(
        self,
        runner: PipelineRunner,
        workspace: WorkspaceManager,
    ):

        self.runner = runner

        self.workspace = workspace

    def execute(
        self,
        job: Job,
    ) -> Job:

        # siapkan folder workspace
        self.workspace.prepare(job)

        # jalankan seluruh pipeline
        self.runner.run(job)

        return job