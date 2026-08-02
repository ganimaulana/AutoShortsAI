from ai.base_agent import BaseAgent


class SubtitleCorrector(BaseAgent):

    def run(self, transcript: str):

        prompt = self.llm.load_prompt(

            "ai/prompts/subtitle.md"

        )

        prompt = prompt.replace(

            "{{TRANSCRIPT}}",

            transcript,

        )

        return self.llm.ask(prompt)