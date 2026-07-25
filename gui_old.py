import customtkinter as ctk
import threading

from downloader import download_video

# ====================================================
# APP INFO
# ====================================================

COMPANY = "Gani Creative Studio"
POWERED = "Powered by Naraseta"
VERSION = "v0.2.0"

# ====================================================
# THEME
# ====================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ====================================================
# WINDOW
# ====================================================

app = ctk.CTk()

app.title(f"{COMPANY} - AutoShorts")
app.geometry("900x620")
app.resizable(False, False)

# ====================================================
# DOWNLOAD FUNCTION
# ====================================================

def proses_download():

    url = url_entry.get().strip()

    if url == "":
        status.configure(text="Please paste a YouTube URL.")
        return

    try:

        download_btn.configure(state="disabled")

        progress.set(0.10)

        status.configure(text="Downloading...")

        app.update()

        download_video(url)

        progress.set(1)

        status.configure(text="Download Complete ✅")

    except Exception as e:

        status.configure(text=f"Error : {e}")

    finally:

        download_btn.configure(state="normal")


def mulai_download():

    threading.Thread(
        target=proses_download,
        daemon=True
    ).start()

# ====================================================
# HEADER
# ====================================================

company = ctk.CTkLabel(
    app,
    text=COMPANY,
    font=("Segoe UI", 34, "bold")
)
company.pack(pady=(35, 0))

powered = ctk.CTkLabel(
    app,
    text=POWERED,
    font=("Segoe UI", 16),
    text_color="gray70"
)
powered.pack(pady=(5, 35))

# ====================================================
# URL ENTRY
# ====================================================

url_entry = ctk.CTkEntry(
    app,
    width=760,
    height=46,
    corner_radius=8,
    placeholder_text="Paste YouTube URL here..."
)
url_entry.pack()

# ====================================================
# DOWNLOAD BUTTON
# ====================================================

download_btn = ctk.CTkButton(
    app,
    text="DOWNLOAD VIDEO",
    width=260,
    height=48,
    corner_radius=8,
    font=("Segoe UI", 18, "bold"),
    command=mulai_download
)

download_btn.pack(pady=35)

# ====================================================
# PROGRESS BAR
# ====================================================

progress = ctk.CTkProgressBar(
    app,
    width=700,
    height=10
)

progress.set(0)

progress.pack()

# ====================================================
# STATUS
# ====================================================

status = ctk.CTkLabel(
    app,
    text="Ready...",
    font=("Segoe UI",16)
)

status.pack(pady=25)

# ====================================================
# FOOTER
# ====================================================

footer = ctk.CTkLabel(
    app,
    text=f"Version {VERSION}",
    font=("Segoe UI",12),
    text_color="gray60"
)

footer.pack(side="bottom", pady=18)

# ====================================================

app.mainloop()