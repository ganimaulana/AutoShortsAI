"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Boundary Detector Test
==================================================
"""

from narrative.boundary_detector import BoundaryDetector
from narrative.io.transcript_io import TranscriptIO

from tests.sample_project import TRANSCRIPT


def test_boundary_detector():

    #
    # Check sample project
    #

    assert TRANSCRIPT.exists(), (
        f"Transcript not found:\n{TRANSCRIPT}"
    )

    #
    # Load transcript
    #

    transcript = TranscriptIO.load(
        TRANSCRIPT
    )

    #
    # Detect
    #

    detector = BoundaryDetector()

    boundaries = detector.detect(
        transcript
    )

    #
    # Output
    #

    print()

    print("=" * 60)
    print("Boundary Detector")
    print("=" * 60)

    print()

    print(f"Segments  : {len(transcript)}")

    print(f"Boundaries: {len(boundaries)}")

    print()

    for index in boundaries:

        seg = transcript[index]

        print(
            f"[{index:03d}] "
            f"{seg.start:8.2f}s"
        )

        print(
            seg.text
        )

        print("-" * 60)

    #
    # Validation
    #

    assert len(boundaries) > 0