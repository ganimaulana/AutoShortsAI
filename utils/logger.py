"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Logger
==================================================
"""

from pathlib import Path
import logging
from datetime import datetime


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / f"{datetime.now():%Y-%m-%d}.log"

logger = logging.getLogger("AutoShortsAI")

logger.setLevel(logging.INFO)

if not logger.handlers:

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)-8s | %(message)s",

        datefmt="%H:%M:%S",

    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)