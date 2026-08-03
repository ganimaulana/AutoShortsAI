"""
==================================================
AutoShortsAI

Workflow Engine
==================================================
"""

from application.workflow import (
    JobState,
    WorkflowStage,
)

from utils.logger import logger


class WorkflowEngine:

    def __init__(self):

        self.state = JobState()

    # -------------------------------------------------

    def begin(self):

        self.state.start()

        logger.info("Workflow started.")

    # -------------------------------------------------

    def stage(
        self,
        stage: WorkflowStage,
        progress: int,
    ):

        self.state.update(
            stage,
            progress,
        )

        logger.info(
            f"[{progress}%] {stage.value}"
        )

    # -------------------------------------------------

    def finish(self):

        self.state.finish()

        logger.info("Workflow finished.")

    # -------------------------------------------------

    def fail(
        self,
        error: Exception,
    ):

        self.state.fail(str(error))

        logger.error(str(error))