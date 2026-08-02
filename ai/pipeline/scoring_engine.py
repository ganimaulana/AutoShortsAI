from domain.features import ClipFeature


class ScoringEngine:

    def score(
        self,
        feature: ClipFeature,
    ) -> float:

        score = 0.0

        # Durasi ideal
        if 45 <= feature.duration <= 70:
            score += 25

        elif 30 <= feature.duration <= 90:
            score += 15

        # Hook
        score += feature.hook_keyword * 5

        # Emotion
        score += feature.emotion_keyword * 4

        # Question
        score += feature.question_count * 3

        # Ending
        score += feature.ending_strength * 4

        # Speaking Rate
        if 2.5 <= feature.speaking_rate <= 4:
            score += 10

        score -= feature.silence_duration * 2

        return score