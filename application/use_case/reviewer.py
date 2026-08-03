from application.services.json_service import JsonService
from application.services.prompt_service import PromptService
from application.services.retry_service import RetryService


class Reviewer:

    def __init__(

        self,

        llm,

        prompt_service,

        json_service,

        retry_service,

    ):

        self.llm = llm

        self.prompts = prompt_service

        self.json = json_service

        self.retry = retry_service

    def run(

        self,

        candidates,

    ):

        system = self.prompts.load(
            "reviewer.md"
        )

        approved = []

        for candidate in candidates:

            prompt = self._build_prompt(
                candidate
            )

            response = self.retry.run(

                lambda:

                    self.llm.ask(

                        prompt,

                        system,

                        temperature=0.2,

                    )

            )

            data = self.json.parse(
                response
            )

            candidate.review.approved = data["approved"]

            candidate.review.score = data["score"]

            candidate.review.hook = data["hook"]

            candidate.review.emotion = data["emotion"]

            candidate.review.retention = data["retention"]

            candidate.review.clarity = data["clarity"]

            candidate.review.title = data["title"]

            candidate.review.reason = data["reason"]

            if candidate.review.approved:

                approved.append(candidate)

        approved.sort(

            key=lambda x:

                x.review.score,

            reverse=True,

        )

        return approved

    def _build_prompt(

        self,

        candidate,

    ):

        return f"""
Duration : {candidate.metrics.duration:.1f} sec

Summary:
{candidate.summary}

Metrics

Overall : {candidate.metrics.overall:.1f}

Hook : {candidate.metrics.hook}

Emotion : {candidate.metrics.emotion}

Retention : {candidate.metrics.retention}

Ending : {candidate.metrics.ending}
"""