from __future__ import annotations

import traceback

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot


class PipelineWorker(QObject):

    finished = Signal(object)

    error = Signal(str)

    log = Signal(str)

    progress = Signal(int, str)

    status = Signal(str)

    def __init__(

        self,

        job,

    ):

        super().__init__()

        self.job = job

        self.cancelled = False

    def cancel(self):

        self.cancelled = True

    @Slot()

    def run(self):

        try:

            if self.cancelled:

                raise RuntimeError(
                    "Pipeline cancelled."
                )

            from core.pipeline import run_pipeline

            print("=" * 60)
            print("WORKER START")
            print("JOB =", self.job)
            print("WORKSPACE =", self.job.workspace)
            print("=" * 60)

            context = run_pipeline(

                self.job,

                progress_callback=self.update_progress,

                log_callback=self.write_log,

                cancel_callback=self.is_cancelled,

            )

            self.write_log(
                "Pipeline Completed"
            )

            print("DEBUG: Pipeline Completed emitted")

            self.finished.emit(

                context

            )

        except Exception as e:

            tb = traceback.format_exc()

            print("=" * 80)
            print(tb)
            print("=" * 80)

            self.error.emit(tb)
            
            print("=" * 80)
            print("PIPELINE EXCEPTION")
            traceback.print_exc()
            print("=" * 80)

            self.error.emit(
                traceback.format_exc()
            )

    def update_progress(

        self,

        percent,

        status,

    ):

        self.progress.emit(
            percent,
            status,
        )

        self.status.emit(

            status

        )

    def write_log(

        self,

        message,

    ):

        self.log.emit(

            message

        )

    def is_cancelled(

        self,

    ):

        return self.cancelled
