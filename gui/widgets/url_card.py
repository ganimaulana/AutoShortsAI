"""
==================================================
Naraseta Studio

URL Card
==================================================
"""

from PySide6.QtWidgets import QLineEdit

from gui.widgets.card import Card
from gui.widgets.section_title import SectionTitle


class UrlCard(Card):

    def __init__(self):

        super().__init__()

        self.layout.addWidget(
            SectionTitle("YouTube URL")
        )

        self.url_edit = QLineEdit()

        self.url_edit.setPlaceholderText(
            "Paste YouTube URL..."
        )

        self.layout.addWidget(
            self.url_edit
        )

    def text(self):

        return self.url_edit.text().strip()

    def clear(self):

        self.url_edit.clear()