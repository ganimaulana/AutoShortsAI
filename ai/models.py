from dataclasses import dataclass, field


@dataclass(slots=True)
class ClipMetrics:

    duration: float = 0

    hook: float = 0

    emotion: float = 0

    retention: float = 0

    ending: float = 0

    silence: float = 0

    speaking_rate: float = 0

    subtitle_quality: float = 0

    technical: float = 0

    overall: float = 0


@dataclass(slots=True)
class ClipCandidate:

    start: float

    end: float

    chapter_id: int

    summary: str = ""

    metrics: ClipMetrics = field(
        default_factory=ClipMetrics
    )