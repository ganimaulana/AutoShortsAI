"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Cache Manager
==================================================
"""

from pathlib import Path
import json


class CacheManager:
    """
    Manage cached project artifacts.

    Example
    -------
    cache = CacheManager(project_path)

    if cache.has_transcript():
        transcript = cache.load_transcript()
    """

    # ==================================================

    def __init__(self, project_path):

        self.project_path = Path(project_path)

    # ==================================================
    # Files
    # ==================================================

    @property
    def transcript_file(self):

        return self.project_path / "transcript.json"

    @property
    def stories_file(self):

        return self.project_path / "stories.json"

    @property
    def ranking_file(self):

        return self.project_path / "ranking.json"

    @property
    def timeline_file(self):

        return self.project_path / "timeline.json"

    # ==================================================
    # Generic
    # ==================================================

    def exists(self, file):

        return Path(file).exists()

    def load(self, file):

        file = Path(file)

        if not file.exists():

            return None

        with open(

            file,

            "r",

            encoding="utf-8",

        ) as f:

            return json.load(f)

    def save(

        self,

        file,

        data,

    ):

        file = Path(file)

        file.parent.mkdir(

            parents=True,

            exist_ok=True,

        )

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

    # ==================================================
    # Transcript
    # ==================================================

    def has_transcript(self):

        return self.transcript_file.exists()

    def load_transcript(self):

        return self.load(

            self.transcript_file

        )

    def save_transcript(

        self,

        data,

    ):

        self.save(

            self.transcript_file,

            data,

        )

    # ==================================================
    # Stories
    # ==================================================

    def has_stories(self):

        return self.stories_file.exists()

    def load_stories(self):

        return self.load(

            self.stories_file

        )

    def save_stories(

        self,

        data,

    ):

        self.save(

            self.stories_file,

            data,

        )

    # ==================================================
    # Ranking
    # ==================================================

    def has_ranking(self):

        return self.ranking_file.exists()

    def load_ranking(self):

        return self.load(

            self.ranking_file

        )

    def save_ranking(

        self,

        data,

    ):

        self.save(

            self.ranking_file,

            data,

        )

    # ==================================================
    # Timeline
    # ==================================================

    def has_timeline(self):

        return self.timeline_file.exists()

    def load_timeline(self):

        return self.load(

            self.timeline_file

        )

    def save_timeline(

        self,

        data,

    ):

        self.save(

            self.timeline_file,

            data,

        )