"""
==================================================
AutoShortsAI
Highlight Detector Test
==================================================
"""

from pathlib import Path

from narrative.highlight_detector import detect_highlights


def test_highlight_detector():

    project = Path("temp/test_project")

    transcript = project / "transcript.json"

    assert transcript.exists(), (
        "transcript.json belum ada.\n"
        "Jalankan test_transcriber.py terlebih dahulu."
    )

    output = detect_highlights(project)

    assert output.exists()

    print()

    print("==========================")

    print("Highlight berhasil dibuat")

    print(output)

    print("==========================")


if __name__ == "__main__":

    test_highlight_detector()