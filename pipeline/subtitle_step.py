from pipeline.base_step import PipelineStep


class SubtitleStep(

    PipelineStep

):

    name = "Subtitle"

    def execute(

        self,

        job,

        context,

    ):

        return context