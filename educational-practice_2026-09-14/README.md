# Учебная практика 14.09.2026

## Описание

Учебная практика: разработка приложения CRM для системы учёта партнёров и их
отгрузок.

* **Язык:** Python 3.10

* **UI:** PyQt5

* **СУБД:** PostgreSQL, драйвер `psycopg2`

* **Тестирование:** pytest

---

## Структура репозитория

```text
educational-practice_2026-09-14/
├── README.md ← этот файл
├── Makefile ← команды сборки и запуска
├── requirements.txt ← зависимости
├── config.example.py ← шаблон подключения к БД
├── app.py ← точка входа приложения
├── 01_business-logic/ ← ядро бизнес-логики (расчёт скидки)
├── 02_db-integration/ ← слой доступа к данным
├── 03_ui/ ← интерфейс пользователя
└── 04_integration-debug/ ← отладка и стресс-тестирование
```

---

## Разделы

### 01. Business Logic

Изолированная функция расчёта индивидуальной скидки партнёра по суммарному
объёму продаж.

- [`README.md`](./01_business-logic/README.md)
- [`discount.py`](./01_business-logic/discount.py)
- [`test_discount.py`](./01_business-logic/test_discount.py)

### 02. DB Integration

Слой доступа к данным: SQL-запрос с `LEFT JOIN` и `SUM`, агрегация объёма
продаж, объединение с функцией расчёта скидки.

- [`README.md`](./02_db-integration/README.md)
- [`repository.py`](./02_db-integration/repository.py)
- [`add_partner_fields.sql`](./02_db-integration/add_partner_fields.sql)
- [`check_repository.py`](./02_db-integration/check_repository.py)

### 03. UI

Главное окно со списком партнёров и рассчитанными скидками.

- [`README.md`](./03_ui/README.md)
- [`main_window.py`](./03_ui/main_window.py)
- [`partner_card.py`](./03_ui/partner_card.py)
- [`style.qss`](./03_ui/style.qss)
- [`resources/`](./03_ui/resources/) — логотип и иконка приложения

### 04. Integration and Debug

Финальный прогон, отладка обработки партнёров без истории продаж,
подготовка проекта к сдаче.

- [`README.md`](./04_integration-debug/README.md)

---

## Порядок запуска

1. Установить зависимости: `pip install -r requirements.txt`.
2. Создать `config.py` из `config.example.py`, заполнить параметры
   подключения к БД.
3. Выполнить [`02_db-integration/add_partner_fields.sql`](./02_db-integration/add_partner_fields.sql) —
   миграция схемы.
4. Запустить приложение: `make run`.

## Команды Makefile

```bash
make test    # unit-тесты бизнес-логики
make check   # проверка слоя интеграции с БД
make run     # запуск приложения
make clean   # очистка кэша
```

> Файл `config.py` добавлен в `.gitignore` и в репозиторий не попадает.