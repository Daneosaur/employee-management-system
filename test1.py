import sqlite3

conn = sqlite3.connect("employee.db")
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Check the schema for each table
for table in tables:
    table_name = table[0]
    print(f"\nSchema for {table_name}:")
    cursor.execute(f"PRAGMA table_info({table_name});")
    schema = cursor.fetchall()
    for column in schema:
        print(column)

conn.close()