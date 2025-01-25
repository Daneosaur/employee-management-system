import sqlite3

conn = sqlite3.connect('employee.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS employees  (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Unique ID, auto-incremented
    name TEXT NOT NULL,                    -- Employee name
    age INTERGER,                          -- Employee age
    position TEXT,                         -- Job title
    salary REAL                            -- Salary
)
''')

conn.commit()
conn.close()

print("Database and table created successfully!")
