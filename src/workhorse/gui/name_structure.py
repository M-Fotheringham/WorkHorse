"""Slide-name generator UI implemented with PySide6."""

from __future__ import annotations

from typing import Any

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


class GuiFrame(QWidget):
    """Page for building and exporting slide names."""

    def __init__(
        self,
        window: QWidget,
        label: str,
        field_groups: dict[str, list[dict[str, Any]]],
    ) -> None:
        super().__init__(window)
        self.window = window
        self.field_groups = field_groups
        self.entries: dict[str, QWidget] = {}
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

        for group_name, fields in self.field_groups.items():
            tab = QWidget()
            tab.setLayout(QVBoxLayout())
            tab.layout().setAlignment(Qt.AlignTop)
            tab.layout().setContentsMargins(12, 12, 12, 12)
            self.tabview.addTab(tab, group_name)
            self._create_fields(tab, fields)

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.submit)
        tab_layout.addWidget(submit_button)

        reset_button = QPushButton("Clear")
        reset_button.clicked.connect(self.reset_form)
        tab_layout.addWidget(reset_button)

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

    def _create_fields(self, tab: QWidget, fields: list[dict[str, Any]]) -> None:
        """Create the input fields for one tab."""
        layout = tab.layout()
        assert layout is not None

        for field in fields:
            field_type = field.get("field_type", "entry")
            text = field.get("text", "Field")
            placeholder = field.get("placeholder", "")
            state = field.get("state", "normal")
            command = field.get("command")

            label = QLabel(text)
            layout.addWidget(label)

            if field_type == "entry":
                entry = QLineEdit()
                entry.setPlaceholderText(str(placeholder))
                entry.setEnabled(state != "disabled")
            elif field_type == "combobox":
                entry = QComboBox()
                entry.addItems([str(value) for value in placeholder])
                entry.setEnabled(state != "disabled")
            elif field_type == "checkbox":
                entry = QCheckBox(text)
                label.hide()
                entry.setEnabled(state != "disabled")
                if command == "enable":
                    entry.stateChanged.connect(self.enable)
            else:
                continue

            layout.addWidget(entry)
            self.entries[text] = entry

    @staticmethod
    def _widget_value(widget: QWidget) -> str | bool:
        if isinstance(widget, QLineEdit):
            return widget.text().strip()
        if isinstance(widget, QComboBox):
            return widget.currentText().strip()
        if isinstance(widget, QCheckBox):
            return widget.isChecked()
        return ""

    def combine_inputs(self, data: dict[str, str | bool]) -> str | None:
        """Combine input values into a WorkHorse slide name."""
        if data.get("PrimCase"):
            optional = str(data.get("IFOptional", ""))
            optional = f"_{optional}" if optional else ""
            return (
                f"{data['PrimCase']}_{data['Primary Ab']}_"
                f"1to{data['Primary dilution factor']}_{data['Polymer']}_"
                f"Opal{data['fluorophore']}_1to{data['TSA dilution factor']}_"
                f"{data['Primscanner']}{optional}"
            )

        if data.get("IHCCase"):
            optional = str(data.get("IHCOptional", ""))
            optional = f"_{optional}" if optional else ""
            if bool(data.get("IHC Titration?")):
                return (
                    f"{data['IHCCase']}_{data['IHC Primary Ab']}_"
                    f"1to{data['IHC Primary dilution factor']}_"
                    f"IHC_{data['IHCscanner']}{optional}"
                )
            return (
                f"{data['IHCCase']}_{data['IHC Primary Ab']}_"
                f"IHC_{data['IHCscanner']}{optional}"
            )

        if data.get("MPCase"):
            return (
                f"{data['MPCase']}_MP{data['Multiplex number']}_"
                f"{data['MPscanner']}"
            )

        if data.get("CSnumber"):
            return f"CS{data['CSnumber']}_{data['Slidenumber']}"

        if data.get("OtherCase"):
            return (
                f"{data['OtherCase']}_{data['section']}_"
                f"{data['Condition']}_{data['Otherscanner']}"
            )

        return None

    def reset_form(self) -> None:
        """Clear all inputs."""
        for entry in self.entries.values():
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
        """Build one slide name and add it to the results pane."""
        data = {text: self._widget_value(entry) for text, entry in self.entries.items()}
        submission = self.combine_inputs(data)

        if not submission:
            QMessageBox.warning(
                self,
                "No slide name generated",
                "Fill in the case field for one tab, then click Submit.",
            )
            return

        self.submissions.append(submission)
        self.update_results()

    def export(self) -> None:
        """Export submitted slide names to an Excel workbook."""
        if not self.submissions:
            QMessageBox.information(self, "Nothing to export", "No slide names have been submitted.")
            return

        directory = directory_selector(parent=self)
        if not directory:
            return

        output_path = f"{directory}/exported_names.xlsx"
        pd.DataFrame({"Slide_Name": self.submissions}).to_excel(output_path, index=False)
        QMessageBox.information(self, "Export complete", f"Saved to:\n{output_path}")

    def enable(self) -> None:
        """Enable/disable the IHC dilution field based on the titration checkbox."""
        checkbox = self.entries.get("IHC Titration?")
        dilution = self.entries.get("IHC Primary dilution factor")
        if isinstance(checkbox, QCheckBox) and isinstance(dilution, QLineEdit):
            dilution.setEnabled(checkbox.isChecked())
            if not checkbox.isChecked():
                dilution.clear()
