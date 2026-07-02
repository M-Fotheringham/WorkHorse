"""Filename text-swapper UI implemented with PySide6."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from workhorse.meta_functions.directory_selector import directory_selector
from workhorse.meta_functions.name_replacer import name_replacer


class GuiFrameRename(QWidget):
    """Page for replacing text in filenames and optionally inside text files."""

    def __init__(self, window: QWidget, label: str) -> None:
        super().__init__(window)
        self.window = window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel(label)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: 600;")
        layout.addWidget(title)

        self.original_text = QLineEdit()
        self.original_text.setPlaceholderText("Original Text")
        layout.addWidget(self.original_text)

        self.new_text = QLineEdit()
        self.new_text.setPlaceholderText("New Text")
        layout.addWidget(self.new_text)

        self.inside_check = QCheckBox("Rename inside .txt files?")
        layout.addWidget(self.inside_check)

        swap_button = QPushButton("Swap")
        swap_button.clicked.connect(self.swap)
        layout.addWidget(swap_button)

        self.swapconf_label = QLabel("")
        self.swapconf_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.swapconf_label)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.window.close)
        layout.addWidget(quit_button)

        menu_button = QPushButton("Main Menu")
        menu_button.clicked.connect(self.window.show_main_menu)
        layout.addWidget(menu_button)

    def swap(self) -> None:
        """Select a directory and perform the requested text swap."""
        original = self.original_text.text()
        new = self.new_text.text()

        if not original:
            QMessageBox.warning(self, "Missing text", "Enter text to replace first.")
            return

        directory = directory_selector(parent=self)
        if not directory:
            return

        try:
            count = name_replacer(
                directory,
                original,
                new,
                self.inside_check.isChecked(),
            )
        except Exception as exc:  # pragma: no cover - shown to user in GUI
            QMessageBox.critical(self, "Swap failed", str(exc))
            return

        self.swapconf_label.setText(f"Swapped {count} file name(s).")
