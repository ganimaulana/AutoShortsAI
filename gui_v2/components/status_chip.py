from PySide6.QtWidgets import QLabel


class StatusChip(QLabel):

    READY = "ready"

    RUNNING = "running"

    WARNING = "warning"

    ERROR = "error"

    def __init__(self):

        super().__init__()

        self.setObjectName(
            "StatusChip"
        )

        self.set_status(
            self.READY
        )

    def set_status(
        self,
        status: str,
    ):

        status = status.lower()

        if status == self.READY:

            self.setText("🟢 READY")

        elif status == self.RUNNING:

            self.setText("🔵 RUNNING")

        elif status == self.WARNING:

            self.setText("🟠 WARNING")

        else:

            self.setText("🔴 ERROR")