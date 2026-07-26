"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Pipeline
==================================================
"""

from domain.project_context import ProjectContext

from core.analyzer import analyze_video
from core.project_manager import (
    create_project,
    save_metadata,
)
from core.downloader import download_video
from core.transcriber import transcribe_video

from narrative.story_builder import StoryBuilder
from narrative.story_ranker import StoryRanker
from narrative.timeline_builder import TimelineBuilder

from core.clip_engine import ClipEngine
from media.subtitle_engine import SubtitleEngine


class Pipeline:

    def __init__(

        self,

        callback=None,


    ):

        self.callback = callback

        self.story_builder = StoryBuilder()

        self.story_ranker = StoryRanker()

        self.timeline_builder = TimelineBuilder()

        self.clip_engine = ClipEngine()

        self.subtitle_engine = SubtitleEngine()
            

    # ==================================================

    def status(self, message):

        print(message)

        if self.callback:
            self.callback(message)

    # ==================================================

    def run(self, url):

        context = ProjectContext(
            url=url
        )

        #
        # Analyze
        #

        self.status("Analyzing video...")

        info = analyze_video(url)

        context.metadata = info

        #
        # Project
        #

        self.status("Creating project...")

        context.project_path = create_project(
            info["title"]
        )

        #
        # Metadata
        #

        self.status("Saving metadata...")

        save_metadata(
            context.project_path,
            info
        )

        #
        # Download
        #

        self.status("Downloading video...")

        context.video_path = download_video(

            url,

            context.project_path,

        )

        #
        # Whisper
        #

        self.status("Transcribing audio...")

        context.transcript = transcribe_video(

            context.video_path,

            context.project_path,

        )

        #
        # Story Builder
        #

        self.status("Building stories...")

        context = self.story_builder.process(
            context
        )

        #
        # Story Ranker
        #

        self.status("Ranking stories...")

        context = self.story_ranker.process(
            context
        )

        #
        # Timeline Builder
        #

        self.status("Building timeline...")

        context = self.timeline_builder.process(
            context
        )

        #
        # Clip Engine
        #

        self.status("Generating clips...")

        context = self.clip_engine.process(
            context
        )

        #
        # Subtitle Engine
        #


        self.status("Rendering subtitles...")

        story_map = {
            story.id: story
            for story in context.stories
        }

        rendered = []

        for clip_file, timeline in zip(
            context.clips,
            context.timeline,
        ):

            story = story_map.get(
                timeline.story_id
            )

            #
            # Safety
            #

            if story is None:
                rendered.append(clip_file)
                continue

            #
            # Burn subtitle
            #

            output_video = clip_file.with_name(
                f"{clip_file.stem}_sub{clip_file.suffix}"
            )

            self.subtitle_engine.process(
                input_video=clip_file,
                segments=story.segments,
                output_video=output_video,
            )

            if output_video.exists():

                if clip_file.exists():
                    clip_file.unlink()

                output_video.rename(
                    clip_file
                )

                rendered.append(
                    clip_file
                )

            else:

                raise FileNotFoundError(
                    f"Subtitle output not found: {output_video}"
                )

            #
            # Replace original clip
            #

            if output_video.exists():

                if clip_file.exists():
                    clip_file.unlink()

                output_video.rename(
                    clip_file
                )

            rendered.append(
                clip_file
            )

            

        context.clips = rendered

        #
        # Finish
        #

        self.status("Completed ✅")


        return context