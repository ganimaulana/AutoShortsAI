from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel

from gui.widgets.card import Card


class ThumbnailWidget(Card):

    def __init__(self):
        super().__init__()

        self.image = QLabel()

        self.image.setAlignment(Qt.AlignCenter)

        self.image.setMinimumSize(360, 202)
        self.image.setMaximumSize(360, 202)

        self.image.setObjectName("Thumbnail")

        self.image.setText("No Thumbnail")

        self.layout.addWidget(
            self.image,
            alignment=Qt.AlignCenter,
        )

    # =====================================

    def setPixmap(self, pixmap):

        if pixmap.isNull():
            return

        self.image.setPixmap(

            pixmap.scaled(

                self.image.size(),

                Qt.KeepAspectRatioByExpanding,

                Qt.SmoothTransformation,

            )

        )

    # =====================================

    def clear(self):

        self.image.clear()

        self.image.setText("No Thumbnail")

    # =====================================

    def setText(self, text):

        self.image.setText(text)

    # =====================================

    def size(self):

        return self.image.size()