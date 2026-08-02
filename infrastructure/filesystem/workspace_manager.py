from pathlib import Path

from domain.job.job import Job


class WorkspaceManager:

    def prepare(
        self,
        job: Job,
    ) -> None:

        if not job.workspace:

            raise RuntimeError(
                "Workspace belum ditentukan."
            )

        folders = [

            "input",

            "transcript",

            "ai",

            "subtitle",

            "output",

            "logs",

            "temp",

        ]

        for folder in folders:

            (

                job.workspace

                / folder

            ).mkdir(

                parents=True,

                exist_ok=True,

            )