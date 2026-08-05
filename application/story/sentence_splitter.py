from __future__ import annotations

import re

from domain.segment import Segment
from domain.story_intelligence import Sentence

from application.story import story_rules


class SentenceSplitter:
    """Converts transcript segments into deterministic sentence units."""

    _sentence_pattern = re.compile(r"[^.!?]+(?:\.\.\.|[.!?])?")

    def split(self, segments: list[Segment]) -> list[Sentence]:
        sentences: list[Sentence] = []
        current_parts: list[str] = []
        current_segment_ids: list[int] = []
        current_start: float | None = None
        current_end: float | None = None
        next_id = 1
        previous_end: float | None = None

        for segment in segments:
            text = self._normalize(segment.text)

            if not text:
                previous_end = segment.end
                continue

            if self._has_silence_gap(previous_end, segment.start) and current_parts:
                next_id = self._append_sentence(
                    sentences,
                    next_id,
                    current_start,
                    current_end,
                    current_parts,
                    current_segment_ids,
                )
                current_parts = []
                current_segment_ids = []
                current_start = None
                current_end = None

            for part in self._split_text(text):
                if current_start is None:
                    current_start = segment.start

                current_end = segment.end
                current_parts.append(part)

                if segment.id not in current_segment_ids:
                    current_segment_ids.append(segment.id)

                if self._should_flush(current_parts, current_start, current_end):
                    next_id = self._append_sentence(
                        sentences,
                        next_id,
                        current_start,
                        current_end,
                        current_parts,
                        current_segment_ids,
                    )
                    current_parts = []
                    current_segment_ids = []
                    current_start = None
                    current_end = None

            previous_end = segment.end

        if current_parts:
            self._append_sentence(
                sentences,
                next_id,
                current_start,
                current_end,
                current_parts,
                current_segment_ids,
            )

        return sentences

    @classmethod
    def _split_text(cls, text: str) -> list[str]:
        return [
            cls._normalize(match.group(0))
            for match in cls._sentence_pattern.finditer(text)
            if cls._normalize(match.group(0))
        ]

    @staticmethod
    def _normalize(text: str) -> str:
        return " ".join(text.strip().split())

    @staticmethod
    def _has_silence_gap(
        previous_end: float | None,
        current_start: float,
    ) -> bool:
        if previous_end is None:
            return False

        return current_start - previous_end >= story_rules.SILENCE_GAP_THRESHOLD

    def _should_flush(
        self,
        parts: list[str],
        start: float | None,
        end: float | None,
    ) -> bool:
        text = self._normalize(" ".join(parts))

        if text.endswith(story_rules.SENTENCE_ENDINGS):
            return True

        if start is not None and end is not None:
            if end - start >= story_rules.MAX_SENTENCE_DURATION:
                return True

        return len(text.split()) >= story_rules.MAX_SENTENCE_WORDS

    def _append_sentence(
        self,
        sentences: list[Sentence],
        sentence_id: int,
        start: float | None,
        end: float | None,
        parts: list[str],
        segment_ids: list[int],
    ) -> int:
        text = self._normalize(" ".join(parts))

        if not text or start is None or end is None:
            return sentence_id

        sentences.append(
            Sentence(
                id=sentence_id,
                start=start,
                end=end,
                text=text,
                segment_ids=segment_ids.copy(),
            )
        )

        return sentence_id + 1
