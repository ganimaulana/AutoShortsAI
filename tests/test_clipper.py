import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from core.clipper import clip_video

# ===========================================
# Cari project terbaru
# ===========================================

projects = sorted(
    Path("projects").iterdir(),
    key=lambda p: p.stat().st_mtime,
    reverse=True
)

project = projects[0]

print("Project :", project.name)

# ===========================================
# Clip pertama
# ===========================================

clip = clip_video(

    input_video=project / "original.mp4",

    output_video=project / "clips" / "clip001.mp4",

    start=10,

    end=30

)

print()

print("SUCCESS")

print(clip)