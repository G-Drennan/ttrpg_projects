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

class CClk_Gui:
    def __init__(self):
         
       
        self.clk_lib = CClk_Lib()


    def core(self):
        root = tk.Tk()
        root.title("Clock Tracker")

        create_frame = tk.Frame(root)
        create_frame.pack()

        tk.Label(create_frame, text="Name").pack(side="left")
        name_entry = tk.Entry(create_frame)
        name_entry.pack(side="left")

        tk.Label(create_frame, text="Count").pack(side="left")
        count_entry = tk.Entry(create_frame)
        count_entry.pack(side="left")

        tk.Button(create_frame, text="Create", command=lambda: self._add_clk(name_entry.get(),int(count_entry.get())) ).pack(side="left")

        root.mainloop()

    def _add_clk(self, name: str, count_total: int):
        self.clk_lib.add_clk(name=name, count_total=count_total)
        self._display_clk(name=name)

    def _display_clk(self, name: str):
        
        clk_root = tk.Tk()
        clk_root.title(name)
        curr_frame = tk.Frame(clk_root)
        curr_frame.pack()
       

        self.clk_lib.set_current_clk(name)
        tk.Label(curr_frame, text=name).pack(side="left")
        progress_label = tk.Label( curr_frame,text=self._progress_display())

        progress_label.pack(side="left")
        tk.Button(curr_frame, text="+1", command=lambda: self._tick(name=name, mode = 'u', progress_label = progress_label) ).pack(side="left")
        tk.Button(curr_frame, text="-1", command=lambda: self._tick(name=name, mode = 'd', progress_label = progress_label) ).pack(side="left")
        tk.Button(curr_frame, text="Reset", command=lambda: self._reset(progress_label=progress_label) ).pack(side="left")
        tk.Button(curr_frame, text="Remove", command=lambda: self._remove(name=name, clk_root = clk_root) ).pack(side="left")

    def _remove(self, name: str, clk_root: tk.Tk):
        self.clk_lib.remove_clk(name=name)
        clk_root.destroy() 

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

def main():
    go = CClk_Gui()
    go.core()

if __name__ == "__main__":
    main()