import customtkinter as ctk
from workhorse.gui.archive_page import GuiArchive


def project_archiver(self):

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

    app = GuiArchive(master=self.master, label="File Archiver", fields=fields)
