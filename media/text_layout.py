"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Text Layout Engine
==================================================
"""

from dataclasses import dataclass


@dataclass(slots=True)
class LayoutConfig:

    max_chars_per_line: int = 24

    max_lines: int = 2

    max_words_per_line: int = 5


class TextLayout:

    def __init__(self, config=None):

        self.config = config or LayoutConfig()

    # -------------------------------------------------

    def wrap(self, text: str) -> list[str]:

        words = text.split()

        if not words:
            return []

        lines = []
        current = []

        for word in words:

            candidate = current + [word]

            candidate_text = " ".join(candidate)

            if (
                len(candidate) <= self.config.max_words_per_line
                and
                len(candidate_text) <= self.config.max_chars_per_line
            ):

                current.append(word)

            else:

                if current:

                    lines.append(
                        " ".join(current)
                    )

                current = [word]

        if current:

            lines.append(
                " ".join(current)
            )

        #
        # Limit total lines
        #

        if len(lines) <= self.config.max_lines:

            return lines

        merged = lines[:self.config.max_lines - 1]

        merged.append(

            " ".join(

                lines[self.config.max_lines - 1:]

            )

        )

        return merged

    # -------------------------------------------------

    def format(self, text: str) -> str:

        return "\\N".join(

            self.wrap(text)

        )