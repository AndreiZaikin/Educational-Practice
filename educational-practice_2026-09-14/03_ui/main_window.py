"""Главное окно приложения: список партнёров и скидок."""

import sys
from pathlib import Path

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

sys.path.append(str(Path(__file__).resolve().parent.parent / "02_db-integration"))

from repository import get_partners_with_discount

from partner_card import PartnerCard


UI_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = UI_DIR / "resources"


class MainWindow(QMainWindow):
    """Главная форма со списком партнёров."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("CRM: Список партнёров и скидок")
        self.resize(720, 560)
        self.setWindowIcon(QIcon(str(RESOURCES_DIR / "icon.png")))
        self._build()

    def _build(self) -> None:
        header = self._build_header()
        cards_area = self._build_cards_area()

        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)
        root_layout.addWidget(header)
        root_layout.addWidget(cards_area, stretch=1)

        self.setCentralWidget(root)

    def _build_header(self) -> QWidget:
        header = QWidget()
        header.setObjectName("header")
        header.setFixedHeight(80)

        logo = QLabel()
        logo.setPixmap(
            QPixmap(str(RESOURCES_DIR / "logo.png"))
        )

        title = QLabel("Список партнёров и скидок")
        title.setObjectName("headerTitle")

        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.addWidget(logo)
        layout.addSpacing(16)
        layout.addWidget(title)
        layout.addStretch()

        return header

    def _build_cards_area(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("cardsPanel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)
        panel_layout.setSpacing(0)

        container = QWidget()
        container.setObjectName("cardsContainer")
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(12)

        partners = get_partners_with_discount()
        for partner in partners:
            container_layout.addWidget(PartnerCard(partner))

        container_layout.addStretch()
        panel_layout.addWidget(container)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(panel)

        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(12, 12, 12, 12)
        wrapper_layout.addWidget(scroll)
        return wrapper


def main() -> None:
    app = QApplication(sys.argv)

    style_path = UI_DIR / "style.qss"
    with open(style_path, encoding="utf-8") as style_file:
        app.setStyleSheet(style_file.read())

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
