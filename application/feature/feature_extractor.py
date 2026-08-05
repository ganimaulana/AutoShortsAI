from __future__ import annotations

import logging

from application.candidate.story_candidate_builder import StoryPatternMatch
from application.feature import feature_rules
from domain.feature_vector import FeatureVector
from domain.story_intelligence import StorySegmentType

logger = logging.getLogger(__name__)


class FeatureExtractor:
    """Extracts deterministic feature vectors from story pattern matches."""

    def extract(self, match: StoryPatternMatch) -> FeatureVector:
        text = " ".join(
            segment.text.strip()
            for segment in match.matched_segments
            if segment.text.strip()
        )
        lower_text = text.lower()
        tokens = feature_rules.TOKEN_PATTERN.findall(lower_text)
        duration = self._duration(match)
        coverage = self._coverage(match)

        logger.debug(
            "Extracting features for pattern '%s' with %d matched segments.",
            match.pattern.name,
            len(match.matched_segments),
        )

        return FeatureVector(
            hook_strength=self._hook_strength(match, text, lower_text),
            curiosity=self._curiosity(text, lower_text),
            conflict=self._conflict(match, lower_text),
            emotion=self._emotion(text, lower_text, tokens),
            novelty=self._novelty(lower_text),
            ending_strength=self._ending_strength(match, lower_text),
            pacing=self._pacing(tokens, duration),
            people=self._people(text, lower_text),
            numbers=self._numbers(lower_text),
            question=self._question(text, lower_text),
            cta=self._cta(lower_text),
            duration=duration,
            coverage=coverage,
        )

    def _hook_strength(
        self,
        match: StoryPatternMatch,
        text: str,
        lower_text: str,
    ) -> float:
        signals = {
            "hook_phrase": self._contains_any(lower_text, feature_rules.HOOK_PHRASES),
            "question": self._question(text, lower_text) > 0.0,
            "hook_segment": self._has_segment_type(match, StorySegmentType.HOOK),
            "surprising_number": self._has_surprising_number(lower_text),
            "curiosity_phrase": self._contains_any(lower_text, feature_rules.CURIOSITY_PHRASES),
        }
        return self._weighted_sum(signals, feature_rules.HOOK_WEIGHTS)

    def _curiosity(self, text: str, lower_text: str) -> float:
        stripped_text = text.strip()
        signals = {
            "curiosity_phrase": self._contains_any(lower_text, feature_rules.CURIOSITY_PHRASES),
            "because": "because" in lower_text,
            "suspense": self._contains_any(lower_text, ("until", "before", "then")),
            "ellipsis": "..." in text,
            "incomplete_statement": stripped_text.endswith((",", ":", "-")),
        }
        return self._weighted_sum(signals, feature_rules.CURIOSITY_WEIGHTS)

    def _conflict(self, match: StoryPatternMatch, lower_text: str) -> float:
        signals = {
            "conflict_keyword": self._contains_any(lower_text, feature_rules.CONFLICT_KEYWORDS),
            "contrast_phrase": self._contains_any(lower_text, feature_rules.CONTRAST_PHRASES),
            "reversal_phrase": self._contains_any(lower_text, feature_rules.REVERSAL_PHRASES),
            "conflict_segment": self._has_segment_type(match, StorySegmentType.CONFLICT),
        }
        return self._weighted_sum(signals, feature_rules.CONFLICT_WEIGHTS)

    def _emotion(self, text: str, lower_text: str, tokens: list[str]) -> float:
        emotion_matches = self._count_terms(lower_text, feature_rules.EMOTION_KEYWORDS)
        density = min(1.0, emotion_matches / 3.0)
        signals = {
            "emotion_keyword": emotion_matches > 0,
            "intensity_keyword": self._contains_any(lower_text, feature_rules.INTENSITY_KEYWORDS),
            "exclamation": "!" in text,
            "emotion_density": density,
        }
        if not tokens:
            signals["emotion_density"] = 0.0

        return self._weighted_sum(signals, feature_rules.EMOTION_WEIGHTS)

    def _novelty(self, lower_text: str) -> float:
        signals = {
            "novelty_keyword": self._contains_any(lower_text, feature_rules.NOVELTY_KEYWORDS),
            "change_phrase": self._contains_any(lower_text, ("changed everything", "for the first time")),
            "suddenness": self._contains_any(lower_text, ("suddenly", "unexpected")),
            "surprising_number": self._has_surprising_number(lower_text),
        }
        return self._weighted_sum(signals, feature_rules.NOVELTY_WEIGHTS)

    def _ending_strength(self, match: StoryPatternMatch, lower_text: str) -> float:
        signals = {
            "ending_phrase": self._contains_any(lower_text, feature_rules.ENDING_PHRASES),
            "result_phrase": self._contains_any(lower_text, feature_rules.RESULT_PHRASES),
            "ending_segment": self._has_segment_type(match, StorySegmentType.ENDING),
            "late_position": self._has_ending_last(match),
        }
        value = self._weighted_sum(signals, feature_rules.ENDING_WEIGHTS)

        if self._cta(lower_text) >= 0.5 and not signals["ending_phrase"]:
            value -= feature_rules.CTA_PENALTY

        return self._clamp(value)

    @staticmethod
    def _people(text: str, lower_text: str) -> float:
        signals = 0
        if feature_rules.PERSON_NAME_PATTERN.search(text):
            signals += 1
        if set(feature_rules.TOKEN_PATTERN.findall(lower_text)).intersection(feature_rules.PERSON_TERMS):
            signals += 1

        return min(1.0, signals / 2.0)

    @staticmethod
    def _numbers(lower_text: str) -> float:
        signals = 0
        if feature_rules.NUMBER_PATTERN.search(lower_text):
            signals += 1
        if set(feature_rules.TOKEN_PATTERN.findall(lower_text)).intersection(feature_rules.NUMBER_WORDS):
            signals += 1
        if FeatureExtractor._has_surprising_number(lower_text):
            signals += 1

        return min(1.0, signals / 3.0)

    @staticmethod
    def _question(text: str, lower_text: str) -> float:
        signals = 0
        if "?" in text:
            signals += 1
        if any(
            lower_text.strip().startswith(f"{starter} ")
            for starter in feature_rules.QUESTION_STARTERS
        ):
            signals += 1

        return min(1.0, signals / 2.0)

    @staticmethod
    def _cta(lower_text: str) -> float:
        matches = FeatureExtractor._count_terms(lower_text, feature_rules.CTA_PHRASES)
        return min(1.0, matches / 2.0)

    @staticmethod
    def _duration(match: StoryPatternMatch) -> float:
        if not match.matched_segments:
            return 0.0

        return max(0.0, match.matched_segments[-1].end - match.matched_segments[0].start)

    @staticmethod
    def _coverage(match: StoryPatternMatch) -> float:
        duration = FeatureExtractor._duration(match)
        if duration <= 0.0:
            return 0.0

        covered_duration = sum(
            max(0.0, segment.end - segment.start)
            for segment in match.matched_segments
        )
        return min(1.0, covered_duration / duration)

    @staticmethod
    def _pacing(tokens: list[str], duration: float) -> float:
        if duration <= 0.0:
            return 0.0

        words_per_second = len(tokens) / duration
        if feature_rules.IDEAL_PACING_MIN <= words_per_second <= feature_rules.IDEAL_PACING_MAX:
            return 1.0
        if words_per_second < feature_rules.IDEAL_PACING_MIN:
            return FeatureExtractor._clamp(
                (words_per_second - feature_rules.LOW_PACING_FLOOR)
                / (feature_rules.IDEAL_PACING_MIN - feature_rules.LOW_PACING_FLOOR)
            )

        return FeatureExtractor._clamp(
            (feature_rules.HIGH_PACING_CEILING - words_per_second)
            / (feature_rules.HIGH_PACING_CEILING - feature_rules.IDEAL_PACING_MAX)
        )

    @staticmethod
    def _has_segment_type(
        match: StoryPatternMatch,
        segment_type: StorySegmentType,
    ) -> bool:
        return any(
            segment.primary_type == segment_type or segment_type in segment.types
            for segment in match.matched_segments
        )

    @staticmethod
    def _has_ending_last(match: StoryPatternMatch) -> bool:
        if not match.matched_segments:
            return False

        last_segment = match.matched_segments[-1]
        return (
            last_segment.primary_type == StorySegmentType.ENDING
            or StorySegmentType.ENDING in last_segment.types
        )

    @staticmethod
    def _contains_any(lower_text: str, terms: tuple[str, ...]) -> bool:
        return any(term in lower_text for term in terms)

    @staticmethod
    def _count_terms(lower_text: str, terms: tuple[str, ...]) -> int:
        return sum(1 for term in terms if term in lower_text)

    @staticmethod
    def _has_surprising_number(lower_text: str) -> bool:
        for match in feature_rules.NUMBER_PATTERN.findall(lower_text):
            normalized = match.replace("$", "").replace("%", "").replace(",", "")
            normalized = normalized.replace(" percent", "")
            try:
                if float(normalized) >= feature_rules.SURPRISING_NUMBER_MINIMUM:
                    return True
            except ValueError:
                continue

        return False

    @staticmethod
    def _weighted_sum(
        signals: dict[str, bool | float],
        weights: dict[str, float],
    ) -> float:
        total = 0.0

        for name, weight in weights.items():
            signal = signals.get(name, False)
            if isinstance(signal, bool):
                total += weight if signal else 0.0
            else:
                total += weight * signal

        return FeatureExtractor._clamp(total)

    @staticmethod
    def _clamp(value: float) -> float:
        return min(1.0, max(0.0, value))
