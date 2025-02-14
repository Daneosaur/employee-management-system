#!/usr/bin/env python3

import sqlite3
import os
from datetime import datetime


# Set the absolut path for the database
db_path = os.path.join(os.path.dirname(__file__), 'employee.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print(f"Using database at: {db_path}")
# conn = sqlite3.connect('employee.db')
# cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birthday DATE NOT NULL,
    hire_date DATE NOT NULL,
    position TEXT NOT NULL,
    hourly_wage REAL NOT NULL,
    address TEXT NOT NULL
)
''')
conn.commit()


cursor.execute('''
CREATE TABLE IF NOT EXISTS sick_days (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    sick_date TEXT NOT NULL,
    reason TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
    )
    ''')
conn.commit()

cursor.execute(''' 
CREATE TABLE IF NOT EXISTS past_employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    birthday TEXT,
    start TEXT,
    position TEXT,
    wage REAL,
    address TEXT,
    separation_date TEXT
    )
    ''')
conn.commit()


cursor.execute('''
CREATE TABLE IF NOT EXISTS salary_changes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    change_date TEXT NOT NULL DEFAULT (DATE('now')),
    new_wage REAL NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
)
''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS bonuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER NOT NULL,
    bonus_date TEXT NOT NULL DEFAULT (DATE('now')),
    amount REAL NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES employees (id)
)
''')
conn.commit()

def add_employee():
    """Add a new employee to the database."""
    name = input("Enter employee name: ")
    birthday = (input("Enter employee date of birth  (YYYY-MM-DD): "))
    hire_date = (input("Enter date of hire  (YYYY-MM-DD): "))
    position = (input("Enter employee position: "))
    hourly_wage = float(input("Enter employee hourly rate: "))
    address = (input("Enter employee address: "))

    cursor.execute(''' 
    INSERT INTO employees (name, birthday, hire_date, position, hourly_wage, address)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, birthday, hire_date, position, hourly_wage, address))
    conn.commit()
    print("Employee {name} added successfully!\n")

def update_employee():
    """Update an existing employee's deatails."""
    name = input("Enter the name of the employee to update: ")
    print("What would you like to update? ")
    print("1. Name\n2. Birthday\n3. Hire Date\n4. Position\n5. Hourly Wage\n6. Address")
    
    choice = int(input("Enter your choice: "))

    field_map = {
        1: "name",
        2: "birthday",
        3: "hire_date",
        4: "position",
        5: "hourly_wage",
        6: "address"
    }
    if choice in field_map:
        new_value = input(f"Enter the new value for {field_map[choice]}: ")
        # Convert hourly_wage to float if updating that field
        if choice == 5:
            new_value = float(new_value)
        cursor.execute(f'''
        UPDATE employees
        SET {field_map[choice]} = ?
        WHERE name = ?
        ''', (new_value, name))
        conn.commit()
        print("Employee updated successfully!")
    else:
        print("Invalid choice!")

def log_sick_day():
    """Log a sick day for an employee."""
    employee_name = input("Enter the employee's name: ")

    cursor.execute('SELECT id FROM employees WHERE name = ?', (employee_name,))
    result = cursor.fetchone()

    if result:
        employee_id = result[0]
        sick_date = input("Emter the date of the sick day (YYYY-MM-DD): ")
        reason = input("Enter the reason given: ")

        cursor.execute('''
        INSERT INTO sick_days (employee_id, sick_date, reason)
        VALUES (?, ?, ?)
        ''', (employee_id, sick_date, reason))
        conn.commit()
        print("Sick day logged successfully!\n")
    else: 
        print(f"No employee found with the name {employee_name}.\n")

def view_sick_days():
    """View sick days for a specific employee."""
    employee_name = input("Enter the employee's name: ")

    cursor.execute('SELECT id FROM employees WHERE name = ?', (employee_name,))
    result = cursor.fetchone()

    if result:
        employee_id = result[0]
        cursor.execute('''
        SELECT sick_date, reason
        FROM sick_days
        WHERE employee_id = ?
        ORDER BY sick_date
        ''', (employee_id,))
        rows = cursor.fetchall()

        if rows:
            print(f"\nSick days for {employee_name}: ")
            for row in rows:
                print(f"Date: {row[0]}, Reason: {row[1]}")
            print()
        else: 
            print(f"\nNo sick days found for {employee_name}.\n")
    else:
        print(f"No employee found with the name {employee_name}.\n")

