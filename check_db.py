import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "students.db"
connection = sqlite3.connect(DB_PATH)

try:
        cursor = connection.cursor()

        # 1. Check for duplicate student codes.
        cursor.execute("""
                SELECT code, COUNT(*)
                FROM students
                GROUP BY code
                HAVING COUNT(*) > 1
        """)

        duplicates = cursor.fetchall()

        print("\n--- Duplicate Student Codes ---")

        if duplicates:
                for code, count in duplicates:
                        print(f"Code: {code}, Count: {count}")
        else:
                print("No duplicate student codes found.")

        # 2. Verify the unique index.
        cursor.execute("PRAGMA index_list('students')")
        indexes = cursor.fetchall()

        print("\n--- Student Indexes ---")

        for index in indexes:
                print(index)

        unique_index_exists = any(
                index[1] == "idx_students_code" and index[2] == 1
                for index in indexes
        )

        print("\n--- Unique Index Verification ---")

        if unique_index_exists:
                print("Verified: idx_students_code is UNIQUE.")
        else:
                print("Warning: UNIQUE index was not found.")

        # 3. Count students.
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]

        print(f"\nTotal students: {student_count}")

finally:
        connection.close()
