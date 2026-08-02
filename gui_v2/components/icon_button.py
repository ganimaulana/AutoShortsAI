import qtawesome as qta

from PySide6.QtWidgets import QPushButton


class IconButton(QPushButton):

    def __init__(
        self,
        text,
        icon,
    ):

        super().__init__(text)

        self.setMinimumHeight(46)

        self.setIcon(

            qta.icon(
                icon,
                color="white",
            )

        )