"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Pipeline Integration Test
==================================================
"""

from pathlib import Path

from core.pipeline import Pipeline


# ==================================================
# Test Video
# ==================================================

TEST_URL = "https://www.youtube.com/watch?v=Frcu00VNXtE"


# ==================================================
# Pipeline
# ==================================================

def test_pipeline():

    pipeline = Pipeline()

    context = pipeline.run(TEST_URL)

    #
    # Context
    #

    assert context is not None

    #
    # Project
    #

    assert context.project_path.exists()

    #
    # Download
    #

    assert context.video_path.exists()

    #
    # Transcript
    #

    assert context.transcript is not None

    assert len(
        context.transcript["segments"]
    ) > 0

    #
    # Story
    #

    assert len(
        context.stories
    ) > 0

    #
    # Timeline
    #

    assert len(
        context.timeline
    ) > 0

    #
    # Clips
    #

    assert len(
        context.clips
    ) > 0

    for clip in context.clips:

        assert Path(clip).exists()

    print()

    print("=" * 50)

    print("Pipeline Integration Test PASSED")

    print("=" * 50)

    print(f"Stories  : {len(context.stories)}")

    print(f"Timeline : {len(context.timeline)}")

    print(f"Clips    : {len(context.clips)}")

    print("=" * 50)