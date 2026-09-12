-- =========================================================
-- Query 1. Partners list with deliveries count
-- PostgreSQL
-- =========================================================
-- Вывод списка партнёров с сортировкой по названию
-- и общим количеством сделанных ими доставок.
-- LEFT JOIN — партнёры без доставок тоже попадают в список.
-- =========================================================

SELECT
    p.partner_id,
    p.company_name,
    COUNT(d.delivery_id) AS deliveries_count
FROM partners p
LEFT JOIN deliveries d ON d.partner_id = p.partner_id
GROUP BY p.partner_id, p.company_name
ORDER BY p.company_name;