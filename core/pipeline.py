"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Pipeline
==================================================
"""

from copy import deepcopy
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
from core.ai_engine import AIEngine
from utils.logger import logger

class Pipeline:

    def __init__(
        self,
        callback=None,
        cancel_token=None,
    ):

        self.callback = callback

        self.story_builder = StoryBuilder()

        self.story_ranker = StoryRanker()

        self.timeline_builder = TimelineBuilder()

        self.clip_engine = ClipEngine()

        self.subtitle_engine = SubtitleEngine()

        self.ai_engine = AIEngine()

        self.cancel_token = cancel_token
            

    # ==================================================

    def status(self, message):

        logger.info(message)

        if self.callback:
            self.callback(message)

    # ==================================================

    def check_cancel(self):

        if (
            self.cancel_token
            and
            self.cancel_token.cancelled
        ):

            raise RuntimeError(
                "Pipeline cancelled."
            )
    # ==================================================
    # Analyze
    # ==================================================

    def step_analyze(self, context):

        self.status("Analyzing video...")

        info = analyze_video(context.url)

        context.metadata = info

    # ==================================================
    # Create Project
    # ==================================================

    def step_create_project(self, context):

        self.status("Creating project...")

        context.project_path = create_project(
            context.metadata["title"]
        )

        self.status("Saving metadata...")

        save_metadata(
            context.project_path,
            context.metadata,
        )

    # ==================================================
    # Download
    # ==================================================

    def step_download(self, context):

        self.status("Downloading video...")

        context.video_path = download_video(
            context.url,
            context.project_path,
        )

    # ==================================================
    # Transcriber
    # ==================================================

    def step_transcriber(self, context):

        self.status("Transcribing audio...")

        context.transcript = transcribe_video(
            context.video_path,
            context.project_path,
        )
        
    # ==================================================
    # Story Builder
    # ==================================================

    def step_story_builder(self, context):

        self.status("Building stories...")

        context = self.story_builder.process(
            context
        )

        return context
    # ==================================================
    # Story Ranker
    # ==================================================

    def step_story_ranker(self, context):

        self.status("Ranking stories...")

        context = self.story_ranker.process(
            context
        )
    
        return context
    # ==================================================
    # Timeline Builder
    # ==================================================

    def step_timeline_builder(self, context):

        self.status("Building timeline...")

        context = self.timeline_builder.process(
            context
        )

        return context
    # ==================================================
    # Clip Engine
    # ==================================================

    def step_clip_engine(self, context):

        self.status("Generating clips...")

        context = self.clip_engine.process(
            context
        )

        return context
    # ==================================================
    # Subtitle Engine
    # ==================================================

    def step_subtitle_engine(self, context):

        self.status("Rendering subtitles...")

        if not context.stories:

            raise RuntimeError(
                "No stories generated."
            )

        story_map = {
            story.id: story
            for story in context.stories
        }

        rendered = []

        if len(context.clips) != len(context.timeline):

            raise RuntimeError(
                f"Timeline ({len(context.timeline)}) "
                f"!= Clips ({len(context.clips)})"
            )

        for clip_file, timeline in zip(
            context.clips,
            context.timeline,
        
        ):
            self.check_cancel()
            story = story_map.get(
                timeline.story_id
            )

            if story is None:
                raise RuntimeError(
                    f"Story ID {timeline.story_id} not found."
                )

            output_video = clip_file.with_name(
                f"{clip_file.stem}_sub{clip_file.suffix}"
            )

            logger.info("=" * 60)
            logger.info(f"Story ID: {story.id}")
            logger.info(f"Clip File: {clip_file}")
            logger.info(f"Timeline: {timeline.start} -> {timeline.end}")
            logger.info(f"Story Segments: {len(story.segments)}")

            for seg in story.segments:
                logger.info(
                    f"{seg.start:.2f} -> {seg.end:.2f} | {seg.text[:80]}"
                )

            #
            # Offset subtitle ke waktu clip
            #

            offset_segments = []

            clip_start = timeline.start
            clip_end = timeline.end

            for seg in story.segments:

                #
                # Lewati jika benar-benar di luar clip
                #

                if seg.end < clip_start:
                    continue

                if seg.start > clip_end:
                    continue

                new_seg = deepcopy(seg)

                #
                # Offset timestamp
                #

                new_seg.start = max(
                    0.0,
                    seg.start - clip_start,
                )

                new_seg.end = max(
                    new_seg.start + 0.01,
                    seg.end - clip_start,
                )

                offset_segments.append(
                    new_seg
                )

            logger.info(
                f"Subtitle Offset Segments: {len(offset_segments)}"
            )

            self.subtitle_engine.process(

                input_video=clip_file,

                segments=offset_segments,

                output_video=output_video,

            )

            self.check_cancel()


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

        context.clips = rendered

    # ==================================================
    # ==================================================
    # ==================================================
    # ==================================================
    # ==================================================
    # ==================================================    
    # ==================================================

    def run(self, url):

        context = ProjectContext(
            url=url
        )

        steps = [

            self.step_analyze,

            self.step_create_project,

            self.step_download,

            self.step_transcriber,

        ]

        for step in steps:

            step(context)

            self.check_cancel()

        context = self.step_story_builder(
            context
        )

        self.check_cancel()

        context = self.step_story_ranker(
            context
        )

        self.check_cancel()

        context = self.step_timeline_builder(
            context
        )

        self.check_cancel()

        context = self.step_clip_engine(
            context
        )

        self.check_cancel()

        self.step_subtitle_engine(
            context
        )

        self.check_cancel()

        self.status("Completed ✅")


        return context