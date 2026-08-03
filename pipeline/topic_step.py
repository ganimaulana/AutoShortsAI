from pipeline.base_step import PipelineStep


class TopicStep(

    PipelineStep

):

    name = "Topic"

    def execute(

        self,

        job,

        context,

    ):

        return context