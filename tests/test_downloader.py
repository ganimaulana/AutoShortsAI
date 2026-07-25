from yt_dlp import YoutubeDL

print("=" * 50)
print("AutoShortsAI Downloader Test")
print("=" * 50)

url = input("Masukkan URL YouTube : ")

opsi = {
    "verbose": True,
    "format": "299+140/137+140/bestvideo+bestaudio/best",
    "merge_output_format": "mp4",
    "outtmpl": "downloads/TEST_%(title)s.%(ext)s",
    "overwrites": True,
}

with YoutubeDL(opsi) as ydl:
    ydl.download([url])

print("\nSelesai!")