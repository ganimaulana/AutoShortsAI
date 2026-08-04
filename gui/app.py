print("===== GUI APP.PY =====")

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow


def main():

    app = QApplication([])

    #
    # Load Theme
    #

    with open(
        "gui/styles.qss",
        "r",
        encoding="utf-8",
    ) as f:

        app.setStyleSheet(
            f.read()
        )

    window = MainWindow()

    window.show()

    app.exec()


if __name__ == "__main__":

    main()