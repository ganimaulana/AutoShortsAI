from core.ai.ollama_provider import OllamaProvider
from core.ai.prompt_builder import PromptBuilder
from core.ai.parser import AIParser


class AIEngine:

    def __init__(self):

        self.provider = OllamaProvider()

    def process(self, transcript):

        #
        # Build Prompt
        #

        prompt = PromptBuilder.build(transcript)

        #
        # Ask AI
        #

        result = self.provider.analyze(prompt)

        #
        # Convert JSON
        #

        timeline = AIParser.parse(

            result,

            transcript,

        )

        return timeline