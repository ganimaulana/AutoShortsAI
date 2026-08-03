from pathlib import Path


class PromptService:

    def __init__(
        self,
        prompt_dir="prompts",
    ):

        self.prompt_dir = Path(prompt_dir)

    def load(
        self,
        filename,
    ):

        return (
            self.prompt_dir /
            filename
        ).read_text(
            encoding="utf8"
        )