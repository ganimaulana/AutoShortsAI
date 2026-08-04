from __future__ import annotations

from pipeline.base_pipeline import PipelineStep


class PipelineRunner:

    def __init__(
        self,
        progress_callback=None,
        log_callback=None,
        cancel_callback=None,
    ):

        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.cancel_callback = cancel_callback

        self.steps = []

    def add_step(self, step: PipelineStep) -> None:

        self.steps.append(step)

    def run(self, job):
        """Run registered steps using one shared Job instance.

        Progress and log callbacks intentionally retain their existing GUI
        signatures: ``(percent, stage_name)`` and ``(message,)``.
        """

        print("=" * 60)
        print("PIPELINE RUNNER START")
        print("TOTAL STEPS =", len(self.steps))
        print("=" * 60)

        total = len(self.steps)

        if total == 0:

            raise RuntimeError("Pipeline has no registered steps.")

        for index, step in enumerate(
            self.steps,
            start=1,
        ):
            print(f"EXECUTING STEP: {step.name}")

            #
            # Cancel
            #

            if self.cancel_callback:

                if self.cancel_callback():

                    job.cancel()

                    raise RuntimeError(
                        "Pipeline cancelled."
                    )

            #
            # Progress
            #

            percent = int(
                ((index - 1) / total) * 100
            )

            if self.progress_callback:

                self.progress_callback(
                    percent,
                    step.name,
                )

            #
            # Log
            #

            if self.log_callback:

                self.log_callback(
                    f"[{step.name}] Started"
                )

            #
            # Execute
            #

            result = step.run(job)

            if not result.success:

                job.fail(result.message)

                raise RuntimeError(
                    result.message
                )

            #
            # Finished
            #

            if self.log_callback:

                self.log_callback(
                    f"[{step.name}] Finished"
                )

            print(f"RUNNER: {step.name} Finished")

        if self.progress_callback:

            self.progress_callback(
                100,
                "Completed",
            )

        print("RUNNER: Pipeline Completed")

        job.complete()

        return job
