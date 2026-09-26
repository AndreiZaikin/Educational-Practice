"""Ручная проверка get_partners_with_discount на реальной БД."""

from app.db.repository import get_partners_with_discount


def main() -> None:
    partners = get_partners_with_discount()

    if not partners:
        print("Список партнёров пуст.")
        return

    print(f"Всего партнёров: {len(partners)}")
    print("-" * 80)

    for partner in partners:
        print(
            f"[{partner['partner_id']}] "
            f"{partner['partner_type'] or '—'} {partner['company_name']} | "
            f"директор: {partner['director'] or '—'} | "
            f"объём: {partner['total_quantity']} | "
            f"скидка: {partner['discount']}%"
        )


if __name__ == "__main__":
    main()