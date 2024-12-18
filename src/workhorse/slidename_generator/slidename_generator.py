import customtkinter as ctk
from workhorse.gui.name_structure import GuiFrame


def slidename_generator(self):
    """Generates slide names based on user input"""

    # Define the types of tabs
    field_groups = {
        "IF": [
            {"text": "PrimCase", "placeholder": "Case"},
            {"text": "Primary Ab", "placeholder": "Primary Ab"},
            {
                "text": "Primary dilution factor",
                "placeholder": "Primary dilution factor",
            },
            {"text": "Polymer", "placeholder": "Polymer"},
            {
                "field_type": "combobox",
                "text": "fluorophore",
                "placeholder": [
                    "",
                    "480",
                    "520",
                    "540",
                    "570",
                    "620",
                    "650",
                    "690",
                    "780",
                ],
            },
            {
                "text": "TSA dilution factor",
                "placeholder": "TSA dilution factor",
            },
            {
                "field_type": "combobox",
                "text": "Primscanner",
                "placeholder": ["", "QUKPolaris_1", "QUKPolaris_2"],
            },
            {"text": "IFOptional", "placeholder": "Optional condition"},
        ],
        "IHC": [
            {"text": "IHCCase", "placeholder": "Case"},
            {"text": "IHC Primary Ab", "placeholder": "Primary Ab"},
            {
                "field_type": "combobox",
                "text": "IHCscanner",
                "placeholder": ["", "QUKPolaris_1", "QUKPolaris_2"],
            },
            {
                "field_type": "checkbox",
                "text": "IHC Titration?",
                "command": "enable",
            },
            {
                "text": "IHC Primary dilution factor",
                "placeholder": "Primary dilution factor",
                "state": "normal",
            },
            {"text": "IHCOptional", "placeholder": "Optional condition"},
        ],
        "Multiplex Validation": [
            {"text": "MPCase", "placeholder": "Case"},
            {"text": "Multiplex number", "placeholder": "Multiplex number"},
            {
                "field_type": "combobox",
                "text": "MPscanner",
                "placeholder": ["", "QUKPolaris_1", "QUKPolaris_2"],
            },
        ],
        "Clinical_Specimen": [
            {"text": "CSnumber", "placeholder": "CS number"},
            {"text": "Slidenumber", "placeholder": "Slide number"},
        ],
        "Other": [
            {"text": "OtherCase", "placeholder": "Case"},
            {"text": "section", "placeholder": "Section number"},
            {"text": "Condition", "placeholder": "Condition"},
            {
                "field_type": "combobox",
                "text": "Otherscanner",
                "placeholder": ["", "QUKPolaris_1", "QUKPolaris_2"],
            },
        ],
    }

    # Main application
    app = GuiFrame(
        master=self.master, label="Slide Details", field_groups=field_groups
    )

    return app
