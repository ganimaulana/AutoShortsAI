import json
import requests

from core.ai.provider import AIProvider


class OllamaProvider(AIProvider):

    def __init__(

        self,

        model="qwen3:8b",

        host="http://localhost:11434",

    ):

        self.model = model

        self.host = host

    def analyze(

        self,

        prompt: str,

    ) -> dict:

        response = requests.post(

            f"{self.host}/api/generate",

            json={

                "model": self.model,

                "prompt": prompt,

                "stream": False,

                "format": "json",

            },

            timeout=600,

        )

        response.raise_for_status()

        result = response.json()

        response_text = result["response"].strip()

        print()

        print("=" * 60)
        print("RAW AI RESPONSE")
        print("=" * 60)
        print(response_text)
        print()

        try:
            return json.loads(response_text)

        except json.JSONDecodeError as e:

            print("=" * 60)
            print("INVALID JSON FROM AI")
            print("=" * 60)
            print(response_text)

            raise ValueError(
                f"AI returned invalid JSON: {e}"
            )