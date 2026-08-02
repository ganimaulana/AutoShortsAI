from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from gui.theme import (
    APP_NAME,
    APP_SUBTITLE,
    APP_AUTHOR,
    VERSION,
)


class Header(QWidget):

    def __init__(self):
        super().__init__()

        root = QHBoxLayout(self)

        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(20)

        # ==========================================
        # LEFT
        # ==========================================

        left = QVBoxLayout()

        self.title = QLabel(APP_NAME)
        self.title.setObjectName("HeaderTitle")

        self.subtitle = QLabel(APP_SUBTITLE)
        self.subtitle.setObjectName("HeaderSubtitle")

        self.author = QLabel(APP_AUTHOR)
        self.author.setObjectName("HeaderAuthor")

        left.addWidget(self.title)
        left.addWidget(self.subtitle)
        left.addSpacing(6)
        left.addWidget(self.author)

        # ==========================================
        # RIGHT
        # ==========================================

        right = QVBoxLayout()

        right.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.ready = QLabel("🟢 READY")
        self.ready.setObjectName("HeaderReady")

        self.version = QLabel(VERSION)
        self.version.setObjectName("HeaderVersion")

        right.addWidget(
            self.ready,
            alignment=Qt.AlignRight
        )

        right.addSpacing(8)

        right.addWidget(
            self.version,
            alignment=Qt.AlignRight
        )

        # ==========================================

        root.addLayout(left)

        root.addStretch()

        root.addLayout(right)