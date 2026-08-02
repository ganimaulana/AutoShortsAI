"""
==================================================
Header Bar
==================================================
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from gui_v2.components.base_card import BaseCard
from gui_v2.components.status_chip import StatusChip
from gui_v2.theme import (
    APP_NAME,
    APP_VERSION,
)


class HeaderBar(BaseCard):

    def build_ui(self):

        super().build_ui()

        root = QHBoxLayout()

        # ==========================
        # LEFT
        # ==========================

        left = QVBoxLayout()

        self.title = QLabel(APP_NAME)
        self.title.setObjectName("HeaderTitle")

        self.subtitle = QLabel(
            "AI Video Automation Platform"
        )
        self.subtitle.setObjectName(
            "HeaderSubtitle"
        )

        left.addWidget(self.title)
        left.addWidget(self.subtitle)

        # ==========================
        # RIGHT
        # ==========================

        right = QVBoxLayout()

        right.setAlignment(
            Qt.AlignRight
        )

        self.status = StatusChip()

        self.version = QLabel(
            f"Version {APP_VERSION}"
        )

        self.version.setObjectName(
            "VersionLabel"
        )

        right.addWidget(
            self.status,
            alignment=Qt.AlignRight
        )

        right.addWidget(
            self.version,
            alignment=Qt.AlignRight
        )

        root.addLayout(left)

        root.addStretch()

        root.addLayout(right)

        self.layout.addLayout(root)