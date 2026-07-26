"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Timeline Builder Test
==================================================
"""

from pathlib import Path

from narrative.story_ranker import StoryRanker
from narrative.timeline_builder import TimelineBuilder

from narrative.io.story_io import StoryIO
from narrative.io.timeline_io import TimelineIO


PROJECT = Path(
    "projects/20260725_124828_Eps_1039_INDONESIA_TIDAK_PERNAH_DIJAJAH_BELANDA!!_JADI_SIAPA"
)

INPUT = PROJECT / "stories.json"

OUTPUT = PROJECT / "timeline.json"


def test_timeline_builder():

    print()

    print("=" * 60)
    print("Timeline Builder")
    print("=" * 60)

    stories = StoryIO.load(INPUT)

    ranker = StoryRanker()

    stories = ranker.rank(stories)

    builder = TimelineBuilder()

    clips = builder.build(stories)

    print()

    print(f"Stories : {len(stories)}")

    print(f"Clips   : {len(clips)}")

    print()

    print("-" * 60)

    for clip in clips:

        print(

            f"Clip #{clip.clip_id:02d}"

        )

        print(

            f"Story      : {clip.story_id}"

        )

        print(

            f"Score      : {clip.score:.1f}"

        )

        print(

            f"Start      : {clip.start:.2f}"

        )

        print(

            f"End        : {clip.end:.2f}"

        )

        print(

            f"Duration   : {clip.duration:.2f}"

        )

        print("-" * 60)

    TimelineIO.save(

        OUTPUT,

        clips

    )

    print()

    print("Saved :")

    print(OUTPUT)

    print("=" * 60)

    assert len(clips) > 0

    assert OUTPUT.exists()