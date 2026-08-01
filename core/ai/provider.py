from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def analyze(self, transcript: str) -> dict:
        """
        Analyze transcript and return JSON.
        """
        raise NotImplementedError