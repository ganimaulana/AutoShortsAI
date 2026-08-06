from __future__ import annotations
from dataclasses import dataclass
from domain.ranked_candidate import RankedCandidate
from application.evaluation.human_feedback import HumanFeedbackDataset
from application.benchmark.metrics import calculate_iou

@dataclass(frozen=True, slots=True)
class EvaluationResult:
    total_candidates: int
    matched_candidates: int
    average_rating: float
    selection_accuracy: float

class EvaluationEngine:
    """Compares AI ranked candidates against human feedback."""

    def evaluate(
        self,
        ranked_candidates: list[RankedCandidate],
        feedback_dataset: HumanFeedbackDataset,
        iou_threshold: float = 0.5
    ) -> EvaluationResult:
        
        all_feedback = feedback_dataset.all()
        selected_feedback = [f for f in all_feedback if f.selected]
        
        if not selected_feedback:
            return EvaluationResult(
                total_candidates=len(ranked_candidates),
                matched_candidates=0,
                average_rating=0.0,
                selection_accuracy=0.0
            )

        matched_feedback = []
        for feedback in selected_feedback:
            for candidate in ranked_candidates:
                iou = calculate_iou(
                    feedback.candidate_start, feedback.candidate_end,
                    candidate.candidate.start, candidate.candidate.end
                )
                if iou >= iou_threshold:
                    matched_feedback.append(feedback)
                    break
        
        matched_count = len(matched_feedback)
        total_selected = len(selected_feedback)
        
        average_rating = (
            sum(f.rating for f in matched_feedback) / matched_count
            if matched_count > 0 else 0.0
        )
        
        selection_accuracy = matched_count / total_selected
        
        return EvaluationResult(
            total_candidates=len(ranked_candidates),
            matched_candidates=matched_count,
            average_rating=average_rating,
            selection_accuracy=selection_accuracy
        )
