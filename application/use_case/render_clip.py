from domain.render.render_plan import RenderPlan


class RenderClip:

    def __init__(

        self,

        ffmpeg,

    ):

        self.ffmpeg = ffmpeg

    def run(

        self,

        plans,

    ):

        outputs = []

        for plan in plans:

            output = self.ffmpeg.render(plan)

            outputs.append(output)

        return outputs