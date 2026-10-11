import sqlite3

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_students_code
        ON students(code)
""")

connection.commit()

print("Students Are Now UNIQUE.")