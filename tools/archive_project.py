from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil

ROOT = Path(__file__).resolve().parent.parent

ZIP_NAME = "AutoShortsAI_Source.zip"

ZIP_PATH = ROOT / ZIP_NAME

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vs",
    ".vscode",
    "projects",
    "downloads",
    "build",
    "dist",
    ".cache",
    ".ruff_cache",
    ".coverage",
    ".gitignore_cache",
}

EXCLUDE_EXT = {
    ".pyc",
    ".pyo",
    ".pyd",
}

print("=" * 60)
print("Creating archive...")
print("=" * 60)

if ZIP_PATH.exists():
    ZIP_PATH.unlink()

count = 0

with ZipFile(
    ZIP_PATH,
    "w",
    compression=ZIP_DEFLATED,
    compresslevel=9,
) as zipf:

    for file in ROOT.rglob("*"):

        if file == ZIP_PATH:
            continue

        relative = file.relative_to(ROOT)

        if any(part in EXCLUDE_DIRS for part in relative.parts):
            continue

        if file.suffix.lower() in EXCLUDE_EXT:
            continue

        if file.is_dir():
            continue

        zipf.write(
            file,
            arcname=relative,
        )

        count += 1

print()
print("=" * 60)
print("Archive Complete")
print("=" * 60)

size_mb = ZIP_PATH.stat().st_size / (1024 * 1024)

print(f"Files archived : {count}")
print(f"Archive        : {ZIP_PATH}")
print(f"Size           : {size_mb:.2f} MB")

print("=" * 60)

try:
    shutil.which("explorer")

    import subprocess

    subprocess.Popen(
        [
            "explorer",
            str(ROOT),
        ]
    )

except Exception:
    pass