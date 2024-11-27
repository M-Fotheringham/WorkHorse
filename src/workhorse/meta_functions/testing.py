import customtkinter as ctk


class GuiFrame:
    def __init__(self, master, label, field_groups):
        """
        Initialize a master GUI with dynamic fields in tabs.

        Args:
            master: The root or parent window.
            label: The main title for the GUI.
            field_groups: A dictionary with group names as keys and field lists as values.
                Example:
                {
                    "Tab1": [{"text": "Field1", "placeholder": "Enter"}],
                    "Tab2": [{"text": "Field2", "placeholder": "Enter"}],
                }
        """

        self.master = master
        self.field_groups = field_groups
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        self.entries = {}

        # Frame setup
        self.frame = ctk.CTkFrame(master=self.master)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Label
        self.label = ctk.CTkLabel(
            master=self.frame, text=label, font=("Arial", 24)
        )
        self.label.pack(pady=12, padx=10)

        # Tabview
        self.tabview = ctk.CTkTabview(master=self.frame)
        self.tabview.pack(fill="both", expand=True, pady=10)

        # Create tabs and populate fields
        for group_name, fields in self.field_groups.items():
            tab = self.tabview.add(group_name)
            self._create_fields(tab, fields)

        # Submit button
        self.submit_button = ctk.CTkButton(
            master=self.frame, text="Submit", command=self.test
        )
        self.submit_button.pack(pady=12, padx=10)

    def _create_fields(self, tab, fields):
        """Create input fields in the specified tab."""
        for field in fields:
            field_type = field.get("field_type", "entry")
            text = field.get("text", "Field")
            placeholder = field.get("placeholder", "")
            show = field.get("show", None)

            if field_type == "entry":
                entry = ctk.CTkEntry(
                    master=tab,
                    placeholder_text=placeholder,
                    show=show,
                )

            elif field_type == "combobox":
                entry = ctk.CTkComboBox(master=tab, values=placeholder)

            else:
                entry = None

            if entry:
                entry.pack(pady=12, padx=10)
                self.entries[text] = entry

    def test(self):
        """Submit entries and close the window."""
        data = {text: entry.get() for text, entry in self.entries.items()}
        print("Collected Data:", data)  # Print data for demonstration
        self.master.destroy()


# Define the different field groups (tabs)
field_groups = {
    "Ab Titration": [
        {"text": "Case", "placeholder": "Case"},
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
        {"text": "TSA dilution factor", "placeholder": "TSA dilution factor"},
        {
            "field_type": "combobox",
            "text": "scanner",
            "placeholder": ["QUKPolaris_1", "QUKPolaris_2"],
        },
    ],
    "IHC": [
        {"text": "Case", "placeholder": "Case"},
        {"text": "Primary Ab", "placeholder": "Primary Ab"},
        {
            "field_type": "combobox",
            "text": "scanner",
            "placeholder": ["QUKPolaris_1", "QUKPolaris_2"],
        },
    ],
    "Multiplex": [
        {"text": "Case", "placeholder": "Case"},
        {"text": "Multiplex number", "placeholder": "Multiplex number"},
        {
            "field_type": "combobox",
            "text": "scanner",
            "placeholder": ["QUKPolaris_1", "QUKPolaris_2"],
        },
    ],
}

# Main application
root = ctk.CTk()
app = GuiFrame(master=root, label="Slide Details", field_groups=field_groups)
root.mainloop()
