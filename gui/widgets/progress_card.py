from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
)

from gui.widgets.card import Card
from gui.widgets.section_title import SectionTitle


class ProgressCard(Card):

    def __init__(self):

        super().__init__()

        self.layout.addWidget(
            SectionTitle(
                "📊 Pipeline Progress"
            )
        )

        self.progress = QProgressBar()

        self.progress.setRange(0, 100)

        self.progress.setValue(0)

        self.layout.addWidget(
            self.progress
        )

        self.status = QLabel("Ready")

        self.status.setStyleSheet(
            "color:#22C55E;font-weight:bold;"
        )

        self.layout.addWidget(
            self.status
        )

    def set_progress(self, value):

        self.progress.setValue(value)

    def set_status(self, text):

        self.status.setText(text)