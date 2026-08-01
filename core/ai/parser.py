from domain.timeline import TimelineClip


class AIParser:
    """
    Convert AI JSON -> TimelineClip
    """

    @staticmethod
    def parse(result, transcript):

        #
        # Build lookup Segment
        #

        segment_lookup = {}

        for segment in transcript:

            segment_lookup[segment.id] = segment

        #
        # Build Timeline
        #

        timeline = []

        clip_id = 1

        for item in result.get("clips", []):

            segment_ids = item.get("segment_ids", [])

            segments = []

            for seg_id in segment_ids:

                if seg_id in segment_lookup:

                    segments.append(
                        segment_lookup[seg_id]
                    )

            if not segments:
                continue

            start = segments[0].start

            end = segments[-1].end

            duration = end - start

            timeline.append(

                TimelineClip(

                    clip_id=clip_id,

                    story_id=clip_id,

                    start=start,

                    end=end,

                    duration=duration,

                    score=100,

                    title=item.get("title", ""),

                    topic=""

                )

            )

            clip_id += 1

        return timeline