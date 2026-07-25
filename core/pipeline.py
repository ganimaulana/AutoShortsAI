"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI Pipeline
==================================================
"""

from core.analyzer import analyze_video
from core.project_manager import (
    create_project,
    save_metadata,
)
from core.downloader import download_video
from core.transcriber import transcribe_video


class Pipeline:

    def __init__(self, callback=None):

        self.callback = callback

    # ==================================================

    def status(self, message):

        print(message)

        if self.callback:
            self.callback(message)

    # ==================================================

    def run(self, url):

        # -------------------------------
        # Analyze
        # -------------------------------

        self.status("Analyzing video...")

        info = analyze_video(url)

        # -------------------------------
        # Project
        # -------------------------------

        self.status("Creating project...")

        project = create_project(
            info["title"]
        )

        # -------------------------------
        # Metadata
        # -------------------------------

        self.status("Saving metadata...")

        save_metadata(
            project,
            info
        )

        # -------------------------------
        # Download
        # -------------------------------

        self.status("Downloading video...")

        video_path = download_video(
            url,
            project
        )

        # -------------------------------
        # Whisper
        # -------------------------------

        self.status("Transcribing audio...")

        transcript = transcribe_video(
            video_path,
            project
        )

        # -------------------------------
        # Finish
        # -------------------------------

        self.status("Completed ✅")

        return {

            "project": project,

            "metadata": info,

            "video": video_path,

            "transcript": transcript

        }