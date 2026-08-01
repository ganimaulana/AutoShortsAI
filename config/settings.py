"""
==================================================
AutoShortsAI

Global Settings
==================================================
"""

from dataclasses import dataclass, field


# ==================================================
# Whisper
# ==================================================

@dataclass(slots=True)
class WhisperSettings:

    model: str = "base"

    device: str = "cpu"

    compute_type: str = "int8"


# ==================================================
# Timeline
# ==================================================

@dataclass(slots=True)
class TimelineSettings:

    max_clips: int = 5

    pre_roll: float = 0.5

    post_roll: float = 0.5


# ==================================================
# Subtitle
# ==================================================

@dataclass(slots=True)
class SubtitleSettings:

    font_size: int = 54

    margin_bottom: int = 180


# ==================================================
# Global Config
# ==================================================

@dataclass(slots=True)
class Settings:

    whisper: WhisperSettings = field(
        default_factory=WhisperSettings
    )

    timeline: TimelineSettings = field(
        default_factory=TimelineSettings
    )

    subtitle: SubtitleSettings = field(
        default_factory=SubtitleSettings
    )

settings = Settings()