-- =========================================================
-- Query 3. Delivery history for a specific partner
-- PostgreSQL
-- =========================================================
-- История отгрузок партнёра за период:
-- партнёр — ООО «Логистик-Экспресс» (partner_id = 1),
-- период  — март 2026 (2026-03-01 … 2026-03-31).
-- Вывод: дата, товар, количество, сумма позиции.
-- =========================================================

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