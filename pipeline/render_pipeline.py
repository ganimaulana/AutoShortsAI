from domain.job.status import JobStatus

from pipeline.base_pipeline import (
    PipelineStep,
    StepResult,
)

from application.use_case.render_plan_builder import (
    RenderPlanBuilder,
)

from infrastructure.ffmpeg.ffmpeg_service import (
    FFmpegService,
)


class RenderPipeline(PipelineStep):

    name = "Render"

    status = JobStatus.RENDERING

    retries = 1

    def __init__(self):

        self.builder = RenderPlanBuilder()

        self.ffmpeg = FFmpegService()

    def execute(self, job):

        candidates = job.metadata["approved_candidates"]

        print("=" * 60)
        print("CANDIDATES TYPE :", type(candidates))
        print("FIRST TYPE      :", type(candidates[0]))
        print("FIRST VALUE     :", candidates[0])
        print("=" * 60)

        plans = self.builder.run(
            job,
            candidates,
        )

        total = len(plans)

        for i, plan in enumerate(plans):

            print(
                f"[Render] {i + 1}/{total}"
            )

            self.ffmpeg.render(plan)

        return StepResult(
            success=True,
        )