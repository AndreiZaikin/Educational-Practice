"""Слой доступа к данным: партнёры и агрегация отгрузок.

sales_history из формулировки ТЗ представлена парой таблиц
deliveries (шапки накладных) и delivery_items (позиции).
"""

import sys
from pathlib import Path

import psycopg2
import psycopg2.extras

# discount лежит в соседней папке с дефисом в имени, config — в корне этапа;
# оба импортируются через sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent / "01_business-logic"))
sys.path.append(str(Path(__file__).resolve().parent.parent))

from discount import calculate_partner_discount

import config


QUERY_PARTNERS_WITH_TOTAL = """
    SELECT
        p.partner_id,
        p.company_name,
        pt.type_name AS partner_type,
        p.director,
        p.address,
        p.phone,
        p.contact_email,
        p.rating,
        COALESCE(SUM(di.quantity), 0) AS total_quantity
    FROM partners AS p
    LEFT JOIN partner_types AS pt
        ON pt.partner_type_id = p.partner_type_id
    LEFT JOIN deliveries AS d
        ON d.partner_id = p.partner_id
    LEFT JOIN delivery_items AS di
        ON di.delivery_id = d.delivery_id
    GROUP BY
        p.partner_id,
        p.company_name,
        pt.type_name,
        p.director,
        p.address,
        p.phone,
        p.contact_email,
        p.rating
    ORDER BY
        p.company_name;
"""


def _get_connection() -> "psycopg2.extensions.connection":
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        options=f"-c search_path={config.DB_SCHEMA}",
    )


def get_partners_with_discount() -> list[dict]:
    connection = _get_connection()

    try:
        with connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor,
        ) as cursor:
            cursor.execute(QUERY_PARTNERS_WITH_TOTAL)
            rows = cursor.fetchall()
    finally:
        connection.close()

    partners: list[dict] = []

    for row in rows:
        partner = dict(row)
        # SUM() возвращает Decimal; приводим к int для calculate_partner_discount
        total_quantity = int(partner["total_quantity"])
        partner["total_quantity"] = total_quantity
        partner["discount"] = calculate_partner_discount(total_quantity)
        partners.append(partner)

    return partners
