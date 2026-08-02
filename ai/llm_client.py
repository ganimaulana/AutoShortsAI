from pathlib import Path

import ollama


class LLMClient:

    def __init__(
        self,
        model="qwen3:8b",
    ):
        self.model = model

    def ask(
        self,
        prompt: str,
    ) -> str:

        response = ollama.chat(

            model=self.model,

            messages=[

                {

                    "role": "user",

                    "content": prompt,

                }

            ],

        )

        return response["message"]["content"]

    @staticmethod
    def load_prompt(path: str) -> str:

        return Path(path).read_text(
            encoding="utf-8"
        )