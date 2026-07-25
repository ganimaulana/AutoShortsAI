import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.project_manager import (
    create_project,
    save_metadata
)

project = create_project(
    "SASYA ARKHISNA FEAT LAILA AYU - NEGORO ANGIN"
)

metadata = {

    "title": "SASYA ARKHISNA",

    "channel": "DC Production",

    "duration": 335,

    "views": 978432,

    "language": "id"

}

save_metadata(
    project,
    metadata
)

print(project)