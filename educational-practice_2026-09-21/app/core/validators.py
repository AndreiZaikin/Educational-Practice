"""Валидация данных формы карточки партнёра."""

import re


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_company_name(value: str) -> str | None:
    """Вернуть текст ошибки или None, если значение корректно."""
    if not value.strip():
        return "Наименование не должно быть пустым."
    return None


def validate_email(value: str) -> str | None:
    if not value.strip():
        return "Email не должен быть пустым."
    if not EMAIL_PATTERN.match(value.strip()):
        return "Email должен быть в формате name@domain.ru."
    return None


def validate_rating(value: str) -> str | None:
    if not value.strip():
        return None
    try:
        rating = int(value)
    except ValueError:
        return "Рейтинг должен быть целым числом от 0. Удалите знаки препинания и повторите попытку."
    if rating < 0:
        return "Рейтинг должен быть целым числом от 0."
    return None


def validate_phone(value: str) -> str | None:
    if not value.strip():
        return None

    digits = re.sub(r"\D", "", value)

    if len(digits) != 11:
        return "Телефон должен содержать 11 цифр в формате +7XXXXXXXXXX."

    return None


def validate_partner_form(data: dict) -> list[str]:
    """Вернуть список ошибок по всем полям формы."""
    errors = []

    checks = [
        validate_company_name(data.get("company_name") or ""),
        validate_email(data.get("contact_email") or ""),
        validate_rating(data.get("rating_raw") or ""),
        validate_phone(data.get("phone") or ""),
    ]

    for error in checks:
        if error is not None:
            errors.append(error)

    return errors
