import sqlite3
from flask import Flask,render_template,request,jsonify

app = Flask(__name__)

def get_db():
    connection = sqlite3.connect("students.db")
    return connection

def get_students():
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    return students 

@app.route("/students/<code>", methods=["DELETE"])
def delete_students(code):
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM students
    WHERE code = ?
    """,(code,))

    connection.commit()

    return jsonify({"Message":"Student Removed Successfully!"})

@app.route("/students/<code>", methods=["PATCH"])
def update_students(code):
    data = request.json
    age = data["age"]

    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET age = ?
        WHERE code = ?
    """,(age, code))

    print("Code:", repr(code))
    print("Age:", repr(age))
    print("Rows Count:", cursor.rowcount)

    connection.commit()

    return jsonify({"Message":"Student Updated Successfully!"})

@app.route("/students", methods=["GET"])
def get_students_routes():
    students = get_students()

    student_list = []

    for student in students:
        student_list.append({
            "id":student[0],
            "name":student[1],
            "age":student[2],
            "code":student[3],
            "field":student[4]
        })

    return jsonify(student_list)

def init_db():
    connection = get_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        code TEXT,
        field TEXT
        )
    """)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/students", methods=["POST"])
def students():
    try:
        data = request.json
        name = data["name"]
        age = data["age"]
        code = data["code"]
        field = data["field"]

        connection = get_db()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO students(name,age,code,field)
            VALUES (?,?,?,?)
        """,(name,age,code,field))

        connection.commit()

        print(name)
        print(age)
        print(code)
        print(field)


        return jsonify ({
            "Message":f"Student {name} has received!",
            "Name":name,
            "Age":age,
            "Code":code,
            "Field":field
        })
    except sqlite3.IntegrityError:
        return jsonify ({
            "Message": "Student code already exists."
        }),409

init_db()

app.run(debug=True)