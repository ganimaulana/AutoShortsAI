from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QVBoxLayout, QGraphicsDropShadowEffect
from PySide6.QtGui import QColor


class Card(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("Card")

        self.setFrameShape(QFrame.NoFrame)

        self.setAttribute(Qt.WA_StyledBackground, True)

        shadow = QGraphicsDropShadowEffect(self)

        shadow.setBlurRadius(28)
        shadow.setOffset(0, 6)
        shadow.setColor(QColor(0, 0, 0, 60))

        self.setGraphicsEffect(shadow)

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            24,
            22,
            24,
            22,
        )

        self.layout.setSpacing(18)

        self.setLayout(self.layout)