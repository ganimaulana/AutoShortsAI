"""
==================================================
Authority Detector
==================================================
"""

from .base_detector import BaseDetector


KEYWORDS = [

    "dokter",
    "profesor",
    "ilmuwan",
    "peneliti",
    "presiden",
    "ahli",
    "universitas",
    "penelitian",
    "riset",
    "laporan"

]


class AuthorityDetector(BaseDetector):

    name = "Authority"

    weight = 12

    def score(self, story):

        text = story.text.lower()

        score = 0

        for word in KEYWORDS:

            if word in text:

                score += 1

        return score * self.weight