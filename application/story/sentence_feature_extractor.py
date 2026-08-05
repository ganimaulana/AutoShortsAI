from __future__ import annotations

from dataclasses import dataclass, field

from domain.story_intelligence import Sentence, StorySegmentType

from application.story import story_rules


@dataclass(slots=True)
class SentenceFeature:
    sentence_id: int
    text: str
    start: float
    end: float
    index: int
    total_sentences: int
    word_count: int
    lower_text: str
    is_question: bool = False
    is_early: bool = False
    is_late: bool = False
    matched_types: list[StorySegmentType] = field(default_factory=list)
    matched_terms: dict[StorySegmentType, list[str]] = field(default_factory=dict)

    @property
    def duration(self) -> float:
        return self.end - self.start


class SentenceFeatureExtractor:
    """Extracts deterministic sentence features from normalized sentences."""

    def extract(self, sentences: list[Sentence]) -> list[SentenceFeature]:
        total = len(sentences)
        features: list[SentenceFeature] = []

        for index, sentence in enumerate(sentences):
            lower_text = sentence.text.lower()
            matched_terms = self._match_terms(lower_text)
            matched_types = list(matched_terms)
            is_question = self._is_question(sentence.text, lower_text)
            is_early = index < story_rules.EARLY_SENTENCE_LIMIT
            is_late = self._is_late(index, total)

            if is_question:
                self._add_type(
                    matched_types,
                    matched_terms,
                    StorySegmentType.QUESTION,
                    "?",
                )

            if is_early and StorySegmentType.QUESTION in matched_types:
                self._add_type(
                    matched_types,
                    matched_terms,
                    StorySegmentType.HOOK,
                    "early question",
                )

            if is_early and StorySegmentType.HOOK in matched_types:
                self._add_type(
                    matched_types,
                    matched_terms,
                    StorySegmentType.HOOK,
                    "early hook",
                )

            if is_late and StorySegmentType.ENDING in matched_types:
                self._add_type(
                    matched_types,
                    matched_terms,
                    StorySegmentType.ENDING,
                    "late ending",
                )

            if not matched_types:
                matched_types.append(StorySegmentType.UNKNOWN)

            features.append(
                SentenceFeature(
                    sentence_id=sentence.id,
                    text=sentence.text,
                    start=sentence.start,
                    end=sentence.end,
                    index=index,
                    total_sentences=total,
                    word_count=len(sentence.text.split()),
                    lower_text=lower_text,
                    is_question=is_question,
                    is_early=is_early,
                    is_late=is_late,
                    matched_types=matched_types,
                    matched_terms=matched_terms,
                )
            )

        return features

    @staticmethod
    def _match_terms(
        lower_text: str,
    ) -> dict[StorySegmentType, list[str]]:
        matched_terms: dict[StorySegmentType, list[str]] = {}

        for segment_type, patterns in story_rules.PATTERNS_BY_TYPE.items():
            matches = [
                pattern
                for pattern in patterns
                if pattern in lower_text
            ]

            if matches:
                matched_terms[segment_type] = matches

        return matched_terms

    @staticmethod
    def _is_question(
        text: str,
        lower_text: str,
    ) -> bool:
        if text.strip().endswith("?"):
            return True

        return any(
            lower_text.startswith(pattern)
            for pattern in story_rules.QUESTION_PATTERNS
        )

    @staticmethod
    def _is_late(
        index: int,
        total: int,
    ) -> bool:
        if total <= 0:
            return False

        return index >= int(total * story_rules.ENDING_POSITION_RATIO)

    @staticmethod
    def _add_type(
        matched_types: list[StorySegmentType],
        matched_terms: dict[StorySegmentType, list[str]],
        segment_type: StorySegmentType,
        term: str,
    ) -> None:
        if segment_type not in matched_types:
            matched_types.append(segment_type)

        terms = matched_terms.setdefault(segment_type, [])

        if term not in terms:
            terms.append(term)
