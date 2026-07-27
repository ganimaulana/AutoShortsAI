"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI
==================================================
"""

from core.pipeline import Pipeline
from core.batch_processor import BatchProcessor


# ==================================================
# Banner
# ==================================================

def banner():

    print()

    print("=" * 60)
    print("             AutoShortsAI v1.0")
    print("=" * 60)
    print()


# ==================================================
# Single URL
# ==================================================

def process_single():

    print()

    url = input(
        "YouTube URL : "
    ).strip()

    if not url:

        print()

        print("URL kosong.")

        return

    pipeline = Pipeline()

    pipeline.run(url)

    print()

    print("Selesai.")

    print()


# ==================================================
# Batch URL
# ==================================================

def process_batch():

    print()

    file = input(
        "URL file : "
    ).strip()

    if not file:

        print()

        print("File URL kosong.")

        return

    batch = BatchProcessor()

    batch.process(file)

    print()

    print("Batch selesai.")

    print()


# ==================================================
# Menu
# ==================================================

def menu():

    while True:

        banner()

        print("1. Process YouTube URL")
        print("2. Batch Processing")
        print("3. Exit")

        print()

        choice = input(
            "Choose : "
        ).strip()

        if choice == "1":

            process_single()

        elif choice == "2":

            process_batch()

        elif choice == "3":

            print()

            print("Goodbye.")

            break

        else:

            print()

            print("Pilihan tidak valid.")

            input("Tekan ENTER...")


# ==================================================
# Main
# ==================================================

def main():

    menu()


if __name__ == "__main__":

    main()