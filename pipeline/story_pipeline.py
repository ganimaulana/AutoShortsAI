from __future__ import annotations

import logging

from application.story.sentence_splitter import SentenceSplitter
from application.story.sentence_feature_extractor import SentenceFeatureExtractor
from application.story.story_analyzer import StoryAnalyzer
from application.candidate.story_candidate_builder import StoryCandidateBuilder
from application.feature.feature_extractor import FeatureExtractor
from application.scoring.scoring_engine import ScoringEngine
from application.ranking.ranking_engine import RankingEngine
from application.ranking.diversity_filter import DiversityFilter
from application.ranking.ranking_rules import RankingRules
from application.ranking.diversity_rules import DiversityRules
from domain.ranked_candidate import RankedCandidate
from domain.segment import Segment
from domain.scoring_profile import ScoringProfile

DEFAULT_DIVERSITY_RULES = DiversityRules(
    overlap_threshold=0.8,
    maximum_candidates=10,
)

class StoryPipeline:
    """Orchestrates the complete deterministic story pipeline."""

    def __init__(
        self,
        splitter: SentenceSplitter,
        sentence_feature_extractor: SentenceFeatureExtractor,
        analyzer: StoryAnalyzer,
        builder: StoryCandidateBuilder,
        feature_extractor: FeatureExtractor,
        scorer: ScoringEngine,
        ranking_engine: RankingEngine,
        diversity_filter: DiversityFilter,
    ) -> None:
        self.splitter = splitter
        self.sentence_feature_extractor = sentence_feature_extractor
        self.analyzer = analyzer
        self.builder = builder
        self.feature_extractor = feature_extractor
        self.scorer = scorer
        self.ranking_engine = ranking_engine
        self.diversity_filter = diversity_filter
        self.logger = logging.getLogger(__name__)

    def build_ranked_candidates(
        self,
        segments: list[Segment],
        scoring_profile: ScoringProfile,
        ranking_rules: RankingRules | None = None,
        diversity_rules: DiversityRules | None = None,
        enable_logging: bool = False,
    ) -> list[RankedCandidate]:
        
        sentences = self.splitter.split(segments)
        if enable_logging:
            self.logger.info("Sentences count: %d", len(sentences))

        features = self.sentence_feature_extractor.extract(sentences)
        story_segments = self.analyzer.analyze(features)
        if enable_logging:
            self.logger.info("Story segments count: %d", len(story_segments))
        
        # Build candidates
        candidate_matches = self.builder.build_matches(story_segments)
        if enable_logging:
            self.logger.info("Candidate matches count: %d", len(candidate_matches))
        
        # Score
        scored_candidates = []
        for match in candidate_matches:
            feature_vector = self.feature_extractor.extract(match.match)
            score = self.scorer.score(feature_vector, scoring_profile)
            scored_candidates.append((match.candidate, score))
        
        # Rank
        ranked_candidates = self.ranking_engine.rank(scored_candidates, ranking_rules)
        if enable_logging:
            self.logger.info("Ranked candidates count: %d", len(ranked_candidates))
        
        # Filter
        if diversity_rules is None:
            diversity_rules = DEFAULT_DIVERSITY_RULES
        final_candidates = self.diversity_filter.filter(ranked_candidates, diversity_rules)
        if enable_logging:
            self.logger.info("Final candidates count: %d", len(final_candidates))
        
        return final_candidates
