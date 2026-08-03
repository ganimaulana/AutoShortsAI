from datetime import datetime

from PySide6.QtGui import QColor
from PySide6.QtGui import QTextCursor

from PySide6.QtWidgets import QTextEdit

from gui.widgets.card import Card
from gui.widgets.section_title import SectionTitle


class LogConsole(Card):

    COLORS = {

        "INFO": "#3B82F6",

        "SUCCESS": "#22C55E",

        "WARNING": "#F59E0B",

        "ERROR": "#EF4444",

    }

    def __init__(self):

        super().__init__()

        self.layout.addWidget(

            SectionTitle(

                "🖥 Log Console"

            )

        )

        self.console = QTextEdit()

        self.console.setReadOnly(True)

        self.console.setMinimumHeight(220)

        self.layout.addWidget(

            self.console

        )

    def log(

        self,

        message,

        level="INFO",

    ):

        color = self.COLORS.get(

            level,

            "#FFFFFF",

        )

        now = datetime.now().strftime(

            "%H:%M:%S"

        )

        self.console.setTextColor(

            QColor(color)

        )

        self.console.append(

            f"[{now}] [{level}] {message}"

        )

        self.console.moveCursor(

            QTextCursor.End

        )

    def clear_logs(self):

        self.console.clear()