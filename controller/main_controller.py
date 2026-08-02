"""
==========================================================
Main Controller

Bridge antara GUI dan Business Logic.

Author : Gani Creative Studio
==========================================================
"""

from PySide6.QtCore import QObject


class MainController(QObject):

    def __init__(self, window):

        super().__init__()

        self.window = window

    # ---------------------------------------------

    def initialize(self):

        pass

    # ---------------------------------------------

    def analyze(self):

        pass

    # ---------------------------------------------

    def start_pipeline(self):

        pass

    # ---------------------------------------------

    def stop_pipeline(self):

        pass