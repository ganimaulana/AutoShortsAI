from pipeline.base_step import PipelineStep


class ReviewerStep(

    PipelineStep

):

    name = "Reviewer"

    def execute(

        self,

        job,

        context,

    ):

        return context