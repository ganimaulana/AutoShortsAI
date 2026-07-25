"""
==================================================
Gani Creative Studio
Powered by Naraseta

Highlight Detector
==================================================
"""

from pathlib import Path
import json


# ============================================================
# CONFIG
# ============================================================

HOOK_WORDS = [

    "rahasia",
    "ternyata",
    "cara",
    "viral",
    "terbesar",
    "jangan",
    "penting",
    "gagal",
    "profit",
    "bahaya",
    "wajib",
    "kunci",
    "cepat",
    "mudah"

]


# ============================================================
# SCORE
# ============================================================

def calculate_score(segment):

    score = 0

    text = segment["text"].lower()

    reasons = []

    # ------------------------------------
    # Hook Words
    # ------------------------------------

    for word in HOOK_WORDS:

        if word in text:

            score += 15

            reasons.append(f"Hook: {word}")

    # ------------------------------------
    # Duration
    # ------------------------------------

    duration = segment["duration"]

    if 10 <= duration <= 60:

        score += 25

        reasons.append("Ideal Duration")

    elif duration < 5:

        score -= 10

    # ------------------------------------
    # Text Length
    # ------------------------------------

    if len(text) > 80:

        score += 20

        reasons.append("High Information")

    elif len(text) > 40:

        score += 10

    return score, reasons


# ============================================================
# DETECTOR
# ============================================================

def detect_highlights(project_path):

    project_path = Path(project_path)

    transcript_file = project_path / "transcript.json"

    output_file = project_path / "highlights.json"

    if not transcript_file.exists():

        raise FileNotFoundError(transcript_file)

    with open(transcript_file, "r", encoding="utf-8") as f:

        transcript = json.load(f)

    highlights = []

    rank = 1

    for segment in transcript:

        score, reasons = calculate_score(segment)

        if score < 20:
            continue

        highlights.append({

            "id": rank,

            "rank": rank,

            "score": score,

            "start": segment["start"],

            "end": segment["end"],

            "duration": segment["duration"],

            "text": segment["text"],

            "reason": reasons

        })

        rank += 1

    highlights.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    for index, item in enumerate(highlights):

        item["rank"] = index + 1

    result = {

        "version": "1.0",

        "clips": highlights

    }

    with open(output_file, "w", encoding="utf-8") as f:

        json.dump(

            result,

            f,

            indent=4,

            ensure_ascii=False

        )

    return output_file