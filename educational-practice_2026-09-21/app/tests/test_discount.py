"""Unit-тесты для функции calculate_partner_discount."""

import pytest

from app.core.discount import calculate_partner_discount

@pytest.mark.parametrize(
    ("total_quantity", "expected_discount"),
    [
        (0, 0),
        (9_999, 0),
        (10_000, 5),
        (49_999, 5),
        (50_000, 10),
        (299_999, 10),
        (300_000, 15),
        (300_001, 15),
    ],
)
def test_calculate_partner_discount(
    total_quantity: int,
    expected_discount: int,
) -> None:
    """Проверить расчёт скидки на пограничных значениях."""
    assert calculate_partner_discount(total_quantity) == expected_discount
