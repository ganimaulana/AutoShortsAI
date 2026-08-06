from __future__ import annotations
import json
from application.scoring.decision_trace import DecisionTrace

class ExplanationExporter:
    """Exports DecisionTrace to dictionary and JSON format."""

    def export_dict(self, trace: DecisionTrace) -> dict:
        return trace.to_dict()

    def export_json(self, trace: DecisionTrace, indent: int = 2) -> str:
        return json.dumps(self.export_dict(trace), indent=indent, sort_keys=False)
