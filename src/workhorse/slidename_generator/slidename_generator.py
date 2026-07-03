"""Slide-name generator page factory."""

from __future__ import annotations

from PySide6.QtWidgets import QWidget

from workhorse.gui.name_structure import GuiFrame
from workhorse.slidename_generator.panels import PANEL_SPECS


def slidename_generator(window: QWidget) -> GuiFrame:
    """Create the slide-name generator page."""
    return GuiFrame(window=window, label="Slide Details", panels=PANEL_SPECS)
