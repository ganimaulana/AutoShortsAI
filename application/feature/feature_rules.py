from __future__ import annotations

import re
from re import Pattern

HOOK_PHRASES: tuple[str, ...] = (
    "did you know",
    "you won't believe",
    "here's why",
    "this is why",
    "what happens when",
    "the truth is",
    "the reason",
)

CURIOSITY_PHRASES: tuple[str, ...] = (
    "secret",
    "hidden",
    "nobody knows",
    "what happened next",
    "open loop",
    "mystery",
)

CONFLICT_KEYWORDS: tuple[str, ...] = (
    "against",
    "blocked",
    "challenge",
    "conflict",
    "crisis",
    "failed",
    "lost",
    "refused",
)

CONTRAST_PHRASES: tuple[str, ...] = (
    "but",
    "despite",
    "even though",
    "however",
    "instead",
)

REVERSAL_PHRASES: tuple[str, ...] = (
    "turned out",
    "went wrong",
    "changed everything",
)

EMOTION_KEYWORDS: tuple[str, ...] = (
    "afraid",
    "amazing",
    "angry",
    "excited",
    "fear",
    "happy",
    "heartbreaking",
    "sad",
    "shocked",
    "surprised",
)

INTENSITY_KEYWORDS: tuple[str, ...] = (
    "extremely",
    "unbelievable",
    "very",
)

NOVELTY_KEYWORDS: tuple[str, ...] = (
    "first",
    "never",
    "new",
    "rare",
    "unique",
    "unexpected",
    "unusual",
)

ENDING_PHRASES: tuple[str, ...] = (
    "that's why",
    "that is why",
    "finally",
    "from now on",
    "in the end",
    "the lesson",
    "what matters",
)

RESULT_PHRASES: tuple[str, ...] = (
    "became",
    "result",
    "solved",
    "worked",
)

CTA_PHRASES: tuple[str, ...] = (
    "check the link",
    "click the link",
    "comment below",
    "follow",
    "like this video",
    "share this",
    "subscribe",
    "turn on notifications",
)

QUESTION_STARTERS: tuple[str, ...] = (
    "are",
    "can",
    "could",
    "did",
    "do",
    "does",
    "how",
    "is",
    "should",
    "what",
    "when",
    "where",
    "who",
    "why",
    "would",
)

PERSON_TERMS: tuple[str, ...] = (
    "artist",
    "ceo",
    "creator",
    "doctor",
    "engineer",
    "founder",
    "he",
    "president",
    "she",
    "teacher",
    "team",
    "they",
)

NUMBER_WORDS: tuple[str, ...] = (
    "billion",
    "eight",
    "five",
    "four",
    "hundred",
    "million",
    "nine",
    "one",
    "percent",
    "seven",
    "six",
    "ten",
    "thousand",
    "three",
    "two",
)

HOOK_WEIGHTS: dict[str, float] = {
    "hook_phrase": 0.30,
    "question": 0.20,
    "hook_segment": 0.20,
    "surprising_number": 0.15,
    "curiosity_phrase": 0.15,
}

CURIOSITY_WEIGHTS: dict[str, float] = {
    "curiosity_phrase": 0.30,
    "because": 0.15,
    "suspense": 0.20,
    "ellipsis": 0.15,
    "incomplete_statement": 0.20,
}

CONFLICT_WEIGHTS: dict[str, float] = {
    "conflict_keyword": 0.35,
    "contrast_phrase": 0.25,
    "reversal_phrase": 0.20,
    "conflict_segment": 0.20,
}

EMOTION_WEIGHTS: dict[str, float] = {
    "emotion_keyword": 0.45,
    "intensity_keyword": 0.20,
    "exclamation": 0.20,
    "emotion_density": 0.15,
}

NOVELTY_WEIGHTS: dict[str, float] = {
    "novelty_keyword": 0.40,
    "change_phrase": 0.25,
    "suddenness": 0.15,
    "surprising_number": 0.20,
}

ENDING_WEIGHTS: dict[str, float] = {
    "ending_phrase": 0.35,
    "result_phrase": 0.25,
    "ending_segment": 0.25,
    "late_position": 0.15,
}

CTA_PENALTY = 0.20
IDEAL_PACING_MIN = 2.0
IDEAL_PACING_MAX = 3.5
LOW_PACING_FLOOR = 0.5
HIGH_PACING_CEILING = 6.0
SURPRISING_NUMBER_MINIMUM = 100

TOKEN_PATTERN: Pattern[str] = re.compile(r"\b[\w']+\b")
NUMBER_PATTERN: Pattern[str] = re.compile(r"\$?\d+(?:[.,]\d+)*(?:%| percent)?")
PERSON_NAME_PATTERN: Pattern[str] = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b")
