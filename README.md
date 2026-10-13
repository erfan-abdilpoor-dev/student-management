# Student Management System

A simple student management web application built with **Python, Flask, SQLite, HTML, CSS, and JavaScript**.

## Features

- Add new students
- View the student list
- Update student ages
- Delete students
- Prevent duplicate student codes
- Display success and error messages
- Store student records in an SQLite database

## Technologies Used

- Python
- Flask
- SQLite
- HTML
- CSS
- JavaScript
- Fetch API

## Project Structure

```text
Test8/
├── app.py
├── check_db.py
├── .gitignore
├── templates/
│   └── index.html
└── static/
    ├── Script.js
    └── style.css
```

## How to Run

1. Install Python.
2. Install Flask:

   ```bash
   pip install flask
   ```

3. Run the application:

   ```bash
   python app.py
   ```

4. Open your browser and visit:

   `http://127.0.0.1:5000`

## Database

The application uses SQLite to store student records. The database file is created locally when the application initializes.

## Purpose

This project was created as a practical learning project to develop skills in backend development, database management, REST APIs, and frontend integration.
