from pathlib import Path

from domain import Segment

from media.subtitle_engine import SubtitleEngine


def test_subtitle_engine(tmp_path):

    segments = [

        Segment(

            id=1,

            start=0,

            end=2,

            text="Hello world"

        ),

        Segment(

            id=2,

            start=2,

            end=5,

            text="AutoShortsAI"

        )

    ]

    output = tmp_path / "subtitle.ass"

    engine = SubtitleEngine()

    engine.generate(

        segments,

        output

    )

    assert output.exists()

    text = output.read_text(

        encoding="utf-8"

    )

    assert "Dialogue:" in text