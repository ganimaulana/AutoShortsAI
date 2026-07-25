import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.project_manager import create_project

folder = create_project(
    "SASYA ARKHISNA FEAT LAILA AYU - NEGORO ANGIN"
)

print(folder)