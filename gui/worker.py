"""
==================================================
Gani Creative Studio
Powered by Naraseta

AutoShortsAI

Pipeline Worker
==================================================
"""

import traceback

from PySide6.QtCore import QObject
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot

from core.pipeline import Pipeline


class PipelineWorker(QObject):

    #
    # Signals
    #

    finished = Signal(object)

    error = Signal(str)

    log = Signal(str)

    # ---------------------------------------------

    def __init__(self, url):

        super().__init__()

        self.url = url

        from core.cancel_token import CancelToken

        self.cancel_token = CancelToken()

    # ---------------------------------------------

    def cancel(self):

        self.cancel_token.cancel()

    # ---------------------------------------------

    @Slot()
    def run(self):

        try:

            pipeline = Pipeline(
                callback=self.log.emit,
                cancel_token=self.cancel_token,
            )

            context = pipeline.run(
                self.url
            )

            self.finished.emit(
                context
            )

        except Exception as e:

            # Print traceback lengkap ke terminal
            traceback.print_exc()

            # Kirim traceback lengkap ke GUI
            self.error.emit(
                f"{str(e)}\n\n{traceback.format_exc()}"
            )