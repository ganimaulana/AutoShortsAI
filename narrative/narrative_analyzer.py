"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Narrative Analyzer
==================================================
"""

from domain.story import Story

from narrative.detectors.hook_detector import HookDetector


class NarrativeAnalyzer:
    """
    Menjalankan seluruh detector terhadap sebuah Story.
    """

    def __init__(self):

        self.detectors = [

            HookDetector(),

        ]

    # -------------------------------------------------

    def analyze(
        self,
        story: Story,
    ) -> Story:

        story.clear_detectors()

        for detector in self.detectors:

            if not detector.enabled:
                continue

            result = detector(story)

            story.add_detector_result(result)

        return story

    # -------------------------------------------------

    def analyze_all(
        self,
        stories: list[Story],
    ) -> list[Story]:

        for story in stories:

            self.analyze(story)

        return stories