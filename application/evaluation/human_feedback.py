from __future__ import annotations
import json
from dataclasses import dataclass, field, asdict

@dataclass(frozen=True, slots=True)
class HumanFeedback:
    candidate_start: float
    candidate_end: float
    rating: int
    selected: bool
    notes: str

@dataclass
class HumanFeedbackDataset:
    feedback: list[HumanFeedback] = field(default_factory=list)

    def add(self, feedback: HumanFeedback) -> None:
        self.feedback.append(feedback)

    def all(self) -> list[HumanFeedback]:
        return list(self.feedback)

    def to_dict(self) -> dict:
        return {"feedback": [asdict(f) for f in self.feedback]}

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)
