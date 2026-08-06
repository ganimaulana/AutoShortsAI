import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import json
import pytest
from application.scoring.decision_trace import DecisionTrace, DecisionStep
from application.scoring.explainability_export import ExplanationExporter

def test_export_empty():
    exporter = ExplanationExporter()
    trace = DecisionTrace()
    data = exporter.export_dict(trace)
    assert data == {"steps": []}
    assert exporter.export_json(trace, indent=None) == json.dumps(data)

def test_export_single_step():
    exporter = ExplanationExporter()
    trace = DecisionTrace()
    trace.add_step(DecisionStep("Stage", {"in": 1}, {"out": 2}, "Expl"))
    data = exporter.export_dict(trace)
    assert len(data["steps"]) == 1
    assert exporter.export_json(trace, indent=None) == json.dumps(data)

def test_export_multiple_steps():
    exporter = ExplanationExporter()
    trace = DecisionTrace()
    trace.add_step(DecisionStep("Stage1", {"in": 1}, {"out": 2}, "Expl1"))
    trace.add_step(DecisionStep("Stage2", {"in": 3}, {"out": 4}, "Expl2"))
    data = exporter.export_dict(trace)
    assert len(data["steps"]) == 2
    assert exporter.export_json(trace, indent=None) == json.dumps(data)
    assert data["steps"][0]["stage"] == "Stage1"
    assert data["steps"][1]["stage"] == "Stage2"

def test_export_determinism():
    exporter = ExplanationExporter()
    trace = DecisionTrace()
    trace.add_step(DecisionStep("Stage", {"k": "v"}, {}, "Expl"))
    
    json1 = exporter.export_json(trace)
    json2 = exporter.export_json(trace)
    assert json1 == json2
