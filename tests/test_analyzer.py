"""
==========================================
AutoShortsAI
Analyzer Test
==========================================
"""

from core.analyzer import analyze_video


def main():

    url = input("URL : ").strip()

    info = analyze_video(url)

    print("\n========== HASIL ==========")

    print(f"Judul      : {info['title']}")
    print(f"Channel    : {info['channel']}")
    print(f"Views      : {info['views']}")
    print(f"Durasi     : {info['duration']} detik")
    print(f"Upload     : {info['upload_date']}")
    print(f"Resolusi   : {info['resolution']}")
    print(f"FPS        : {info['fps']}")
    print(f"Thumbnail  : {info['thumbnail']}")


if __name__ == "__main__":
    main()