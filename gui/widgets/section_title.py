from PySide6.QtWidgets import QLabel

from gui.theme import *


class SectionTitle(QLabel):

    def __init__(self,text):

        super().__init__(text)

        self.setFont(HEADER_FONT)