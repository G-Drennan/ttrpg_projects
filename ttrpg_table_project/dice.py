
import random as rand
import tkinter as tk
from tkinter import ttk


class CDice_gui_tk(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)

        self.title("Dice Roller")
        self.geometry("500x400")

        self.dice_lib = CDice_Roller_lib()

        self._build_gui()

    def _build_gui(self):

        # ------------------------
        # Add Dice Row
        # ------------------------
        top = ttk.Frame(self)
        top.pack(fill="x", padx=5, pady=5)

        ttk.Label(top, text="Expression:").pack(side="left")

        self.entry = ttk.Entry(top)
        self.entry.pack(side="left", fill="x", expand=True, padx=5)

        ttk.Button(
            top,
            text="Add",
            command=self.add_dice
        ).pack(side="left")

        # ------------------------
        # Scrollable Dice List
        # ------------------------
        middle = ttk.Frame(self)
        middle.pack(fill="both", expand=True, padx=5, pady=5)

        canvas = tk.Canvas(middle)
        scrollbar = ttk.Scrollbar(
            middle,
            orient="vertical",
            command=canvas.yview
        )

        self.roll_frame = ttk.Frame(canvas)

        self.roll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=self.roll_frame,
            anchor="nw"
        )

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # ------------------------
        # Result
        # ------------------------
        self.result_var = tk.StringVar(
            value="Result:"
        )

        ttk.Label(
            self,
            textvariable=self.result_var,
            font=("Arial", 14)
        ).pack(fill="x", padx=5, pady=5)

    def add_dice(self):

        expr = self.entry.get().strip()

        if not expr:
            return

        try:
            self.dice_lib.add(expr)

            row = ttk.Frame(self.roll_frame)
            row.pack(fill="x", pady=2)

            ttk.Label(
                row,
                text=expr
            ).pack(side="left", padx=5)

            ttk.Button(
                row,
                text="Roll",
                command=lambda e=expr:
                self.roll_dice(e)
            ).pack(side="right")

            self.entry.delete(0, tk.END)

        except Exception as err:
            self.result_var.set(f"Error: {err}")

    def roll_dice(self, expr):

        result = self.dice_lib.roll_die(expr)

        self.result_var.set(
            f"{expr} = {result}"
        )
    # |User Input| [add]
    #List of dice added 
        #Dice Text from user input [roll] result text

class CDice_Roller_lib:
    def __init__(self):
          self.dice_lib = {} #{str: CDice_Roller}
    
    def add(self, user_input): 
        self.dice_lib[user_input] = CDice_Roller(user_input)
    
    def roll_die(self,user_input): 
        return self.dice_lib[user_input].get_roll()

class CDice_Roller:
    def __init__(self, user_input: str):
        self.dX_pos = []
        self.dX_neg = []
        self.mod = 0
        self._syntax_translate(user_input)

    def _syntax_translate(self, user_input: str):
        #e.g 2d4 + 2d6 + 4 becomes rand(4) + rand(4) + rand(6) + rand(6) + 4
        #or 3d8 - 1d12 -2 becomes rand(8) + rand(8) - rand(12) + rand(8) -2 ect
        #extract the pos dice (self.dX_poss) e.g 3d8, the neg numbers (self.dX_neg) e.g -1d12 and the modifiers (self.mod) +2-3=-1 add togehter before assigned in self.mod
                # Remove spaces
                expr = user_input.replace(" ", "")
        
                # Ensure every term has a sign
                if expr[0] not in "+-":
                    expr = "+" + expr #enure the first term is + if no - is found
        
                # Split into signed terms [('+', '3d8'), ('-', '1d12'), ('-', '2')]
                terms = re.findall(r'([+-])([^+-]+)', expr)
                #print(terms)
                for sign, term in terms:
                    #print(sign, term)
                    # Dice term: NdX
                    dice_match = re.fullmatch(r'(\d+)d(\d+)', term, re.IGNORECASE)
        
                    if dice_match:
                        num_dice = int(dice_match.group(1))
                        dice_size = int(dice_match.group(2))
        
                        if sign == "+":
                            for n in range(num_dice): 
                                self.dX_pos.append(dice_size)
                        else:
                            for n in range(num_dice): 
                                self.dX_neg.append(dice_size)
        
                    # Modifier
                    elif term.isdigit():
                        value = int(term)
        
                        if sign == "+":
                            self.mod += value
                        else:
                            self.mod -= value
        
                    else:
                        raise ValueError(f"Invalid term: {term}") 

    def get_roll(self) -> str:
        result = 0 
        for die in self.dX_pos:
            result +=rand.randint(1,die)
        for die in self.dX_neg:
            result -=rand.randint(1,die)

        result += self.mod

        return str(result) 

import re

