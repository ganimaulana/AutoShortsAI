from ai.base_agent import BaseAgent


class StoryAnalyzer(BaseAgent):

    def run(self, subtitle: str):

        prompt = self.llm.load_prompt(

            "ai/prompts/story.md"

        )

        prompt = prompt.replace(

            "{{SUBTITLE}}",

            subtitle,

        )

        return self.llm.ask(prompt)