"""Карточка партнёра для списка на главной форме."""

from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)


class PartnerCard(QFrame):
    """Карточка с краткой информацией о партнёре."""

    def __init__(self, partner: dict, parent=None) -> None:
        super().__init__(parent)
        self.setObjectName("partnerCard")
        self.setFrameShape(QFrame.NoFrame)
        self._partner = partner
        self._build()

    def _build(self) -> None:
        title_label = QLabel(self._format_title())
        title_label.setObjectName("partnerTitle")

        details_label = QLabel(self._format_details())
        details_label.setObjectName("partnerDetail")

        discount_label = QLabel(f"{self._partner['discount']}%")
        discount_label.setObjectName("partnerDiscount")

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
        phone = self._partner.get("phone") or "—"
        rating = self._partner.get("rating")
        rating_text = f"{rating}" if rating is not None else "—"
        return f"Директор: {director}\n{phone}\nРейтинг: {rating_text}"
