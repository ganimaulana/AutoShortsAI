from __future__ import annotations
from pipeline.story_pipeline import StoryPipeline
from domain.segment import Segment
from domain.scoring_profile import ScoringProfile
from application.ranking.ranking_rules import RankingRules
from application.ranking.diversity_rules import DiversityRules
from application.benchmark.metrics import calculate_precision_at_k, calculate_recall_at_k
from dataclasses import dataclass

@dataclass
class BenchmarkResult:
    precision_at_k: float
    recall_at_k: float

class BenchmarkRunner:
    def __init__(self, pipeline: StoryPipeline):
        self.pipeline = pipeline

    def run(
        self,
        segments: list[Segment],
        expected_candidates: list[tuple[float, float]],
        scoring_profile: ScoringProfile,
        ranking_rules: RankingRules | None = None,
        diversity_rules: DiversityRules | None = None,
        k: int = 5
    ) -> BenchmarkResult:
        ranked_candidates = self.pipeline.build_ranked_candidates(
            segments,
            scoring_profile,
            ranking_rules,
            diversity_rules
        )
        
        precision = calculate_precision_at_k(ranked_candidates, expected_candidates, k)
        recall = calculate_recall_at_k(ranked_candidates, expected_candidates, k)
        
        return BenchmarkResult(precision_at_k=precision, recall_at_k=recall)
