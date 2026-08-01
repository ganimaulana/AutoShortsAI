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
    """
    Hasil analisis dari sebuah detector.

    Contoh:
        HookDetector
        EmotionDetector
        ConflictDetector
        EndingDetector
    """

    # Nama detector
    detector: str

    # Nilai 0 - 100
    score: float

    # Tingkat keyakinan detector (0.0 - 1.0)
    confidence: float = 1.0

    # Kalimat atau kata yang menjadi alasan detector
    matches: list[str] = field(default_factory=list)

    # Penjelasan singkat
    reason: str = ""

    def to_dict(self) -> dict:

        return {

            "detector": self.detector,

            "score": self.score,

            "confidence": self.confidence,

            "matches": self.matches,

            "reason": self.reason,

        }