-- =========================================================
-- Import script for Educational Practice
-- PostgreSQL
-- =========================================================

-- ---------------------------------------------------------
-- 1. Очистка таблиц
-- ---------------------------------------------------------
TRUNCATE delivery_items, deliveries, products, partners RESTART IDENTITY CASCADE;

-- ---------------------------------------------------------
-- 2. Импорт данных
-- ---------------------------------------------------------

COPY partners (partner_id, company_name, inn, contact_email, phone, rating)
FROM 'D:/Hexlet/hexlet-4-year/Educational-Practice/educational-practice_2026-09-07/03_etl/data/partners.csv'
WITH (FORMAT csv, HEADER true, NULL '');

COPY products (product_id, product_name)
FROM 'D:/Hexlet/hexlet-4-year/Educational-Practice/educational-practice_2026-09-07/03_etl/data/products.csv'
WITH (FORMAT csv, HEADER true, NULL '');

COPY deliveries (delivery_id, partner_id, delivery_date)
FROM 'D:/Hexlet/hexlet-4-year/Educational-Practice/educational-practice_2026-09-07/03_etl/data/deliveries.csv'
WITH (FORMAT csv, HEADER true, NULL '');

COPY delivery_items (delivery_item_id, delivery_id, product_id, quantity, total_amount)
FROM 'D:/Hexlet/hexlet-4-year/Educational-Practice/educational-practice_2026-09-07/03_etl/data/delivery_items.csv'
WITH (FORMAT csv, HEADER true, NULL '');

-- ---------------------------------------------------------
-- 3. Синхронизация последовательностей
-- ---------------------------------------------------------
-- После явной вставки PK из файлов необходимо восстановить последовательности
-- ---------------------------------------------------------
SELECT setval('partners_partner_id_seq',
              (SELECT MAX(partner_id) FROM partners));

SELECT setval('products_product_id_seq',
              (SELECT MAX(product_id) FROM products));

SELECT setval('deliveries_delivery_id_seq',
              (SELECT MAX(delivery_id) FROM deliveries));

SELECT setval('delivery_items_delivery_item_id_seq',
              (SELECT MAX(delivery_item_id) FROM delivery_items));

-- ---------------------------------------------------------
-- 4. Проверочные запросы
-- ---------------------------------------------------------
SELECT '1. partners' AS table_name, COUNT(*) AS table_count, 4 AS data_count FROM partners
UNION ALL
SELECT '2. products', COUNT(*), 3 FROM products
UNION ALL
SELECT '3. deliveries', COUNT(*), 5 FROM deliveries
UNION ALL
SELECT '4. delivery_items', COUNT(*), 5 FROM delivery_items
ORDER BY table_name;