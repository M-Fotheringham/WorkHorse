import customtkinter as ctk
import os


def directory_selector():
    d = ctk.filedialog.askdirectory(
        title="Select a directory", initialdir=os.getcwd()
    )

    return d
