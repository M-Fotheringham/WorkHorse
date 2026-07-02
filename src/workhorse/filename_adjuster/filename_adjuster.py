"""Filename adjuster page factory."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from workhorse.gui.rename_page import GuiFrameRename


def filename_adjuster(window: QWidget) -> GuiFrameRename:
    """Create the filename-adjuster page."""
    return GuiFrameRename(window=window, label="File Text Swap")
