"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Clip Engine Test
==================================================
"""

from pathlib import Path

from core.clip_engine import ClipEngine

from narrative.io.timeline_io import TimelineIO


# ==================================================
# PROJECT
# ==================================================

PROJECT = Path(
    "projects/20260725_124828_Eps_1039_INDONESIA_TIDAK_PERNAH_DIJAJAH_BELANDA!!_JADI_SIAPA"
)

TIMELINE = PROJECT / "timeline.json"

OUTPUT = PROJECT / "clips"

VIDEO = PROJECT / "original.mp4"


# ==================================================
# TEST
# ==================================================

def test_clip_engine():

    print()

    print("=" * 60)
    print("Clip Engine")
    print("=" * 60)

    #
    # Pastikan video tersedia
    #

    assert VIDEO.exists(), (
        f"Video tidak ditemukan:\n{VIDEO}"
    )

    #
    # Load timeline
    #

    timeline = TimelineIO.load(
        TIMELINE
    )

    #
    # Generate clips
    #

    engine = ClipEngine()

    clips = engine.generate(

        video_path=VIDEO,

        timeline=timeline,

        output_dir=OUTPUT,

    )

    #
    # Result
    #

    print()

    print(f"Timeline : {len(timeline)}")

    print(f"Generated: {len(clips)}")

    print()

    print("-" * 60)

    for clip in clips:

        print(clip.name)

    print("-" * 60)

    print()

    print("Saved :")

    print(OUTPUT)

    print("=" * 60)

    #
    # Assertions
    #

    assert len(clips) == len(timeline)

    for clip in clips:

        assert clip.exists()