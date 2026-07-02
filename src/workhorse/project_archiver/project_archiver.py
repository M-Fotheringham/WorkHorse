"""Project archiver page factory."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from workhorse.gui.archive_page import GuiArchive


ARCHIVE_FIELDS = [
    {
        "field_type": "dir_button",
        "text": "Select LOCAL 'experiment' folder",
    },
    {
        "field_type": "dir_button",
        "text": "Select GRAID 'data' folder",
    },
    {
        "field_type": "dir_button",
        "text": "Select TEAMS 'data' folder",
    },
    {"field_type": "submit_button", "text": "Archive!"},
]


def project_archiver(window: QWidget) -> GuiArchive:
    """Create the project-archiver page."""
    return GuiArchive(window=window, label="File Archiver", fields=ARCHIVE_FIELDS)
