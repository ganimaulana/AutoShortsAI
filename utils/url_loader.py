from pathlib import Path


def load_urls(file_path):

    path = Path(file_path)

    return [
        line.strip()
        for line in path.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]