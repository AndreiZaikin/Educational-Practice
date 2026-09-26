# Учебная практика 21.09.2026

## Описание

Учебная практика: разработка многооконного приложения CRM с формами
добавления и редактирования партнёров, интеграцией с базой данных,
валидацией ввода и диалоговыми уведомлениями.

* **Язык:** Python 3.10

* **UI:** PyQt5

* **СУБД:** PostgreSQL, драйвер `psycopg2`

* **Тестирование:** pytest

---

## Структура репозитория

```text
educational-practice_2026-09-21/
├── README.md ← этот файл
├── Makefile ← команды сборки и запуска
├── requirements.txt ← зависимости
├── config.example.py ← шаблон подключения к БД
├── 01_multiwindow-architecture/ ← многооконная архитектура
├── 02_partner-edit-form/ ← форма добавления/редактирования
├── 03_form-db-integration/ ← интеграция формы с БД
├── 04_exceptions-notifications/ ← обработка исключений и уведомления
└── app/ ← приложение
    ├── __main__.py ← точка входа
    ├── config.py ← параметры подключения (в .gitignore)
    ├── core/ ← бизнес-логика и валидация
    ├── db/ ← слой доступа к данным
    ├── ui/ ← интерфейс
    └── tests/ ← unit-тесты
```

---

## Разделы

### 01. Multiwindow Architecture

Два окна приложения, навигация между ними, заголовки.

- [`README.md`](./01_multiwindow-architecture/README.md)

### 02. Partner Edit Form

Форма добавления и редактирования партнёра, поля, подсказки, миграция
рейтинга.

- [`README.md`](./02_partner-edit-form/README.md)

### 03. Form–DB Integration

CRUD-операции, режимы добавления и редактирования, обновление списка.

- [`README.md`](./03_form-db-integration/README.md)

### 04. Exceptions and Notifications

Валидация ввода, три типа диалоговых окон, обработка ошибок СУБД.

- [`README.md`](./04_exceptions-notifications/README.md)

---

## Порядок запуска

1. Установить зависимости: `pip install -r requirements.txt`.
2. Создать `app/config.py` из `config.example.py`, заполнить параметры
   подключения к БД.
3. Запустить приложение: `make run`.

## Команды Makefile

```bash
make test    # unit-тесты бизнес-логики
make check   # проверка слоя интеграции с БД
make run     # запуск приложения
make clean   # очистка кэша
```

> Файл `app/config.py` добавлен в `.gitignore` и в репозиторий не попадает.