import customtkinter as ctk
import pandas as pd
from workhorse.meta_functions.directory_selector import directory_selector
from workhorse.meta_functions.name_replacer import name_replacer


class GuiFrameRename:
    def __init__(self, master, label):
        """
        Initialize a master GUI with dynamic fields in tabs.

        Args:
            master: The root or parent window.
            label: The main title for the GUI.
            field_groups: A dictionary with field lists as values.
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

        # Original text
        self.original_text = ctk.CTkEntry(
            master=self.frame, placeholder_text="Original Text"
        )
        self.original_text.pack(pady=12, padx=10)

        # New text
        self.new_text = ctk.CTkEntry(
            master=self.frame, placeholder_text="New Text"
        )
        self.new_text.pack(pady=12, padx=10)

        # Rename inside files checkbox
        self.inside_check = ctk.CTkCheckBox(
            master=self.frame, text="Rename inside files?"
        )
        self.inside_check.pack(pady=12, padx=10)

        # Swap button
        self.swap_button = ctk.CTkButton(
            master=self.frame, text="Swap", command=self.swap
        )
        self.swap_button.pack(pady=12, padx=10)

        # Swap confirmation label
        self.swapconf_label = ctk.CTkLabel(
            master=self.frame, text=""
        )
        self.swapconf_label.pack(pady=12, padx=10)

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

    def swap(self):
        d = directory_selector()

        name_replacer(
            d,
            self.original_text.get(),
            self.new_text.get(),
            self.inside_check.get(),
        )

        self.swapconf_label.configure(text="Swapped!")

    def quit(self):
        self.master.destroy()

    def menu(self):
        self.frame.destroy()
        self.frame.destroy()

        from workhorse.gui.main_menu import Menu

        app = Menu(master=self.master, label="Main Menu")
