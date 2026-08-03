from __future__ import annotations


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

    def add_step(

        self,

        step,

    ):

        self.steps.append(step)

    def run(

        self,

        job,

    ):

        total = len(self.steps)

        context = None

        for index, step in enumerate(

            self.steps,

            start=1,

        ):

            if self.cancel_callback:

                if self.cancel_callback():

                    raise RuntimeError(

                        "Pipeline cancelled."

                    )

            percent = int(

                ((index - 1) / total)

                * 100

            )

            if self.progress_callback:

                self.progress_callback(

                    percent,

                    step.name,

                )

            if self.log_callback:

                self.log_callback(

                    f"[{step.name}] Started"

                )

            context = step.execute(

                job,

                context,

            )

            if self.log_callback:

                self.log_callback(

                    f"[{step.name}] Finished"

                )

        if self.progress_callback:

            self.progress_callback(

                100,

                "Completed",

            )

        return context