import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from application.scoring.decision_trace import DecisionTrace, DecisionStep
from application.scoring.explainability import CandidateExplanationBuilder

def test_explainability_empty_trace():
    builder = CandidateExplanationBuilder()
    trace = DecisionTrace()
    assert builder.build(trace) == "No decisions recorded."

def test_explainability_single_step():
    builder = CandidateExplanationBuilder()
    trace = DecisionTrace()
    trace.add_step(DecisionStep("Stage", {"key": "val"}, {"bonus_count": 1}, "Expl"))
    
    report = builder.build(trace)
    assert "Stage" in report
    assert "Key: val" in report
    assert "Applied 1 bonus(es)" in report
    assert "Expl" in report

def test_explainability_multiple_steps():
    builder = CandidateExplanationBuilder()
    trace = DecisionTrace()
    trace.add_step(DecisionStep("Stage 1", {"k1": "v1"}, {}, "Expl 1"))
    trace.add_step(DecisionStep("Stage 2", {"k2": "v2"}, {"total_score": 91.3}, "Expl 2"))
    
    report = builder.build(trace)
    assert report.count("↓") == 1
    assert "Stage 1" in report
    assert "Stage 2" in report
    assert "Expl 1" in report
    assert "Expl 2" in report
    assert "91.3" in report

def test_explainability_determinism():
    builder = CandidateExplanationBuilder()
    trace = DecisionTrace()
    trace.add_step(DecisionStep("Stage", {"k": "v"}, {}, "Expl"))
    
    report1 = builder.build(trace)
    report2 = builder.build(trace)
    assert report1 == report2
