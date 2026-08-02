from ai.base_agent import BaseAgent


class ClipSelector(BaseAgent):

    def run(self, subtitle: str):

        prompt = self.llm.load_prompt(

            "ai/prompts/clip.md"

        )

        prompt = prompt.replace(

            "{{SUBTITLE}}",

            subtitle,

        )

        return self.llm.ask(prompt)