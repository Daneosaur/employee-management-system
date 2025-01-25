import sqlite3

conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

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

print("Employee table created!")

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


def add_employee():
    """Add a new employee to the database."""
    name = input("Enter employee name: ")
    birthday = (input("Enter employee date of birth  (YYYY-MM-DD): "))
    hire_date = (input("Enter date of hire  (YYYY-MM-DD): "))
    position = (input("Enter employee position: "))
    hourly_wage = int(input("Enter employee hourly rate: "))
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
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Birthday: {row[2]}, Hire Date: {row[3]}, "
                  f"Position: {row[4]}, Hourly Wage: ${row[5]:.2f}, Address: {row[6]}")
            print("\n")
        print()
    else:
        print("\nNo employees fount!\n")

def view_past_employees():
    """View all past employees."""
    cursor.execute('SELECT * FROM past_employees')
    rows = cursor.fetchall()
    if rows:
        print("\nPast employees in the database:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Birthday: {row[2]}, Hire Date: {row[3]}, "
                  f"Position: {row[4]}, Hourly Wage: ${row[5]:.2f}, Address: {row[6]}")
        print()
    else:
        print("\nNo past employees found!\n")



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
        print("9. Exit")
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
            print("Exiting the application. Goodbye!")
            break
        else: 
            print("Invalid choice. Please try again.\n")

main_menu()

conn.close()