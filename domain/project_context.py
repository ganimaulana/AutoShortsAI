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
from typing import List, Dict, Any

from domain.story import Story
from domain.timeline import TimelineClip


@dataclass(slots=True)
class ProjectContext:
    """
    Shared object passed between all engines.

    Every engine receives ProjectContext,
    modifies it,
    then returns it.
    """

    # =================================================
    # Project
    # =================================================

    project_path: Path | None = None

    # =================================================
    # Source
    # =================================================

    url: str = ""

    metadata: Dict[str, Any] = field(default_factory=dict)

    video_path: Path | None = None

    # =================================================
    # Transcript
    # =================================================

    transcript: Dict[str, Any] = field(default_factory=dict)

    # =================================================
    # Narrative
    # =================================================

    stories: List[Story] = field(default_factory=list)

    # =================================================
    # Timeline
    # =================================================

    timeline: List[TimelineClip] = field(default_factory=list)

    # =================================================
    # Clips
    # =================================================

    clips: List[Path] = field(default_factory=list)