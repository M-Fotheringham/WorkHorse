import customtkinter as ctk
import pandas as pd
from workhorse.meta_functions.directory_selector import directory_selector

# from PIL import Image


class GuiFrame:
    def __init__(self, master, label, field_groups):
        """
        Initialize a master GUI with dynamic fields in tabs.

        Args:
            master: The root or parent window.
            label: The main title for the GUI.
            field_groups: A dictionary with field lists as values.
        """

        self.master = master
        self.field_groups = field_groups
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("green")

        self.entries = {}
        self.submissions = []  # Store submitted strings

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

        # Layout for tabs and results
        self.tab_frame = ctk.CTkFrame(master=self.frame)
        self.tab_frame.pack(side="left", padx=10, fill="y", expand=True)

        self.result_frame = ctk.CTkFrame(master=self.frame)
        self.result_frame.pack(side="right", padx=10, fill="y", expand=True)

        # Tabview
        self.tabview = ctk.CTkTabview(master=self.tab_frame)
        self.tabview.pack(fill="both", expand=True, pady=10)

        # Create tabs and populate fields
        for group_name, fields in self.field_groups.items():
            tab = self.tabview.add(group_name)
            self._create_fields(tab, fields)

        # Submit button
        self.submit_button = ctk.CTkButton(
            master=self.tab_frame, text="Submit", command=self.submit
        )
        self.submit_button.pack(pady=12, padx=10)

        self.reset_button = ctk.CTkButton(
            master=self.tab_frame, text="Clear", command=self.reset_form
        )
        self.reset_button.pack(pady=12, padx=10)

        # Result display
        self.result_label = ctk.CTkLabel(
            master=self.result_frame,
            text="Slide Names:\n",
            font=("Arial", 16),
            justify="left",
        )
        self.result_label.pack(pady=12, padx=10)

        # Export button
        self.export_button = ctk.CTkButton(
            master=self.result_frame, text="Export", command=self.export
        )
        self.export_button.pack(pady=12, padx=10)

        # Quit button
        self.quit_button = ctk.CTkButton(
            master=self.result_frame, text="Quit", command=self.quit
        )
        self.quit_button.pack(pady=24, padx=10)

        # Main Menu button
        self.menu_button = ctk.CTkButton(
            master=self.result_frame,
            text="Main Menu",
            command=self.menu,
            state="disabled",
        )
        self.menu_button.pack(pady=24, padx=10)

    def _create_fields(self, tab, fields):
        """Create input fields in the specified tab."""
        for field in fields:
            field_type = field.get("field_type", "entry")
            text = field.get("text", "Field")
            placeholder = field.get("placeholder", "")
            show = field.get("show", None)
            state = field.get("state", "normal")
            command = field.get("command", None)
            command = {"enable": self.enable, None: None}[command]

            if field_type == "entry":
                entry = ctk.CTkEntry(
                    master=tab,
                    placeholder_text=placeholder,
                    show=show,
                    state=state,
                )

            elif field_type == "combobox":
                entry = ctk.CTkComboBox(master=tab, values=placeholder)

            elif field_type == "checkbox":
                entry = ctk.CTkCheckBox(master=tab, text=text, command=command)

            else:
                entry = None

            if entry:
                entry.pack(pady=12, padx=10)
                self.entries[text] = entry

    def combine_inputs(self, data):
        """Combine input data into a single string."""

        if data["PrimCase"] != "":

            if data["IFOptional"] != "":
                print(data["IFOptional"])
                data["IFOptional"] = f"_{data['IFOptional']}"

            name = f"""{data["PrimCase"]}_{data["Primary Ab"]}_1to{data["Primary dilution factor"]}_{data["Polymer"]}_Opal{data["fluorophore"]}_1to{data["TSA dilution factor"]}_{data["Primscanner"]}{data["IFOptional"]}"""

        elif data["IHCCase"] != "":

            if data["IHCOptional"] != "":
                data["IHCOptional"] = f"_{data['IHCOptional']}"

            if data["IHC Titration?"]:
                name = f"""{data["IHCCase"]}_{data["IHC Primary Ab"]}_1to{data["IHC Primary dilution factor"]}_IHC_{data["IHCscanner"]}{data["IHCOptional"]}"""
            else:
                name = f"""{data["IHCCase"]}_{data["IHC Primary Ab"]}_IHC_{data["IHCscanner"]}{data["IHCOptional"]}"""

        elif data["MPCase"] != "":
            name = f"""{data["MPCase"]}_MP{data["Multiplex number"]}_{data["MPscanner"]}"""

        elif data["CSnumber"] != "":
            name = f"""CS{data["CSnumber"]}_{data["Slidenumber"]}"""

        elif data["OtherCase"] != "":
            name = f"""{data["OtherCase"]}_{data["section"]}_{data["condition"]}_{data["Otherscanner"]}"""

        else:
            name = None

        return name

    def reset_form(self):
        """Clear all input fields."""
        for entry in self.entries.values():
            if isinstance(entry, ctk.CTkEntry):
                entry.delete(0, ctk.END)

    def update_results(self):
        """Update the results display with all submissions."""
        submissions_text = "\n".join(self.submissions)
        self.result_label.configure(text=f"Slide Names:\n{submissions_text}")

    def submit(self):
        """Process inputs, update results, and reset the form."""
        # Collect data
        data = {text: entry.get() for text, entry in self.entries.items()}

        # Combine data into a string
        submission = self.combine_inputs(data)
        self.submissions.append(submission)

        # Update results display
        self.update_results()

        # # Reset the form
        # self.reset_form()

    def export(self):
        """Export slide names as xlsx."""
        # Get submissions as pandas df
        export = pd.DataFrame({"Slide_Name": self.submissions})

        d = directory_selector()

        export.to_excel(f"{d}/exported_names.xlsx")

    def enable(self):
        for widget in self.tab_frame.winfo_children():
            if isinstance(widget, ctk.CTkEntry):
                widget.configure(state="normal")

    def quit(self):
        self.master.destroy()

    def menu(self):
        self.result_frame.destroy()
        self.tab_frame.destroy()

        from workhorse.gui.main_menu import Menu

        app = Menu(master=self.master, label="Main Menu")
