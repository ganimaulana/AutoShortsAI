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


class BaseDetector(ABC):
    """
    Base class for all narrative detectors.
    """

    name = "Detector"

    weight = 1.0

    @abstractmethod
    def score(
        self,
        story: Story,
    ) -> float:
        """
        Return score contribution.

        Must return 0.0 or higher.
        """
        raise NotImplementedError