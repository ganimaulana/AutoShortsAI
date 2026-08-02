from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QGraphicsDropShadowEffect,
)

from PySide6.QtGui import QColor

from gui_v2.theme import (
    Radius,
    Space,
)


class Card(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName("Card")

        shadow = QGraphicsDropShadowEffect()

        shadow.setBlurRadius(24)

        shadow.setOffset(0, 6)

        shadow.setColor(
            QColor(
                0,
                0,
                0,
                80,
            )
        )

        self.setGraphicsEffect(
            shadow
        )

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(

            Space.CARD,

            Space.CARD,

            Space.CARD,

            Space.CARD,

        )

        self.layout.setSpacing(
            Space.GAP
        )

        self.setLayout(
            self.layout
        )