"""Main menu and application shell for the WorkHorse PySide6 app."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPixmap
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


BACKGROUND_IMAGE = Path("docs") / "_figs" / "workhorse_logo.webp"


def find_project_file(relative_path: Path) -> Path | None:
    """Find a project-level file from source, editable installs, or packaged builds."""
    search_roots = [Path.cwd()]
    search_roots.extend(Path(__file__).resolve().parents)

    for root in search_roots:
        candidate = root / relative_path
        if candidate.exists():
            return candidate

    return None


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
        self._background_pixmap = self._load_background_pixmap()

        self.setObjectName("mainMenu")
        self.setStyleSheet(
            """
            QWidget#menuPanel {
                background-color: rgba(255, 255, 255, 215);
                border-radius: 18px;
            }

            QLabel#pageTitle {
                color: #202020;
                font-size: 24px;
                font-weight: 600;
            }

            QPushButton {
                font-size: 16px;
                min-width: 220px;
                padding: 8px 16px;
            }
            """
        )

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.setContentsMargins(24, 24, 24, 24)

        menu_panel = QWidget(self)
        menu_panel.setObjectName("menuPanel")
        menu_panel.setMaximumWidth(380)

        layout = QVBoxLayout(menu_panel)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(14)
        layout.setContentsMargins(32, 32, 32, 32)

        title = QLabel(label)
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("pageTitle")
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

        outer_layout.addWidget(menu_panel, alignment=Qt.AlignCenter)

    def _load_background_pixmap(self) -> QPixmap:
        """Load the main-menu background image."""
        image_path = find_project_file(BACKGROUND_IMAGE)
        if image_path is None:
            return QPixmap()

        return QPixmap(str(image_path))

    def paintEvent(self, event) -> None:  # noqa: N802
        """Paint a scalable background image behind the menu controls."""
        painter = QPainter(self)

        if self._background_pixmap.isNull():
            painter.fillRect(self.rect(), QColor("#f5f5f5"))
            return

        scaled_background = self._background_pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,
            Qt.SmoothTransformation,
        )
        x = (self.width() - scaled_background.width()) // 2
        y = (self.height() - scaled_background.height()) // 2
        painter.drawPixmap(x, y, scaled_background)
