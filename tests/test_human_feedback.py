import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
import json
from application.evaluation.human_feedback import HumanFeedback, HumanFeedbackDataset

def test_add_feedback():
    dataset = HumanFeedbackDataset()
    feedback = HumanFeedback(1.0, 5.0, 5, True, "Good")
    dataset.add(feedback)
    assert dataset.all() == [feedback]

def test_multiple_feedback():
    dataset = HumanFeedbackDataset()
    f1 = HumanFeedback(1.0, 5.0, 5, True, "Good")
    f2 = HumanFeedback(5.0, 10.0, 3, False, "Okay")
    dataset.add(f1)
    dataset.add(f2)
    assert dataset.all() == [f1, f2]

def test_serialization():
    dataset = HumanFeedbackDataset()
    dataset.add(HumanFeedback(1.0, 5.0, 5, True, "Good"))
    
    data = dataset.to_dict()
    assert "feedback" in data
    assert len(data["feedback"]) == 1
    assert data["feedback"][0]["rating"] == 5

def test_deterministic_json():
    dataset = HumanFeedbackDataset()
    dataset.add(HumanFeedback(1.0, 5.0, 5, True, "Good"))
    
    json1 = dataset.to_json()
    json2 = dataset.to_json()
    assert json1 == json2
    
    parsed = json.loads(json1)
    assert parsed["feedback"][0]["candidate_start"] == 1.0
