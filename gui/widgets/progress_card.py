from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QVBoxLayout,
)

from gui.widgets.card import Card
from gui.widgets.section_title import SectionTitle


class ProgressCard(Card):

    def __init__(self):
        super().__init__()

        self.layout.setSpacing(12)

        self.layout.addWidget(
            SectionTitle("📊 Pipeline Progress")
        )

        # Status
        self.status = QLabel("🟢 Ready")
        self.status.setStyleSheet("""
            color:#22C55E;
            font-size:12pt;
            font-weight:bold;
        """)

        self.layout.addWidget(self.status)

        # Progress Bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setMinimumHeight(24)

        self.layout.addWidget(self.progress)

        # Step
        self.step = QLabel("Waiting...")
        self.step.setStyleSheet("""
            color:#A1A1AA;
            font-size:10pt;
        """)

        self.layout.addWidget(self.step)

        self.layout.addStretch()

    def set_progress(self, value):
        self.progress.setValue(value)

    def set_status(self, text):

        self.status.setText(f"🟢 {text}")

        self.step.setText(text)