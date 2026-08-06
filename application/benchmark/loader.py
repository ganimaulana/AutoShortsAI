from __future__ import annotations
import json
from pathlib import Path
from domain.segment import Segment

class BenchmarkLoader:
    @staticmethod
    def load_transcript(file_path: Path) -> list[Segment]:
        with open(file_path, "r") as f:
            data = json.load(f)
        return [Segment(id=item["id"], start=item["start"], end=item["end"], text=item["text"]) for item in data]

    @staticmethod
    def load_expected_candidates(file_path: Path) -> list[tuple[float, float]]:
        with open(file_path, "r") as f:
            data = json.load(f)
        return [(item["start"], item["end"]) for item in data]
