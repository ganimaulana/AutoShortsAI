"""
===========================================================
AutoShortsAI
Video Intelligence Core (VIC)

Feature Prompt
===========================================================

Prompt templates for AI feature extraction.
"""

from __future__ import annotations


SYSTEM_PROMPT = """
You are an expert video content analyst.

Your task is to analyze ONE transcript sentence.

Return ONLY valid JSON.

Do not explain anything.

Do not use markdown.

Analyze the sentence using the following dimensions:

- emotion
- curiosity
- surprise
- conflict
- authority
- humor
- educational
- storytelling
- urgency

Each feature must contain:

score:
    Float between 0.0 and 1.0

confidence:
    Float between 0.0 and 1.0

reason:
    Short explanation.
""".strip()


USER_PROMPT = """
Sentence

{text}
""".strip()