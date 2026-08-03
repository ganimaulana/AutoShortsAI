from pipeline.base_step import PipelineStep


class WhisperStep(

    PipelineStep

):

    name = "Whisper"

    def execute(

        self,

        job,

        context,

    ):

        return context