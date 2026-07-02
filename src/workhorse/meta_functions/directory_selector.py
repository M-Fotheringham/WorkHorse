"""Directory-selection helper for Qt widgets."""

from __future__ import annotations

import os

from PySide6.QtWidgets import QFileDialog, QWidget


def directory_selector(parent: QWidget | None = None) -> str:
    """Return a selected directory path, or an empty string if cancelled."""
    return QFileDialog.getExistingDirectory(
        parent,
        "Select a directory",
        os.getcwd(),
        QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
    )
