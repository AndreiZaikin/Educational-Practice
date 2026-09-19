# Интеграция с БД и агрегация данных (SQL + Backend)

## Постановка задачи

Функция расчета скидки принимает на вход общее количество товара. Эти данные
нужно динамически забирать из базы данных для каждого партнера.

Задача:

1. Подключите вашу базу данных к программному коду (через ORM или native-
   драйвер вроде `psycopg2`, `pyodbc`) или реализуйте программный интерфейс (API) для
   возможности асинхронного взаимодействия с клиентской стороной на базе
   JavaScript.
2. Напишите функцию/метод, который выполняет SQL-запрос с группировкой
   (`SUM(quantity)` и `LEFT JOIN`), чтобы вытащить из таблицы `sales_history` суммарный
   объем продаж по конкретному партнеру.
3. Объедините запрос к БД и функцию из Подзадания 1: на выходе должен
   получаться объект или словарь с данными партнера, дополненный его текущим
   процентом скидки.

## Состав работы

| Файл | Назначение |
|------|------------|
| `add_partner_fields.sql` | Миграция: справочник типов партнёров и поля карточки в `partners`. |
| `repository.py` | Функция `get_partners_with_discount`. |
| `check_repository.py` | Ручная проверка функции на реальной БД. |

## Реализация

### Миграция `add_partner_fields.sql`

Состав:

- создание справочника `partner_types` (`partner_type_id`, `type_name`);
- наполнение справочника значениями `ООО`, `ЗАО`, `ОАО`, `ИП`, `ПАО`;
- добавление в `partners` полей `partner_type_id`, `address`, `director`;
- внешний ключ `partners.partner_type_id → partner_types.partner_type_id`
  с правилом `ON DELETE RESTRICT`.

Тип партнёра вынесен в справочник в соответствии с 3NF. Значения
справочника используются как источник выпадающего списка в UI (ТЗ 3.10).

`CREATE TABLE IF NOT EXISTS`, `ADD COLUMN IF NOT EXISTS` и
`ON CONFLICT DO NOTHING` обеспечивают идемпотентность, кроме
`ADD CONSTRAINT FOREIGN KEY` (PostgreSQL не поддерживает `IF NOT EXISTS`
для ограничений). Миграция применяется однократно.

### Функция `get_partners_with_discount`

Возвращает `list[dict]`, один словарь на партнёра.

| Ключ | Источник |
|------|----------|
| `partner_id`, `company_name`, `director`, `address`, `phone`, `contact_email`, `rating` | `partners` |
| `partner_type` | `partner_types.type_name` |
| `total_quantity` | `COALESCE(SUM(delivery_items.quantity), 0)` |
| `discount` | `calculate_partner_discount(total_quantity)` |

Запрос использует `LEFT JOIN` от `partners` к `deliveries` и
`delivery_items`. Партнёры без отгрузок получают `total_quantity = 0`.

Таблица `sales_history` из формулировки ТЗ представлена в схеме парой
`deliveries` и `delivery_items`.

Соединение открывается на каждый вызов и закрывается в `finally`.
Параметры подключения — `config.py` (шаблон `config.example.py`,
реальный файл в `.gitignore`).

### `check_repository.py`

Выводит список партнёров с типом, директором, объёмом продаж и скидкой.
Для ручной проверки; `pytest` не собирает.

## Применение

### 1. Настройка подключения

```bash
cp config.example.py config.py
```

Заполнить в `config.py`: `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.

### 2. Миграция

```bash
psql -h <host> -U <user> -d <database> \
    -f 02_db-integration/add_partner_fields.sql
```

### 3. Проверка

```bash
cd 02_db-integration
python check_repository.py
```