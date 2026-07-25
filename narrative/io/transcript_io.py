"""
==================================================
Narrative Intelligence Engine (NIE)

Transcript IO
==================================================
"""

from pathlib import Path

from domain import Segment

from .base_io import BaseIO


class TranscriptIO(BaseIO):

    @staticmethod
    def load(path):

        data = BaseIO.load_json(path)

        segments = []

        for i, item in enumerate(data):

            segments.append(

                Segment(

                    id=i + 1,

                    start=item["start"],

                    end=item["end"],

                    text=item["text"]

                )

            )

        return segments

    @staticmethod
    def save(path, segments):

        output = []

        for segment in segments:

            output.append({

                "start": segment.start,

                "end": segment.end,

                "text": segment.text

            })

        BaseIO.save_json(
            path,
            output
        )