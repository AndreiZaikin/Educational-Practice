"""Карточка партнёра для списка на главной форме."""

import re

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)


def format_phone(value: str | None) -> str:
    """Отформатировать телефон для отображения: +7 XXX XXX XX XX."""
    if not value:
        return "—"

    digits = re.sub(r"\D", "", value)

    if len(digits) == 11 and digits[0] in ("7", "8"):
        digits = "7" + digits[1:]

    if len(digits) != 11:
        return value

    return (
        f"+{digits[0]} "
        f"{digits[1:4]} "
        f"{digits[4:7]} "
        f"{digits[7:9]} "
        f"{digits[9:11]}"
    )


class PartnerCard(QFrame):
    """Карточка с краткой информацией о партнёре."""

    doubleClicked = pyqtSignal(int)

    def __init__(self, partner: dict, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("partnerCard")
        self.setFrameShape(QFrame.NoFrame)
        self._partner = partner
        self._build()

    def mouseDoubleClickEvent(self, event) -> None:
        self.doubleClicked.emit(self._partner["partner_id"])
        super().mouseDoubleClickEvent(event)

    def _build(self) -> None:
        title_label = QLabel(self._format_title())
        title_label.setObjectName("partnerTitle")
        title_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        details_label = QLabel(self._format_details())
        details_label.setObjectName("partnerDetail")
        details_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        discount_label = QLabel(f"{self._partner['discount']}%")
        discount_label.setObjectName("partnerDiscount")
        discount_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        top_row = QHBoxLayout()
        top_row.addWidget(title_label)
        top_row.addStretch()
        top_row.addWidget(discount_label)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 15, 70, 15)
        layout.addLayout(top_row)
        layout.addWidget(details_label)

    def _format_title(self) -> str:
        # Тип партнёра хранится в отдельном справочнике; в карточке
        # выводится вместе с наименованием через разделитель.
        partner_type = self._partner.get("partner_type") or "—"
        company_name = self._partner.get("company_name") or "—"
        return f"{partner_type} | {company_name}"

    def _format_details(self) -> str:
        director = self._partner.get("director") or "—"
        phone = format_phone(self._partner.get("phone"))
        rating = self._partner.get("rating")
        rating_text = f"{rating}" if rating is not None else "—"
        return f"Директор: {director}\n{phone}\nРейтинг: {rating_text}"
