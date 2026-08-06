from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass(frozen=True, slots=True)
class DecisionStep:
    stage: str
    input_summary: dict[str, Any]
    output_summary: dict[str, Any]
    explanation: str

@dataclass
class DecisionTrace:
    steps: list[DecisionStep] = field(default_factory=list)

    def add_step(self, step: DecisionStep) -> None:
        self.steps.append(step)

    def to_dict(self) -> dict[str, Any]:
        return {
            "steps": [
                {
                    "stage": step.stage,
                    "input_summary": step.input_summary,
                    "output_summary": step.output_summary,
                    "explanation": step.explanation,
                }
                for step in self.steps
            ]
        }
