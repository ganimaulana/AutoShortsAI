from __future__ import annotations

from collections.abc import Callable

from domain.job.job import Job
from pipeline.base_pipeline import PipelineStep


class PipelineRunner:

    def __init__(
        self,
        steps: list[PipelineStep],
        *,
        progress_callback: Callable[[int, str], None] | None = None,
        log_callback: Callable[[str], None] | None = None,
        cancel_callback: Callable[[], bool] | None = None,
    ):

        self.steps = steps

        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.cancel_callback = cancel_callback

    def _log(self, message: str) -> None:

        if self.log_callback:
            self.log_callback(message)

    def _progress(
        self,
        percent: int,
        status: str,
    ) -> None:

        if self.progress_callback:
            self.progress_callback(
                percent,
                status,
            )

    def run(
        self,
        job: Job,
    ) -> Job:

        total = len(self.steps)

        if total == 0:
            job.complete()
            return job

        for index, step in enumerate(self.steps):

            if self.cancel_callback and self.cancel_callback():

                job.cancel()

                self._log(
                    "[SYSTEM] Pipeline cancelled."
                )

                return job

            percent = int(
                (index / total) * 100
            )

            job.update_progress(percent)

            self._progress(
                percent,
                step.name,
            )

            self._log(
                f"[{step.name}] Started"
            )

            attempt = 0

            while True:

                result = step.run(job)

                if result.success:

                    break

                attempt += 1

                self._log(

                    f"[{step.name}] Retry "

                    f"{attempt}/{step.retries}"

                )

                if attempt > step.retries:

                    job.fail(result.message)

                    self._log(

                        f"[ERROR] {result.message}"

                    )

                    return job

            self._log(
                f"[{step.name}] Finished"
            )

        job.complete()

        self._progress(
            100,
            "Completed",
        )

        self._log(
            "[SUCCESS] Pipeline completed."
        )

        return job