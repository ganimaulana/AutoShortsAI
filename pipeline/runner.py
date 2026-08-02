from __future__ import annotations

from domain.job.job import Job
from domain.job.status import JobStatus

from pipeline.base_pipeline import PipelineStep


class PipelineRunner:

    def __init__(
        self,
        steps: list[PipelineStep],
    ):
        self.steps = steps

    def run(
        self,
        job: Job,
    ) -> Job:

        total = len(self.steps)

        for index, step in enumerate(self.steps):

            job.update_progress(

                int(

                    index

                    /

                    total

                    * 100

                )

            )

            attempt = 0

            while True:

                result = step.run(job)

                if result.success:
                    break

                attempt += 1

                if attempt > step.retries:

                    job.fail(result.message)

                    return job

        job.complete()

        return job