from dataclasses import dataclass

@dataclass(slots=True)
class Candidate:
    """Represents a potential video clip candidate."""
    start: float
    end: float
    score: float = 0.0
    reason: str = ""
