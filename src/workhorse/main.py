"""Application entry point for WorkHorse."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from workhorse.gui.main_menu import WorkHorseWindow


def main() -> int:
    """Start the WorkHorse Qt application."""
    app = QApplication.instance() or QApplication(sys.argv)
    window = WorkHorseWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
