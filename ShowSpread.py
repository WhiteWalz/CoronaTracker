from tkinter import ttk
import tkinter as tk
import CoronaTracker
import sqlite3

def run():
    root = tk.Tk()
    root.title('Virus Spreads as per Mutation Patterns')
    root.minsize(300, 300)

    mainframe = tk.Frame(master=root, height=20, width=50)
    tableFrame = tk.Frame(master=mainframe)
    regions = get_regions()
    region_selected = tk.StringVar(master=root, name='reg')
    region_selected.set(regions[0])
    dropdown = tk.OptionMenu(mainframe, region_selected, *regions)

    def generate_table(area, dummy1, dummy2):
        nonlocal tableFrame
        tableFrame.destroy()
        tableFrame = tk.Frame(master=mainframe)
        tableFrame.grid(row=1, column=1)
        results = get_spreads(root.getvar(area))
        titles = ('Source Region', '# of Cases from Source')
        tab = Table(tableFrame, titles, results)

    region_selected.trace_add('write', generate_table)

    mainframe.pack()
    dropdown.grid(row=0, column=1)
    tableFrame.grid(row=1, column=1)

    root.mainloop()

class Table:

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

def get_regions():
    conn = sqlite3.connect('Sequences.db')
    curs = conn.cursor()
    curs.execute('''SELECT DISTINCT end_location FROM spreads;''')
    regions = []
    for region in curs.fetchall():
        regions.append(region[0])
    conn.close()
    return regions

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