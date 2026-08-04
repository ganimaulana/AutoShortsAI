"""
==================================================
AutoShortsAI

Base Pipeline Step
==================================================
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from time import perf_counter


@dataclass(slots=True)
class StepResult:
    """
    Standard result returned by every pipeline step.
    """

    success: bool = True

    message: str = ""

    elapsed: float = 0.0


class PipelineStep(ABC):
    """
    Base class for every pipeline step.
    """

    name = "Unnamed"

    retries = 0

    def run(
        self,
        job,
        context,
    ) -> StepResult:

        start = perf_counter()

        attempt = 0

        while True:

            try:

                result = self.execute(
                    job,
                    context,
                )

                if result is None:

                    result = StepResult()

                result.elapsed = (
                    perf_counter() - start
                )

                return result

            except Exception as e:

                attempt += 1

                if attempt > self.retries:

                    return StepResult(
                        success=False,
                        message=str(e),
                        elapsed=perf_counter() - start,
                    )

    @abstractmethod
    def run(
        self,
        job,
        context,
    ) -> StepResult:

        from time import perf_counter
        import traceback

        start = perf_counter()

        attempt = 0

        while True:

            try:

                print(f"[{self.name}] execute()")

                result = self.execute(
                    job,
                    context,
                )

                if result is None:
                    result = StepResult()

                result.elapsed = perf_counter() - start

                print(f"[{self.name}] SUCCESS")

                return result

            except Exception as e:

                print("=" * 80)
                print(f"[{self.name}] EXCEPTION")
                traceback.print_exc()
                print("=" * 80)

                attempt += 1

                if attempt > self.retries:

                    return StepResult(
                        success=False,
                        message=traceback.format_exc(),
                        elapsed=perf_counter() - start,
                    )

                print(
                    f"[{self.name}] retry {attempt}/{self.retries}"
                )