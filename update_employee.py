import sqlite3

conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

name = input("Enter employee name to update: ")
new_salary = float(input(f"Enter new salary for {name}: "))
new_position = input(f"Enter new position for {name}: ")

cursor.execute('''
UPDATE employees
set salary = ?, position = ?
WHERE name = ?
 ''', (new_salary, new_position, name))

conn.commit()
conn.close()

print("Employee salary updated successfully!")
