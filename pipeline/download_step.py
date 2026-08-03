from pipeline.base_step import PipelineStep


class DownloadStep(

    PipelineStep

):

    name = "Download"

    def execute(

        self,

        job,

        context,

    ):

        #
        # nanti yt-dlp
        #

        print(

            "Downloading",

            job,

        )

        return context