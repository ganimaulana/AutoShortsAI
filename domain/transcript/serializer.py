from __future__ import annotations

import json
from pathlib import Path

from domain.transcript.models import (
    Transcript,
    Sentence,
    Word,
    Chapter,
)


class TranscriptSerializer:

    @staticmethod
    def save(
        transcript: Transcript,
        path: Path,
    ) -> None:

        data = {

            "language": transcript.language,

            "duration": transcript.duration,

            "sentences": [],

            "chapters": [],

        }

        for sentence in transcript.sentences:

            data["sentences"].append(

                {

                    "id": sentence.id,

                    "start": sentence.start,

                    "end": sentence.end,

                    "text": sentence.text,

                    "words": [

                        {

                            "text": w.text,

                            "start": w.start,

                            "end": w.end,

                        }

                        for w in sentence.words

                    ],

                }

            )

        for chapter in transcript.chapters:

            data["chapters"].append(

                {

                    "id": chapter.id,

                    "start": chapter.start,

                    "end": chapter.end,

                    "title": chapter.title,

                    "summary": chapter.summary,

                    "emotion": chapter.emotion,

                    "score": chapter.score,

                }

            )

        path.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

        with open(

            path,

            "w",

            encoding="utf8",

        ) as f:

            json.dump(

                data,

                f,

                ensure_ascii=False,

                indent=2,

            )

    @staticmethod
    def load(
        path: Path,
    ) -> Transcript:

        with open(

            path,

            encoding="utf8",

        ) as f:

            data = json.load(f)

        transcript = Transcript(

            language=data["language"],

            duration=data["duration"],

        )

        for item in data["sentences"]:

            sentence = Sentence(

                id=item["id"],

                start=item["start"],

                end=item["end"],

                text=item["text"],

            )

            for w in item["words"]:

                sentence.words.append(

                    Word(

                        text=w["text"],

                        start=w["start"],

                        end=w["end"],

                    )

                )

            transcript.sentences.append(sentence)

        return transcript