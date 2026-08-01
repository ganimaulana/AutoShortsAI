"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Batch Runner
==================================================
"""

from core.pipeline import Pipeline


class BatchRunner:

    def __init__(self, callback=None):

        self.pipeline = Pipeline(
            callback=callback
        )

    # -------------------------------------------------

    def run(self, urls):

        results = []

        for index, url in enumerate(
            urls,
            start=1,
        ):

            print()

            print("=" * 60)

            print(
                f"[{index}/{len(urls)}] {url}"
            )

            print("=" * 60)

            result = self.pipeline.run(url)

            results.append(result)

        return results