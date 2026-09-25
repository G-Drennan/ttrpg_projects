from roll_table_gui_tk import CGUI_tk
from clock import CClk_Gui
import tkinter as tk

def main():
    root = tk.Tk()
    root.withdraw() # Hide the root window

    CGUI_tk(root)
    CClk_Gui(root)

    root.mainloop()



if __name__ == "__main__":
    main()