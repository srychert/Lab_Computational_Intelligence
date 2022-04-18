import argparse
import sys
import tkinter as tk
import json
import re

class SimpleTableInput(tk.Frame):
    def __init__(self, parent, rows, columns):
        tk.Frame.__init__(self, parent)

        self._entry = {}
        self.rows = rows
        self.columns = columns

        # register a command to use for validation
        vcmd = (self.register(self._validate), "%P")

        # create the table of widgets
        for row in range(self.rows):
            for column in range(self.columns):
                index = (row, column)
                e = tk.Entry(self, validate="key", validatecommand=vcmd, width=3, font=('Arial 24'), justify="center")
                e.grid(row=row, column=column, stick="nsew", ipady=10)
                self._entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(self.columns):
            self.grid_columnconfigure(column, weight=1)
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(rows, weight=1)

    def get(self):
        '''Return a list of lists, containing the data in the table'''
        result = []
        for row in range(self.rows):
            current_row = []
            for column in range(self.columns):
                index = (row, column)
                if self._entry[index].get() == "":
                    current_row.append(0)
                else:
                    current_row.append(int(self._entry[index].get()))
            result.append(current_row)
        return result

    def _validate(self, P):
        '''Perform input validation.

        Allow only empty or a value that can be converted to a int
        '''
        if P.strip() == "":
            return True

        try:
            f = int(P)
        except ValueError:
            self.bell()
            return False
        return True

class Input(tk.Frame):
    def __init__(self, parent, width, length):
        tk.Frame.__init__(self, parent)
        self.table = SimpleTableInput(self, length, width)
        self.submit = tk.Button(self, text="Submit", command=self.on_submit)
        self.table.pack(side="top", fill="both", expand=True)
        self.submit.pack(side="bottom")

    def on_submit(self):
        print(self.table.get())
        puzzles = {}
        with open("puzzles.json", "r") as f:
            puzzles = json.load(f)

        key = int(max(puzzles.keys(), default=-1)) + 1
        puzzles[key] = self.table.get()
        json_str = json.dumps(puzzles)
        splited = re.split("]],", json_str)
        for i in range(len(splited)):
            if i != len(splited) - 1:
                splited[i] = splited[i] + "]],\n"
        final = "".join(splited)
        with open("puzzles.json", "w") as f:
            f.write(final)
        sys.exit(0)


root = tk.Tk()
parser = argparse.ArgumentParser(description='size for board')
parser.add_argument('--w', action="store", dest='w', default=4)
parser.add_argument('--h', action="store", dest='h', default=4)
args = parser.parse_args()
Input(root, int(args.w), int(args.h)).pack(side="top", fill="both", expand=True)
root.mainloop()