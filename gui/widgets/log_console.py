"""
==================================================
Naraseta Studio

Log Console
==================================================
"""

from datetime import datetime

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QTextEdit,
    QVBoxLayout,
)

from gui.widgets.card import Card
from gui.widgets.section_title import SectionTitle


class LogConsole(Card):

    def __init__(self):

        super().__init__()

        SectionTitle(
            "📜 System Log"
        )

        self.console = QTextEdit()

        self.console.setReadOnly(True)

        self.layout.addWidget(
            self.console
        )

    def append(self, message):

        timestamp = datetime.now().strftime("%H:%M:%S")

        color = "#FFFFFF"

        if "[ERROR]" in message:
            color = "#EF4444"

        elif "[SUCCESS]" in message:
            color = "#22C55E"

        elif "[INFO]" in message:
            color = "#3B82F6"

        elif "[SYSTEM]" in message:
            color = "#A1A1AA"

        self.console.append(

            f'<span style="color:{color}">'
            f'[{timestamp}] {message}'
            f'</span>'

        )

        self.console.ensureCursorVisible()

    def clear_console(self):

        self.console.clear()