def total_sick_days_per_year():
    """Calculates total sick days for an employee in a given year."""
    employee_name = input("Enter the employee's name: ")
    year = input("Enter the year: ")

    cursor.execute('SELECT id FROM employees WHERE name = ?', (employee_name,))
    result = cursor.fetchone()

    if result:
        employee_id = result[0]
        cursor.execute('''
        SELECT COUNT(*)
        FROM sick_days
        WHERE employee_id = ? AND strftime('%Y', sick_date) = ?
        ''', (employee_id, year))
        total = cursor.fetchone()[0]

        print(f"\nTotal sick days for {employee_name} in {year}: {total}\n")
    else: 
        print(f"No employee found with the name {employee_name}.\n")


def delete_employee():
    """Delete an employee from the database and move them to the past_employees table."""
    name = input("Enter the name of the employee to delete: ")
    
    # Retrieve the employee details
    cursor.execute('SELECT * FROM employees WHERE name = ?', (name,))
    employee = cursor.fetchone()

    if employee:
        # Insert the employee's details into the past_employees table
        cursor.execute('''
        INSERT INTO past_employees (id, name, birthday, start, position, wage, address, separation_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, DATE('now'))
        ''', (employee[0], employee[1], employee[2], employee[3], employee[4], employee[5], employee[6]))
        conn.commit()

        # Delete the employee from the employees table
        cursor.execute('DELETE FROM employees WHERE id = ?', (employee[0],))
        conn.commit()
        print(f"Employee {name} has been moved to the Past Employees table and deleted from the Employees table.")
    else:
        print(f"Employee {name} not found.")

def view_employees():
    """View all employees."""
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()

    if rows:
        print("\nEmployees in the database:")
        print(f"{'ID':<5} {'Name':<20} {'Birthday':<12} {'Hire Date':<12} {'Position':<15} {'Wage':<8} {'Address':<30}")
        print("-" * 100)

        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<12} {row[3]:<12} {row[4]:<15} ${row[5]:<7.2f} {row[6]:<30}")
        print()
    else:
        print("\nNo employees found!\n")

def view_past_employees():
    """View all past employees."""
    cursor.execute('SELECT * FROM past_employees')
    rows = cursor.fetchall()
    if rows:
        print("\nEmployees in the database:")
        print(f"{'ID':<5} {'Name':<20} {'Birthday':<12} {'Hire Date':<12} {'Position':<15} {'Wage':<8} {'Address':<30}")
        print("-" * 100)

        for row in rows:
            print(f"{row[0]:<5} {row[1]:<20} {row[2]:<12} {row[3]:<12} {row[4]:<15} ${row[5]:<7.2f} {row[6]:<30}")
        print()
    else:
        print("\nNo employees found!\n")

def permanently_delete_employee():
    """Permanently delete an employee and associated records from the database, with confirmation."""
    name = input("Enter the name of the employee to be deleted: ")

    cursor.execute('SELECT * FROM employees WHERE name = ?', (name,))
    employee = cursor.fetchone()

    if employee:
        print(f"\nEmployee found: {name}")
        print("Are you sure wnat to permanently delete this record? This cannot be undone.")
        confirmation = input("Type 'YES' to confirm or anything else to cancel: ")

        if confirmation == "YES":
            employee_id = employee[0]

            cursor.execute('DELETE FROM sick_days WHERE employee_id = ?', (employee_id,))
            cursor.execute('DELETE FROM employees WHERE id = ?', (employee_id,))

            conn.commit()
            print(f"Employee {name} and all associated records have been permanently deleted.")
        else: 
            print("Deletion canceled.")
    else:
        print(f"Employee {name} not found.")

def add_salary_change():
    """Record a salary change for an employee."""
    name = input("Enter the employee's name: ")
    new_wage = float(input("Enter the new hourly wage: "))
    
    cursor.execute('SELECT id FROM employees WHERE name = ?', (name,))
    result = cursor.fetchone()
    
    if result:
        employee_id = result[0]
        cursor.execute('INSERT INTO salary_changes (employee_id, new_wage) VALUES (?, ?)', (employee_id, new_wage))
        cursor.execute('UPDATE employees SET hourly_wage = ? WHERE id = ?', (new_wage, employee_id))
        conn.commit()
        print(f"Salary updated to ${new_wage:.2f} for {name}.")
    else:
        print(f"No employee found with the name {name}.")

