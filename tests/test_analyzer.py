from analyzer import analyze_video

url = input("URL : ")

info = analyze_video(url)

print()

print("Judul :", info["title"])

print("Channel :", info["channel"])

print("Views :", info["views"])

print("Durasi :", info["duration"])

print("Upload :", info["upload_date"])