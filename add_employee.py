import sqlite3

conn = sqlite3.connect('employee.db')
cursor = conn.cursor()

cursor.execute('''
INSERT INTO employees (name, age, position, salary)
VALUES ('Hadrian Marlowe', 36, 'Fabricator', 30)
''')

conn.commit()
conn.close()

print("Employee added successfully!")

