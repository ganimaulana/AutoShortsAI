from pipeline.base_step import PipelineStep


class RenderStep(

    PipelineStep

):

    name = "Render"

    def execute(

        self,

        job,

        context,

    ):

        return context