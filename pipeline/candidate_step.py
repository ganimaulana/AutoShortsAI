from pipeline.base_step import PipelineStep


class CandidateStep(

    PipelineStep

):

    name = "Candidate"

    def execute(

        self,

        job,

        context,

    ):

        return context