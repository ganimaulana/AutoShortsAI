"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

AI Clip Domain Model
==================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class AIClip:
    """
    Raw clip recommendation returned by AI.
    """

    title: str

    reason: str

    segment_ids: list[int]