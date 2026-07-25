import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from narrative.io import TranscriptIO
from narrative.story_builder import StoryBuilder
from narrative.io import StoryIO

# =============================================

PROJECT = Path(
    "projects/20260725_124828_Eps_1039_INDONESIA_TIDAK_PERNAH_DIJAJAH_BELANDA!!_JADI_SIAPA"
)

TRANSCRIPT = PROJECT / "transcript.json"

STORIES = PROJECT / "stories.json"

# =============================================

segments = TranscriptIO.load(TRANSCRIPT)

builder = StoryBuilder()

stories = builder.build(segments)

StoryIO.save(
    STORIES,
    stories
)

print()

print("=" * 60)

print("Story Builder")

print("=" * 60)

print("Segments :", len(segments))

print("Stories  :", len(stories))

print("=" * 60)

for story in stories:

    print()

    print(f"Story #{story.id}")

    print(f"Duration : {story.duration:.2f}")

    print(f"Words    : {story.word_count}")

    print(story.text[:120])

    print("-" * 60)

print()

print("Saved :")

print(STORIES)