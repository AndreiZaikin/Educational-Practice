"""Точка входа приложения CRM."""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "03_ui"))
sys.path.append(str(Path(__file__).resolve().parent / "02_db-integration"))
sys.path.append(str(Path(__file__).resolve().parent / "01_business-logic"))

from main_window import main


if __name__ == "__main__":
    main()
