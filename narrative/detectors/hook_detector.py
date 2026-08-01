"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Hook Detector
==================================================
"""

from narrative.detectors.base_detector import BaseDetector
from domain.detector_result import DetectorResult
from domain.story import Story


class HookDetector(BaseDetector):

    name = "Hook"

    weight = 1.0

    KEYWORDS = {

        "secret": 25,
        "truth": 20,
        "finally": 15,
        "suddenly": 20,
        "watch": 15,
        "look": 10,
        "listen": 10,
        "imagine": 20,
        "warning": 20,
        "never": 15,
        "always": 10,
        "nobody": 25,
        "everyone": 10,
        "everything": 20,
        "nothing": 15,
        "impossible": 25,
        "shocking": 30,
        "unbelievable": 30,
        "can't believe": 35,
        "changed my life": 35,
        "lost everything": 40,
    }

    def analyze(
        self,
        story: Story,
    ) -> DetectorResult:

        text = story.text.lower()

        score = 0

        matches = []

        for keyword, value in self.KEYWORDS.items():

            if keyword in text:

                score += value

                matches.append(keyword)

        score = min(score, 100)

        if score >= 80:

            reason = "Excellent hook"

        elif score >= 60:

            reason = "Strong hook"

        elif score >= 40:

            reason = "Average hook"

        else:

            reason = "Weak hook"

        return DetectorResult(

            detector=self.name,

            score=score,

            confidence=1.0,

            matches=matches,

            reason=reason,

        )