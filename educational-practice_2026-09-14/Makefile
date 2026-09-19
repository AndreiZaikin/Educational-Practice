PYTHON := $(shell command -v python 2>/dev/null || command -v python3)

.PHONY: help test check run clean

help:
	@echo "test  - запустить unit-тесты бизнес-логики"
	@echo "check - проверить слой интеграции с БД"
	@echo "run   - запустить приложение"
	@echo "clean - удалить кэш Python и pytest"

test:
	cd 01_business-logic && $(PYTHON) -m pytest -v test_discount.py

check:
	cd 02_db-integration && $(PYTHON) check_repository.py

run:
	$(PYTHON) app.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete