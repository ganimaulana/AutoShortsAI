"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Project State
==================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json


@dataclass
class ProjectState:

    #
    # Basic
    #

    title: str = ""

    url: str = ""

    project_path: Path | None = None

    #
    # Status
    #

    status: str = "created"

    current_step: str = ""

    progress: int = 0

    #
    # Result
    #

    clips: int = 0

    stories: int = 0

    #
    # Time
    #

    started_at: str = field(

        default_factory=lambda:

        datetime.now().isoformat()

    )

    finished_at: str | None = None

    # -------------------------------------------------

    def save(self):

        if self.project_path is None:

            return

        data = {

            "title": self.title,

            "url": self.url,

            "status": self.status,

            "current_step": self.current_step,

            "progress": self.progress,

            "stories": self.stories,

            "clips": self.clips,

            "started_at": self.started_at,

            "finished_at": self.finished_at,

        }

        file = self.project_path / "project.json"

        with open(

            file,

            "w",

            encoding="utf-8",

        ) as f:

            json.dump(

                data,

                f,

                indent=4,

                ensure_ascii=False,

            )

    # -------------------------------------------------

    @classmethod

    def load(

        cls,

        project_path,

    ):

        file = Path(

            project_path

        ) / "project.json"

        if not file.exists():

            raise FileNotFoundError(file)

        with open(

            file,

            encoding="utf-8",

        ) as f:

            data = json.load(f)

        state = cls()

        state.title = data["title"]

        state.url = data["url"]

        state.status = data["status"]

        state.current_step = data["current_step"]

        state.progress = data["progress"]

        state.stories = data["stories"]

        state.clips = data["clips"]

        state.started_at = data["started_at"]

        state.finished_at = data["finished_at"]

        state.project_path = Path(

            project_path

        )

        return state