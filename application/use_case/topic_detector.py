from __future__ import annotations

from domain.transcript.models import (
    Chapter,
    Transcript,
)


class TopicDetector:
    """
    Rule Based Topic Detector V1

    Rules:

    - Maksimal 90 detik
    - Maksimal 12 sentence
    - Silence > 2.5 detik = chapter baru
    """

    MAX_DURATION = 90.0

    MAX_SENTENCE = 12

    SILENCE_THRESHOLD = 2.5

    def run(
        self,
        transcript: Transcript,
    ) -> Transcript:

        transcript.chapters.clear()

        if not transcript.sentences:
            return transcript

        current = []

        chapter_id = 1

        chapter_start = transcript.sentences[0].start

        previous = None

        for sentence in transcript.sentences:

            create_new = False

            if previous:

                silence = (
                    sentence.start -
                    previous.end
                )

                if silence >= self.SILENCE_THRESHOLD:
                    create_new = True

            duration = (
                sentence.end -
                chapter_start
            )

            if duration >= self.MAX_DURATION:
                create_new = True

            if len(current) >= self.MAX_SENTENCE:
                create_new = True

            if create_new:

                transcript.chapters.append(

                    Chapter(

                        id=chapter_id,

                        start=current[0].start,

                        end=current[-1].end,

                        sentences=current.copy(),

                    )

                )

                chapter_id += 1

                current.clear()

                chapter_start = sentence.start

            current.append(sentence)

            previous = sentence

        if current:

            transcript.chapters.append(

                Chapter(

                    id=chapter_id,

                    start=current[0].start,

                    end=current[-1].end,

                    sentences=current.copy(),

                )

            )

        return transcript