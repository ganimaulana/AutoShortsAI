from __future__ import annotations

from domain.story_intelligence import StorySegment, StorySegmentType

from application.story import story_rules
from application.story.sentence_feature_extractor import SentenceFeature


class StoryAnalyzer:
    """Groups sentence features into deterministic story segments."""

    def analyze(self, features: list[SentenceFeature]) -> list[StorySegment]:
        story_segments: list[StorySegment] = []
        current_features: list[SentenceFeature] = []
        current_primary_type: StorySegmentType | None = None

        for feature in features:
            primary_type = self._select_primary_type(feature.matched_types)

            if current_primary_type is not None and primary_type != current_primary_type:
                story_segments.append(
                    self._build_story_segment(
                        len(story_segments) + 1,
                        current_primary_type,
                        current_features,
                    )
                )
                current_features = []

            current_primary_type = primary_type
            current_features.append(feature)

        if current_features and current_primary_type is not None:
            story_segments.append(
                self._build_story_segment(
                    len(story_segments) + 1,
                    current_primary_type,
                    current_features,
                )
            )

        return story_segments

    @staticmethod
    def _select_primary_type(
        matched_types: list[StorySegmentType],
    ) -> StorySegmentType:
        if not matched_types:
            return StorySegmentType.UNKNOWN

        for segment_type in story_rules.PRIMARY_TYPE_PRIORITY:
            if segment_type in matched_types:
                return segment_type

        return StorySegmentType.UNKNOWN

    def _build_story_segment(
        self,
        segment_id: int,
        primary_type: StorySegmentType,
        features: list[SentenceFeature],
    ) -> StorySegment:
        return StorySegment(
            id=segment_id,
            primary_type=primary_type,
            types=self._merge_types(features),
            start=features[0].start,
            end=features[-1].end,
            text=" ".join(feature.text for feature in features),
            sentence_ids=[
                feature.sentence_id
                for feature in features
            ],
        )

    @staticmethod
    def _merge_types(
        features: list[SentenceFeature],
    ) -> list[StorySegmentType]:
        merged: list[StorySegmentType] = []

        for segment_type in story_rules.PRIMARY_TYPE_PRIORITY:
            if any(segment_type in feature.matched_types for feature in features):
                merged.append(segment_type)

        if not merged:
            merged.append(StorySegmentType.UNKNOWN)

        return merged
