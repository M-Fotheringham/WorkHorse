import customtkinter as ctk
from workhorse.slidename_generator.slidename_generator import (
    slidename_generator,
)
from workhorse.filename_adjuster.filename_adjuster import filename_adjuster
from workhorse.project_archiver.project_archiver import project_archiver

# from PIL import Image


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
        self.master.title("WorkHorse")

        self.entries = {}

        # Frame setup
        self.frame = ctk.CTkFrame(master=self.master)
        self.frame.pack(pady=20, padx=20, fill="both", expand=True)

        # # Load and resize background image
        # bg_image = ctk.CTkImage(light_image=Image.open("C:\\Users\\Michael\\
        # OneDrive - Queen's University\\Documents\\Projects\\Workflow_
        # Automation\\docs\\_figs\\workhorse_banner.png"), size=(600, 400)
        # )

        # background_label = ctk.CTkLabel(self.frame, image=bg_image, text="")
        # background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

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
        )
        self.quit_button.pack(pady=12, padx=10)

        # Project Archiver button
        self.archive_button = ctk.CTkButton(
            master=self.frame,
            text="File Archiver",
            command=self.archiving,
            state="disabled"
        )
        self.archive_button.pack(pady=12, padx=10)

        # Quit button
        self.quit_button = ctk.CTkButton(
            master=self.frame, text="Quit", command=self.quit
        )
        self.quit_button.pack(pady=24, padx=10)

    def naming(self):
        """Redirects to a window to collect parameters for slide naming."""
        self.frame.destroy()

        slidename_generator(self)

        return

    def renaming(self):
        """Redirects to a window to collect parameters for renaming."""
        self.frame.destroy()

        filename_adjuster(self)

        return

    def archiving(self):
        """Will redirect to a window to collect parameters for archiving."""
        self.frame.destroy()

        project_archiver(self)

        return

    def quit(self):
        self.master.destroy()
