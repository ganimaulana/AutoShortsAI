from dataclasses import dataclass, field


@dataclass
class Word:

    text: str
    start: float
    end: float


@dataclass
class Sentence:

    start: float
    end: float
    text: str


@dataclass
class Chapter:

    start: float
    end: float
    title: str = ""
    summary: str = ""
    sentences: list[Sentence] = field(default_factory=list)