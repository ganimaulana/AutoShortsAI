"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Batch Processor
==================================================
"""

from pathlib import Path

from core.pipeline import Pipeline


class BatchProcessor:

    def __init__(self):

        self.pipeline = Pipeline()

    # -------------------------------------------------

    def process(

        self,

        url_file,

    ):

        url_file = Path(url_file)

        if not url_file.exists():

            raise FileNotFoundError(url_file)

        urls = []

        with open(

            url_file,

            "r",

            encoding="utf-8",

        ) as f:

            for line in f:

                line = line.strip()

                if line:

                    urls.append(line)

        total = len(urls)

        print()

        print("=" * 60)

        print(f"Found {total} URLs")

        print("=" * 60)

        print()

        for i, url in enumerate(

            urls,

            start=1,

        ):

            print()

            print("=" * 60)

            print(

                f"[{i}/{total}]"

            )

            print(url)

            print("=" * 60)

            print()

            try:

                self.pipeline.run(

                    url

                )

            except Exception as e:

                print()

                print(

                    "FAILED"

                )

                print(e)

                print()

        print()

        print("=" * 60)

        print("Batch Finished")

        print("=" * 60)