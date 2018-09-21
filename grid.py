#!/bin/python3
"""
Example Tkinter Grid
"""

import tkinter as tk


class Grid(tk.Frame):
    """A Tkinter grid"""

    def __init__(self, master, columns, *args, **kwargs):
        """
        Construct a new grid

        Parameters:
            master (tk.Tk|tk.Frame): Frame containing this widget
            columns (int): Amount of columns in the grid
        """
        super().__init__(master, *args, **kwargs)

        self._row = 0

        # configure the grid to fill the space
        for column in range(columns):
            tk.Grid.columnconfigure(self, column, weight=1)

    def add_row(self, values):
        """
        Append a new row of values to the grid

        Parameters:
            values (tuple<*>): Values stored in this row
        """
        for column, value in enumerate(values):
            label = tk.Label(self, text=value)
            label.grid(row=self._row, column=column, sticky=tk.W)

        self._row += 1


def main():
    root = tk.Tk()
    root.title("Tkinter Grid Example")
    grid = Grid(root, 6)
    grid.pack()

    grid.add_row(("", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"))
    grid.add_row(("08:00", "", "", "", "P10", "P15"))
    grid.add_row(("09:00", "", "P04", "", "P10", "P15"))
    grid.add_row(("10:00", "", "P04", "", "P11", "P16"))
    grid.add_row(("11:00", "", "P05", "P08", "P11", "P16"))
    grid.add_row(("12:00", "", "P05", "P08", "P12", ""))
    grid.add_row(("13:00", "P01", "", "P09", "P12", ""))
    grid.add_row(("14:00", "P01", "P06", "P09", "P13", ""))
    grid.add_row(("15:00", "P02", "P06", "", "P13", ""))
    grid.add_row(("16:00", "P02", "P07", "", "P14", ""))
    grid.add_row(("17:00", "P03", "P07", "", "P14", ""))
    grid.add_row(("18:00", "P03", "P17", "", "", ""))
    grid.add_row(("19:00", "", "P17", "", "", ""))

    root.mainloop()


if __name__ == "__main__":
    main()
