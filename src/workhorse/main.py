import customtkinter as ctk
from workhorse.gui.main_menu import Menu

root = ctk.CTk()
root.title("WorkHorse")
app = Menu(master=root, label="Main Menu")
root.mainloop()
