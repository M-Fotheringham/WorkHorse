"""Project archiver UI implemented with PySide6."""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from workhorse.meta_functions.directory_copier import directory_copier
from workhorse.meta_functions.directory_selector import directory_selector


class GuiArchive(QWidget):
    """Prototype page for collecting archiver directories."""

    def __init__(
        self,
        window: QWidget,
        label: str,
        fields: list[dict[str, Any]],
    ) -> None:
        super().__init__(window)
        self.window = window
        self.fields = fields
        self.directory: dict[str, str] = {}
        self.buttons: dict[str, QPushButton] = {}

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel(label)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: 600;")
        layout.addWidget(title)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)

        for field in fields:
            field_type = field.get("field_type", "entry")
            text = field.get("text", "Field")

            if field_type == "dir_button":
                button = QPushButton(text)
                button.clicked.connect(lambda checked=False, t=text: self.dir_select(t))
                self.buttons[text] = button
                layout.addWidget(button)
            elif field_type == "submit_button":
                button = QPushButton(text)
                button.clicked.connect(self.submit)
                layout.addWidget(button)

        layout.addWidget(self.status_label)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.window.close)
        layout.addWidget(quit_button)

        menu_button = QPushButton("Main Menu")
        menu_button.clicked.connect(self.window.show_main_menu)
        layout.addWidget(menu_button)

    def dir_select(self, text: str) -> None:
        """Select a directory for one archive role."""
        directory = directory_selector(parent=self)
        if not directory:
            return
        self.directory[text] = directory
        self.buttons[text].setText(f"✓ {text}")

    def submit(self) -> None:
        """Run the archiver backend when all directories have been selected."""
        required = [
            "Select LOCAL 'experiment' folder",
            "Select GRAID 'data' folder",
            "Select TEAMS 'data' folder",
        ]
        missing = [label for label in required if not self.directory.get(label)]
        if missing:
            QMessageBox.warning(
                self,
                "Missing directories",
                "Select all required directories before archiving.",
            )
            return

        directory_copier(
            self.directory[required[0]],
            self.directory[required[1]],
            self.directory[required[2]],
        )
        self.status_label.setText("Archive request submitted.")
