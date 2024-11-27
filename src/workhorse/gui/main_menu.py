import customtkinter as ctk
from workhorse.meta_functions.name_structure import GuiFrame


class Menu:
    def __init__(self, master, label):
        """
        Initialize a master GUI with dynamic fields in tabs.

        Args:
            master: The root or parent window.
            label: The main title for the GUI.
            fields: A dictionary with field lists as values.
        """

        self.master = master
        # self.fields = fields
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        self.entries = {}

        # Frame setup
        self.frame = ctk.CTkFrame(master=self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Label
        self.label = ctk.CTkLabel(
            master=self.frame, text=label, font=("Arial", 24)
        )
        self.label.pack(pady=12, padx=10)

        # Slide Name Generator button
        self.quit_button = ctk.CTkButton(
            master=self.frame, text="Slide Name Generator", command=self.naming
        )
        self.quit_button.pack(pady=12, padx=10)

        # File Name Adjuster button
        self.quit_button = ctk.CTkButton(
            master=self.frame,
            text="File Name Adjuster",
            command=self.renaming,
            state="disabled",
        )
        self.quit_button.pack(pady=12, padx=10)

        # Quit button
        self.quit_button = ctk.CTkButton(
            master=self.frame, text="Quit", command=self.quit
        )
        self.quit_button.pack(pady=24, padx=10)

    def naming(self):
        """Redirects to a window to collect parameters for slide naming."""
        self.frame.destroy()

        # Define the types of tabs
        field_groups = {
            "Ab Titration": [
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
                    "text": "scanner",
                    "placeholder": ["", "QUKPolaris_1", "QUKPolaris_2"],
                },
            ],
            "IHC": [
                {"text": "IHCCase", "placeholder": "Case"},
                {"text": "Primary Ab", "placeholder": "Primary Ab"},
                {
                    "field_type": "combobox",
                    "text": "scanner",
                    "placeholder": ["QUKPolaris_1", "QUKPolaris_2"],
                },
            ],
            "Multiplex": [
                {"text": "MPCase", "placeholder": "Case"},
                {"text": "Multiplex number", "placeholder": "Multiplex number"},
                {
                    "field_type": "combobox",
                    "text": "scanner",
                    "placeholder": ["QUKPolaris_1", "QUKPolaris_2"],
                },
            ],
            "Clinical_Specimen": [
                {"text": "CSnumber", "placeholder": "CS number"},
                {"text": "Slidenumber", "placeholder": "Slide number"},
            ],
        }

        # Main application
        app = GuiFrame(
            master=self.master, label="Slide Details", field_groups=field_groups
        )
        root.mainloop()

        return

    def renaming(self):
        """Will redirect to a window to collect parameters for renaming."""
        return

    def quit(self):
        self.master.destroy()


root = ctk.CTk()
app = Menu(master=root, label="Main Menu")
root.mainloop()
