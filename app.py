from pathlib import Path
import os
import sqlite3
from functools import wraps

from flask import Flask, render_template, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR.parent / "students.db"
print("Database path:", DB_PATH)

app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE = True,
    SESSION_COOKIE_SAMESITE="Lax",
)

if not app.secret_key:
    raise RuntimeError("FLASK_SECRET_KEY unidentified.")


def login_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return jsonify({"Message": "Please Log In First."}), 401

        return function(*args, **kwargs)

    return wrapper


def get_db():
    return sqlite3.connect(DB_PATH)


def get_students():
    connection = get_db()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, age, code, field
            FROM students
        """)

        return cursor.fetchall()

    finally:
        connection.close()


def init_db():
    connection = get_db()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age INTEGER,
                code TEXT,
                field TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        """)

        connection.commit()
    finally:
        connection.close()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"Message": "Invalid Request."}), 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"Message": "Username and password must be text."}), 400

    username = username.strip()

    if not username or not password:
        return jsonify({
            "Message": "Username and password are required."
        }), 400

    if len(password) < 8:
        return jsonify({
            "Message": "Password must be at least 8 characters."
        }), 400

    password_hash = generate_password_hash(password)
    connection = get_db()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))

        connection.commit()

        return jsonify({
            "Message": "User registered successfully."
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "Message": "Username Already Exists."
        }), 409

    finally:
        connection.close()


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"Message": "Invalid Request."}), 400

    username = data.get("username")
    password = data.get("password")

    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({"Message": "Invalid Request."}), 400

    username = username.strip()

    if not username or not password:
        return jsonify({
            "Message": "Username and password are required."
        }), 400

    connection = get_db()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT password_hash
            FROM users
            WHERE username = ?
        """, (username,))

        user = cursor.fetchone()

        if user is None or not check_password_hash(user[0], password):
            return jsonify({
                "Message": "Invalid Username or Password."
            }), 401

        session["username"] = username

        return jsonify({"Message": "Login Successful."}), 200

    finally:
        connection.close()


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    session.clear()

    return jsonify({"Message": "Logout Successful."}), 200


@app.route("/students", methods=["GET"])
@login_required
def get_students_routes():
    students = get_students()

    student_list = []

    for student in students:
        student_list.append({
            "id": student[0],
            "name": student[1],
            "age": student[2],
            "code": student[3],
            "field": student[4]
        })

    return jsonify(student_list), 200


@app.route("/students", methods=["POST"])
@login_required
def students():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"Message": "Invalid Request."}), 400

    name = data.get("name")
    age = data.get("age")
    code = data.get("code")
    field = data.get("field")

    if not all(isinstance(value, str) for value in (name, code, field)):
        return jsonify({
            "Message": "Name, code and field must be text."
        }), 400

    name = name.strip()
    code = code.strip()
    field = field.strip()

    if not name or not code or not field:
        return jsonify({
            "Message": "Name, code and field are required."
        }), 400

    if isinstance(age, bool) or not isinstance(age, int) or age < 0:
        return jsonify({
            "Message": "Age must be a non-negative integer."
        }), 400

    connection = get_db()

    try:
        cursor = connection.cursor()

        # Check for an existing student code.
        cursor.execute(
            "SELECT 1 FROM students WHERE code = ?",
            (code,)
        )

        if cursor.fetchone() is not None:
            return jsonify({
                "Message": "Student code already exists."
            }), 409

        cursor.execute("""
            INSERT INTO students (name, age, code, field)
            VALUES (?, ?, ?, ?)
        """, (name, age, code, field))

        connection.commit()

        return jsonify({
            "Message": f"Student {name} has been added.",
            "Name": name,
            "Age": age,
            "Code": code,
            "Field": field
        }), 201

    finally:
        connection.close()


@app.route("/students/<code>", methods=["PATCH"])
@login_required
def update_students(code):
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or "age" not in data:
        return jsonify({
            "Message": "A valid age is required."
        }), 400

    age = data["age"]

    if isinstance(age, bool) or not isinstance(age, int) or age < 0:
        return jsonify({
            "Message": "Age must be a non-negative integer."
        }), 400

    connection = get_db()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE students
            SET age = ?
            WHERE code = ?
        """, (age, code))

        if cursor.rowcount == 0:
            return jsonify({
                "Message": "Student not found."
            }), 404

        connection.commit()

        return jsonify({
            "Message": "Student Updated Successfully!"
        }), 200

    finally:
        connection.close()


@app.route("/students/<code>", methods=["DELETE"])
@login_required
def delete_students(code):
    connection = get_db()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM students
            WHERE code = ?
        """, (code,))

        if cursor.rowcount == 0:
            return jsonify({
                "Message": "Student not found."
            }), 404

        connection.commit()

        return jsonify({
            "Message": "Student Removed Successfully!"
        }), 200

    finally:
        connection.close()


init_db()

if __name__ == "__main__":
    app.run(debug=False)
