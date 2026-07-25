import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from core.pipeline import Pipeline


pipeline = Pipeline()

pipeline.run(

    "https://www.youtube.com/watch?v=Frcu00VNXtE&t=32s"

)