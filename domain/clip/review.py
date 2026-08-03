from dataclasses import dataclass
from dataclasses import dataclass, field

from domain.clip.metrics import ClipMetrics
from domain.clip.review import ClipReview


@dataclass(slots=True)
class ClipReview:

    approved: bool = False

    score: int = 0

    hook: int = 0

    emotion: int = 0

    retention: int = 0

    clarity: int = 0

    title: str = ""

    reason: str = ""

@dataclass(slots=True)
class ClipCandidate:

    start: float

    end: float

    chapter_id: int

    summary: str = ""

    metrics: ClipMetrics = field(
        default_factory=ClipMetrics
    )

    review: ClipReview = field(
        default_factory=ClipReview
    )