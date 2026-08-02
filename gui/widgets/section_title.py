from PySide6.QtWidgets import QLabel
from gui.theme import HEADER_FONT


class SectionTitle(QLabel):

    def __init__(self, text):
        super().__init__(text)

        self.setFont(HEADER_FONT)

        self.setMinimumHeight(36)

        self.setContentsMargins(0, 4, 0, 4)