from __future__ import annotations

from domain.clip.models import ClipCandidate
from application.pipeline.feature_extractor import FeatureExtractor
from application.pipeline.scoring_engine import ScoringEngine


class CandidateGenerator:

    """
    Membuat banyak kandidat clip menggunakan Sliding Window.

    Contoh:

    Chapter 180 detik

    menghasilkan

    0-60
    20-80
    40-100
    60-120
    80-140
    100-160
    120-180
    """

    WINDOW = 60.0
    STEP = 20.0

    MIN_DURATION = 30.0

    def __init__(self):

        self.extractor = FeatureExtractor()

        self.scorer = ScoringEngine()

    def run(self, transcript):

        candidates = []

        for chapter in transcript.chapters:

            chapter_duration = (
                chapter.end -
                chapter.start
            )

            if chapter_duration <= self.WINDOW:

                candidate = self._build_candidate(
                    chapter,
                    chapter.start,
                    chapter.end,
                )

                candidates.append(candidate)

                continue

            start = chapter.start

            while start < chapter.end:

                end = start + self.WINDOW

                if end > chapter.end:
                    end = chapter.end

                duration = end - start

                if duration >= self.MIN_DURATION:

                    candidate = self._build_candidate(
                        chapter,
                        start,
                        end,
                    )

                    candidates.append(candidate)

                start += self.STEP

        candidates.sort(

            key=lambda c:
                c.metrics.overall,

            reverse=True,

        )

        return candidates

    def _build_candidate(

        self,

        chapter,

        start,

        end,

    ):

        feature = self.extractor.extract(

            chapter,

            start,

            end,

        )

        score = self.scorer.score(

            feature

        )

        candidate = ClipCandidate(

            start=start,

            end=end,

            chapter_id=chapter.id,

            summary=chapter.summary,

        )

        candidate.metrics = feature.metrics

        candidate.metrics.overall = score

        return candidate