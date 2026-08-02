from ai.base_agent import BaseAgent


SYSTEM_PROMPT = """
You are a subtitle editor.

Rules:

- Do not change meaning.
- Fix punctuation.
- Fix capitalization.
- Preserve timestamps.
- Return only corrected text.
"""


class SubtitleCorrector(BaseAgent):

    def __init__(

        self,

        llm,

    ):

        self.llm = llm

    def run(

        self,

        transcript,

    ):

        for sentence in transcript.sentences:

            corrected = self.llm.ask(

                prompt=sentence.text,

                system=SYSTEM_PROMPT,

            )

            sentence.text = corrected.strip()

        return transcript