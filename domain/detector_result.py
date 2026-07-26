"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Detector Result
==================================================
"""

from dataclasses import dataclass, field


@dataclass(slots=True)
class DetectorResult:

    detector: str

    score: float

    matches: list[str] = field(default_factory=list)

    reason: str = ""