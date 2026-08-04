from pathlib import Path

from domain.render.render_plan import RenderPlan


class RenderPlanBuilder:

    def run(self, job, candidates):

        plans = []

        output_dir = job.workspace / "output"

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        for index, candidate in enumerate(candidates, start=1):

            output = output_dir / f"clip_{index:03d}.mp4"

            subtitle = (
                job.workspace
                / "subtitle"
                / f"clip_{index:03d}.ass"
            )

            start = (
                candidate["start"]
                if isinstance(candidate, dict)
                else candidate.start
            )

            end = (
                candidate["end"]
                if isinstance(candidate, dict)
                else candidate.end
            )

            plans.append(

                RenderPlan(

                    input_video=job.manifest.video,

                    output_video=output,

                    subtitle_file=subtitle,

                    start=start,

                    end=end,

                )

            )

        return plans