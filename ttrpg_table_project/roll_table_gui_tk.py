import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from roll_table_reader_base import CTableLibrary, CRollTable


class CGUI:
    DEV_PASSWORD = "W1z@rd5"

    def __init__(self):
        self.tl = CTableLibrary()
        self.password_entered = False

        self.root = tk.Tk()
        self.root.title("Roll Table Library")
        self.root.geometry("900x700")

        self._build_ui()
        self.refresh_tables()

        self.root.mainloop()

    def _build_ui(self):
        title = tk.Label(
            self.root,
            text="ROLL TABLE LIBRARY",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=10)

        tk.Label(search_frame, text="Search").pack(anchor="w")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_tables())

        tk.Entry(
            search_frame,
            textvariable=self.search_var
        ).pack(fill="x")

        tk.Label(search_frame, text="Dev Password").pack(anchor="w")

        self.password_var = tk.StringVar()

        pw_entry = tk.Entry(
            search_frame,
            textvariable=self.password_var,
            show="*"
        )
        pw_entry.pack(fill="x")
        pw_entry.bind("<KeyRelease>", self._password_changed)

        self.dev_frame = tk.LabelFrame(
            self.root,
            text="Developer Functions"
        )
        self.dev_frame.pack(fill="x", padx=10, pady=10)

        tk.Label(
            self.dev_frame,
            text="Table Name; Entry 1, Entry 2, Entry 3"
        ).pack(anchor="w")

        self.new_table_var = tk.StringVar()

        tk.Entry(
            self.dev_frame,
            textvariable=self.new_table_var
        ).pack(fill="x")

        tk.Button(
            self.dev_frame,
            text="Create New Table",
            command=self.create_table
        ).pack(pady=5)

        self.dev_frame.pack_forget()

        # Scrollable table area
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container)
        scrollbar = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.canvas.yview
        )

        self.table_frame = tk.Frame(self.canvas)

        self.table_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0),
            window=self.table_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Mouse wheel support
        self.canvas.bind_all(
            "<MouseWheel>",
            lambda event: self.canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )
        )

    def _password_changed(self, event=None):
        self.password_entered = (
            self.password_var.get() == self.DEV_PASSWORD
        )

        if self.password_entered:
            self.dev_frame.pack(fill="x", padx=10, pady=10)
        else:
            self.dev_frame.pack_forget()

        self.refresh_tables()

    def create_table(self):
        try:
            self.tl._create_new_table(
                txt=self.new_table_var.get()
            )
            self.new_table_var.set("")
            self.refresh_tables()

        except Exception as ex:
            messagebox.showerror(
                "Error",
                str(ex)
            )

    def refresh_tables(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        search_text = self.search_var.get()

        tables = self.tl.search_bar(search_text)

        for rt in tables:
            self._display_table(rt, tables)

    def _display_table(
        self,
        rt: CRollTable,
        filtered_tables
    ):
        frame = tk.LabelFrame(
            self.table_frame,
            text=rt.name
        )
        frame.pack(
            fill="x",
            padx=5,
            pady=5
        )

        info = (
            f"Tags: {rt.get_unpacked_tags()}    "
            f"Dice Type: {rt.rollExpression}"
        )

        tk.Label(
            frame,
            text=info
        ).pack(anchor="w")

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x")

        tk.Button(
            btn_frame,
            text="🎲 Roll",
            command=lambda r=rt: messagebox.showinfo(
                "Roll Result",
                str(r.roll_value())
            )
        ).pack(side="left")

        tk.Button(
            btn_frame,
            text="Display Table",
            command=lambda r=rt: self.show_table(r)
        ).pack(side="left")

        if self.password_entered:

            tk.Button(
                btn_frame,
                text="Delete Table",
                command=lambda r=rt: self.delete_table(
                    r,
                    filtered_tables
                )
            ).pack(side="left")

            tag_entry = tk.Entry(frame)
            tag_entry.pack(fill="x")

            tk.Button(
                frame,
                text="Modify Tags",
                command=lambda r=rt, e=tag_entry:
                    self.modify_tags(r, e.get())
            ).pack(anchor="w")

            tk.Button(
                frame,
                text="Remove Tags",
                command=lambda r=rt:
                    self.remove_tags(r)
            ).pack(anchor="w")

    def show_table(self, rt):
        window = tk.Toplevel(self.root)
        window.title(rt.name)

        text = tk.Text(window)
        text.pack(fill="both", expand=True)

        text.insert(
            "1.0",
            rt.markdown_render(task="output_txt")
        )

    def delete_table(
        self,
        rt,
        filtered_tables
    ):
        self.tl.del_table(
            rt.get_id(),
            filtered_tables
        )

        self.refresh_tables()

    def modify_tags(
        self,
        rt,
        tags
    ):
        self.tl.add_tags(
            tags,
            rt=rt
        )

        self.refresh_tables()

    def remove_tags(
        self,
        rt
    ):
        self.tl.remove_tags(rt=rt)
        self.refresh_tables()


def main():
    CGUI()


if __name__ == "__main__":
    main()