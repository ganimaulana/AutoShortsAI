from PySide6.QtWidgets import QLineEdit


class InputField(QLineEdit):

    def __init__(
        self,
        placeholder="",
    ):

        super().__init__()

        self.setPlaceholderText(
            placeholder
        )

        self.setMinimumHeight(48)

    def value(self):

        return self.text().strip()

    def clear_value(self):

        self.clear()