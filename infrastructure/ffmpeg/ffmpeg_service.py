from pathlib import Path
import subprocess

from domain.render.render_plan import RenderPlan


class FFmpegService:

    def render(
        self,
        plan: RenderPlan,
    ) -> Path:

        duration = plan.end - plan.start

        command = [

            "ffmpeg",

            "-hide_banner",

            "-loglevel",

            "error",

            "-y",

            "-ss",

            str(plan.start),

            "-i",

            str(plan.input_video),

            "-t",

            str(duration),

        ]

        filters = []

        #
        # Vertical crop
        #

        if plan.crop_vertical:

            filters.append(
                "scale=1080:1920:force_original_aspect_ratio=increase,"
                "crop=1080:1920"
            )

        #
        # Subtitle (optional)
        #

        if (
            plan.burn_subtitle
            and plan.subtitle_file
            and Path(plan.subtitle_file).exists()
        ):

            filters.append(
                f"subtitles={plan.subtitle_file}"
            )

        if filters:

            command.extend(

                [

                    "-vf",

                    ",".join(filters),

                ]

            )

        command.extend(

            [

                "-c:v",

                "libx264",

                "-preset",

                "medium",

                "-crf",

                "18",

                "-c:a",

                "aac",

                "-movflags",

                "+faststart",

                str(plan.output_video),

            ]

        )

        print("=" * 60)
        print("FFMPEG COMMAND")
        print(command)
        print("=" * 60)

        subprocess.run(
            command,
            check=True,
        )

        return plan.output_video