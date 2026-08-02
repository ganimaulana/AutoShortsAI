from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import perf_counter

from domain.job.job import Job
from domain.job.status import JobStatus


@dataclass(slots=True)
class StepResult:
    """
    Hasil eksekusi satu pipeline step.
    """

    success: bool

    message: str = ""

    elapsed: float = 0.0


class PipelineStep(ABC):
    """
    Base class untuk semua Pipeline.
    """

    # Nama step yang tampil di GUI
    name: str = "Pipeline"

    # Status Job ketika step ini berjalan
    status: JobStatus = JobStatus.PENDING

    # Retry otomatis jika gagal
    retries: int = 0

    def run(self, job: Job) -> StepResult:
        """
        Wrapper agar semua pipeline mempunyai
        timer dan error handling yang sama.
        """

        job.update_status(
            self.status,
            self.name,
        )

        start = perf_counter()

        try:

            result = self.execute(job)

            result.elapsed = perf_counter() - start

            return result

        except Exception as e:

            return StepResult(

                success=False,

                message=str(e),

                elapsed=perf_counter() - start,

            )

    @abstractmethod
    def execute(
        self,
        job: Job,
    ) -> StepResult:
        """
        Diimplementasikan oleh masing-masing pipeline.
        """
        ...