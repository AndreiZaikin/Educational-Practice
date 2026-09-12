# 01. Database Design — проектирование схемы БД

## Задание

Вам необходимо спроектировать схему БД в **3-й нормальной форме (3NF)** для обеспечения функционала: просмотра партнеров, редактирования их данных и вывода истории отгрузок.

Инструкции к заданию:

* Выделите как минимум 3 сущности (например: `partners, products, sales_history/deliveries`).
* Сформулируйте ограничения целостности: первичные ключи (`PK`), внешние ключи (`FK`), ограничения `NOT NULL` и `UNIQUE` (например, для ИНН/Email партнера).
* Используйте согласованную схему именования (snake_case, множественное или единственное число для таблиц — на выбор, но строго в одном стиле).
* Сгенерируйте средствами СУБД или постройте визуально концептуальную/логическую **ER-диаграмму** и экспортируйте её в формат **PDF**.

## Реализация

### Сущности

| Таблица | Назначение |
| :--- | :--- |
| `partners` | Справочник партнёров |
| `products` | Справочник товаров |
| `deliveries` | Шапки отгрузок (накладные) |
| `delivery_items` | Позиции отгрузок |

### Связи

- `partners` 1 — N `deliveries`
- `deliveries` 1 — N `delivery_items`
- `products` 1 — N `delivery_items`

### Ограничения целостности

| Таблица | PK | FK | NOT NULL | UNIQUE |
| :--- | :--- | :--- | :--- | :--- |
| `partners` | `partner_id` | — | `company_name` | `inn`, `contact_email` |
| `products` | `product_id` | — | `product_name` | `product_name` |
| `deliveries` | `delivery_id` | `partner_id` → `partners` | `partner_id`, `delivery_date` | — |
| `delivery_items` | `delivery_item_id` | `delivery_id` → `deliveries`, `product_id` → `products` | `delivery_id`, `product_id`, `quantity`, `total_amount` | (`delivery_id`, `product_id`) |

### Правила ON DELETE

| FK | Действие |
| :--- | :--- |
| `deliveries.partner_id` | `RESTRICT` |
| `delivery_items.delivery_id` | `CASCADE` |
| `delivery_items.product_id` | `RESTRICT` |

  ## Содержимое раздела

- `er_diagram.pdf` — ER-диаграмма, сгенерированная в pgAdmin.