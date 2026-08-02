from domain.transcript.models import (
    Transcript,
    Chapter,
    Sentence,
)


class TopicDetector:

    """
    Membagi transcript menjadi beberapa chapter.

    V1:
    - Maksimal 90 detik
    - Maksimal 12 sentence
    """

    MAX_DURATION = 90
    MAX_SENTENCE = 12

    def run(
        self,
        transcript: Transcript,
    ) -> Transcript:

        transcript.chapters.clear()

        chapter = []

        chapter_start = None

        chapter_id = 1

        for sentence in transcript.sentences:

            if chapter_start is None:

                chapter_start = sentence.start

            chapter.append(sentence)

            duration = sentence.end - chapter_start

            if (

                duration >= self.MAX_DURATION

                or

                len(chapter) >= self.MAX_SENTENCE

            ):

                transcript.chapters.append(

                    Chapter(

                        id=chapter_id,

                        start=chapter[0].start,

                        end=chapter[-1].end,

                        sentences=chapter.copy(),

                    )

                )

                chapter_id += 1

                chapter = []

                chapter_start = None

        if chapter:

            transcript.chapters.append(

                Chapter(

                    id=chapter_id,

                    start=chapter[0].start,

                    end=chapter[-1].end,

                    sentences=chapter.copy(),

                )

            )

        return transcript