from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):

    @abstractmethod
    def generate(

        self,

        prompt: str,

        system: str = "",

        temperature: float = 0.2,

    ) -> str:
        ...