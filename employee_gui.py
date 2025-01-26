import tkinter as tk 
from tkinter import ttk 
import sqlite3

conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

root = tk.Tk()
root.title("Employee Management System")

table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True)

columns = ("ID", "Name", "Birthday", "Hire Date", "Position", "Hourly Wage", "Address")
tree = ttk.Treeview(table_frame, columns=columns, show="headings")
tree.pack(fill=tk.BOTH, expand=True)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

def load_employees():
    for row in tree.get_children():
        tree.delete(row)

        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)

def add_employee():
    def save_employee():
        name = name_entry.get()
        birthday = birthday_entry.get()
        hire_date = hire_date_entry.get()
        position = position_entry.get()
        hourly_wage = wage_entry.get()
        address = address_entry.get()

        cursor.execute('''
        INSERT INTO employees (name, birthday, hire_date, position, hourly_wage, address)
        VALUES (?,?,?,?,?,?)
        ''', (name, birthday, hire_date, position, hourly_wage, address))
        conn.commit()

        load_employees()
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Employee")

    tk.Label(add_window, text="Name").grid(row=0, column=0)
    tk.Label(add_window, text="Birthday (YYYY-MM-DD)").grid(row=1, column=0)
    tk.Label(add_window, text="Hire Date (YYYY-MM-DD)").grid(row=2, column=0)
    tk.Label(add_window, text="Position").grid(row=3, column=0)
    tk.Label(add_window, text="Hourly Wage").grid(row=4, column=0)
    tk.Label(add_window, text="Address").grid(row=5, column=0)

    name_entry = tk.Entry(add_window)
    birthday_entry = tk.Entry(add_window)
    hire_date_entry = tk.Entry(add_window)
    position_entry = tk.Entry(add_window)
    wage_entry = tk.Entry(add_window)
    address_entry = tk.Entry(add_window)

    name_entry.grid(row=0, column=1)
    birthday_entry.grid(row=1, column=1)
    hire_date_entry.grid(row=2, column=1)
    position_entry.grid(row=3, column=1)
    wage_entry.grid(row=4, column=1)
    address_entry.grid(row=5, column=1)

    tk.Button(add_window, text="Save", command=save_employee).grid(row=6, column=1)

button_frame = tk.Frame(root)
button_frame.pack(fill=tk.X)

tk.Button(button_frame, text="Add Employee", command=add_employee).pack(side=tk.LEFT)
tk.Button(button_frame, text="Refresh", command=load_employees).pack(side=tk.LEFT)

# Load employees when the app starts
load_employees()

# Start the Tkinter main loop
root.mainloop()