
import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parent.parent / "students.db"

connection = sqlite3.connect(db_path)

try:
    cursor = connection.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
    """)
    print("Tables:", cursor.fetchall())

    cursor.execute("SELECT COUNT(*) FROM students")
    print("Students:", cursor.fetchone()[0])

    cursor.execute("SELECT COUNT(*) FROM users")
    print("Users:", cursor.fetchone()[0])

finally:
    connection.close()
