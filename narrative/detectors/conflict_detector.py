"""
==================================================
Conflict Detector
==================================================
"""

from .base_detector import BaseDetector


KEYWORDS = [

    "vs",
    "melawan",
    "konflik",
    "perang",
    "serang",
    "bertengkar",
    "menolak",
    "krisis",
    "gagal",
    "kalah",
    "menang"

]


class ConflictDetector(BaseDetector):

    name = "Conflict"

    weight = 20

    def score(self, story):

        text = story.text.lower()

        total = 0

        for word in KEYWORDS:

            if word in text:

                total += 1

        return total * self.weight