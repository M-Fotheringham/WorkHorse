"""Panel and field definitions for WorkHorse slide-name generation.

This module deliberately separates:
- the internal field id used by the program, and
- the display label shown to the user.

That makes it safe for multiple panels to display the same label, such as
"Case", without overwriting entries from another panel.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal, Mapping, Sequence


FieldType = Literal["entry", "combobox", "checkbox"]
FieldValue = str | bool
PanelValues = Mapping[str, FieldValue]
NameBuilder = Callable[[PanelValues], str | None]


@dataclass(frozen=True)
class FieldSpec:
    """Definition for one GUI input field."""

    id: str
    label: str
    placeholder: str | Sequence[str] = ""
    field_type: FieldType = "entry"
    enabled: bool = True
    enables: str | None = None
    required: bool = True


@dataclass(frozen=True)
class PanelSpec:
    """Definition for one slide-name-generator tab."""

    id: str
    title: str
    fields: tuple[FieldSpec, ...]
    build_name: NameBuilder


SCANNERS = ("", "QUKPolaris_1", "QUKPolaris_2")
FLUOROPHORES = ("", "480", "520", "540", "570", "620", "650", "690", "780")


def text(values: PanelValues, field_id: str) -> str:
    """Return a stripped string value from a panel value dictionary."""
    value = values.get(field_id, "")
    if isinstance(value, bool):
        return ""
    return value.strip()


def optional_suffix(values: PanelValues, field_id: str) -> str:
    """Return an underscore-prefixed optional suffix when the field is filled."""
    value = text(values, field_id)
    return f"_{value}" if value else ""


def build_if_name(values: PanelValues) -> str | None:
    """Build an immunofluorescence slide name."""
    case = text(values, "case")
    if not case:
        return None

    return (
        f"{case}_{text(values, 'primary_ab')}_"
        f"1to{text(values, 'primary_dilution')}_{text(values, 'polymer')}_"
        f"Opal{text(values, 'fluorophore')}_1to{text(values, 'tsa_dilution')}_"
        f"{text(values, 'scanner')}{optional_suffix(values, 'optional')}"
    )


def build_ihc_name(values: PanelValues) -> str | None:
    """Build an immunohistochemistry slide name."""
    case = text(values, "case")
    if not case:
        return None

    if bool(values.get("titration")):
        return (
            f"{case}_{text(values, 'primary_ab')}_"
            f"1to{text(values, 'primary_dilution')}_"
            f"IHC_{text(values, 'scanner')}{optional_suffix(values, 'optional')}"
        )

    return (
        f"{case}_{text(values, 'primary_ab')}_"
        f"IHC_{text(values, 'scanner')}{optional_suffix(values, 'optional')}"
    )


def build_multiplex_name(values: PanelValues) -> str | None:
    """Build a multiplex-validation slide name."""
    case = text(values, "case")
    if not case:
        return None

    return f"{case}_MP{text(values, 'multiplex_number')}_{text(values, 'scanner')}"


def build_clinical_specimen_name(values: PanelValues) -> str | None:
    """Build a clinical-specimen slide name."""
    cs_number = text(values, "cs_number")
    if not cs_number:
        return None

    return f"CS{cs_number}_{text(values, 'slide_number')}"


def build_other_name(values: PanelValues) -> str | None:
    """Build a generic slide name."""
    case = text(values, "case")
    if not case:
        return None

    return (
        f"{case}_{text(values, 'section')}_"
        f"{text(values, 'condition')}_{text(values, 'scanner')}"
    )


PANEL_SPECS: tuple[PanelSpec, ...] = (
    PanelSpec(
        id="if",
        title="IF",
        fields=(
            FieldSpec("case", "Case", "Case"),
            FieldSpec("primary_ab", "Primary Ab", "Primary Ab"),
            FieldSpec("primary_dilution", "Primary dilution factor", "Primary dilution factor"),
            FieldSpec("polymer", "Polymer", "Polymer"),
            FieldSpec("fluorophore", "Fluorophore", FLUOROPHORES, field_type="combobox"),
            FieldSpec("tsa_dilution", "TSA dilution factor", "TSA dilution factor"),
            FieldSpec("scanner", "Scanner", SCANNERS, field_type="combobox"),
            FieldSpec("optional", "Optional condition", "Optional condition", required=False),
        ),
        build_name=build_if_name,
    ),
    PanelSpec(
        id="ihc",
        title="IHC",
        fields=(
            FieldSpec("case", "Case", "Case"),
            FieldSpec("primary_ab", "Primary Ab", "Primary Ab"),
            FieldSpec("scanner", "Scanner", SCANNERS, field_type="combobox"),
            FieldSpec(
                "titration",
                "Titration?",
                field_type="checkbox",
                enables="primary_dilution",
            ),
            FieldSpec(
                "primary_dilution",
                "Primary dilution factor",
                "Primary dilution factor",
                enabled=False,
            ),
            FieldSpec("optional", "Optional condition", "Optional condition", required=False),
        ),
        build_name=build_ihc_name,
    ),
    PanelSpec(
        id="multiplex_validation",
        title="Multiplex Validation",
        fields=(
            FieldSpec("case", "Case", "Case"),
            FieldSpec("multiplex_number", "Multiplex number", "Multiplex number"),
            FieldSpec("scanner", "Scanner", SCANNERS, field_type="combobox"),
        ),
        build_name=build_multiplex_name,
    ),
    PanelSpec(
        id="clinical_specimen",
        title="Clinical Specimen",
        fields=(
            FieldSpec("cs_number", "CS number", "CS number"),
            FieldSpec("slide_number", "Slide number", "Slide number"),
        ),
        build_name=build_clinical_specimen_name,
    ),
    PanelSpec(
        id="other",
        title="Other",
        fields=(
            FieldSpec("case", "Case", "Case"),
            FieldSpec("section", "Section number", "Section number"),
            FieldSpec("condition", "Condition", "Condition"),
            FieldSpec("scanner", "Scanner", SCANNERS, field_type="combobox"),
        ),
        build_name=build_other_name,
    ),
)
