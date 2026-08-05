from pipeline.base_pipeline import PipelineStep, StepResult
from application.candidate.candidate_builder import CandidateBuilder
from pipeline.story_pipeline import StoryPipeline

# Dependencies for StoryPipeline
from application.story.sentence_splitter import SentenceSplitter
from application.story.sentence_feature_extractor import SentenceFeatureExtractor
from application.story.story_analyzer import StoryAnalyzer
from application.candidate.story_candidate_builder import StoryCandidateBuilder
from application.feature.feature_extractor import FeatureExtractor
from application.scoring.scoring_engine import ScoringEngine
from application.scoring.profile_registry import ProfileRegistry
from application.ranking.ranking_engine import RankingEngine
from application.ranking.diversity_filter import DiversityFilter
from application.ranking.diversity_rules import DiversityRules
from utils.logger import logger

DEFAULT_SCORING_PROFILE = "Storytelling"
DEFAULT_DIVERSITY_RULES = DiversityRules(
    overlap_threshold=0.8,
    maximum_candidates=10,
)

class CandidatePipeline(PipelineStep):
    """Pipeline step to generate and store clip candidates."""

    name = "Candidate"

    def __init__(
        self,
        legacy_builder: CandidateBuilder | None = None,
        story_pipeline: StoryPipeline | None = None,
        profile_registry: ProfileRegistry | None = None,
        use_story_pipeline: bool = False,
        strict_story_pipeline: bool = False,
    ) -> None:
        self.legacy_builder = legacy_builder or CandidateBuilder()
        self.story_pipeline = story_pipeline or StoryPipeline(
            splitter=SentenceSplitter(),
            sentence_feature_extractor=SentenceFeatureExtractor(),
            analyzer=StoryAnalyzer(),
            builder=StoryCandidateBuilder(),
            feature_extractor=FeatureExtractor(),
            scorer=ScoringEngine(),
            ranking_engine=RankingEngine(),
            diversity_filter=DiversityFilter(),
        )
        self.profile_registry = profile_registry or ProfileRegistry()
        self.use_story_pipeline = use_story_pipeline
        self.strict_story_pipeline = strict_story_pipeline

    def execute(self, job) -> StepResult:
        """Executes candidate generation and stores results in metadata."""
        segments = job.manifest.transcript_segments
        
        use_story = job.metadata.get("USE_STORY_PIPELINE", self.use_story_pipeline)
        strict_story = job.metadata.get("STRICT_STORY_PIPELINE", self.strict_story_pipeline)
        
        # Store (Candidate, Score) tuples to handle both paths uniformly
        prepared_candidates = []
        
        if use_story:
            try:
                # Retrieve rules from job metadata or use defaults/registry
                profile_name = job.metadata.get("SCORING_PROFILE", DEFAULT_SCORING_PROFILE)
                scoring_profile = self.profile_registry.get_profile(profile_name)
                ranking_rules = job.metadata.get("RANKING_RULES")
                diversity_rules = job.metadata.get("DIVERSITY_RULES", DEFAULT_DIVERSITY_RULES)
                
                ranked_candidates = self.story_pipeline.build_ranked_candidates(
                    segments,
                    scoring_profile,
                    ranking_rules,
                    diversity_rules,
                )
                
                prepared_candidates = [
                    (rc.candidate, rc.score.total_score) 
                    for rc in ranked_candidates
                ]
                
            except Exception as e:
                logger.exception("StoryPipeline failed")
                if strict_story:
                    raise
                
                # Fallback to legacy
                candidates = self.legacy_builder.build(segments)
                prepared_candidates = [(c, c.score) for c in candidates]
        else:
            candidates = self.legacy_builder.build(segments)
            prepared_candidates = [(c, c.score) for c in candidates]

        # TODO (Sprint 3):
        # Replace legacy metadata dictionaries with Manifest.candidates after downstream pipelines are migrated.
        job.metadata["approved_candidates"] = [
            {
                "id": i,
                "title": c.reason,
                "score": int(score),
                "start": c.start,
                "end": c.end,
            }
            for i, (c, score) in enumerate(prepared_candidates, start=1)
        ]

        return StepResult(
            success=True,
            message="Candidate generation completed"
        )
