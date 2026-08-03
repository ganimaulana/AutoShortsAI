"""
==================================================
AutoShortsAI

Workflow Stages
==================================================
"""

from enum import Enum


class WorkflowStage(str, Enum):

    PENDING = "pending"

    DOWNLOAD = "download"

    TRANSCRIBE = "transcribe"

    ANALYZE = "analyze"

    STORY = "story"

    TIMELINE = "timeline"

    SUBTITLE = "subtitle"

    RENDER = "render"

    EXPORT = "export"

    FINISHED = "finished"

    FAILED = "failed"