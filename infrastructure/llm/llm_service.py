class LLMService:

    def __init__(

        self,

        provider,

    ):

        self.provider = provider

    def ask(

        self,

        prompt,

        system="",

        temperature=0.2,

    ):

        return self.provider.generate(

            prompt,

            system,

            temperature,

        )