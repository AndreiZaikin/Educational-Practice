"""Форма добавления и редактирования партнёра."""

import re

import psycopg2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from app.core.validators import validate_partner_form
from app.db.repository import (
    create_partner,
    get_partner_by_id,
    get_partner_types,
    update_partner,
)


class PartnerEditWindow(QDialog):
    """Диалоговое окно карточки партнёра."""

    def __init__(self, partner_id: int | None = None, parent=None) -> None:
        super().__init__(parent)
        self.setWindowModality(Qt.ApplicationModal)
        self._partner_id = partner_id
        self._initial_state: dict = {}
        self._build()
        self._setup_title()
        self._load_data()

    def _setup_title(self) -> None:
        if self._partner_id is None:
            self.setWindowTitle("CRM: Карточка партнёра [Добавление]")
        else:
            self.setWindowTitle("CRM: Карточка партнёра [Редактирование]")

    def _build(self) -> None:
        self.setFixedSize(520, 560)

        self._company_name = QLineEdit()
        self._partner_type = QComboBox()
        self._director = QLineEdit()
        self._address = QLineEdit()
        self._phone = QLineEdit()
        self._phone.setPlaceholderText("+7XXXXXXXXXX")
        self._email = QLineEdit()
        self._email.setPlaceholderText("name@domain.ru")
        self._rating = QLineEdit()
        self._rating.setPlaceholderText("Целое число от 0")

        form = QFormLayout()
        form.addRow("Наименование *", self._company_name)
        form.addRow("Тип партнёра", self._partner_type)
        form.addRow("Рейтинг", self._rating)
        form.addRow("Адрес", self._address)
        form.addRow("ФИО директора", self._director)
        form.addRow("Телефон", self._phone)
        form.addRow("Email *", self._email)

        save_button = QPushButton("Сохранить")
        save_button.clicked.connect(self._on_save)

        cancel_button = QPushButton("Отмена")
        cancel_button.clicked.connect(self._on_cancel)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(cancel_button)
        buttons_layout.addWidget(save_button)

        note = QLabel("* — обязательные поля")
        note.setObjectName("formNote")

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(note)
        layout.addStretch()
        layout.addLayout(buttons_layout)

    def _load_data(self) -> None:
        self._fill_partner_types()

        if self._partner_id is None:
            self._initial_state = self._collect_form_data()
            return

        partner = get_partner_by_id(self._partner_id)

        if partner is None:
            QMessageBox.critical(
                self,
                "Ошибка",
                "Партнёр не найден в базе данных.",
            )
            self.reject()
            return

        self._company_name.setText(partner["company_name"] or "")
        self._director.setText(partner["director"] or "")
        self._address.setText(partner["address"] or "")
        self._phone.setText(partner["phone"] or "")
        self._email.setText(partner["contact_email"] or "")
        self._rating.setText(
            str(partner["rating"]) if partner["rating"] is not None else ""
        )

        # partner_type_id может быть None — выбираем пустой пункт списка
        index = self._partner_type.findData(partner["partner_type_id"])
        self._partner_type.setCurrentIndex(index if index >= 0 else 0)

        self._initial_state = self._collect_form_data()

    def _fill_partner_types(self) -> None:
        self._partner_type.addItem("<не выбран>", None)

        for partner_type in get_partner_types():
            self._partner_type.addItem(
                partner_type["type_name"],
                partner_type["partner_type_id"],
            )

    def _normalize_phone(self) -> str | None:
        """Привести телефон к +7XXXXXXXXXX или вернуть исходный текст."""
        digits = re.sub(r"\D", "", self._phone.text())

        if not digits:
            return None

        if len(digits) == 11 and digits[0] in ("7", "8"):
            return "+7" + digits[1:]

        if len(digits) == 10:
            return "+7" + digits

        return self._phone.text().strip()

    def _collect_form_data(self) -> dict:
        rating_text = self._rating.text().strip()

        return {
            "company_name": self._company_name.text().strip(),
            "partner_type_id": self._partner_type.currentData(),
            "director": self._director.text().strip() or None,
            "address": self._address.text().strip() or None,
            "phone": self._normalize_phone(),
            "contact_email": self._email.text().strip(),
            "rating": int(rating_text) if rating_text.isdigit() else None,
            "rating_raw": rating_text,
        }

    def _is_dirty(self) -> bool:
        return self._collect_form_data() != self._initial_state

    def _on_save(self) -> None:
        data = self._collect_form_data()
        errors = validate_partner_form(data)

        if errors:
            QMessageBox.critical(
                self,
                "Ошибка валидации",
                "\n".join(errors),
            )
            return

        payload = {
            key: value
            for key, value in data.items()
            if key != "rating_raw"
        }

        try:
            if self._partner_id is None:
                create_partner(payload)
            else:
                update_partner(self._partner_id, payload)
        except psycopg2.IntegrityError as error:
            QMessageBox.critical(
                self,
                "Ошибка сохранения",
                f"СУБД отклонила данные: {error}",
            )
            return
        except psycopg2.Error as error:
            QMessageBox.critical(
                self,
                "Ошибка СУБД",
                f"Не удалось сохранить партнёра: {error}",
            )
            return

        self.accept()

    def _on_cancel(self) -> None:
        if not self._is_dirty():
            self.reject()
            return

        answer = QMessageBox.warning(
            self,
            "Несохранённые изменения",
            "Изменения будут потеряны. Продолжить?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if answer == QMessageBox.Yes:
            self.reject()
