from core.ai.ollama_provider import OllamaProvider

from core.ai.prompt_builder import PromptBuilder


class Segment:

    def __init__(

        self,

        id,

        start,

        end,

        text,

    ):

        self.id=id

        self.start=start

        self.end=end

        self.text=text


segments=[

    Segment(1,0,5,"Halo semuanya."),

    Segment(2,5,12,"Hari ini saya akan menceritakan kisah seseorang."),

    Segment(3,12,20,"Ia kehilangan seluruh hartanya."),

    Segment(4,20,32,"Namun akhirnya berhasil bangkit."),

]

prompt=PromptBuilder.build(

    segments

)

provider=OllamaProvider()

result=provider.analyze(

    prompt

)

print(result)