"""
==================================================
Curiosity Detector
==================================================
"""

from .base_detector import BaseDetector


KEYWORDS = [

    "kenapa",
    "mengapa",
    "bagaimana",
    "apa yang terjadi",
    "ternyata",
    "fakta",
    "alasan",
    "rahasia",
    "misteri"

]


class CuriosityDetector(BaseDetector):

    name = "Curiosity"

    weight = 18

    def score(self, story):

        text = story.text.lower()

        score = 0

        for word in KEYWORDS:

            if word in text:

                score += 1

        return score * self.weight