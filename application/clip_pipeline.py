class ClipPipeline:

    def __init__(
        self,
        subtitle_corrector,
        topic_detector,
        candidate_generator,
        reviewer,
    ):

        self.subtitle_corrector = subtitle_corrector

        self.topic_detector = topic_detector

        self.candidate_generator = candidate_generator

        self.reviewer = reviewer

    def execute(self, transcript):

        corrected = self.subtitle_corrector.run(
            transcript
        )

        chapters = self.topic_detector.run(
            corrected
        )

        candidates = self.candidate_generator.run(
            chapters
        )

        reviews = self.reviewer.run(
            candidates
        )

        return reviews