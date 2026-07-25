"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Story Ranker Test
==================================================
"""

from pathlib import Path

from narrative.story_ranker import StoryRanker
from narrative.io.story_io import StoryIO


# ==================================================
# CONFIG
# ==================================================

PROJECT = Path(
    "projects/20260725_124828_Eps_1039_INDONESIA_TIDAK_PERNAH_DIJAJAH_BELANDA!!_JADI_SIAPA"
)

INPUT = PROJECT / "stories.json"

OUTPUT = PROJECT / "ranked_stories.json"


# ==================================================
# TEST
# ==================================================

def test_story_ranker():

    print()

    print("=" * 60)
    print("Story Ranker")
    print("=" * 60)

    stories = StoryIO.load(INPUT)

    print(f"Loaded Stories : {len(stories)}")

    ranker = StoryRanker()

    stories = ranker.rank(stories)

    print()

    print("Top Stories")

    print("-" * 60)

    for story in stories[:10]:

        print(
            f"Story #{story.id:02d}"
        )

        print(
            f"Score        : {story.score:.1f}"
        )

        print(
            f"Hook         : {story.hook_score:.1f}"
        )

        print(
            f"Conflict     : {story.conflict_score:.1f}"
        )

        print(
            f"Ending       : {story.ending_score:.1f}"
        )

        print(
            f"Engagement   : {story.engagement_score:.1f}"
        )

        print(
            f"Duration     : {story.duration:.1f}"
        )

        print(
            story.text[:120]
        )

        print("-" * 60)

    StoryIO.save(

        OUTPUT,

        stories

    )

    print()

    print("Saved :")

    print(OUTPUT)

    print("=" * 60)

    assert len(stories) > 0

    assert OUTPUT.exists()