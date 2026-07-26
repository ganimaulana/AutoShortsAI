"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Base Engine
==================================================
"""

from abc import ABC
from abc import abstractmethod

from domain.project_context import ProjectContext


class BaseEngine(ABC):
    """
    Base class for every engine.
    """

    @abstractmethod
    def process(
        self,
        context: ProjectContext,
    ) -> ProjectContext:
        """
        Execute engine.

        Must return the updated ProjectContext.
        """
        raise NotImplementedError