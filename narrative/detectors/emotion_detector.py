"""
Emotion Detector
"""

from .base_detector import BaseDetector


WORDS = [

    "sedih",
    "marah",
    "bahagia",
    "menangis",
    "emosi",
    "kecewa",
    "bangga",
    "mengejutkan",
    "tragis",
    "heboh",

]


class EmotionDetector(BaseDetector):

    name = "Emotion"

    weight = 15

    def score(self, story):

        text = story.text.lower()

        total = 0

        for word in WORDS:

            if word in text:

                total += 1

        return total * self.weight