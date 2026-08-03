from domain.job.status import JobStatus

from pipeline.base_pipeline import (

    PipelineStep,

    StepResult,

)

from application.use_cases.render_plan_builder import (

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

        candidates = job.metadata[
            "approved_candidates"
        ]

        plans = self.builder.run(

            job,

            candidates,

        )

        total = len(plans)

        for i, plan in enumerate(plans):

            self.ffmpeg.render(plan)

            

        return StepResult(
            success=True,
        )