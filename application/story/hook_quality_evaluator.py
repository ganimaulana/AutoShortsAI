from __future__ import annotations
from domain.story_intelligence import StorySegment, StorySegmentType

class HookQualityEvaluator:
    """Evaluates hook quality using deterministic story segment intelligence."""

    def evaluate(self, segments: list[StorySegment]) -> float:
        """Returns a normalized hook quality score (0-100)."""
        if not segments:
            return 0.0
        
        # Focus on the first segment (the potential hook)
        hook_segment = segments[0]
        score = 0.0
        
        if StorySegmentType.HOOK in hook_segment.types or hook_segment.primary_type == StorySegmentType.HOOK:
            score += 50.0
        if StorySegmentType.QUESTION in hook_segment.types or hook_segment.primary_type == StorySegmentType.QUESTION:
            score += 30.0
        if StorySegmentType.CONFLICT in hook_segment.types or hook_segment.primary_type == StorySegmentType.CONFLICT:
            score += 20.0
            
        return min(100.0, score)
