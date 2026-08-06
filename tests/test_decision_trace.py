import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from application.scoring.decision_trace import DecisionTrace, DecisionStep

def test_decision_trace_steps():
    trace = DecisionTrace()
    step1 = DecisionStep("stage1", {"in": 1}, {"out": 2}, "expl1")
    step2 = DecisionStep("stage2", {"in": 2}, {"out": 3}, "expl2")
    
    trace.add_step(step1)
    trace.add_step(step2)
    
    assert len(trace.steps) == 2
    assert trace.steps[0] == step1
    assert trace.steps[1] == step2
    assert trace.steps[0].stage == "stage1"
    assert trace.steps[1].stage == "stage2"

def test_decision_trace_serialization():
    trace = DecisionTrace()
    step1 = DecisionStep("stage1", {"in": 1}, {"out": 2}, "expl1")
    trace.add_step(step1)
    
    data = trace.to_dict()
    assert data["steps"][0]["stage"] == "stage1"
    assert data["steps"][0]["explanation"] == "expl1"
    assert data["steps"][0]["input_summary"] == {"in": 1}
    assert data["steps"][0]["output_summary"] == {"out": 2}
