import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox
)
import sqlite3

# Database setup
DB_PATH = "employee.db"

def create_connection():
    return sqlite3.connect(DB_PATH)

class EmployeeManagementApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Employee Management System")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Buttons
        self.view_employees_button = QPushButton("View Employees")
        self.add_employee_button = QPushButton("Add Employee")
        self.delete_employee_button = QPushButton("Delete Employee")

        self.view_employees_button.clicked.connect(self.view_employees)
        self.add_employee_button.clicked.connect(self.open_add_employee_dialog)
        self.delete_employee_button.clicked.connect(self.open_delete_employee_dialog)

        layout.addWidget(self.view_employees_button)
        layout.addWidget(self.add_employee_button)
        layout.addWidget(self.delete_employee_button)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def view_employees(self):
        dialog = ViewEmployeesDialog()
        dialog.exec()

    def open_add_employee_dialog(self):
        dialog = AddEmployeeDialog()
        dialog.exec()

    def open_delete_employee_dialog(self):
        dialog = DeleteEmployeeDialog()
        dialog.exec()

class ViewEmployeesDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Employees")
        self.setGeometry(200, 200, 600, 400)

        layout = QVBoxLayout()

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_employees()

    def load_employees(self):
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT id, name, birthday, hire_date, position, hourly_wage, address FROM employees")
        employees = cursor.fetchall()

        self.table.setRowCount(len(employees))
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Birthday", "Hire Date", "Position", "Hourly Wage", "Address"])

        for row_idx, row_data in enumerate(employees):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        connection.close()

class AddEmployeeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Add Employee")
        self.setGeometry(200, 200, 400, 300)

        layout = QFormLayout()

        self.name_input = QLineEdit()
        self.birthday_input = QLineEdit()
        self.hire_date_input = QLineEdit()
        self.position_input = QLineEdit()
        self.hourly_wage_input = QLineEdit()
        self.address_input = QLineEdit()

        layout.addRow("Name:", self.name_input)
        layout.addRow("Birthday (YYYY-MM-DD):", self.birthday_input)
        layout.addRow("Hire Date (YYYY-MM-DD):", self.hire_date_input)
        layout.addRow("Position:", self.position_input)
        layout.addRow("Hourly Wage:", self.hourly_wage_input)
        layout.addRow("Address:", self.address_input)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.add_employee)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def add_employee(self):
        name = self.name_input.text()
        birthday = self.birthday_input.text()
        hire_date = self.hire_date_input.text()
        position = self.position_input.text()
        hourly_wage = self.hourly_wage_input.text()
        address = self.address_input.text()

        if not (name and birthday and hire_date and position and hourly_wage and address):
            QMessageBox.warning(self, "Input Error", "All fields are required!")
            return

        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("""
            INSERT INTO employees (name, birthday, hire_date, position, hourly_wage, address)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (name, birthday, hire_date, position, float(hourly_wage), address))

            connection.commit()
            QMessageBox.information(self, "Success", "Employee added successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            connection.close()

class DeleteEmployeeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Employee")
        self.setGeometry(200, 200, 400, 200)

        layout = QFormLayout()

        self.employee_id_input = QLineEdit()
        layout.addRow("Employee ID:", self.employee_id_input)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.delete_employee)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box)
        self.setLayout(layout)

    def delete_employee(self):
        employee_id = self.employee_id_input.text()

        if not employee_id:
            QMessageBox.warning(self, "Input Error", "Employee ID is required!")
            return

        try:
            connection = create_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
            employee = cursor.fetchone()

            if not employee:
                QMessageBox.warning(self, "Error", "No employee found with this ID!")
                return

            cursor.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            connection.commit()
            QMessageBox.information(self, "Success", "Employee deleted successfully!")
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")
        finally:
            connection.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = EmployeeManagementApp()
    main_window.show()
    sys.exit(app.exec())
