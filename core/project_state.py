"""
==================================================
AutoShortsAI

Project State
==================================================
"""

from pathlib import Path

from narrative.io.base_io import BaseIO


class ProjectState:

    FILE_NAME = "state.json"

    @classmethod
    def path(cls, project_path) -> Path:
        return Path(project_path) / cls.FILE_NAME

    @classmethod
    def exists(cls, project_path) -> bool:
        return cls.path(project_path).exists()

    @classmethod
    def load(cls, project_path):

        path = cls.path(project_path)

        if not path.exists():
            return {}

        return BaseIO.load_json(path)

    @classmethod
    def save(cls, project_path, state: dict):

        BaseIO.save_json(
            cls.path(project_path),
            state,
        )