"""
==================================================
Gani Creative Studio
Powered by Naraseta

Project Manager
==================================================
"""

from pathlib import Path
from datetime import datetime
import re

PROJECTS_DIR = Path("projects")


def safe_filename(text: str) -> str:
    """
    Mengubah judul video menjadi nama folder yang aman.
    """

    text = re.sub(r'[\\/*?:"<>|]', "", text)
    text = re.sub(r"\s+", "_", text.strip())

    return text[:60]


def create_project(title: str):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    folder_name = f"{timestamp}_{safe_filename(title)}"

    project_path = PROJECTS_DIR / folder_name

    project_path.mkdir(parents=True, exist_ok=True)

    (project_path / "clips").mkdir(exist_ok=True)
    (project_path / "subtitles").mkdir(exist_ok=True)
    (project_path / "export").mkdir(exist_ok=True)
    (project_path / "logs").mkdir(exist_ok=True)

    return project_path

import json


def save_metadata(project_path, metadata):

    file = project_path / "metadata.json"

    with open(file, "w", encoding="utf-8") as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )