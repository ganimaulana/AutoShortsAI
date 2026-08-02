from ai.base_agent import BaseAgent


class ChapterSplitter(BaseAgent):

    def run(self, subtitle: str):

        prompt = self.llm.load_prompt(
            "ai/prompts/chapter.md"
        )

        prompt = prompt.replace(
            "{{SUBTITLE}}",
            subtitle,
        )

        return self.llm.ask(prompt)