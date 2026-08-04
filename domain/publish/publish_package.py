from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class PublishPackage:

    video: Path

    title: str

    description: str

    tags: list[str]

    publish_at: str = ""