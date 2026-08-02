from ollama import Client

from infrastructure.llm.base_provider import BaseLLMProvider


class OllamaProvider(BaseLLMProvider):

    def __init__(

        self,

        host="http://localhost:11434",

        model="qwen3:8b",

    ):

        self.client = Client(host=host)

        self.model = model

    def generate(

        self,

        prompt,

        system="",

        temperature=0.2,

    ):

        response = self.client.chat(

            model=self.model,

            messages=[

                {

                    "role": "system",

                    "content": system,

                },

                {

                    "role": "user",

                    "content": prompt,

                },

            ],

            options={

                "temperature": temperature,

            },

        )

        return response["message"]["content"]