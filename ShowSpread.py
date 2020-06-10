from tkinter import ttk
import tkinter as tk
import CoronaTracker
import sqlite3

def run():
    """The main execution method for this module. Will create the GUI and then loop as the program runs,
        recreating the table displaying the spreads whenever a new location is selected from the dropdown."""
    root = tk.Tk()
    root.title('Virus Spreads as per Mutation Patterns')
    root.minsize(300, 300)

    # This section simply sets the scene and creates the dropdown menu. The dropdown menu is tied to the region_selected variable
    mainframe = tk.Frame(master=root, height=20, width=50)
    tableFrame = tk.Frame(master=mainframe)
    regions = get_regions()
    region_selected = tk.StringVar(master=root, name='reg')
    region_selected.set(regions[0])
    dropdown = tk.OptionMenu(mainframe, region_selected, *regions)

    # This function generates the table for a given area. It's a local method so that it can access the tableFrame
    def generate_table(area, dummy1, dummy2):
        nonlocal tableFrame
        tableFrame.destroy()
        tableFrame = tk.Frame(master=mainframe)
        tableFrame.grid(row=1, column=1)
        results = get_spreads(root.getvar(area))
        titles = ('Source Region', '# of Cases from Source')
        tab = Table(tableFrame, titles, results)

    # Bind updates of the dropdown to the creation of tables.
    region_selected.trace_add('write', generate_table)

    # Place the dropdown and the frame holding the table into their appropriate grid positions.
    mainframe.pack()
    dropdown.grid(row=0, column=1)
    tableFrame.grid(row=1, column=1)

    root.mainloop()

# The table class is used to generate a table in any given frame. Can be reused in other programs if needed.
class Table:
    """The table class creates the table representation of the SQL data. Can be generalized for use with other
        programs' data but would require small edits. This implementation assumes the number of columns is
        2 for formatting purposes, specifically the width necessary to properly display data."""
    def __init__(self, parent, titles, rows):
        for i in range(len(titles)):
            if i == 0:
                wid=30
            else:
                wid=8
            self.ele = tk.Entry(parent, fg='red', bg='gray', borderwidth=3, width=wid)
            self.ele.grid(row=0, column=i)
            self.ele.insert(tk.END, titles[i])
        self.populate_table(parent, rows)

    def populate_table(self, parent, rows):
        for i in range(len(rows)):
            for j in range(len(rows[0])):
                if j % 2 == 0:
                    wid = 30
                else:
                    wid = 8
                self.ele = tk.Entry(parent, borderwidth=2, width=wid)
                self.ele.grid(row=i+1, column=j)
                self.ele.insert(tk.END, rows[i][j])

# Simple method which obtains all the regions from the spreads table in the sequences database to be returned as a list
#? Gets used to populate the dropdown menu.
def get_regions():
    conn = sqlite3.connect('Sequences.db')
    curs = conn.cursor()
    curs.execute('''SELECT DISTINCT end_location FROM spreads;''')
    regions = []
    for region in curs.fetchall():
        regions.append(region[0])
    conn.close()
    return regions

# Method which finds the source region and number of cases from there through the SQL data for any given region.
def get_spreads(region):
    conn = sqlite3.connect('Sequences.db')
    curs = conn.cursor()
    curs.execute('''SELECT start_location, COUNT(rowid) FROM spreads
                    WHERE end_location=? GROUP BY start_location;''', (region,))
    results =[]
    while row := curs.fetchone():
        results.append((row[0], row[1]))

    conn.close()
    return tuple(results)

def generate_table(root, area):

    results = get_spreads(area)
    titles = ('Source Region', '# of Cases from Source')
    tab = Table(root, titles, results)

if __name__ == "__main__":
    run()