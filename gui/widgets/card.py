from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
)


class Card(QFrame):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName("Card")

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        self.layout.setSpacing(15)

        self.setStyleSheet("""
        QFrame {
            background-color: #232326;
            border: 1px solid #3F3F46;
            border-radius: 18px;
        }
        """)