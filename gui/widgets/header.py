from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from gui.theme import *

class Header(QWidget):

    def __init__(self):

        super().__init__()

        root = QHBoxLayout(self)

        root.setContentsMargins(0,0,0,0)

        #
        # Left
        #

        left = QVBoxLayout()

        title = QLabel(APP_NAME)
        title.setFont(TITLE_FONT)

        subtitle = QLabel(APP_SUBTITLE)
        subtitle.setFont(BODY_FONT)

        author = QLabel(APP_AUTHOR)
        author.setFont(SMALL_FONT)

        left.addWidget(title)
        left.addWidget(subtitle)
        left.addWidget(author)

        #
        # Right
        #

        right = QVBoxLayout()

        version = QLabel(VERSION)
        version.setFont(SMALL_FONT)

        status = QLabel("● Ready")

        status.setStyleSheet(
            "color:#22C55E;"
        )

        right.addStretch()
        right.addWidget(version)
        right.addWidget(status)

        root.addLayout(left)

        root.addStretch()

        root.addLayout(right)