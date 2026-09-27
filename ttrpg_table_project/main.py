from roll_table_gui_tk import CGUI_tk
from clock import CClk_Gui_tk
from dice import CDice_gui_tk

import tkinter as tk
from tkinter import ttk

def main():
    '''ui = '3d8 + 2d6 - 1d12 -2'
    dr = CDice_Roller(ui)
    print(ui, '\n', dr.dX_pos, dr.dX_neg,  dr.mod) 
    
    print(dr.get_roll())'''
    
    root = tk.Tk()
    #root.withdraw() # Hide the root window
    CDice_gui_tk(root) 
    CGUI_tk(root)
    CClk_Gui_tk(root)

    root.mainloop()#'''

if __name__ == "__main__":
    main()