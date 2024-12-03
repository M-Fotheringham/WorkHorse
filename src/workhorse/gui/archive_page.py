import customtkinter as ctk
from workhorse.meta_functions.directory_selector import directory_selector
from workhorse.meta_functions.directory_copier import directory_copier


class GuiArchive:
    def __init__(self, master, label, fields):
        """
        Initialize a master GUI with dynamic fields in tabs.

        Args:
            master: The root or parent window.
            label: The main title for the GUI.
        """

        self.master = master
        self.fields = fields
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        # Frame setup
        self.frame = ctk.CTkFrame(master=self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Label
        self.label = ctk.CTkLabel(
            master=self.frame, text=label, font=("Arial", 24)
        )
        self.label.pack(pady=12, padx=10)

        # Store entries as dictionary
        self.entries = {}
        self.directory = {}

        # Create tabs and populate fields
        self._create_fields(self.fields)

        # Quit button
        self.quit_button = ctk.CTkButton(
            master=self.frame, text="Quit", command=self.quit
        )
        self.quit_button.pack(pady=24, padx=10)

        # Main Menu button
        self.menu_button = ctk.CTkButton(
            master=self.frame,
            text="Main Menu",
            command=self.menu,
            state="disabled",
        )
        self.menu_button.pack(pady=24, padx=10)

    def _create_fields(self, fields):
        """Create input fields in the specified tab."""

        for field in fields:
            field_type = field.get("field_type", "entry")
            text = field.get("text", "Field")
            placeholder = field.get("placeholder", "")
            show = field.get("show", None)
            state = field.get("state", "normal")

            if field_type == "entry":
                entry = ctk.CTkEntry(
                    master=self.frame,
                    placeholder_text=placeholder,
                    show=show,
                )

            elif field_type == "combobox":
                entry = ctk.CTkComboBox(master=self.frame, values=placeholder)

            elif field_type == "dir_button":
                entry = ctk.CTkButton(
                    master=self.frame,
                    text=text,
                    state=state,
                    command=lambda t=text: self.dir_select(t),
                )

            elif field_type == "submit_button":
                entry = ctk.CTkButton(
                    master=self.frame,
                    text=text,
                    state=state,
                    command=self.submit,
                )

            else:
                entry = None

            if entry:
                entry.pack(pady=12, padx=10)
                self.entries[text] = entry

    def dir_select(self, text):

        d = directory_selector()

        self.directory[text] = d

    def submit(self):
        local_dir = self.directory["Select LOCAL 'experiment' folder"]
        graid_dir = self.directory["Select GRAID 'data' folder"]
        teams_dir = self.directory["Select TEAMS 'data' folder"]

        # Another module

    def quit(self):
        self.master.destroy()

    def menu(self):
        self.frame.destroy()

        from workhorse.gui.main_menu import Menu

        app = Menu(master=self.master, label="Main Menu")


fields = [
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
