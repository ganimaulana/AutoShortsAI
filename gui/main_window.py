from PIL import Image
from urllib.request import urlretrieve
import threading
import customtkinter as ctk

from core.downloader import download_video
from core.analyzer import analyze_video

# ==========================================================
# APP INFO
# ==========================================================

COMPANY = "Gani Creative Studio"
POWERED = "Powered by Naraseta"
VERSION = "v0.3.0"

# ==========================================================
# HELPER
# ==========================================================

def format_duration(seconds):

    if seconds is None:
        return "-"

    minutes = seconds // 60
    sec = seconds % 60

    return f"{minutes:02}:{sec:02}"


def format_views(views):

    if views is None:
        return "-"

    return f"{views:,}".replace(",", ".")


def format_date(date):

    if not date:
        return "-"

    return f"{date[6:8]}/{date[4:6]}/{date[:4]}"


# ==========================================================
# MAIN WINDOW
# ==========================================================

class MainWindow(ctk.CTk):

    def __init__(self):

        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(f"{COMPANY} - AutoShorts")

        self.geometry("980x720")

        self.resizable(False, False)

        self.build_header()

        self.build_url()

        self.build_video_card()

        self.build_buttons()

        self.build_progress()

        self.build_footer()

    # ======================================================

    def build_header(self):

        company = ctk.CTkLabel(
            self,
            text=COMPANY,
            font=("Segoe UI",34,"bold")
        )

        company.pack(pady=(25,0))

        powered = ctk.CTkLabel(
            self,
            text=POWERED,
            font=("Segoe UI",16),
            text_color="gray70"
        )

        powered.pack(pady=(5,25))

    # ======================================================

    def build_url(self):

        label = ctk.CTkLabel(
            self,
            text="Paste YouTube URL",
            font=("Segoe UI",18,"bold")
        )

        label.pack()

        self.url_entry = ctk.CTkEntry(
            self,
            width=760,
            height=45,
            placeholder_text="https://youtube.com/watch?v=..."
        )

        self.url_entry.pack(pady=15)

    # ======================================================

    def build_video_card(self):

        self.card = ctk.CTkFrame(
            self,
            width=840,
            height=190
        )

        self.card.pack()

        self.card.pack_propagate(False)

        self.title_label = ctk.CTkLabel(
            self.card,
            text="Title : -",
            anchor="w",
            font=("Segoe UI",17,"bold")
        )

        self.title_label.pack(fill="x",padx=20,pady=(15,5))

        self.channel_label = ctk.CTkLabel(
            self.card,
            text="Channel : -",
            anchor="w"
        )

        self.channel_label.pack(fill="x",padx=20)

        self.duration_label = ctk.CTkLabel(
            self.card,
            text="Duration : -",
            anchor="w"
        )

        self.duration_label.pack(fill="x",padx=20)

        self.views_label = ctk.CTkLabel(
            self.card,
            text="Views : -",
            anchor="w"
        )

        self.views_label.pack(fill="x",padx=20)

        self.upload_label = ctk.CTkLabel(
            self.card,
            text="Upload : -",
            anchor="w"
        )

        self.upload_label.pack(fill="x",padx=20)

        self.resolution_label = ctk.CTkLabel(
            self.card,
            text="Resolution : -",
            anchor="w"
        )

        self.resolution_label.pack(fill="x",padx=20)

    # ======================================================

    def build_buttons(self):

        frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        frame.pack(pady=20)

        self.analyze_btn = ctk.CTkButton(
            frame,
            text="Analyze",
            width=180,
            height=45,
            font=("Segoe UI",16,"bold"),
            command=self.start_analyze
        )

        self.analyze_btn.pack(
            side="left",
            padx=10
        )

        self.download_btn = ctk.CTkButton(
            frame,
            text="Download",
            width=180,
            height=45,
            font=("Segoe UI",16,"bold"),
            command=self.start_download
        )

        self.download_btn.pack(
            side="left",
            padx=10
        )

    # ======================================================

    def build_progress(self):

        self.progress = ctk.CTkProgressBar(
            self,
            width=720
        )

        self.progress.pack()

        self.progress.set(0)

        self.status = ctk.CTkLabel(
            self,
            text="Ready...",
            font=("Segoe UI",16)
        )

        self.status.pack(pady=20)
       # ======================================================
    # FOOTER
    # ======================================================

    def build_footer(self):

        footer = ctk.CTkLabel(
            self,
            text=f"Version {VERSION}",
            font=("Segoe UI", 12),
            text_color="gray60"
        )

        footer.pack(side="bottom", pady=18)

    # ======================================================
    # ANALYZE
    # ======================================================

    def start_analyze(self):

        threading.Thread(
            target=self.process_analyze,
            daemon=True
        ).start()

    def process_analyze(self):

        url = self.url_entry.get().strip()

        if url == "":
            self.status.configure(
                text="Please paste a YouTube URL."
            )
            return

        self.analyze_btn.configure(state="disabled")

        self.progress.set(0.10)

        self.status.configure(text="Analyzing video...")

        try:

            info = analyze_video(url)

            self.title_label.configure(
                text=f"Title : {info['title']}"
            )

            self.channel_label.configure(
                text=f"Channel : {info['channel']}"
            )

            self.duration_label.configure(
                text=f"Duration : {format_duration(info['duration'])}"
            )

            self.views_label.configure(
                text=f"Views : {format_views(info['views'])}"
            )

            self.upload_label.configure(
                text=f"Upload : {format_date(info['upload_date'])}"
            )

            self.resolution_label.configure(
                text=f"Resolution : {info['resolution']}  |  {info['fps']} FPS"
            )

            self.progress.set(1)

            self.status.configure(
                text="Analyze Complete ✅"
            )

        except Exception as e:

            self.progress.set(0)

            self.status.configure(
                text=f"Error : {e}"
            )

        finally:

            self.analyze_btn.configure(state="normal")

    # ======================================================
    # DOWNLOAD
    # ======================================================

    def start_download(self):

        threading.Thread(
            target=self.process_download,
            daemon=True
        ).start()

    def process_download(self):

        url = self.url_entry.get().strip()

        if url == "":
            self.status.configure(
                text="Please paste a YouTube URL."
            )
            return

        self.download_btn.configure(state="disabled")

        self.progress.set(0.10)

        self.status.configure(
            text="Downloading..."
        )

        try:

            download_video(url)

            self.progress.set(1)

            self.status.configure(
                text="Download Complete ✅"
            )

        except Exception as e:

            self.progress.set(0)

            self.status.configure(
                text=f"Error : {e}"
            )

        finally:

            self.download_btn.configure(state="normal")

    # ======================================================
    # RESET
    # ======================================================

    def reset_video_info(self):

        self.title_label.configure(text="Title : -")
        self.channel_label.configure(text="Channel : -")
        self.duration_label.configure(text="Duration : -")
        self.views_label.configure(text="Views : -")
        self.upload_label.configure(text="Upload : -")
        self.resolution_label.configure(text="Resolution : -")

        self.progress.set(0)

        self.status.configure(text="Ready...")

    # ======================================================
    # RUN
    # ======================================================

    def run(self):

        self.mainloop() 
