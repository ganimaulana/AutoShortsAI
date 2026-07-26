"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Keyword Matcher
==================================================
"""

import re


class KeywordMatcher:

    @staticmethod
    def normalize(text: str) -> str:

        text = text.lower()

        text = re.sub(

            r"[^\w\s]",

            " ",

            text

        )

        text = re.sub(

            r"\s+",

            " ",

            text

        )

        return text.strip()

    # -------------------------------------------------

    @classmethod
    def contains(

        cls,

        text: str,

        keyword: str,

    ) -> bool:

        text = cls.normalize(text)

        keyword = cls.normalize(keyword)

        pattern = rf"\b{re.escape(keyword)}\b"

        return re.search(

            pattern,

            text

        ) is not None

    # -------------------------------------------------

    @classmethod
    def find(

        cls,

        text: str,

        keywords: list[str],

    ) -> list[str]:

        matches = []

        for keyword in keywords:

            if cls.contains(

                text,

                keyword,

            ):

                matches.append(keyword)

        return matches