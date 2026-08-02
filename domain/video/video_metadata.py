from dataclasses import dataclass, field


@dataclass(slots=True)
class VideoMetadata:

    id: str = ""

    title: str = ""

    channel: str = ""

    uploader: str = ""

    description: str = ""

    language: str = ""

    duration: int = 0

    width: int = 0

    height: int = 0

    fps: float = 0

    view_count: int = 0

    like_count: int = 0

    upload_date: str = ""

    thumbnail: str = ""

    categories: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)