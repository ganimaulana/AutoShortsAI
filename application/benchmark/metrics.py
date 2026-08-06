from __future__ import annotations
from domain.ranked_candidate import RankedCandidate

def calculate_iou(start1: float, end1: float, start2: float, end2: float) -> float:
    intersection = max(0.0, min(end1, end2) - max(start1, start2))
    union = (end1 - start1) + (end2 - start2) - intersection
    return intersection / union if union > 0.0 else 0.0

def calculate_precision_at_k(ranked_candidates: list[RankedCandidate], expected_candidates: list[tuple[float, float]], k: int, iou_threshold: float = 0.5) -> float:
    if not ranked_candidates or not expected_candidates:
        return 0.0
    
    top_k = ranked_candidates[:k]
    matches = 0
    for cand in top_k:
        if any(calculate_iou(cand.candidate.start, cand.candidate.end, exp[0], exp[1]) >= iou_threshold for exp in expected_candidates):
            matches += 1
    
    return matches / len(top_k)

def calculate_recall_at_k(ranked_candidates: list[RankedCandidate], expected_candidates: list[tuple[float, float]], k: int, iou_threshold: float = 0.5) -> float:
    if not expected_candidates:
        return 1.0
    
    top_k = ranked_candidates[:k]
    matches = 0
    for exp in expected_candidates:
        if any(calculate_iou(cand.candidate.start, cand.candidate.end, exp[0], exp[1]) >= iou_threshold for cand in top_k):
            matches += 1
            
    return matches / len(expected_candidates)
