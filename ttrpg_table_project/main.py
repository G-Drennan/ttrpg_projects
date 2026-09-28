import tkinter as tk
from tkinter import ttk

from roll_table_gui_tk import CRoll_table_GUI_tk
from clock import CClk_Gui_tk
from dice import CDice_gui_tk


def open_dice():
    CDice_gui_tk(root)

def open_roll_table():
    CRoll_table_GUI_tk(root)

def open_clock():
    CClk_Gui_tk(root)


root = tk.Tk()

ttk.Button(root, text="Dice", command=open_dice).pack(padx=5, pady=5)
ttk.Button(root, text="Roll Table", command=open_roll_table).pack(padx=5, pady=5)
ttk.Button(root, text="Clock", command=open_clock).pack(padx=5, pady=5)

root.mainloop()