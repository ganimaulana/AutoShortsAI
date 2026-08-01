"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Base Detector
==================================================
"""

from abc import ABC
from abc import abstractmethod

from domain.story import Story
from domain.detector_result import DetectorResult


class BaseDetector(ABC):
    """
    Base class untuk seluruh detector.

    Semua detector WAJIB mengembalikan DetectorResult,
    bukan float.
    """

    name = "Detector"

    weight = 1.0

    enabled = True

    @abstractmethod
    def analyze(
        self,
        story: Story,
    ) -> DetectorResult:
        """
        Jalankan analisis terhadap Story.

        Harus mengembalikan DetectorResult.
        """
        raise NotImplementedError

    def __call__(
        self,
        story: Story,
    ) -> DetectorResult:

        return self.analyze(story)