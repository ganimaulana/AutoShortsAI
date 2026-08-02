from dataclasses import dataclass


@dataclass(slots=True)
class ClipCandidate:

    start: float
    end: float

    score: float

    reason: str

    chapter_id: int

    reviewed: bool = False


@dataclass(slots=True)
class ClipReview:

    approved: bool

    hook: int

    emotion: int

    clarity: int

    retention: int

    final_score: int

    feedback: str