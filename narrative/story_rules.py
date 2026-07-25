"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Story Rules
==================================================
"""


class StoryRules:
    """
    Rule collection for Story Builder.
    """

    # ----------------------------------------------

    TRANSITION_WORDS = {

        "nah",

        "jadi",

        "oke",

        "kemudian",

        "selanjutnya",

        "berikutnya",

        "lalu",

        "next",

        "sekarang",

        "baik"

    }

    # ----------------------------------------------

    MIN_SEGMENT_WORDS = 6

    MIN_STORY_DURATION = 20

    TARGET_STORY_DURATION = 35

    MAX_STORY_DURATION = 60

    MAX_SILENCE_GAP = 3.0