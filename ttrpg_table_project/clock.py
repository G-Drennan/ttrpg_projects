import tkinter as tk
from tkinter import messagebox

class CClk:
    def __init__(self, count_total):
        self.count_total = count_total
        self.count_progress = 0

    def tick_up(self):
        if self.count_progress < self.count_total:
            self.count_progress+=1

    def tick_down(self):
            if self.count_progress > 0:
                self.count_progress-=1

    def reset(self):
        self.count_progress = 0

    def get_current_progress(self):
        return self.count_progress

    def get_max_progress(self):
        return self.count_total

    def iscomplete(self):
        if self.count_total == self.count_progress:
            return True
        else:
            return False

class CClk_Lib:
    def __init__(self):   
        self.clk_dict = {} #name: CClk
        self.current_clk = None

    def add_clk(self, name: str, count_total: int):
        print("Created: ", name)
        self.clk_dict[name] = CClk(count_total)

    def set_current_clk(self, name: str) -> CClk:
        self.current_clk = self.clk_dict[name]

    def remove_clk(self, name: str):
        self.clk_dict.pop(name)

    def tick(self, name: str, mode: str = 'u'):
        if mode == 'u':
            self.clk_dict[name].tick_up()
        elif mode == 'd':
            self.clk_dict[name].tick_down()

class CClk_Gui_tk:
    def __init__(self, parent: tk.Tk):
         
        self.root = tk.Toplevel(parent)
        self.root.title("Clock Tracker")
        self.clk_lib = CClk_Lib()
        self.core() 
        #self.root.mainloop()


    def core(self):
        

        create_frame = tk.Frame(self.root)
        create_frame.pack()

        tk.Label(create_frame, text="Name").pack(side="left")
        name_entry = tk.Entry(create_frame)
        name_entry.pack(side="left")

        tk.Label(create_frame, text="Count").pack(side="left")
        count_entry = tk.Entry(create_frame)
        count_entry.pack(side="left")

        tk.Button(create_frame, text="Create", command=lambda: self._add_clk(name_entry.get(),int(count_entry.get())) ).pack(side="left")

        

    def _add_clk(self, name: str, count_total: int):
        self.clk_lib.add_clk(name=name, count_total=count_total)
        self._display_clk(name=name)

    def _display_clk(self, name: str):
        self.clk_lib.set_current_clk(name)
        #clk_root = tk.Toplevel(self.root)
        #clk_root.title(name)
        curr_frame = tk.LabelFrame(
            self.root,
            text=name
        )
        curr_frame.pack( 
            fill="x",
            padx=5,
            pady=5
        )

        progress_label = tk.Label(
            curr_frame,
            text=self._progress_display()
        )
        progress_label.pack(anchor="w")

        btn_frame = tk.Frame(curr_frame)
        btn_frame.pack(fill="x")

        tk.Button(
            btn_frame,
            text="+1",
            command=lambda:
                self._tick(
                    name=name,
                    mode='u',
                    progress_label=progress_label
                )
        ).pack(side="left")

        tk.Button(
            btn_frame,
            text="-1",
            command=lambda:
                self._tick(
                    name=name,
                    mode='d',
                    progress_label=progress_label
                )
        ).pack(side="left")

        tk.Button(
            btn_frame,
            text="Reset",
            command=lambda:
                self._reset(progress_label)
        ).pack(side="left")

        tk.Button(
            btn_frame,
            text="Remove",
            command=lambda:
                self._remove(name, self.root)
        ).pack(side="left")

    def _remove(self, name: str, clk_root: tk.Tk):
        self.clk_lib.remove_clk(name=name)
        self._refresh_clks() 

    def _refresh_clks(self):


        # Returns a list of all widgets currently inside self.clk_frame
        for widget in self.root.winfo_children():
            # Permanently remove the widget from the GUI
            widget.destroy()

        #Reset the display
        self.core() 

        # Returns (name, clk) pairs from your library
        for name, clk in self.clk_lib.clk_dict.items():
            # Your function that draws one clock
            self._display_clk(name)

    def _tick(self, name: str, mode: str, progress_label: tk.Label):
        self.clk_lib.tick(name=name, mode = mode) 
        progress_label.config(text=self._progress_display())

    def _reset(self, progress_label):
        self.clk_lib.current_clk.reset()
        progress_label.config(text=self._progress_display())

    def _progress_display(self):
        count = self.clk_lib.current_clk.get_max_progress()
        progress = self.clk_lib.current_clk.get_current_progress()
        progressbar = ""
        for n in range(count):
            if n < progress:
                progressbar += "█"
            else:
                progressbar += "□"

        if self.clk_lib.current_clk.iscomplete():
            progressbar += " FULL" 
        return progressbar