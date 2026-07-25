"""
==================================================
Narrative Intelligence Engine (NIE)

Project Model
==================================================
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Project:

    root: Path

    @property
    def transcript(self):

        return self.root / "transcript.json"

    @property
    def stories(self):

        return self.root / "stories.json"

    @property
    def ranked(self):

        return self.root / "ranked_stories.json"

    @property
    def timeline(self):

        return self.root / "timeline.json"

    @property
    def video(self):

        return self.root / "original.mp4"

    @property
    def clips(self):

        return self.root / "clips"

    @property
    def subtitles(self):

        return self.root / "subtitles"