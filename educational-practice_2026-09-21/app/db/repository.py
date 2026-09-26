"""Слой доступа к данным: партнёры, отгрузки и CRUD-операции.

sales_history из формулировки ТЗ представлена парой таблиц
deliveries (шапки накладных) и delivery_items (позиции).
"""

import psycopg2
import psycopg2.extras

from app import config
from app.core.discount import calculate_partner_discount


QUERY_PARTNERS_WITH_TOTAL = """
    SELECT
        p.partner_id,
        p.company_name,
        pt.type_name AS partner_type,
        p.partner_type_id,
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
        p.partner_type_id,
        p.director,
        p.address,
        p.phone,
        p.contact_email,
        p.rating
    ORDER BY
        p.company_name;
"""

QUERY_PARTNER_BY_ID = """
    SELECT
        partner_id,
        company_name,
        partner_type_id,
        director,
        address,
        phone,
        contact_email,
        rating
    FROM partners
    WHERE partner_id = %s;
"""

QUERY_PARTNER_TYPES = """
    SELECT partner_type_id, type_name
    FROM partner_types
    ORDER BY type_name;
"""

INSERT_PARTNER = """
    INSERT INTO partners (
        company_name, partner_type_id, director, address, phone, contact_email, rating
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING partner_id;
"""

UPDATE_PARTNER = """
    UPDATE partners
    SET company_name = %s,
        partner_type_id = %s,
        director = %s,
        address = %s,
        phone = %s,
        contact_email = %s,
        rating = %s
    WHERE partner_id = %s;
"""

DELETE_PARTNER = "DELETE FROM partners WHERE partner_id = %s;"


def _get_connection() -> "psycopg2.extensions.connection":
    return psycopg2.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        dbname=config.DB_NAME,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        options=f"-c search_path={config.DB_SCHEMA}",
    )


def _normalize_row(row: dict) -> dict:
    """Привести типы полей партнёра к удобным для UI."""
    partner = dict(row)
    if "total_quantity" in partner:
        partner["total_quantity"] = int(partner["total_quantity"])
    if partner.get("rating") is not None:
        partner["rating"] = int(partner["rating"])
    return partner


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
        partner = _normalize_row(row)
        partner["discount"] = calculate_partner_discount(partner["total_quantity"])
        partners.append(partner)

    return partners


def get_partner_by_id(partner_id: int) -> dict | None:
    connection = _get_connection()

    try:
        with connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor,
        ) as cursor:
            cursor.execute(QUERY_PARTNER_BY_ID, (partner_id,))
            row = cursor.fetchone()
    finally:
        connection.close()

    if row is None:
        return None

    return _normalize_row(row)


def get_partner_types() -> list[dict]:
    connection = _get_connection()

    try:
        with connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor,
        ) as cursor:
            cursor.execute(QUERY_PARTNER_TYPES)
            rows = cursor.fetchall()
    finally:
        connection.close()

    return [dict(row) for row in rows]


def create_partner(data: dict) -> int:
    connection = _get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                INSERT_PARTNER,
                (
                    data["company_name"],
                    data["partner_type_id"],
                    data["director"],
                    data["address"],
                    data["phone"],
                    data["contact_email"],
                    data["rating"],
                ),
            )
            partner_id = cursor.fetchone()[0]
        connection.commit()
    finally:
        connection.close()

    return partner_id


def update_partner(partner_id: int, data: dict) -> None:
    connection = _get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                UPDATE_PARTNER,
                (
                    data["company_name"],
                    data["partner_type_id"],
                    data["director"],
                    data["address"],
                    data["phone"],
                    data["contact_email"],
                    data["rating"],
                    partner_id,
                ),
            )
        connection.commit()
    finally:
        connection.close()


def delete_partner(partner_id: int) -> None:
    connection = _get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(DELETE_PARTNER, (partner_id,))
        connection.commit()
    finally:
        connection.close()
