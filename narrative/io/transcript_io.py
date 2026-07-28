"""
==================================================
Narrative Intelligence Engine (NIE)

Transcript IO
==================================================
"""

from pathlib import Path

from domain.segment import Segment
from domain.word import Word

from .base_io import BaseIO


class TranscriptIO(BaseIO):

    FILE_NAME = "transcript.json"

    # ==================================================
    # PATH
    # ==================================================

    @classmethod
    def path(cls, project_path) -> Path:
        """
        Return transcript.json path from project folder.
        """
        return Path(project_path) / cls.FILE_NAME

    # ==================================================
    # RESOLVE PATH
    # ==================================================

    @classmethod
    def resolve_path(cls, path) -> Path:
        """
        Backward compatible.

        Support:

        TranscriptIO.load(project_path)

        and

        TranscriptIO.load(project_path / "transcript.json")
        """

        path = Path(path)

        #
        # Already transcript.json
        #

        if path.suffix.lower() == ".json":
            return path

        #
        # Project folder
        #

        return path / cls.FILE_NAME

    # ==================================================
    # EXISTS
    # ==================================================

    @classmethod
    def exists(cls, path) -> bool:

        return cls.resolve_path(path).exists()

    # ==================================================
    # LOAD
    # ==================================================

    @classmethod
    def load(cls, path):

        path = cls.resolve_path(path)

        data = BaseIO.load_json(path)

        segments = []

        for i, item in enumerate(
            data,
            start=1,
        ):

            words = []

            for w in item.get(
                "words",
                [],
            ):

                words.append(

                    Word(

                        text=w["text"],

                        start=w["start"],

                        end=w["end"],

                        confidence=w.get(
                            "confidence"
                        ),

                    )

                )

            segments.append(

                Segment(

                    id=item.get(
                        "id",
                        i,
                    ),

                    start=item["start"],

                    end=item["end"],

                    text=item["text"],

                    words=words,

                )

            )

        return segments

    # ==================================================
    # SAVE
    # ==================================================

    @classmethod
    def save(
        cls,
        path,
        segments,
    ):

        path = cls.resolve_path(path)

        output = []

        for segment in segments:

            words = []

            for word in getattr(
                segment,
                "words",
                [],
            ):

                words.append(

                    {

                        "text": word.text,

                        "start": word.start,

                        "end": word.end,

                        "confidence": word.confidence,

                    }

                )

            output.append(

                {

                    "id": segment.id,

                    "start": segment.start,

                    "end": segment.end,

                    "duration": round(

                        segment.end - segment.start,

                        2,

                    ),

                    "text": segment.text,

                    "words": words,

                }

            )

        BaseIO.save_json(
            path,
            output,
        )