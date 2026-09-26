"""Главное окно приложения: список партнёров и скидок."""

import traceback

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.db.repository import get_partners_with_discount
from app.ui.partner_card import PartnerCard
from app.ui.partner_edit_window import PartnerEditWindow
from app.ui.paths import ICON_PATH, LOGO_PATH


class MainWindow(QMainWindow):
    """Главная форма со списком партнёров."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("CRM: Реестр партнёров")
        self.resize(720, 560)
        self.setWindowIcon(QIcon(str(ICON_PATH)))
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
        logo.setPixmap(QPixmap(str(LOGO_PATH)))

        title = QLabel("Список партнёров и скидок")
        title.setObjectName("headerTitle")

        add_button = QPushButton("Добавить партнёра")
        add_button.clicked.connect(self._on_add_partner)

        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 8, 16, 8)
        layout.addWidget(logo)
        layout.addSpacing(16)
        layout.addWidget(title)
        layout.addStretch()
        layout.addWidget(add_button)

        return header

    def _build_cards_area(self) -> QWidget:
        panel = QFrame()
        panel.setObjectName("cardsPanel")
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)
        panel_layout.setSpacing(0)

        self._container = QWidget()
        self._container.setObjectName("cardsContainer")
        self._container_layout = QVBoxLayout(self._container)
        self._container_layout.setContentsMargins(0, 0, 0, 0)
        self._container_layout.setSpacing(12)

        self._reload_cards()
        panel_layout.addWidget(self._container)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(panel)

        wrapper = QWidget()
        wrapper_layout = QVBoxLayout(wrapper)
        wrapper_layout.setContentsMargins(12, 12, 12, 12)
        wrapper_layout.addWidget(scroll)
        return wrapper

    def _reload_cards(self) -> None:
        while self._container_layout.count():
            item = self._container_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        for partner in get_partners_with_discount():
            card = PartnerCard(partner)
            card.doubleClicked.connect(self._on_card_double_clicked)
            self._container_layout.addWidget(card)

        self._container_layout.addStretch()

    def _on_add_partner(self) -> None:
        try:
            dialog = PartnerEditWindow(parent=self)
            result = dialog.exec_()
        except Exception:
            traceback.print_exc()
            return

        if result == PartnerEditWindow.Accepted:
            QMessageBox.information(self, "Успех", "Партнёр добавлен.")
            self._reload_cards()

    def _on_card_double_clicked(self, partner_id: int) -> None:
        try:
            dialog = PartnerEditWindow(partner_id=partner_id, parent=self)
            result = dialog.exec_()
        except Exception:
            traceback.print_exc()
            return

        if result == PartnerEditWindow.Accepted:
            QMessageBox.information(self, "Успех", "Изменения сохранены.")
            self._reload_cards()
