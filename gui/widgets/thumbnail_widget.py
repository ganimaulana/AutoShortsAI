from PySide6.QtWidgets import QLabel, QSizePolicy
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class ThumbnailWidget(QLabel):

    def __init__(self):

        super().__init__()

        self.setFixedSize(340, 190)

        self.setAlignment(Qt.AlignCenter)

        self.setText(

        "No Thumbnail\n\nPaste YouTube URL"

        )

        self.setStyleSheet("""
            QLabel{
                background:#1E1E1E;
                border:1px solid #3F3F46;
                border-radius:12px;
                color:#888;
            }
        """)

    def set_thumbnail(self, image_path):

        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            return

        pixmap = pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        self.setPixmap(pixmap)