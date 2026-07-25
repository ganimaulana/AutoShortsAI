import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from core.highlight_detector import detect_highlights

projects = sorted(
    Path("projects").iterdir(),
    key=lambda p: p.stat().st_mtime,
    reverse=True
)

project = None

for p in projects:

    if (p / "transcript.json").exists():

        project = p
        break

if project is None:
    raise Exception("Tidak ada project yang memiliki transcript.json")

print("Project :", project.name)

output = detect_highlights(project)

print("Highlight :", output)