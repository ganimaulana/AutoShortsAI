"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Boundary Detector
==================================================
"""

from domain.segment import Segment


BOUNDARY_WORDS = {

    "kenapa",
    "mengapa",
    "bagaimana",
    "ternyata",
    "nah",
    "jadi",
    "sekarang",
    "lalu",
    "kemudian",
    "fakta",
    "rahasia",
    "bayangkan",

}


class BoundaryDetector:

    def __init__(

        self,

        pause_threshold=2.5,

        score_threshold=30,

    ):

        self.pause_threshold = pause_threshold

        self.score_threshold = score_threshold

    # -------------------------------------------------

    def detect(

        self,

        segments: list[Segment],

    ) -> list[int]:

        if not segments:

            return []

        boundaries = [0]

        previous = segments[0]

        for index in range(1, len(segments)):

            current = segments[index]

            score = 0

            #
            # Pause
            #

            pause = current.start - previous.end

            if pause >= self.pause_threshold:

                score += 30

            #
            # Opening keyword
            #

            text = current.text.lower()

            for word in BOUNDARY_WORDS:

                if text.startswith(word):

                    score += 20

                    break

            #
            # Question
            #

            if "?" in current.text:

                score += 10

            #
            # Speaker change
            #

            if (

                previous.speaker

                and current.speaker

                and previous.speaker != current.speaker

            ):

                score += 25

            #
            # Save
            #

            if score >= self.score_threshold:

                boundaries.append(index)

            previous = current

        return boundaries