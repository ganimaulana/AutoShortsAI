from PySide6.QtWidgets import (
    QLabel,
    QFormLayout,
)

from gui.widgets.card import Card
from gui.widgets.section_title import SectionTitle

from gui.theme import BODY_FONT


class InfoCard(Card):

    def __init__(self):

        super().__init__()

        self.layout.addWidget(
            SectionTitle(
                "📄 Video Information"
            )
        )

        form = QFormLayout()
        form.setSpacing(12)

        self.title = QLabel("-")
        self.channel = QLabel("-")
        self.views = QLabel("-")
        self.duration = QLabel("-")
        self.language = QLabel("-")
        self.upload = QLabel("-")
        self.resolution = QLabel("-")

        labels = [
            ("Title", self.title),
            ("Channel", self.channel),
            ("Views", self.views),
            ("Duration", self.duration),
            ("Language", self.language),
            ("Upload", self.upload),
            ("Resolution", self.resolution),
        ]

        for text, widget in labels:
            widget.setWordWrap(True)
            widget.setFont(BODY_FONT)
            form.addRow(text + " :", widget)

        self.layout.addLayout(form)

    def update_info(self, metadata):

        self.title.setText(
            metadata.get("title", "-")
        )

        self.channel.setText(
            metadata.get("channel", "-")
        )

        self.views.setText(
            metadata.get("views_text", "-")
        )

        self.duration.setText(
            metadata.get("duration_text", "-")
        )

        self.language.setText(
            metadata.get("language", "-")
        )

        self.upload.setText(
            metadata.get("upload_date", "-")
        )

        self.resolution.setText(
            metadata.get("resolution", "-")
        )