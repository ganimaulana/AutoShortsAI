"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Project Context
==================================================
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from domain.segment import Segment
from domain.story import Story
from domain.timeline import TimelineClip


@dataclass(slots=True)
class ProjectContext:
    """
    Shared object passed between all engines.
    """

    # =================================================
    # Project
    # =================================================

    project_path: Path | None = None

    # =================================================
    # Source
    # =================================================

    url: str = ""

    metadata: dict[str, Any] = field(default_factory=dict)

    video_path: Path | None = None

    # =================================================
    # Transcript
    # =================================================

    transcript: list[Segment] = field(default_factory=list)

    # =================================================
    # Narrative
    # =================================================

    stories: list[Story] = field(default_factory=list)

    # =================================================
    # Timeline
    # =================================================

    timeline: list[TimelineClip] = field(default_factory=list)

    # =================================================
    # Clips
    # =================================================

    clips: list[Path] = field(default_factory=list)

    # =================================================
    # Pipeline
    # =================================================

    status: str = ""

    progress: float = 0.0

    # =================================================
    # Helper Properties
    # =================================================

    @property
    def transcript_path(self):

        if self.project_path is None:
            return None

        return self.project_path / "transcript.json"

    @property
    def stories_path(self):

        if self.project_path is None:
            return None

        return self.project_path / "stories.json"

    @property
    def ranked_stories_path(self):

        if self.project_path is None:
            return None

        return self.project_path / "ranked_stories.json"

    @property
    def timeline_path(self):

        if self.project_path is None:
            return None

        return self.project_path / "timeline.json"

    @property
    def clips_dir(self):

        if self.project_path is None:
            return None

        return self.project_path / "clips"

    @property
    def output_dir(self):

        if self.project_path is None:
            return None

        return self.project_path / "output"