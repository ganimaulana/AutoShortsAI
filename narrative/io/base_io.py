"""
==================================================
Narrative Intelligence Engine (NIE)

Base IO
==================================================
"""

from pathlib import Path
import json


class BaseIO:
    """
    Base class for JSON file operations.
    """

    @staticmethod
    def load_json(path):

        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    @staticmethod
    def save_json(path, data):

        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False
            )