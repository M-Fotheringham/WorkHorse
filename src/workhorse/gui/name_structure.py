"""Slide-name generator UI implemented with PySide6."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from workhorse.meta_functions.directory_selector import directory_selector
from workhorse.slidename_generator.panels import FieldSpec, FieldValue, PanelSpec


class GuiFrame(QWidget):
    """Page for building and exporting slide names."""

    def __init__(
        self,
        window: QWidget,
        label: str,
        panels: tuple[PanelSpec, ...],
    ) -> None:
        super().__init__(window)
        self.window = window
        self.panel_specs = {panel.id: panel for panel in panels}
        self.panel_order = [panel.id for panel in panels]
        self.entries: dict[str, dict[str, QWidget]] = {}
        self.submissions: list[str] = []

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(24, 24, 24, 24)
        outer_layout.setSpacing(14)

        title = QLabel(label)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: 600;")
        outer_layout.addWidget(title)

        body_layout = QHBoxLayout()
        body_layout.setSpacing(18)
        outer_layout.addLayout(body_layout, stretch=1)

        self.tab_frame = QFrame()
        self.tab_frame.setFrameShape(QFrame.StyledPanel)
        tab_layout = QVBoxLayout(self.tab_frame)
        tab_layout.setContentsMargins(12, 12, 12, 12)
        body_layout.addWidget(self.tab_frame, stretch=2)

        self.result_frame = QFrame()
        self.result_frame.setFrameShape(QFrame.StyledPanel)
        result_layout = QVBoxLayout(self.result_frame)
        result_layout.setContentsMargins(12, 12, 12, 12)
        body_layout.addWidget(self.result_frame, stretch=1)

        self.tabview = QTabWidget()
        tab_layout.addWidget(self.tabview, stretch=1)

        for panel in panels:
            self.entries[panel.id] = {}
            tab = QWidget()
            tab_layout_inner = QVBoxLayout(tab)
            tab_layout_inner.setAlignment(Qt.AlignTop)
            tab_layout_inner.setContentsMargins(12, 12, 12, 12)
            self.tabview.addTab(tab, panel.title)
            self._create_fields(tab, panel)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)
        tab_layout.addWidget(submit_button)

        reset_button = QPushButton("Clear Current Tab")
        reset_button.clicked.connect(self.reset_current_form)
        tab_layout.addWidget(reset_button)

        reset_all_button = QPushButton("Clear All Tabs")
        reset_all_button.clicked.connect(self.reset_all_forms)
        tab_layout.addWidget(reset_all_button)

        result_title = QLabel("Slide Names")
        result_title.setStyleSheet("font-size: 16px; font-weight: 600;")
        result_layout.addWidget(result_title)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.result_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.result_label)
        result_layout.addWidget(scroll, stretch=1)

        export_button = QPushButton("Export")
        export_button.clicked.connect(self.export)
        result_layout.addWidget(export_button)

        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(self.window.close)
        result_layout.addWidget(quit_button)

        menu_button = QPushButton("Main Menu")
        menu_button.clicked.connect(self.window.show_main_menu)
        result_layout.addWidget(menu_button)

    def _create_fields(self, tab: QWidget, panel: PanelSpec) -> None:
        """Create the input fields for one tab."""
        layout = tab.layout()
        assert layout is not None

        for field in panel.fields:
            label = QLabel(field.label)
            layout.addWidget(label)

            entry = self._create_widget(field)
            if isinstance(entry, QCheckBox):
                label.hide()
                if field.enables:
                    entry.stateChanged.connect(
                        lambda _state=0, controller=entry, target_id=field.enables: (
                            self._sync_enabled_field(controller, panel.id, target_id)
                        )
                    )

            layout.addWidget(entry)
            self.entries[panel.id][field.id] = entry

    @staticmethod
    def _create_widget(field: FieldSpec) -> QWidget:
        """Create the Qt widget for one field spec."""
        if field.field_type == "entry":
            entry = QLineEdit()
            entry.setPlaceholderText(str(field.placeholder))
        elif field.field_type == "combobox":
            entry = QComboBox()
            if isinstance(field.placeholder, str):
                entry.addItem(field.placeholder)
            else:
                entry.addItems([str(value) for value in field.placeholder])
        elif field.field_type == "checkbox":
            entry = QCheckBox(field.label)
        else:  # pragma: no cover - Literal typing should prevent this.
            raise ValueError(f"Unsupported field type: {field.field_type}")

        entry.setEnabled(field.enabled)
        return entry

    def _current_panel_id(self) -> str:
        """Return the internal id for the currently selected tab."""
        return self.panel_order[self.tabview.currentIndex()]

    def _sync_enabled_field(
        self,
        controller: QCheckBox,
        panel_id: str,
        target_id: str,
    ) -> None:
        """Enable/disable a target field from a checkbox in the same panel."""
        target = self.entries[panel_id].get(target_id)

        if isinstance(target, QLineEdit):
            target.setEnabled(controller.isChecked())
            if not controller.isChecked():
                target.clear()

    @staticmethod
    def _widget_value(widget: QWidget) -> FieldValue:
        if isinstance(widget, QLineEdit):
            return widget.text().strip()
        if isinstance(widget, QComboBox):
            return widget.currentText().strip()
        if isinstance(widget, QCheckBox):
            return widget.isChecked()
        return ""

    def _panel_values(self, panel_id: str) -> dict[str, FieldValue]:
        """Return values from a single panel only."""
        return {
            field_id: self._widget_value(entry)
            for field_id, entry in self.entries[panel_id].items()
        }

    def _field_is_required(self, panel_id: str, field: FieldSpec) -> bool:
        """Return whether a field on one panel must be filled before submission."""
        if not field.required:
            return False

        # Checkboxes are controls, not text values the user must fill.
        if field.field_type == "checkbox":
            return False

        entry = self.entries[panel_id].get(field.id)

        # Disabled fields are not currently applicable. This keeps the IHC
        # primary dilution field optional until the titration checkbox enables it.
        if entry is not None and not entry.isEnabled():
            return False

        return True

    def _missing_required_fields(self, panel_id: str) -> list[str]:
        """Return blank required fields for the currently selected panel only."""
        panel = self.panel_specs[panel_id]
        missing: list[str] = []

        for field in panel.fields:
            if not self._field_is_required(panel_id, field):
                continue

            entry = self.entries[panel_id].get(field.id)
            if entry is None:
                continue

            value = self._widget_value(entry)
            if value == "":
                missing.append(field.label)

        return missing

    def reset_current_form(self) -> None:
        """Clear inputs on the currently selected tab."""
        self._reset_entries(self.entries[self._current_panel_id()])

    def reset_all_forms(self) -> None:
        """Clear inputs on every tab."""
        for panel_entries in self.entries.values():
            self._reset_entries(panel_entries)

    @staticmethod
    def _reset_entries(entries: dict[str, QWidget]) -> None:
        """Clear a dictionary of input widgets."""
        for entry in entries.values():
            if isinstance(entry, QLineEdit):
                entry.clear()
            elif isinstance(entry, QComboBox):
                entry.setCurrentIndex(0)
            elif isinstance(entry, QCheckBox):
                entry.setChecked(False)

    def update_results(self) -> None:
        """Refresh the submitted slide-name list."""
        self.result_label.setText("\n".join(self.submissions))

    def submit(self) -> None:
        """Build one slide name from the current tab and add it to the results pane."""
        panel_id = self._current_panel_id()
        missing = self._missing_required_fields(panel_id)

        if missing:
            QMessageBox.warning(
                self,
                "Missing required fields",
                "Please fill in the following fields before submitting:\n\n"
                + "\n".join(f"- {field}" for field in missing),
            )
            return

        panel = self.panel_specs[panel_id]
        submission = panel.build_name(self._panel_values(panel_id))

        if not submission:
            QMessageBox.warning(
                self,
                "No slide name generated",
                "Fill in the case field for the current tab, then click Submit.",
            )
            return

        self.submissions.append(submission)
        self.update_results()

    def export(self) -> None:
        """Export submitted slide names to an Excel workbook."""
        if not self.submissions:
            QMessageBox.information(
                self,
                "Nothing to export",
                "No slide names have been submitted.",
            )
            return

        directory = directory_selector(parent=self)
        if not directory:
            return

        output_path = Path(directory) / "exported_names.xlsx"
        pd.DataFrame({"Slide_Name": self.submissions}).to_excel(output_path, index=False)
        QMessageBox.information(self, "Export complete", f"Saved to:\n{output_path}")
