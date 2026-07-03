"""Main menu and application shell for the WorkHorse PySide6 app."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from workhorse.filename_adjuster.filename_adjuster import filename_adjuster
from workhorse.project_archiver.project_archiver import project_archiver
from workhorse.slidename_generator.slidename_generator import slidename_generator


class WorkHorseWindow(QMainWindow):
    """Top-level Qt window that swaps between WorkHorse pages."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("WorkHorse")
        self.resize(900, 600)
        self.show_main_menu()

    def _set_page(self, page: QWidget) -> None:
        self.setCentralWidget(page)

    def show_main_menu(self) -> None:
        self._set_page(Menu(self, label="Main Menu"))

    def show_slide_name_generator(self) -> None:
        self._set_page(slidename_generator(self))

    def show_filename_adjuster(self) -> None:
        self._set_page(filename_adjuster(self))

    def show_project_archiver(self) -> None:
        self._set_page(project_archiver(self))


class Menu(QWidget):
    """Main menu page."""

    def __init__(self, window: WorkHorseWindow, label: str) -> None:
        super().__init__(window)
        self.window = window

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel(label)
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("pageTitle")
        title.setStyleSheet("font-size: 24px; font-weight: 600;")
        layout.addWidget(title)

        slide_button = QPushButton("Slide Name Generator")
        slide_button.clicked.connect(self.window.show_slide_name_generator)
        layout.addWidget(slide_button)

        rename_button = QPushButton("File Name Adjuster")
        rename_button.clicked.connect(self.window.show_filename_adjuster)
        layout.addWidget(rename_button)

        archive_button = QPushButton("File Archiver")
        archive_button.clicked.connect(self.window.show_project_archiver)
        archive_button.setEnabled(False)
        layout.addWidget(archive_button)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(QApplication.instance().quit)
        layout.addWidget(quit_button)
