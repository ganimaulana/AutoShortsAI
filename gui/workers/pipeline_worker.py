from __future__ import annotations

import traceback

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot


class PipelineWorker(QObject):

    started = Signal()

    finished = Signal()

    failed = Signal(str)

    progress = Signal(int)

    status = Signal(str)

    log = Signal(str, str)

    def __init__(self, orchestrator, job):

        super().__init__()

        self.orchestrator = orchestrator

        self.job = job

    @Slot()
    def run(self):

        try:

            self.started.emit()

            self.log.emit(
                "Pipeline started",
                "SUCCESS",
            )

            self.orchestrator.execute(
                self.job
            )

            self.progress.emit(100)

            self.status.emit(
                "Completed"
            )

            self.log.emit(
                "Pipeline finished",
                "SUCCESS",
            )

            self.finished.emit()

        except Exception:

            error = traceback.format_exc()

            self.failed.emit(error)

            self.log.emit(
                error,
                "ERROR",
            )