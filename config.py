"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Global Configuration
==================================================
"""

from pathlib import Path

# ==================================================
# ROOT
# ==================================================

ROOT_DIR = Path(__file__).resolve().parent

# ==================================================
# FOLDERS
# ==================================================

ASSETS_DIR = ROOT_DIR / "assets"

PROJECTS_DIR = ROOT_DIR / "projects"

DOWNLOADS_DIR = ROOT_DIR / "downloads"

OUTPUT_DIR = ROOT_DIR / "output"

TEMP_DIR = ROOT_DIR / "temp"

LOGS_DIR = ROOT_DIR / "logs"

ICONS_DIR = ROOT_DIR / "icons"

# ==================================================
# WHISPER
# ==================================================

WHISPER_MODEL = "base"

WHISPER_DEVICE = "cpu"

WHISPER_COMPUTE = "int8"

# ==================================================
# STORY BUILDER
# ==================================================

MIN_SEGMENT_WORDS = 6

MIN_STORY_DURATION = 20

TARGET_STORY_DURATION = 35

MAX_STORY_DURATION = 60

MAX_SILENCE_GAP = 3.0

# ==================================================
# STORY RANKER
# ==================================================

HOOK_SCORE = 30

CONFLICT_SCORE = 20

SOLUTION_SCORE = 20

EMOTION_SCORE = 15

DURATION_SCORE = 15

# ==================================================
# VIDEO
# ==================================================

VIDEO_FORMAT = "mp4"

VIDEO_WIDTH = 1080

VIDEO_HEIGHT = 1920

VIDEO_FPS = 30

# ==================================================
# SUBTITLE
# ==================================================

SUBTITLE_FONT = "Arial"

SUBTITLE_SIZE = 54

SUBTITLE_COLOR = "white"

# ==================================================
# EXPORT
# ==================================================

EXPORT_FORMAT = "mp4"

EXPORT_CODEC = "libx264"

EXPORT_AUDIO = "aac"

# ==================================================
# GUI
# ==================================================

APP_NAME = "AutoShortsAI"

WINDOW_WIDTH = 1400

WINDOW_HEIGHT = 900