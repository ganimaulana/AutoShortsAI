from collections import Counter
from domain.transcript.models import Transcript
from domain.features import ClipFeature


HOOK_WORDS = {
    "mengapa",
    "kenapa",
    "tahukah",
    "rahasia",
    "awas",
    "jangan",
    "ternyata",
    "bayangkan",
}

EMOTION_WORDS = {
    "menangis",
    "haru",
    "bahagia",
    "sedih",
    "marah",
    "subhanallah",
    "masyaallah",
}


class FeatureExtractor:

    def extract(
        self,
        transcript: Transcript,
    ) -> list[ClipFeature]:

        features = []

        for chapter in transcript.chapters:

            text = " ".join(
                s.text.lower()
                for s in chapter.sentences
            )

            words = text.split()

            counter = Counter(words)

            hook = sum(
                counter[w]
                for w in HOOK_WORDS
                if w in counter
            )

            emotion = sum(
                counter[w]
                for w in EMOTION_WORDS
                if w in counter
            )

            duration = chapter.end - chapter.start

            speaking_rate = (

                len(words)

                /

                max(duration,1)

            )

            features.append(

                ClipFeature(

                    start=chapter.start,

                    end=chapter.end,

                    duration=duration,

                    word_count=len(words),

                    sentence_count=len(chapter.sentences),

                    silence_duration=0,

                    speaking_rate=speaking_rate,

                    question_count=text.count("?"),

                    exclamation_count=text.count("!"),

                    emotion_keyword=emotion,

                    hook_keyword=hook,

                    ending_strength=0,

                )

            )

        return features