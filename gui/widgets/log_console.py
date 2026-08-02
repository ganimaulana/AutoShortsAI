from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import QTextEdit

from datetime import datetime

from gui.widgets.card import Card


class LogConsole(Card):

    def __init__(self):
        super().__init__()

        self.console = QTextEdit()

        self.console.setReadOnly(True)

        self.console.setObjectName("LogConsole")

        self.layout.addWidget(self.console)

    # =====================================

    def append(self, text):

        now = datetime.now().strftime("%H:%M:%S")

        color = "#E5E7EB"

        icon = "•"

        upper = text.upper()

        if "SUCCESS" in upper:

            color = "#22C55E"

            icon = "✔"

        elif "ERROR" in upper:

            color = "#EF4444"

            icon = "✖"

        elif "WARNING" in upper:

            color = "#F59E0B"

            icon = "⚠"

        elif "INFO" in upper:

            color = "#38BDF8"

            icon = "ℹ"

        elif "SYSTEM" in upper:

            color = "#A855F7"

            icon = "⚙"

        html = f"""
<div style="
margin-bottom:6px;
font-family:Consolas;
font-size:12px;
">

<span style="color:#6B7280;">
[{now}]
</span>

<span style="color:{color};font-weight:bold;">
{icon}
</span>

<span style="color:white;">
{text}
</span>

</div>
"""

        self.console.insertHtml(html)

        self.console.moveCursor(
            QTextCursor.End
        )

    # =====================================

    def clear(self):

        self.console.clear()