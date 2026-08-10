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

            ass_path = Path(plan.subtitle_file).resolve().as_posix()

            ass_path = ass_path.replace(":", "\\:")

            filters.append(
                f"subtitles='{ass_path}'"
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
            # Redirect std streams so FFmpeg never inherits invalid GUI
            # standard handles on Windows. A PySide6 app launched without a
            # console exposes invalid stdin/stdout/stderr handles; passing
            # them to CreateProcess raises OSError [Errno 22] Invalid argument.
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return plan.output_video
