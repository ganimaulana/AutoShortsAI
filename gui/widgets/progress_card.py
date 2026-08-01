from PySide6.QtWidgets import QProgressBar


class ProgressCard(QProgressBar):

    def __init__(self):

        super().__init__()

        self.setRange(0,100)

        self.setValue(0)

    def progress(self,value):

        self.setValue(value)