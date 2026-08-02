"""
==========================================================
Base Card

Semua Card pada GUI V2 mewarisi class ini.
==========================================================
"""

from PySide6.QtWidgets import QVBoxLayout

from gui_v2.components.base_widget import BaseWidget


class BaseCard(BaseWidget):

    def build_ui(self):

        self.setObjectName("Card")

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            24,
            24,
            24,
            24,
        )

        self.layout.setSpacing(18)