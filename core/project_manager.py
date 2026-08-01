"""
==================================================
Gani Creative Studio
Powered by Naraseta

Project Manager
==================================================
"""

from pathlib import Path
from datetime import datetime
import json
import re

PROJECTS_DIR = Path("projects")


def safe_filename(text: str) -> str:
    """
    Membuat nama folder yang aman untuk Windows.
    """

    if not text:
        return "untitled"

    # Hapus karakter ilegal Windows
    text = re.sub(r'[\\/*?:"<>|]', "", text)

    # Ganti semua karakter selain huruf, angka, spasi, _ dan -
    text = re.sub(r"[^A-Za-z0-9 _-]", "", text)

    # Spasi -> underscore
    text = re.sub(r"\s+", "_", text.strip())

    # Hapus titik/underscore di depan & belakang
    text = text.strip("._ ")

    if not text:
        text = "untitled"

    return text[:60]


def create_project(title: str):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    folder_name = f"{timestamp}_{safe_filename(title)}"

    project_path = PROJECTS_DIR / folder_name

    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
    project_path.mkdir(parents=True, exist_ok=True)

    for folder in [
        "clips",
        "subtitles",
        "export",
        "logs",
    ]:
        (project_path / folder).mkdir(
            parents=True,
            exist_ok=True,
        )

    return project_path


def save_metadata(project_path, metadata):

    file = Path(project_path) / "metadata.json"

    with open(file, "w", encoding="utf-8") as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False,
        )