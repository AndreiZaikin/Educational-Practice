"""Пути к ресурсам UI."""

from pathlib import Path

UI_DIR = Path(__file__).resolve().parent

STYLE_PATH = UI_DIR / "style.qss"
RESOURCES_DIR = UI_DIR / "resources"
ICON_PATH = RESOURCES_DIR / "icon.png"
LOGO_PATH = RESOURCES_DIR / "logo.png"