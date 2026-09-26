PYTHON := $(shell command -v python 2>/dev/null || command -v python3)

.PHONY: help test check run clean

help:
	@echo "test  - запустить unit-тесты бизнес-логики"
	@echo "check - проверить слой интеграции с БД"
	@echo "run   - запустить приложение"
	@echo "clean - удалить кэш Python и pytest"

test:
	$(PYTHON) -m pytest -v app/tests/test_discount.py

check:
	$(PYTHON) -m app.db.check_repository

run:
	$(PYTHON) -m app

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete