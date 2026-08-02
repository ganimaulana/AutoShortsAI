from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)

import qtawesome as qta

from gui.widgets.card import Card


class UrlCard(Card):

    def __init__(self):
        super().__init__()

        # ===================================
        # TITLE
        # ===================================

        title = QLabel("🔗 YouTube URL")
        title.setObjectName("CardTitle")

        subtitle = QLabel(
            "Paste a YouTube video URL to analyze and generate Shorts automatically."
        )
        subtitle.setObjectName("CardSubtitle")

        self.layout.addWidget(title)
        self.layout.addWidget(subtitle)

        self.layout.addSpacing(10)

        # ===================================
        # URL INPUT
        # ===================================

        row = QHBoxLayout()
        row.setSpacing(12)

        self.url_edit = QLineEdit()

        self.url_edit.setPlaceholderText(
            "https://www.youtube.com/watch?v=..."
        )

        self.url_edit.setMinimumHeight(48)

        # Paste Button

        self.paste_button = QPushButton(" Paste")

        self.paste_button.setIcon(
            qta.icon(
                "fa5s.paste",
                color="white",
            )
        )

        self.paste_button.setFixedWidth(130)
        self.paste_button.setMinimumHeight(48)

        row.addWidget(
            self.url_edit,
            1,
        )

        row.addWidget(
            self.paste_button,
        )

        self.layout.addLayout(row)

    # =====================================

    # =====================================

    def text(self):
        return self.url_edit.text().strip()

    # =====================================

    def set_text(self, text):
        self.url_edit.setText(text)

    # =====================================

    def clear_text(self):
        self.url_edit.clear()

    # =====================================

    def line_edit(self):
        return self.url_edit