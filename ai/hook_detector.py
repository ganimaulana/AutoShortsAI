"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Hook Detector
==================================================
"""


class HookDetector:

    def __init__(self):

        self.keywords = [

            "suddenly",
            "finally",
            "watch",
            "look",
            "imagine",
            "secret",
            "truth",
            "nobody",
            "everything",
            "impossible",
            "warning",
            "lost",
            "shocking",
            "can't believe",

        ]

    # ==================================================

    def score(self, text):

        text = text.lower()

        score = 0

        for keyword in self.keywords:

            if keyword in text:

                score += 10

        return score

    # ==================================================

    def process(self, story):

        best_score = -1
        best_segment = None

        for segment in story.segments:

            score = self.score(segment.text)

            if score > best_score:

                best_score = score
                best_segment = segment

        story.hook_score = best_score

        story.hook_segment = best_segment

        return story