from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QWidget,
    QGridLayout,
)

from gui.widgets.card import Card


class InfoCard(Card):

    def __init__(self):
        super().__init__()

        title = QLabel("🎬 Video Information")
        title.setObjectName("CardTitle")

        self.layout.addWidget(title)

        self.layout.addSpacing(8)

        grid = QGridLayout()

        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(16)

        self.data = {}

        items = [

            ("Title", "title"),

            ("Channel", "channel"),

            ("Views", "views_text"),

            ("Duration", "duration_text"),

            ("Language", "language"),

            ("Upload", "upload_date"),

            ("Resolution", "resolution"),

        ]

        for row, (label, key) in enumerate(items):

            left = QLabel(label)

            left.setObjectName("InfoLabel")

            value = QLabel("-")

            value.setObjectName("InfoValue")

            value.setWordWrap(True)

            value.setAlignment(
                Qt.AlignLeft | Qt.AlignTop
            )

            self.data[key] = value

            grid.addWidget(
                left,
                row,
                0,
            )

            grid.addWidget(
                value,
                row,
                1,
            )

        self.layout.addLayout(grid)

        self.layout.addStretch()

    # ====================================

    def clear(self):

        for widget in self.data.values():

            widget.setText("-")

    # ====================================

    def update_info(self, info):

        if not info:

            self.clear()

            return

        for key, widget in self.data.items():

            widget.setText(

                str(

                    info.get(
                        key,
                        "-"
                    )

                )

            )