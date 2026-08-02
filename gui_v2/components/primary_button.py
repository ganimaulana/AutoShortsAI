from PySide6.QtWidgets import QPushButton
import qtawesome as qta


class PrimaryButton(QPushButton):

    def __init__(
        self,
        text: str,
        icon: str | None = None,
    ):

        super().__init__(text)

        self.setMinimumHeight(46)

        self.setCursor(
            self.cursor().shape()
        )

        if icon:

            self.setIcon(

                qta.icon(
                    icon,
                    color="white",
                )

            )