from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parent.parent

ZIP_NAME = "AutoShortsAI_Source.zip"

ZIP_PATH = ROOT / ZIP_NAME

# ==========================================================
# Folder yang tidak ikut
# ==========================================================

EXCLUDE_DIRS = {
    ".git",
    ".venv",
    ".vscode",
    ".idea",
    ".vs",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".cache",
    "projects",
    "downloads",
    "dist",
    "build",
    ".github",
    ".history",
}

# ==========================================================
# Extension yang tidak ikut
# ==========================================================

EXCLUDE_EXT = {
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".wmv",
    ".webm",

    ".mp3",
    ".wav",
    ".flac",
    ".aac",
    ".ogg",

    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".webp",

    ".zip",
    ".rar",
    ".7z",

    ".exe",
    ".dll",
    ".pyd",

    ".onnx",
    ".pt",
    ".pth",
    ".ckpt",
    ".bin",

    ".log",
}

# ==========================================================
# File yang selalu ikut
# ==========================================================

ALWAYS_INCLUDE = {
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "README.md",
    "app.py",
}

# ==========================================================
# Folder source
# ==========================================================

SOURCE_DIRS = {
    "application",
    "core",
    "domain",
    "gui",
    "infrastructure",
    "media",
    "pipeline",
    "docs",
    "tests",
}

MAX_FILE_SIZE_MB = 20

MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

# ==========================================================

print("=" * 60)
print("Creating ChatGPT Source Archive")
print("=" * 60)

if ZIP_PATH.exists():
    ZIP_PATH.unlink()

count = 0
skipped = 0

with ZipFile(
    ZIP_PATH,
    "w",
    ZIP_DEFLATED,
    compresslevel=9,
) as zipf:

    for file in ROOT.rglob("*"):

        if not file.is_file():
            continue

        if file == ZIP_PATH:
            continue

        relative = file.relative_to(ROOT)

        # Skip folder
        if any(part in EXCLUDE_DIRS for part in relative.parts):
            skipped += 1
            continue

        # Root files
        if len(relative.parts) == 1:

            if file.name in ALWAYS_INCLUDE:

                zipf.write(file, relative)

                count += 1

            continue

        # Folder selain source
        if relative.parts[0] not in SOURCE_DIRS:
            skipped += 1
            continue

        # Skip extension
        if file.suffix.lower() in EXCLUDE_EXT:
            skipped += 1
            continue

        # Skip file besar
        if file.stat().st_size > MAX_FILE_SIZE:
            skipped += 1
            continue

        zipf.write(file, relative)

        count += 1

print()
print("=" * 60)
print("Archive Complete")
print("=" * 60)

size = ZIP_PATH.stat().st_size / 1024 / 1024

print(f"Files archived : {count}")
print(f"Files skipped  : {skipped}")
print(f"Archive        : {ZIP_PATH}")
print(f"Archive Size   : {size:.2f} MB")
print("=" * 60)