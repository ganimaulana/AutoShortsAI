from __future__ import annotations

from application.services.batch_service import BatchService
from application.services.prompt_service import PromptService
from application.services.retry_service import RetryService
from application.services.llm_service import LLMService

from domain.transcript.models import Transcript


class SubtitleCorrector:

    """
    Memperbaiki subtitle hasil Whisper.

    - Grammar
    - Capitalization
    - Punctuation
    - Tidak mengubah arti
    """

    def __init__(
        self,
        llm: LLMService,
        prompt_service: PromptService,
        batch_service: BatchService,
        retry_service: RetryService,
        batch_size: int = 20,
    ):

        self.llm = llm
        self.prompt_service = prompt_service
        self.batch_service = batch_service
        self.retry = retry_service
        self.batch_size = batch_size

    def run(
        self,
        transcript: Transcript,
    ) -> Transcript:

        system_prompt = self.prompt_service.load(
            "subtitle.md"
        )

        for batch in self.batch_service.split(
            transcript.sentences,
            self.batch_size,
        ):

            numbered = []

            for i, sentence in enumerate(batch, start=1):
                numbered.append(
                    f"{i}. {sentence.text}"
                )

            prompt = "\n".join(numbered)

            response = self.retry.run(
                lambda: self.llm.ask(
                    prompt=prompt,
                    system=system_prompt,
                    temperature=0.0,
                )
            )

            corrected = self._parse_response(
                response,
                len(batch),
            )

            for sentence, text in zip(
                batch,
                corrected,
            ):
                sentence.text = text

        return transcript

    def _parse_response(
        self,
        text: str,
        expected: int,
    ) -> list[str]:

        lines = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            if "." in line:

                left, right = line.split(
                    ".",
                    1,
                )

                if left.strip().isdigit():

                    line = right.strip()

            lines.append(line)

        if len(lines) != expected:

            raise RuntimeError(
                f"Subtitle count mismatch. "
                f"Expected {expected}, got {len(lines)}."
            )

        return lines