import sys

print("1. Program started")

from PySide6.QtWidgets import QApplication

print("2. PySide imported")

from gui.main_window import MainWindow

print("3. MainWindow imported")

from gui.theme import DARK_THEME

print("4. Theme imported")


def main():

    print("5. Creating QApplication")

    app = QApplication(sys.argv)

    print("6. Applying theme")

    app.setStyleSheet(DARK_THEME)

    print("7. Creating window")

    window = MainWindow()

    print("8. Showing window")

    window.show()

    print("9. Executing app")

    sys.exit(app.exec())


if __name__ == "__main__":
    main()