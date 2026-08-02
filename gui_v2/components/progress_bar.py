from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QProgressBar,
)


class ProgressBar(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout(self)

        layout.setSpacing(10)

        self.percent = QLabel("0%")

        self.percent.setObjectName(
            "ProgressPercent"
        )

        layout.addWidget(
            self.percent
        )

        self.bar = QProgressBar()

        self.bar.setRange(
            0,
            100,
        )

        self.bar.setTextVisible(
            False
        )

        layout.addWidget(
            self.bar
        )

    def set_value(
        self,
        value: int,
    ):

        self.bar.setValue(value)

        self.percent.setText(
            f"{value}%"
        )