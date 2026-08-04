from pathlib import Path

from faster_whisper import WhisperModel

from domain.job.status import JobStatus

from pipeline.base_pipeline import (
    PipelineStep,
    StepResult,
)


class WhisperPipeline(PipelineStep):

    name = "Whisper"

    status = JobStatus.TRANSCRIBING

    retries = 1

    def __init__(

        self,

        model_size="small",

        device="auto",

        compute_type="auto",

    ):

        self.model = WhisperModel(

            model_size,

            device=device,

            compute_type=compute_type,

        )

    def execute(

        self,

        job,

    ):

        video = job.manifest.video

        segments, info = self.model.transcribe(

            str(video),

            word_timestamps=True,

        )

        output = []

        for segment in segments:

            words = []

            if segment.words:

                for w in segment.words:

                    words.append(

                        {

                            "word": w.word,

                            "start": w.start,

                            "end": w.end,

                        }

                    )

            output.append(

                {

                    "start": segment.start,

                    "end": segment.end,

                    "text": segment.text,

                    "words": words,

                }

            )

        transcript_dir = (

            job.workspace /

            "transcript"

        )

        transcript_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        transcript_file = (

            transcript_dir /

            "raw.json"

        )

        import json

        with open(

            transcript_file,

            "w",

            encoding="utf8",

        ) as f:

            json.dump(

                output,

                f,

                ensure_ascii=False,

                indent=2,

            )

        job.manifest.transcript_raw = transcript_file

        #
        # Temporary candidate
        #

        if output:

            start = output[0]["start"]

            end = output[-1]["end"]

            #
            # Maksimal 60 detik
            #

            end = min(
                end,
                start + 60,
            )

            job.metadata["approved_candidates"] = [

                {

                    "id": 1,

                    "title": "Auto Candidate",

                    "score": 100,

                    "start": start,

                    "end": end,

                }

            ]

        return StepResult(

            success=True,

            message="Transcript created",

        )