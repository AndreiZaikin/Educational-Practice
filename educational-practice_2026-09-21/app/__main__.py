"""Точка входа приложения CRM."""

import sys
import traceback

from PyQt5.QtWidgets import QApplication

from app.ui.main_window import MainWindow
from app.ui.paths import STYLE_PATH


def main() -> None:
    sys.excepthook = lambda *args: traceback.print_exception(*args)

    app = QApplication(sys.argv)

    with open(STYLE_PATH, encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
