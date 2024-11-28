from workhorse.gui.rename_page import GuiFrameRename


def filename_adjuster(self):
    """Generates slide names based on user input"""

    # Main application
    app = GuiFrameRename(
        master=self.master, label="File Text Swap"
    )

    return app
