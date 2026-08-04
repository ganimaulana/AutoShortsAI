from __future__ import annotations

from domain.job.job import Job

from application.workflow import (
    WorkflowEngine,
    WorkflowStage,
)

from pipeline.runner import PipelineRunner

from infrastructure.filesystem.workspace_manager import (
    WorkspaceManager,
)


class JobOrchestrator:
    """
    Single entry point untuk menjalankan satu Job.
    """

    def __init__(
        self,
        runner: PipelineRunner,
        workspace: WorkspaceManager,
        workflow: WorkflowEngine,
    ):

        self.runner = runner
        self.workspace = workspace
        self.workflow = workflow

    def execute(
        self,
        job: Job,
    ) -> Job:

        self.workflow.begin()

        try:

            self.workspace.prepare(job)

            self.workflow.stage(
                WorkflowStage.DOWNLOAD,
                0,
            )

            self.runner.run(job)

            self.workflow.finish()

            return job

        except Exception as e:

            self.workflow.fail(e)

            raise