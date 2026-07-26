from pathlib import Path

from narrative.io.transcript_io import TranscriptIO

from media.subtitle_engine import SubtitleEngine


PROJECT = Path(
    "projects/20260725_124828_Eps_1039_INDONESIA_TIDAK_PERNAH_DIJAJAH_BELANDA!!_JADI_SIAPA"
)

VIDEO = PROJECT / "clips" / "clip001.mp4"

TRANSCRIPT = PROJECT / "transcript.json"

OUTPUT = PROJECT / "clips" / "clip001_subtitled.mp4"


def test_burn_subtitle():

    assert VIDEO.exists()
    assert TRANSCRIPT.exists()

    segments = TranscriptIO.load(
        TRANSCRIPT
    )

    engine = SubtitleEngine()

    output = engine.process(

        VIDEO,

        segments,

        OUTPUT,

    )

    assert output.exists()

    print()

    print("=" * 60)
    print("Subtitle Engine")
    print("=" * 60)
    print()

    print(output)

    print()

    print("=" * 60)