def add_bonus():
    """Record a bonus for an employee."""
    name = input("Enter the employee's name: ")
    bonus_amount = float(input("Enter the bonus amount: "))
    
    cursor.execute('SELECT id FROM employees WHERE name = ?', (name,))
    result = cursor.fetchone()
    
    if result:
        employee_id = result[0]
        cursor.execute('INSERT INTO bonuses (employee_id, amount) VALUES (?, ?)', (employee_id, bonus_amount))
        conn.commit()
        print(f"Bonus of ${bonus_amount:.2f} added for {name}.")
    else:
        print(f"No employee found with the name {name}.")
def fetch_employee_data(employee_id):
    cursor.execute("SELECT name, hourly_wage FROM employees WHERE id = ?", (employee_id,))
    employee = cursor.fetchone()
    
    cursor.execute("SELECT change_date, new_wage FROM salary_changes WHERE employee_id = ? ORDER BY change_date ASC", (employee_id,))
    salary_history = cursor.fetchall()
    
    cursor.execute("SELECT bonus_date, amount FROM bonuses WHERE employee_id = ? ORDER BY bonus_date ASC", (employee_id,))
    bonuses = cursor.fetchall()
    
    if employee:
        return {
            'name': employee[0],
            'hourly_rate': employee[1],
            'salary_history': salary_history,
            'bonuses': bonuses
        }
    return None

def generate_comp_report():
    """Generate and display an employee compensation report."""
    name = input("Enter the employee's name: ")
    cursor.execute("SELECT id FROM employees WHERE name = ?", (name,))
    result = cursor.fetchone()
    
    if not result:
        print(f"No employee found with the name {name}.")
        return
    
    employee_id = result[0]
    employee_data = fetch_employee_data(employee_id)
    
    report_date = datetime.today().strftime('%b %d, %Y')
    total_annual_pay = employee_data['hourly_rate'] * 2080
    total_bonus = sum(bonus[1] for bonus in employee_data['bonuses'])
    total_compensation = total_annual_pay + total_bonus
    
    print(f"""
Employee Compensation Review

{report_date}

{employee_data['name']}

Compensation History:
Date        New Hourly Wage
-----------------------------------
""")
    for change in employee_data['salary_history']:
        print(f"{change[0]}    ${change[1]:.2f}")
    
    print(f"""

Yearly Gross Pay: 
${employee_data['hourly_rate']:.2f}/hr x 2080 hours = ${total_annual_pay:,.2f}

Bonuses:
Date        Amount
-----------------------------------
""")
    for bonus in employee_data['bonuses']:
        print(f"{bonus[0]}    ${bonus[1]:,.2f}")
    
    print(f"""
Total Compensation: ${total_compensation:,.2f}
""")

def main_menu():
    """Main menu for application."""
    while True:
        print("\/\/\/\/\/ Welcome to the Centerline Studio Employee Management System! \/\/\/\/\/")
        print("1. Add Employee")
        print("2. Update Employee")
        print("3. Delete Employee")
        print("4. View Employees")
        print("5. View Past Employees")
        print("6. Log Sick Day")
        print("7. View Sick Days")
        print("8. Total Sick Days Per Year")
        print("9. Permanently delete employee record")
        print("10. Add Salary Change")
        print("11. Add Bonus")
        print("12. Generate Compensation Report")
        print("13. Exit")
        
        choice = int(input("Enter your choice: "))
        if choice == 1:
            add_employee()
        elif choice == 2:
            update_employee()
        elif choice == 3:
            delete_employee()
        elif choice == 4:
            view_employees()
        elif choice == 5:
            view_past_employees()
        elif choice == 6:
            log_sick_day()
        elif choice == 7:
            view_sick_days()
        elif choice == 8:
            total_sick_days_per_year()
        elif choice == 9:
            permanently_delete_employee()
        elif choice == 10:
            add_salary_change()
        elif choice == 11:
            add_bonus()
        elif choice == 12:
            generate_comp_report()
        elif choice == 13:
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")

main_menu()

conn.close()

