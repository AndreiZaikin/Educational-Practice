-- =========================================================
-- Verification queries for Educational Practice
-- PostgreSQL
-- =========================================================
-- Три запроса, демонстрирующие покрытие бизнес-требований:
--   1. Список партнёров + количество доставок
--   2. Транзакция: новый партнёр + доставка + позиция
--   3. История отгрузок конкретного партнёра за период
--
-- Query Tool (pgAdmin) показывает результат только последнего
-- SELECT. Для запуска по отдельности используйте файлы
-- в папке split/.
-- =========================================================


-- ---------------------------------------------------------
-- 1. Список партнёров с количеством доставок
-- ---------------------------------------------------------
-- LEFT JOIN — партнёры без доставок тоже попадают в список
-- (для них COUNT вернёт 0).
-- Сортировка — по названию компании.
-- ---------------------------------------------------------
SELECT
    p.partner_id,
    p.company_name,
    COUNT(d.delivery_id) AS deliveries_count
FROM partners p
LEFT JOIN deliveries d ON d.partner_id = p.partner_id
GROUP BY p.partner_id, p.company_name
ORDER BY p.company_name;


-- ---------------------------------------------------------
-- 2. Транзакция: новый партнёр + первая доставка + позиция
-- ---------------------------------------------------------
-- Демонстрация атомарной записи связанных данных.
-- ID передаются через RETURNING, без currval().
--
-- ВНИМАНИЕ: скрипт вставляет тестовые данные.
-- При повторном запуске упадёт на UNIQUE (inn).
-- Для повторного запуска:
--   - удалите тестового партнёра, либо
--   - замените ИНН, либо
--   - замените COMMIT на ROLLBACK.
-- ---------------------------------------------------------
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


-- ---------------------------------------------------------
-- 3. История отгрузок партнёра за период
-- ---------------------------------------------------------
-- Партнёр: ООО «Логистик-Экспресс» (partner_id = 1)
-- Период: март 2026 (2026-03-01 … 2026-03-31)
-- Вывод: дата, товар, количество, сумма позиции.
-- ---------------------------------------------------------
SELECT
    p.company_name,
    d.delivery_date,
    pr.product_name,
    di.quantity,
    di.total_amount
FROM partners p
JOIN deliveries d       ON d.partner_id = p.partner_id
JOIN delivery_items di  ON di.delivery_id = d.delivery_id
JOIN products pr        ON pr.product_id = di.product_id
WHERE p.partner_id = 1
  AND d.delivery_date BETWEEN DATE '2026-03-01' AND DATE '2026-03-31'
ORDER BY d.delivery_date, pr.product_name;