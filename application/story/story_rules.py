from __future__ import annotations

from domain.story_intelligence import StorySegmentType

SENTENCE_ENDINGS: tuple[str, ...] = ("...", ".", "!", "?")

MAX_SENTENCE_DURATION = 12.0
MAX_SENTENCE_WORDS = 35
SILENCE_GAP_THRESHOLD = 1.2

EARLY_SENTENCE_LIMIT = 2
ENDING_POSITION_RATIO = 0.8

QUESTION_PATTERNS: tuple[str, ...] = (
    "did you know",
    "what",
    "why",
    "how",
    "when",
    "where",
    "who",
    "is it",
    "are you",
    "can you",
    "do you",
)

FACT_PATTERNS: tuple[str, ...] = (
    "according to",
    "research shows",
    "studies show",
    "data shows",
    "the fact is",
    "in fact",
    "percent",
    "%",
    "million",
    "billion",
)

HOOK_PATTERNS: tuple[str, ...] = (
    "did you know",
    "you won't believe",
    "here's why",
    "this is why",
    "what happens when",
    "the truth is",
    "the reason",
    "why does",
    "how did",
)

CONTEXT_PATTERNS: tuple[str, ...] = (
    "at first",
    "before",
    "back then",
    "in the beginning",
    "started as",
    "was founded",
    "used to",
    "for years",
)

PROBLEM_PATTERNS: tuple[str, ...] = (
    "problem",
    "issue",
    "mistake",
    "wrong",
    "failed",
    "can't",
    "cannot",
    "hard",
    "difficult",
    "struggle",
    "risk",
    "danger",
)

CONFLICT_PATTERNS: tuple[str, ...] = (
    "but",
    "however",
    "instead",
    "even though",
    "despite",
    "against",
    "challenge",
    "conflict",
    "refused",
    "blocked",
    "lost",
    "crisis",
)

BUILD_UP_PATTERNS: tuple[str, ...] = (
    "then",
    "after that",
    "next",
    "suddenly",
    "over time",
    "eventually",
    "as a result",
    "started to",
    "began to",
)

SOLUTION_PATTERNS: tuple[str, ...] = (
    "solution",
    "fixed",
    "solved",
    "decided to",
    "started using",
    "the answer",
    "we found",
    "they found",
    "so we",
    "what worked",
)

RESULT_PATTERNS: tuple[str, ...] = (
    "result",
    "finally",
    "ended up",
    "in the end",
    "became",
    "grew",
    "increased",
    "decreased",
    "earned",
    "saved",
    "won",
    "lost",
)

ENDING_PATTERNS: tuple[str, ...] = (
    "that's why",
    "that is why",
    "and that's it",
    "from now on",
    "the lesson",
    "what matters",
    "in conclusion",
)

CTA_PATTERNS: tuple[str, ...] = (
    "subscribe",
    "follow",
    "like this video",
    "comment below",
    "share this",
    "check the link",
    "click the link",
    "turn on notifications",
)

PATTERNS_BY_TYPE: dict[StorySegmentType, tuple[str, ...]] = {
    StorySegmentType.QUESTION: QUESTION_PATTERNS,
    StorySegmentType.FACT: FACT_PATTERNS,
    StorySegmentType.HOOK: HOOK_PATTERNS,
    StorySegmentType.CONTEXT: CONTEXT_PATTERNS,
    StorySegmentType.PROBLEM: PROBLEM_PATTERNS,
    StorySegmentType.CONFLICT: CONFLICT_PATTERNS,
    StorySegmentType.BUILD_UP: BUILD_UP_PATTERNS,
    StorySegmentType.SOLUTION: SOLUTION_PATTERNS,
    StorySegmentType.RESULT: RESULT_PATTERNS,
    StorySegmentType.ENDING: ENDING_PATTERNS,
    StorySegmentType.CTA: CTA_PATTERNS,
}

PRIMARY_TYPE_PRIORITY: tuple[StorySegmentType, ...] = (
    StorySegmentType.CTA,
    StorySegmentType.HOOK,
    StorySegmentType.QUESTION,
    StorySegmentType.PROBLEM,
    StorySegmentType.CONFLICT,
    StorySegmentType.BUILD_UP,
    StorySegmentType.SOLUTION,
    StorySegmentType.RESULT,
    StorySegmentType.ENDING,
    StorySegmentType.FACT,
    StorySegmentType.CONTEXT,
    StorySegmentType.UNKNOWN,
)
