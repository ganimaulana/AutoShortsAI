"""
==================================================
AutoShortsAI

Workflow Job State
==================================================
"""

from dataclasses import dataclass, field
from datetime import datetime

from application.workflow.workflow_stage import WorkflowStage


@dataclass(slots=True)
class JobState:

    stage: WorkflowStage = WorkflowStage.PENDING

    progress: int = 0

    started_at: datetime | None = None

    finished_at: datetime | None = None

    error: str | None = None

    metadata: dict = field(default_factory=dict)

    def start(self):

        self.started_at = datetime.now()

        self.error = None

    def finish(self):

        self.finished_at = datetime.now()

        self.stage = WorkflowStage.FINISHED

        self.progress = 100

    def fail(self, message: str):

        self.stage = WorkflowStage.FAILED

        self.error = message

    def update(
        self,
        stage: WorkflowStage,
        progress: int,
    ):

        self.stage = stage

        self.progress = progress