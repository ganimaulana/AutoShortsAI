"""
==================================================
Virality Detector
==================================================
"""

from .base_detector import BaseDetector


KEYWORDS = [

    "viral",
    "heboh",
    "jutaan",
    "trending",
    "shock",
    "terbongkar",
    "menggemparkan",
    "menghebohkan"

]


class ViralityDetector(BaseDetector):

    name = "Virality"

    weight = 18

    def score(self, story):

        text = story.text.lower()

        total = 0

        for word in KEYWORDS:

            if word in text:

                total += 1

        return total * self.weight