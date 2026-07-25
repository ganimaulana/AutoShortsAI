import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.transcriber import transcribe_video

hasil = transcribe_video(
    r"downloads\'Trouble Is A Friend' Live Session.mp4"
)

print()

print("Language :", hasil["language"])

print("Segments :", hasil["segments"])

print()

print("Transcript :", hasil["transcript"])

print("JSON :", hasil["json"])