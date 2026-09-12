# Учебная практика 07.09.2026

## Описание

Учебная практика: проектирование, развёртывание и наполнение базы данных для системы учёта партнёров и их отгрузок.

* **СУБД:** PostgreSQL

* **Схема:** 3NF

* **Сущности:** `partners`, `products`, `deliveries`, `delivery_items`

---

## Структура репозитория

```text
educational-practice_2026-09-07/
├── README.md ← этот файл
├── 01_database-design/ ← проектирование схемы + ER-диаграмма
├── 02_ddl-script/ ← DDL-скрипт развёртывания
├── 03_etl/ ← очистка данных + импорт
└── 04_verification-sql-queries/ ← проверочные запросы
```

---

## Разделы

### 01. Database Design

Проектирование схемы БД в 3NF, ER-диаграмма.

- [`README.md`](./01_database-design/README.md)
- [`er_diagram.pdf`](./01_database-design/er_diagram.pdf)

### 02. DDL Script

Скрипт развёртывания структуры БД.

- [`README.md`](./02_ddl-script/README.md)
- [`schema.sql`](./02_ddl-script/schema.sql)

### 03. ETL

Очистка исходных данных, импорт в СУБД, проверка количества строк.

- [`README.md`](./03_etl/README.md)
- [`import.sql`](./03_etl/import.sql)
- [`data/raw/`](./03_etl/data/raw/) — исходные файлы
- [`data/`](./03_etl/data/) — очищенные файлы

### 04. Verification SQL Queries

Запросы, демонстрирующие покрытие бизнес-требований.

- [`README.md`](./04_verification-sql-queries/README.md)
- [`queries.sql`](./04_verification-sql-queries/queries.sql)
- [`split/`](./04_verification-sql-queries/split/) — те же запросы по одному в файле

---

## Порядок запуска

1. Выполнить [`02_ddl-script/schema.sql`](./02_ddl-script/schema.sql) — создание таблиц.
2. Выполнить [`03_etl/import.sql`](./03_etl/import.sql) — импорт данных.
3. Выполнить запросы из [`04_verification-sql-queries/`](./04_verification-sql-queries/) — проверка.

> Пути к CSV в `import.sql` — абсолютные и привязаны к машине автора. При запуске на другой машине замените их на свои.