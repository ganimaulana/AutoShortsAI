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
    Contract untuk satu tahap pipeline berbasis ``Job``.

    Pipeline tidak lagi meneruskan context terpisah antar tahap. Semua input,
    state runtime, dan artefak tahap disimpan pada ``Job`` beserta manifest dan
    metadata-nya.
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

            if not isinstance(result, StepResult):

                raise TypeError(
                    f"{self.__class__.__name__}.execute() "
                    "must return StepResult."
                )

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
        Jalankan satu tahap dengan ``job`` sebagai satu-satunya execution unit.
        """
        ...
