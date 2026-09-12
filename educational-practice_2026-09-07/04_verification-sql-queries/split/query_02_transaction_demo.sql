-- =========================================================
-- Query 2. Transaction demo
-- PostgreSQL
-- =========================================================
-- Демонстрация транзакции: создание нового партнёра,
-- его первой доставки и позиции доставки
-- в рамках одного блока BEGIN...COMMIT.
--
-- ВНИМАНИЕ: скрипт вставляет тестовые данные.
-- При повторном запуске упадёт на UNIQUE (inn).
-- Для повторного запуска:
--   - удалите тестового партнёра, либо
--   - замените ИНН, либо
--   - замените COMMIT на ROLLBACK.
-- =========================================================

BEGIN;

WITH new_partner AS (
    INSERT INTO partners (company_name, inn, contact_email, phone, rating)
    VALUES ('ООО "Тестовый партнёр"', '9999999999', 'test@example.com', NULL, NULL)
    RETURNING partner_id
),
new_delivery AS (
    INSERT INTO deliveries (partner_id, delivery_date)
    SELECT partner_id, DATE '2026-04-01' FROM new_partner
    RETURNING delivery_id
)
INSERT INTO delivery_items (delivery_id, product_id, quantity, total_amount)
SELECT delivery_id, 1, 5, 2500 FROM new_delivery;

COMMIT;