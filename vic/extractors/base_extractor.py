"""
===========================================================
AutoShortsAI
Video Intelligence Core (VIC)

Base Feature Extractor
===========================================================

Abstract interface for all AI feature extractors.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from ..sentence_features import SentenceFeatures


class BaseExtractor(ABC):
    """
    Base interface for all feature extractors.

    Every extractor must analyze a sentence and
    return the enriched SentenceFeatures object.
    """

    @abstractmethod
    async def extract(
        self,
        sentence: SentenceFeatures,
    ) -> SentenceFeatures:
        """
        Analyze one sentence.

        Parameters
        ----------
        sentence
            Sentence to analyze.

        Returns
        -------
        SentenceFeatures
            Same sentence enriched with extracted features.
        """
        raise NotImplementedError